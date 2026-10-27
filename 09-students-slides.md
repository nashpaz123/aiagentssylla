<div dir="rtl" lang="he" style="direction: rtl; text-align: right; unicode-bidi: embed;">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 9 — מצגת סטודנטים
## ‏Debugging & Project · דיבוג Agents + שיחה עם LLM ב-API

> **משך משוער:** ~1.5–2 שעות (קצר ולעניין).  
> חלק א׳: דיבוג עם Claude Code / Lab 08.  
> חלק ב׳: פרויקט — Python → Ollama מקומי + OpenRouter בענן.

---

# ‏חלק א׳ — Debugging

## ‏1 — כותרת

**‏Debugging & Project**  
סוכן "עובד" רק אם אפשר להוכיח בלוג / ב-API — לא בנרטיב

---

## ‏2 — מילון קצר

| מונח | משמעות |
|---|---|
| ‏**Observation** | תוצאת כלי אמיתית (לא מה שהמודל סיפר) |
| ‏**Tool log** | `TOOL -> …` / `sent=true` |
| ‏**`/context`** | מה ממלא את החלון עכשיו |
| ‏**OpenAI-compatible API** | אותו פורמט ל-Ollama / OpenRouter / וכו׳ |

---

## ‏3 — כלל הזהב

**המודל משקר בנימוס.**  
האמת = תוצאת כלי · קובץ · HTTP · env — לא "שלחתי" / "תיקנתי".

---

## ‏4 — שלושת באגים הנפוצים

| באג | סימפטום | בדיקה |
|---|---|---|
| נרטיב בלי כלי | "שלחתי לטלגרם" | אין `notify_telegram` / `sent=true` |
| env חסר | "עובד אצלי" | `show` → `MISSING` |
| קונטקסט | שכח הוראה | `/context` · אחרי `/compact` הוראת צ׳אט נעלמה |

---

## ‏5 — דיבוג חי עם Claude (Lab 08)

```bash
cd labs/08-agent-surfaces
# export או .env עם ANTHROPIC + TELEGRAM_*
python3 surface_claude.py show
python3 surface_claude.py chat --lead L-SMB --message "שלח לטלגרם שלי"
```

חפשו בלוג: <code dir="ltr">TOOL -> notify_telegram</code> · `sent=true` · הודעה בנייד.

ב-Claude Code על תיקיית הדמו:

<pre dir="ltr"><code>/context</code></pre>

---

## ‏6 — צ׳קליסט דיבוג (להקליט)

- ‏[ ] יש קריאת כלי בלוג  
- ‏[ ] תוצאת הכלי `ok` / `sent=true`  
- ‏[ ] env מלא (`show`)  
- ‏[ ] אחרי compact — הוראות חשובות ב-`CLAUDE.md` / Rules  

---

# ‏חלק ב׳ — Project: LLM דרך Python API

## ‏7 — מטרת הפרויקט

עד עכשיו דיברנו עם מודלים בעיקר דרך צ׳אט (Cursor, Claude Code, ממשקי Web). בפרויקט הזה יורדים קומה למטה: איך **קוד Python** מדבר עם LLM — בלי UI — כמו שקורה באפליקציות ובשירותים אמיתיים.

המטרה פשוטה ומעשית: להריץ את **אותה** קריאת API פעם מול מודל מקומי (Ollama על המחשב שלכם) ופעם מול שירות ענן (OpenRouter), ולהבין שרוב הכלים מדברים בפורמט **OpenAI-compatible**. מחליפים בעיקר כתובת, מפתח ושם מודל — לא כותבים ספרייה חדשה לכל ספק.

בסוף תוכלו להדביק סקריפט קצר, לקבל תשובה מהמודל, ולדבג כשלים נפוצים (שירות כבוי, מודל חסר, מפתח שגוי). זה הבסיס לכל agent/runtime שקורא למודל מאחורי הקלעים.

---

## ‏8 — צ׳אט ≠ API

הצ׳אט הוא UI. מאחורי הקלעים רצה **קריאת API**.  
היום: אותה קריאה מ-Python — מקומית (Ollama) ובענן (OpenRouter).

---

## ‏9 — מונחים לפרויקט

| מונח | בקצרה |
|---|---|
| ‏**LLM** | מודל שעונה בשפה טבעית |
| ‏**Token** | יחידת טקסט למודל (לא תמיד מילה שלמה) |
| ‏**Ollama** | מריץ מודלים על המחשב שלכם (פורט <code dir="ltr">11434</code>) |
| ‏**OpenRouter** | שער לכמה מודלים בענן (כולל מסלול חינמי ל-lab) |
| ‏**OpenAI-compatible** | אותו SDK — מחליפים URL / key / model |
| ‏**API key** | מפתח שמזהה אתכם מול השירות (חובה ב-OpenRouter; ב-Ollama מקומי לא נבדק) |

---

## ‏10 — אילו קבצים לפתוח ולהבין

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

---

## ‏11 — מבנה הודעה (JSON בזיכרון)

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

---

## ‏12 — שלושת המשתנים (+ שמות אצלנו)

במאמרים/דוגמאות כלליות מופיע לפעמים `LLM_API_KEY` / `LLM_BASE_URL` / `MODEL`.  
**ב-Lab שלנו השמות מפורשים לפי backend:**

| רעיון כללי | Ollama (ב-`.env`) | OpenRouter (ב-`.env`) |
|---|---|---|
| כתובת | `OLLAMA_BASE_URL` | `OPENROUTER_BASE_URL` |
| מפתח | לא חובה (אפשר כל מחרוזת) | **`OPENROUTER_API_KEY`** ← זה ה-API key |
| מודל | `OLLAMA_MODEL` | `OPENROUTER_MODEL` |

ערכי ברירת מחדל — ראו <code dir="ltr">.env.example</code>.

---

## ‏13 — איך מייצרים API key ל-OpenRouter

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

---

## ‏14 — התקנות — פקודה־פקודה

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

---

## ‏15 — Lab — הרצה מפורטת

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

---

## ‏16 — מה קורה בקוד (לעקוב ב-`chat_llm.py`)

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

---

## ‏17 — Debug לפרויקט (Ollama · OpenRouter)

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

---

## ‏18 — סיכום

- דיבוג Agents: תוצאת כלי > סיפור המודל  
- פרויקט: צ׳אט UI ≠ API · קבצים ב-`labs/09-llm-api/`  
- מפתח ענן: `OPENROUTER_API_KEY` מ-openrouter.ai  
- דיבוג פרויקט: curl / pull / key / `--debug`  

---

## ‏19 — תרגיל בית

1. הריצו Ollama + OpenRouter עם אותו `--message` והשוו מהירות/סגנון  
2. הוסיפו `--system "Answer only in Hebrew"`  
3. כבו Ollama / מחקו מפתח — ודאו ש-`--debug` מציג כשל ברור  
4. קראו ב-`chat_llm.py` את `client_for` והסבירו בקול מה משתנה בין backends  
5. (בונוס) Lab 08: כבו token ובדקו כשל גלוי בלוג  

</div>
