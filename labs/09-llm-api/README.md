<div dir="rtl" lang="he" style="direction: rtl; text-align: right; unicode-bidi: embed;">

# ‏Lab 09 — שיחה עם LLM ב-Python (Ollama · OpenRouter)

## ‏מטרת הפרויקט

עד עכשיו דיברנו עם מודלים בעיקר דרך צ׳אט (Cursor, Claude Code, ממשקי Web). בפרויקט הזה יורדים קומה למטה: איך **קוד Python** מדבר עם LLM — בלי UI — כמו שקורה באפליקציות ובשירותים אמיתיים.

המטרה פשוטה ומעשית: להריץ את **אותה** קריאת API פעם מול מודל מקומי (Ollama על המחשב שלכם) ופעם מול שירות ענן (OpenRouter), ולהבין שרוב הכלים מדברים בפורמט **OpenAI-compatible**. מחליפים בעיקר כתובת, מפתח ושם מודל — לא כותבים ספרייה חדשה לכל ספק.

בסוף תוכלו להדביק סקריפט קצר, לקבל תשובה מהמודל, ולדבג כשלים נפוצים (שירות כבוי, מודל חסר, מפתח שגוי). זה הבסיס לכל agent/runtime שקורא למודל מאחורי הקלעים.

## ‏מפת קבצים — על מה להסתכל

| קובץ | תפקיד |
|---|---|
| ‏<code dir="ltr">chat_llm.py</code> | הסקריפט הראשי — קריאת API |
| ‏<code dir="ltr">.env.example</code> | תבנית משתנים (להעתיק ל-`.env`) |
| ‏<code dir="ltr">.env</code> | סודות מקומיים — **לא בגיט** |
| ‏<code dir="ltr">requirements.txt</code> | `openai`, `httpx` |

**בתוך `chat_llm.py`:**

| חלק | מה עושה |
|---|---|
| ‏`load_dotenv` | טוען `.env` ל-environment (בלי לדרוס `export` קיים) |
| ‏`client_for` | בוחר URL / key / model לפי `--backend` |
| ‏`main` | בונה `messages`, קורא ל-`chat.completions.create`, מדפיס תשובה |

אין קובץ JSON של נתונים עסקיים — ההודעות נבנות בזיכרון מארגומנטי CLI.

## ‏איך מייצרים OPENROUTER_API_KEY (מפתח ה-API)

1. היכנסו ל-<code dir="ltr">https://openrouter.ai</code> והירשמו.  
2. **Keys** → **Create API Key** (או "Get API Key").  
3. העתיקו מפתח שמתחיל ב-`sk-or-v1-…`.  
4. שימו ב-`.env`:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

או:

```bash
export OPENROUTER_API_KEY='sk-or-v1-...'
```

> בדוגמאות כלליות לפעמים קוראים למשתנה `LLM_API_KEY`. אצלנו השם המפורש הוא **`OPENROUTER_API_KEY`**.  
> Ollama מקומי לא דורש מפתח אמיתי.

## ‏התקנה — מה כל פקודה עושה

```bash
cd labs/09-llm-api
python3 -m venv .venv          # יוצר סביבת Python מבודדת בתיקייה
source .venv/bin/activate        # מפעיל אותה בטרמינל הנוכחי
pip install -r requirements.txt  # מתקין את הספריות מהקובץ
cp .env.example .env             # מעתיק תבנית → עורכים סודות כאן
```

## ‏מסלול A — Ollama (מקומי)

```bash
# התקינו Ollama מ-https://ollama.com והפעילו את האפליקציה

ollama pull qwen3.5:4b   # מוריד מודל קל לדיסק
ollama list                # מוודא שהמודל שם
curl -s http://localhost:11434   # בדיקת חיים לשרת המקומי

python3 chat_llm.py --backend ollama \
  --message "Hi — who are you? One sentence."
# --backend ollama  → client_for בוחר localhost:11434
# --message         → תוכן role=user
```

עם הוראת מערכת:

```bash
python3 chat_llm.py --backend ollama \
  --system "Answer only in Hebrew." \
  --message "What is an API?"
```

## ‏מסלול B — OpenRouter (ענן)

1. צרו `OPENROUTER_API_KEY` (סעיף למעלה) ומלאו ב-`.env`.  
2. הריצו:

```bash
python3 chat_llm.py --backend openrouter \
  --message "Hi — who are you? One sentence."
```

## ‏ארגומנטי CLI

| ארגומנט | משמעות |
|---|---|
| ‏`--backend ollama\|openrouter` | לאן מתחברים |
| ‏`--message "..."` | שאלת המשתמש |
| ‏`--system "..."` | הוראת system (אופציונלי) |
| ‏`--debug` | מדפיס base_url, model, key_set, usage, traceback |

## ‏דיבוג לפרויקט

| כשל | מה להריץ |
|---|---|
| Ollama לא עונה | <code dir="ltr">curl -s http://localhost:11434</code> · פתחו את אפליקציית Ollama |
| מודל חסר | <code dir="ltr">ollama pull qwen3.5:4b</code> · בדקו `OLLAMA_MODEL` ב-`.env` |
| OpenRouter 401 | בדקו `OPENROUTER_API_KEY` ב-`.env` / `export` |
| שגיאת API כללית | <code dir="ltr">python3 chat_llm.py --backend ollama --debug --message ping</code> |

## ‏מה לבדוק

- ‏[ ] קראתם את `chat_llm.py` (במיוחד `client_for`)  
- ‏[ ] יש `.env` מ-`.env.example`  
- ‏[ ] Ollama עונה מקומית  
- ‏[ ] נוצר מפתח OpenRouter ויש תשובה מ-`--backend openrouter`  
- ‏[ ] `--debug` מציג חיבור/שגיאה ברורה בכשל  

</div>
