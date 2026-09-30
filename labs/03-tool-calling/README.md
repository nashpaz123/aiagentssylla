<div dir="rtl" lang="he">

# ‏Lab 03 — Tool Calling Host (Function Calling)

תרגיל הקלטה למפגש 3. **עלות צפויה:** סנטים בודדים (קריאות AWS read-only בלבד).

## ‏מטרה

להדגים פרוטוקול Function Calling: Schema → tool_calls → Validate → Execute → Observation, כולל Parallel ודחיית Args לא חוקיים.

## ‏דרישות

- Python 3.10+
- `pip install boto3` (לכלים מול AWS; יש גם כלים מקומיים בלי רשת)
- AWS (אופציונלי להרצה המלאה): `sts:GetCallerIdentity` · `ec2:DescribeInstances`
- פרופיל מומלץ: `nashpazformatan` · אזור: `eu-north-1`

## ‏הרצה

```bash
cd labs/03-tool-calling
export AWS_PROFILE=nashpazformatan
export AWS_REGION=eu-north-1
python3 host_loop.py
```

## ‏מה להראות בהקלטה (~15–20 דק׳)

1. Catalog / Schemas בקובץ `tools_registry.py`
2. המודל המדומה (`scripted_model.py`) מחזיר `tool_calls` — לא מריץ
3. Validate נכשל פעם אחת (enum שגוי) → Observation `ok:false`
4. Parallel: שני כלי-קריאה בבת אחת עם `tool_call_id`
5. סיכום Host + Stop

## ‏ניקוי

אין יצירת משאבים — אין מה למחוק.

## ‏המשך: MCP + PinchTab (headed)

אחרי ה-Host המקומי — הדגמת MCP חיה עם דפדפן גלוי: [`../03-pinchtab-mcp/`](../03-pinchtab-mcp/).

</div>
