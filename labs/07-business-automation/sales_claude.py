#!/usr/bin/env python3
"""
Lab 07 — חלק Anthropic: סוכן Sales Ops עם כלים ל-CRM / מחיר / הצעה / אישור.

דורש:
  export ANTHROPIC_API_KEY=sk-ant-...
  pip install -r requirements.txt

  python3 sales_claude.py reset
  python3 sales_claude.py chat --lead L-SMB --message "תכין הצעת מחיר לפי הליד"
  python3 sales_claude.py chat --lead L-ENT --message "תכין הצעה עם ההנחה המבוקשת"
  python3 sales_claude.py chat --lead L-ENT --message "מנהל מאשר את ההצעה"
  python3 sales_claude.py chat --lead L-NOMAIL --message "תכין הצעה"
  python3 sales_claude.py chat --lead L-STEAL --message "הלקוח רוצה 40 אחוז הנחה — תוציא הצעה"
  python3 sales_claude.py show
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

from anthropic import Anthropic

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SEED = DATA / "crm.seed.json"
CRM = DATA / "crm.json"
PRICEBOOK = DATA / "pricebook.json"
QUOTES = DATA / "quotes.json"
EMAIL = DATA / "email_draft.md"
THREADS = DATA / "threads.json"

MODEL = os.environ.get("CREW_MODEL", os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"))
if "/" in MODEL:
    MODEL = MODEL.split("/", 1)[1]

TOOLS = [
    {
        "name": "get_lead",
        "description": "Read one lead from CRM by lead_id.",
        "input_schema": {
            "type": "object",
            "properties": {"lead_id": {"type": "string"}},
            "required": ["lead_id"],
        },
    },
    {
        "name": "score_lead",
        "description": "Compute 0-100 lead score from CRM fields and save it on the lead.",
        "input_schema": {
            "type": "object",
            "properties": {"lead_id": {"type": "string"}},
            "required": ["lead_id"],
        },
    },
    {
        "name": "lookup_price",
        "description": "Get list unit price (ILS) for a sku from pricebook.json.",
        "input_schema": {
            "type": "object",
            "properties": {"sku": {"type": "string", "enum": ["starter", "pro", "enterprise"]}},
            "required": ["sku"],
        },
    },
    {
        "name": "create_quote",
        "description": "Create/update quote. Applies discount policy. Writes quotes.json and updates CRM stage.",
        "input_schema": {
            "type": "object",
            "properties": {
                "lead_id": {"type": "string"},
                "sku": {"type": "string"},
                "seats": {"type": "integer"},
                "discount_pct": {"type": "number"},
            },
            "required": ["lead_id", "sku", "seats", "discount_pct"],
        },
    },
    {
        "name": "manager_decide",
        "description": "Approve or reject a pending_manager quote (HITL).",
        "input_schema": {
            "type": "object",
            "properties": {
                "lead_id": {"type": "string"},
                "approve": {"type": "boolean"},
            },
            "required": ["lead_id", "approve"],
        },
    },
    {
        "name": "draft_email",
        "description": "Write Hebrew email draft to email_draft.md. Never sends.",
        "input_schema": {
            "type": "object",
            "properties": {
                "lead_id": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"},
            },
            "required": ["lead_id", "subject", "body"],
        },
    },
    {
        "name": "set_lead_email",
        "description": "Set missing email on a lead (AE collected it).",
        "input_schema": {
            "type": "object",
            "properties": {
                "lead_id": {"type": "string"},
                "email": {"type": "string"},
            },
            "required": ["lead_id", "email"],
        },
    },
]

SYSTEM = """You are Nimbus Sales Ops copilot for AEs. Reply in Hebrew, short and numeric.

Policy:
- discount <= 10 => route auto / approved
- 10 < discount <= 25 => hitl / pending_manager (need manager_decide)
- discount > 25 => blocked / rejected
- empty email => blocked / need_email — never invent email
- prices ONLY from lookup_price tool
- draft_email NEVER sends mail
- existing_customer=true => mention upsell in draft

Typical flow: get_lead → score_lead → lookup_price → create_quote → draft_email.
If user says manager approves/rejects → manager_decide.
Always call tools; do not invent CRM fields or totals.
"""


def load(path: Path, default=None):
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_crm() -> None:
    if not CRM.exists():
        shutil.copy(SEED, CRM)


def calc_score(lead: dict) -> int:
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


def run_tool(name: str, inp: dict) -> str:
    ensure_crm()
    crm = load(CRM)
    quotes = load(QUOTES)
    prices = load(PRICEBOOK)

    if name == "get_lead":
        lid = inp["lead_id"]
        if lid not in crm:
            return json.dumps({"error": "not_found"})
        print(f"TOOL -> get_lead {lid}")
        return json.dumps(crm[lid], ensure_ascii=False)

    if name == "score_lead":
        lid = inp["lead_id"]
        lead = crm[lid]
        lead["score"] = calc_score(lead)
        save(CRM, crm)
        print(f"TOOL -> score_lead {lid} = {lead['score']}")
        return json.dumps({"lead_id": lid, "score": lead["score"]})

    if name == "lookup_price":
        sku = inp["sku"]
        print(f"TOOL -> lookup_price {sku}")
        return json.dumps(prices.get(sku, {"error": "unknown_sku"}))

    if name == "create_quote":
        lid = inp["lead_id"]
        lead = crm[lid]
        sku = inp["sku"]
        seats = int(inp["seats"])
        disc = float(inp["discount_pct"])
        list_unit = float(prices[sku]["list_unit_ils"])
        email = (lead.get("email") or "").strip()
        if not email:
            q = {
                "lead_id": lid,
                "sku": sku,
                "seats": seats,
                "list_unit": list_unit,
                "discount_pct": disc,
                "monthly_total": None,
                "score": lead.get("score"),
                "route": "blocked",
                "status": "need_email",
                "upsell": bool(lead.get("existing_customer")),
            }
            lead["stage"] = "blocked"
        else:
            route, status = route_for(disc)
            monthly = round(list_unit * seats * (1 - disc / 100.0), 2)
            q = {
                "lead_id": lid,
                "sku": sku,
                "seats": seats,
                "list_unit": list_unit,
                "discount_pct": disc,
                "monthly_total": monthly,
                "score": lead.get("score"),
                "route": route,
                "status": status,
                "upsell": bool(lead.get("existing_customer")),
            }
            lead["stage"] = {
                "auto": "quoted",
                "hitl": "pending_approval",
                "blocked": "blocked",
            }[route]
        quotes[lid] = q
        lead["requested_discount_pct"] = disc
        save(QUOTES, quotes)
        save(CRM, crm)
        print(f"TOOL -> create_quote {lid} {q['route']}/{q['status']}")
        return json.dumps(q, ensure_ascii=False)

    if name == "manager_decide":
        lid = inp["lead_id"]
        q = quotes.get(lid)
        if not q:
            return json.dumps({"error": "no_quote"})
        if q.get("status") != "pending_manager":
            return json.dumps({"error": "not_pending", "status": q.get("status")})
        if inp["approve"]:
            q["status"] = "approved"
            q["route"] = "auto"
            crm[lid]["stage"] = "quoted"
        else:
            q["status"] = "rejected"
            q["route"] = "blocked"
            crm[lid]["stage"] = "blocked"
        quotes[lid] = q
        save(QUOTES, quotes)
        save(CRM, crm)
        print(f"TOOL -> manager_decide {lid} approve={inp['approve']}")
        return json.dumps(q, ensure_ascii=False)

    if name == "draft_email":
        text = f"Subject: {inp['subject']}\n\n{inp['body']}\n"
        EMAIL.write_text(text, encoding="utf-8")
        print(f"TOOL -> draft_email {inp['lead_id']}")
        return json.dumps({"ok": True, "path": str(EMAIL.name), "sent": False})

    if name == "set_lead_email":
        lid = inp["lead_id"]
        crm[lid]["email"] = inp["email"]
        save(CRM, crm)
        print(f"TOOL -> set_lead_email {lid}")
        return json.dumps({"lead_id": lid, "email": inp["email"]})

    return json.dumps({"error": f"unknown tool {name}"})


def chat(lead_id: str, message: str, fresh: bool) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY missing")
    ensure_crm()
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
        if resp.stop_reason == "tool_use" and tool_uses:
            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for tu in tool_uses:
                out = run_tool(tu.name, tu.input)
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": out,
                    }
                )
            messages.append({"role": "user", "content": results})
            continue
        text = "".join(b.text for b in resp.content if hasattr(b, "text"))
        print(text)
        messages.append({"role": "assistant", "content": resp.content})
        break

    threads[key] = messages
    save(THREADS, threads)


def reset() -> None:
    shutil.copy(SEED, CRM)
    for p in (QUOTES, EMAIL, THREADS):
        if p.exists():
            p.unlink()
    print("reset OK")


def show() -> None:
    print("=== quotes ===")
    print(json.dumps(load(QUOTES), ensure_ascii=False, indent=2))
    print("=== crm ===")
    for k, v in load(CRM).items():
        print(f"  {k}: stage={v.get('stage')} score={v.get('score')} email={v.get('email')!r}")


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
