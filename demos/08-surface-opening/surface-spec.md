# Surface spec (demo) — Nimbus Sales Ops briefing

## Goal

Turn a quote from `data/sample_quote.json` into **two surfaces**:

1. **HTML card** → `out/briefing.html` — self-contained, RTL Hebrew, browser-ready.
2. **Telegram message** → `out/telegram.txt` — then the instructor runs `./send-telegram.sh` to **send it** to their personal Telegram.

## HTML rules

- Single file: inline CSS, no external CDN required offline.
- RTL (`dir="rtl"`), Hebrew labels.
- Show: company, SKU, seats, discount, monthly_total, route, status, owner.
- Color by route: `auto` = green, `hitl` = amber, `blocked` = red.
- Footer: "סיכום פנימי ל-AE · נשלח גם לטלגרם הפנימי".

## Telegram rules

- Hebrew, short (≤ 15 lines).
- Lead with emoji: ✅ auto · ⏳ hitl · 🚫 blocked
- Never invent numbers — only from the JSON.
- End with: "Internal ops alert · not the customer email"

## Do not

- Do not call Telegram API from Claude Code in this demo (network allowlist); writing `out/telegram.txt` is enough — `send-telegram.sh` sends after.
- Do not modify `data/sample_quote.json` unless the prompt asks.
