#!/usr/bin/env python3
"""
Lab 07 — Business automation (דטרמיניסטי, בלי מפתח).

מנוע Sales Ops: CRM → score → quote → route (auto/hitl/blocked) → draft email.
כפתורים שמשנים תוצאה: lead_id, --discount, --approve/--reject, --set-email.

  python3 sales_lab.py reset
  python3 sales_lab.py run --lead L-SMB
  python3 sales_lab.py run --lead L-ENT
  python3 sales_lab.py approve --lead L-ENT
  python3 sales_lab.py run --lead L-NOMAIL
  python3 sales_lab.py run --lead L-NOMAIL --set-email hero@startup.co.il
  python3 sales_lab.py run --lead L-UPSELL
  python3 sales_lab.py run --lead L-STEAL
  python3 sales_lab.py run --lead L-SMB --discount 22
  python3 sales_lab.py show
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SEED = DATA / "crm.seed.json"
CRM = DATA / "crm.json"
PRICEBOOK = DATA / "pricebook.json"
QUOTES = DATA / "quotes.json"
EMAIL = DATA / "email_draft.md"
AUDIT = DATA / "audit.log"


def load(path: Path, default=None):
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def audit(msg: str) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as f:
        f.write(msg.rstrip() + "\n")
    print(f"AUDIT | {msg}")


def reset() -> None:
    shutil.copy(SEED, CRM)
    for p in (QUOTES, EMAIL, AUDIT):
        if p.exists():
            p.unlink()
    audit("reset")


def score_lead(lead: dict) -> int:
    score = 0
    score += {"low": 10, "medium": 25, "high": 40}.get(lead.get("budget_band", "low"), 10)
    score += {"exploring": 5, "this_quarter": 20, "this_month": 30, "rfp_open": 35, "renewal": 25}.get(
        lead.get("urgency", "exploring"), 5
    )
    score += {"smb": 10, "midmarket": 20, "enterprise": 30}.get(lead.get("segment", "smb"), 10)
    if lead.get("existing_customer"):
        score += 15
    if (lead.get("email") or "").strip():
        score += 10
    else:
        score -= 20
    return max(0, min(100, score))


def route_for(discount: float) -> tuple[str, str]:
    if discount <= 10:
        return "auto", "approved"
    if discount <= 25:
        return "hitl", "pending_manager"
    return "blocked", "rejected"


def run_lead(lead_id: str, discount: float | None, set_email: str | None) -> None:
    crm = load(CRM)
    if lead_id not in crm:
        raise SystemExit(f"unknown lead {lead_id}")
    lead = crm[lead_id]
    if set_email is not None:
        lead["email"] = set_email
        audit(f"set_email {lead_id} -> {set_email}")

    prices = load(PRICEBOOK)
    sku = lead["sku_interest"]
    if sku not in prices:
        raise SystemExit(f"unknown sku {sku}")
    list_unit = float(prices[sku]["list_unit_ils"])
    seats = int(lead["seats"])
    disc = float(discount if discount is not None else lead["requested_discount_pct"])
    lead["requested_discount_pct"] = disc
    lead["score"] = score_lead(lead)

    quotes = load(QUOTES)
    email = (lead.get("email") or "").strip()

    if not email:
        q = {
            "lead_id": lead_id,
            "sku": sku,
            "seats": seats,
            "list_unit": list_unit,
            "discount_pct": disc,
            "monthly_total": None,
            "score": lead["score"],
            "route": "blocked",
            "status": "need_email",
            "upsell": bool(lead.get("existing_customer")),
        }
        lead["stage"] = "blocked"
        draft = f"חסר אימייל לליד {lead_id}. לא ניתן להוציא הצעה."
        audit(f"quote {lead_id} BLOCKED need_email score={lead['score']}")
    else:
        route, status = route_for(disc)
        monthly = round(list_unit * seats * (1 - disc / 100.0), 2)
        q = {
            "lead_id": lead_id,
            "sku": sku,
            "seats": seats,
            "list_unit": list_unit,
            "discount_pct": disc,
            "monthly_total": monthly,
            "score": lead["score"],
            "route": route,
            "status": status,
            "upsell": bool(lead.get("existing_customer")),
        }
        if route == "auto":
            lead["stage"] = "quoted"
        elif route == "hitl":
            lead["stage"] = "pending_approval"
        else:
            lead["stage"] = "blocked"
        kind = "upsell" if lead.get("existing_customer") else "new_logo"
        draft = (
            f"Subject: Nimbus — הצעה ל{lead['company']}\n\n"
            f"שלום,\n"
            f"מצורפת הצעה ({kind}): {sku} × {seats}, הנחה {disc}%, "
            f"סה״כ חודשי {monthly} ₪.\n"
            f"סטטוס פנימי: {route}/{status}. ציון ליד: {lead['score']}.\n"
        )
        if route == "hitl":
            draft += "ההצעה ממתינה לאישור מנהל — אין לשלוח כמאושרת.\n"
        elif route == "blocked":
            draft += "ההנחה חורגת מהמדיניות (>25%). הציעו חבילה חלופית.\n"
        audit(f"quote {lead_id} {route}/{status} monthly={monthly} score={lead['score']}")

    quotes[lead_id] = q
    save(QUOTES, quotes)
    save(CRM, crm)
    EMAIL.write_text(draft + "\n", encoding="utf-8")
    print(json.dumps(q, ensure_ascii=False, indent=2))
    print(f"stage={lead['stage']}")


def approve(lead_id: str, ok: bool) -> None:
    crm = load(CRM)
    quotes = load(QUOTES)
    if lead_id not in quotes:
        raise SystemExit("no quote — run first")
    q = quotes[lead_id]
    if q.get("route") != "hitl" and q.get("status") != "pending_manager":
        raise SystemExit(f"quote not pending_manager: {q.get('status')}")
    if ok:
        q["status"] = "approved"
        q["route"] = "auto"
        crm[lead_id]["stage"] = "quoted"
        audit(f"manager APPROVE {lead_id}")
    else:
        q["status"] = "rejected"
        q["route"] = "blocked"
        crm[lead_id]["stage"] = "blocked"
        audit(f"manager REJECT {lead_id}")
    quotes[lead_id] = q
    save(QUOTES, quotes)
    save(CRM, crm)
    print(json.dumps(q, ensure_ascii=False, indent=2))


def show() -> None:
    print("=== quotes ===")
    print(json.dumps(load(QUOTES), ensure_ascii=False, indent=2))
    print("=== crm stages/scores ===")
    for k, v in load(CRM).items():
        print(f"  {k}: stage={v.get('stage')} score={v.get('score')} disc={v.get('requested_discount_pct')}%")
    if AUDIT.exists():
        print("=== audit (tail) ===")
        print("\n".join(AUDIT.read_text(encoding="utf-8").strip().splitlines()[-12:]))


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("reset")
    sub.add_parser("show")
    r = sub.add_parser("run")
    r.add_argument("--lead", required=True)
    r.add_argument("--discount", type=float, default=None)
    r.add_argument("--set-email", default=None)
    a = sub.add_parser("approve")
    a.add_argument("--lead", required=True)
    j = sub.add_parser("reject")
    j.add_argument("--lead", required=True)
    args = p.parse_args()
    if not CRM.exists():
        reset()
    if args.cmd == "reset":
        reset()
    elif args.cmd == "show":
        show()
    elif args.cmd == "run":
        run_lead(args.lead, args.discount, args.set_email)
    elif args.cmd == "approve":
        approve(args.lead, True)
    else:
        approve(args.lead, False)


if __name__ == "__main__":
    main()
