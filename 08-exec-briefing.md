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
| Tool | פעולה שה-agent קורא לה (Write, send_telegram…) |
| Surface | משטח פלט לאדם (HTML / Telegram) |
| Draft ≠ Send | טיוטת הודעה לקובץ ≠ שליחה לרשת |
| Bot token / Chat ID | סוד הבוט ויעד השליחה — לא בגיט |

---

## ‏3 — למה HTML וטלגרם?

| ערוץ | למי מתאים |
|---|---|
| טרמינל | מפתחים בהקלטה / דיבוג |
| HTML card | AE / מנהל — פתיחה בדפדפן, צבע לפי מסלול |
| Telegram | דחיפה לנייד — "יש הצעה ממתינה" |

שערי כסף ממפגש 7 נשארים: auto ירוק · HITL ענבר · חסימה אדומה — **גם בכרטיס**.

---

## ‏4 — Draft ≠ Send (שוב)

1. הסוכן כותב `telegram.txt` / כרטיס HTML  
2. שליחה לטלגרם = כלי נפרד + token + בקשה מפורשת  
3. בלי הרשאה — המערכת מדווחת שגיאה, לא "נשלח"

---

## ‏5 — מה רואים בשיעור (מעשי)

| שלב | מה קורה |
|---|---|
| דמו Claude Code (מעטפת CLI) | Agent כותב `briefing.html` + `telegram.txt` |
| Lab Anthropic (runtime) | כלים: `render_*` ואז `send_telegram` אופציונלי |
| Cursor (מעטפת IDE) | Agent משפר עיצוב הכרטיס בלי לשנות מספרים |

לידים לדוגמה: SMB (אוטומטי) · Enterprise (ממתין למנהל) · Upsell (לקוח קיים).

---

## ‏6 — סיכונים שצריך לסגור בפיילוט

- Token של טלגרם בריפו / בצילום מסך  
- שליחה אוטומטית לכל הצעה (ספאם / דליפת PII)  
- הצהרת "נשלח" בלי אישור מה-API  
- מספרים מהמודל במקום מהמערכת  

---

## ‏7 — ROI למשטחים

| בעל עניין | ערך |
|---|---|
| AE | כרטיס מוכן + התראה בנייד |
| מנהל מכירות | רואה HITL בלי לפתוח CRM |
| RevOps / אבטחה | שליחה מבוקרת + לוג |

---

## ‏קישורים

| קובץ | תפקיד |
|---|---|
| [`08-students-slides.md`](08-students-slides.md) | מצגת |
| [`08-cursor-claude-surfaces.md`](08-cursor-claude-surfaces.md) | תסריט מרצה |
| [`demos/08-surface-opening/`](demos/08-surface-opening/) | דמו פתיחה |
| [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/) | Lab |

</div>
