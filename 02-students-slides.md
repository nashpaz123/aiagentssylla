<div dir="rtl">

# מפגש 2 — מצגת סטודנטים
## Agent Architecture: Planning ו-Execution

> **לסטודנטים** · מצגת קצרה לליווי השיעור  
> **משך מפגש משוער:** ~2.5–3 שעות

---

## 1. כותרת

**Agent Architecture**  
Planning ו-Execution

![Goal → Plan → Actions](assets/02/01-goal-plan-actions.png)

---

## 2. איפה עצרנו?

- Goal · Decide · Act · Observe
- היום: איך הופכים מטרה לתוכנית — ואיך מבצעים אותה עם בקרה

---

## 3. השאלה של היום

> אם אני נותן ל-Agent מטרה גדולה — איך הוא יודע מה לעשות קודם?

תשובה קצרה: **Planning**  
אבל: כמה לתכנן? מתי לתכנן מחדש? מה קורה כשהתוכנית נשברת?

---

## 4. Planning = גשר

```text
GOAL → PLAN → ACTIONS → RESULT
```

- מטרה ≠ תוכנית
- תוכנית היא השערה עבודה (Hypothesis), לא אמת מוחלטת

---

## 5. Task Decomposition

![Task Decomposition](assets/02/02-task-decomposition.png)

- מפרקים כדי להתקדם, לא כדי להרשים
- פירוק דק מדי = רעש; גס מדי = חוסר שליטה

---

## 6. Open Loop מול Closed Loop

![Open vs Closed Loop](assets/02/03-open-vs-closed-loop.png)

| Open Loop | Closed Loop |
|---|---|
| מתכננים הכול מראש | מתכננים + מתבוננים + מתקנים |
| טוב לתהליכים יציבים | טוב ל-Agents בעולם אמיתי |

---

## 7. ReAct

![ReAct](assets/02/04-react.png)

- **Thought → Action → Observation** (חוזר)
- יתרון: גמישות
- חיסרון: יכול להיות יקר / מתפזר בלי תקציב איטרציות

---

## 8. Plan-and-Execute

![Plan-and-Execute](assets/02/05-plan-and-execute.png)

- **Planner** בונה תוכנית
- **Executor** מבצע צעדים
- משוב → Re-plan כשצריך

לא תמיד חייבים Planner נפרד — תלוי במורכבות.

---

## 9. Execution: הצלחה אינה דבר אחד

![Three kinds of success](assets/02/10-three-success.png)

1. Tool success — הכלי עבד  
2. Step success — קיבלנו מידע שימושי  
3. Goal success — המטרה באמת הושגה  

---

## 10. Failure Handling

![Failure Handling](assets/02/06-failure-handling.png)

- Retry (לפי סוג שגיאה) + Backoff  
- כלי חלופי  
- Local / Global re-plan  
- Escalation לאדם  

---

## 11. Max Iterations ו-Stop Conditions

- בלי תקרה — לולאות יקרות / אינסופיות
- הגדירו: הצלחה, כישלון, ״לא יודע״, חוסר תקציב

**Iteration Budget** = כמה סיבובים מותרים למשימה.

---

## 12. Dependencies ו-Branches

- לא הכול חייב להיות סדרתי
- Parallelization עוזר — ומוסיף מורכבות
- Conditional execution: Agent בוחר ענף לפי Observation

---

## 13. קוד דטרמיניסטי מול החלטות LLM

| בקוד | במודל |
|---|---|
| Validations, retries טכניים, timeouts | בחירת כלי, פירוק משימה, שיפוט |
| הרשאות קשיחות | ניסוח, סיכום, השערות |

---

## 14. דוגמה מלאה: Incident Agent

![Incident Agent](assets/02/09-incident-agent.png)

זרימה טיפוסית:
1. Status / Symptoms  
2. Metrics / Logs  
3. Deploy history  
4. Hypothesis + Evidence  
5. Re-plan אם ההשערה נשברה  

![Metrics](assets/screens/metrics-dashboard.png)

![Kubernetes](assets/screens/k8s-pods-logs.png)

---

## 15. הדגמה — Plan then Execute

![CI console](assets/screens/ci-console.png)

![Demo plan execute](assets/02/demo-plan-execute.png)

שימו לב: תוכנית ראשונית → מידע חדש → **re-plan** → תשובה עם ראיה.

---

## 16. Evidence, Hypothesis, Confidence

- אל תתאהבו בהשערה הראשונה
- אספו Evidence
- עדכנו Confidence — או החליפו Hypothesis

---

## 17. Constraints ו-Policy Gate

![Policy Gate](assets/02/07-policy-gate.png)

![Approval dialog](assets/screens/approval-dialog.png)

מטרה בלי אילוצים לא מספיקה:
- זמן, עלות, הרשאות, ״אסור לגעת בפרוד בלי אישור״

---

## 18. Execution State

![Execution State](assets/02/08-execution-state.png)

צריך לזכור: איפה אנחנו, מה כבר ניסינו, מה מצאנו, כמה תקציב נשאר.

---

## 19. Idempotency, Timeouts, Cost

- פעולות שחוזרות לא צריכות לשבור את העולם
- Timeouts לכל כלי ולמשימה כולה
- Planning צריך להיות **Cost-aware** (איכות / זמן / כסף)

---

## 20. Anti-Patterns (קצרים)

1. לתכנן 40 צעדים כשאפשר 5  
2. להניח ש-Tool success = Goal success  
3. בלי Max iterations  
4. בלי HITL על פעולות מסוכנות  
5. Prompt ארוך במקום State + Plan אמיתיים  

---

## 21. תרגיל 1 — תכננו Agent ל-CI

**הנחיה (20–25 דק׳):**

מטרה: *״מצא למה Job ב-CI נכשל.״*

הסתמכו על הקונסול מההדגמה בשיעור.

Tools זמינים:
`get_job_status` · `get_console_log` · `get_recent_changes` · `get_runner_info` · `search_previous_failures`

ענו בכתב:

1. מה ה-Agent חייב לדעת **קודם**? (3 פריטים)  
2. האם חייבים לקרוא את כל ה-Tools? למה כן/לא  
3. אם `get_console_log()` נכשל — מה עושים עכשיו? (2 אפשרויות לפחות)  
4. מתי עוצרים עם תשובה? מתי Escalation?

**מה להגיש:** חצי עמוד. אפשר בזוגות.

---

## 22. תרגיל 2 — תרחיש עם Re-plan

**הנחיה (15–20 דק׳):**

הנחה ראשונית של ה-Agent: *״הבנייה נכשלה בגלל Runner.״*  
Observation חדש: Runner תקין, אבל dependency חסר ב-`requirements.txt`.

כתבו:
- מה היה ה-Plan המקורי?
- מה ה-Local re-plan?
- מתי הייתם עושים Global re-plan במקום?
- איזה Stop condition מתאים כאן?

---

## 23. תרגיל 3 (אופציונלי) — Checklist ל-Production

סמנו ✓/✗ עבור Agent שאתם מכירים / מתכננים:

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

## 24. Design Review מהיר

שאלה אחת לסיכום:

> תכננתם Incident Agent. איזו החלטה תשאירו ל-LLM, ואיזו תקבעו בקוד דטרמיניסטי — ולמה?

---

## 25. סיכום

- Planning הוא Hypothesis, לא תסריט קשיח  
- Closed loop + Validation + Stop conditions  
- Tool success ≠ Goal success  
- State, Policy ו-Budget הם חלק מהארכיטקטורה  
- במפגש הבא: **Tool Use ו-Function Calling**

---

## 26. הכנה למפגש 3

- הביאו רשימה של 3 Tools שהייתם נותנים ל-Agent בעבודה שלכם  
- לכל Tool: קלט, פלט, האם מסוכן

</div>
