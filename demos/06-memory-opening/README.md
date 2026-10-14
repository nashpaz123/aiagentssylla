<div dir="rtl" lang="he">

# ‏הדגמת פתיחה — מפגש 6: Checkpoint ≠ Memory

**משך:** ~5–8 דקות. **מומלץ: Claude Code (או Cursor).** חלופה בלי מפתח: `memory_opening.py`.

מטרה: תור סטטוס בלי Store מתחיל מאפס; עם `out/store.json` הסוכן זוכר — כולל **99→auto** מול **101→hitl**.

## ‏א׳ — Claude Code (מומלץ להקלטה)

```bash
cd demos/06-memory-opening
./run-claude.sh reset
./run-claude.sh turn1          # C-99 / 99 → כותב out/store.json (auto)
./run-claude.sh status         # קורא מה-Store — חייב לזכור
./run-claude.sh turn1-101      # C-101 / 101 → hitl (לא מוחק את C-99)
cat out/store.json
```

אינטראקטיבי (רואים subagent בזמן אמת):

```bash
cd demos/06-memory-opening
claude --setting-sources project,local
/agents                        # אמור להציג support
# הדביקו את prompt-turn1.md, אחר כך prompt-status.md, אחר כך prompt-turn1-101.md
```

## ‏ב׳ — Cursor

פתחו את התיקייה ב-Cursor, צ׳אט Agent, והדביקו שלבים מ-`prompt-cursor.md` (Turn A → B → C).

## ‏ג׳ — חלופה בלי API (פייתון דטרמיניסטי)

```bash
python3 memory_opening.py --mode none --amount 99
python3 memory_opening.py --reset
python3 memory_opening.py --mode store --customer C-99 --amount 99
python3 memory_opening.py --mode store --customer C-99 --status
python3 memory_opening.py --mode store --customer C-101 --amount 101
```

## ‏מה להגיד על המסך

1. אחרי `turn1`: "נשמר לקובץ — זה Memory/Store, לא Checkpoint של שיחה."
2. אחרי `status`: "המודל *חייב* לקרוא את הקובץ; בלי קובץ — אין זיכרון."
3. אחרי `turn1-101`: "אותו סוכן, קלט אחר → hitl."
4. אופציונלי: מחקו את C-99 מה-Store והריצו `status` שוב — אמנזיה מכוונת.

</div>
