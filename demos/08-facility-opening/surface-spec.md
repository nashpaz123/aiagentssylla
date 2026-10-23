# Surface spec (demo) — Atlas Facility Ops

Turn a work order from `data/sample_work_orders.json` into **two surfaces**:

1. **HTML card** → `out/work_order.html` — RTL, self-contained CSS, color by `severity`:
   - `open` → blue banner
   - `sla_breach` → red banner
   - `blocked` → amber banner
2. **Telegram message** → `out/telegram.txt` — then run `./send-telegram.sh` to send to your chat.

Include: wo id, site, category, title, priority, severity, SLA hours, assignee, asset_id.

Rules:
- Do not invent fields. Numbers come from JSON only.
- This is facility ops — not sales (no prices / seats / discounts).
- Do not call Telegram API from Claude Code; writing `out/telegram.txt` is enough — `send-telegram.sh` sends after.
- Do not modify `data/sample_work_orders.json` unless the prompt asks.
