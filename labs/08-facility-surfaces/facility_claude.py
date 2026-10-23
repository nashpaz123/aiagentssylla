#!/usr/bin/env python3
"""
Lab 08B — Facility Surfaces: Anthropic agent → HTML card + Telegram send.

Domain: Atlas Facility Ops (building work orders) — NOT sales/quotes.
Same surface pattern as labs/08-agent-surfaces, different data + language.

Requires:
  ANTHROPIC_API_KEY + TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
  (copy .env.example → .env)

  python3 facility_claude.py reset
  python3 facility_claude.py chat --wo WO-HVAC --message "הכן כרטיס ושלח התראה"
  python3 facility_claude.py notify --wo WO-ELEV
  python3 facility_claude.py show
"""

from __future__ import annotations

import argparse
import html
import json
import os
import shutil
from pathlib import Path

import httpx
from anthropic import Anthropic

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "out"
SEED = DATA / "work_orders.seed.json"
ORDERS = DATA / "work_orders.json"
THREADS = DATA / "threads.json"
HTML_PATH = OUT / "work_order.html"
TG_PATH = OUT / "telegram.txt"
LAST_SEND = OUT / "last_send.json"

MODEL = os.environ.get("CREW_MODEL", os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"))
if "/" in MODEL:
    MODEL = MODEL.split("/", 1)[1]

TOOLS = [
    {
        "name": "get_work_order",
        "description": "Load one facility work order by wo_id from work_orders.json.",
        "input_schema": {
            "type": "object",
            "properties": {"wo_id": {"type": "string"}},
            "required": ["wo_id"],
        },
    },
    {
        "name": "render_html_card",
        "description": "Write a self-contained RTL Hebrew HTML work-order card to out/work_order.html.",
        "input_schema": {
            "type": "object",
            "properties": {
                "wo_id": {"type": "string"},
                "headline": {"type": "string"},
                "footer_note": {"type": "string"},
            },
            "required": ["wo_id"],
        },
    },
    {
        "name": "notify_telegram",
        "description": (
            "Build Hebrew Telegram alert for the work order, save out/telegram.txt, "
            "AND send it now via Bot API to TELEGRAM_CHAT_ID. Requires TELEGRAM_BOT_TOKEN."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "wo_id": {"type": "string"},
                "extra_line": {"type": "string"},
            },
            "required": ["wo_id"],
        },
    },
]

SYSTEM = """You are a Surface agent for Atlas Facility Ops (ניהול מתקנים / קריאות שירות בבניין).
Reply in Hebrew, short. This is NOT sales — no prices, seats, or customer quotes.

Pipeline for every briefing request:
1) get_work_order
2) render_html_card
3) notify_telegram  — ALWAYS send to the facility manager Telegram chat (env TELEGRAM_*)

Severity colors must match severity: open / sla_breach / blocked.
Never invent SLA or assignee. Do not claim sent=true unless notify_telegram returned sent=true.
"""


def load_dotenv_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def load(path: Path, default=None):
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def content_as_dicts(content) -> list | str:
    if isinstance(content, str):
        return content
    out: list = []
    for b in content:
        if isinstance(b, dict):
            out.append(b)
        elif hasattr(b, "model_dump"):
            out.append(b.model_dump(mode="json"))
        elif getattr(b, "type", None) == "text":
            out.append({"type": "text", "text": b.text})
        elif getattr(b, "type", None) == "tool_use":
            out.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.input})
        else:
            raise TypeError(f"cannot serialize content block: {type(b)}")
    return out


def ensure_data() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not ORDERS.exists():
        shutil.copy(SEED, ORDERS)


def telegram_env() -> tuple[str, str]:
    load_dotenv_file(ROOT / ".env")
    load_dotenv_file(ROOT.parent.parent / "demos" / "08-surface-opening" / ".env")
    load_dotenv_file(ROOT.parent.parent / "demos" / "08-facility-opening" / ".env")
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    return token, chat_id


def require_telegram() -> tuple[str, str]:
    token, chat_id = telegram_env()
    if not token or not chat_id:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required.\n"
            f"Copy {ROOT / '.env.example'} → {ROOT / '.env'} and fill your bot + chat id."
        )
    return token, chat_id


def accent_for(severity: str) -> str:
    return {"open": "#1b6f9e", "sla_breach": "#b00020", "blocked": "#b86e00"}.get(severity, "#334")


def build_html(wo: dict, wo_id: str, headline: str | None, footer: str | None) -> str:
    sev = wo.get("severity", "")
    accent = accent_for(sev)
    title = headline or f"קריאת שירות — {wo.get('title', wo_id)}"
    foot = footer or "התראה פנימית למנהל מתקנים · נשלחה גם לטלגרם"
    sla = wo.get("sla_hours_left")
    sla_txt = f"{sla} שעות" if sla is not None and sla >= 0 else f"חריגה · {abs(sla)} שעות"
    rows = [
        ("מס׳ קריאה", wo_id),
        ("אתר", wo.get("site")),
        ("קטגוריה", wo.get("category")),
        ("כותרת", wo.get("title")),
        ("עדיפות", wo.get("priority")),
        ("חומרה", wo.get("severity")),
        ("SLA", sla_txt),
        ("אחראי", wo.get("assignee")),
        ("נפתח ע״י", wo.get("opened_by")),
        ("נכס", wo.get("asset_id")),
        ("הערות", wo.get("notes")),
    ]
    trs = "".join(
        f"<tr><th>{html.escape(str(k))}</th><td>{html.escape(str(v))}</td></tr>" for k, v in rows
    )
    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)}</title>
<style>
  :root {{ --accent: {accent}; }}
  body {{ margin:0; font-family: "Segoe UI", "Heebo", Arial, sans-serif;
         background: linear-gradient(160deg, #10161c 0%, #1c2834 55%, #12181e 100%);
         color:#e8eef6; min-height:100vh; display:flex; align-items:center; justify-content:center; }}
  .card {{ width:min(580px, 92vw); background:#17212b; border:1px solid #2a3a4e;
           border-radius:18px; box-shadow:0 18px 50px rgba(0,0,0,.45); overflow:hidden; }}
  .banner {{ background:var(--accent); padding:18px 22px; font-weight:700; font-size:1.1rem; }}
  .body {{ padding:22px; }}
  table {{ width:100%; border-collapse:collapse; }}
  th, td {{ text-align:right; padding:10px 6px; border-bottom:1px solid #2a3a4e; }}
  th {{ color:#9bb0c7; font-weight:600; width:34%; }}
  .foot {{ padding:14px 22px 20px; color:#9bb0c7; font-size:.9rem; }}
  .pill {{ display:inline-block; margin-top:8px; padding:4px 10px; border-radius:999px;
           background:rgba(255,255,255,.12); font-size:.85rem; }}
</style>
</head>
<body>
  <article class="card">
    <header class="banner">{html.escape(title)}
      <div class="pill">{html.escape(str(sev))} · {html.escape(str(wo.get("priority")))}</div>
    </header>
    <div class="body"><table>{trs}</table></div>
    <footer class="foot">{html.escape(foot)}</footer>
  </article>
</body>
</html>
"""


def build_telegram(wo: dict, wo_id: str, extra: str | None) -> str:
    icon = {"open": "🔧", "sla_breach": "🚨", "blocked": "⏳"}.get(wo.get("severity", ""), "•")
    sla = wo.get("sla_hours_left")
    sla_txt = f"SLA נותר: {sla}ש׳" if sla is not None and sla >= 0 else f"חריגת SLA: {abs(sla)}ש׳"
    lines = [
        f"{icon} Atlas Facility · {wo_id}",
        f"{wo.get('title')}",
        f"{wo.get('site')} · {wo.get('category')} · נכס {wo.get('asset_id')}",
        f"חומרה: {wo.get('severity')} / עדיפות: {wo.get('priority')}",
        sla_txt,
        f"אחראי: {wo.get('assignee')} · נפתח: {wo.get('opened_by')}",
    ]
    if wo.get("notes"):
        lines.append(f"הערה: {wo.get('notes')}")
    if extra:
        lines.append(extra)
    lines.append("Internal facility alert · not a customer message")
    return "\n".join(lines) + "\n"


def send_telegram_text(text: str) -> dict:
    token, chat_id = require_telegram()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = httpx.post(url, json={"chat_id": chat_id, "text": text}, timeout=30.0)
    try:
        body = r.json()
    except Exception:
        body = {"raw": r.text[:300]}
    result = {"ok": r.is_success, "sent": r.is_success, "http": r.status_code, "body": body}
    save(LAST_SEND, result)
    return result


def run_tool(name: str, inp: dict) -> str:
    ensure_data()
    orders = load(ORDERS)

    if name == "get_work_order":
        wid = inp["wo_id"]
        print(f"TOOL -> get_work_order {wid}")
        if wid not in orders:
            return json.dumps({"error": "not_found"})
        return json.dumps(orders[wid], ensure_ascii=False)

    if name == "render_html_card":
        wid = inp["wo_id"]
        wo = orders[wid]
        doc = build_html(wo, wid, inp.get("headline"), inp.get("footer_note"))
        HTML_PATH.write_text(doc, encoding="utf-8")
        print(f"TOOL -> render_html_card {wid} -> {HTML_PATH}")
        return json.dumps({"ok": True, "path": str(HTML_PATH), "severity": wo.get("severity")})

    if name == "notify_telegram":
        wid = inp["wo_id"]
        wo = orders[wid]
        text = build_telegram(wo, wid, inp.get("extra_line"))
        TG_PATH.write_text(text, encoding="utf-8")
        print(f"TOOL -> notify_telegram {wid} (write + send)")
        try:
            result = send_telegram_text(text)
        except SystemExit as e:
            return json.dumps({"ok": False, "sent": False, "error": "missing_telegram_env", "hint": str(e)})
        print(f"TOOL -> notify_telegram sent={result.get('sent')} http={result.get('http')}")
        return json.dumps(
            {"ok": result["ok"], "sent": result["sent"], "path": str(TG_PATH), "http": result["http"]},
            ensure_ascii=False,
        )

    return json.dumps({"error": f"unknown tool {name}"})


def chat(wo_id: str, message: str, fresh: bool) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        load_dotenv_file(ROOT / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY missing")
    require_telegram()
    ensure_data()
    threads = load(THREADS)
    key = wo_id
    if fresh or key not in threads:
        threads[key] = []
    messages = threads[key]
    messages.append({"role": "user", "content": f"[wo_id={wo_id}] {message}"})

    client = Anthropic()
    while True:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        )
        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        assistant_content = content_as_dicts(resp.content)
        if resp.stop_reason == "tool_use" and tool_uses:
            messages.append({"role": "assistant", "content": assistant_content})
            results = []
            for tu in tool_uses:
                out = run_tool(tu.name, tu.input)
                results.append({"type": "tool_result", "tool_use_id": tu.id, "content": out})
            messages.append({"role": "user", "content": results})
            continue
        text = "".join(b.text for b in resp.content if hasattr(b, "text"))
        print(text)
        messages.append({"role": "assistant", "content": assistant_content})
        break

    threads[key] = messages
    save(THREADS, threads)
    if HTML_PATH.exists():
        print(f"HTML: file://{HTML_PATH.resolve()}")
    if TG_PATH.exists():
        print(f"TG copy: {TG_PATH}")


def notify(wo_id: str, extra: str | None = None) -> None:
    require_telegram()
    ensure_data()
    orders = load(ORDERS)
    if wo_id not in orders:
        raise SystemExit(f"unknown work order {wo_id}")
    wo = orders[wo_id]
    HTML_PATH.write_text(build_html(wo, wo_id, None, None), encoding="utf-8")
    text = build_telegram(wo, wo_id, extra)
    TG_PATH.write_text(text, encoding="utf-8")
    result = send_telegram_text(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"HTML: file://{HTML_PATH.resolve()}")
    if not result.get("sent"):
        raise SystemExit("Telegram send failed")


def reset() -> None:
    shutil.copy(SEED, ORDERS)
    for p in (THREADS, HTML_PATH, TG_PATH, LAST_SEND):
        if p.exists():
            p.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    print("reset OK")


def show() -> None:
    ensure_data()
    token, chat = telegram_env()
    print("=== telegram env ===")
    print(f"TELEGRAM_BOT_TOKEN: {'set' if token else 'MISSING'}")
    print(f"TELEGRAM_CHAT_ID: {chat if chat else 'MISSING'}")
    print("=== work_orders ===")
    print(json.dumps(load(ORDERS), ensure_ascii=False, indent=2))
    print("=== surfaces ===")
    print("html:", HTML_PATH if HTML_PATH.exists() else "(none)")
    print("telegram copy:", TG_PATH if TG_PATH.exists() else "(none)")
    if TG_PATH.exists():
        print("--- telegram.txt ---")
        print(TG_PATH.read_text(encoding="utf-8"))
    if LAST_SEND.exists():
        print("--- last_send.json ---")
        print(LAST_SEND.read_text(encoding="utf-8"))


def main() -> None:
    load_dotenv_file(ROOT / ".env")
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("reset")
    sub.add_parser("show")
    c = sub.add_parser("chat")
    c.add_argument("--wo", required=True, help="WO-HVAC | WO-ELEV | WO-ACCESS")
    c.add_argument("--message", required=True)
    c.add_argument("--fresh-thread", action="store_true")
    n = sub.add_parser("notify")
    n.add_argument("--wo", required=True)
    n.add_argument("--extra", default=None)
    args = p.parse_args()
    if args.cmd == "reset":
        reset()
    elif args.cmd == "show":
        show()
    elif args.cmd == "notify":
        notify(args.wo, args.extra)
    else:
        chat(args.wo, args.message, args.fresh_thread)


if __name__ == "__main__":
    main()
