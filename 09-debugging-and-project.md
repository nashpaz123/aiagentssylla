<div dir="rtl" lang="he" style="direction: rtl; text-align: right; unicode-bidi: embed;">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 9 — תסריט מרצה
## ‏Debugging & Project

> מצגת: [`09-students-slides.md`](09-students-slides.md)  
> Lab דיבוג: [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/) · Lab פרויקט: [`labs/09-llm-api/`](labs/09-llm-api/)

**הכנה:** `.env` ל-Lab 08 · Ollama · מפתח OpenRouter ב-Lab 09.

---

## ‏1 — כותרת

[סטודנטים · 1]

**על המסך:**

**‏Debugging & Project**  
סוכן "עובד" רק אם אפשר להוכיח בלוג / ב-API — לא בנרטיב

**להקראה:**

**[פתיחה — דקה]**
היום קצרים: דיבוג Agents, ואז פרויקט API. בלי חזרה על מפגשים 1–8.

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

**[מילון]**
Observation = האמת. /context = רנטגן לחלון.

---

## ‏3 — כלל הזהב

[סטודנטים · 3]

**על המסך:**

**המודל משקר בנימוס.**  
האמת = תוצאת כלי · קובץ · HTTP · env — לא "שלחתי" / "תיקנתי".

**להקראה:**

**[כלל זהב]**
אמרו בקול: "אם אין שורת כלי בלוג — זה לא קרה."

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

**[שלושה באגים]**
עברו טבלה. דוגמה 1: Lab 08 בלי TELEGRAM. דוגמה 2: compact מחק הוראת צ׳אט.

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

**[דמו דיבוג — 8–10 דקות]**
```bash
cd labs/08-agent-surfaces
source .venv/bin/activate   # אם קיים
python3 surface_claude.py show
python3 surface_claude.py chat --lead L-SMB --message "שלח לטלגרם שלי"
```
הצביעו על TOOL ו-sent. אם אין env — תנו לזה להיכשל בכוונה קודם.
אופציונלי: `cd demos/08-context-opening && claude` ואז `/context`.

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

**[צ׳קליסט]**
הקריאו ארבע נקודות. עבור לפרויקט.

---

## ‏7 — מטרת הפרויקט

[סטודנטים · 7]

**על המסך:**

עד עכשיו דיברנו עם מודלים בעיקר דרך צ׳אט (Cursor, Claude Code, ממשקי Web). בפרויקט הזה יורדים קומה למטה: איך **קוד Python** מדבר עם LLM — בלי UI — כמו שקורה באפליקציות ובשירותים אמיתיים.

המטרה פשוטה ומעשית: להריץ את **אותה** קריאת API פעם מול מודל מקומי (Ollama על המחשב שלכם) ופעם מול שירות ענן (OpenRouter), ולהבין שרוב הכלים מדברים בפורמט **OpenAI-compatible**. מחליפים בעיקר כתובת, מפתח ושם מודל — לא כותבים ספרייה חדשה לכל ספק.

בסוף תוכלו להדביק סקריפט קצר, לקבל תשובה מהמודל, ולדבג כשלים נפוצים (שירות כבוי, מודל חסר, מפתח שגוי). זה הבסיס לכל agent/runtime שקורא למודל מאחורי הקלעים.

**להקראה:**

**[מטרת הפרויקט — 2–3 דקות]**
הקריאו את שלוש הפסקאות לאט. הדגישו:
1. יורדים מתחת לצ׳אט — לקריאת API ב-Python.  
2. אותו קוד · שני backends (מקומי וענן).  
3. בסוף יודעים להריץ ולדבג — זה הבסיס ל-runtime של agent.
אל תרוצו עדיין לקוד; קודם המסגרת.

---

## ‏8 — צ׳אט ≠ API

[סטודנטים · 8]

**על המסך:**

הצ׳אט הוא UI. מאחורי הקלעים רצה **קריאת API**.  
היום: אותה קריאה מ-Python — מקומית (Ollama) ובענן (OpenRouter).

**להקראה:**

**[צ׳אט ≠ API]**
משפט אחד: הצ׳אט הוא UI; היום נבנה את הקריאה שמתחתיו.

---

## ‏9 — מונחים לפרויקט

[סטודנטים · 9]

**על המסך:**

| מונח | בקצרה |
|---|---|
| ‏**LLM** | מודל שעונה בשפה טבעית |
| ‏**Token** | יחידת טקסט למודל (לא תמיד מילה שלמה) |
| ‏**Ollama** | מריץ מודלים על המחשב שלכם |
| ‏**OpenRouter** | שער לכמה מודלים בענן (כולל מסלול חינמי ל-lab) |
| ‏**OpenAI-compatible** | אותו SDK — מחליפים URL / key / model |

**להקראה:**

**[מונחים]**
Ollama = מקומי. OpenRouter = ענן. OpenAI-compatible = אותו SDK.

---

## ‏10 — מבנה הודעה

[סטודנטים · 10]

**על המסך:**

```json
[
  {"role": "system", "content": "Be brief."},
  {"role": "user", "content": "How do I boil an egg?"}
]
```

`system` אופציונלי · `user` = השאלה · `assistant` = תשובות קודמות (זיכרון שיחה).

**להקראה:**

**[JSON]**
הסבירו roles במשפט אחד כל אחד.

---

## ‏11 — שלושת המשתנים

[סטודנטים · 11]

**על המסך:**

| משתנה | Ollama | OpenRouter |
|---|---|---|
| ‏`base_url` | <code dir="ltr">http://localhost:11434/v1</code> | <code dir="ltr">https://openrouter.ai/api/v1</code> |
| ‏`api_key` | כל מחרוזת (לא נבדק) | מפתח מ-OpenRouter |
| ‏`model` | למשל <code dir="ltr">qwen3.5:4b</code> | למשל <code dir="ltr">openai/gpt-4.1-nano</code> |

**להקראה:**

**[שלושת המשתנים]**
לב הפרויקט: מחליפים רק URL, key, model.

---

## ‏12 — התקנות קצרות

[סטודנטים · 12]

**על המסך:**

- ‏Python 3 + `pip install openai httpx`  
- ‏[Ollama](https://ollama.com/) רץ ברקע  
- חשבון + API key ב-[OpenRouter](https://openrouter.ai/)  

```bash
ollama pull qwen3.5:4b
```

**להקראה:**

**[התקנות]**
אם כבר מותקן — דלגו. אחרת: Ollama, `ollama pull qwen3.5:4b`, מפתח OpenRouter.

---

## ‏13 — Lab — הרצה

[סטודנטים · 13]

**על המסך:**

תיקייה: [`labs/09-llm-api/`](labs/09-llm-api/)

```bash
cd labs/09-llm-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

python3 chat_llm.py --backend ollama --message "Hi — who are you? One sentence."
# מלאו OPENROUTER_API_KEY ב-.env ואז:
python3 chat_llm.py --backend openrouter --message "Hi — who are you? One sentence."
```

**להקראה:**

**[Lab חי — 10–12 דקות]**
```bash
cd labs/09-llm-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 chat_llm.py --backend ollama --message "Hi — who are you? One sentence."
```
אחר כך OpenRouter. השוו מהירות בקול.

---

## ‏14 — מה קורה בקוד (בקצרה)

[סטודנטים · 14]

**על המסך:**

```python
from openai import OpenAI
client = OpenAI(base_url=..., api_key=...)
resp = client.chat.completions.create(model=..., messages=[...])
print(resp.choices[0].message.content)
```

ספריית `openai` בונה את ה-HTTP · אתם רק בוחרים לאן להתחבר.

**להקראה:**

**[קוד]**
פתחו chat_llm.py. שלוש שורות: OpenAI(...), create(...), choices[0].

---

## ‏15 — Debug לפרויקט (Ollama · OpenRouter)

[סטודנטים · 15]

**על המסך:**

אותו כלל זהב — עכשיו על ה-API שלכם.

| כשל | בדיקה מדויקת |
|---|---|
| ‏Connection refused | Ollama רץ? <code dir="ltr">curl -s http://localhost:11434</code> |
| ‏model not found | <code dir="ltr">ollama pull qwen3.5:4b</code> · שם המודל ב-`.env` |
| ‏401 / missing key | `OPENROUTER_API_KEY` ב-`.env` או `export` |
| ‏תשובה ריקה / Exception | הריצו עם <code dir="ltr">--debug</code> · קראו את הודעת השגיאה המלאה |
| ‏עובד ב-Ollama נכשל ב-OpenRouter | בדקו שרק `backend` + 3 משתנים השתנו — לא קוד אחר |

```bash
cd labs/09-llm-api
python3 chat_llm.py --backend ollama --debug --message "ping"
python3 chat_llm.py --backend openrouter --debug --message "ping"
```

**להקראה:**

**[Debug פרויקט — 5–7 דקות]**
כשל בכוונה ואז תיקון:
```bash
curl -s http://localhost:11434 || echo "Ollama down"
python3 chat_llm.py --backend ollama --debug --message ping
```
ואז OpenRouter בלי מפתח. "האמת בהודעת השגיאה."

---

## ‏16 — סיכום

[סטודנטים · 16]

**על המסך:**

- דיבוג Agents: תוצאת כלי > סיפור המודל  
- פרויקט: צ׳אט UI ≠ API · Ollama + OpenRouter  
- דיבוג פרויקט: curl / pull / key / `--debug`

**להקראה:**

**[סיכום]**
דיבוג Agents + מטרת פרויקט + API + דיבוג API.

---

## ‏17 — תרגיל בית

[סטודנטים · 17]

**על המסך:**

1. הריצו Ollama + OpenRouter עם אותו `--message` והשוו מהירות/סגנון  
2. הוסיפו `--system "Answer only in Hebrew"`  
3. כבו Ollama בכוונה / מחקו מפתח OpenRouter — ודאו ש-`--debug` מציג כשל ברור  
4. (בונוס) Lab 08: כבו token ובדקו כשל גלוי בלוג  

</div>

**להקראה:**

**[בית]**
הקריאו את הפריטים. הדגישו debug מכוון.

---

</div>
