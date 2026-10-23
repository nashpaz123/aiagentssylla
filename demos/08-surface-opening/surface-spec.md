# Surface spec (demo) — Nimbus Sales Ops briefing

## Goal

Turn a quote from `data/sample_quote.json` into **two surfaces**:

1. **HTML card** → `out/briefing.html` — self-contained, RTL Hebrew, looks good when opened in a browser (no server required).
2. **Telegram message** → `out/telegram.txt` — plain text / MarkdownV2-safe-ish summary an AE can paste or a bot can send.

## HTML rules

- Single file: inline CSS, no external CDN required for the demo to look OK offline.
- RTL (`dir="rtl"`), Hebrew labels.
- Show: company, SKU, seats, discount, monthly_total, route, status, owner.
- Color by route: `auto` = green accent, `hitl` = amber, `blocked` = red.
- Footer: "טיוטה פנימית — לא נשלח ללקוח אוטומטית".

## Telegram rules

- Hebrew, short (≤ 15 lines).
- Lead with emoji status: ✅ auto · ⏳ hitl · 🚫 blocked
- Never invent numbers — only from the JSON.
- End with: "Draft only · not sent to customer"

## Do not

- Do not call Telegram API in this Claude Code demo (Lab does that with a token).
- Do not modify `data/sample_quote.json` unless the prompt asks.
