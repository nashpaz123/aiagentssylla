#!/usr/bin/env python3
"""
הדגמת פתיחה — מפגש 6: מה קורה בלי זיכרון בין תורות, ומה קורה עם Store פשוט.

אין מפתח API. אפשר להריץ פעמיים עם לקוחות/סכומים שונים ולראות תוצאות שונות.

דוגמאות:
  python3 memory_opening.py --mode none
  python3 memory_opening.py --mode store --customer C-99 --amount 99
  python3 memory_opening.py --mode store --customer C-99 --amount 99   # תור 2: זוכר
  python3 memory_opening.py --mode store --customer C-101 --amount 101
  python3 memory_opening.py --forget --customer C-99
  python3 memory_opening.py --show
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

STORE = Path(__file__).resolve().parent / "out" / "profiles.json"
THRESHOLD = 100.0


def load() -> dict:
    if not STORE.exists():
        return {}
    return json.loads(STORE.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    STORE.parent.mkdir(parents=True, exist_ok=True)
    STORE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def policy_line(amount: float) -> str:
    if amount <= THRESHOLD:
        return f"סכום {amount:.0f} ≤ {THRESHOLD:.0f} → אישור אוטומטי (בלי HITL)."
    return f"סכום {amount:.0f} > {THRESHOLD:.0f} → נדרש אישור נציג (HITL) לפני התחייבות."


def turn_without_memory(customer: str, amount: float) -> None:
    print("== מצב: אין זיכרון בין תורות ==")
    print(f"[תור 1] {customer}: אני רוצה החזר על {amount:.0f} ש\"ח")
    print(f"        סוכן: קיבלתי. {policy_line(amount)}")
    print(f"[תור 2] {customer}: מה הסטטוס של הבקשה שלי?")
    print("        סוכן: אין לי הקשר. איזו הזמנה? כמה ביקשת? (שכחתי — אין Store)")
    print("GOAL: show that without memory, turn 2 starts blank.")


def turn_with_store(customer: str, amount: float | None, status_only: bool) -> None:
    data = load()
    profile = data.get(customer, {})
    print("== מצב: Store פשוט (profiles.json) ==")
    print(f"קובץ: {STORE}")

    if status_only or (amount is None and customer in data):
        print(f"[תור 2+] {customer}: מה הסטטוס של הבקשה שלי?")
        if not profile:
            print("        סוכן: אין לי רישום עליך. פתח בקשה חדשה.")
        else:
            print(
                f"        סוכן: זוכר — בקשה על {profile['amount']:.0f} ש\"ח, "
                f"מסלול={profile['route']}, סטטוס={profile['status']}."
            )
        print("GOAL: turn 2 uses prior profile.")
        return

    assert amount is not None
    route = "auto" if amount <= THRESHOLD else "hitl"
    status = "approved" if route == "auto" else "pending_human"
    print(f"[תור 1] {customer}: אני רוצה החזר על {amount:.0f} ש\"ח")
    print(f"        סוכן: {policy_line(amount)}")
    profile = {
        "amount": amount,
        "route": route,
        "status": status,
        "note": "opening demo — session 6",
    }
    data[customer] = profile
    save(data)
    print(f"        נשמר ל-Store: {json.dumps(profile, ensure_ascii=False)}")
    print("        (הריצו שוב עם אותו --customer בלי --amount, או עם --status, לראות תור 2)")


def main() -> None:
    p = argparse.ArgumentParser(description="Session 6 opening demo — Checkpoint≠Memory")
    p.add_argument("--mode", choices=["none", "store"], default="store")
    p.add_argument("--customer", default="C-99")
    p.add_argument("--amount", type=float, default=None, help="סכום החזר בתור 1")
    p.add_argument("--status", action="store_true", help="תור סטטוס בלבד (משתמש ב-Store)")
    p.add_argument("--forget", action="store_true", help="מוחק פרופיל לקוח מה-Store")
    p.add_argument("--show", action="store_true", help="מציג את כל ה-Store")
    p.add_argument("--reset", action="store_true", help="מוחק את כל profiles.json")
    args = p.parse_args()

    if args.reset:
        if STORE.exists():
            STORE.unlink()
        print("Store cleared.")
        return
    if args.show:
        print(json.dumps(load(), ensure_ascii=False, indent=2) or "{}")
        return
    if args.forget:
        data = load()
        gone = data.pop(args.customer, None)
        save(data)
        print(f"forgot {args.customer}: {gone}")
        return

    if args.mode == "none":
        amount = args.amount if args.amount is not None else 99.0
        turn_without_memory(args.customer, amount)
        return

    amount = args.amount
    if amount is None and not args.status and args.customer not in load():
        amount = 99.0  # default first turn
    turn_with_store(args.customer, amount, status_only=args.status)


if __name__ == "__main__":
    main()
