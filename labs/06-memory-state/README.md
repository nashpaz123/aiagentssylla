<div dir="rtl" lang="he">

# ‏Lab 06 — Memory & State Management

**עלות:** אפס (בלי LLM). דורש `langgraph` (כמו מפגש 4).

## ‏מטרה

להבדיל בין:

| מנגנון | חיים | תפקיד במעבדה |
|---|---|---|
| ‏**Checkpointer** (`InMemorySaver` + `thread_id`) | בתוך ריצת תהליך / thread | שומר `messages` של השיחה |
| ‏**Store** (`data/profiles.json`) | בין ריצות / תהליכים | זוכר בקשת החזר של לקוח |

ולראות ששינוי קלט (`--amount` / `--customer` / `--thread` / `forget`) משנה תוצאה בהרצה הבאה.

## ‏התקנה

```bash
cd labs/06-memory-state
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## ‏הרצות מומלצות (שונות זו מזו)

```bash
# איפוס
python3 memory_lab.py reset

# 99 → auto, נשמר ב-Store
python3 memory_lab.py chat --customer C-99 --amount 99

# אותו לקוח, תור סטטוס — קורא מה-Store (גם אם זה תהליך חדש)
python3 memory_lab.py chat --customer C-99 --message "מה הסטטוס?"

# 101 → hitl
python3 memory_lab.py chat --customer C-101 --amount 101
python3 memory_lab.py chat --customer C-101 --message "מה הסטטוס?"

# אותו לקוח, thread אחר — ה-Checkpointer לא רואה את הודעות ה-thread הקודם,
# אבל ה-Store עדיין זוכר את הפרופיל (הבדל חשוב!)
python3 memory_lab.py chat --customer C-101 --message "מה הסטטוס?" --thread other-thread

# מוחקים רק את C-99 מה-Store — הסטטוס שלו ייעלם; C-101 נשאר
python3 memory_lab.py forget --customer C-99
python3 memory_lab.py chat --customer C-99 --message "מה הסטטוס?"
python3 memory_lab.py show
```

## ‏מה לבדוק בלוג

1. ‏`route=auto` מול `route=hitl` לפי סף 100.  
2. ‏`messages_in_thread` גדל כשנשארים באותו `--thread`.  
3. ‏`--thread other-thread`: Checkpoint חדש, אבל התשובה עדיין מה-Store.  
4. ‏`forget` מוחק Memory ארוך-טווח בלי למחוק את קוד הגרף.

## ‏קבצים

| קובץ | תפקיד |
|---|---|
| ‏`memory_lab.py` | גרף + CLI |
| ‏`data/profiles.json` | Store (נוצר בהרצה) |
| ‏`data/checkpoints.sqlite` | לוג thread פשוט להמחשה |

</div>
