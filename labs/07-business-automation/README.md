<div dir="rtl" lang="he">

# ‏Lab 07 — Agents לאוטומציה עסקית (Sales Ops)

שני מסלולים (אותם מושגים עסקיים):

| חלק | קובץ | מפתח? | מה מדגים |
|---|---|---|---|
| ‏**A (מומלץ)** |‏ `sales_claude.py` |‏ `ANTHROPIC_API_KEY` | סוכן Claude עם כלי CRM/מחיר/הצעה/HITL |
| ‏**B** |‏ `sales_lab.py` | לא | אותו מנוע דטרמיניסטי + audit log |

## ‏מטרה

| שלב | כלי / פעולה | תוצאה עסקית |
|---|---|---|
| קריאת ליד | `get_lead` | עובדות מ-CRM, לא מהמודל |
| ציון | `score_lead` | 0–100 לפי תקציב/דחיפות/סגמנט |
| מחיר | `lookup_price` | מחירון — אסור להמציא |
| הצעה | `create_quote` | ‏≤10% auto · ≤25% HITL · >25% blocked |
| מייל | `draft_email` | טיוטה בלבד (`sent=false`) |
| מנהל | `manager_decide` | אישור/דחייה להצעות HITL |

כפתורים שמשנים תוצאה: `L-SMB` / `L-ENT` / `L-NOMAIL` / `L-UPSELL` / `L-STEAL` · `--discount` · `approve` · `--set-email`.

## ‏התקנה

```bash
cd labs/07-business-automation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## ‏חלק A — Anthropic (מומלץ)

```bash
export ANTHROPIC_API_KEY=sk-ant-...

python3 sales_claude.py reset
python3 sales_claude.py chat --lead L-SMB --message "תכין הצעת מחיר לפי הליד"
python3 sales_claude.py chat --lead L-ENT --message "תכין הצעה עם ההנחה המבוקשת"
python3 sales_claude.py chat --lead L-ENT --message "מנהל מאשר את ההצעה"
python3 sales_claude.py chat --lead L-NOMAIL --message "תכין הצעה"
python3 sales_claude.py chat --lead L-STEAL --message "הלקוח רוצה 40 אחוז — תוציא הצעה"
python3 sales_claude.py chat --lead L-UPSELL --message "תכין הצעת שדרוג ללקוח קיים"
python3 sales_claude.py show
```

בלוג חפשו `TOOL ->` — זו עבודת האוטומציה, לא "המודל ניחש".

## ‏חלק B — בלי מפתח

```bash
python3 sales_lab.py reset
python3 sales_lab.py run --lead L-SMB
python3 sales_lab.py run --lead L-ENT
python3 sales_lab.py approve --lead L-ENT
python3 sales_lab.py run --lead L-NOMAIL
python3 sales_lab.py run --lead L-NOMAIL --set-email hero@startup.co.il
python3 sales_lab.py run --lead L-STEAL
python3 sales_lab.py run --lead L-SMB --discount 22
python3 sales_lab.py run --lead L-UPSELL
python3 sales_lab.py show
```

## ‏מה לבדוק

- [ ] ‏L-SMB (5%) → `auto` / `quoted`
- [ ] ‏L-ENT (18%) → `hitl` ואחרי `approve` → `quoted`
- [ ] ‏L-NOMAIL → `need_email`; אחרי `--set-email` אפשר להציע
- [ ] ‏L-STEAL (40%) → `blocked` / `rejected`
- [ ] ‏L-UPSELL → `upsell=true` בציטוט
- [ ] שינוי `--discount 22` על SMB הופך HITL בלי שינוי קוד

</div>
