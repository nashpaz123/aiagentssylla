<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 2 — מצגת סטודנטים
## ‏Agent Architecture: Planning ו-Execution

> מצגת להצגה בהקלטה · מספור **סטודנטים בלבד** (1…N).  
> מרצה: `[סטודנטים · N]` באותו מספר וכותרת.  
> **משך משוער:** ~2.5–3 שעות **הקלטה** (הוראה + Lab חי + הדגמות פתרון).  
> אין זמן עבודה לסטודנטים חיים — תרגילים = הדגמת מרצה בקול.  
> חזרה קצרה על מפגש 1 (Goal/Decide/Act/Observe, Spectrum, HITL בסיסי) — בלי פירוט מחדש.

---

# ‏חלק א׳ — פתיחה

## ‏1 — כותרת

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="360" />
</p>

**Agent Architecture**  
Planning ו-Execution

![Goal → Plan → Actions](assets/02/01-goal-plan-actions.png)

---

## ‏2 — מה היום (+ חזרה קצרה על מפגש 1)

| נבנה היום | מפגש 1 (בקצרה) |
|---|---|
| Planning / Decomposition | מהו Agent מול Chat |
| Open/Closed · ReAct · Plan-and-Execute | Spectrum L0–L6 |
| Validation · Failure · Budget · State | HITL ברמת מבוא |
| Lab חי: Claude Code + AWS (read-only) | |

---

## ‏3 — שאלת המפגש + תוצרים

> מטרה גדולה → איך בוחרים צעד ראשון, ומתי משנים תוכנית?

בסוף המפגש תדעו:
1. לפרק מטרה ל-Hypothesis Plan  
2. להבדיל Tool / Step / Goal success  
3. לתכנן Failure + Stop + Budget  
4. להריץ לולאה חיה ולזהות Re-plan  

---

# ‏חלק ב׳ — Planning לעומק

## ‏4 — Planning = גשר

**הגדרה:** Planning — דרך אפשרית ממטרה לתוצאה (השערה, לא חוזה).

```text
GOAL → PLAN → ACTIONS → RESULT
```

דוגמה אנושית (קצר):
מטרה: *״חופשה ברומא באוקטובר עד ₪6,000.״*  
תוכנית: תאריכים → טיסות → מלון → אטרקציות → Buffer לביטולים.

---

## ‏5 — משימה פשוטה מול מורכבת

| פשוטה | מורכבת |
|---|---|
| Ping לשרת | חקירת אי־יציבות מאז Release |
| כמעט בלי Planning | סדרת החלטות + Evidence |

תרחישי עבודה:
1. *״העתק קובץ A→B״* — Workflow  
2. *״למה הלקוח כועס על חיוב?״* — Agent  
3. *״Deploy ל־prod אחרי בדיקות״* — היברידי (Plan + Policy)

---

## ‏6 — תוכנית = Hypothesis + רמות פירוט

```text
1. Get logs
2. Check metrics
3. Check deployments
4. Analyze
```

או כוונה מופשטת: `Investigate recent instability` + החלטות מקומיות.

רמות: **Full plan מראש** · **Skeleton** · **Step-wise (ReAct)**.

---

## ‏7 — סוגי טעויות Planning

| סוג | דוגמה |
|---|---|
| Missing step | Deploy בלי Security Scan |
| Wrong order | Rollback לפני אבחון |
| Wrong assumption | ״תמיד Runner אשם״ |
| Overplanning | 40 צעדים למשימה של 5 |
| Underplanning | ״תתקן את הפרוד״ כצעד אחד |

---

# ‏חלק ג׳ — Task Decomposition

## ‏8 — Task Decomposition

![Task Decomposition](assets/02/02-task-decomposition.png)

**הגדרה:** פירוק לתת־משימות שניתן לבצע, לבדוק ולהיכשל בהן בבירור.

כלל: יחידת משמעות — לא מספר יפה של שורות.

---

## ‏9 — Decomposition בדוגמת Latency

מטרה: *״מצא למה latency עלה.״*

```text
1. Check when latency increased
2. Compare with deployments
3. Check CPU / Memory
4. Check database latency
5. Inspect application logs
6. Correlate findings
7. Identify most likely cause
```

Hypothesis ראשונית — לא חוזה.

---

## ‏10 — דוגמה מפורטת: Decomposition לחיסכון בענן

מטרה: *״הורד את חשבון הענן החודשי ב־20% בלי לפגוע ב־SLA.״*

פירוק שמדגימים בקול:
```text
1. Baseline: עלות 30 יום לפי שירות
2. מצא Top-5 עלויות
3. בדוק idle / over-provision (non-prod קודם)
4. הצע rightsizing עם הערכת חיסכון
5. בדוק השפעה על latency/error budget
6. Policy: אין שינוי prod בלי אישור
7. דוח: חיסכון צפוי + סיכונים + צעדי HITL
```

תלויות: 1→2→3; 4 תלוי ב־3; 5 לפני כל שינוי; 6 חוסם ביצוע אוטומטי.

---

# ‏חלק ד׳ — Open / Closed Loop

## ‏11 — Open Loop מול Closed Loop

![Open vs Closed Loop](assets/02/03-open-vs-closed-loop.png)

| Open | Closed |
|---|---|
| Plan → ביצוע ליניארי | Plan → Execute → Observe → Re-plan? |
| תהליכים יציבים | עולם עם הפתעות |

**לזכור:** Workflow קבוע עדיף כשאין אי־ודאות וכל הצעדים ידועים מראש.

---

## ‏12 — אותה מטרה בשתי גישות

מטרה: *״בדוק למה Checkout נכשל ל־3% מהמשתמשים.״*

**Open:** רשימה קבועה Metrics→Logs→DB→CDN→Report (גם אם כבר מצאתם אחרי Logs).  
**Closed:** Metrics → Observation → מקצרים ל־Payments API → Evidence → Stop מוקדם.

הערך: Adaptation חוסך זמן וכסף — אם יש Stop + Budget.

---

# ‏חלק ה׳ — ReAct

## ‏13 — ReAct

![ReAct](assets/02/04-react.png)

**הגדרה:** Reason → Act → Observe → חזרה.

יתרון: גמישות. חיסרון: יקר / thrashing בלי תקציב.

---

## ‏14 — ReAct בדוגמה (API 500)

```text
Reason: need logs
Act:    get_logs
Observe: DB timeout
Reason: check pool
Act:    get_db_pool_metrics
Observe: pool 95% full
Reason: enough evidence? → report or dig deeper
```

---

## ‏15 — כש-ReAct מתפזר

סימנים:
- אותם Tools שוב ושוב  
- Confidence לא עולה  
- Tokens עולים בלי Evidence חדש  

טיפול: Iteration budget · Tool allow-list · ״אין Evidence חדש ×2 → Stop/Escalate״.

---

# ‏חלק ו׳ — Plan-and-Execute

## ‏16 — Plan-and-Execute

![Plan-and-Execute](assets/02/05-plan-and-execute.png)

**הגדרה:** Planner בונה תוכנית · Executor מבצע · Re-plan לפי משוב.

```text
1. Inspect deployment
2. Inspect logs
3. Compare release
4. Recommend rollback
```

יתרון: Review / HITL לפני ביצוע מסוכן.

---

## ‏17 — אותו Incident: ReAct מול Plan-and-Execute

| | ReAct | Plan-and-Execute |
|---|---|---|
| צעד ראשון | לפי Thought | לפי Plan שאושר |
| שינוי כיוון | כל Observation | Re-plan מפורש |
| מתאים ל | חקירה פתוחה | סיכון + צורך בביקורת |
| סיכון | מתפזר | נצמד לתוכנית שגויה |

---

## ‏18 — מתי Planner נפרד?

| בלי הפרדה | עם Planner נפרד |
|---|---|
| משימות קצרות | תוכנית ארוכה לבדיקה |
| עלות נמוכה | Policy / Approval אחרי Plan |
| פחות State | Production עם סיכון |

---

# ‏חלק ז׳ — Execution ו-Validation

## ‏19 — שלושה סוגי הצלחה

![Three kinds of success](assets/02/10-three-success.png)

**הגדרה:** Execution / Validation.

1. Tool success · 2. Step success · 3. Goal success  

‏Tool success ≠ Goal success.

**לזכור:** Tool fail = הכלי נכשל · Task fail = המשימה לא הושגה (גם אם הכלי החזיר 200).

---

## ‏20 — Validation — כמה פנים

```text
search_tickets() → 200 OK → { "tickets": [] }
```

| מקרה | משמעות |
|---|---|
| 200 + [] | ״לא מצאתי״ — מידע! |
| 200 + schema שבור | Step fail |
| 200 + נתונים לא רלוונטיים | Semantic fail |
| Timeout | Tool fail → typed retry |

---

# ‏חלק ח׳ — Failure וגבולות

## ‏21 — Failure Handling

![Failure Handling](assets/02/06-failure-handling.png)

Timeout · Auth · Bad params · Empty · Rate limit · Unexpected · Model mistake

טיפול: typed retry · כלי חלופי · Local/Global re-plan · Escalation

---

## ‏22 — מטריצת Retry + Backoff

```text
Timeout           → Retry + backoff
Rate limit        → Wait + Retry
Invalid parameter → Fix args + Retry once
Permission denied → Stop / Escalate
Dangerous op      → HITL
Empty useful data → Re-plan (not blind retry)
```

```text
Backoff: 1s → 2s → 4s → 8s (עם תקרה)
```

---

## ‏23 — Budget, Stop, Success Criteria

**הגדרה:** Iteration Limit · Stop Condition.

דוגמה למשימת דוח:
- Success: קובץ + 4 סעיפים + נתונים נבדקו  
- Fail: אין גישה למקור > 2 ניסיונות  
- Stop: 12 tool calls / 5 דק׳ / Confidence גבוהה מספיק  

**לזכור:** בלי תקרה Agent יכול לשרוף Tokens/כסף/זמן בלי סוף.

---

# ‏חלק ט׳ — מבנה והחלטות

## ‏24 — Dependencies ו-Branches

**הגדרה:** Parallel Execution.

- מקבילי כשאין תלות · זהירות מ-rate limits  
- Branches: `severity==high` → HITL (עדיף בקוד)

---

## ‏25 — קוד דטרמיניסטי מול LLM

| בקוד | במודל |
|---|---|
| Policy, timeouts, retries טכניים | בחירת כיוון, השערות, סיכום |
| Allow-list של Tools | ניסוח / סיווג |

```python
if severity == "critical":
    require_human_approval()
```

---

## ‏26 — דוגמאות החלטה: קוד או מודל?

1. האם Restart מותר בלי אישור בלילה? → **קוד/Policy**  
2. איזה שירות לבדוק קודם לפי תסמינים? → **מודל**  
3. האם JSON תקין? → **קוד**  
4. האם הממצאים מספיקים להמלצת Rollback? → **מודל + כללי Confidence**

---

# ‏חלק י׳ — Incident, Demo, Lab חי

## ‏27 — Incident Agent (מלא)

![Incident Agent](assets/02/09-incident-agent.png)

מטרה: latency גבוה ב-API · סיבה סבירה · המלצה.  
Tools קריאה בלבד: metrics · logs · deployments · incidents

זרימה: Confirm → Correlate deploy → Logs → Re-plan לפי Evidence

![Metrics](assets/screens/metrics-dashboard.png)

![Kubernetes](assets/screens/k8s-pods-logs.png)

---

## ‏28 — צעדים + Re-plan בדוגמה

```text
get_metrics     → p95 80ms→620ms (מאושר)
get_deployments → 3.8.1 לפני 32 דק׳ (correlation ≠ proof)
get_logs        → DB timeout
REPLAN          → pool metrics + before/after + prior incidents
```

Workflow קבוע היה ממשיך גם אחרי שיש תשובה. Agent יכול Stop מוקדם.

---

## ‏29 — הדגמה CI + Pseudocode

![CI console](assets/screens/ci-console.png)

![Demo plan execute](assets/02/demo-plan-execute.png)

```python
goal = user_request
while not done:
    decision = llm(goal=goal, state=state, tools=available_tools)
    result = execute(decision)
    state = update(state, result)
    done = check_stop(state)
```

---

## ‏30 — Lab חי: מטרה ומגבלות

**מחוץ למצגת / לצד המצגת:** Claude Code + AWS.

מטרה: לאשר גישה ל-AWS ולדגום אם יש מדדי EC2 CPU (read-only).

מגבלות בהקלטה:
- אזור אחד · בלי Create/Update/Delete  
- `MAX_ITERATIONS = 5`  
- תקציב: סנטים  

קוד: `labs/02-aws-agent-loop/`

---

## ‏31 — Lab חי: מה נריץ

```bash
cd labs/02-aws-agent-loop
export AWS_PROFILE=nashpazformatan
export AWS_REGION=eu-north-1
python3 agent_loop.py
```

שימו לב בלייב:
1. Initial plan  
2. Observation מ-STS / CloudWatch  
3. Local re-plan אם 0 נקודות מדד  
4. Stop + findings  

אופציונלי: לשנות Plan ב-Claude Code ולהריץ שוב.

---

## ‏32 — Lab חי: Debrief

מה ראינו?
- Plan ≠ חוזה  
- Observation ריק עדיין Evidence  
- Re-plan מקומי זול מ-Global  
- Stop condition עצר לפני לולאה מיותרת  

**לזכור אחרי Lab:** allow-list של Tools · max iterations · אין write בלי HITL.

---

# ‏חלק יא׳ — Evidence, Policy, State

## ‏33 — Evidence, Hypothesis, Confidence

```text
Hypothesis → Evidence → Supports? → ↑confidence / החלף Hypothesis
```

Correlation ≠ Proof. Low / Medium / High.

---

## ‏34 — Wrong Assumption (Release)

Agent מניח: `Build → Test → Deploy`  
ארגון דורש: Scan → Approvals → Staging → Prod Approval.

בלי Constraints התוכנית ״עובדת״ במעבדה ונכשלת בפרוד.

---

## ‏35 — Local מול Global Re-plan

**הגדרה:** Re-planning.

| Local | Global |
|---|---|
| צעד נכשל → חלופה | זורקים מסגרת חקירה |
| זול | יקר |

**לזכור:** Local כשנשברת רק פעולה; Global כשנשברת מסגרת החקירה.

---

## ‏36 — Constraints ו-Policy Gate

![Policy Gate](assets/02/07-policy-gate.png)

![Approval dialog](assets/screens/approval-dialog.png)

**הגדרה:** Constraint / Policy.

זמן · עלות · הרשאות · ״אין נגיעה בפרוד בלי אישור״

---

## ‏37 — Execution State

![Execution State](assets/02/08-execution-state.png)

**הגדרה:** Execution State.

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

---

## ‏38 — Idempotency, Timeouts, Cost

**הגדרה:** Idempotency.

- `idempotency_key` ליצירות  
- Timeouts: Tool / Agent / Task  
- Quality ↔ Cost ↔ Time · סננו Context ל-LLM  

---

# ‏חלק יב׳ — Anti-patterns ותרגילים

## ‏39 — Anti-Patterns

1. 40 צעדים במקום 5  
2. Tool success = Goal success  
3. בלי Max iterations  
4. בלי HITL על מסוכן  
5. Prompt ארוך במקום State+Plan  
6. ReAct בלי Evidence gate (חדש)

---

## ‏40 — הדגמה 1 — תכנון Agent ל-CI (בעיה)

מטרה: *״מצא למה Job ב-CI נכשל.״*

Tools: `get_job_status` · `get_console_log` · `get_recent_changes` · `get_runner_info` · `search_previous_failures`

שאלות שנענה עליהן בהדגמה:
1. מה חייבים לדעת קודם?  
2. חובה כל ה-Tools?  
3. אם `get_console_log` נכשל — מה עכשיו?  
4. Stop מול Escalation  

---

## ‏41 — הדגמה 1 — פתרון מלא בקול

1. **קודם:** job id · זמן כשל · branch/commit · הודעת כשל קצרה מהסטטוס  
2. **לא חובה כל הכלים** — מתחילים ב-`get_job_status` ואז `get_console_log`  
3. **Log נכשל:** `get_recent_changes` · `search_previous_failures` · אם אין נתונים → Escalate  
4. **Stop:** Evidence ממוקד + המלצה אחת · **Escalate:** אין גישה ללוג/שינויים אחרי 2 ניסיונות  

Plan לדוגמה: status → log → (אם ImportError) recent_changes → confirm dependency → report.

---

## ‏42 — הדגמה 2 — Re-plan מלא

הנחה ראשונית: Runner אשם.  
Observation: Runner תקין · חסר dependency ב-`requirements.txt`.

- **Plan מקורי:** runner_info → console → conclude runner  
- **Local re-plan:** אחרי runner תקין → חפש בלוג `ModuleNotFound` / השווה requirements ל-lock  
- **Global:** רק אם מתברר שזה בכלל job אחר / pipeline אחר  
- **Stop:** נמצא החבילה החסרה + שורת לוגו התומכת · המלצה: להוסיף ל-requirements ולהריץ מחדש  

---

## ‏43 — הדגמה 3 — Checklist על Agent לדוגמה

עבור CI Agent מההדגמה — סטטוס לדוגמה:

- [x] Goal+Success · [x] Budget · [x] Failure typed  
- [x] Policy read-only · [x] HITL על re-run job  
- [x] State · [ ] Trace מלא (חסר — נוסיף במפגש Observability)  
- [x] Timeouts · [x] Cost limit על tool calls  

---

## ‏44 — הדגמה 4 — Design Review מלא

תרחיש: *״מצא סיבה ב-Production ותקן.״*  
Tools: `read_logs` · `get_metrics` · `restart_service` · `scale_service` · `deploy_version` · `delete_resource`

תשובות שנקריא:
1. **אוטומטי:** logs + metrics בלבד  
2. **HITL:** restart / scale / deploy  
3. **אסור או תמיד HITL+שני מאשרים:** delete_resource  
4. **דטרמיניסטי בקוד:** allow-list · severity→HITL · max iterations  
5. **Stop:** סיבה סבירה + Confidence בינוני+ בלי תיקון, או אחרי תיקון מאושר + בדיקת מדד  
6. **אנטי-לולאה:** budget · אין retry עיוור על permission denied  
7. **Trace:** כל Tool call + החלטה + אישור אדם בלוג מובנה  

---

## ‏45 — סיכום

- Planning = Hypothesis + מגבלות  
- Closed loop + Validation + Budget/Stop  
- Tool ≠ Goal success  
- State · Policy · Idempotency שייכים לארכיטקטורה  
- Lab: ראינו Re-plan על Observation אמיתי/ריק  
- מפגש 3: **Tool Use ו-Function Calling**

---

## ‏46 — הכנה למפגש 3

- 3 Tools מהעבודה: קלט · פלט · מסוכן?/HITL  
- בונוס: סמנו איזה מהם Idempotent

</div>
