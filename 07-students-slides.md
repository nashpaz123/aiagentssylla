<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 7 — מצגת סטודנטים
## ‏Agents לאוטומציה עסקית

> **משך משוער:** ~2.5–3.5 שעות (הדגמת פתיחה + הוראה + Lab עשיר + Design Review).  
> נפתח ב-Sales Ops ב-Claude Code/Cursor — CRM → הצעת מחיר → שער כסף.  
> Lab עם Anthropic API (או חלופה בלי מפתח) ותרחישי SMB / Enterprise / Upsell / Blocked.  
> חזרה קצרה: כלים (3) · צוות (5) · Memory/Store (6).

---

# ‏חלק א׳ — פתיחה והדגמה

_סוכן מכירות רץ על לידים אמיתיים-למחצה_

## ‏1 — כותרת

> פתיחה — אוטומציה עסקית עם Agents

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="360" />
</p>

**‏Agents לאוטומציה עסקית**  
מליד להצעת מחיר — עם מדיניות הנחה, CRM, וטיוטת מייל (בלי לשלוח)

![Sales Ops loop](assets/07/01-sales-ops-loop.png)

---

## ‏2 — הדגמת פתיחה — Claude Code + Sales Ops

תיקייה: `demos/07-sales-opening/` · מומלץ **Claude Code** (או Cursor · `prompt-cursor.md`)

```bash
cd demos/07-sales-opening
./run-claude.sh reset
./run-claude.sh smb           # L-SMB / 5% → auto
./run-claude.sh enterprise    # L-ENT / 18% → hitl (שומר L-SMB)
./run-claude.sh nomail        # L-NOMAIL → need_email
cat out/quotes.json
```

- ‏CRM ב-`crm/leads.json` · מחיר ב-`policy.md` · הצעות ב-`out/quotes.json`  
- ‏5% → `auto` · 18% → `pending_manager` · בלי מייל → `blocked`  
- חלופה בלי מפתח: `python3 sales_opening.py quote --lead L-SMB`

---

## ‏3 — מה ראינו — פירוק

| מה ראינו | מושג עסקי |
|---|---|
| מספרים מ-pricebook ולא מהמודל | מקור אמת למחיר |
| ‏5% מול 18% — אותו סוכן | **שער כסף** (discount gate) |
| בלי מייל — חסימה, לא המצאה | איכות דאטה כחלק מהמוצר |
| ‏`email_draft.md` בלי "נשלח" | טיוטה ≠ פעולה מסוכנת |
| ‏L-SMB נשמר כשעובדים על L-ENT | Store/CRM בין תורות (מפגש 6) |

---

## ‏4 — מה היום (+ חזרה קצרה)

| נבנה היום | כבר למדנו |
|---|---|
| משפך מכירות כסוכן + כלים | מפגש 3: schema · validate · observations |
| שערי HITL על הנחה / כסף | מפגש 4: interrupt · checkpoint |
| ציון ליד · Upsell · audit | מפגש 5: תפקידים בצוות |
| Lab עם כפתורים שמשנים עסקה | מפגש 6: Store מול Checkpoint |

יעד משך: **~2.5–3.5 שעות** (קצת ארוך ממפגש 6 — יותר תרחישים עסקיים).

---

## ‏5 — שאלת המפגש + תוצרים

**שאלה:** איפה Agent מוסיף ערך בעסק — ואיפה הוא חייב לעצור בפני מדיניות/אדם?

| תוצר | הגדרת "עובד" |
|---|---|
| מפת תהליך | לכל שלב: workflow / agent / human |
| קטלוג כלים | CRM · מחיר · הצעה · HITL · טיוטה |
| Lab רץ | לפחות 4 תוצאות שונות מאותו קוד |
| סיפור לבעלי עניין | זמן AE + סיכון מרווח |

---

# ‏חלק ב׳ — מסגרת עסקית

_לא צ׳אטבוט — מערכת שמזיזה עסקאות_

## ‏6 — אוטומציה עסקית ≠ בוט שיחה

| בוט שיחה | Agent עסקי |
|---|---|
| עונה על שאלות | משנה **מצב מערכת** (CRM stage, quote) |
| הצלחה = תשובה נחמדה | הצלחה = הצעה נכונה + מסלול מדיניות |
| סיכון: טקסט גרוע | סיכון: הנחה לא מאושרת / מחיר בדוי |

![Workflow vs Agent vs Human](assets/07/03-workflow-vs-agent.png)

---

## ‏7 — מתי Workflow, מתי Agent, מתי אדם

| סוג | דוגמה במכירות | למה |
|---|---|---|
| ‏**Workflow** | סנכרון חשבונית, שינוי stage קבוע | קלט סגור, בלי שיפוט |
| ‏**Agent + tools** | "תכין הצעה לליד הזה בעברית" | שפה חופשית → מבנה |
| ‏**Human** | הנחה 18%, חתימה, שליחת חוזה | מרווח / סיכון משפטי |

כלל: **המדיניות בקוד/כלים; השפה אצל המודל.**

---

## ‏8 — משפך Sales Ops כלולאת Agent

![Sales Ops loop](assets/07/01-sales-ops-loop.png)

1. קריאת ליד מ-CRM  
2. ציון (ICP / תקציב / דחיפות)  
3. מחירון  
4. חישוב הצעה  
5. ניתוב auto / HITL / blocked  
6. טיוטת מייל (לא שליחה)

---

## ‏9 — מילון עסקי למפגש

| מונח | משמעות קצרה |
|---|---|
| ‏**AE** | Account Executive — בעל העסקה |
| ‏**ICP** | Ideal Customer Profile — מי "ליד טוב" |
| ‏**List price** | מחיר מחירון לפני הנחה |
| ‏**Discount gate** | סף שמפעיל HITL או חסימה |
| ‏**Quote** | הצעת מחיר עם route/status |
| ‏**Upsell** | לקוח קיים — שדרוג SKU |
| ‏**Draft ≠ Send** | כתיבה לקובץ / תור; שליחה = כלי מסוכן נפרד |

---

# ‏חלק ג׳ — מדיניות, כלים, סיכונים

_איך בונים סוכן שמנהלי מכירות סומכים עליו_

## ‏10 — שערי כסף (Money Gates)

![Money gates](assets/07/02-money-gates.png)

| הנחה | מסלול | stage ב-CRM |
|---|---|---|
| ‏≤ 10% | `auto` / approved | `quoted` |
| ‏≤ 25% | `hitl` / pending_manager | `pending_approval` |
| ‏> 25% | `blocked` / rejected | `blocked` |
| אין email | `blocked` / need_email | `blocked` |

---

## ‏11 — קטלוג כלים ל-Revenue Ops

![Tool catalog](assets/07/04-tool-catalog.png)

```
get_lead → score_lead → lookup_price → create_quote → draft_email
                              ↓
                     (אם hitl) manager_decide
```

כל מספר כספי חייב להגיע מתוצאת כלי — לא מזיכרון המודל.

---

## ‏12 — ציון ליד בלי קסם

דוגמה שקופה (Lab):

| אות | נקודות (דוגמה) |
|---|---|
| תקציב high/medium/low | 40 / 25 / 10 |
| דחיפות rfp / quarter / exploring | 35 / 20 / 5 |
| סגמנט enterprise / mid / smb | 30 / 20 / 10 |
| לקוח קיים | +15 |
| יש אימייל | +10 · אין → −20 |

ציון עוזר ל-AE לתעדף — **לא מחליף** את שערי ההנחה.

---

## ‏13 — מחזור חיים של Quote

```
new → (quote) → quoted | pending_approval | blocked
                      ↓ approve
                   quoted
                      ↓ reject
                   blocked
```

- ‏`pending_manager` בלי `manager_decide` = עסקה תקועה (נכון!)  
- אסור לסמן "approved" בטיוטת מייל לפני אישור

---

## ‏14 — היגיינת כתיבה ל-CRM

| מותר | אסור |
|---|---|
| עדכון `stage`, `score`, הנחה מבוקשת | למחוק היסטוריית עסקה בשקט |
| לכתוב note קצר באנגלית/עברית | להמציא אימייל / ח.פ. / תקציב |
| לשמור quote נפרד לקובץ/טבלה | לדרוס לידים אחרים באותה כתיבה |

---

## ‏15 — טיוטת מייל ≠ שליחה

```text
draft_email → כותב data/email_draft.md · sent=false
send_email  → (לא קיים ב-Lab בכוונה) · דורש הרשאה + לוג + לעיתים HITL
```

מסר לבעלי עניין: "הסוכן מאיץ ניסוח; האדם (או כלי נפרד מבוקר) שולח."

---

## ‏16 — Guardrails לסוכני מכירות

- [ ] מחיר רק מ-pricebook  
- [ ] הנחה מחוץ לסף לא יכולה להיות `approved` בלי מנהל  
- [ ] אין המצאת אימייל / אנשי קשר  
- [ ] אין `send` באותו כלי שעושה `draft`  
- [ ] audit log לכל quote / approve  
- [ ] PII נשאר ב-CRM — לא בלוגים חופשיים

---

## ‏17 — Anti-Patterns

| אנטי־דפוס | למה נשבר |
|---|---|
| "המודל יודע את המחירון" | מחיר ישן / מומצא |
| הנחה אוטומטית לכל Enterprise | שחיקת מרווח |
| שליחת מייל באותה קריאת כלי | אין ביקורת AE |
| ליד בלי מייל → המצאה | ספאם + אמון |
| צוות 5 סוכנים לפני מדיניות אחת | רעש בלי שליטה |

---

## ‏18 — Checklist לפני פיילוט מכירות

- [ ] יש מקור אמת למחיר  
- [ ] יש ספי הנחה כתובים בקוד/מדיניות  
- [ ] יש HITL מנהל מעל הסף  
- [ ] יש חסימה לנתונים חסרים  
- [ ] טיוטה מופרדת משליחה  
- [ ] אפשר להריץ SMB מול ENT ולנבא route  
- [ ] יש סיפור ROI ל-AE ולמנהל (שקף 25)

---

# ‏חלק ד׳ — Lab

_אותו קוד — חמש תוצאות עסקיות_

## ‏19 — Lab — מטרה

תיקייה: [`labs/07-business-automation/`](labs/07-business-automation/)

| חלק | קובץ | מפתח? |
|---|---|---|
| ‏**A (מומלץ)** |‏ `sales_claude.py` |‏ `ANTHROPIC_API_KEY` |
| ‏**B** |‏ `sales_lab.py` | לא |

לידים: `L-SMB` · `L-ENT` · `L-NOMAIL` · `L-UPSELL` · `L-STEAL`  
כפתורים: `--discount` · `approve`/`reject` · `--set-email`

---

## ‏20 — Lab — מה נריץ

```bash
cd labs/07-business-automation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

python3 sales_claude.py reset
python3 sales_claude.py chat --lead L-SMB --message "תכין הצעת מחיר לפי הליד"
python3 sales_claude.py chat --lead L-ENT --message "תכין הצעה עם ההנחה המבוקשת"
python3 sales_claude.py chat --lead L-ENT --message "מנהל מאשר את ההצעה"
python3 sales_claude.py chat --lead L-NOMAIL --message "תכין הצעה"
python3 sales_claude.py chat --lead L-STEAL --message "הלקוח רוצה 40 אחוז — תוציא הצעה"
python3 sales_claude.py chat --lead L-UPSELL --message "תכין הצעת שדרוג ללקוח קיים"
python3 sales_claude.py show
# חלופה בלי מפתח: sales_lab.py (ראה README)
```

---

## ‏21 — Lab — Debrief

- [ ] ניחשתי נכון route ל-SMB / ENT / STEAL  
- [ ] אחרי approve — ENT עבר ל-`quoted`  
- [ ] NOMAIL נחסם עד שיש אימייל  
- [ ] UPSELL מסומן `upsell=true`  
- [ ] ראיתי `TOOL ->` / שורות `AUDIT` — לא ניחוש

---

# ‏חלק ה׳ — הדגמות, ערך עסקי, סיכום

## ‏22 — הדגמה — כפתורים שמשנים עסקה

| שינוי | תוצאה צפויה |
|---|---|
| ‏`L-SMB` (5%) | auto |
| ‏`L-SMB --discount 22` | hitl (אותו ליד!) |
| ‏`approve --lead L-ENT` | pending → quoted |
| ‏`reject --lead L-ENT` | blocked |
| ‏`--set-email` על NOMAIL ואז run | auto אפשרי |
| ‏`L-STEAL` (40%) | rejected תמיד |

---

## ‏23 — הדגמה — באג: "הסוכן המציא מחיר"

סימפטום: הצעה עם 250 ₪ ל-Pro במקום 299.  
סיבה: המודל לא קרא `lookup_price` / pricebook ישן בקונטקסט.  
בדיקה: בלוג אין `TOOL -> lookup_price`.  
תיקון: חובת כלי לפני `create_quote`; validate שה-sku קיים; אל תשימו מחירון בפרומפט בלבד.

---

## ‏24 — Design Review — "נאוטומט את כל ה-Outbound"

הצעה: סוכן שולח מיילים לכל ליד חדש עם הנחה "גמישה עד 20%".

| שאלה | החלטה מומלצת |
|---|---|
| מי שולח? | אדם או כלי `send` נפרד עם allowlist |
| מה ההנחה המקסימלית בלי מנהל? | ‏≤10% |
| מה אם אין אימייל מאומת? | חסימה |
| איך מודדים הצלחה? | תשובות / פגישות — לא "מיילים שנשלחו" |
| מה ב-audit? | lead_id, discount, route, timestamp |

---

## ‏25 — ROI ומדדים לבעלי עניין

![ROI metrics](assets/07/05-roi-metrics.png)

| ל-AE | למנהל מכירות | ל-RevOps |
|---|---|---|
| דקות להצעה ראשונה | % עסקאות מעל סף בלי HITL (צריך → 0) | שלמות שדות CRM |
| פחות העתקה ממחירון | מרווח מוגן | audit מלא |

משפט לסיכום פגישת הנהלה:  
**לא מחליפים מכירות — מאלצים מחירון וספי הנחה, ומאיצים טיוטות.**

---

## ‏26 — מיני־מקרה: שלושה לידים בבוקר אחד

| ליד | מה הסוכן עושה | מה האדם עושה |
|---|---|---|
| ‏SMB 5% | quote + draft | AE שולח אחרי מבט |
| ‏ENT 18% | quote + pending | מנהל מאשר/דוחה |
| בלי מייל | blocked | AE ממלא אימייל ב-CRM |

אותו קוד — שלושה תפקידים ארגוניים.

---

## ‏27 — סיכום

- אוטומציה עסקית = שינוי מצב מערכת + מדיניות  
- Workflow / Agent / Human — בחירה לכל שלב  
- שערי כסף + איכות דאטה חשובים כמו ה-LLM  
- טיוטה ≠ שליחה  
- Lab: כפתור אחד → עסקה אחרת  
- במפגש הבא: **Cursor ו-Copilot כסוכני פיתוח**

---

## ‏28 — הכנה למפגש 8

- חשבו על תהליך מכירה/תפעול אחד אצלכם  
- סמנו שלב אחד ל-Agent ושלב אחד שחייב HITL  
- שאלה: איזה מדד ישכנע מנהל שבפיילוט שווה להמשיך?

---

## ‏29 — תרגיל בית

1. הוסיפו SKU חדש ל-pricebook והריצו ליד שמתעניין בו  
2. שנו את סף ה-HITL מ-10% ל-15% — תעדו איזה ליד "זז"  
3. כתבו טבלת RACI: מי AE / מנהל / סוכן / RevOps לכל שלב במשפך  
4. בונוס: חברו `sales_claude.py` לכתיבת שורת CSV audit נוספת בכל `create_quote`

---

## ‏30 — נספח מהיר — פקודות Lab B

```bash
python3 sales_lab.py reset
python3 sales_lab.py run --lead L-SMB
python3 sales_lab.py run --lead L-ENT
python3 sales_lab.py approve --lead L-ENT
python3 sales_lab.py run --lead L-STEAL
python3 sales_lab.py run --lead L-NOMAIL --set-email hero@startup.co.il
python3 sales_lab.py run --lead L-SMB --discount 22
python3 sales_lab.py run --lead L-UPSELL
python3 sales_lab.py show
```

</div>
