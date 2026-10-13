<div dir="rtl" lang="he">

# ‏הדגמת פתיחה — מפגש 6: Checkpoint ≠ Memory

**משך:** ~4–6 דקות. **בלי מפתח API.**

מטרה: להראות שתור שני בלי Store מתחיל מאפס, ועם Store הסוכן "זוכר" בקשת החזר — כולל ההבדל 99 מול 101.

## ‏הרצה

```bash
cd demos/06-memory-opening

# 1) בלי זיכרון — תור 2 ריק
python3 memory_opening.py --mode none --amount 99

# 2) עם Store — תור 1 (99 → auto)
python3 memory_opening.py --mode store --customer C-99 --amount 99

# 3) אותו לקוח, תור סטטוס — זוכר
python3 memory_opening.py --mode store --customer C-99 --status

# 4) לקוח אחר, 101 → hitl
python3 memory_opening.py --mode store --customer C-101 --amount 101
python3 memory_opening.py --mode store --customer C-101 --status

# שינוי / ניקוי
python3 memory_opening.py --show
python3 memory_opening.py --forget --customer C-99
python3 memory_opening.py --reset
```

ה-Store נשמר ב-`out/profiles.json` (לא ב-git). שנו `--amount` / `--customer` והריצו שוב — התוצאה משתנה.

## ‏מה להגיד על המסך

1. ‏`--mode none`: "אין קובץ, אין זיכרון — תור 2 שואל מחדש."
2. ‏`--amount 99` ואז `--status`: "זוכר 99 ומסלול auto."
3. ‏`--amount 101`: "אותו קוד, מסלול hitl — שינוי קלט = שינוי התנהגות."
4. ‏זה **Memory / Store** בין ריצות. **Checkpoint** (מפגש 4) שומר מצב *בתוך* ריצה כדי להמשיך — נושא נפרד שנחדד במפגש.

</div>
