<div dir="rtl" lang="he">

# ‏הדגמת פתיחה — מפגש 5: צוות של 3 סוכנים ב-Claude Code (או Cursor)

**משך:** ~5–8 דקות על המסך. **מטרה:** לראות Multi-Agent אמיתי *לפני* שמסבירים אותו — תפקידים, מסירה (hand-off), ביקורת.

## ‏מה בתיקייה

| קובץ | תפקיד |
|---|---|
| ‏`policy.md` | מקור האמת — מדיניות החזרים (6 סעיפים) |
| ‏`brief.md` | הבקשה: FAQ קצר בעברית ללקוחות |
| ‏`.claude/agents/researcher.md` | סוכן 1 — עובדות בלבד, קריאה בלבד |
| ‏`.claude/agents/writer.md` | סוכן 2 — כותב `out/faq.md` מהעובדות בלבד |
| ‏`.claude/agents/reviewer.md` | סוכן 3 — משווה למדיניות, מחזיר `APPROVE` / `REVISE`, קריאה בלבד |
| ‏`prompt.md` | הוראות ה-Orchestrator: סדר, תקרת 2 סבבים, "NEEDS HUMAN" |
| ‏`run-claude.sh` | הרצה אחת לא-אינטראקטיבית (`claude -p`) |
| ‏`prompt-cursor.md` | אותה הדגמה בצ׳אט של Cursor (subagents דרך Task) |
| ‏`out/` | התוצרים: `facts.md`, `faq.md`, `review.md` (לא נשמרים ב-git) |
| ‏`sample-output/` | תוצרים מהרצת בדיקה אמיתית — גיבוי להקלטה |

## ‏הרצה — Claude Code

**להקלטה (רואים את הקריאות לכל subagent בזמן אמת):**

```bash
cd demos/05-crew-opening
claude                 # סשן אינטראקטיבי
/agents                # מציג את researcher / writer / reviewer מהתיקייה
# ואז מדביקים את התוכן של prompt.md
```

**לא-אינטראקטיבי (בדיקה / חזרה מהירה, ~70 שניות):**

```bash
./run-claude.sh
```

הרצת בדיקה אמיתית (Claude Code 2.1): שלושת הסוכנים רצו בתור, סבב ביקורת אחד, `VERDICT: APPROVE`.
התוצרים שהתקבלו שמורים ב-`sample-output/` — אפשר להראות אותם אם אין רשת בזמן ההקלטה.

מה להראות על המסך תוך כדי:

1. את שלושת הקבצים ב-`.claude/agents/` — frontmatter: `name`, `tools`, `model`, ואז פרומפט התפקיד.
2. בפלט: ה-Orchestrator קורא ל-Task לכל סוכן **בתור**, ומקבל חזרה סיכום קצר — לא את כל ההקשר של הסוכן.
3. ‏`out/review.md` — הפסיקה. אם `REVISE`: סבב שני של Writer + Reviewer. מקסימום 2 סבבים.
4. הסיכום בסוף: מי רץ, מה ייצר, כמה סבבים, פסיקה סופית.

## ‏הרצה — Cursor (חלופה)

פתחו את התיקייה הזו ב-Cursor, פתחו צ׳אט Agent, והדביקו את התוכן של `prompt-cursor.md`.
ה-Agent יפעיל subagents (Task) לפי התפקידים ויכתוב ל-`out/`.

## ‏למה ההדגמה הזאת

- אותו רעיון כמו CrewAI: **תפקיד = פרומפט מערכת + כלים מורשים + תקציב**.
- ה-Reviewer רואה רק את ה-artifact (`faq.md`) — לא את ה"מחשבות" של ה-Writer. זו בידוד הקשר (context isolation).
- תקרת סבבים + "NEEDS HUMAN" = ה-Budget וה-HITL ממפגשים 2 ו-4, מיושמים על צוות.

## ‏אם משהו נכשל

- ‏`claude: command not found` — התקינו Claude Code או השתמשו בחלופת Cursor.
- הסוכנים לא מופיעים — ודאו שאתם מריצים מתוך התיקייה (`.claude/agents/` יחסי לתיקיית העבודה).
- בקשת הרשאה לכתיבה — זה ה-HITL של הכלי עצמו; אשרו רק כתיבה ל-`out/`.

</div>
