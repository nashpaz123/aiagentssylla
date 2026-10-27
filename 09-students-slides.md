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

## ‏7 — צ׳אט ≠ API

הצ׳אט הוא UI. מאחורי הקלעים רצה **קריאת API**.  
היום: אותה קריאה מ-Python — מקומית (Ollama) ובענן (OpenRouter).

---

## ‏8 — מונחים לפרויקט

| מונח | בקצרה |
|---|---|
| ‏**LLM** | מודל שעונה בשפה טבעית |
| ‏**Token** | יחידת טקסט למודל (לא תמיד מילה שלמה) |
| ‏**Ollama** | מריץ מודלים על המחשב שלכם |
| ‏**OpenRouter** | שער לכמה מודלים בענן (כולל מסלול חינמי ל-lab) |
| ‏**OpenAI-compatible** | אותו SDK — מחליפים URL / key / model |

---

## ‏9 — מבנה הודעה

```json
[
  {"role": "system", "content": "Be brief."},
  {"role": "user", "content": "How do I boil an egg?"}
]
```

`system` אופציונלי · `user` = השאלה · `assistant` = תשובות קודמות (זיכרון שיחה).

---

## ‏10 — שלושת המשתנים

| משתנה | Ollama | OpenRouter |
|---|---|---|
| ‏`base_url` | <code dir="ltr">http://localhost:11434/v1</code> | <code dir="ltr">https://openrouter.ai/api/v1</code> |
| ‏`api_key` | כל מחרוזת (לא נבדק) | מפתח מ-OpenRouter |
| ‏`model` | למשל <code dir="ltr">qwen3.5:4b</code> | למשל <code dir="ltr">openai/gpt-4.1-nano</code> |

---

## ‏11 — התקנות קצרות

- ‏Python 3 + `pip install openai httpx`  
- ‏[Ollama](https://ollama.com/) רץ ברקע  
- חשבון + API key ב-[OpenRouter](https://openrouter.ai/)  

```bash
ollama pull qwen3.5:4b
```

---

## ‏12 — Lab — הרצה

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

## ‏13 — מה קורה בקוד (בקצרה)

```python
from openai import OpenAI
client = OpenAI(base_url=..., api_key=...)
resp = client.chat.completions.create(model=..., messages=[...])
print(resp.choices[0].message.content)
```

ספריית `openai` בונה את ה-HTTP · אתם רק בוחרים לאן להתחבר.

---

## ‏14 — סיכום

- דיבוג: תוצאת כלי > סיפור המודל  
- פרויקט: צ׳אט UI ≠ API  
- Ollama מקומי · OpenRouter ענן · אותו Python  
- מפגש הסיום המשולב — Testing + Capstone בפורמט קצר  

---

## ‏15 — תרגיל בית

1. הריצו Ollama + OpenRouter עם אותו `--message` והשוו מהירות/סגנון  
2. הוסיפו `--system "Answer only in Hebrew"`  
3. (בונוס) חזרו ל-Lab 08: כבו token במכוון ובדקו שהכשל גלוי בלוג  

</div>
