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

## ‏מה לבדוק בהרצה

1. ‏CASE קצר (`hi there`) בוחר ענף `short` וממיר ל־UPPER  
2. ‏CASE ארוך בוחר ענף `long` ומייצר סיכום מקוצר  
3. ‏`step_log` מראה את סדר הצמתים  
4. שני המקרים מסיימים ב־`GOAL_COMPLETE: True`

## ‏מה הקוד מדגים

| רעיון | איפה בקוד |
|---|---|
| ‏State / TypedDict | `DemoState` |
| ‏Node | `normalize`, `handle_short`, `handle_long`, `summarize` |
| ‏Conditional Edge | `route_by_length` + `add_conditional_edges` |
| ‏START / END | חיבורי `add_edge` |

## ‏אתגר המשך (אופציונלי)

הוסיפו צומת `count_words` בין `normalize` לענפים, או שדה `word_count` ב-State.

## ‏ניקוי

אין משאבי ענן. אפשר למחוק `.venv` מקומית.

</div>
