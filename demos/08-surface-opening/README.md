<div dir="rtl" lang="he">

# ‏הדגמת פתיחה — מפגש 8: Surfaces (HTML + Telegram text)

**משך:** ~8–12 דקות. **Claude Code** או **Cursor**.

מטרה: אותו Quote → שני משטחי פלט יפים:
1. `out/briefing.html` — כרטיס בדפדפן  
2. `out/telegram.txt` — הודעה מוכנה לטלגרם (בלי שליחה בדמו)

השליחה האמיתית לטלגרם — ב-Lab עם `TELEGRAM_BOT_TOKEN`.

## ‏א׳ — Claude Code

```bash
cd demos/08-surface-opening
./run-claude.sh reset
./run-claude.sh smb           # L-SMB / auto → כרטיס ירוק
# פתחו את out/briefing.html בדפדפן
./run-claude.sh enterprise    # L-ENT / hitl → כרטיס ענבר
cat out/telegram.txt
```

## ‏ב׳ — Cursor

הדביקו שלבים מ-`prompt-cursor.md`.

## ‏מה להגיד על המסך

1. "המודל לא 'מדבר יפה' בטרמינל — הוא כותב משטח שהמשתמש רואה."
2. SMB מול ENT: אותו pipeline, עיצוב/מסר שונים לפי route.
3. `telegram.txt` ≠ שליחה; השליחה דורשת bot token ב-Lab.

</div>
