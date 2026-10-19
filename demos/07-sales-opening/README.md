<div dir="rtl" lang="he">

# ‏הדגמת פתיחה — מפגש 7: Sales Ops Agent

**משך:** ~8–12 דקות. **Claude Code** או **Cursor** (נדרש חיבור למודל / מנוי).

מטרה: סוכן מכירות קורא CRM + מדיניות מחיר, כותב הצעת מחיר, ומנתב:
**5% → auto** · **18% → HITL מנהל** · **בלי מייל → blocked**.

## ‏א׳ — Claude Code (מומלץ להקלטה)

```bash
cd demos/07-sales-opening
./run-claude.sh reset
./run-claude.sh smb           # L-SMB / 5% → auto + email draft
./run-claude.sh enterprise    # L-ENT / 18% → pending_manager (שומר L-SMB)
./run-claude.sh nomail        # L-NOMAIL → need_email
cat out/quotes.json
```

אינטראקטיבי:

```bash
claude --setting-sources project,local
/agents   # אמור להציג sales
# הדביקו prompt-smb.md → prompt-enterprise.md → prompt-nomail.md
```

## ‏ב׳ — Cursor

הדביקו שלבים מ-`prompt-cursor.md`.

## ‏מה להגיד על המסך

1. אחרי SMB: "המספרים מה-pricebook + מדיניות — לא מהמודל."
2. אחרי Enterprise: "אותו סוכן, הנחה אחרת → שער כסף (HITL)."
3. אחרי NOMAIL: "חסר שדה עסקי קריטי → חסימה, לא המצאה."
4. `out/email_draft.md` = טיוטה בלבד; שליחה = פעולה מסוכנת נפרדת.

</div>
