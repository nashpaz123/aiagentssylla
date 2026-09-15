<div dir="rtl">

# מפגש 2 — Agent Architecture: Planning ו-Execution
## קובץ מרצה (תסריט מלא להקלטה)

> **משך מיועד:** כ־2.5–3 שעות תוכן מוקלט + עצירות, הדגמות, תרגילים ושאלות  
> **מיקום בקורס:** מפגש 2  
> **מטרת המפגש:** להבין איך Agent הופך מטרה לתוכנית עבודה, איך הוא מבצע את התוכנית, איך הוא מגיב לכישלונות, מתי הוא מתכנן מחדש, ואיך מתכננים Execution Loop שאפשר לשלוט ולדבג.  
> **מצגת סטודנטים:** [`02-students-slides.md`](02-students-slides.md)  
> **נכסים:** `assets/02/`

> **הערת הקלטה:** צילומי המסך להדגמות נמצאים ב־`assets/screens/`.  
> בהקלטה עברו ביניהם לפי סדר התרחיש.  
> יצירה מחדש: `python3 scripts/gen_mock_uis.py`

---

# הנחיות למרצה

המסמך ממשיך את המבנה של מפגש 1.

הכותרות יכולות לשמש כשקופיות.

הטקסט שמתחתיהן מיועד להקראה ולכן הוא כתוב בצורה מדוברת, עם פסקאות לא ארוכות מדי.

הסימונים:

- **[מצלמה]** — הצעת צילום או מעבר זווית.
- **[תמונה]** — ויזואל מומלץ (מוטמע מ־`assets/02/` כשקיים).
- **[הדגמה]** — מעבר למסך, קוד או מערכת.
- **[שאלה]** — שאלה לקהל.
- **[עצירה]** — מקום טבעי לנשימה, הדגשה או מעבר.
- **[תרגיל]** — פעילות.
- **[B-ROLL]** — ויזואל שרץ בזמן ההקראה.

---

# חלק א' — פתיחה וחיבור למפגש הקודם

## שקופית 1 — הכותרת

**על המסך:**

> Agent Architecture  
> Planning ו-Execution

![Planning & Execution](assets/02/01-goal-plan-actions.png)

Agent יושב במרכז: משמאל מטרה ומשימות, מימין כלים ותוצאות, באמצע לולאת Decision → Action → Observation.

---

## שקופית 2 — איפה עצרנו?

[מצלמה: פריים בינוני.]

במפגש הקודם בנינו את היסודות.

דיברנו על ההבדל בין Workflow לבין Agent.

ראינו את הרעיון של:

Goal.

Decision.

Action.

Observation.

וראינו ש-Agent לא חייב לבצע מראש רשימה קשיחה של צעדים.

הוא יכול לקבל מטרה.

לקבל החלטה.

לבצע.

לראות מה קרה.

ואז להחליט שוב.

היום אנחנו לוקחים את הרעיון הזה ומכניסים אותו לתוך ארכיטקטורה.

---

## שקופית 3 — השאלה של היום

על המסך:

> **אם אני נותן ל-Agent מטרה גדולה — איך הוא יודע מה לעשות קודם?**

זו השאלה.

ואפשר מיד לתת לה תשובה פשוטה:

Planning.

אבל Planning הוא הרבה יותר מ"תרשום לי רשימה של משימות".

צריך להבין:

מתי מתכננים?

כמה מתכננים?

האם מתכננים הכול מראש?

מה עושים כשהתוכנית נשברת?

ומה קורה כשהתוכנית עצמה היא חלק מהבעיה?

---

# חלק ב' — מה זה Planning?

## שקופית 4 — תוכנית היא גשר בין מטרה לפעולה

**על המסך:**

```text
GOAL
  ↓
PLAN
  ↓
ACTIONS
  ↓
RESULT
```

כשאדם אומר:

"תארגן לי חופשה",

זו מטרה.

זו לא תוכנית.

כדי לבצע אותה צריך לפרק אותה.

לבדוק תאריכים.

לבדוק יעד.

לבדוק טיסות.

לבדוק מלון.

לבדוק תקציב.

ואולי לשנות את התוכנית אם משהו לא מסתדר.

Agent צריך להתמודד עם אותו רעיון.

---

## שקופית 5 — משימה פשוטה מול משימה מורכבת

משימה פשוטה:

> "בדוק אם שרת מסוים זמין."

משימה מורכבת:

> "חקור למה השירות לא יציב מאז הגרסה האחרונה, מצא את הסיבה הסבירה והכן תוכנית פעולה."

במשימה הראשונה כמעט אין צורך ב-Planning.

במשימה השנייה יש סדרה של החלטות.

וזה בדיוק המקום שבו Planning מתחיל להיות שימושי.

---

## שקופית 6 — Planning הוא לא בהכרח רשימה

אפשר לחשוב על תוכנית בכמה רמות.

לפעמים היא רשימה:

```text
1. Get logs
2. Check metrics
3. Check deployments
4. Analyze
```

אבל לפעמים היא יותר מופשטת:

```text
Investigate recent instability
```

ומתחת לזה Agent יחליט בזמן הביצוע אילו פעולות דרושות.

לכן Planning הוא ספקטרום.

יש Planning מלא מראש.

ויש Planning מקומי, רגע לפני כל פעולה.

---

# חלק ג' — Task Decomposition

## שקופית 7 — פירוק משימה

![Task Decomposition](assets/02/02-task-decomposition.png)

כשאנחנו מדברים על Task Decomposition, אנחנו בעצם אומרים:

קיבלתי משימה גדולה.

אני רוצה להפוך אותה לחלקים שאפשר לבצע.

---

## שקופית 8 — למה בכלל לפרק?

כי משימה גדולה היא בדרך כלל עמומה מדי לביצוע ישיר.

נניח שאמרנו:

> "שפר את ביצועי השירות."

מה זאת אומרת?

צריך קודם להבין מה הבעיה.

אולי CPU.

אולי Database.

אולי Network.

אולי Cache.

אולי קוד.

אי אפשר לבצע את המטרה כמו שהיא.

צריך לפרק אותה לשאלות יותר קטנות.

---

## שקופית 9 — Decomposition בדוגמת DevOps

המטרה:

> "מצא למה latency עלה."

אפשר לפרק:

```text
1. Check when latency increased
2. Compare with deployments
3. Check CPU / Memory
4. Check database latency
5. Inspect application logs
6. Correlate findings
7. Identify most likely cause
```

אבל שימו לב.

זו לא בהכרח התוכנית הנכונה.

אנחנו עדיין רק הצענו Hypothesis.

---

## שקופית 10 — תוכנית היא Hypothesis

זו נקודה חשובה.

אנחנו נוטים לחשוב על Plan כאילו הוא אמת.

אבל בפועל הוא יותר קרוב להשערה.

Agent אומר:

"זה כנראה המסלול שיעזור לי לפתור את הבעיה."

ואז הוא מתחיל לבצע.

אחרי הפעולה הראשונה יכול להיות שהכול משתנה.

---

# חלק ד' — Open-Loop Planning מול Closed-Loop Planning

## שקופית 11 — Open Loop

![Open vs Closed Loop](assets/02/03-open-vs-closed-loop.png)

**על המסך:**

```text
Plan
 ↓
Step 1
 ↓
Step 2
 ↓
Step 3
 ↓
Done
```

זה דומה לאוטומציה מסורתית.

התוכנית נקבעת מראש.

המערכת מבצעת.

היא לא משנה הרבה במהלך הדרך.

---

## שקופית 12 — Closed Loop

עכשיו:

```text
Plan
 ↓
Execute
 ↓
Observe
 ↓
Evaluate
 ↓
Re-plan?
 ↙      ↘
Yes      No
 ↓        ↓
Plan     Next step
```

זו כבר מערכת הרבה יותר דינמית.

Agent מקבל מידע חדש.

והמידע הזה יכול לשנות את מה שהוא עומד לעשות.

---

## שקופית 13 — למה Closed Loop מתאים ל-Agents?

כי העולם לא תמיד צפוי.

API יכול להיכשל.

Data יכול להיות חסר.

Tool יכול להחזיר משהו שלא ציפינו.

בעיה יכולה להיות שונה ממה שחשבנו.

ולכן:

> Plan טוב הוא לא בהכרח Plan שלא משתנה.

לפעמים Plan טוב הוא Plan שיודע להשתנות.

---

# חלק ה' — ReAct

## שקופית 14 — ReAct

![ReAct](assets/02/04-react.png)

על המסך:

> **Reason → Act → Observe → Reason**

ReAct הוא רעיון מרכזי להבנת Agentic behavior.

ה-Agent מקבל משימה.

הוא חושב איזה מידע חסר לו.

הוא מבצע פעולה.

הוא מסתכל על התוצאה.

ואז ממשיך מהנקודה הזאת.

---

## שקופית 15 — ReAct בדוגמה

משימה:

> "מצא למה ה-API מחזיר 500."

Agent:

**Reason**

אני צריך לראות Logs.

**Act**

קורא Tool של Logs.

**Observe**

אני רואה Database timeout.

**Reason**

עכשיו צריך לבדוק Database connectivity.

**Act**

קורא Tool נוסף.

**Observe**

Connection pool כמעט מלא.

**Reason**

זה נראה כמו כיוון חזק.

כאן אפשר לעצור או להמשיך לאסוף Evidence.

---

## שקופית 16 — היתרון של ReAct

לא צריך להחליט את כל הדרך מראש.

ה-Agent משתמש במידע החדש כדי לבחור את הפעולה הבאה.

זה מצוין כאשר הבעיה לא ידועה מראש.

אבל יש לזה גם מחיר.

אם כל צעד תלוי בהחלטה חדשה של המודל, ההתנהגות הופכת פחות צפויה.

---

## שקופית 17 — החיסרון

יותר החלטות אומרות:

יותר latency.

יותר Tokens.

יותר Tool Calls.

יותר הזדמנויות לטעות.

ולכן לפעמים דווקא Plan מראש נותן מערכת יציבה יותר.

---

# חלק ו' — Plan-and-Execute

## שקופית 18 — Plan-and-Execute

![Plan-and-Execute](assets/02/05-plan-and-execute.png)

גישה אחרת:

```text
Goal
 ↓
Planner
 ↓
Plan
 ↓
Executor
 ↓
Results
 ↓
Re-plan if needed
```

כאן מפרידים בין שני תפקידים.

Planner אומר:

"אלה המשימות."

Executor אומר:

"אני אבצע אותן."

---

## שקופית 19 — למה להפריד?

כי לפעמים אנחנו רוצים:

- תוכנית ברורה.
- יכולת לבדוק את התוכנית לפני ביצוע.
- Execution עקבי יותר.
- Human approval אחרי Planning.
- Debugging יותר קל.

למשל:

Agent מציע:

```text
1. Inspect deployment
2. Inspect logs
3. Compare release
4. Recommend rollback
```

אדם יכול להגיד:

"אל תעשה rollback."

ואז ההמשך משתנה.

---

## שקופית 20 — Planner מול Executor

**על המסך:**

```text
        Goal
         ↓
    ┌──────────┐
    │ Planner  │
    └────┬─────┘
         ↓
       Plan
         ↓
    ┌──────────┐
    │ Executor │
    └────┬─────┘
         ↓
       Tools
         ↓
      Results
         ↓
     Re-plan?
```

הפרדה כזאת מאפשרת לנו לחשוב על שני סוגים שונים של בעיות.

Planning problem.

Execution problem.

---

# חלק ז' — האם תמיד צריך Planner נפרד?

## שקופית 21 — לא בהכרח

אפשר להשתמש ב-LLM אחד שעושה הכול.

למשל:

```text
LLM
 ↓
Plan
 ↓
Tool
 ↓
Observation
 ↓
Next decision
```

אין כאן Planner ו-Executor נפרדים.

אותו מודל עושה את שני התפקידים.

---

## שקופית 22 — למה זה לפעמים עדיף?

כי זה פשוט יותר.

פחות Components.

פחות State.

פחות תקשורת.

פחות מורכבות.

ולמשימות קטנות, זה בדרך כלל מספיק.

---

## שקופית 23 — למה לפעמים כן להפריד?

כשיש לנו צורך בשליטה.

לדוגמה:

Planner:

```text
Generate plan
```

Policy Engine:

```text
Is this plan allowed?
```

Human:

```text
Approve?
```

Executor:

```text
Execute
```

עכשיו יש לנו נקודות בקרה.

---

# חלק ח' — Execution

## שקופית 24 — Planning בלי Execution לא שווה הרבה

אפשר לייצר Plan מדהים.

אבל אם המערכת לא יודעת לבצע אותו, לא השגנו כלום.

Execution הוא המקום שבו התוכנית פוגשת את העולם.

ה-Agent צריך:

לבחור Tool.

למלא פרמטרים.

להפעיל.

לקבל Result.

ולוודא שהתוצאה מתאימה למה שחשב.

---

## שקופית 25 — Execution Step

לכל Step אפשר לחשוב על ארבעה חלקים:

```text
Intent
 ↓
Tool Selection
 ↓
Tool Execution
 ↓
Result Validation
```

למשל:

Intent:

"אני צריך לבדוק את סטטוס ה-Pod."

Tool:

`get_pod_status`

Execution:

קוראים לכלי.

Validation:

האם באמת קיבלנו נתונים?

---

## שקופית 26 — Tool Success לא אומר Task Success

זו הבחנה חשובה.

הכלי יכול להצליח.

אבל המשימה עדיין יכולה להיכשל.

לדוגמה:

```text
get_logs() → HTTP 200
```

הכלי עבד.

אבל אולי הוא החזיר:

```text
No logs found
```

או אולי התוצאה לא רלוונטית.

לכן Execution צריך גם **Semantic Validation**.

---

# חלק ט' — Validation

## שקופית 27 — שלושה סוגי הצלחה

![Three kinds of success](assets/02/10-three-success.png)

### Transport Success

הקריאה הצליחה.

### Schema Success

קיבלנו מבנה תקין.

### Semantic Success

קיבלנו משהו שבאמת עוזר למשימה.

אלה שלוש רמות שונות.

---

## שקופית 28 — דוגמה

Tool:

```text
search_tickets()
```

HTTP:

```text
200 OK
```

JSON:

```json
{
  "tickets": []
}
```

הכול תקין מבחינת API.

אבל אם Agent חיפש תקלה ספציפית, התוצאה הריקה היא מידע חשוב.

היא לא אומרת "הכל בסדר".

היא אומרת:

> "לא מצאתי כאן את מה שחיפשתי."

---

# חלק י' — Failure Handling

## שקופית 29 — Agent תמיד ייתקל בכשלונות

![Failure Handling](assets/02/06-failure-handling.png)

מערכת אמיתית צריכה להתמודד עם:

```text
Tool timeout
Authentication failure
Bad parameters
Empty result
Rate limit
Network error
Unexpected data
Model mistake
```

ולכן Failure Handling צריך להיות חלק מהארכיטקטורה.

לא משהו שנוסיף אחרי שהמערכת כבר נשברת.

---

## שקופית 30 — Retry

התגובה הראשונה לכשל היא לפעמים Retry.

אבל Retry עיוור יכול להיות מסוכן.

אם Tool מחזיר:

```text
Invalid customer_id
```

לעשות אותו דבר שוב לא יעזור.

---

## שקופית 31 — Retry לפי סוג שגיאה

אפשר לחשוב על:

```text
Timeout
 → Retry

Rate limit
 → Wait + Retry

Invalid parameter
 → Fix + Retry

Permission denied
 → Stop / Escalate

Dangerous operation
 → Human approval
```

כלומר, ה-Agent לא רק שואל:

"נכשלתי?"

אלא:

> "איזה סוג כשלון קרה?"

---

## שקופית 32 — Exponential Backoff

[הדגמה על לוח או קוד]

אם שירות לא זמין זמנית, לא כדאי לעשות:

```text
retry
retry
retry
retry
```

ברצף.

אפשר להשתמש ב:

```text
1 sec
2 sec
4 sec
8 sec
...
```

עם מגבלה.

זה לא רעיון ייחודי ל-Agents.

זה עיקרון Software Engineering קלאסי.

אבל ב-Agent systems צריך לשלב אותו בתוך הלולאה.

---

# חלק יא' — Max Iterations

## שקופית 33 — למה צריך Limit?

נניח:

```text
Goal
 ↓
Try
 ↓
Fail
 ↓
Try another
 ↓
Fail
 ↓
Try another
 ↓
Fail
```

בלי מגבלה, Agent יכול להמשיך הרבה יותר זמן ממה שהתכוונו.

לכן צריך:

```text
MAX_ITERATIONS = 10
```

או Limit אחר שמתאים למערכת.

---

## שקופית 34 — Iteration Budget

אני אוהב לחשוב על זה כעל תקציב.

Agent קיבל:

- תקציב זמן.
- תקציב Tool Calls.
- תקציב Tokens.
- תקציב פעולות.

הוא צריך להשיג את המטרה בתוך הגבולות.

זו דרך טובה מאוד לחשוב על Production Agents.

---

# חלק יב' — Stop Conditions

## שקופית 35 — מתי Agent אומר "סיימתי"?

זה נשמע פשוט.

אבל בפועל זו אחת הבעיות.

אפשר להגדיר:

```text
Success condition
Failure condition
Timeout
Iteration limit
Human escalation
Confidence threshold
```

---

## שקופית 36 — Success Criteria

נניח שהמשימה היא:

> "צור דוח."

מה זה "סיימתי"?

האם:

קובץ קיים?

יש בו את כל הסעיפים?

הנתונים נבדקו?

הוא נשמר במקום הנכון?

מישהו אישר אותו?

Agent צריך לדעת מה נחשב הצלחה.

---

## שקופית 37 — Goal Completion Check

אפשר להוסיף שלב:

```text
Execute
 ↓
Evaluate
 ↓
Goal complete?
 ├── Yes → Finish
 └── No  → Continue
```

ה-Evaluate יכול להיות:

- Rule.
- Validator.
- Another LLM call.
- Human.
- שילוב שלהם.

---

# חלק יג' — Planning Granularity

## שקופית 38 — כמה לפרק?

זו שאלה מעשית.

אפשר ליצור:

```text
Task 1
Task 2
Task 3
```

או:

```text
Task 1.1
Task 1.2
Task 1.3
Task 2.1
...
```

יותר מדי פירוק יוצר:

יותר צעדים.

יותר State.

יותר Latency.

יותר נקודות כשל.

מעט מדי פירוק מקשה על Execution.

---

## שקופית 39 — כלל אצבע

לא לפרק לפי מספר צעדים יפה.

לפרק לפי יחידות משמעותיות.

כל Step צריך להיות משהו שאפשר:

- להבין.
- לבצע.
- לבדוק.
- להיכשל בו בצורה ברורה.

---

# חלק יד' — Dependencies בין משימות

## שקופית 40 — לא הכול חייב להיות סדרתי

נניח:

```text
Goal
 |
 +--> Search docs
 |
 +--> Search tickets
 |
 +--> Check release history
```

אפשר לעשות את שלושתם במקביל.

רק אחר כך:

```text
Results
   ↓
Analysis
```

זה נקרא Parallelization.

---

## שקופית 41 — למה זה חשוב?

כי Agentic systems יכולים להיות איטיים.

אם יש לנו שלושה Tools שלא תלויים אחד בשני:

```text
A → 2 sec
B → 3 sec
C → 4 sec
```

ביצוע סדרתי:

בערך 9 שניות.

ביצוע מקבילי:

קרוב יותר ל־4 שניות, בהנחה שאין overhead משמעותי.

---

## שקופית 42 — אבל Parallelization מוסיף מורכבות

צריך להתמודד עם:

- Concurrency.
- Race conditions.
- Rate limits.
- Partial failures.
- Aggregation.
- Ordering.

לכן לא עושים Parallelization רק כי אפשר.

עושים אותו כשהוא נותן ערך.

---

# חלק טו' — Conditional Execution

## שקופית 43 — תוכנית עם Branches

תוכנית לא חייבת להיות קו ישר.

לדוגמה:

```text
Get ticket
    |
    v
Is critical?
  /     \
Yes      No
 |        |
Human    Auto
approval handling
```

זה כבר Execution Graph.

---

## שקופית 44 — Agent צריך לבחור Branch

נניח:

```text
if severity == "low":
    continue automatically

if severity == "high":
    ask human
```

ה-Agent יכול להיות זה שמזהה את ה־severity.

אבל את המדיניות עצמה עדיף לעיתים להחזיק בקוד.

זה נותן שילוב טוב בין גמישות לשליטה.

---

# חלק טז' — Deterministic Code מול LLM Decisions

## שקופית 45 — מה כדאי להשאיר בקוד?

כלל שימושי:

> מה שלא צריך "חשיבה" — עדיף להגדיר באופן דטרמיניסטי.

לדוגמה:

```python
if severity == "critical":
    require_human_approval()
```

אין צורך לבקש מ־LLM להחליט אם Critical דורש אישור.

המדיניות כבר ידועה.

---

## שקופית 46 — ומה להשאיר ל-LLM?

דברים כמו:

- פרשנות.
- סיווג.
- בחירת כיוון חקירה.
- יצירת Hypotheses.
- בחירת Tool מתוך אפשרויות חוקיות.
- סיכום ממצאים.

זו נקודת ארכיטקטורה חשובה.

אנחנו לא בונים "AI במקום קוד".

אנחנו בונים:

> **AI בתוך מערכת תוכנה.**

---

# חלק יז' — דוגמה מלאה: Incident Agent

## שקופית 47 — הדרישה

![Incident Agent](assets/02/09-incident-agent.png)

[הדגמה]

![Metrics](assets/screens/metrics-dashboard.png)

![Kubernetes](assets/screens/k8s-pods-logs.png)

> "חקור Alert של latency גבוה בשירות API, מצא את הסיבה הסבירה והכן המלצה."

[מצלמה: מעבר למסך]

בואו לא נתחיל ישר עם קוד.

נתחיל מארכיטקטורה.

---

## שקופית 48 — Tools

```text
get_metrics()
get_logs()
get_events()
get_deployments()
get_recent_changes()
search_incidents()
```

יש לנו כלים לקריאת מידע.

בשלב הראשון אין Tool שמשנה Production.

זה חשוב.

---

## שקופית 49 — Initial Plan

ה-Agent יכול להתחיל:

```text
1. Confirm latency increase
2. Determine start time
3. Check recent deployments
4. Check resource metrics
5. Check logs
6. Search known incidents
7. Correlate findings
```

זה Plan התחלתי.

לא חוזה.

---

## שקופית 50 — Step 1

Tool:

```text
get_metrics(service="api")
```

Result:

```text
p95 latency:
80ms → 620ms
```

Observation:

הבעיה אמיתית.

וגם אפשר לראות שהשינוי התחיל לפני 30 דקות.

---

## שקופית 51 — Step 2

Agent בודק Deployment History.

Result:

```text
deployment api version 3.8.1
started 32 minutes ago
```

עכשיו יש Correlation.

אבל Correlation הוא לא הוכחה.

---

## שקופית 52 — Step 3

ה-Agent בודק Logs.

Result:

```text
database connection timeout
```

עכשיו יש Evidence נוסף.

הכיוון נהיה מעניין יותר.

---

## שקופית 53 — Re-planning

במקום להמשיך בדיוק לפי התוכנית המקורית, Agent יכול לשנות אותה.

תוכנית חדשה:

```text
1. Inspect DB timeout frequency
2. Compare before/after release
3. Check connection pool metrics
4. Search previous incidents
5. Estimate confidence
```

זו Re-planning.

---

## שקופית 54 — מה היה קורה ב-Workflow קבוע?

Workflow קבוע היה יכול לבצע:

```text
Metrics
Logs
Deployment
Events
Database
```

גם אם כבר קיבלנו את התשובה.

Agent יכול לבחור לעצור מוקדם.

או לבחור להעמיק במקום הנכון.

זה בדיוק הערך של Adaptation.

---

# חלק יח' — Evidence ו-Hypothesis

## שקופית 55 — Agent לא אמור להתאהב בהשערה הראשונה

נניח שראינו:

Deployment התחיל.

Latency עלה.

קל להגיד:

"מצאתי. Deployment אשם."

אבל אולי זו רק התאמה בזמנים.

יכול להיות שהבעיה בכלל ב־Database.

לכן Agent טוב צריך לחפש Evidence.

---

## שקופית 56 — Hypothesis Loop

```text
Hypothesis
   ↓
Evidence
   ↓
Supports?
 ├── Yes → Increase confidence
 └── No  → Change hypothesis
```

זו דרך מצוינת לחשוב על Agent לחקירה.

הוא לא רק מבצע.

הוא גם חוקר.

---

## שקופית 57 — Confidence

Confidence לא חייב להיות מספר מדויק.

אפשר לחשוב:

```text
Low
Medium
High
```

או:

```text
Evidence:
- Deployment correlation
- DB timeout increase
- Pool saturation
```

ומעל זה:

> "High confidence that the latency increase is related to database connection pressure after the recent release."

---

# חלק יט' — Re-planning בצורה נכונה

## שקופית 58 — מתי לעשות Re-plan?

לא בכל פעולה.

אחרת המערכת הופכת ליקרה מאוד.

אפשר לבצע Re-plan כאשר:

- התגלתה עובדה חדשה.
- Tool נכשל.
- התוכנית כבר לא רלוונטית.
- נמצאה דרך טובה יותר.
- נוצר Branch חדש.
- הגענו ל־risk threshold.

---

## שקופית 59 — Local Re-planning

לא חייבים לבנות תוכנית חדשה לכל המשימה.

לפעמים מספיק:

```text
Current step failed
 ↓
Choose alternative
```

זה Re-planning מקומי.

---

## שקופית 60 — Global Re-planning

בבעיה גדולה יותר:

```text
Original plan
 ↓
Major new evidence
 ↓
Discard plan
 ↓
Generate new plan
```

כאן Agent בעצם מתחיל לחשוב מחדש על המשימה.

---

# חלק כ' — Planning Errors

## שקופית 61 — תוכנית לא נכונה

יש כמה סוגים:

### Missing step

משהו חשוב לא נכלל.

### Wrong order

השלבים קיימים אבל בסדר לא נכון.

### Wrong assumption

התוכנית מניחה עובדה שאינה נכונה.

### Overplanning

יש יותר מדי צעדים.

### Underplanning

אין מספיק פירוט.

---

## שקופית 62 — דוגמה ל-Wrong Assumption

משימה:

> "פרסם את ה-Release."

Agent מניח:

```text
Build → Test → Deploy
```

אבל בפועל הארגון דורש:

```text
Build
→ Security Scan
→ Approval
→ Staging
→ Integration Test
→ Production Approval
→ Production
```

לכן Agent צריך לדעת את ה־Constraints של הסביבה.

---

# חלק כא' — Planning עם Constraints

## שקופית 63 — מטרה בלי Constraints לא מספיקה

אפשר להגיד:

> "Deploy the application."

אבל צריך גם:

```text
Allowed environments
Allowed hours
Required approvals
Rollback policy
Change window
Security requirements
```

Agent צריך להכיר את המסגרת שבתוכה הוא פועל.

---

## שקופית 64 — Constraint Layer

![Policy Gate](assets/02/07-policy-gate.png)

---

# חלק כב' — Planning כמשימה בפני עצמה

## שקופית 65 — Planner הוא גם Agent

שימו לב למשהו מעניין.

Planner עצמו יכול להיות LLM.

הוא מקבל:

Goal.

Context.

Constraints.

ומחזיר:

Plan.

אבל עכשיו יש לנו בעיה.

איך בודקים שה־Plan טוב?

---

## שקופית 66 — Plan Validation

אפשר לבדוק:

### Completeness

האם חסר שלב?

### Validity

האם השלבים בכלל אפשריים?

### Safety

האם קיימת פעולה מסוכנת?

### Dependencies

האם הסדר הגיוני?

### Cost

האם התוכנית יקרה מדי?

---

## שקופית 67 — Plan Review

לכן ארכיטקטורה מעניינת יכולה להיות:

```text
Goal
 ↓
Planner
 ↓
Plan
 ↓
Validator
 ↓
Policy
 ↓
Human? 
 ↓
Executor
```

יש הרבה מערכות אמיתיות שבהן דווקא החלק של Validation חשוב יותר מהחלק של Planning.

---

# חלק כג' — Execution State

## שקופית 68 — איך זוכרים איפה נמצאים?

![Execution State](assets/02/08-execution-state.png)

אם יש לנו:

```text
Task 1
Task 2
Task 3
Task 4
```

המערכת צריכה לדעת:

- מה כבר בוצע.
- מה הצליח.
- מה נכשל.
- מה עכשיו.
- מה מחכה.
- מה דילגנו עליו.

זה State.

---

## שקופית 69 — דוגמת State

```json
{
  "goal": "Investigate API latency",
  "current_step": "check_logs",
  "completed_steps": [
    "get_metrics",
    "get_deployments"
  ],
  "failed_steps": [],
  "findings": [
    "latency increased 32 minutes ago",
    "deployment 3.8.1 happened 35 minutes ago"
  ]
}
```

זה רק מבנה דוגמה.

בהמשך הקורס נלמד State ו-Memory בצורה עמוקה יותר.

---

## שקופית 70 — למה State חשוב?

בלי State, קשה מאוד לעשות:

Retry.

Resume.

Human approval.

Re-planning.

Debugging.

Multi-step execution.

State הוא הבסיס שעליו Agent יכול להמשיך לעבוד.

---

# חלק כד' — Human Approval בתוך Execution

## שקופית 71 — Approval באמצע תהליך

תהליך:

```text
Plan
 ↓
Inspect
 ↓
Prepare action
 ↓
Risk detected
 ↓
Human approval
 ↓
Execute
```

ה-Agent לא חייב להתחיל מהתחלה אחרי האישור.

הוא צריך להמשיך מהמקום שבו עצר.

לכן State חשוב.

---

# חלק כה' — Idempotency

## שקופית 72 — בעיה מאוד חשובה

נניח Agent ביצע:

```text
create_ticket()
```

הפעולה הצליחה.

אבל התשובה מהשרת אבדה.

Agent לא יודע אם זה הצליח.

מה הוא עושה?

אם הוא מריץ שוב, יכול להיות שנקבל שני Tickets.

---

## שקופית 73 — Idempotent Actions

אידמפוטנטיות אומרת, בפשטות:

פעולה שאפשר לבצע שוב בלי ליצור תוצאה לא רצויה כפולה, כאשר זו אותה בקשה.

לדוגמה, במקום:

```text
create_ticket()
```

אפשר להשתמש ב:

```text
create_ticket(idempotency_key="abc123")
```

והשרת יכול למנוע יצירה כפולה.

---

## שקופית 74 — למה Agent Systems צריכים את זה?

כי Agent עובד בעולם שבו:

- Requests יכולים להיכשל.
- Responses יכולים להיעלם.
- Retry קיים.
- זמן עובר.
- התהליך יכול להיפסק.

לכן כל פעולה משמעותית צריכה להיות מתוכננת גם במקרה שנצטרך לחזור עליה.

---

# חלק כו' — Timeouts

## שקופית 75 — Agent לא יכול לחכות לנצח

Tool יכול להיתקע.

API יכול להיות איטי.

Database יכול לא לענות.

צריך:

```text
Tool timeout
Agent timeout
Overall task timeout
```

אלו שלוש שכבות שונות.

---

## שקופית 76 — Timeout Strategy

למשל:

```text
Tool call:
30 sec

Agent run:
5 min

Daily batch:
30 min
```

המספרים כאן הם דוגמה.

העיקרון הוא לתת גבולות לכל שכבה.

---

# חלק כז' — Cost-Aware Planning

## שקופית 77 — Plan צריך לקחת בחשבון Cost

נניח שיש שתי אפשרויות.

### Option A

5 Tool Calls פשוטים.

### Option B

20 Tool Calls + מודל גדול + כמה Iterations.

שניהם אולי מגיעים לתשובה.

אבל Option B עולה יותר ולוקח יותר זמן.

לכן אפשר לבנות Planner שמעדיף:

> "המסלול הזול ביותר שנותן מספיק Evidence."

---

## שקופית 78 — Quality / Cost / Time

[על המסך]

```text
                Quality
                  /\
                 /  \
                /    \
               /      \
              /        \
          Cost -------- Time
```

ב-Agent Systems אנחנו כמעט תמיד מאזנים בין שלושה דברים:

איכות.

עלות.

זמן.

---

# חלק כח' — Context Planning

## שקופית 79 — גם מידע עולה כסף

Agent לא צריך לראות את כל העולם בכל צעד.

אם יש לנו אלפי Logs, אין סיבה לשלוח את כולם למודל.

Agent יכול לעבוד כך:

```text
Raw data
 ↓
Filter
 ↓
Relevant subset
 ↓
LLM
```

זו אחת הסיבות ש-Tool Design ו-Context Management כל כך חשובים.

---

## שקופית 80 — Tool שמחזיר יותר מדי מידע

Tool גרוע:

```text
get_logs()
→ 200,000 lines
```

Tool טוב יותר:

```text
get_logs(
  service,
  start_time,
  end_time,
  level,
  pattern
)
```

עכשיו Agent מקבל מידע יותר ממוקד.

---

# חלק כט' — Planning מול Prompting

## שקופית 81 — האם Prompt ארוך = Planning?

לא.

Prompt יכול להכיל:

> "תעשה את שלב 1, אחר כך שלב 2, אחר כך שלב 3..."

זה עדיין יכול להיות Workflow קשיח.

Planning אמיתי במערכת Agentic כולל אפשרות שהמערכת תחליט על הדרך בהתאם למטרה ולמצב.

---

## שקופית 82 — System Instructions

אנחנו יכולים להגיד:

> "השלם את המשימה תוך שמירה על המדיניות."

זה Constraint.

אנחנו לא חייבים להגיד בדיוק:

> "בצע Tool A ואז B ואז C."

זו הבחנה מאוד חשובה.

---

# חלק ל' — Demo Architecture

## שקופית 83 — נבנה מערכת קטנה

[הדגמה]

![CI console](assets/screens/ci-console.png)

![Demo: Plan then Execute](assets/02/demo-plan-execute.png)

בהקלטה: הציגו את הקונסול כ־Observation, ואז את רצף ה־re-plan.

[הדגמה]

המטרה:

> "מצא את הסיבה הסבירה לבעיית API."

Components:

```text
User
 ↓
Agent
 ↓
Tools
 ├── metrics
 ├── logs
 ├── deployments
 └── incidents
```

---

## שקופית 84 — Pseudocode

```python
goal = user_request

while not done:
    decision = llm(
        goal=goal,
        state=state,
        tools=available_tools
    )

    result = execute_tool(decision)

    state = update_state(state, result)

    if should_stop(state):
        done = True
```

הקוד כאן בכוונה פשוט.

המטרה היא לראות את העיקרון.

---

## שקופית 85 — מה חסר?

אם זה היה Production, היינו צריכים לפחות:

```text
Validation
Retries
Timeouts
Permissions
Logging
Tracing
Iteration limits
Error handling
Human approval
```

וזה בדיוק למה Agent Engineering הוא Software Engineering.

---

# חלק לא' — Demo: Plan First

## שקופית 86 — Planning לפני Execution

![Demo: Plan then Execute](assets/02/demo-plan-execute.png)

```python
plan = planner(goal, context)

if not validate(plan):
    plan = planner(goal, context, feedback="invalid plan")

for step in plan:
    result = execute(step)

    if needs_replanning(result):
        plan = replan(state)
```

שוב, זה Pseudocode.

אבל הוא נותן לנו מודל ארכיטקטוני.

---

# חלק לב' — תרגיל

## שקופית 87 — תרגיל: תכננו Agent

[תרגיל]

המטרה:

> "מצא למה Job ב-CI נכשל."

Tools:

```text
get_job_status()
get_console_log()
get_recent_changes()
get_runner_info()
search_previous_failures()
```

---

## שקופית 88 — שלב ראשון

בקשו מהקהל לכתוב:

> "מה ה-Agent צריך לדעת קודם?"

תנו כמה תשובות.

אולי:

Job status.

Failure time.

Build number.

Runner.

---

## שקופית 89 — שלב שני

שאלו:

> "האם חייבים לקרוא את כל ה-Tools?"

לא.

זו בדיוק הנקודה.

Agent צריך לבחור.

---

## שקופית 90 — שלב שלישי

עכשיו שנו את התרחיש.

`get_console_log()` נכשל.

שאלו:

> "מה עכשיו?"

אפשר:

Retry.

בדיקת Runner.

שימוש ב־Artifact.

Escalation.

Re-plan.

---

# חלק לג' — תרגיל מתקדם

## שקופית 91 — תרחיש

Agent מקבל:

> "פרוס את הגרסה החדשה ל-Production."

הוא יוצר תוכנית:

```text
1. Get latest image
2. Deploy
3. Check health
4. Notify team
```

שאלו:

> "מה חסר?"

---

## שקופית 92 — תשובות

Security scan.

Approval.

Staging.

Smoke tests.

Rollback plan.

Health criteria.

Monitoring.

Audit.

הנקודה היא ש־Planning טוב לא רק מחלק משימות.

הוא גם צריך לקחת בחשבון Constraints.

---

# חלק לד' — Anti-Patterns

## שקופית 93 — Anti-pattern #1

> **Plan Everything Forever**

Agent מנסה לתכנן 50 צעדים מראש.

הבעיה:

העולם ישתנה לפני שנגיע לצעד 20.

עדיף לפעמים לתכנן את הכיוון, ולא את כל הפרטים.

---

## שקופית 94 — Anti-pattern #2

> **Re-plan After Everything**

גם זה לא טוב.

אם אחרי כל Tool Call אנחנו יוצרים Plan חדש:

עלות עולה.

Latency עולה.

State גדל.

והמערכת יכולה להתחיל להתנדנד בין החלטות.

---

## שקופית 95 — Anti-pattern #3

> **LLM Decides Everything**

לא צריך לתת ל-LLM להחליט:

האם User מורשה.

האם Production change דורש Approval.

האם Resource מסוים אסור למחיקה.

דברים כאלה עדיף לקבע ב-Policy.

---

## שקופית 96 — Anti-pattern #4

> **No Validation**

Agent קיבל תשובה מהכלי.

ומיד ממשיך.

זה מסוכן.

צריך לשאול:

"האם התוצאה באמת אומרת את מה שאני חושב שהיא אומרת?"

---

## שקופית 97 — Anti-pattern #5

> **No Stop Condition**

Agent שמקבל:

> "מצא פתרון"

בלי Definition of Done.

עלול להמשיך לחפש פתרון גם כשהוא כבר מספיק טוב.

---

# חלק לה' — תכנון Production Agent

## שקופית 98 — Checklist

לפני Production, שאלו:

```text
Goal?
Plan?
Tools?
Constraints?
State?
Retries?
Timeout?
Max iterations?
Validation?
Stop condition?
Human approval?
Observability?
Permissions?
Cost limit?
```

זה Checklist טוב מאוד ל-Design Review.

---

# חלק מו' — Connection למפגשים הבאים

## שקופית 99 — עכשיו אנחנו צריכים Tools

במפגש הזה ראינו איך Agent מתכנן.

אבל עד עכשיו השתמשנו ב-Tools כאילו הם כבר קיימים.

במפגש הבא אנחנו נבנה את הדבר הזה.

איך מגדירים Tool?

איך מתארים אותו?

איך המודל מבקש להפעיל אותו?

איך אנחנו מעבירים Parameters?

ומה קורה כשה-Tool נכשל?

זה יוביל אותנו ל:

> **Tool Use ו-Function Calling**

---

## שקופית 100 — ומה אחר כך?

אחרי שנבין Tools, נוכל לבנות Agent הרבה יותר אמיתי.

כי אז יהיו לנו:

```text
Goal
 ↓
Planning
 ↓
Tool Selection
 ↓
Execution
 ↓
Observation
 ↓
Re-planning
```

זה כבר שלד של מערכת Agentic רצינית.

---

# חלק מז' — סיכום המפגש

## שקופית 101 — מה צריך לזכור?

Planning הוא הדרך שבה Agent מתרגם מטרה לפעולות.

Execution הוא המקום שבו הפעולות פוגשות את העולם.

Observation מאפשר ללמוד מהתוצאות.

Re-planning מאפשר לשנות כיוון.

Constraints ו-Policies שומרים על הגבולות.

Validation מוודא שלא רק ביצענו פעולה — אלא שהתקבלה תוצאה נכונה.

---

## שקופית 102 — המשפט המרכזי

על המסך:

> **Plan → Execute → Observe → Evaluate → Re-plan**

[מצלמה: פריים בינוני.]

זה אולי המשפט הכי חשוב של המפגש.

לא:

> Plan once.

אלא:

> Plan, execute, learn, and adapt.

אבל גם לא:

> Let the model do whatever it wants.

המטרה היא:

**Adaptive execution בתוך גבולות ברורים.**

---

# נספח א' — דיאגרמות נוספות

קבצים מוכנים תחת `assets/02/`:

| קובץ | שימוש |
|---|---|
| `01-goal-plan-actions.png` | פתיחה / Goal→Plan |
| `02-task-decomposition.png` | פירוק משימה |
| `03-open-vs-closed-loop.png` | Open/Closed loop |
| `04-react.png` | ReAct |
| `05-plan-and-execute.png` | Plan-and-Execute |
| `06-failure-handling.png` | Failure handling |
| `07-policy-gate.png` | Policy / Constraints |
| `08-execution-state.png` | State |
| `09-incident-agent.png` | Incident agent |
| `10-three-success.png` | סוגי הצלחה |
| `demo-plan-execute.png` | הדגמת טרמינל |

חידוש דיאגרמות: `python3 scripts/gen_diagrams.py`


## Diagram 1 — Agent Loop

```text
             ┌───────────┐
             │    GOAL   │
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │   PLAN    │
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │  EXECUTE  │
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │  OBSERVE  │
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │ EVALUATE  │
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │   DONE?   │
             └──┬─────┬──┘
               YES    NO
                │      │
                ↓      └────→ RE-PLAN
              RESULT
```

---

## Diagram 2 — Planner / Executor

```text
                 Goal
                  ↓
             ┌─────────┐
             │ Planner │
             └────┬────┘
                  ↓
                Plan
                  ↓
          ┌──────────────┐
          │ Policy Check │
          └──────┬───────┘
                 ↓
          ┌────────────┐
          │  Executor  │
          └──────┬─────┘
                 ↓
               Tools
                 ↓
              Results
                 ↓
             Re-plan?
```

---

## Diagram 3 — Parallel Execution

```text
              Goal
               ↓
             Plan
               ↓
       ┌───────┼───────┐
       ↓       ↓       ↓
     Tool A  Tool B  Tool C
       ↓       ↓       ↓
       └───────┼───────┘
               ↓
            Combine
               ↓
            Analyze
```

---

# נספח ב' — Prompts לתמונות

## תמונה 1 — Agent Planning

```text
Modern professional AI agent planning illustration.
An AI system receives a high-level business goal and visually
breaks it into several smaller tasks before execution.
Clear hierarchy from goal to plan to actions.
Enterprise technology training aesthetic, clean semi-realistic
illustration, dark neutral background, blue and violet accents,
16:9, no logos, no readable tiny text.
```

## תמונה 2 — Re-planning

```text
Educational visualization of an AI agent changing its execution plan
after discovering new information.
Show an original path splitting into a new path after an observation.
Clear arrows, clean technical architecture style, professional AI
engineering presentation, 16:9, dark modern background, minimal.
```

## תמונה 3 — Failure Handling

```text
AI agent execution flow encountering a tool failure and intelligently
choosing between retry, alternative action, or human escalation.
Professional software engineering diagram, modern enterprise AI style,
clear branching paths, minimal visual clutter, 16:9.
```

## תמונה 4 — Policy Gate

```text
AI agent creates a candidate plan that passes through a strict
policy and governance gate before execution.
Visualize a plan entering a checkpoint, with allowed and blocked
paths. Professional cloud and AI architecture illustration,
modern enterprise design, 16:9, minimal text.
```

## תמונה 5 — DevOps Investigation Agent

```text
AI agent investigating a production incident.
Central agent connected to Kubernetes, metrics, logs, deployment
history, incident database and monitoring systems.
Show the agent gathering evidence and changing its investigation path.
Professional DevOps and AI engineering presentation, modern dark
technology aesthetic, 16:9, no logos.
```

## תמונה 6 — State

```text
Technical visualization of an AI agent execution state.
Show current step, completed steps, failed steps, findings and
pending actions as structured state around a central agent.
Clean architecture diagram, professional enterprise AI training,
dark neutral background, 16:9.
```

---

# נספח ג' — קטעי B-ROLL

## B-ROLL 1

מסך עם Workflow ליניארי.

לעבור ממנו בהדרגה ללולאה עם חצים.

הקריינות:

> "בתהליך רגיל אנחנו יודעים הרבה פעמים מה הצעד הבא. ב-Agent, הצעד הבא יכול להיות תלוי במה שקיבלנו עכשיו."

---

## B-ROLL 2

טרמינל עם סדרת פקודות:

```text
kubectl get pods
kubectl get events
kubectl logs
```

הקריינות:

> "תחשבו על Agent כמו איש צוות שקיבל משימת חקירה. הוא לא חייב להריץ את כל הפקודות שיש לו. הוא בוחר את הכלי הבא לפי מה שכבר גילה."

---

## B-ROLL 3

דיאגרמת Plan.

לאחר מכן למחוק שלב ולהכניס שלב חדש.

הקריינות:

> "התוכנית היא לא חוזה. היא השערה לגבי הדרך הטובה להגיע למטרה."

---

# נספח ד' — משפטי מעבר להקלטה

### מעבר 1

"עכשיו כשהבנו מה זה Planning, בואו נראה למה תכנון מראש לא תמיד מספיק."

### מעבר 2

"וזה בדיוק המקום שבו נכנסת הלולאה."

### מעבר 3

"עכשיו נעבור מהתכנון עצמו אל הביצוע."

### מעבר 4

"ופה יש הבדל קטן אבל חשוב בין פעולה שהצליחה לבין משימה שהצליחה."

### מעבר 5

"עד עכשיו דיברנו על Agent שמתקדם. עכשיו בואו נדבר על Agent שנתקע."

### מעבר 6

"וכש-Agent נתקע, אנחנו לא רוצים רק Retry. אנחנו רוצים להבין למה הוא נכשל."

### מעבר 7

"עכשיו נוסיף מגבלות. כי Agent חכם בלי גבולות יכול להיות מערכת בעייתית מאוד."

### מעבר 8

"עכשיו ניקח את כל הרעיונות האלה ונחבר אותם לדוגמה אחת."

---

# נספח ה' — שאלות לקהל

## שאלה 1

מתי הייתם מעדיפים Workflow קבוע על Agent?

## שאלה 2

מתי כדאי לתכנן הכול מראש?

## שאלה 3

מתי עדיף Re-planning?

## שאלה 4

האם Tool שקיבל HTTP 200 בהכרח הצליח?

## שאלה 5

למה צריך Max Iterations?

## שאלה 6

מה ההבדל בין Tool Failure לבין Task Failure?

## שאלה 7

איזה דברים עדיף להשאיר בקוד ולא למסור להחלטת LLM?

---

# נספח ו' — מילון מונחים

## Planning

יצירת דרך אפשרית להגיע ממטרה לתוצאה.

## Task Decomposition

פירוק משימה גדולה לתת-משימות שאפשר לבצע.

## Execution

ביצוע בפועל של השלבים והתפעול מול Tools ומערכות חיצוניות.

## Re-planning

שינוי התוכנית בעקבות מידע חדש, כשל או שינוי במצב.

## ReAct

דפוס המבוסס על Reason → Act → Observe וחזרה להחלטה.

## Plan-and-Execute

הפרדה בין יצירת תוכנית לבין ביצוע התוכנית.

## Validation

בדיקה שהתוצאה שקיבלנו אכן תקינה ורלוונטית.

## Stop Condition

תנאי שמגדיר מתי המשימה הסתיימה, נכשלה או צריכה להיעצר.

## Iteration Limit

מגבלה על מספר מחזורי Agent.

## Idempotency

יכולת לבצע בקשה חוזרת בלי ליצור תוצאה כפולה או בלתי רצויה, כאשר אותה בקשה כבר טופלה.

## Constraint

גבול שהמערכת צריכה לעבוד בתוכו.

## Policy

כלל שמגדיר מה מותר ומה אסור.

## Execution State

המידע על מצב המשימה בזמן שהיא מתבצעת.

## Parallel Execution

הרצת מספר פעולות בלתי תלויות במקביל.

---

# נספח ז' — שאלת Design Review לסיום

## תרחיש

יש Agent שמקבל:

> "מצא את הסיבה לבעיה ב-Production ותקן אותה."

יש לו:

```text
read_logs()
get_metrics()
restart_service()
scale_service()
deploy_version()
delete_resource()
```

### שאלות

מה מותר לו לעשות אוטומטית?

מה צריך אישור?

איזה Tools מסוכנים מדי?

מה צריך להישאר דטרמיניסטי?

איך הייתם מגדירים Stop Condition?

איך הייתם מונעים לולאה אינסופית?

איך הייתם יודעים מה Agent עשה?

---

# שקופית סיום

## שקופית 103 — Planning הוא לא לנחש את העתיד

על המסך:

> **Planning = לבחור את הצעד הבא הטוב ביותר תחת מגבלות, ואז ללמוד מהתוצאה.**

[עצירה]

זה ההבדל בין Agent שמריץ Script.

לבין Agent שבאמת מנהל תהליך.

במפגש הבא נוסיף את אחד החלקים החשובים ביותר במערכת:

**Tools ו-Function Calling.**

שם ה-Agent מפסיק רק לחשוב על פעולות.

והמערכת מאפשרת לו לבצע אותן בפועל.

</div>
