<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏AI Agents — חומרי הקלטה (סילבוס)

> **פורמט:** הקלטה מראש — **לא** שיעור מול קהל חי.  
> המרצה מקריא תסריט ומציג את מצגת הסטודנטים; אין אינטראקציה חיה עם תלמידים בזמן הצילום.  
> **מפגש 7 ואילך:** Labs והדגמות מבוססי מפתח/מודל (Anthropic · Claude Code · Cursor) — לא משקיעים במסלולי fallback דטרמיניסטיים בלי API.

> תיקייה: `/stuff/prj/aiagentssylla/`  
> מקור סילבוס: `AI Agents ומערכות אוטונומיות - סילבוס.pdf`

## ‏מבנה לכל מפגש

| קובץ | קהל | תוכן |
|---|---|---|
| `NN-….md` | **מרצה** | תסריט מלא להקראה, סימוני מצלמה, הדגמות, נספחים |
| `NN-students-slides.md` | **סטודנטים** | מצגת קצרה + הנחיות תרגילים |
| `assets/NN/` | שניהם | דיאגרמות וצילומי־הדגמה (PNG) |

### ‏סנכרון להקלטה (חובה בכל מפגש)

- **מצגת הסטודנטים = עמוד השדרה** על המסך בהקלטה (מספור `1…N` בלבד).
- מצגת המרצה עוקבת **אחד־לאחד**: לכל מספר סטודנטים בלוק `## N — …` עם `[סטודנטים · N]` ואותה כותרת.
- מותר לנפח את תסריט ההקראה תחת כל בלוק; **אסור** סעיפי תוכן מרצה באמצע בלי מספר סטודנטים תואם.
- **החל ממפגש 2:** כל בלוק קוד / פסאודוקוד במצגת המרצה חייב להופיע גם במצגת הסטודנטים (באותו מספר).
- **יעד משך לכל מפגש (ממפגש 2 והלאה):** **יותר משעתיים**, יעד **~2.5–3 שעות הקלטה רצופה**.  
  התסריט חייב להיות **צפוף להקראה** — פירוט מלא על כל דוגמה, בלי קיצורי דרך.
- **הקלטה ≠ כיתה חיה:** אין שקט לחשיבה, אין איסוף תשובות מקהל, אין זמן פתרון עצמאי לסטודנטים.  
  תרגילים = **הדגמת מרצה** עם פתרון מלא בקול (או Lab שהמרצה מריץ).
- **מפגש 2:** Lab חי read-only (`labs/02-aws-agent-loop/`, פרופיל `nashpazformatan`) + הדגמות פתרון מורחבות; חזרה על מפגש 1 — מצביע קצר בלבד.
- **מפגש 3:** Lab Host ל-Function Calling (`labs/03-tool-calling/`, פרופיל `nashpazformatan`) — Validate · Parallel · Observations; הדגמת MCP חיה עם PinchTab headed (`labs/03-pinchtab-mcp/`); חזרה על מפגש 2 — מצביע קצר בלבד.
- **מפגש 4:** Lab גרף LangGraph דטרמיניסטי בלי מפתח LLM (`labs/04-langgraph-basics/`) — State · Conditional edges · לוג צמתים; חזרה על מפגש 3 — מצביע קצר בלבד; מילון ראשי תיבות (MCP · RAG · HITL …) חובה בהקראה.
- **מפגש 5 (קצר יותר — ~2–2.5 שעות):** נפתח ב**הדגמה חיה** של צוות 3 subagents ב-Claude Code / Cursor (`demos/05-crew-opening/`), ואז CrewAI (Agent · Task · Crew · Process), Guardrails לצוות, ו-Lab (`labs/05-crewai-multi-agent/` — `mini_crew.py` בלי מפתח, `crew_demo.py` עם CrewAI אמיתי).
- **מפגש 6 (~2–2.5 שעות):** הדגמת פתיחה מומלצת ב-Claude Code/Cursor (`demos/06-memory-opening/`) — Store ב-`out/store.json`, 99 מול 101; Lab עם `memory_claude.py` + `ANTHROPIC_API_KEY` (או `memory_lab.py` בלי מפתח) וכפתורים (`--fresh-thread` / `forget`).
- **מפגש 7 (~2.5–3.5 שעות):** Agents לאוטומציה עסקית (Sales Ops) — הדגמת Claude Code/Cursor (`demos/07-sales-opening/`) עם SMB/ENT/NOMAIL; Lab עם `sales_claude.py` + `ANTHROPIC_API_KEY` (שערי הנחה, HITL מנהל, upsell). תדריך מנהלים: [`07-exec-briefing.md`](07-exec-briefing.md). **בלי מסלול דטרמיניסטי ללא מפתח.**
- **מפגש 8 (~2.5–3.5 שעות):** Cursor + Claude Code (בלי Copilot) + משטחי פלט — הדגמת HTML + שליחת Telegram אמיתית (`demos/08-surface-opening/` + `send-telegram.sh`); Lab עם `surface_claude.py` + `ANTHROPIC_API_KEY` + `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` (צ׳אט פנימי שלכם). תדריך: [`08-exec-briefing.md`](08-exec-briefing.md).

## ‏מוכן עכשיו

| מפגש | מרצה | סטודנטים | נכסים |
|---|---|---|---|
| 1 מבוא ל-Agents | [`01-introduction-to-ai-agents.md`](01-introduction-to-ai-agents.md) | [`01-students-slides.md`](01-students-slides.md) | `assets/01/` |
| 2 Planning & Execution | [`02-agent-planning-and-execution.md`](02-agent-planning-and-execution.md) | [`02-students-slides.md`](02-students-slides.md) | `assets/02/` |
| 3 Tool Use & Function Calling | [`03-tool-use-and-function-calling.md`](03-tool-use-and-function-calling.md) | [`03-students-slides.md`](03-students-slides.md) | `assets/03/` |
| 4 LangGraph | [`04-langgraph-for-agents.md`](04-langgraph-for-agents.md) | [`04-students-slides.md`](04-students-slides.md) | `assets/04/` |
| 5 CrewAI & Multi-Agent | [`05-crewai-multi-agent.md`](05-crewai-multi-agent.md) | [`05-students-slides.md`](05-students-slides.md) | `assets/05/` · `demos/05-crew-opening/` |
| 6 Memory & State | [`06-memory-and-state.md`](06-memory-and-state.md) | [`06-students-slides.md`](06-students-slides.md) | `assets/06/` · `demos/06-memory-opening/` |
| 7 Business automation | [`07-business-automation.md`](07-business-automation.md) · תדריך מנהלים: [`07-exec-briefing.md`](07-exec-briefing.md) | [`07-students-slides.md`](07-students-slides.md) | `assets/07/` · `demos/07-sales-opening/` |
| 8 Cursor · Claude · Surfaces | [`08-cursor-claude-surfaces.md`](08-cursor-claude-surfaces.md) · תדריך: [`08-exec-briefing.md`](08-exec-briefing.md) | [`08-students-slides.md`](08-students-slides.md) | `assets/08/` · `demos/08-surface-opening/` |

## ‏חידוש דיאגרמות וצילומי מסך

```bash
python3 scripts/gen_diagrams.py   # דיאגרמות ארכיטקטורה
python3 scripts/gen_mock_uis.py   # צילומי מסך להדגמות (CRM/K8s/CI/…)
```

**הערת הקלטה:** צילומי המסך להדגמות נמצאים ב־`assets/screens/` (נוחים למעבר בהקלטה).

## ‏מפגשים הבאים (מהסילבוס)

9 Testing · 10 Capstone

</div>
