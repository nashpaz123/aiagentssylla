<div dir="rtl" lang="he">

# ‏Lab 04 — LangGraph Basics

תרגיל למפגש 4. **עלות צפויה:** אפס (בלי קריאות LLM / בלי AWS).

## ‏מטרה

להריץ `StateGraph` קטן מקומית: State משותף, צמתים, וקשת מותנית (`short` / `long`) — בלי מפתח API.

## ‏דרישות

- Python 3.10+
- ‏`langgraph`, `langchain-core` (דרך `requirements.txt`)

אם `python3 -m venv` נכשל אצלכם (חסר `python3-venv`), אפשר במקום זאת:

```bash
pip3 install --user -r requirements.txt
python3 graph_demo.py
```

## ‏הרצה (מומלץ עם venv)

```bash
cd labs/04-langgraph-basics
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 graph_demo.py
```

## ‏מה לבדוק בהרצה (חלק 1 — `graph_demo.py`)

1. ‏CASE קצר (`hi there`) בוחר ענף `short` וממיר ל־UPPER  
2. ‏CASE ארוך בוחר ענף `long` ומייצר סיכום מקוצר  
3. ‏`step_log` מראה את סדר הצמתים  
4. שני המקרים מסיימים ב־`GOAL_COMPLETE: True`

## ‏חלק 2 — Checkpoint · thread_id · HITL (`hitl_demo.py`)

```bash
python3 hitl_demo.py approve   # או: python3 hitl_demo.py reject
```

מה לבדוק:

1. ‏CASE A — סכום 40: המדיניות לא דורשת אדם → `auto_approve`  
2. ‏CASE B — סכום 249: `interrupt()` עוצר, מודפס payload לאדם, `get_state` מראה `next = hitl_approve`, ואז `Command(resume=...)` ממשיך על **אותו** `thread_id`  
3. ‏CASE C — ‏`thread_id` אחר → `get_state` ריק (אין מאיפה להמשיך)

בלי `compile(checkpointer=...)` אין Checkpoint, ולכן אין עצירה והמשך — זה בדיוק הבאג מהדגמה 3 במפגש.

## ‏מה הקוד מדגים

| רעיון | איפה בקוד |
|---|---|
| ‏State / TypedDict | `DemoState`, `RefundState` |
| ‏Node | `normalize`, `handle_short`, `handle_long`, `summarize`, `lookup_order`, `policy` |
| ‏Conditional Edge | `route_by_length`, `route_after_policy` + `add_conditional_edges` |
| ‏START / END | חיבורי `add_edge` |
| ‏Checkpointer + thread_id | `InMemorySaver`, `{"configurable": {"thread_id": ...}}` |
| ‏HITL |‏ `interrupt(...)` ב-`hitl_approve`, `Command(resume=...)` |
| ‏Budget |‏ `MAX_STEPS` ב-`route_after_policy` |

## ‏אתגר המשך (אופציונלי)

הוסיפו צומת `count_words` בין `normalize` לענפים, או שדה `word_count` ב-State.

## ‏ניקוי

אין משאבי ענן. אפשר למחוק `.venv` מקומית.

</div>
