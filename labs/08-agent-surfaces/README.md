<div dir="rtl" lang="he" style="text-align: right; unicode-bidi: plaintext;">

# ‏Lab 08 — Agent Surfaces (HTML + Telegram send)

דורש:

- `ANTHROPIC_API_KEY`
- ‏`TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (**שליחה אמיתית לצ׳אט שלך**)

| כלי | מה עושה |
|---|---|
| `get_quote` | קורא ליד מ-`data/quotes.json` |
| `render_html_card` | כרטיס RTL → `out/briefing.html` |
| `notify_telegram` | כותב `out/telegram.txt` **ושולח** לטלגרם עכשיו |

## ‏התקנה

```bash
cd labs/08-agent-surfaces
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# ערכו .env: ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
```

**איך משיגים Chat ID (הצ׳אט שלך):**

1. צרו בוט ב-@BotFather → העתיקו את ה-token ל-`.env`  
2. פתחו צ׳אט עם הבוט ולחצו Start / שלחו איזו הודעה  
3. פתחו בדפדפן: `https://api.telegram.org/bot<TOKEN>/getUpdates`  
4. מצאו `"chat":{"id": ...}` — זה `TELEGRAM_CHAT_ID`

## ‏הרצה

```bash
python3 surface_claude.py reset

# Agent מלא (HTML + שליחה לטלגרם):
python3 surface_claude.py chat --lead L-SMB --message "הכן כרטיס HTML ושלח סיכום לטלגרם שלי"
# פתחו out/briefing.html בדפדפן — ובדקו את הטלפון

python3 surface_claude.py chat --lead L-ENT --message "הכן כרטיס ושלח — ממתין למנהל"
python3 surface_claude.py chat --lead L-UPSELL --message "הכן כרטיס ושלח ללקוח קיים (upsell)"

# בלי LLM — רק HTML + שליחה חוזרת:
python3 surface_claude.py notify --lead L-SMB
python3 surface_claude.py show
```

## ‏מה לבדוק

- ‏[ ] הודעה מגיעה לטלגרם האישי  
- ‏[ ] HTML נפתח עם צבע לפי route  
- ‏[ ] בלוג: `TOOL -> notify_telegram` עם `sent=true`  
- ‏[ ] בלי `.env` מלא — היציאה נכשלת עם הודעה ברורה (לא "נשלח" מזויף)

</div>

## ‏גיוון דומיין

אותו דפוס על **קריאות שירות בבניין** (לא מכירות): [`../08-facility-surfaces/`](../08-facility-surfaces/) · דמו [`../../demos/08-facility-opening/`](../../demos/08-facility-opening/).
