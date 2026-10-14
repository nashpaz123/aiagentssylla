<div dir="rtl" lang="he">

# ‏Lab 06 — Memory & State Management

שני מסלולים (אותם מושגים):

| חלק | קובץ | מפתח? | מה מדגים |
|---|---|---|---|
| ‏**A (מומלץ)** |‏ `memory_claude.py` |‏ `ANTHROPIC_API_KEY` | סוכן Claude עם כלי Store + היסטוריית thread |
| ‏**B** |‏ `memory_lab.py` | לא | גרף LangGraph דטרמיניסטי (Checkpointer + Store) |

## ‏מטרה

| מנגנון | חיים | איפה |
|---|---|---|
| Thread / Working | בתוך שיחה | היסטוריית הודעות / Checkpointer |
| Store / Memory | בין ריצות |‏ `data/profiles.json` (+ כלים) |

שינוי קלט (`99`/`101`, `--fresh-thread`, `forget`) → תוצאה אחרת בהרצה הבאה.

## ‏התקנה

```bash
cd labs/06-memory-state
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## ‏חלק A — Anthropic (מומלץ)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# אופציונלי: export ANTHROPIC_MODEL=claude-sonnet-4-5

python3 memory_claude.py reset
python3 memory_claude.py chat --customer C-99 --message "אני רוצה החזר על 99 שקל"
python3 memory_claude.py chat --customer C-99 --message "מה הסטטוס של הבקשה שלי?"
python3 memory_claude.py chat --customer C-101 --message "אני רוצה החזר על 101 שקל"
# Checkpoint ריק, Store חי:
python3 memory_claude.py chat --customer C-99 --message "מה הסטטוס?" --fresh-thread
python3 memory_claude.py forget --customer C-99
python3 memory_claude.py chat --customer C-99 --message "מה הסטטוס?"
python3 memory_claude.py show
```

בלוג חפשו שורות `TOOL -> get_profile` / `save_profile` — זו קריאת ה-Memory המפורשת.

## ‏חלק B — בלי מפתח (LangGraph)

```bash
python3 memory_lab.py reset
python3 memory_lab.py chat --customer C-99 --amount 99
python3 memory_lab.py chat --customer C-99 --message "מה הסטטוס?"
python3 memory_lab.py chat --customer C-101 --amount 101
python3 memory_lab.py chat --customer C-101 --message "מה הסטטוס?" --thread other
python3 memory_lab.py forget --customer C-99
python3 memory_lab.py show
```

## ‏מה לבדוק

1. ‏99 → `auto` / 101 → `hitl`  
2. ‏`--fresh-thread` או `--thread other`: שיחה חדשה, Store עדיין זוכר  
3. ‏`forget` מוחק רק לקוח אחד  

חלופת הדגמה בלי Lab: `demos/06-memory-opening/` עם Claude Code / Cursor.

</div>
