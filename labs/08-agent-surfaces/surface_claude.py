#!/usr/bin/env python3
"""
Lab 08 — Agent Surfaces: Anthropic agent that renders a pretty HTML card
and optionally sends a Telegram message.

Requires:
  export ANTHROPIC_API_KEY=sk-ant-...
  # optional for real send:
  export TELEGRAM_BOT_TOKEN=...
  export TELEGRAM_CHAT_ID=...

  python3 surface_claude.py reset
  python3 surface_claude.py chat --lead L-SMB --message "הכן כרטיס HTML וטיוטת טלגרם"
  python3 surface_claude.py chat --lead L-ENT --message "הכן כרטיס — הדגש שממתין למנהל"
  python3 surface_claude.py chat --lead L-SMB --message "שלח את הסיכום לטלגרם"
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
        "name": "render_telegram_message",
        "description": "Write a short Hebrew Telegram message to out/telegram.txt (does NOT send).",
        "input_schema": {
            "type": "object",
            "properties": {
                "lead_id": {"type": "string"},
                "extra_line": {"type": "string"},
            },
            "required": ["lead_id"],
        },
    },
    {
        "name": "send_telegram",
        "description": "Send out/telegram.txt (or provided text) via Bot API. Needs TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Optional override; default = contents of out/telegram.txt",
                }
            },
        },
    },
]

SYSTEM = """You are a Surface agent for Nimbus Sales Ops. Reply in Hebrew, short.

You turn CRM quotes into user-facing surfaces:
1) get_quote
2) render_html_card (always for briefing requests)
3) render_telegram_message (always when asked for Telegram / סיכום)
4) send_telegram ONLY when the user explicitly asks to send AND tokens exist

Never invent prices. Color/status must match route: auto / hitl / blocked.
Draft ≠ Send: render_telegram_message does not send.
"""


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


def accent_for(route: str) -> str:
    return {"auto": "#1b7f4e", "hitl": "#b86e00", "blocked": "#b00020"}.get(route, "#334")


def build_html(q: dict, lead_id: str, headline: str | None, footer: str | None) -> str:
    route = q.get("route", "")
    accent = accent_for(route)
    title = headline or f"הצעת מחיר — {q.get('company', lead_id)}"
    foot = footer or "טיוטה פנימית — לא נשלח ללקוח אוטומטית"
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
    lines.append("Draft only · not sent to customer")
    return "\n".join(lines) + "\n"


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

    if name == "render_telegram_message":
        lid = inp["lead_id"]
        q = quotes[lid]
        text = build_telegram(q, lid, inp.get("extra_line"))
        TG_PATH.write_text(text, encoding="utf-8")
        print(f"TOOL -> render_telegram_message {lid} -> {TG_PATH}")
        return json.dumps({"ok": True, "path": str(TG_PATH), "preview": text[:200], "sent": False})

    if name == "send_telegram":
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
        text = (inp.get("text") or "").strip()
        if not text and TG_PATH.exists():
            text = TG_PATH.read_text(encoding="utf-8")
        if not token or not chat_id:
            print("TOOL -> send_telegram BLOCKED (missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID)")
            return json.dumps(
                {
                    "ok": False,
                    "sent": False,
                    "error": "missing_telegram_env",
                    "hint": "export TELEGRAM_BOT_TOKEN=... and TELEGRAM_CHAT_ID=...",
                }
            )
        if not text:
            return json.dumps({"ok": False, "sent": False, "error": "empty_text"})
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = httpx.post(url, json={"chat_id": chat_id, "text": text}, timeout=30.0)
        print(f"TOOL -> send_telegram status={r.status_code}")
        try:
            body = r.json()
        except Exception:
            body = {"raw": r.text[:300]}
        return json.dumps({"ok": r.is_success, "sent": r.is_success, "http": r.status_code, "body": body}, ensure_ascii=False)

    return json.dumps({"error": f"unknown tool {name}"})


def chat(lead_id: str, message: str, fresh: bool) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY missing")
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
        print(f"TG draft: {TG_PATH}")


def reset() -> None:
    shutil.copy(SEED, QUOTES)
    for p in (THREADS, HTML_PATH, TG_PATH):
        if p.exists():
            p.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    print("reset OK")


def show() -> None:
    ensure_data()
    print("=== quotes ===")
    print(json.dumps(load(QUOTES), ensure_ascii=False, indent=2))
    print("=== surfaces ===")
    print("html:", HTML_PATH if HTML_PATH.exists() else "(none)")
    print("telegram draft:", TG_PATH if TG_PATH.exists() else "(none)")
    if TG_PATH.exists():
        print("--- telegram.txt ---")
        print(TG_PATH.read_text(encoding="utf-8"))


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("reset")
    sub.add_parser("show")
    c = sub.add_parser("chat")
    c.add_argument("--lead", required=True)
    c.add_argument("--message", required=True)
    c.add_argument("--fresh-thread", action="store_true")
    args = p.parse_args()
    if args.cmd == "reset":
        reset()
    elif args.cmd == "show":
        show()
    else:
        chat(args.lead, args.message, args.fresh_thread)


if __name__ == "__main__":
    main()
