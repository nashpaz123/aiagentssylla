<div dir="rtl" lang="he">

# ‏הדגמת פתיחה — מפגש 8: Surfaces (HTML + Telegram)

**משך:** ~8–12 דקות. **Claude Code** או **Cursor** + שליחה לטלגרם שלך.

מטרה: אותו Quote →  
1. `out/briefing.html` בדפדפן  
2. הודעה **שנשלחת** לטלגרם (`./send-telegram.sh`)

## ‏הכנה חד־פעמית

```bash
cd demos/08-surface-opening
cp .env.example .env
# מלאו TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID (הצ׳אט שלכם)
```

## ‏א׳ — Claude Code + שליחה

```bash
./run-claude.sh reset
./run-claude.sh smb           # כותב HTML + telegram.txt
./send-telegram.sh            # שולח את out/telegram.txt אליכם
# פתחו out/briefing.html בדפדפן — ובדקו את הטלפון

./run-claude.sh enterprise
./send-telegram.sh
```

## ‏ב׳ — Cursor

הדביקו שלבים מ-`prompt-cursor.md`, ואז `./send-telegram.sh`.

## ‏מה להגיד על המסך

1. "המשתמש רואה כרטיס — והתראה מגיעה לנייד."  
2. SMB מול ENT: אותו pipeline, מסר וצבע שונים.  
3. זה צ׳אט **פנימי** (המרצה/AE) — לא מייל ללקוח הסופי.

</div>
