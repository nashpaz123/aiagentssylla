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

פירוט מלא להשגת token + chat id — **בסוף הקובץ**.

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

## ‏גיוון דומיין

אותו דפוס על **קריאות שירות בבניין** (לא מכירות): [`../08-facility-surfaces/`](../08-facility-surfaces/) · דמו [`../../demos/08-facility-opening/`](../../demos/08-facility-opening/).

## ‏איך משיגים TELEGRAM_BOT_TOKEN ו-TELEGRAM_CHAT_ID

אפשר לשים ב-`.env` **או** לעשות `export` באותו טרמינל לפני ההרצה.

### ‏1) Bot token — `@BotFather`

1. בטלגרם חפשו **@BotFather** ופתחו צ׳אט.  
2. שלחו <code dir="ltr">/newbot</code> (או השתמשו בבוט קיים עם <code dir="ltr">/token</code> / <code dir="ltr">/mybots</code>).  
3. עקבו אחרי ההנחיות (שם + username שמסתיים ב-`bot`).  
4. BotFather מחזיר מחרוזת בסגנון <code dir="ltr">123456789:AAH...</code> — זה **`TELEGRAM_BOT_TOKEN`**.  
5. אל תשימו את ה-token בגיט / בצילום מסך בהקלטה.

### ‏2) Chat ID — הצ׳אט שלכם עם הבוט

1. פתחו צ׳אט עם הבוט החדש ולחצו **Start** (או שלחו כל הודעה, למשל `hi`).  
2. בדפדפן (החליפו `<TOKEN>` ב-token שלכם):

<pre dir="ltr"><code>https://api.telegram.org/bot&lt;TOKEN&gt;/getUpdates
</code></pre>

3. ב-JSON חפשו <code dir="ltr">"chat":{"id": ...}</code> — המספר (למשל <code dir="ltr">123456789</code>, לפעמים שלילי לקבוצות) הוא **`TELEGRAM_CHAT_ID`**.  
4. אם קיבלתם <code dir="ltr">{"ok":true,"result":[]}</code> — שלחו שוב הודעה לבוט ורעננו את ה-URL.

### ‏3) הגדרה ב-Lab

**קובץ `.env`** (מהדוגמה):

```bash
cp .env.example .env
# ANTHROPIC_API_KEY=...
# TELEGRAM_BOT_TOKEN=123456789:AAH...
# TELEGRAM_CHAT_ID=123456789
```

**או `export` בטרמינל** (גובר על `.env` אם כבר הוגדר):

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export TELEGRAM_BOT_TOKEN='123456789:AAH...'
export TELEGRAM_CHAT_ID='123456789'
```

בדיקה מהירה בלי LLM:

```bash
python3 surface_claude.py show
```

חפשו ש-`TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` מסומנים כ-`set` (לא `MISSING`).

</div>
