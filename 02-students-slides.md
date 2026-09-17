<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 2 — מצגת סטודנטים
## ‏Agent Architecture: Planning ו-Execution

> מצגת קצרה להצגה בהקלטה.  
> המספור כאן הוא **של מצגת הסטודנטים בלבד** (1…N).  
> בקובץ המרצה מופיע הסימון `[סטודנטים · N]` ליד הקטע שמתאים למספר הזה.  
> **משך משוער:** ~2.5–3 שעות (כולל תרגילים והדגמות).

---

# ‏חלק א׳ — פתיחה וחיבור למפגש הקודם

## ‏1 — כותרת

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="360" />
</p>

**Agent Architecture**  
Planning ו-Execution

![Goal → Plan → Actions](assets/02/01-goal-plan-actions.png)

---

## ‏2 — איפה עצרנו?

- ‏Goal · Decide · Act · Observe
- Workflow מול Agent · Spectrum · Tools + Guardrails
- היום: איך הופכים מטרה לתוכנית — ואיך מבצעים עם בקרה

---

## ‏3 — השאלה של היום

> אם אני נותן ל-Agent מטרה גדולה — איך הוא יודע מה לעשות קודם?

תשובה קצרה: **Planning**  
אבל: כמה לתכנן? מתי לתכנן מחדש? מה קורה כשהתוכנית נשברת?

---

# ‏חלק ב׳ — מה זה Planning?

## ‏4 — Planning = גשר

```text
GOAL → PLAN → ACTIONS → RESULT
```

- מטרה ≠ תוכנית
- ״תארגן חופשה״ = מטרה · רשימת בדיקות = תוכנית

---

## ‏5 — משימה פשוטה מול מורכבת

| פשוטה | מורכבת |
|---|---|
| ״בדוק אם השרת זמין״ | ״חקור למה השירות לא יציב מאז הגרסה״ |
| כמעט בלי Planning | סדרת החלטות + Hypothesis |

Planning שימושי כשיש **אי־ודאות** וצריך לבחור מסלול.

---

## ‏6 — תוכנית = Hypothesis

- תוכנית היא השערת עבודה — לא אמת מוחלטת
- אפשר רשימה מפורטת **או** כוונה מופשטת ואז החלטות מקומיות
- אחרי Observation ראשון — התוכנית יכולה להשתנות

---

# ‏חלק ג׳ — Task Decomposition

## ‏7 — Task Decomposition

![Task Decomposition](assets/02/02-task-decomposition.png)

- מפרקים כדי להתקדם, לא כדי להרשים
- פירוק דק מדי = רעש · גס מדי = חוסר שליטה
- כל Step צריך להיות: מובן · ניתן לביצוע · ניתן לבדיקה · כישלון ברור

---

## ‏8 — Decomposition בדוגמה

מטרה: *״מצא למה latency עלה.״*

```text
1. מתי עלה?  2. Deployments  3. CPU/Mem
4. DB latency  5. Logs  6. Correlate  7. סיבה סבירה
```

זו Hypothesis ראשונית — לא חוזה.

---

# ‏חלק ד׳ — Open Loop מול Closed Loop

## ‏9 — Open Loop מול Closed Loop

![Open vs Closed Loop](assets/02/03-open-vs-closed-loop.png)

| Open Loop | Closed Loop |
|---|---|
| מתכננים הכול מראש ומבצעים | מתכננים + מתבוננים + מתקנים |
| טוב לתהליכים יציבים | טוב ל-Agents בעולם אמיתי |

> Plan טוב יודע להשתנות כשצריך.

---

# ‏חלק ה׳ — ReAct

## ‏10 — ReAct

![ReAct](assets/02/04-react.png)

- ‏**Thought → Action → Observation** (חוזר)
- יתרון: גמישות כשהבעיה לא ידועה מראש
- חיסרון: יקר / מתפזר בלי תקציב איטרציות

---

## ‏11 — ReAct בדוגמה

משימה: *״מצא למה ה-API מחזיר 500.״*

1. Reason → צריך Logs  
2. Act → `get_logs`  
3. Observe → Database timeout  
4. Reason → בדיקת connectivity / pool  
5. Act → Tool נוסף · Observe → pool כמעט מלא  

עצירה עם Evidence — או המשך איסוף.

---

# ‏חלק ו׳ — Plan-and-Execute

## ‏12 — Plan-and-Execute

![Plan-and-Execute](assets/02/05-plan-and-execute.png)

- ‏**Planner** בונה תוכנית  
- ‏**Executor** מבצע צעדים  
- משוב → Re-plan כשצריך  

יתרון: בדיקת תוכנית לפני ביצוע · HITL · Debugging קל יותר.

---

## ‏13 — מתי Planner נפרד?

| בלי הפרדה | עם Planner נפרד |
|---|---|
| משימות קצרות / ReAct | תוכנית ארוכה לבדיקה |
| עלות נמוכה | Policy / Approval אחרי Plan |
| פחות State | Production עם סיכון |

לא תמיד חייבים — תלוי במורכבות ובסיכון.

---

# ‏חלק ז׳ — Execution ו-Validation

## ‏14 — שלושה סוגי הצלחה

![Three kinds of success](assets/02/10-three-success.png)

1. ‏**Tool success** — הכלי עבד (HTTP 200…)  
2. ‏**Step success** — קיבלנו מידע שימושי  
3. ‏**Goal success** — המטרה באמת הושגה  

‏Tool success ≠ Goal success.

---

## ‏15 — Validation בדוגמה

```text
search_tickets() → 200 OK → { "tickets": [] }
```

- ‏Transport + Schema תקינים  
- סמנטית: ״לא מצאתי״ — מידע חשוב, לא ״הכל בסדר״  
- צריך **Semantic Validation** בתוך ה-Loop

---

# ‏חלק ח׳ — Failure Handling וגבולות

## ‏16 — Failure Handling

![Failure Handling](assets/02/06-failure-handling.png)

- ‏Retry לפי סוג שגיאה + Backoff  
- כלי חלופי  
- ‏Local / Global re-plan  
- ‏Escalation לאדם  

Timeout ≠ Invalid parameter ≠ Permission denied.

---

## ‏17 — Max Iterations ו-Stop Conditions

- בלי תקרה — לולאות יקרות / אינסופיות
- ‏**Iteration Budget** = כמה סיבובים / Tool calls / Tokens מותרים
- Stop: הצלחה · כישלון · ״לא יודע״ · Timeout · Escalation · Confidence

---

# ‏חלק ט׳ — מבנה תוכנית והחלטות

## ‏18 — Dependencies ו-Branches

- לא הכול חייב להיות סדרתי · Parallelization חוסך זמן ומוסיף מורכבות
- ‏Conditional execution: Agent בוחר ענף לפי Observation
- מדיניות קשיחה (severity → HITL) עדיף בקוד

---

## ‏19 — קוד דטרמיניסטי מול LLM

| בקוד | במודל |
|---|---|
| Validations, retries טכניים, timeouts | בחירת כלי, פירוק, השערות |
| הרשאות / Policy קשיחים | פרשנות, סיכום, סיווג |

> AI **בתוך** מערכת תוכנה — לא במקום קוד.

---

# ‏חלק י׳ — דוגמה והדגמה

## ‏20 — דוגמה מלאה: Incident Agent

![Incident Agent](assets/02/09-incident-agent.png)

מטרה: חקור latency גבוה ב-API · מצא סיבה סבירה · המלצה.

Tools (קריאה בלבד): `get_metrics` · `get_logs` · `get_deployments` · `search_incidents` …

זרימה: Confirm → Correlate deploy → Logs → Re-plan לפי Evidence

![Metrics](assets/screens/metrics-dashboard.png)

![Kubernetes](assets/screens/k8s-pods-logs.png)

---

## ‏21 — הדגמה — Plan then Execute

![CI console](assets/screens/ci-console.png)

![Demo plan execute](assets/02/demo-plan-execute.png)

שימו לב: תוכנית ראשונית → מידע חדש → **re-plan** → תשובה עם ראיה.

---

# ‏חלק יא׳ — Evidence, Policy ו-State

## ‏22 — Evidence, Hypothesis, Confidence

```text
Hypothesis → Evidence → Supports? → ↑confidence / החלף Hypothesis
```

- אל תתאהבו בהשערה הראשונה (Correlation ≠ Proof)
- אספו Evidence · עדכנו Confidence (Low / Medium / High)

---

## ‏23 — Local מול Global Re-plan

| Local | Global |
|---|---|
| צעד נכשל → חלופה | Evidence גדול → זורקים תוכנית |
| זול ומהיר | יקר יותר · חשיבה מחדש |

Re-plan לא בכל צעד — רק כשצריך.

---

## ‏24 — Constraints ו-Policy Gate

![Policy Gate](assets/02/07-policy-gate.png)

![Approval dialog](assets/screens/approval-dialog.png)

מטרה בלי אילוצים לא מספיקה:
זמן · עלות · הרשאות · ״אסור לגעת בפרוד בלי אישור״

---

## ‏25 — Execution State

![Execution State](assets/02/08-execution-state.png)

צריך לזכור: איפה אנחנו · מה ניסינו · מה מצאנו · כמה תקציב נשאר.

בלי State קשה: Retry · Resume · HITL · Debug.

---

## ‏26 — Idempotency, Timeouts, Cost

- פעולות שחוזרות לא צריכות לשבור את העולם (`idempotency_key`)
- Timeouts: Tool · Agent run · משימה שלמה
- Planning **Cost-aware**: איכות / זמן / כסף · Context מסונן ל-LLM

---

# ‏חלק יב׳ — Anti-patterns, תרגילים וסיכום

## ‏27 — Anti-Patterns

1. לתכנן 40 צעדים כשאפשר 5  
2. להניח ש-Tool success = Goal success  
3. בלי Max iterations  
4. בלי HITL על פעולות מסוכנות  
5. ‏Prompt ארוך במקום State + Plan אמיתיים  

---

## ‏28 — תרגיל 1 — תכננו Agent ל-CI

**הנחיה (20–25 דק׳):**

מטרה: *״מצא למה Job ב-CI נכשל.״* · הסתמכו על הקונסול מההדגמה.

Tools: `get_job_status` · `get_console_log` · `get_recent_changes` · `get_runner_info` · `search_previous_failures`

ענו בכתב:
1. מה ה-Agent חייב לדעת **קודם**? (3 פריטים)  
2. האם חייבים לקרוא את כל ה-Tools? למה כן/לא  
3. אם `get_console_log()` נכשל — מה עושים? (2 אפשרויות לפחות)  
4. מתי עוצרים עם תשובה? מתי Escalation?

**הגשה:** חצי עמוד · אפשר בזוגות.

---

## ‏29 — תרגיל 2 — תרחיש עם Re-plan

**הנחיה (15–20 דק׳):**

הנחה ראשונית: *״הבנייה נכשלה בגלל Runner.״*  
Observation: Runner תקין · חסר dependency ב-`requirements.txt`.

כתבו:
- Plan מקורי · Local re-plan · מתי Global? · Stop condition

---

## ‏30 — תרגיל 3 — Checklist ל-Production

**הנחיה (10–15 דק׳):** סמנו ✓/✗ עבור Agent שאתם מכירים / מתכננים:

- [ ] Goal ברור + Success criteria  
- [ ] Iteration budget  
- [ ] Failure handling  
- [ ] Policy / permissions  
- [ ] HITL על פעולות רגישות  
- [ ] State שמור  
- [ ] Trace / logs מובנים  
- [ ] Timeouts  
- [ ] Cost limits  

---

## ‏31 — Design Review מהיר

> תכננתם Incident Agent. איזו החלטה תשאירו ל-LLM, ואיזו תקבעו בקוד דטרמיניסטי — ולמה?

דיון קצר בכיתה / בהקלטה: 5–8 דק׳.

---

## ‏32 — סיכום

- ‏Planning הוא Hypothesis, לא תסריט קשיח  
- ‏Closed loop + Validation + Stop conditions  
- ‏Tool success ≠ Goal success  
- ‏State, Policy ו-Budget הם חלק מהארכיטקטורה  
- במפגש הבא: **Tool Use ו-Function Calling**

---

## ‏33 — הכנה למפגש 3

- הביאו רשימה של 3 Tools שהייתם נותנים ל-Agent בעבודה שלכם  
- לכל Tool: קלט, פלט, האם מסוכן / דורש HITL

</div>
