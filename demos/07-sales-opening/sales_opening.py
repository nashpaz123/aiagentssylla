#!/usr/bin/env python3
"""
חלופה דטרמיניסטית להדגמת פתיחה מפגש 7 — בלי מפתח API.

  python3 sales_opening.py reset
  python3 sales_opening.py quote --lead L-SMB
  python3 sales_opening.py quote --lead L-ENT
  python3 sales_opening.py quote --lead L-NOMAIL
  python3 sales_opening.py show
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CRM = ROOT / "crm" / "leads.json"
SEED = ROOT / "crm" / "leads.seed.json"
OUT = ROOT / "out"
QUOTES = OUT / "quotes.json"
EMAIL = OUT / "email_draft.md"

PRICE = {"starter": 99.0, "pro": 299.0, "enterprise": 799.0}


def ensure_seed() -> None:
    if not SEED.exists():
        shutil.copy(CRM, SEED)


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def route_for(discount: float) -> tuple[str, str]:
    if discount <= 10:
        return "auto", "approved"
    if discount <= 25:
        return "hitl", "pending_manager"
    return "blocked", "rejected"


def quote_lead(lead_id: str) -> None:
    ensure_seed()
    leads = load_json(CRM)
    if lead_id not in leads:
        raise SystemExit(f"unknown lead {lead_id}")
    lead = leads[lead_id]
    quotes = load_json(QUOTES)

    email = (lead.get("email") or "").strip()
    sku = lead["sku_interest"]
    seats = int(lead["seats"])
    discount = float(lead["requested_discount_pct"])
    list_unit = PRICE[sku]

    if not email:
        q = {
            "lead_id": lead_id,
            "sku": sku,
            "seats": seats,
            "list_unit": list_unit,
            "discount_pct": discount,
            "monthly_total": None,
            "route": "blocked",
            "status": "need_email",
            "note": "Missing email — cannot quote",
        }
        lead["stage"] = "blocked"
        body = (
            f"ליד {lead_id} ({lead['company']}) חסום: אין אימייל.\n"
            "לא נוצרה הצעת מחיר מאושרת. יש לאסוף מייל מה-AE ולנסות שוב."
        )
    else:
        route, status = route_for(discount)
        monthly = round(list_unit * seats * (1 - discount / 100.0), 2)
        q = {
            "lead_id": lead_id,
            "sku": sku,
            "seats": seats,
            "list_unit": list_unit,
            "discount_pct": discount,
            "monthly_total": monthly,
            "route": route,
            "status": status,
            "note": f"{lead['segment']} deal; existing={lead.get('existing_customer')}",
        }
        if route == "auto":
            lead["stage"] = "quoted"
        elif route == "hitl":
            lead["stage"] = "pending_approval"
        else:
            lead["stage"] = "blocked"
        body = (
            f"הצעה ל-{lead['company']} ({lead_id})\n"
            f"SKU={sku} · {seats} מושבים · הנחה {discount}% · סה״כ חודשי {monthly} ₪\n"
            f"מסלול: {route} / {status}\n"
        )
        if route == "hitl":
            body += "ממתין לאישור מנהל — לא לשלוח ללקוח כמאושר.\n"
        elif route == "auto":
            body += "מאושר אוטומטית — אפשר לשלוח אחרי סקירת AE.\n"
        else:
            body += "נדחה — הנחה מעל 25%. הציעו חבילה אחרת.\n"

    quotes[lead_id] = q
    save_json(QUOTES, quotes)
    save_json(CRM, leads)
    EMAIL.write_text(
        f"Subject: Nimbus — הצעת מחיר ל{lead['company']}\n\n{body}\n",
        encoding="utf-8",
    )
    print(json.dumps(q, ensure_ascii=False, indent=2))
    print(f"stage → {lead['stage']}")
    print(f"wrote {QUOTES.relative_to(ROOT)} and {EMAIL.relative_to(ROOT)}")


def show() -> None:
    print("=== quotes ===")
    print(json.dumps(load_json(QUOTES), ensure_ascii=False, indent=2) or "{}")
    print("=== stages ===")
    for k, v in load_json(CRM).items():
        print(f"  {k}: {v.get('stage')}")


def reset() -> None:
    ensure_seed()
    shutil.copy(SEED, CRM)
    if QUOTES.exists():
        QUOTES.unlink()
    if EMAIL.exists():
        EMAIL.unlink()
    print("reset OK")


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("reset")
    sub.add_parser("show")
    q = sub.add_parser("quote")
    q.add_argument("--lead", required=True)
    args = p.parse_args()
    if args.cmd == "reset":
        reset()
    elif args.cmd == "show":
        show()
    else:
        quote_lead(args.lead)


if __name__ == "__main__":
    main()
