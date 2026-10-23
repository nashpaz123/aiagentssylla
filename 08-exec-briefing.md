<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 8 — תדריך מנהלים (High Level)
## ‏Cursor · Claude · משטחי פלט (UI / Telegram)

> **למי:** מנהלי מוצר, מכירות, RevOps — ומרצה שצריך שפה עסקית בהקלטה.  
> **בלי Copilot:** במסלול שלנו רק Cursor + Claude Code + Anthropic.  
> מצגת מלאה: [`08-students-slides.md`](08-students-slides.md)

---

## ‏1 — המסר המרכזי

סוכן שלא מוציא פלט **למשתמש** נשאר כלי למפתחים.

אנחנו מחברים:

1. **מעטפות** (Cursor / Claude Code) — מריצות coding agents שבונים ומתקנים  
2. **Runtime agent** (Anthropic + כלים) — רץ בזמן אמת על ליד/הצעה  
3. **Surfaces** — כרטיס HTML בדפדפן · הודעת Telegram לנייד  

**משפט להנהלה:**  
אותה עסקה שרצה במפגש 7 — היום AE רואה אותה ככרטיס יפה ומקבל התראה בטלגרם, בלי לקרוא לוג.

---

## ‏2 — מילון קצר

| מונח | משמעות |
|---|---|
| Cursor / Claude Code | **מעטפות** שמריצות agents — לא הכלים עצמם |
| Coding agent | ה-agent שבתוך המעטפת ומשנה קבצים |
| Tool | פעולה שה-agent קורא לה (Write, `notify_telegram`…) |
| Surface | משטח פלט לאדם (HTML / Telegram) |
| notify_telegram | כותב הודעה **ושולח** לצ׳אט הפנימי (שלכם) |
| Bot token / Chat ID | סוד הבוט + הצ׳אט שלכם — ב-`.env`, לא בגיט |

---

## ‏3 — למה HTML וטלגרם?

| ערוץ | למי מתאים |
|---|---|
| טרמינל | מפתחים בהקלטה / דיבוג |
| HTML card | AE / מנהל — פתיחה בדפדפן, צבע לפי מסלול |
| Telegram | דחיפה לנייד — "יש הצעה ממתינה" |

שערי כסף ממפגש 7 נשארים: auto ירוק · HITL ענבר · חסימה אדומה — **גם בכרטיס**.

---

## ‏4 — טלגרם פנימי = שולחים

1. הסוכן בונה כרטיס HTML **ושולח** סיכום לטלגרם שלכם (צ׳אט פנימי)  
2. דמו: `./send-telegram.sh` אחרי Claude · Lab: כלי `notify_telegram`  
3. בלי `TELEGRAM_*` ב-`.env` — כישלון ברור, לא "נשלח" מזויף  
4. ללקוח הסופי (מייל וכו׳) — עדיין עם שער ממפגש 7; כאן היעד הוא **אתם**

---

## ‏5 — מה רואים בשיעור (מעשי)

| שלב | מה קורה |
|---|---|
| דמו Claude Code (מעטפת CLI) | Agent כותב HTML + טקסט → `./send-telegram.sh` שולח אליכם |
| Lab Anthropic (runtime) | `render_html_card` + `notify_telegram` (חובה env) |
| Cursor (מעטפת IDE) | Agent משפר עיצוב הכרטיס בלי לשנות מספרים |

לידים לדוגמה: SMB (אוטומטי) · Enterprise (ממתין למנהל) · Upsell (לקוח קיים).

---

## ‏6 — סיכונים שצריך לסגור בפיילוט

- Token של טלגרם בריפו / בצילום מסך  
- שליחה ללקוח סופי בלי שער (המפגש = צ׳אט פנימי בלבד)  
- הצהרת "נשלח" בלי `sent=true` מה-API  
- מספרים מהמודל במקום מהמערכת  

---

## ‏7 — ROI למשטחים

| בעל עניין | ערך |
|---|---|
| AE | כרטיס מוכן + התראה אמיתית בנייד |
| מנהל מכירות | רואה HITL בלי לפתוח CRM |
| RevOps / אבטחה | יעד פנימי מבוקר + לוג שליחה |

---

## ‏קישורים

| קובץ | תפקיד |
|---|---|
| [`08-students-slides.md`](08-students-slides.md) | מצגת |
| [`08-cursor-claude-surfaces.md`](08-cursor-claude-surfaces.md) | תסריט מרצה |
| [`demos/08-surface-opening/`](demos/08-surface-opening/) | דמו פתיחה |
| [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/) | Lab |

</div>
