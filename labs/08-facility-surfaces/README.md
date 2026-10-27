<div dir="rtl" lang="he" style="text-align: right; unicode-bidi: plaintext;">

# ‏Lab 08B — Facility Surfaces (Atlas · קריאות שירות)

**דומיין אחר מ-Nimbus:** ניהול מתקנים / קריאות שירות בבניין — לא הצעות מחיר ולא הזמנות לקוח.

אותו דפוס משטחים: כרטיס HTML + שליחת טלגרם אמיתית.

דורש: `ANTHROPIC_API_KEY` · `TELEGRAM_BOT_TOKEN` · `TELEGRAM_CHAT_ID`

| כלי | מה עושה |
|---|---|
| `get_work_order` | קורא קריאה מ-`data/work_orders.json` |
| `render_html_card` | כרטיס RTL → `out/work_order.html` |
| `notify_telegram` | כותב `out/telegram.txt` **ושולח** עכשיו |

| מזהה | חומרה | תרחיש |
|---|---|---|
| `WO-HVAC` | ‏`open` (כחול) | מיזוג באגף |
| `WO-ELEV` | ‏`sla_breach` (אדום) | מעלית בחניון — חריגת SLA |
| `WO-ACCESS` | ‏`blocked` (ענבר) | קורא תגיות ממתין לספק |

## ‏התקנה

```bash
cd labs/08-facility-surfaces
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # או העתיקו מ-demos/08-surface-opening/.env
```

## ‏הרצה

```bash
python3 facility_claude.py reset

python3 facility_claude.py chat --wo WO-HVAC --message "הכן כרטיס HTML ושלח התראה למנהל מתקנים"
python3 facility_claude.py chat --wo WO-ELEV --message "קריאה דחופה — חריגת SLA, שלח עכשיו"
python3 facility_claude.py chat --wo WO-ACCESS --message "הכן כרטיס ושלח — חסום אצל ספק"

# בלי LLM — HTML + שליחה חוזרת:
python3 facility_claude.py notify --wo WO-ELEV
python3 facility_claude.py show
```

## ‏מה לבדוק

- ‏[ ] הצבע בכרטיס תואם חומרה (כחול / אדום / ענבר)  
- ‏[ ] אין מחירים / מושבים / הנחות — זה לא Nimbus  
- ‏[ ] הודעה מגיעה לטלגרם עם `Atlas Facility`  
- ‏[ ] `TOOL -> get_work_order` ואז `notify_telegram` עם `sent=true`

השוואה ל-Lab המכירות: [`../08-agent-surfaces/`](../08-agent-surfaces/)

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
python3 facility_claude.py show
```

חפשו ש-`TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` מסומנים כ-`set` (לא `MISSING`).

</div>
