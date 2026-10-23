#!/usr/bin/env python3
"""
Lab 08 — Agent Surfaces: Anthropic agent → HTML card + Telegram send (real).

Requires:
  export ANTHROPIC_API_KEY=sk-ant-...
  export TELEGRAM_BOT_TOKEN=...
  export TELEGRAM_CHAT_ID=...   # your personal chat / private group
  # or copy .env.example → .env

  python3 surface_claude.py reset
  python3 surface_claude.py chat --lead L-SMB --message "הכן כרטיס ושלח סיכום לטלגרם"
  python3 surface_claude.py notify --lead L-ENT   # HTML + send, no chat loop
  python3 surface_claude.py show
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
SEED = DATA / "quotes.seed.json"
QUOTES = DATA / "quotes.json"
THREADS = DATA / "threads.json"
HTML_PATH = OUT / "briefing.html"
TG_PATH = OUT / "telegram.txt"
LAST_SEND = OUT / "last_send.json"

MODEL = os.environ.get("CREW_MODEL", os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"))
if "/" in MODEL:
    MODEL = MODEL.split("/", 1)[1]

TOOLS = [
    {
        "name": "get_quote",
        "description": "Load one quote/lead by lead_id from quotes.json.",
        "input_schema": {
            "type": "object",
            "properties": {"lead_id": {"type": "string"}},
            "required": ["lead_id"],
        },
    },
    {
        "name": "render_html_card",
        "description": "Write a self-contained RTL Hebrew HTML briefing card to out/briefing.html.",
        "input_schema": {
            "type": "object",
            "properties": {
                "lead_id": {"type": "string"},
                "headline": {"type": "string"},
                "footer_note": {"type": "string"},
            },
            "required": ["lead_id"],
        },
    },
    {
        "name": "notify_telegram",
        "description": (
            "Build Hebrew Telegram text for the lead, save out/telegram.txt, "
            "AND send it now via Bot API to TELEGRAM_CHAT_ID. Requires TELEGRAM_BOT_TOKEN."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "lead_id": {"type": "string"},
                "extra_line": {"type": "string"},
            },
            "required": ["lead_id"],
        },
    },
]

SYSTEM = """You are a Surface agent for Nimbus Sales Ops. Reply in Hebrew, short.

Pipeline for every briefing request:
1) get_quote
2) render_html_card
3) notify_telegram  — ALWAYS send to the instructor/AE Telegram chat (env TELEGRAM_*)

This is an internal ops channel — sending is required, not optional.
Still never invent prices. Color/status must match route: auto / hitl / blocked.
Do not claim sent=true unless notify_telegram returned sent=true.
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
    if not QUOTES.exists():
        shutil.copy(SEED, QUOTES)


def telegram_env() -> tuple[str, str]:
    load_dotenv_file(ROOT / ".env")
    load_dotenv_file(ROOT.parent.parent / "demos" / "08-surface-opening" / ".env")
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


def accent_for(route: str) -> str:
    return {"auto": "#1b7f4e", "hitl": "#b86e00", "blocked": "#b00020"}.get(route, "#334")


def build_html(q: dict, lead_id: str, headline: str | None, footer: str | None) -> str:
    route = q.get("route", "")
    accent = accent_for(route)
    title = headline or f"הצעת מחיר — {q.get('company', lead_id)}"
    foot = footer or "סיכום פנימי ל-AE · נשלח גם לטלגרם הפנימי"
    rows = [
        ("ליד", lead_id),
        ("חברה", q.get("company")),
        ("SKU", q.get("sku")),
        ("מושבים", q.get("seats")),
        ("מחיר יחידה", f"{q.get('list_unit')} ₪"),
        ("הנחה", f"{q.get('discount_pct')}%"),
        ("סה״כ חודשי", f"{q.get('monthly_total')} ₪"),
        ("מסלול", q.get("route")),
        ("סטטוס", q.get("status")),
        ("AE", q.get("owner")),
        ("אימייל", q.get("email")),
        ("Upsell", "כן" if q.get("upsell") else "לא"),
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
         background: linear-gradient(160deg, #0f1419 0%, #1a2332 50%, #121820 100%);
         color:#e8eef6; min-height:100vh; display:flex; align-items:center; justify-content:center; }}
  .card {{ width:min(560px, 92vw); background:#182230; border:1px solid #2a3a4e;
           border-radius:18px; box-shadow:0 18px 50px rgba(0,0,0,.45); overflow:hidden; }}
  .banner {{ background:var(--accent); padding:18px 22px; font-weight:700; font-size:1.15rem; }}
  .body {{ padding:22px; }}
  table {{ width:100%; border-collapse:collapse; }}
  th, td {{ text-align:right; padding:10px 6px; border-bottom:1px solid #2a3a4e; }}
  th {{ color:#9bb0c7; font-weight:600; width:38%; }}
  .foot {{ padding:14px 22px 20px; color:#9bb0c7; font-size:.9rem; }}
  .pill {{ display:inline-block; margin-top:8px; padding:4px 10px; border-radius:999px;
           background:rgba(255,255,255,.12); font-size:.85rem; }}
</style>
</head>
<body>
  <article class="card">
    <header class="banner">{html.escape(title)}
      <div class="pill">{html.escape(str(route))} · {html.escape(str(q.get("status")))}</div>
    </header>
    <div class="body"><table>{trs}</table></div>
    <footer class="foot">{html.escape(foot)}</footer>
  </article>
</body>
</html>
"""


def build_telegram(q: dict, lead_id: str, extra: str | None) -> str:
    icon = {"auto": "✅", "hitl": "⏳", "blocked": "🚫"}.get(q.get("route", ""), "•")
    lines = [
        f"{icon} Nimbus · {q.get('company')} ({lead_id})",
        f"SKU {q.get('sku')} · {q.get('seats')} מושבים · הנחה {q.get('discount_pct')}%",
        f"סה״כ חודשי: {q.get('monthly_total')} ₪",
        f"מסלול: {q.get('route')} / {q.get('status')}",
        f"AE: {q.get('owner')}",
    ]
    if q.get("upsell"):
        lines.append("סוג: Upsell ללקוח קיים")
    if extra:
        lines.append(extra)
    lines.append("Internal ops alert · not the customer email")
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
    quotes = load(QUOTES)

    if name == "get_quote":
        lid = inp["lead_id"]
        print(f"TOOL -> get_quote {lid}")
        if lid not in quotes:
            return json.dumps({"error": "not_found"})
        return json.dumps(quotes[lid], ensure_ascii=False)

    if name == "render_html_card":
        lid = inp["lead_id"]
        q = quotes[lid]
        doc = build_html(q, lid, inp.get("headline"), inp.get("footer_note"))
        HTML_PATH.write_text(doc, encoding="utf-8")
        print(f"TOOL -> render_html_card {lid} -> {HTML_PATH}")
        return json.dumps({"ok": True, "path": str(HTML_PATH), "route": q.get("route")})

    if name == "notify_telegram":
        lid = inp["lead_id"]
        q = quotes[lid]
        text = build_telegram(q, lid, inp.get("extra_line"))
        TG_PATH.write_text(text, encoding="utf-8")
        print(f"TOOL -> notify_telegram {lid} (write + send)")
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


def chat(lead_id: str, message: str, fresh: bool) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        load_dotenv_file(ROOT / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY missing")
    require_telegram()
    ensure_data()
    threads = load(THREADS)
    key = lead_id
    if fresh or key not in threads:
        threads[key] = []
    messages = threads[key]
    messages.append({"role": "user", "content": f"[lead_id={lead_id}] {message}"})

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


def notify(lead_id: str, extra: str | None = None) -> None:
    """HTML + Telegram send without LLM — good for live demo / re-send."""
    require_telegram()
    ensure_data()
    quotes = load(QUOTES)
    if lead_id not in quotes:
        raise SystemExit(f"unknown lead {lead_id}")
    q = quotes[lead_id]
    HTML_PATH.write_text(build_html(q, lead_id, None, None), encoding="utf-8")
    text = build_telegram(q, lead_id, extra)
    TG_PATH.write_text(text, encoding="utf-8")
    result = send_telegram_text(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"HTML: file://{HTML_PATH.resolve()}")
    if not result.get("sent"):
        raise SystemExit("Telegram send failed")


def reset() -> None:
    shutil.copy(SEED, QUOTES)
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
    print("=== quotes ===")
    print(json.dumps(load(QUOTES), ensure_ascii=False, indent=2))
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
    c.add_argument("--lead", required=True)
    c.add_argument("--message", required=True)
    c.add_argument("--fresh-thread", action="store_true")
    n = sub.add_parser("notify")
    n.add_argument("--lead", required=True)
    n.add_argument("--extra", default=None)
    args = p.parse_args()
    if args.cmd == "reset":
        reset()
    elif args.cmd == "show":
        show()
    elif args.cmd == "notify":
        notify(args.lead, args.extra)
    else:
        chat(args.lead, args.message, args.fresh_thread)


if __name__ == "__main__":
    main()
