<div dir="rtl" lang="he" style="direction: rtl; text-align: right; unicode-bidi: embed;">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 9 — תסריט מרצה
## ‏Debugging & Project

> מצגת: [`09-students-slides.md`](09-students-slides.md)  
> Lab פרויקט: [`labs/09-llm-api/`](labs/09-llm-api/) · דיבוג Agents: [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/)

**הכנה:** Lab 08 env · Ollama · מפתח OpenRouter מוכן מראש להקלטה.

---

## ‏1 — כותרת

[סטודנטים · 1]

**על המסך:**

**‏Debugging & Project**  
סוכן "עובד" רק אם אפשר להוכיח בלוג / ב-API — לא בנרטיב

**להקראה:**

**[פתיחה]** דיבוג ואז פרויקט API. קצרים.

---

## ‏2 — מילון קצר

[סטודנטים · 2]

**על המסך:**

| מונח | משמעות |
|---|---|
| ‏**Observation** | תוצאת כלי אמיתית (לא מה שהמודל סיפר) |
| ‏**Tool log** | `TOOL -> …` / `sent=true` |
| ‏**`/context`** | מה ממלא את החלון עכשיו |
| ‏**OpenAI-compatible API** | אותו פורמט ל-Ollama / OpenRouter / וכו׳ |

**להקראה:**

**[מילון]** Observation = אמת. /context = רנטגן.

---

## ‏3 — כלל הזהב

[סטודנטים · 3]

**על המסך:**

**המודל משקר בנימוס.**  
האמת = תוצאת כלי · קובץ · HTTP · env — לא "שלחתי" / "תיקנתי".

**להקראה:**

**[כלל זהב]** בלי שורת כלי בלוג — זה לא קרה.

---

## ‏4 — שלושת באגים הנפוצים

[סטודנטים · 4]

**על המסך:**

| באג | סימפטום | בדיקה |
|---|---|---|
| נרטיב בלי כלי | "שלחתי לטלגרם" | אין `notify_telegram` / `sent=true` |
| env חסר | "עובד אצלי" | `show` → `MISSING` |
| קונטקסט | שכח הוראה | `/context` · אחרי `/compact` הוראת צ׳אט נעלמה |

**להקראה:**

**[באגים]** טבלה + דוגמאות Lab 08 / compact.

---

## ‏5 — דיבוג חי עם Claude (Lab 08)

[סטודנטים · 5]

**על המסך:**

```bash
cd labs/08-agent-surfaces
# export או .env עם ANTHROPIC + TELEGRAM_*
python3 surface_claude.py show
python3 surface_claude.py chat --lead L-SMB --message "שלח לטלגרם שלי"
```

חפשו בלוג: <code dir="ltr">TOOL -> notify_telegram</code> · `sent=true` · הודעה בנייד.

ב-Claude Code על תיקיית הדמו:

<pre dir="ltr"><code>/context</code></pre>

**להקראה:**

**[דמו דיבוג]**
```bash
cd labs/08-agent-surfaces && python3 surface_claude.py show
python3 surface_claude.py chat --lead L-SMB --message "שלח לטלגרם שלי"
```

---

## ‏6 — צ׳קליסט דיבוג (להקליט)

[סטודנטים · 6]

**על המסך:**

- ‏[ ] יש קריאת כלי בלוג  
- ‏[ ] תוצאת הכלי `ok` / `sent=true`  
- ‏[ ] env מלא (`show`)  
- ‏[ ] אחרי compact — הוראות חשובות ב-`CLAUDE.md` / Rules  

---

# ‏חלק ב׳ — Project: LLM דרך Python API

**להקראה:**

**[צ׳קליסט]** ארבע נקודות → מעבר לפרויקט.

---

## ‏7 — מטרת הפרויקט

[סטודנטים · 7]

**על המסך:**

עד עכשיו דיברנו עם מודלים בעיקר דרך צ׳אט (Cursor, Claude Code, ממשקי Web). בפרויקט הזה יורדים קומה למטה: איך **קוד Python** מדבר עם LLM — בלי UI — כמו שקורה באפליקציות ובשירותים אמיתיים.

המטרה פשוטה ומעשית: להריץ את **אותה** קריאת API פעם מול מודל מקומי (Ollama על המחשב שלכם) ופעם מול שירות ענן (OpenRouter), ולהבין שרוב הכלים מדברים בפורמט **OpenAI-compatible**. מחליפים בעיקר כתובת, מפתח ושם מודל — לא כותבים ספרייה חדשה לכל ספק.

בסוף תוכלו להדביק סקריפט קצר, לקבל תשובה מהמודל, ולדבג כשלים נפוצים (שירות כבוי, מודל חסר, מפתח שגוי). זה הבסיס לכל agent/runtime שקורא למודל מאחורי הקלעים.

**להקראה:**

**[מטרה]** שלוש פסקאות לאט. יורדים מתחת לצ׳אט.

---

## ‏8 — צ׳אט ≠ API

[סטודנטים · 8]

**על המסך:**

הצ׳אט הוא UI. מאחורי הקלעים רצה **קריאת API**.  
היום: אותה קריאה מ-Python — מקומית (Ollama) ובענן (OpenRouter).

**להקראה:**

**[UI≠API]** משפט אחד.

---

## ‏9 — מונחים לפרויקט

[סטודנטים · 9]

**על המסך:**

| מונח | בקצרה |
|---|---|
| ‏**LLM** | מודל שעונה בשפה טבעית |
| ‏**Token** | יחידת טקסט למודל (לא תמיד מילה שלמה) |
| ‏**Ollama** | מריץ מודלים על המחשב שלכם (פורט <code dir="ltr">11434</code>) |
| ‏**OpenRouter** | שער לכמה מודלים בענן (כולל מסלול חינמי ל-lab) |
| ‏**OpenAI-compatible** | אותו SDK — מחליפים URL / key / model |
| ‏**API key** | מפתח שמזהה אתכם מול השירות (חובה ב-OpenRouter; ב-Ollama מקומי לא נבדק) |

**להקראה:**

**[מונחים]** כולל API key — חובה בענן בלבד.

---

## ‏10 — אילו קבצים לפתוח ולהבין

[סטודנטים · 10]

**על המסך:**

תיקייה: <code dir="ltr">labs/09-llm-api/</code>

| קובץ | למה מסתכלים |
|---|---|
| ‏<code dir="ltr">chat_llm.py</code> | כל הלוגיקה: טעינת `.env`, בחירת backend, בניית `messages`, קריאת API |
| ‏<code dir="ltr">.env.example</code> | תבנית משתנים — מה להעתיק ל-`.env` |
| ‏<code dir="ltr">.env</code> | הסודות שלכם (לא בגיט) — מפתח OpenRouter + שמות מודלים |
| ‏<code dir="ltr">requirements.txt</code> | תלויות: `openai`, `httpx` |
| ‏<code dir="ltr">README.md</code> | מדריך הרצה + דיבוג |

**בתוך `chat_llm.py` — פונקציות חשובות:**

| חלק בקוד | מה עושה |
|---|---|
| ‏`load_dotenv` | קורא שורות `KEY=value` מ-`.env` ל-`os.environ` (רק אם עדיין לא הוגדר ב-export) |
| ‏`client_for("ollama")` | בונה `OpenAI(base_url=localhost:11434/v1, …)` + שם מודל מקומי |
| ‏`client_for("openrouter")` | דורש `OPENROUTER_API_KEY`, מצביע ל-`https://openrouter.ai/api/v1` |
| ‏`main` | מפרסר `--backend` / `--message` / `--system` / `--debug` ושולח `chat.completions.create` |

אין כאן JSON נתונים נפרד (בניגוד ל-Lab 08) — ה"חוזה" הוא רשימת הודעות בזיכרון + משתני סביבה.

**להקראה:**

**[קבצים — 4–5 דקות]**
פתחו ב-Cursor/IDE את `labs/09-llm-api/`.
1. `.env.example` על המסך — מה המשתנים.  
2. `chat_llm.py` — גללו ל-`client_for` ו-`main`.  
3. אמרו: אין JSON עסקי; ההודעות נבנות מ-CLI.

---

## ‏11 — מבנה הודעה (JSON בזיכרון)

[סטודנטים · 11]

**על המסך:**

זה מה שנשלח ל-API (לא קובץ בדיסק):

```json
[
  {"role": "system", "content": "Be brief."},
  {"role": "user", "content": "How do I boil an egg?"}
]
```

| ‏`role` | משמעות |
|---|---|
| ‏`system` | הוראות התנהגות (אופציונלי) — אצלנו דרך <code dir="ltr">--system</code> |
| ‏`user` | מה שאתם שואלים — <code dir="ltr">--message</code> |
| ‏`assistant` | תשובות קודמות (לשיחה רב־סיבובית; לא חובה ב-lab הבסיסי) |

**להקראה:**

**[messages]** טבלת roles. הראו התאמה ל-`--message` / `--system`.

---

## ‏12 — שלושת המשתנים (+ שמות אצלנו)

[סטודנטים · 12]

**על המסך:**

במאמרים/דוגמאות כלליות מופיע לפעמים `LLM_API_KEY` / `LLM_BASE_URL` / `MODEL`.  
**ב-Lab שלנו השמות מפורשים לפי backend:**

| רעיון כללי | Ollama (ב-`.env`) | OpenRouter (ב-`.env`) |
|---|---|---|
| כתובת | `OLLAMA_BASE_URL` | `OPENROUTER_BASE_URL` |
| מפתח | לא חובה (אפשר כל מחרוזת) | **`OPENROUTER_API_KEY`** ← זה ה-API key |
| מודל | `OLLAMA_MODEL` | `OPENROUTER_MODEL` |

ערכי ברירת מחדל — ראו <code dir="ltr">.env.example</code>.

**להקראה:**

**[משתנים]** הדגישו: אצלנו OPENROUTER_API_KEY לא LLM_API_KEY כללי.

---

## ‏13 — איך מייצרים API key ל-OpenRouter

[סטודנטים · 13]

**על המסך:**

Ollama מקומי **לא** דורש מפתח אמיתי. לענן:

1. היכנסו ל-<code dir="ltr">https://openrouter.ai</code> והירשמו (אימייל).  
2. לחצו **Keys** / **Create API Key** (לעיתים דרך "Get API Key" במסך הבית).  
3. תנו שם למפתח; אפשר credit limit לפי מה שהממשק מציע (ל-lab מספיק מפתח חינמי/מודל חינמי).  
4. **העתיקו את המפתח מיד** (בדרך כלל מתחיל ב-`sk-or-v1-…`) — לא תוכלו לראות שוב את המלא.  
5. שימו ב-`.env`:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

או בטרמינל:

```bash
export OPENROUTER_API_KEY='sk-or-v1-...'
```

אל תשימו מפתח בגיט / בצילום מסך בהקלטה.

**להקראה:**

**[יצירת מפתח — 3–4 דקות]**
על המסך (או צילום מוכן): openrouter.ai → Keys → Create.
העתיקו ל-`.env`. אמרו מה קורה בלי מפתח (`CONFIG ERROR`).
Ollama לא צריך מפתח אמיתי.

---

## ‏14 — התקנות — פקודה־פקודה

[סטודנטים · 14]

**על המסך:**

**Python + ספריות (חד־פעמי בתיקיית ה-Lab):**

```bash
cd labs/09-llm-api
python3 -m venv .venv          # סביבה מבודדת
source .venv/bin/activate        # Linux/macOS; ב-Windows: .venv\Scripts\activate
pip install -r requirements.txt  # מתקין openai + httpx
cp .env.example .env             # יוצרים קובץ סודות מקומי
```

**Ollama:**

1. התקינו מ-<code dir="ltr">https://ollama.com</code> והפעילו את האפליקציה.  
2. משכו מודל קל (לוקח מקום בדיסק):

```bash
ollama pull qwen3.5:4b   # מוריד את המשקולות למחשב
ollama list                # מוודאים שהמודל מופיע
curl -s http://localhost:11434   # אמור להחזיר משהו בסגנון Ollama is running
```

3. אופציונלי — צ׳אט CLI לוודא שהמודל חי:

```bash
ollama run qwen3.5:4b
# כתבו Hi ואז /bye ליציאה
```

**OpenRouter:** צרו מפתח (שקף 13) ומלאו ב-`.env`.

**להקראה:**

**[התקנות]**
הריצו/הקריאו כל פקודה ומה היא עושה (venv, pip, pull, curl).

---

## ‏15 — Lab — הרצה מפורטת

[סטודנטים · 15]

**על המסך:**

```bash
cd labs/09-llm-api
source .venv/bin/activate

# --- מסלול A: מקומי ---
python3 chat_llm.py --backend ollama \
  --message "Hi — who are you? One sentence."
# מדפיס: backend=ollama model=… ואז תשובת המודל

# עם system role:
python3 chat_llm.py --backend ollama \
  --system "Answer only in Hebrew." \
  --message "What is an API?"

# --- מסלול B: ענן (אחרי OPENROUTER_API_KEY ב-.env) ---
python3 chat_llm.py --backend openrouter \
  --message "Hi — who are you? One sentence."
```

| ארגומנט | מה עושה |
|---|---|
| ‏`--backend ollama\|openrouter` | בוחר לאן מתחברים (`client_for`) |
| ‏`--message "..."` | תוכן הודעת `user` |
| ‏`--system "..."` | מוסיף הודעת `system` לפני ה-user |
| ‏`--debug` | מדפיס base_url, model, האם יש key, usage, שגיאות מלאות |

**להקראה:**

**[Lab חי]**
```bash
cd labs/09-llm-api && source .venv/bin/activate
python3 chat_llm.py --backend ollama --message "Hi — who are you? One sentence."
python3 chat_llm.py --backend openrouter --message "Hi — who are you? One sentence."
```
עברו על טבלת הארגומנטים.

---

## ‏16 — מה קורה בקוד (לעקוב ב-`chat_llm.py`)

[סטודנטים · 16]

**על המסך:**

```python
from openai import OpenAI
client = OpenAI(base_url=..., api_key=...)
resp = client.chat.completions.create(model=..., messages=[...])
print(resp.choices[0].message.content)
```

| שורה | משמעות |
|---|---|
| ‏`OpenAI(...)` | פותח "קו" לשרת ה-API (לא OpenAI בלבד — גם Ollama/OpenRouter) |
| ‏`chat.completions.create` | שולח את ה-`messages` וממתין לתשובה |
| ‏`choices[0].message.content` | הטקסט של התשובה הראשונה |

בקוד המלא: `load_dotenv(ROOT / ".env")` רץ לפני הכול; `--debug` מדפיס את החיבור לפני/אחרי הקריאה.

**להקראה:**

**[קוד]** שלוש השורות + איפה זה ב-chat_llm.py.

---

## ‏17 — Debug לפרויקט (Ollama · OpenRouter)

[סטודנטים · 17]

**על המסך:**

| כשל | בדיקה מדויקת |
|---|---|
| ‏Connection refused | Ollama רץ? <code dir="ltr">curl -s http://localhost:11434</code> |
| ‏model not found | <code dir="ltr">ollama pull qwen3.5:4b</code> · השוו ל-`OLLAMA_MODEL` ב-`.env` |
| ‏401 / missing key | פתחו `.env` · ודאו `OPENROUTER_API_KEY=sk-or-v1-…` בלי רווחים/מרכאות שבורות |
| ‏תשובה ריקה / Exception | <code dir="ltr">--debug</code> · קראו `API ERROR` / traceback |
| ‏עובד ב-Ollama נכשל ב-OpenRouter | רק `--backend` + משתני `.env` — לא קוד אחר |

```bash
python3 chat_llm.py --backend ollama --debug --message "ping"
python3 chat_llm.py --backend openrouter --debug --message "ping"
```

**להקראה:**

**[Debug]**
כשל מכוון + `--debug`. curl ל-11434. מפתח חסר.

---

## ‏18 — סיכום

[סטודנטים · 18]

**על המסך:**

- דיבוג Agents: תוצאת כלי > סיפור המודל  
- פרויקט: צ׳אט UI ≠ API · קבצים ב-`labs/09-llm-api/`  
- מפתח ענן: `OPENROUTER_API_KEY` מ-openrouter.ai  
- דיבוג פרויקט: curl / pull / key / `--debug`

**להקראה:**

**[סיכום]** נקודות על המסך.

---

## ‏19 — תרגיל בית

[סטודנטים · 19]

**על המסך:**

1. הריצו Ollama + OpenRouter עם אותו `--message` והשוו מהירות/סגנון  
2. הוסיפו `--system "Answer only in Hebrew"`  
3. כבו Ollama / מחקו מפתח — ודאו ש-`--debug` מציג כשל ברור  
4. קראו ב-`chat_llm.py` את `client_for` והסבירו בקול מה משתנה בין backends  
5. (בונוס) Lab 08: כבו token ובדקו כשל גלוי בלוג  

</div>

**להקראה:**

**[בית]** הדגישו קריאת client_for + debug מכוון.

---

</div>
