#!/usr/bin/env python3
"""
Lab 06 — חלק Anthropic: סוכן תמיכה עם כלים ל-Store (Memory) + היסטוריית שיחה (Working/Thread).

דורש:
  export ANTHROPIC_API_KEY=sk-ant-...
  pip install -r requirements.txt   # כולל anthropic

דוגמאות (תוצאות שונות בין הרצות):
  python3 memory_claude.py reset
  python3 memory_claude.py chat --customer C-99 --message "אני רוצה החזר על 99 שקל"
  python3 memory_claude.py chat --customer C-99 --message "מה הסטטוס של הבקשה שלי?"
  python3 memory_claude.py chat --customer C-101 --message "אני רוצה החזר על 101 שקל"
  python3 memory_claude.py chat --customer C-99 --message "מה הסטטוס?" --fresh-thread
  python3 memory_claude.py forget --customer C-99
  python3 memory_claude.py show
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from anthropic import Anthropic

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STORE_PATH = DATA / "profiles.json"
THREADS_PATH = DATA / "threads.json"
MODEL = os.environ.get("CREW_MODEL", os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"))
# allow CREW_MODEL like anthropic/claude-sonnet-4-5
if "/" in MODEL:
    MODEL = MODEL.split("/", 1)[1]

THRESHOLD = 100.0

TOOLS = [
    {
        "name": "get_profile",
        "description": "Read long-term Memory for a customer_id from the Store. Returns JSON or empty.",
        "input_schema": {
            "type": "object",
            "properties": {"customer_id": {"type": "string"}},
            "required": ["customer_id"],
        },
    },
    {
        "name": "save_profile",
        "description": "Write/update long-term Memory for a customer (amount, route auto|hitl, status).",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "amount": {"type": "number"},
                "route": {"type": "string", "enum": ["auto", "hitl"]},
                "status": {"type": "string", "enum": ["approved", "pending_human"]},
                "note": {"type": "string"},
            },
            "required": ["customer_id", "amount", "route", "status"],
        },
    },
    {
        "name": "forget_profile",
        "description": "Delete a customer from the Store (GDPR-style forget).",
        "input_schema": {
            "type": "object",
            "properties": {"customer_id": {"type": "string"}},
            "required": ["customer_id"],
        },
    },
]

SYSTEM = f"""You are ACME support. Hebrew replies, short.

Policy: amount <= {THRESHOLD:.0f} => route=auto, status=approved.
amount > {THRESHOLD:.0f} => route=hitl, status=pending_human.

Long-term Memory = Store tools only (get_profile / save_profile / forget_profile).
On a NEW refund request: parse amount, call save_profile, then confirm.
On STATUS: call get_profile first. If empty — you do not remember. Never invent.
Never store secrets/card numbers.
"""


def load_store() -> dict:
    if not STORE_PATH.exists():
        return {}
    return json.loads(STORE_PATH.read_text(encoding="utf-8"))


def save_store(data: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_threads() -> dict:
    if not THREADS_PATH.exists():
        return {}
    return json.loads(THREADS_PATH.read_text(encoding="utf-8"))


def save_threads(data: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    THREADS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def run_tool(name: str, inp: dict) -> str:
    store = load_store()
    if name == "get_profile":
        return json.dumps(store.get(inp["customer_id"], {}), ensure_ascii=False)
    if name == "save_profile":
        cid = inp["customer_id"]
        store[cid] = {
            "amount": inp["amount"],
            "route": inp["route"],
            "status": inp["status"],
            "note": inp.get("note", ""),
        }
        save_store(store)
        return json.dumps({"ok": True, "saved": store[cid]}, ensure_ascii=False)
    if name == "forget_profile":
        gone = store.pop(inp["customer_id"], None)
        save_store(store)
        return json.dumps({"ok": True, "deleted": gone}, ensure_ascii=False)
    return json.dumps({"error": f"unknown tool {name}"})


def chat(customer: str, message: str, fresh_thread: bool) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY is required (or use memory_lab.py / Claude Code demo without a raw key).")

    client = Anthropic()
    threads = load_threads()
    thread_id = f"thread-{customer}"
    if fresh_thread or thread_id not in threads:
        threads[thread_id] = []
    history = threads[thread_id]

    user_text = f"[customer_id={customer}] {message}"
    messages = list(history) + [{"role": "user", "content": user_text}]

    print(f"model={MODEL} thread={thread_id} fresh={fresh_thread or not history}")
    print(f"store={STORE_PATH}")

    for _ in range(8):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        )
        # Collect assistant content for next turn
        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "end_turn" or not tool_uses:
            # print text blocks
            for b in resp.content:
                if hasattr(b, "text") and b.type == "text":
                    print("ASSISTANT:", b.text)
            break

        results = []
        for tu in tool_uses:
            print(f"TOOL -> {tu.name}({json.dumps(tu.input, ensure_ascii=False)})")
            out = run_tool(tu.name, tu.input)
            print(f"TOOL <- {out}")
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": out,
                }
            )
        messages.append({"role": "user", "content": results})

    # Persist only plain text turns in thread log (simplified Checkpoint)
    # Keep last exchange as text for continuity
    plain = []
    for b in resp.content:
        if getattr(b, "type", None) == "text":
            plain.append(b.text)
    assistant_text = "\n".join(plain) or "(no text)"
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": assistant_text})
    threads[thread_id] = history[-12:]  # rolling buffer
    save_threads(threads)
    print(f"messages_in_thread={len(threads[thread_id])}")
    print("GOAL_COMPLETE: True")


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("chat")
    c.add_argument("--customer", required=True)
    c.add_argument("--message", required=True)
    c.add_argument("--fresh-thread", action="store_true", help="אפס היסטוריית שיחה (Checkpoint) — ה-Store נשאר")
    c.set_defaults(func=lambda a: chat(a.customer, a.message, a.fresh_thread))

    s = sub.add_parser("show")
    s.set_defaults(func=lambda a: print(json.dumps({"store": load_store(), "threads": {k: len(v) for k, v in load_threads().items()}}, ensure_ascii=False, indent=2)))

    f = sub.add_parser("forget")
    f.add_argument("--customer", required=True)
    f.set_defaults(func=lambda a: (print(run_tool("forget_profile", {"customer_id": a.customer}))))

    r = sub.add_parser("reset")
    def do_reset(_):
        for path in (STORE_PATH, THREADS_PATH):
            if path.exists():
                path.unlink()
        print("reset ok")
    r.set_defaults(func=do_reset)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
