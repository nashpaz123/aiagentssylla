<div dir="rtl" lang="he" style="direction: rtl; text-align: right; unicode-bidi: embed;">

# ‏Lab 09 — שיחה עם LLM ב-Python (Ollama · OpenRouter)

אותו קוד OpenAI-compatible — מחליפים רק `base_url` / מפתח / שם מודל.

## ‏התקנה

```bash
cd labs/09-llm-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## ‏מסלול A — Ollama (מקומי)

1. התקינו [Ollama](https://ollama.com/) והריצו את האפליקציה.  
2. משכו מודל קל והריצו:

```bash
ollama pull qwen3.5:4b
ollama run qwen3.5:4b
```

3. בטרמינל אחר:

```bash
python3 chat_llm.py --backend ollama --message "Hi — who are you? One sentence."
```

## ‏מסלול B — OpenRouter (ענן)

1. צרו מפתח ב-[OpenRouter](https://openrouter.ai/) שימו ב-`.env` כ-`OPENROUTER_API_KEY`.  
2. הריצו:

```bash
python3 chat_llm.py --backend openrouter --message "Hi — who are you? One sentence."
```

## ‏מה לבדוק

- ‏[ ] Ollama עונה מקומית  
- ‏[ ] OpenRouter עונה בענן (בדרך כלל מהר יותר)  
- ‏[ ] הבנתם שרק 3 משתנים מחליפים backend  

</div>
