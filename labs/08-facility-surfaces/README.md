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

</div>
