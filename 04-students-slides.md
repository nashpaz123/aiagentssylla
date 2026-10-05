<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 4 — מצגת סטודנטים
## ‏LangGraph לבניית Agents

> **משך משוער:** ~2.5–3 שעות (הוראה + Lab + הדגמות).  
> חזרה קצרה על מפגש 3 (Tools / MCP) — בלי פירוט מחדש.  
> מונחים - בסיסים עד מתקדמת.

---

# ‏חלק א׳ — פתיחה ומילון

## ‏1 — כותרת

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="360" />
</p>

**LangGraph**  
בניית Agents כגרף מצבים (State Graph)

![LangGraph Hero](assets/04/01-langgraph-hero.png)

---

## ‏2 — מה היום (+ חזרה קצרה על מפגש 3)

| נבנה היום | מפגש 3 (בקצרה) |
|---|---|
| גרף · Node · Edge · State | Tool Schema · Function Calling |
| Conditional edges · Loops | Validate · Parallel · Observations |
| Checkpoint · thread_id · HITL interrupt | MCP · PinchTab (דוגמה) |
| Lab: גרף קטן רץ בפייתון | Host שמריץ tool_calls |

לא חוזרים בפירוט על Schema — מניחים אותו כנתון.

---

## ‏3 — שאלת המפגש + תוצרים

> איך הופכים לולאת Agent לרשימת צעדים מפורשת שאפשר לעצור, לדבג, ולחדש?

בסוף המפגש תדעו:
1. להסביר Graph / Node / Edge / State בעברית פשוטה  
2. לבנות StateGraph קטן עם קשת מותנית  
3. להבין Checkpoint, thread_id, ו-interrupt ל-HITL  
4. להריץ Lab גרף בפייתון ולקרוא את הזרימה

---

## ‏4 — מילון ראשי תיבות (חובה)

| ראשי תיבות | פירוש מלא (EN) | בעברית פשוטה |
|---|---|---|
| **LLM** | Large Language Model | מודל שפה גדול (Claude / GPT וכו׳) |
| **API** | Application Programming Interface | ממשק תכנותי בין מערכות |
| **JSON** | JavaScript Object Notation | פורמט נתונים מובנה טקסטואלי |
| **SDK** | Software Development Kit | ערכת פיתוח / ספריות מוכנות |
| **HITL** | Human In The Loop | אדם בתוך הלולאה (אישור / התערבות) |
| **MCP** | Model Context Protocol | פרוטוקול לחיבור כלי-עזר לסוכנים |
| **RAG** | Retrieval-Augmented Generation | יצירה מועשרת בשליפה ממאגר |
| **FSM / State Machine** | Finite State Machine | מכונת מצבים — מצבים + מעברים |
| **DAG** | Directed Acyclic Graph | גרף מכוון בלי מעגלים |
| **LangGraph** | (שם ספרייה) | בניית Agents כגרף מצבים (יכול לכלול לולאות) |

הערה: LangGraph **מאפשר לולאות** — לא חייב להיות DAG.

---

## ‏5 — מה זה גרף? Node ו-Edge

![Graph Basics](assets/04/02-graph-basics.png)

- **Node (צומת):** פעולה / שלב  
- **Edge (קשת):** מעבר לשלב הבא  
- **Directed (מכוון):** החץ קובע כיוון  

דוגמה אנושית: בית קפה  
`הזמנה → הכנה → תשלום → מסירה`

---

## ‏6 — למה לא מספיק סקריפט ליניארי?

| סקריפט A→B→C | גרף עם החלטות |
|---|---|
| תמיד אותו סדר | לפעמים מדלגים / חוזרים |
| קשה לעצור באמצע ולחזור | Checkpoint בין צעדים |
| דיבאג = לקרוא לוג ארוך | דיבאג = איזה צומת רץ |

‏Agent אמיתי צריך **ענפים ולולאות** — לא רק צינור חד־כיווני.

---

# ‏חלק ב׳ — מהו LangGraph

## ‏7 — מה זה LangGraph?

**הגדרה:** ספרייה לבניית אפליקציות LLM כ**גרף מצבים** — עם לולאות, ענפים, ושמירת מצב.

```text
State + Nodes + Edges  →  compile()  →  invoke / stream
```

שייך למשפחת LangChain / LangSmith, אבל מתמקד ב**אורקסטרציה** (תזמור הצעדים), לא רק בשרשור פרומפטים.

---

## ‏8 — LangChain · LangGraph · LangSmith — מי זה מי

| שם | תפקיד קצר |
|---|---|
| **LangChain** | לבני קריאות ל-LLM, פרומפטים, שרשורים, אינטגרציות |
| **LangGraph** | תזמור זרימה כגרף (מצב, ענפים, לולאות, שמירה) |
| **LangSmith** | מעקב, לוגים, הערכה (Observability) |

אפשר לבנות Agent בלי LangChain המלא — אבל הרבה דוגמאות משלבות.

---

## ‏9 — מכונת מצבים (State Machine) בעברית

מכונת מצבים = רשימת **מצבים** + כללי **מעבר**.

דוגמה תמיכה:
`חדש → בבדיקה → ממתין לאישור → סגור`

ב-LangGraph:
- המצב החי = אובייקט **State**  
- המעבר = **Edge** (לפעמים מותנה)

---

## ‏10 — StateGraph — השלד

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    text: str

def shout(state: State) -> dict:
    return {"text": state["text"].upper()}

g = StateGraph(State)
g.add_node("shout", shout)
g.add_edge(START, "shout")
g.add_edge("shout", END)
app = g.compile()
print(app.invoke({"text": "hello"}))  # {'text': 'HELLO'}
```

---

# ‏חלק ג׳ — State

## ‏11 — מה זה State?

![Shared State](assets/04/03-shared-state.png)

**State** = תיבת הזיכרון המשותפת של הריצה.

כל Node:
1. קורא מה-State  
2. עושה עבודה  
3. מחזיר **עדכונים** (לא בהכרח את כל התיבה)

---

## ‏12 — TypedDict וחוזה השדות

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # מצטבר
    goal: str
    needs_hitl: bool
```

- שדות ברורים = פחות באגים  
- ‏`Annotated[..., add_messages]` = Reducer שמ**מוסיף** הודעות במקום לדרוס

---

## ‏13 — Reducer — למה אכפת לנו

| בלי Reducer חכם | עם Reducer מתאים |
|---|---|
| עדכון דורס ערך קודם | עדכון מתמזג לפי כלל |
| קל לאבד היסטוריית messages | ‏`add_messages` שומר רצף |

כלל אצבע: שדות-רשימה שצומחים לאורך הריצה כמעט תמיד צריכים Reducer.

---

## ‏14 — דוגמת State לסוכן תמיכה

```python
class SupportState(TypedDict):
    customer_id: str
    question: str
    messages: Annotated[list, add_messages]
    order_status: str | None
    draft_reply: str | None
    needs_hitl: bool
```

מי ממלא מה?
- קלט משתמש → `customer_id`, `question`  
- כלי → `order_status`  
- LLM → `draft_reply`, `messages`  
- Policy → `needs_hitl`

---

# ‏חלק ד׳ — Nodes ו-Edges

## ‏15 — Node = פונקציה עם חוזה

```python
def lookup_order(state: SupportState) -> dict:
    # כאן בדרך כלל Tool / API
    status = fake_get_order(state["customer_id"])
    return {"order_status": status}
```

כללי בריאות:
- קלט ברור מה-State  
- פלט = עדכונים בלבד  
- תופעות לוואי — רק כאן (לא ב-Edge)

---

## ‏16 — Edge רגיל מול Conditional Edge

![Conditional Edges](assets/04/04-conditional-edges.png)

```python
graph.add_edge("lookup", "draft")          # תמיד
graph.add_conditional_edges(
    "draft",
    route_after_draft,                     # פונקציית החלטה
    {"hitl": "approve", "end": END, "tools": "lookup"},
)
```

---

## ‏17 — START, END, ולולאות

```text
START → agent ⇄ tools → (maybe HITL) → END
```

לולאה חוקית ב-LangGraph:
`agent → tools → agent → …` עד תנאי עצירה.

בלי תנאי עצירה = לולאה אינסופית = חשבון עננים בוער.

---

## ‏18 — מתי Edge ומתי Logic בתוך Node?

| שמים ב-Edge | שמים ב-Node |
|---|---|
| לאן הולכים עכשיו | איך מבצעים פעולה |
| ‏if needs_hitl | קריאת API / LLM |
| עצירה / המשך | חישוב, פרסור, Validate |

אם צומת אחד עושה הכל כולל ניתוב — הגרף מאבד ערך.

---

# ‏חלק ה׳ — לולאת Agent + Tools

## ‏19 — חיבור למפגש 3: Tools בתוך Node

![Agent Tools Loop](assets/04/07-agent-tools-loop.png)

במפגש 3: המודל מציע `tool_calls` · Host מריץ · Observation חוזר.  
במפגש 4: אותו דבר — רק שה-Host הוא **גרף** עם צומת Agent וצומת Tools.

---

## ‏20 — should_continue — נתב פשוט

```python
def should_continue(state: AgentState) -> str:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    if state.get("needs_hitl"):
        return "hitl"
    return "end"
```

הנתב קורא State — לא מדבר עם הרשת.

---

## ‏21 — תנאי עצירה ו-Budget בגרף

עצרו כאשר:
- אין `tool_calls` ויש תשובה  
- ‏`step_count >= MAX_STEPS`  
- שגיאת Policy חוזרת  
- Confidence נמוך → HITL / Escalate  

שמרו `step_count` ב-State ועדכנו בכל סיבוב.

---

# ‏חלק ו׳ — Checkpoint ו-Threads

## ‏22 — מה זה Checkpoint?

![Checkpoint](assets/04/05-checkpoint.png)

**Checkpoint** = צילום State אחרי צעד (super-step).

מאפשר:
- להמשיך אחרי קריסה  
- HITL  
- דיבאג / Time travel (לפי יכולת הספרייה)

---

## ‏23 — thread_id — איזו שיחה זו?

```python
config = {"configurable": {"thread_id": "ticket-9912"}}
app.invoke(inputs, config=config)
# אחר כך:
app.invoke(None, config=config)  # ממשיך אותו thread (לפי דפוס הספרייה)
```

‏`thread_id` = מזהה חוט ריצה / שיחה.  
בלי אותו id — ה-Checkpointer לא יודע איזה מצב לטעון.

---

## ‏24 — Checkpointer: זיכרון מול דיסק

| סוג | שימוש |
|---|---|
| ‏InMemorySaver | למידה / טסטים — נמחק עם התהליך |
| Sqlite / Postgres וכו׳ | פרוד — שורד ריסטארט |

‏`compile(checkpointer=...)` מדליק שמירה.

---

# ‏חלק ז׳ — HITL ו-Interrupt

## ‏25 — interrupt — עצירה לאדם

![HITL Interrupt](assets/04/06-hitl-interrupt.png)

**רעיון:** הגרף מגיע לנקודה רגישה → `interrupt(...)` → ממתין לקלט חיצוני → `resume`.

דורש Checkpointer + `thread_id`.

---

## ‏26 — דוגמת מדיניות: מתי interrupt

| מצב | האם interrupt? |
|---|---|
| קריאת לוגים | לא |
| טיוטת מייל ללקוח | לרוב כן |
| Refund / Delete | כן / אסור |
| תשובת FAQ ודאית | לא |

חיבור ל-Policy Gate ממפגש 2–3 — עכשיו כצומת או כתנאי לפני צומת.

---

## ‏27 — Resume — איך ממשיכים

דפוס כללי:
1. ריצה נעצרת ב-interrupt  
2. מציגים לאדם את ה-payload  
3. ממשיכים עם פקודת resume (למשל `Command(resume=...)` לפי גרסת הספרייה)

האדם לא "מריץ את המודל" — הוא מחזיר ערך לגרף.

---

# ‏חלק ח׳ — דפוסים מתקדמים (מבוא)

## ‏28 — Fan-out / Fan-in

```text
        ┌→ metrics ┐
agent ──┼→ logs    ├──→ summarize → END
        └→ deploys ┘
```

מקביליות בגרף: כמה צמתים באותו super-step, אחר כך איסוף.

---

## ‏29 — Send / Map-Reduce (מבוא)

כשמספר המשימות דינמי (N כרטיסים, N קבצים):
- יוצרים שליחות דינמיות לכל פריט  
- אוספים תוצאות לסיכום  

זה נושא מתקדם — מספיק להכיר שקיים (`Send` ב-API של LangGraph).

---

## ‏30 — Subgraphs (מבוא)

גרף בתוך גרף = מודולריזציה.

דוגמה: גרף-על של Incident  
→ תת-גרף חקירת לוגים  
→ תת-גרף אישור שינוי  

טוב לצוותים גדולים · זהירות ממורכבות יתר.

---

## ‏31 — Streaming — לראות תוך כדי

```python
for event in app.stream(inputs, config=config):
    print(event)  # עדכונים לפי צומת / אירוע
```

שימושי ל-UI: להראות למשתמש התקדמות, לא רק תשובה סופית.

---

# ‏חלק ט׳ — מתי כן/לא ו-Anti-Patterns

## ‏32 — מתי לא להשתמש ב-LangGraph?

- סקריפט חד־פעמי בלי החלטות  
- צ׳אט פשוט בלי כלים  
- זרימה קבועה לגמרי שאפשר Workflow Engine רגיל  

‏LangGraph זורח כשיש **מצב + ענפים + לולאות + שמירה**.

---

## ‏33 — Anti-Patterns

1. צומת ענק אחד שעושה הכל  
2. לולאה בלי `MAX_STEPS`  
3. HITL בלי Checkpointer  
4. דריסת `messages` בלי Reducer  
5. ‏thread_id אקראי בכל בקשת HTTP  
6. לערבב ניתוב עסקי בתוך פרומפט בלבד בלי Edge

---

## ‏34 — Checklist תכנון גרף

- [ ] State מוגדר עם שדות עסקיים  
- [ ] Reducers לרשימות צומחות  
- [ ] צמתים קטנים עם אחריות אחת  
- [ ] Conditional edges במקום if ענק  
- [ ] Stop / Budget  
- [ ] Checkpoint אם יש HITL או פרוד  
- [ ] Trace: שם צומת + tool_call_id

---

# ‏חלק י׳ — Lab חי

## ‏35 — Lab: מטרה

**מטרה:** להריץ גרף LangGraph קטן מקומית, לראות State עובר בין צמתים, וקשת מותנית.

Lab: [`labs/04-langgraph-basics/`](labs/04-langgraph-basics/)

מגבלות:
- בלי חובת מפתח LLM (מצב דמו דטרמיניסטי)  
- אופציונלי: חיבור מודל אמיתי בהמשך

---

## ‏36 — Lab: מה נריץ

```bash
cd labs/04-langgraph-basics
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 graph_demo.py
```

תראו:
1. State התחלתי  
2. מעבר צמתים עם לוג  
3. ענף מותנה (קצר / ארוך)  
4. סיכום סופי

---

## ‏37 — Lab: Debrief

Checklist:
- [ ] יודע מה היה ב-State לפני/אחרי כל צומת  
- [ ] מבין למה נבחר הענף המותנה  
- [ ] יכול להוסיף צומת לוג אחד בעצמו  
- [ ] מבין למה עדיין אין כאן LLM חובה

---

# ‏חלק יא׳ — הדגמות פתרון

## ‏38 — הדגמה 1 — מציור לגרף

תרחיש: *״בדוק סטטוס הזמנה וענה ללקוח; אם refund — HITL.״*

על המסך נפרק ל:
`START → lookup → draft → route → (hitl|end)`

---

## ‏39 — הדגמה 1 — פתרון מבנה

```text
State: customer_id, question, order_status, draft, needs_hitl, messages
Nodes: lookup_order, draft_reply, hitl_approve
Edges: START→lookup→draft→(conditional)→hitl|END
hitl→END
```

---

## ‏40 — הדגמה 2 — באג Reducer

סימפטום: אחרי הצעד השני נעלמו הודעות ראשונות.

סיבה שכיחה: החזרתם `messages=[new]` בלי `add_messages`.

תיקון: Annotated + reducer, או להחזיר רק את התוספת לפי החוזה של הספרייה.

---

## ‏41 — הדגמה 3 — HITL בלי שמירה

סימפטום: אחרי אישור האדם הגרף מתחיל מאפס.

סיבה: אין Checkpointer או thread_id לא תואם.

תיקון: `compile(checkpointer=...)` + אותו `thread_id` ב-resume.

---

## ‏42 — הדגמה 4 — Design Review לגרף Incident

צמתים מוצעים: `fetch_metrics`, `fetch_logs`, `correlate`, `propose_action`, `hitl_action`, `execute_action`

תשובות שנקריא:
1. אילו מקביליים? metrics+logs  
2. היכן Budget? אחרי correlate  
3. היכן HITL? לפני execute_action  
4. מה ב-State? evidence[], hypothesis, approved_action

---

# ‏חלק יב׳ — סיכום

## ‏43 — סיכום

- גרף = Nodes + Edges + State  
- ‏LangGraph = תזמור Agent כגרף (עם לולאות)  
- Conditional edges = if/else מפורש  
- Checkpoint + thread_id = זיכרון ריצה  
- interrupt = HITL אמיתי  
- Tools ממפגש 3 חיים בתוך Nodes  
- מפגש 5: **CrewAI ו-Multi-Agent**

---

## ‏44 — הכנה למפגש 5

- ציירו 2–3 תפקידי סוכן לאותה משימה (למשל Researcher / Writer / Reviewer)  
- סמנו מי מדבר עם מי  
- שאלה: מתי Multi-Agent עוזר — ומתי הוא רעש?

---

## ‏45 — תרגיל בית

1. הוסיפו ל-Lab צומת אחד משלכם (למשל סופר מילים)  
2. הוסיפו ענף מותנה נוסף  
3. כתבו ב-5 שורות: מה היה ה-State לפני ואחרי  
4. בונוס: קראו מה זה RAG במשפט אחד בעברית שלכם

---

</div>
