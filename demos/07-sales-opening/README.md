<div dir="rtl" lang="he">

# ‏הדגמת פתיחה — מפגש 7: Sales Ops Agent

**משך:** ~8–12 דקות. **Claude Code** או **Cursor** (נדרש חיבור למודל / מנוי).

מטרה: סוכן מכירות קורא CRM + מדיניות מחיר, כותב הצעת מחיר, ומנתב:
**5% → auto** · **18% → HITL מנהל** · **בלי מייל → blocked**.

## ‏מאיפה מגיעים 5% ו-18%?

| מה | קובץ | שדה / סעיף |
|---|---|---|
| הנחה שמבקשים (SMB / Enterprise) | `crm/leads.json` (או `crm/leads.seed.json`) | `requested_discount_pct` — כרגע **5** ב-`L-SMB`, **18** ב-`L-ENT` |
| מתי זה auto / HITL / blocked | `policy.md` | Discount & approval — ≤10% / ≤25% / >25% |
| מחיר ליחידה | `policy.md` | Pricing (list) |

‏`./run-claude.sh smb` רק מפעיל את הסוכן על ליד `L-SMB` — **הוא לא מקבע את האחוז**.  
לשנות תרחיש: ערכו את `requested_discount_pct`, ואם צריך התחלה נקייה — עדכנו גם את ה-seed ואז `./run-claude.sh reset`.

## ‏א׳ — Claude Code (מומלץ להקלטה)

```bash
cd demos/07-sales-opening
# אופציונלי לפני ריצה: grep requested_discount_pct crm/leads.json
./run-claude.sh reset
./run-claude.sh smb           # קורא L-SMB (5%) → auto לפי policy
./run-claude.sh enterprise    # קורא L-ENT (18%) → hitl (שומר L-SMB)
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

1. לפני הריצה: "5 ו-18 חיים ב-`requested_discount_pct` ב-CRM; הספים 10/25 ב-`policy.md`."
2. אחרי SMB: "5 ≤ 10 → auto. המספרים מה-pricebook + מדיניות — לא מהמודל."
3. אחרי Enterprise: "18 > 10 → HITL. אותו סוכן, קלט הנחה אחר מה-CRM."
4. אחרי NOMAIL: "חסר שדה עסקי קריטי → חסימה, לא המצאה."
5. `out/email_draft.md` = טיוטה בלבד; שליחה = פעולה מסוכנת נפרדת.

</div>
