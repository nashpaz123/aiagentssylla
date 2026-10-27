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
| ‏**Ollama** | מריץ מודלים על המחשב שלכם |
| ‏**OpenRouter** | שער לכמה מודלים בענן (כולל מסלול חינמי ל-lab) |
| ‏**OpenAI-compatible** | אותו SDK — מחליפים URL / key / model |

---

## ‏10 — מבנה הודעה

```json
[
  {"role": "system", "content": "Be brief."},
  {"role": "user", "content": "How do I boil an egg?"}
]
```

`system` אופציונלי · `user` = השאלה · `assistant` = תשובות קודמות (זיכרון שיחה).

---

## ‏11 — שלושת המשתנים

| משתנה | Ollama | OpenRouter |
|---|---|---|
| ‏`base_url` | <code dir="ltr">http://localhost:11434/v1</code> | <code dir="ltr">https://openrouter.ai/api/v1</code> |
| ‏`api_key` | כל מחרוזת (לא נבדק) | מפתח מ-OpenRouter |
| ‏`model` | למשל <code dir="ltr">qwen3.5:4b</code> | למשל <code dir="ltr">openai/gpt-4.1-nano</code> |

---

## ‏12 — התקנות קצרות

- ‏Python 3 + `pip install openai httpx`  
- ‏[Ollama](https://ollama.com/) רץ ברקע  
- חשבון + API key ב-[OpenRouter](https://openrouter.ai/)  

```bash
ollama pull qwen3.5:4b
```

---

## ‏13 — Lab — הרצה

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

---

## ‏14 — מה קורה בקוד (בקצרה)

```python
from openai import OpenAI
client = OpenAI(base_url=..., api_key=...)
resp = client.chat.completions.create(model=..., messages=[...])
print(resp.choices[0].message.content)
```

ספריית `openai` בונה את ה-HTTP · אתם רק בוחרים לאן להתחבר.

---

## ‏15 — Debug לפרויקט (Ollama · OpenRouter)

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

---

## ‏16 — סיכום

- דיבוג Agents: תוצאת כלי > סיפור המודל  
- פרויקט: צ׳אט UI ≠ API · Ollama + OpenRouter  
- דיבוג פרויקט: curl / pull / key / `--debug`  

---

## ‏17 — תרגיל בית

1. הריצו Ollama + OpenRouter עם אותו `--message` והשוו מהירות/סגנון  
2. הוסיפו `--system "Answer only in Hebrew"`  
3. כבו Ollama בכוונה / מחקו מפתח OpenRouter — ודאו ש-`--debug` מציג כשל ברור  
4. (בונוס) Lab 08: כבו token ובדקו כשל גלוי בלוג  

</div>
