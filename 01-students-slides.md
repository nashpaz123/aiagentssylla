<div dir="rtl" lang="he">

# ‏מפגש 1 — מצגת סטודנטים
## ‏מבוא לסוכני AI ו-Agentic Workflows

> מצגת קצרה להצגה בהקלטה.  
> מספור השקופיות כאן הוא **של מצגת הסטודנטים בלבד** (1…N).  
> בקובץ המרצה מופיע הסימון `[סטודנטים · N]` ליד הקטע שמתאים לשקופית הזו.

---

## ‏1 — כותרת

**AI Agents ומערכות אוטונומיות**  
מפגש 1: מהו Agent ומה הופך Workflow ל-Agentic

![Human + Agent + Tools](assets/01/01-human-agent-tools.png)

---

## ‏2 — למה Agents?

- ‏ChatGPT עונה לנו.
- ‏Agent **עובד בשבילנו** לקראת מטרה.
- ההבדל: תשובה אחת מול תהליך עם החלטות.

---

## ‏3 — תשובה מול משימה

| מערכת קלאסית | Agent |
|---|---|
| ״ענה לי״ | ״בצע עבורי״ |
| פעולה בודדת | סדרת פעולות |
| קלט → פלט | מטרה → תהליך |
| המשתמש מנהל | המערכת מנהלת חלק |

---

## ‏4 — ארבע מילים לזכור

**Goal → Decide → Act → Observe**

![Agent Loop](assets/01/03-agent-loop.png)

---

## ‏5 — מה LLM לבד עושה?

```text
User → Prompt → LLM → Response
```

- ‏LLM מייצר פלט (טקסט, קוד, JSON…).
- כדי **לפעול בעולם** צריך Tools.

---

## ‏6 — LLM + Tools

![LLM + Tools](assets/01/04-llm-tools.png)

---

## ‏7 — Chat מול Agent

![Chat vs Agent](assets/01/02-chat-vs-agent.png)

---

## ‏8 — Workflow מול Agent

![Workflow vs Agent](assets/01/05-workflow-vs-agent.png)

- **Workflow:** נתיב קבוע מראש.
- **Agent:** בוחר צעדים לפי מה שקורה בדרך.
- אם אפשר לתאר מראש כל צעד — זה לא Agent.

---

## ‏9 — AI Agent Spectrum

![AI Agent Spectrum L0–L6](assets/01/06-agent-spectrum-l0-l6.png)

---

## ‏10 — הרמות בקצרה

| Level | שם | בקצרה |
|---|---|---|
| L0 | Rules Automation | בלי AI |
| L1 | AI-Assisted Tools | אדם נוהג |
| L2 | Custom Assistants | ריאקטיבי |
| L3 | AI Workflows | תסריט + AI |
| L4 | Task Agents | agency מוגבלת |
| L5 | Collaborative Agents | צוות Agents |
| L6 | Autonomous Ecosystems | חזית |

**הקו החשוב:** בין L3 ל־L4.

---

## ‏11 — Agent washing ו־5 מאפיינים

- הרבה מוצרים נקראים Agent בלי יכולת אמיתית.
- השאלה: *איזו רמה התהליך באמת דורש?*

Agent אמיתי צריך את כולם:
1. ‏Goal-orientation  
2. ‏Autonomous planning  
3. ‏Tool use & action  
4. ‏Self-evaluation & adaptation  
5. ‏Meaningful autonomy  

---

## ‏12 — L0 עד L3

- **L0** — if/then, jobs, סקריפטים  
- **L1** — feature בתוך מוצר  
- **L2** — Custom GPT / Gem / Project (יועץ)  
- **L3** — Workflow עם AI בנקודות · כאן רוב ה־washing  

---

## ‏13 — L4 עד L6

- **L3→L4:** מטרה חדשה — נכשל (Workflow) או מתכנן (Agent)?  
- **L4** — Task Agent: מתכנן, כלים, מתקן כיוון, בגבולות  
- **L5** — כמה Agents + Orchestrator  
- **L6** — אקוסיסטם תמיד־פעיל (חזית)  

---

## ‏14 — שאלות + Takeaway

שאלו: מטרה או תסריט? מי קובע צעדים? מה בכישלון? מה לבד מול HITL? מה הכי גרוע שיכול לקרות?

- לא הכול צריך L4+ · הרבה ערך ב־L1–L3  
- ‏L4+ דורש Policy, Trace, Guardrails  

---

## ‏15 — ארבעת המרכיבים

1. **Goal**  
2. **Decision**  
3. **Action**  
4. **Observation**  

---

## ‏16 — Agent Loop

![Agent Loop](assets/01/03-agent-loop.png)

Goal → Decide → Act → Observe → Continue / Stop

---

## ‏17 — Planning

![Task Decomposition](assets/02/02-task-decomposition.png)

- ‏Decomposition  
- תוכנית = Hypothesis  
- ‏Re-planning (Local / Global)  

![Open vs Closed Loop](assets/02/03-open-vs-closed-loop.png)

---

## ‏18 — ReAct

![ReAct](assets/02/04-react.png)

**Reason → Act → Observe** (חוזר)

| ReAct | Plan-and-Execute |
|---|---|
| צעד־צעד גמיש | תוכנית ואז ביצוע |
| עלול להתפזר | עלול להיתקע על תוכנית שגויה |

---

## ‏19 — מתי Agent הוא רעיון גרוע?

- תהליך דטרמיניסטי → Workflow  
- משימה פתוחה + כלים + אי־ודאות → Agent (L4)  
- העדפה: **היברידי**

> אם אפשר לכתוב את כל התהליך בבירור — נסו קודם Workflow.

---

## ‏20 — דוגמה DevOps

מטרה: ״בדוק למה ה־API לא יציב ותן המלצה.״

![Kubernetes](assets/screens/k8s-pods-logs.png)

---

## ‏21 — DevOps · Metrics + Workbench

![Metrics](assets/screens/metrics-dashboard.png)

![Agent Workbench DevOps](assets/screens/agent-workbench-devops.png)

---

## ‏22 — Tool Design

- ‏Tool = שם + תיאור + הרשאות  
- תיאור משפיע על בחירה  
- ‏Tool רחב מדי = סיכון  

![Tool Permissions](assets/01/14-tool-permissions.png)

---

## ‏23 — Human in the Loop

![Human Approval](assets/01/07-human-approval.png)

![Approval dialog](assets/screens/approval-dialog.png)

Auto · Approval · Blocked

---

## ‏24 — Guardrails וכישלונות

![Guardrails](assets/01/08-guardrails.png)

![Failure Loop](assets/01/15-failure-loop.png)

---

## ‏25 — Context, Memory, Trace

![Context](assets/01/13-context.png)

![Agent Trace](assets/01/09-agent-trace.png)

---

## ‏26 — Support Agent · מסכים

![Email](assets/screens/email-inbound.png)

![Tickets](assets/screens/ticketing-queue.png)

---

## ‏27 — Support Agent · CRM + Workbench

![CRM](assets/screens/crm-customer.png)

![Workbench](assets/screens/agent-workbench-support.png)

---

## ‏28 — ארכיטקטורה ו־Multi-Agent

![Agent Architecture](assets/01/16-agent-architecture.png)

![Multi-Agent](assets/01/12-multi-agent.png)

- ‏Agent הוא Software System  
- יותר אוטונומיה → יותר עלות, latency, Security  

---

## ‏29 — תרגיל 1: Agent או Workflow?

**הנחיה (10–15 דק׳):** לכל תרחיש — **Agent / Workflow / לא בטוח** + נימוק + **רמת Spectrum (L0–L6)**.

1. סיכום יומי של 50 מיילים לאותו פורמט  
2. חקירת תקלה בפרודקשן שלא חוזרת על עצמה  
3. שליחת חשבונית אחרי אישור אדם  
4. מענה ללקוח עם CRM + Knowledge Base  
5. העתקת קבצים A→B כל לילה  

**הגשה:** טבלה 5 שורות.

---

## ‏30 — תרגיל 2: תכנון Agent

**הנחיה (20–25 דק׳):** Nova Retail / ticket #8831 או משימה שלכם.

| שדה | תוכן |
|---|---|
| Goal | משפט אחד |
| Spectrum level | L? ולמה |
| Tools | 3–6 |
| Decisions | 2–3 |
| HITL | איפה אישור |
| Stop | מתי עוצרים |
| Risks | סיכון אחד |

---

## ‏31 — בדיקת הבנה + סיכום

1. במה Agent שונה מצ׳אטבוט?  
2. מה הקו בין L3 ל־L4?  
3. מה Observation ולמה קריטי?  
4. מתי עדיף Workflow?  
5. ‏Guardrail אחד שחובה כמעט תמיד?  

**לזכור:** Goal → Decide → Act → Observe · הספקטרום · Tools + Guardrails  

---

## ‏32 — למפגש הבא

**Planning ו-Execution** לעומק.

הכנה: הביאו דוגמה אחת מהעבודה שמתאימה ל-Agent (בלי לפתור עדיין).

</div>
