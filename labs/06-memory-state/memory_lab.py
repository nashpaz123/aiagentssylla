#!/usr/bin/env python3
"""
Lab 06 — Memory & State: Checkpointer (בתוך ריצה) + Store (בין ריצות).

בלי מפתח LLM. אפשר להריץ שוב עם לקוחות/סכומים/thread שונים ולראות תוצאות שונות.

פקודות:
  python3 memory_lab.py chat --customer C-99 --amount 99
  python3 memory_lab.py chat --customer C-99 --message "מה הסטטוס?"
  python3 memory_lab.py chat --customer C-101 --amount 101
  python3 memory_lab.py chat --customer C-101 --message "מה הסטטוס?" --thread other
  python3 memory_lab.py show
  python3 memory_lab.py forget --customer C-99
  python3 memory_lab.py reset
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STORE_PATH = DATA / "profiles.json"
CKPT_PATH = DATA / "checkpoints.sqlite"
THRESHOLD = 100.0

# Checkpointer: InMemorySaver by default; --persist uses a tiny sqlite table we manage
# for demo clarity (LangGraph SqliteSaver needs langgraph-checkpoint-sqlite; we keep deps light).


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    customer_id: str
    amount: float | None
    route: str | None
    reply: str


def load_store() -> dict:
    if not STORE_PATH.exists():
        return {}
    return json.loads(STORE_PATH.read_text(encoding="utf-8"))


def save_store(data: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def lookup_profile(state: AgentState) -> dict:
    store = load_store()
    profile = store.get(state["customer_id"])
    msgs = []
    if profile:
        msgs.append(
            {
                "role": "system",
                "content": (
                    f"KNOWN_PROFILE amount={profile['amount']} "
                    f"route={profile['route']} status={profile['status']}"
                ),
            }
        )
    return {"messages": msgs}


def decide(state: AgentState) -> dict:
    """תור חדש עם amount → כותב ל-Store. תור סטטוס → קורא מ-Store."""
    store = load_store()
    cid = state["customer_id"]
    amount = state.get("amount")
    last_user = ""
    for m in reversed(state["messages"]):
        role = m.get("role") if isinstance(m, dict) else getattr(m, "type", None)
        content = m.get("content") if isinstance(m, dict) else getattr(m, "content", "")
        if role in ("user", "human"):
            last_user = content
            break

    wants_status = amount is None or "סטטוס" in last_user or "status" in last_user.lower()

    if wants_status and amount is None:
        profile = store.get(cid)
        if not profile:
            reply = f"אין לי זיכרון על {cid}. פתחו בקשת החזר עם --amount."
            route = "unknown"
        else:
            reply = (
                f"זוכר את {cid}: סכום={profile['amount']}, "
                f"מסלול={profile['route']}, סטטוס={profile['status']}."
            )
            route = profile["route"]
        return {
            "route": route,
            "reply": reply,
            "messages": [{"role": "assistant", "content": reply}],
        }

    assert amount is not None
    route = "auto" if amount <= THRESHOLD else "hitl"
    status = "approved" if route == "auto" else "pending_human"
    store[cid] = {"amount": amount, "route": route, "status": status}
    save_store(store)
    if route == "auto":
        reply = f"בקשה על {amount:.0f} אושרה אוטומטית (≤{THRESHOLD:.0f}). נשמר ב-Store."
    else:
        reply = f"בקשה על {amount:.0f} ממתינה לנציג (>{THRESHOLD:.0f}). נשמר ב-Store כ-{status}."
    return {
        "route": route,
        "reply": reply,
        "messages": [{"role": "assistant", "content": reply}],
    }


def build_app(checkpointer):
    g = StateGraph(AgentState)
    g.add_node("lookup_profile", lookup_profile)
    g.add_node("decide", decide)
    g.add_edge(START, "lookup_profile")
    g.add_edge("lookup_profile", "decide")
    g.add_edge("decide", END)
    return g.compile(checkpointer=checkpointer)


# --- tiny sqlite log of thread snapshots (illustrates "checkpoint across process") ---

def ckpt_log_init() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(CKPT_PATH) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS thread_log("
            "id INTEGER PRIMARY KEY, thread_id TEXT, customer_id TEXT, reply TEXT)"
        )


def ckpt_log_append(thread_id: str, customer_id: str, reply: str) -> None:
    with sqlite3.connect(CKPT_PATH) as con:
        con.execute(
            "INSERT INTO thread_log(thread_id, customer_id, reply) VALUES (?,?,?)",
            (thread_id, customer_id, reply),
        )


def cmd_chat(args: argparse.Namespace) -> None:
    ckpt_log_init()
    saver = InMemorySaver()
    app = build_app(saver)
    thread_id = args.thread or f"thread-{args.customer}"
    config = {"configurable": {"thread_id": thread_id}}

    if args.amount is not None:
        user_text = f"בקשת החזר על {args.amount:.0f} ש\"ח"
        amount = args.amount
    else:
        user_text = args.message or "מה הסטטוס של הבקשה שלי?"
        amount = None

    result = app.invoke(
        {
            "messages": [{"role": "user", "content": user_text}],
            "customer_id": args.customer,
            "amount": amount,
            "route": None,
            "reply": "",
        },
        config,
    )
    ckpt_log_append(thread_id, args.customer, result["reply"])
    snap = app.get_state(config)
    print(f"thread_id={thread_id}")
    print(f"customer={args.customer}")
    print(f"route={result.get('route')}")
    print(f"reply={result['reply']}")
    print(f"checkpoint.next={list(snap.next)}")
    print(f"messages_in_thread={len(snap.values.get('messages', []))}")
    print(f"store_file={STORE_PATH}")
    print("GOAL_COMPLETE: True")


def cmd_show(_: argparse.Namespace) -> None:
    print("=== profiles (long-term Store) ===")
    print(json.dumps(load_store(), ensure_ascii=False, indent=2) or "{}")
    print("=== thread_log (checkpoint-ish sqlite) ===")
    if not CKPT_PATH.exists():
        print("(empty)")
        return
    with sqlite3.connect(CKPT_PATH) as con:
        rows = con.execute(
            "SELECT id, thread_id, customer_id, reply FROM thread_log ORDER BY id"
        ).fetchall()
    for r in rows:
        print(f"{r[0]}. thread={r[1]} customer={r[2]} | {r[3]}")


def cmd_forget(args: argparse.Namespace) -> None:
    data = load_store()
    print("forgot:", data.pop(args.customer, None))
    save_store(data)


def cmd_reset(_: argparse.Namespace) -> None:
    if STORE_PATH.exists():
        STORE_PATH.unlink()
    if CKPT_PATH.exists():
        CKPT_PATH.unlink()
    print("reset: store + checkpoint log cleared")


def main() -> None:
    p = argparse.ArgumentParser(description="Lab 06 — Memory & State")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("chat", help="תור אחד בגרף (עם Checkpointer + Store)")
    c.add_argument("--customer", required=True)
    c.add_argument("--amount", type=float, default=None)
    c.add_argument("--message", default=None)
    c.add_argument("--thread", default=None, help="ברירת מחדל: thread-<customer>")
    c.set_defaults(func=cmd_chat)

    s = sub.add_parser("show")
    s.set_defaults(func=cmd_show)
    f = sub.add_parser("forget")
    f.add_argument("--customer", required=True)
    f.set_defaults(func=cmd_forget)
    r = sub.add_parser("reset")
    r.set_defaults(func=cmd_reset)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
