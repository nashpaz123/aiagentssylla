<div dir="rtl" lang="he">

# ‏Lab 08 — Agent Surfaces (HTML + Telegram)

דורש **`ANTHROPIC_API_KEY`**.  
שליחה אמיתית לטלגרם (אופציונלי): `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`.

| כלי | מה עושה |
|---|---|
| `get_quote` | קורא ליד מ-`data/quotes.json` |
| `render_html_card` | כרטיס RTL יפה → `out/briefing.html` |
| `render_telegram_message` | טיוטת הודעה → `out/telegram.txt` (**לא שולח**) |
| `send_telegram` | Bot API — רק עם env + בקשה מפורשת לשלוח |

## ‏התקנה

```bash
cd labs/08-agent-surfaces
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
# אופציונלי:
# export TELEGRAM_BOT_TOKEN=123:ABC...
# export TELEGRAM_CHAT_ID=...
```

איך משיגים Chat ID: שלחו הודעה לבוט, ואז  
`https://api.telegram.org/bot<TOKEN>/getUpdates` — חפשו `chat.id`.

## ‏הרצה

```bash
python3 surface_claude.py reset
python3 surface_claude.py chat --lead L-SMB --message "הכן כרטיס HTML וטיוטת טלגרם להצעה"
# פתחו את out/briefing.html בדפדפן

python3 surface_claude.py chat --lead L-ENT --message "הכן כרטיס — הדגש שממתין למנהל"
python3 surface_claude.py chat --lead L-UPSELL --message "הכן כרטיס וטיוטה ללקוח קיים (upsell)"

# שליחה אמיתית (רק אם יש token):
python3 surface_claude.py chat --lead L-SMB --message "שלח את הסיכום לטלגרם עכשיו"
python3 surface_claude.py show
```

## ‏מה לבדוק

- [ ] HTML נפתח בדפדפן עם צבע לפי route (ירוק auto / ענבר hitl)  
- [ ] `telegram.txt` קיים **לפני** שליחה  
- [ ] בלי token — `send_telegram` מחזיר `missing_telegram_env` ולא ממציא הצלחה  
- [ ] עם token — הודעה מגיעה לצ׳אט; בלוג `TOOL -> send_telegram`

</div>
