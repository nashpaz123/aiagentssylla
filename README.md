<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏AI Agents — חומרי הקלטה (סילבוס)

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
- **יעד משך:** ~2.5–3 שעות לתוכן מוקלט (כולל תרגילים והדגמות).

## ‏מוכן עכשיו

| מפגש | מרצה | סטודנטים | נכסים |
|---|---|---|---|
| 1 מבוא ל-Agents | [`01-introduction-to-ai-agents.md`](01-introduction-to-ai-agents.md) | [`01-students-slides.md`](01-students-slides.md) | `assets/01/` |
| 2 Planning & Execution | [`02-agent-planning-and-execution.md`](02-agent-planning-and-execution.md) | [`02-students-slides.md`](02-students-slides.md) | `assets/02/` |

## ‏חידוש דיאגרמות וצילומי מסך

```bash
python3 scripts/gen_diagrams.py   # דיאגרמות ארכיטקטורה
python3 scripts/gen_mock_uis.py   # צילומי מסך להדגמות (CRM/K8s/CI/…)
```

**הערת הקלטה:** צילומי המסך להדגמות נמצאים ב־`assets/screens/` (נוחים למעבר בהקלטה).


## ‏מפגשים הבאים (מהסילבוס)

3 Tool Use · 4 LangGraph · 5 CrewAI/Multi-Agent · 6 Memory · 7 Business · 8 Cursor · 9 Testing · 10 Capstone

</div>
