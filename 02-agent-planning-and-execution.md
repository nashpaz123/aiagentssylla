<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 2 — Agent Architecture: Planning ו-Execution
## ‏קובץ מרצה (תסריט מלא להקלטה)

> **משך מיועד:** כ־2.5–3 שעות תוכן מוקלט + עצירות, הדגמות, תרגילים ושאלות  
> **מיקום בקורס:** מפגש 2  
> **מטרת המפגש:** להבין איך Agent הופך מטרה לתוכנית עבודה, איך הוא מבצע, איך מגיבים לכישלונות, מתי מתכננים מחדש, ואיך בונים Execution Loop שאפשר לשלוט ולדבג.  
> **מצגת סטודנטים:** [`02-students-slides.md`](02-students-slides.md)  
> **נכסים:** `assets/02/` · `assets/screens/`

> **הערת הקלטה:** צילומי המסך להדגמות ב־`assets/screens/`.  
> יצירה מחדש: `python3 scripts/gen_mock_uis.py` · דיאגרמות: `python3 scripts/gen_diagrams.py`

---

# ‏הנחיות למרצה

בהקלטה: **מקריאים מכאן** ומציגים במקביל את [`02-students-slides.md`](02-students-slides.md).

הסימון **`[סטודנטים · N]`** = עברו ל־N במצגת הסטודנטים.  
**מספור המרצה = מספור הסטודנטים** (1…33). אין סעיפי תוכן באמצע בלי מספר סטודנטים תואם.

המסמך בנוי כמו מצגת־תסריט. הטקסט שמתחת לכותרות מיועד להקראה, עם פסקאות קצרות לנשימה.

- **[סטודנטים · N]** — מספר N במצגת הסטודנטים (גללו לשם לפני ההקראה).
- **[מצלמה]** — הצעה לצילום/מעבר זווית.
- **[תמונה]** — דיאגרמה או מסך על מצגת הסטודנטים.
- **[הדגמה]** — מעבר למסך / קונסול.
- **[שאלה]** — שאלה לקהל.
- **[עצירה]** — נשימה / הדגשה.
- **[תרגיל]** — פעילות עם שעון.

---

# ‏חלק א׳ — פתיחה וחיבור למפגש הקודם

## ‏1 — כותרת

[סטודנטים · 1]

**על המסך:** כותרת + לוגו + דיאגרמת Goal → Plan → Actions.

![Planning & Execution](assets/02/01-goal-plan-actions.png)

[מצלמה: פריים בינוני, חיוך קצר.]

ברוכים הבאים למפגש השני.

במפגש הקודם בנינו שפה משותפת: מהו Agent, במה הוא שונה מצ׳אט או מ-Workflow, ומה הספקטרום של אוטונומיה.

היום אנחנו יורדים קומה אחת למטה בארכיטקטורה.

השאלה היא לא רק "האם זה Agent".

השאלה היא: **איך הוא מתכנן, ואיך הוא מבצע בלי לאבד שליטה.**

[עצירה]

---

## ‏2 — איפה עצרנו?

[סטודנטים · 2]

[מצלמה: פריים בינוני.]

במפגש הקודם דיברנו על ארבע מילים:

Goal.

Decide.

Act.

Observe.

ראינו ש-Agent לא חייב לבצע מראש רשימה קשיחה של צעדים.

הוא יכול לקבל מטרה, להחליט, לבצע, לראות מה קרה — ואז להחליט שוב.

דיברנו גם על Spectrum: הרבה מוצרים נקראים Agent בלי agency אמיתית.

והדגשנו Tools ו-Guardrails.

היום אנחנו לוקחים את הלולאה הזו ומכניסים לתוכה שני מושגים מרכזיים:

**Planning** — איך נולדת דרך עבודה.

ו־**Execution** — איך הדרך פוגשת את העולם האמיתי, עם כישלונות, מדיניות ומצב.

[עצירה]

---

## ‏3 — השאלה של היום

[סטודנטים · 3]

על המסך:

> אם אני נותן ל-Agent מטרה גדולה — איך הוא יודע מה לעשות קודם?

זו השאלה שתלווה אותנו כל המפגש.

אפשר מיד לתת תשובה פשוטה: Planning.

אבל Planning הוא הרבה יותר מ"תרשום לי רשימה של משימות".

צריך להבין:

מתי מתכננים?

כמה מתכננים?

האם מתכננים הכול מראש?

מה עושים כשהתוכנית נשברת?

ומה קורה כשהתוכנית עצמה היא חלק מהבעיה?

[שאלה לקהל]

חשבו על משימה מהעבודה שלכם שהיא גדולה מדי לביצוע בפקודה אחת.

מה הצעד הראשון שהייתם עושים בעצמכם?

[עצירה]

---

# ‏חלק ב׳ — מה זה Planning?

## ‏4 — Planning = גשר

[סטודנטים · 4]

**על המסך:**

```text
GOAL → PLAN → ACTIONS → RESULT
```

כשאדם אומר "תארגן לי חופשה" — זו מטרה.

זו לא תוכנית.

כדי לבצע אותה צריך לפרק: תאריכים, יעד, טיסות, מלון, תקציב.

ואולי לשנות את התוכנית אם משהו לא מסתדר.

Agent צריך להתמודד עם אותו רעיון.

מטרה אומרת לאן רוצים להגיע.

תוכנית אומרת איך מנסים להגיע לשם עכשיו.

[עצירה]

הנקודה החשובה: מטרה ≠ תוכנית.

אם נותנים ל-Agent רק מטרה בלי מסגרת — הוא עלול לבחור מסלול יקר, מסוכן או לא רלוונטי.

Planning הוא הגשר.

---

## ‏5 — משימה פשוטה מול מורכבת

[סטודנטים · 5]

משימה פשוטה:

> "בדוק אם שרת מסוים זמין."

משימה מורכבת:

> "חקור למה השירות לא יציב מאז הגרסה האחרונה, מצא את הסיבה הסבירה והכן תוכנית פעולה."

במשימה הראשונה כמעט אין צורך ב-Planning עמוק.

יש כלי, יש בדיקה, יש תשובה.

במשימה השנייה יש סדרה של החלטות: מאיפה מתחילים, מה בודקים קודם, מתי עוצרים, מה נחשב "סיבה סבירה".

וזה בדיוק המקום שבו Planning מתחיל להיות שימושי.

[שאלה]

איזו משימה מהשבוע שלכם הייתה "פשוטה" ואיזו דרשה חקירה?

[עצירה]

---

## ‏6 — תוכנית = Hypothesis

[סטודנטים · 6]

זו נקודה שכדאי לחזור עליה בהקלטה לאט.

אנחנו נוטים לחשוב על Plan כאילו הוא אמת.

בפועל הוא יותר קרוב להשערה.

Agent אומר: "זה כנראה המסלול שיעזור לי לפתור את הבעיה."

ואז הוא מתחיל לבצע.

אחרי הפעולה הראשונה יכול להיות שהכול משתנה.

Planning הוא גם ספקטרום.

לפעמים התוכנית היא רשימה מפורטת:

```text
1. Get logs
2. Check metrics
3. Check deployments
4. Analyze
```

ולפעמים היא מופשטת יותר: "Investigate recent instability" — ומתחת לזה Agent מחליט בזמן הביצוע.

יש Planning מלא מראש.

ויש Planning מקומי, רגע לפני כל פעולה.

שניהם לגיטימיים — השאלה היא הקשר.

[עצירה]

---

# ‏חלק ג׳ — Task Decomposition

## ‏7 — Task Decomposition

[סטודנטים · 7]

![Task Decomposition](assets/02/02-task-decomposition.png)

[תמונה על המסך]

כשאנחנו מדברים על Task Decomposition, אנחנו אומרים:

קיבלתי משימה גדולה.

אני רוצה להפוך אותה לחלקים שאפשר לבצע.

למה לפרק?

כי משימה גדולה היא בדרך כלל עמומה מדי לביצוע ישיר.

"שפר את ביצועי השירות" — מה זאת אומרת?

CPU? Database? Network? Cache? קוד?

אי אפשר לבצע את המטרה כמו שהיא.

צריך לפרק לשאלות קטנות יותר.

[עצירה]

כלל אצבע: לא לפרק לפי מספר צעדים יפה.

לפרק לפי יחידות משמעותיות.

כל Step צריך להיות משהו שאפשר להבין, לבצע, לבדוק, ולהיכשל בו בצורה ברורה.

פירוק דק מדי יוצר רעש, State כבד ו-latency.

פירוק גס מדי מקשה על שליטה ועל Debugging.

---

## ‏8 — Decomposition בדוגמה

[סטודנטים · 8]

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

אבל שימו לב — זו לא בהכרח התוכנית הנכונה.

אנחנו עדיין רק הצענו Hypothesis.

יכול להיות שאחרי הצעד הראשון נגלה שהעלייה הייתה קצרה ונעלמה — ואז נשנה כיוון.

[עצירה]

---

# ‏חלק ד׳ — Open Loop מול Closed Loop

## ‏9 — Open Loop מול Closed Loop

[סטודנטים · 9]

![Open vs Closed Loop](assets/02/03-open-vs-closed-loop.png)

Open Loop דומה לאוטומציה מסורתית:

Plan → Step 1 → Step 2 → Step 3 → Done.

התוכנית נקבעת מראש.

המערכת מבצעת.

היא לא משנה הרבה במהלך הדרך.

Closed Loop אחרת לגמרי:

Plan → Execute → Observe → Evaluate → Re-plan?

Agent מקבל מידע חדש.

והמידע הזה יכול לשנות את מה שהוא עומד לעשות.

[עצירה]

למה Closed Loop מתאים ל-Agents?

כי העולם לא תמיד צפוי.

API יכול להיכשל.

Data יכול להיות חסר.

Tool יכול להחזיר משהו שלא ציפינו.

בעיה יכולה להיות שונה ממה שחשבנו.

ולכן המשפט שכדאי לזכור:

> Plan טוב הוא לא בהכרח Plan שלא משתנה.

לפעמים Plan טוב הוא Plan שיודע להשתנות.

[שאלה]

מתי הייתם מעדיפים Open Loop קבוע על Closed Loop?

---

# ‏חלק ה׳ — ReAct

## ‏10 — ReAct

[סטודנטים · 10]

![ReAct](assets/02/04-react.png)

על המסך: Thought → Action → Observation (חוזר).

ReAct הוא רעיון מרכזי להבנת Agentic behavior.

ה-Agent מקבל משימה.

הוא חושב איזה מידע חסר לו.

הוא מבצע פעולה.

הוא מסתכל על התוצאה.

ואז ממשיך מהנקודה הזאת.

היתרון: לא צריך להחליט את כל הדרך מראש.

ה-Agent משתמש במידע החדש כדי לבחור את הפעולה הבאה.

זה מצוין כאשר הבעיה לא ידועה מראש.

החיסרון: יותר החלטות אומרות יותר latency, יותר Tokens, יותר Tool Calls, יותר הזדמנויות לטעות.

בלי תקציב איטרציות — ReAct יכול להתפזר.

[עצירה]

---

## ‏11 — ReAct בדוגמה

[סטודנטים · 11]

משימה: "מצא למה ה-API מחזיר 500."

Agent חושב: אני צריך לראות Logs.

Act: קורא Tool של Logs.

Observe: Database timeout.

Reason: עכשיו צריך לבדוק Database connectivity.

Act: Tool נוסף.

Observe: Connection pool כמעט מלא.

Reason: זה נראה כמו כיוון חזק.

כאן אפשר לעצור עם Evidence — או להמשיך לאסוף.

[עצירה]

שימו לב מה קרה: אף אחד לא כתב מראש "אחרי Logs לך ל-pool".

הצעד הבא נולד מהתצפית.

זו הגמישות של ReAct — וגם הסיכון שלה אם אין Stop.

---

# ‏חלק ו׳ — Plan-and-Execute

## ‏12 — Plan-and-Execute

[סטודנטים · 12]

![Plan-and-Execute](assets/02/05-plan-and-execute.png)

גישה אחרת:

Goal → Planner → Plan → Executor → Results → Re-plan if needed.

כאן מפרידים בין שני תפקידים.

Planner אומר: אלה המשימות.

Executor אומר: אני אבצע אותן.

למה להפריד?

כי לפעמים רוצים תוכנית ברורה.

יכולת לבדוק את התוכנית לפני ביצוע.

Execution עקבי יותר.

Human approval אחרי Planning.

Debugging יותר קל.

למשל Agent מציע:

```text
1. Inspect deployment
2. Inspect logs
3. Compare release
4. Recommend rollback
```

ואדם יכול לאשר או לחסום לפני שהמערכת נוגעת בפרודקשן.

[עצירה]

---

## ‏13 — מתי Planner נפרד?

[סטודנטים · 13]

לא תמיד חייבים Planner נפרד.

במשימות קצרות, ReAct פשוט יכול להספיק — פחות State, פחות עלות.

Planner נפרד מתחיל להשתלם כשיש תוכנית ארוכה שרוצים לבדוק, Policy Gate, Approval, או סיכון גבוה.

[שאלה]

אם הייתם בונים Agent לפתיחת Ticket בלבד — הייתם מפרידים Planner?

ואם Agent שמשנה Production — מה אז?

[עצירה]

המסר: הארכיטקטורה נגזרת מהסיכון ומהמורכבות — לא מהטרנד.

---

# ‏חלק ז׳ — Execution ו-Validation

## ‏14 — שלושה סוגי הצלחה

[סטודנטים · 14]

![Three kinds of success](assets/02/10-three-success.png)

Planning בלי Execution לא שווה הרבה.

Execution הוא המקום שבו התוכנית פוגשת את העולם.

לכל Step אפשר לחשוב על: Intent → Tool Selection → Tool Execution → Result Validation.

והבחנה קריטית:

**Tool Success לא אומר Task Success.**

הכלי יכול להחזיר HTTP 200 — אבל המשימה עדיין נכשלה.

שלושה סוגי הצלחה על המסך:

1. Tool success — הכלי עבד.  
2. Step success — קיבלנו מידע שימושי.  
3. Goal success — המטרה באמת הושגה.

[עצירה]

אם זוכרים רק משפט אחד מהמפגש — זה יכול להיות המשפט הזה.

---

## ‏15 — Validation בדוגמה

[סטודנטים · 15]

Tool: `search_tickets()`

HTTP: 200 OK

JSON: `{ "tickets": [] }`

הכול תקין מבחינת API.

אבל אם Agent חיפש תקלה ספציפית, התוצאה הריקה היא מידע חשוב.

היא לא אומרת "הכל בסדר".

היא אומרת: "לא מצאתי כאן את מה שחיפשתי."

לכן Execution צריך גם Semantic Validation — לא רק בדיקת סטטוס קוד.

[שאלה]

האם Tool שקיבל HTTP 200 בהכרח הצליח עבור המשימה?

[עצירה]

---

# ‏חלק ח׳ — Failure Handling וגבולות

## ‏16 — Failure Handling

[סטודנטים · 16]

![Failure Handling](assets/02/06-failure-handling.png)

Agent תמיד ייתקל בכשלונות בעולם אמיתי:

Timeout, Authentication failure, Bad parameters, Empty result, Rate limit, Network error, Unexpected data, Model mistake.

Failure Handling צריך להיות חלק מהארכיטקטורה — לא משהו שמוסיפים אחרי שהמערכת כבר נשברת.

Retry הוא לא תשובה אוטומטית.

אם הכלי מחזיר Invalid customer_id — לעשות אותו דבר שוב לא יעזור.

Retry לפי סוג שגיאה:

Timeout → Retry.

Rate limit → Wait + Retry.

Invalid parameter → Fix + Retry.

Permission denied → Stop / Escalate.

Dangerous operation → Human approval.

ואפשר Exponential Backoff — עיקרון Software Engineering קלאסי שצריך לשבת בתוך ה-Loop של ה-Agent.

[עצירה]

---

## ‏17 — Max Iterations ו-Stop Conditions

[סטודנטים · 17]

בלי מגבלה, Agent יכול להמשיך הרבה יותר זמן ממה שהתכוונו:

Try → Fail → Try another → Fail → …

לכן צריך Limit: למשל MAX_ITERATIONS = 10 — או תקציב אחר.

אני אוהב לחשוב על זה כעל **Iteration Budget**:

תקציב זמן, Tool Calls, Tokens, פעולות.

Agent צריך להשיג את המטרה בתוך הגבולות.

ומתי אומרים "סיימתי"?

Success condition, Failure condition, Timeout, Iteration limit, Human escalation, Confidence threshold.

גם "צור דוח" דורש הגדרה: האם הקובץ קיים מספיק? האם הנתונים נבדקו? האם מישהו אישר?

Agent צריך לדעת מה נחשב הצלחה.

[עצירה]

---

# ‏חלק ט׳ — מבנה תוכנית והחלטות

## ‏18 — Dependencies ו-Branches

[סטודנטים · 18]

לא הכול חייב להיות סדרתי.

Search docs, Search tickets, Check release history — לפעמים אפשר במקביל, ואז Analysis.

Parallelization חוסך זמן — ומוסיף מורכבות: Concurrency, Race conditions, Rate limits, Partial failures, Aggregation.

לא עושים Parallelization רק כי אפשר.

תוכנית גם לא חייבת להיות קו ישר — יש Branches.

Is critical? → Human approval או Auto handling.

Agent יכול לזהות את ה־Severity.

את המדיניות עצמה — עדיף לעיתים להחזיק בקוד.

[עצירה]

---

## ‏19 — קוד דטרמיניסטי מול LLM

[סטודנטים · 19]

כלל שימושי:

> מה שלא צריך "חשיבה" — עדיף להגדיר באופן דטרמיניסטי.

לדוגמה בקוד:

```python
if severity == "critical":
    require_human_approval()
```

אין צורך לבקש מ־LLM להחליט אם Critical דורש אישור.

מה להשאיר למודל: פרשנות, סיווג, בחירת כיוון חקירה, Hypotheses, בחירת Tool מתוך אפשרויות חוקיות, סיכום ממצאים.

אנחנו לא בונים "AI במקום קוד".

אנחנו בונים: **AI בתוך מערכת תוכנה.**

[שאלה]

איזה דברים בעבודה שלכם עדיף להשאיר בקוד ולא למסור להחלטת LLM?

[עצירה]

---

# ‏חלק י׳ — דוגמה והדגמה

## ‏20 — דוגמה מלאה: Incident Agent

[סטודנטים · 20]

![Incident Agent](assets/02/09-incident-agent.png)

[הדגמה / B-ROLL]

![Metrics](assets/screens/metrics-dashboard.png)

![Kubernetes](assets/screens/k8s-pods-logs.png)

הדרישה:

> "חקור Alert של latency גבוה בשירות API, מצא את הסיבה הסבירה והכן המלצה."

Tools בשלב הראשון — קריאה בלבד:

get_metrics, get_logs, get_events, get_deployments, get_recent_changes, search_incidents.

אין Tool שמשנה Production. זה חשוב.

Initial Plan לדוגמה:

Confirm latency → start time → deployments → resources → logs → known incidents → correlate.

Step 1: get_metrics — p95 מ־80ms ל־620ms. הבעיה אמיתית, התחילה לפני ~30 דק׳.

Step 2: deployment 3.8.1 לפני 32 דק׳. יש Correlation — אבל Correlation הוא לא הוכחה.

Step 3: logs עם database connection timeout. יש Evidence נוסף.

עכשיו Re-planning: Inspect DB timeout frequency, compare before/after release, connection pool, previous incidents, estimate confidence.

מה היה קורה ב-Workflow קבוע? הוא היה יכול להריץ את כל השלבים גם אם כבר יש תשובה.

Agent יכול לעצור מוקדם — או להעמיק במקום הנכון.

זה הערך של Adaptation.

[עצירה]

---

## ‏21 — הדגמה — Plan then Execute

[סטודנטים · 21]

[הדגמה]

![CI console](assets/screens/ci-console.png)

![Demo: Plan then Execute](assets/02/demo-plan-execute.png)

בהקלטה: הציגו את הקונסול כ־Observation, ואז את רצף ה־re-plan.

מטרה לדוגמה: "מצא את הסיבה הסבירה לבעיית CI / API."

שימו לב לסיפור: תוכנית ראשונית → מידע חדש → re-plan → תשובה עם ראיה.

אפשר להראות Pseudocode ברמת רעיון:

```python
goal = user_request
while not done:
    decision = llm(goal=goal, state=state, tools=available_tools)
    result = execute(decision)
    state = update(state, result)
    done = check_stop(state)
```

מה חסר ב־loop הזה ב־Production? Policy, budgets, idempotency, tracing — נגיע לזה מיד.

[עצירה]

---

# ‏חלק יא׳ — Evidence, Policy ו-State

## ‏22 — Evidence, Hypothesis, Confidence

[סטודנטים · 22]

Agent לא אמור להתאהב בהשערה הראשונה.

Deployment התחיל + Latency עלה — קל להגיד "ה-Deploy אשם".

אולי זו רק התאמה בזמנים. אולי הבעיה ב־Database.

Hypothesis Loop:

Hypothesis → Evidence → Supports? → Increase confidence / Change hypothesis.

Confidence לא חייב להיות מספר מדויק — Low / Medium / High מספיק.

או רשימת Evidence + משפט סיכום עם רמת ביטחון.

[עצירה]

---

## ‏23 — Local מול Global Re-plan

[סטודנטים · 23]

לא בכל פעולה עושים Re-plan — אחרת המערכת יקרה מאוד.

Re-plan כש: התגלתה עובדה חדשה, Tool נכשל, התוכנית לא רלוונטית, נמצאה דרך טובה יותר, Branch חדש, risk threshold.

Local: Current step failed → Choose alternative.

Global: Major new evidence → Discard plan → Generate new plan.

[שאלה]

מתי כדאי לתכנן הכול מראש, ומתי עדיף Re-planning?

[עצירה]

---

## ‏24 — Constraints ו-Policy Gate

[סטודנטים · 24]

![Policy Gate](assets/02/07-policy-gate.png)

![Approval dialog](assets/screens/approval-dialog.png)

מטרה בלי Constraints לא מספיקה.

"Deploy the application" בלי: Allowed environments, hours, approvals, Rollback policy, Change window, Security.

Constraint Layer / Policy Gate עומדת בין Plan לבין Execution.

Approval באמצע תהליך: Plan → Inspect → Prepare action → Risk → Human approval → Execute.

ה-Agent לא חייב להתחיל מהתחלה אחרי האישור — הוא ממשיך מהמקום שבו עצר. לכן State חשוב.

[עצירה]

---

## ‏25 — Execution State

[סטודנטים · 25]

![Execution State](assets/02/08-execution-state.png)

המערכת צריכה לדעת: מה בוצע, מה הצליח, מה נכשל, מה עכשיו, מה מחכה, מה דילגנו.

דוגמת State:

```json
{
  "goal": "Investigate API latency",
  "current_step": "check_logs",
  "completed_steps": ["get_metrics", "get_deployments"],
  "failed_steps": [],
  "findings": [
    "latency increased 32 minutes ago",
    "deployment 3.8.1 happened 35 minutes ago"
  ]
}
```

בלי State קשה לעשות Retry, Resume, Human approval, Re-planning, Debugging, Multi-step execution.

בהמשך הקורס נעמיק ב-Memory — היום מספיק להבין ש-State הוא בסיס לביצוע רציף.

[עצירה]

---

## ‏26 — Idempotency, Timeouts, Cost

[סטודנטים · 26]

Idempotency: Agent ביצע create_ticket(), התשובה אבדה — אם מריצים שוב עלולים לקבל שני Tickets.

לכן: create_ticket(idempotency_key="abc123").

Timeouts בשלוש שכבות: Tool timeout, Agent timeout, Overall task timeout.

Cost-aware planning: 5 Tool Calls פשוטים מול 20 קריאות + מודל גדול — שניהם אולי מגיעים לתשובה, אבל המחיר שונה.

מאזנים Quality / Cost / Time.

וגם Context עולה כסף: לא לשלוח 200,000 שורות לוג למודל — Filter → Relevant subset → LLM.

Tool טוב מקבל פרמטרים ממוקדים (service, time range, level, pattern).

[עצירה]

הערה קצרה: Prompt ארוך עם "תעשה 1 ואז 2 ואז 3" הוא לא Planning אמיתי — זה יכול להיות Workflow קשיח בתחפושת.

Planning במערכת Agentic כולל אפשרות שהמערכת תחליט על הדרך לפי מטרה ומצב, בתוך מגבלות.

---

# ‏חלק יב׳ — Anti-patterns, תרגילים וסיכום

## ‏27 — Anti-Patterns

[סטודנטים · 27]

חמישה מלכודות שכדאי לנקוב בשמות:

1. לתכנן 40 צעדים כשאפשר 5.  
2. להניח ש-Tool success = Goal success.  
3. בלי Max iterations.  
4. בלי HITL על פעולות מסוכנות.  
5. Prompt ארוך במקום State + Plan אמיתיים.

[עצירה]

אם אתם רואים אחד מאלה בסקירה ארכיטקטונית — עצרו ותקנו לפני שמדברים על "איזה מודל יותר חכם".

---

## ‏28 — תרגיל 1 — תכננו Agent ל-CI

[סטודנטים · 28]

[תרגיל · 20–25 דק׳]

הקריאו את ההנחיה מהמסך.

מטרה: מצא למה Job ב-CI נכשל.

Tools על המסך. אפשר להשאיר את צילום הקונסול מההדגמה ברקע.

מה להגיש: חצי עמוד, אפשר בזוגות.

בזמן העבודה אפשר לעבור בין תלמידים / לערוך B-ROLL של הקונסול.

אחרי הזמן: אספו 2–3 תשובות קצרות לדיון — במיוחד סעיף 3 (כישלון get_console_log) וסעיף 4 (Stop / Escalation).

[עצירה]

---

## ‏29 — תרגיל 2 — תרחיש עם Re-plan

[סטודנטים · 29]

[תרגיל · 15–20 דק׳]

הקריאו את התרחיש: הנחה ראשונית על Runner, Observation חדש על dependency חסר.

בקשו Plan מקורי, Local re-plan, מתי Global, ו-Stop condition.

בדיון: הדגישו ש-Local הוא ברירת מחדל זולה, ו-Global כשהמסגרת של החקירה השתנתה.

[עצירה]

---

## ‏30 — תרגיל 3 — Checklist ל-Production

[סטודנטים · 30]

[תרגיל · 10–15 דק׳]

בקשו לסמן ✓/✗ על הרשימה עבור Agent אמיתי מהעבודה או מהתרגילים הקודמים.

אחרי הזמן: שאלו איזה פריט חסר הכי הרבה אצל אנשים — בדרך כלל Iteration budget או HITL או Trace.

[עצירה]

---

## ‏31 — Design Review מהיר

[סטודנטים · 31]

[שאלה / דיון · 5–8 דק׳]

> תכננתם Incident Agent. איזו החלטה תשאירו ל-LLM, ואיזו תקבעו בקוד דטרמיניסטי — ולמה?

כוונו את הדיון לדוגמאות: בחירת כיוון חקירה למודל; Restart / Deploy / Delete — Policy בקוד + HITL.

אפשר להישען על נספח ז׳ אם רוצים להעמיק אחרי ההקלטה.

[עצירה]

---

## ‏32 — סיכום

[סטודנטים · 32]

מה צריך לזכור:

Planning הוא Hypothesis, לא תסריט קשיח.

Closed loop + Validation + Stop conditions.

Tool success ≠ Goal success.

State, Policy ו-Budget הם חלק מהארכיטקטורה — לא "תוספות אחר כך".

המשפט המרכזי:

> Planning = לבחור את הצעד הבא הטוב ביותר תחת מגבלות, ואז ללמוד מהתוצאה.

זה ההבדל בין Agent שמריץ Script לבין Agent שמנהל תהליך.

[עצירה]

---

## ‏33 — הכנה למפגש 3

[סטודנטים · 33]

במפגש הבא: **Tool Use ו-Function Calling**.

שם ה-Agent מפסיק רק לחשוב על פעולות — והמערכת מאפשרת לו לבצע אותן בפועל.

הכנה: הביאו 3 Tools מהעבודה — קלט, פלט, האם מסוכן / דורש HITL.

[מצלמה: סגירה חמה.]

תודה — נתראה במפגש 3.

---

# ‏נספח א׳ — דיאגרמות וקבצים

קבצים תחת `assets/02/`:

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

חידוש: `python3 scripts/gen_diagrams.py`

---

# ‏נספח ב׳ — משפטי מעבר להקלטה

1. "עכשיו כשהבנו מה זה Planning, בואו נראה למה תכנון מראש לא תמיד מספיק."
2. "וזה בדיוק המקום שבו נכנסת הלולאה."
3. "עכשיו נעבור מהתכנון עצמו אל הביצוע."
4. "ופה יש הבדל קטן אבל חשוב בין פעולה שהצליחה לבין משימה שהצליחה."
5. "עד עכשיו דיברנו על Agent שמתקדם. עכשיו בואו נדבר על Agent שנתקע."
6. "וכש-Agent נתקע, אנחנו לא רוצים רק Retry. אנחנו רוצים להבין למה הוא נכשל."
7. "עכשיו נוסיף מגבלות. כי Agent חכם בלי גבולות יכול להיות מערכת בעייתית מאוד."
8. "עכשיו ניקח את כל הרעיונות האלה ונחבר אותם לדוגמה אחת."

---

# ‏נספח ג׳ — שאלות לקהל (מאגר)

1. מתי הייתם מעדיפים Workflow קבוע על Agent?
2. מתי כדאי לתכנן הכול מראש?
3. מתי עדיף Re-planning?
4. האם Tool שקיבל HTTP 200 בהכרח הצליח?
5. למה צריך Max Iterations?
6. מה ההבדל בין Tool Failure לבין Task Failure?
7. איזה דברים עדיף להשאיר בקוד ולא למסור להחלטת LLM?

---

# ‏נספח ד׳ — מילון מונחים

**Planning** — יצירת דרך אפשרית ממטרה לתוצאה.  
**Task Decomposition** — פירוק משימה גדולה לתת־משימות.  
**Execution** — ביצוע מול Tools ומערכות.  
**Re-planning** — שינוי תוכנית בעקבות מידע חדש או כשל.  
**ReAct** — Reason → Act → Observe.  
**Plan-and-Execute** — הפרדה בין יצירת תוכנית לביצוע.  
**Validation** — בדיקה שהתוצאה תקינה ורלוונטית.  
**Stop Condition** — מתי המשימה הסתיימה / נכשלה / נעצרת.  
**Iteration Limit** — מגבלה על מחזורי Agent.  
**Idempotency** — חזרה על בקשה בלי תוצאה כפולה בלתי רצויה.  
**Constraint / Policy** — גבולות וכללי מותר/אסור.  
**Execution State** — מצב המשימה בזמן ריצה.  
**Parallel Execution** — הרצת פעולות בלתי תלויות במקביל.

---

# ‏נספח ה׳ — Design Review מורחב (אופציונלי)

תרחיש: Agent מקבל "מצא את הסיבה לבעיה ב-Production ותקן אותה."

Tools: read_logs, get_metrics, restart_service, scale_service, deploy_version, delete_resource.

שאלו: מה אוטומטי? מה באישור? אילו Tools מסוכנים? מה דטרמיניסטי? Stop Condition? מניעת לולאה אינסופית? איך יודעים מה Agent עשה (Trace)?

</div>
