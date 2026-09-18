# Lab 02 — Agent Loop חי (Claude Code + AWS)

תרגיל הקלטה למפגש 2. **עלות צפויה:** סנטים בודדים (קריאות `sts` / `cloudwatch` בלבד; אין יצירת משאבים).

## מטרה

לבנות/להריץ לולאת Planning → Execute → Observe → Re-plan מול AWS **בקריאה בלבד**, ולהדגים שהתוכנית משתנה אחרי Observation.

## דרישות

- AWS CLI / credentials עם הרשאות מינימליות: `sts:GetCallerIdentity`, `cloudwatch:GetMetricData` (או `ListMetrics`)
- Python 3.10+ · `pip install boto3`
- אופציונלי בהקלטה: Claude Code על הלאפטופ לבניית/שינוי הסקריפט בלייב

## הרצה

```bash
cd labs/02-aws-agent-loop
export AWS_PROFILE=nashpazformatan
export AWS_REGION=eu-north-1
python3 agent_loop.py
```

הסקריפט גם מגדיר כברירת מחדל `AWS_PROFILE=nashpazformatan` ו־`eu-north-1` אם לא הוגדר אחרת.

## מה להראות בהקלטה (~15–20 דק׳)

1. מטרה על המסך (שקופית Lab במצגת הסטודנטים)
2. הרצת `agent_loop.py` — Plan ראשוני
3. Observation מ־STS / CloudWatch
4. Re-plan מקומי כשהמדדים ריקים / חלקיים
5. עצירה עם Stop condition + סיכום Evidence

## ניקוי

אין משאבים ליצור — אין מה למחוק. אל תריצו Tools שכותבים ל־Production.
