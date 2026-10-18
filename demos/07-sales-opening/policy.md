# Nimbus Sales Policy (demo)

Company: **Nimbus** — B2B SaaS (collaboration seats).

## Discount & approval

1. Discount **≤ 10%** inclusive → `route=auto`, `status=approved` (AE may send quote).
2. Discount **> 10% and ≤ 25%** → `route=hitl`, `status=pending_manager` (manager must approve).
3. Discount **> 25%** → `route=blocked`, `status=rejected` (do not quote; propose alternatives).

## Pricing (list)

| SKU | Name | List price / seat / month (ILS) |
|-----|------|----------------------------------|
| starter | Starter | 99 |
| pro | Pro | 299 |
| enterprise | Enterprise | 799 |

## Lead handling

1. Always read `crm/leads.json` for the lead before quoting.
2. Compute: `line_total = list_price * seats * (1 - discount_pct/100)` (monthly).
3. Write/update `out/quotes.json` keyed by `lead_id`.
4. Update the lead's `stage` in `crm/leads.json`: `qualified` → `quoted` → `pending_approval` or `closed_won_pending`.
5. Never invent prices. Never send email — only draft text in the reply / `out/email_draft.md`.
6. If lead has no `email` → `route=blocked`, ask for email; do not quote.
7. If `existing_customer=true` → prefer upsell language; still use same discount rules.
