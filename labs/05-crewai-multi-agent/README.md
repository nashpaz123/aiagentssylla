<div dir="rtl" lang="he">

# ‏Lab 05 — CrewAI & Multi-Agent

תרגיל למפגש 5. שני חלקים:

| חלק | קובץ | דורש מפתח API? | עלות |
|---|---|---|---|
| 1 |‏ `mini_crew.py` | לא | אפס |
| 2 |‏ `crew_demo.py` | כן (OpenAI / Anthropic) | כמה סנטים להרצה |

## ‏מטרה

להבין את אבני הבניין של Multi-Agent — **Agent · Task · Crew · Process** — ואת שלוש תבניות התזמור:
רציף (sequential), היררכי (manager), ולולאת Writer ⇄ Reviewer עם תקרת סבבים.

## ‏חלק 1 — בלי מודל (`mini_crew.py`)

```bash
cd labs/05-crewai-multi-agent
python3 mini_crew.py sequential
python3 mini_crew.py hierarchical
python3 mini_crew.py loop
```

מה לבדוק:

1. ‏`sequential` — שלוש משימות, כל אחת לסוכן אחר; הפלט של `research` נכנס כ-context ל-`write` ול-`review`.
2. ‏`hierarchical` — ה"מנהל" (כאן: פונקציה דטרמיניסטית, ב-CrewAI אמיתי: LLM) בוחר מי מבצע כל משימה.
3. ‏`loop` — הזמנה של 249: ה-Reviewer מחזיר `REVISE`, ה-Writer מתקן, סבב 2 מסתיים ב-`APPROVE`. שימו לב ל-`MAX_ROUNDS` ולשורת `tokens+=` של כל סוכן.

ניסוי מומלץ: שנו `MAX_ROUNDS = 1` והריצו `loop` שוב — תראו `ESCALATE_TO_HUMAN`. זו ההתנהגות הנכונה כשצוות לא מתכנס.

## ‏חלק 2 — CrewAI אמיתי (`crew_demo.py`)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt            # כולל crewai[anthropic] — נדרש למודל Anthropic
                                           # (לא: uv add — אין pyproject.toml בתיקייה זו)

# המפתח ו-CREW_MODEL חייבים להתאים לאותו ספק.
# ברירת המחדל של crew_demo.py היא openai/gpt-4o-mini — בלי CREW_MODEL יחפש OPENAI_API_KEY גם אם הגדרתם Anthropic.

# OpenAI:
export OPENAI_API_KEY=sk-...
export CREW_MODEL=openai/gpt-4o-mini

# Anthropic (שני השורות — לא רק המפתח):
export ANTHROPIC_API_KEY=sk-ant-...
export CREW_MODEL=anthropic/claude-sonnet-4-5

python3 crew_demo.py --dry-run             # בונה את הצוות בלי לקרוא למודל
python3 crew_demo.py                       # Process.sequential
python3 crew_demo.py hierarchical          # manager_llm מחלק משימות
```

אם מופיע `OPENAI_API_KEY is required` למרות ש־`ANTHROPIC_API_KEY` מוגדר — חסר `CREW_MODEL=anthropic/...`.  
אם מופיע `ImportError: Anthropic native provider not available` — חסר ה-extra:  
`pip install "crewai[anthropic]"` (או מחדש `pip install -r requirements.txt`). לא `uv add` בתיקייה זו.

מה לבדוק:

1. בלוג (`verbose=True`) רואים לכל סוכן: מחשבה → קריאת כלי (`get_order`) → תשובה. זו לולאת מפגש 1 בתוך כל Agent.
2. ‏`t_write.context=[t_research]` — ה-Writer מקבל את העובדות, לא את הטיקט הגולמי.
3. ה-Reviewer מחזיר `REVISE` אם סכום מעל 100 ללא אזכור אישור אדם.
4. ‏`hierarchical` יקר יותר בטוקנים — השוו את אורך הלוג.

להדלקת HITL: הסירו את ההערה מ-`human_input=True` במשימת `review`.

## ‏מה הקוד מדגים

| רעיון | ‏`mini_crew.py` | ‏`crew_demo.py` |
|---|---|---|
| ‏Agent (role / goal / tools) |‏ `Agent(...)` dataclass |‏ `crewai.Agent(role, goal, backstory, tools, llm)` |
| ‏Task (description / expected_output / context) |‏ `Task(...)` |‏ `crewai.Task(..., context=[...])` |
| ‏Crew + Process |‏ `Crew(process="sequential"/"hierarchical")` |‏ `Process.sequential` / `Process.hierarchical` + `manager_llm` |
| כלי ממפגש 3 |‏ `research()` קורא ל-dict |‏ `@tool("get_order")` |
| תקציב |‏ `TOKEN_BUDGET_PER_AGENT`, `MAX_ROUNDS` |‏ `max_iter` לכל Agent |
| ‏HITL |‏ `ESCALATE_TO_HUMAN` אחרי MAX_ROUNDS |‏ `human_input=True` |

## ‏ניקוי

אין משאבי ענן. אפשר למחוק `.venv` מקומית.

</div>
