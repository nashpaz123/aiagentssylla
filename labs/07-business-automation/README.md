<div dir="rtl" lang="he">

# ‏Lab 07 — Agents לאוטומציה עסקית (Sales Ops)

דורש **`ANTHROPIC_API_KEY`**. קובץ יחיד: `sales_claude.py`.

## ‏מטרה

| שלב | כלי / פעולה | תוצאה עסקית |
|---|---|---|
| קריאת ליד | `get_lead` | עובדות מ-CRM, לא מהמודל |
| ציון | `score_lead` | 0–100 לפי תקציב/דחיפות/סגמנט |
| מחיר | `lookup_price` | מחירון — אסור להמציא |
| הצעה | `create_quote` | ‏≤10% auto · ≤25% HITL · >25% blocked |
| מייל | `draft_email` | טיוטה בלבד (`sent=false`) |
| מנהל | `manager_decide` | אישור/דחייה להצעות HITL |
| השלמת מייל | `set_lead_email` | פותח ליד שנחסם ב-need_email |

כפתורים שמשנים תוצאה: לידים שונים · בקשת הנחה בהודעה · אישור/דחיית מנהל · השלמת אימייל.

## ‏התקנה

```bash
cd labs/07-business-automation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
# אופציונלי: export ANTHROPIC_MODEL=claude-sonnet-4-5
```

## ‏הרצה

```bash
python3 sales_claude.py reset
python3 sales_claude.py chat --lead L-SMB --message "תכין הצעת מחיר לפי הליד"
python3 sales_claude.py chat --lead L-ENT --message "תכין הצעה עם ההנחה המבוקשת"
python3 sales_claude.py chat --lead L-ENT --message "מנהל מאשר את ההצעה"
python3 sales_claude.py chat --lead L-NOMAIL --message "תכין הצעה"
python3 sales_claude.py chat --lead L-NOMAIL --message "המייל הוא hero@startup.co.il — עדכן והכן הצעה"
python3 sales_claude.py chat --lead L-STEAL --message "הלקוח רוצה 40 אחוז — תוציא הצעה"
python3 sales_claude.py chat --lead L-UPSELL --message "תכין הצעת שדרוג ללקוח קיים"
python3 sales_claude.py chat --lead L-SMB --message "תכין שוב עם 22 אחוז הנחה" --fresh-thread
python3 sales_claude.py show
```

בלוג חפשו `TOOL ->` — זו עבודת האוטומציה, לא "המודל ניחש".

## ‏מה לבדוק

- [ ] ‏L-SMB (5%) → `auto` / `quoted`
- [ ] ‏L-ENT (18%) → `hitl` ואחרי approve → `quoted`
- [ ] ‏L-NOMAIL → `need_email`; אחרי עדכון מייל אפשר להציע
- [ ] ‏L-STEAL (40%) → `blocked` / `rejected`
- [ ] ‏L-UPSELL → `upsell=true` בציטוט
- [ ] ‏SMB עם 22% בהודעה → HITL בלי שינוי קוד

</div>
