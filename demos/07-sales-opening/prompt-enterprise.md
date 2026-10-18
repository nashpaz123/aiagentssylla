Work ONLY in this folder. Use the `sales` subagent (or act as sales if Task is unavailable).

AE Noa asks: process lead **L-ENT** — create a quote for their requested SKU/seats/discount.

1. Read `policy.md` and `crm/leads.json` (L-ENT). Keep any existing L-SMB quote in `out/quotes.json`.
2. Write/update `out/quotes.json` for L-ENT.
3. Update L-ENT `stage` (expect HITL / pending_manager because discount > 10%).
4. Optionally refresh `out/email_draft.md` with a draft that says "pending manager approval" — do not claim approved.
5. Reply in Hebrew: deal size, discount, why manager gate.

Do not invent prices. Do not auto-approve >10% discount.
