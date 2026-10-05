<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 3 — Tool Use ו-Function Calling
## ‏קובץ מרצה (תסריט מלא להקלטה)

> **משך מיועד:** ~2.5–3 שעות **הקלטה רצופה**  
> **קהל בהקלטה:** אין זמן עבודה לסטודנטים חיים · אין שקט לחשיבה · אין המתנה לתשובות מקהל חי  
> **תרגילים/הדגמות:** המרצה מקריא פתרון מלא · אין זמן פתרון עצמאי של צופים  
> **מצגת סטודנטים:** [`03-students-slides.md`](03-students-slides.md)  
> **Lab:** [`labs/03-tool-calling/`](labs/03-tool-calling/) · PinchTab MCP: [`labs/03-pinchtab-mcp/`](labs/03-pinchtab-mcp/) · פרופיל AWS `nashpazformatan` · `eu-north-1`

> מספור המרצה = מספור הסטודנטים (1…48). לא מפרטים שוב את מפגש 2 לעומק.

---

# ‏הנחיות למרצה (הקלטה)

- מקריאים את בלוק **להקראה** במלואו; מותר להרחיב אבל לא לקצר את הפירוט על הדוגמאות.
- ‏**`[סטודנטים · N]`** — גללו למספר N לפני ההקראה.
- **אין** סימוני המתנה לקהל. שאלות רטוריות נענות מיד בקול המרצה.
- ‏**`[Lab חי]`** — מסוף לפי `labs/03-tool-calling/`.
- כל בלוק קוד אצל המרצה מופיע גם אצל הסטודנטים באותו מספר.

---

# ‏חלק א׳ — פתיחה

## ‏1 — כותרת

‏[סטודנטים · 1]

**על המסך:**

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="360" />
</p>

**Tool Use ו-Function Calling**  
איך Agent נוגע בעולם

![Augmented LLM: Retrieval · Tools · Memory](assets/03/01-tool-calling-loop.png)

**להקראה:**

ברוכים הבאים למפגש השלישי בקורס AI Agents ומערכות אוטונומיות.

על המסך הכותרת: Tool Use ו-Function Calling — איך Agent נוגע בעולם. הלוגו של SPRINT Tech Academy, והדיאגרמה שמחברת LLM, Host, ו-Tool.

במפגש הקודם למדנו איך בונים תוכנית, איך רצים בלולאה סגורה, ואיך שמים Budget ו-Stop. היום לא חוזרים על זה בפירוט. היום יורדים לרזולוציה של הפעולה עצמה: מהו Tool, איך המודל מבקש אותו, ומי באמת מריץ אותו.

הדיאגרמה על המסך היא החוזה של היום. המודל מציע קריאה. ה-Host מאמת ומריץ. הכלי נוגע בעולם. Observation חוזר למודל. אם מישהו מבלבל בין שלושת התיבות האלה — מקבלים מערכת מסוכנת או מערכת שלא עובדת.

המטרה של המפגש היא מבצעית: לצאת עם יכולת לכתוב Schema, להסביר את הפרוטוקול, לתכנן Validate ו-Policy, ולהריץ Lab חי שבו אתם רואים tool_calls והרצה אמיתית ב-Host.

עוד מילה על הסדר בקורס. מפגש 1 נתן שפה. מפגש 2 נתן מנוע תכנון וביצוע. מפגש 3 נותן את הידיים שנוגעות במערכות. בלי הידיים האלה Agent נשאר מצגת.

אם תראו בהמשך הקורס Graphs ו-Multi-Agent — כולם יושבים על אותו חוזה Tool. לכן כדאי להישאר מדויקים היום במושגים.

במפגש 2 דיברנו על Goal → Plan → Actions → Result. היום Actions מתפרקים ל-tool_calls, ו-Result מתפרק ל-Observations מובנים. אם Observation לא חוזר למודל או ל-State — אין לולאה, יש קריאת API חד־פעמית.

דוגמה לפתיחה מהשטח: צוות חיבר GPT ל-Jira בלי Schema ברור. המודל יצר טיקטים עם שדות חסרים. אחרי Schema עם enum ל-priority ועם required ל-project_key — מספר הטיקטים השבורים צנח. זה המפגש הזה במשפט.

---

## ‏2 — מה היום (+ חזרה קצרה על מפגש 2)

‏[סטודנטים · 2]

**על המסך:**

| נבנה היום | מפגש 2 (בקצרה) |
|---|---|
| חוזה Tool · Schema · Protocol | Planning / Decomposition |
| tool_choice · Parallel · Validate | Closed Loop · ReAct · P&E |
| Catalog · Policy · MCP + PinchTab | Budget · Stop · Policy Gate |
|‏ Lab: Host + PinchTab headed | Lab לולאת Plan→Observe |

**להקראה:**

שימו לב לטבלה על המסך.

בטור השמאלי — מה שבונים היום: חוזה Tool, Schema, פרוטוקול Function Calling, tool_choice, Parallel, Validate, Catalog, Policy, MCP עם דוגמת PinchTab, ו-Lab של Host שמריץ Tools לפי Schema — כולל הדגמת headed browser.

בטור הימני — מה שלא נפרט שוב: Planning, Decomposition, Closed Loop, ReAct, Plan-and-Execute, Budget ו-Stop ברמת העומק של מפגש 2. אם משהו משם חסר — חזרו למפגש 2. היום אנחנו מתקדמים כדי להספיק עומק על Tools.

הסיבה חשובה: בלי Planning יש בלגן. אבל בלי Tool Use נכון — גם Planning מושלם לא נוגע בעולם בבטחה. ממפגש 3 והלאה נניח שיש לכם לולאת ביצוע; השאלה היא איך מחברים אליה כלים אמיתיים.

שימו לב גם מה לא מופיע בטור השמאלי: אנחנו לא בונים היום LangGraph, לא CrewAI, ולא Memory מלא. אלה מפגשים 4, 5 ו-6. אם תקפצו לשם בלי Tool Use — תבנו Graphs יפים על חוזה כלים שבור.

חזרה קצרה מאוד על מפגש 2 במילה אחת לכל מושג: Hypothesis Plan, Closed Loop, Validation משולשת, Budget, Policy Gate. מעכשיו כל אחד מהם יופיע כהקשר לכלי, לא כשיעור חדש.

אם אתם באים ממפגש 2 עם Lab של agent_loop — שימו לב להבדל: שם Re-plan היה הגיבור. כאן הגיבור הוא החוזה של כל צעד Execute.

---

## ‏3 — שאלת המפגש + תוצרים

‏[סטודנטים · 3]

**על המסך:**

> המודל רוצה לפעול — מי מריץ, עם איזה חוזה, ואיך לא נשברים?

בסוף המפגש תדעו:
1. לכתוב Tool Schema שעובד (ולזהות Schema גרוע)  
2. להסביר את פרוטוקול Function Calling מקצה לקצה  
3. לתכנן Validate · Errors · Parallel · tool_choice  
4. להריץ Host חי שמאמת ומריץ Tools

**להקראה:**

השאלה שתלווה את כל המפגש כתובה על המסך:

המודל רוצה לפעול — מי מריץ, עם איזה חוזה, ואיך לא נשברים?

זו שאלת ארכיטקטורה, לא שאלת פרומפט. כי ברגע שיש LLM עם כלים, קל לתת לו גישה ל-API ולקוות לטוב. בפועל בלי Schema טוב, בלי Validate, ובלי הפרדה בין הצעה לביצוע — מקבלים הזיות פרמטרים, קריאות מסוכנות, ולוגים שאי אפשר לדבג.

ארבעת התוצרים בסוף המפגש:

ראשית — לכתוב Tool Schema שעובד, ולזהות Schema גרוע ממרחק.

שנית — להסביר את פרוטוקול Function Calling מקצה לקצה, כולל tool_call_id.

שלישית — לתכנן Validate, Errors, Parallel, ו-tool_choice.

רביעית — להריץ Host חי שמאמת ומריץ Tools.

אם אתם זוכרים רק את ארבע הנקודות האלה — המפגש הצליח.

בואו נהפוך את ארבעת התוצרים לשאלות בדיקה עצמית.

האם אני יכול לכתוב Schema לכלי מהעבודה שלי בלי להשתמש במילה do_stuff?

האם אני יכול לצייר על נייר את חמשת שלבי הפרוטוקול בלי להסתכל?

האם אני יודע מתי Parallel אסור?

האם ראיתי Host שמחזיר SCHEMA error במקום לקרוס?

ארבע תשובות חיוביות — המפגש עשה את שלו.

תוצר מעשי נוסף שלא כתוב במפורש אבל יוצא מהמפגש: אוצר מילים משותף לשיחה עם מפתחים — tool_call, Observation, parallel_safe, policy deny.

---

# ‏חלק ב׳ — מהו Tool

## ‏4 — Tool = חוזה מול העולם

‏[סטודנטים · 4]

**על המסך:**

**הגדרה:** Tool — פעולה מוגדרת שהקוד יכול לבצע; המודל רק **מציע** אותה.

```text
GOAL → (LLM) tool_call → (HOST) execute → OBSERVE → …
```

בלי Tool: המודל מדבר.  
עם Tool: המערכת יכולה **לשנות או לקרוא** מציאות.

**להקראה:**

הגדרה על המסך: Tool הוא פעולה מוגדרת שהקוד יכול לבצע; המודל רק מציע אותה.

השרשרת: Goal נכנס למודל. המודל מחזיר tool_call. ה-Host מריץ. Observation חוזר. וחוזר חלילה.

בלי Tool — המודל מדבר. הוא יכול להיות מבריק, אבל הוא לא קורא DB ולא משנה מערכת.

עם Tool — המערכת יכולה לקרוא או לשנות מציאות. ולכן כל Tool הוא גם סיכון וגם הזדמנות.

חשוב לדייק בשפה: אנשים אומרים ״המודל קרא ל-API״. זה קיצור מסוכן. המודל ביקש. הקוד שלכם קרא. האחריות על הביצוע היא של ה-Host, לא של ספק המודל.

נחזור לשרשרת עם דוגמת ענן. Goal: מה ה-CPU של האינסטנס. Plan ממפגש 2 אמר cloudwatch_sample. היום נפרק איך נראית הקריאה עצמה כ-tool_call עם Schema, ואיך Validate מוודא שיש InstanceId לפני GetMetricData.

יש בלבול נפוץ בין Tool לבין Skill של מוצר. Tool בארכיטקטורה הוא חוזה טכני: name, schema, handler. Skill בשיווק הוא יכולת עסקית. אנחנו מדברים היום על החוזה הטכני.

עוד בלבול: Function Calling ו-Tool Use הם אותו רעיון משפחתי. שמות שונים אצל ספקים. הרעיון: המודל בוחר פונקציה מוצהרת וממלא ארגומנטים.

כשהמוצר אומר ״יש לנו Agent שמדבר עם Salesforce״ — תרגמו מיד: אילו Tools, מי ה-Host, מה ה-Validate.

---

## ‏5 — Act בלי Tool מול Act עם Tool

‏[סטודנטים · 5]

**על המסך:**

| בלי Tool | עם Tool |
|---|---|
| טקסט / המלצה | קריאה ל-API / DB / CLI |
| אין תופעת לוואי אמיתית | יש Observation אמיתי |
| קשה לבדוק | אפשר Validate + Trace |

דוגמה: *״מה סטטוס הזמנה 9912?״*  
בלי Tool → ניחוש. עם Tool → `get_order(order_id=9912)`.

**להקראה:**

הטבלה משווה Act בלי Tool מול Act עם Tool.

בלי Tool יש טקסט והמלצה. אין תופעת לוואי אמיתית. קשה לבדוק האם ״המערכת עשתה משהו״ — כי היא לא עשתה.

עם Tool יש קריאה ל-API או DB או CLI. יש Observation אמיתי. אפשר Validate. אפשר Trace.

הדוגמה הקצרה: הלקוח שואל מה סטטוס הזמנה 9912. בלי Tool המודל עלול לנחש או להמציא. עם Tool יש get_order עם order_id. אם ההזמנה לא קיימת — Observation אומר NOT_FOUND, לא סיפור יפה.

זה גם החיבור למפגש 2: Tool success הוא לא Goal success. get_order יכול להחזיר 200, ועדיין לא עניתם על שאלת הלקוח אם לא סיכמתם נכון.

דוגמת DevOps במקביל לדוגמת ההזמנה. שאלה: כמה pods ב-CrashLoop. בלי Tool — ניחוש. עם Tool — get_pods עם namespace ו-label selector. Observation מחזיר רשימה. אחר כך get_logs על pod ספציפי.

שימו לב לסדר: לפעמים צריך Sequential כי ה-pod name מגיע מהתצפית הראשונה. זה יחזור בחלק Parallel.

עוד דוגמה: תרגום מסמך. בלי Tool זה טקסט. עם Tool translate(text, target_lang) יש מדידה, עלות, ולוג. אותו הבדל בדיוק.

---

## ‏6 — ארבעת חלקי כלי טוב

‏[סטודנטים · 6]

**על המסך:**

| חלק | תפקיד |
|---|---|
| **Name** | מזהה יציב לקוד |
| **Description** | Prompt לבחירה (מתי להשתמש / מתי לא) |
| **Schema** | פרמטרים typed + required/enum |
| **Side-effects** | read / write / money / delete — ל-Policy |

**להקראה:**

ארבעה חלקים לכל כלי טוב.

ה-Name — מזהה יציב לקוד. לא שירה. לא do_stuff. שם שתוכלו לחפש בלוגים.

ה-Description — זה ה-Prompt של הכלי. המודל בוחר לפי הטקסט הזה. כתבו מתי להשתמש ומתי לא.

ה-Schema — פרמטרים עם טיפוסים, required, ו-enum איפה שאפשר.

ה-Side-effects — האם זה read, write, money, או delete. זה מה שמזין Policy Gate.

אם אחד מארבעת החלקים חלש — הכלי ״עובד בדמו״ ונכשל בפרוד. במיוחד Description עמום ו-Schema רחב מדי.

‏Side-effects הם לא הערת שוליים בתיעוד. הם שדה החלטה. צוות טוב מסמן לכל כלי: read / write / money / delete / external-comms. אחר כך Policy Gate קורא את הסימון.

‏Name צריך להיות יציב לאורך גרסאות. אם שיניתם התנהגות דרמטית — שנו שם או גרסה ב-description, אחרת Trace ישן משקר.

‏Side-effect external-comms חשוב: שליחת מייל או הודעה ללקוח. גם בלי כסף וגם בלי delete — זה בלתי הפיך חברתית. לרוב HITL או תבניות מאושרות.

---

# ‏חלק ג׳ — פרוטוקול Function Calling

## ‏7 — חמשת השלבים

‏[סטודנטים · 7]

**על המסך:**

![Function Calling Loop](assets/03/02-protocol-steps.png)

1. שולחים schemas + מטרה  
2. המודל מחזיר `tool_calls` (לא תשובה סופית)  
3. **ה-Host** מריץ (לא המודל)  
4. מחזירים תוצאות עם `tool_call_id`  
5. המודל ממשיך או עונה

**להקראה:**

על המסך חמשת השלבים של הפרוטוקול.

אחד: שולחים למודל את רשימת ה-Schemas ואת מטרת המשתמש.

שניים: המודל מחזיר tool_calls. שימו לב — זו עדיין לא תשובה סופית למשתמש.

שלוש: ה-Host מריץ. לא המודל. לא הספק. הקוד שלכם.

ארבע: מחזירים תוצאות עם tool_call_id כדי שהמודל יידע מה שייך למה.

חמש: המודל ממשיך עם עוד קריאות, או עונה סופית.

אם אתם זוכרים רק משפט אחד מהמפגש: Model proposes, Code executes, Observation returns.

בספקים השונים תראו שמות שדות שונים: input_schema מול parameters, tool_use מול tool_calls. אל תיתנו לסינטקס להסיח את הדעת. חמשת השלבים זהים.

בהקלטה נראה את זה גם ב-Lab עם מודל מדומה — כדי שלא נהיה תלויים במפתח API כדי ללמד את החוזה.

שלב 2 הוא המקום שבו אנשים טועים בהדגמות: הם מראים תשובת מודל סופית בלי tool_calls. זה Chat. כדי ללמד Agents צריך להראות את הבקשה המבנית באמצע.

שלב 3 הוא המקום שבו אבטחה חיה. אם דילגתם עליו — נתתם למודל להריץ. גם אם טכנית הקוד שלכם רץ, בלי Validate זה עדיין ״המודל מחליט על side effect״.

תרגיל מחשבתי: אם שלב 4 מחזיר תוצאות בלי ids, איך תדבגו Parallel של שלושה get_logs? התשובה: לא תדבגו. לכן שלב 4 הוא לא אסתטיקה.

---

## ‏8 — מי מבצע? המודל מציע, הקוד מריץ

‏[סטודנטים · 8]

**על המסך:**

```text
LLM  →  { name, arguments, id }
Host →  validate → handler(args) → result
Host →  { role: tool, tool_call_id, content }
LLM  →  answer | more tool_calls
```

כלל ברזל: **אין ביצוע בתוך המודל.**  
אם יש תופעת לוואי — היא רק אחרי Validate ב-Host.

**להקראה:**

הפסאודוקוד על המסך מפרק את האחריות.

ה-LLM מחזיר name, arguments, ו-id.

ה-Host עושה validate, קורא ל-handler, ומקבל result.

ה-Host מחזיר הודעת tool עם tool_call_id.

ה-LLM עונה או מבקש עוד כלים.

כלל הברזל: אין ביצוע בתוך המודל. אם יש תופעת לוואי — היא רק אחרי Validate ב-Host. זה נשמע בסיסי, אבל רוב התקריות עם Agents מתחילות כשמישהו נותן למודל ״להריץ״ בלי שכבת בקרה.

נפרק את validate לדוגמה מספרית. arguments הגיעו כמחרוזת JSON. Parse נכשל → Observation parse_error. Parse הצליח אבל minutes="many" → SCHEMA. Schema עבר אבל הכלי delete_customer → Policy deny / HITL. רק אם הכול עבר — handler.

הסדר הזה חוסך תקריות. אל תחליפו אותו ב-try/except כללי בלי קודים.

במערכות אמיתיות handler לעיתים עוטף SDK. ה-Validate שלכם עדיין לפני ה-SDK. אל תסמכו על ה-SDK שיברור args הזויים בנימוס.

---

## ‏9 — תפקידי הודעות (Message Roles)

‏[סטודנטים · 9]

**על המסך:**

|‏ Role | מה יש בפנים |
|---|---|
|‏ `user` | מטרה / הקשר |
|‏ `assistant` | טקסט ו/או `tool_calls[]` |
|‏ `tool` | תוצאת כלי + `tool_call_id` |
| (שוב) `assistant` | תשובה או קריאות נוספות |

ספקים שונים (OpenAI / Anthropic / Gemini) — אותו רעיון, סינטקס שונה.

**להקראה:**

תפקידי ההודעות.

תפקיד user — המטרה וההקשר.

תפקיד assistant — טקסט ו/או מערך tool_calls.

תפקיד tool — תוצאת הכלי מחוברת ל-id של הקריאה.

ואז שוב assistant — תשובה או קריאות נוספות.

ספקים שונים משתמשים בשמות שונים קצת: OpenAI, Anthropic, Gemini. הרעיון זהה. אל תתעסקו היום בסינטקס של ספק אחד כאילו הוא האמת היחידה. תתמקדו בחוזה.

בהודעת assistant יכולים להיות גם טקסט וגם tool_calls יחד. הטקסט לעיתים מסביר כוונה; אל תסמכו עליו כ-Evidence. Evidence מגיע מ-Observation.

כשמסכמים למשתמש אחרי כלים — העדיפו tool_choice none כדי שלא ימשיך לקרוא סתם.

‏Anthropic שם tool_result בתוך הודעת user. OpenAI משתמש ב-role tool. כשתקראו דוקס — חפשו את הרעיון, לא את שם השדה בלבד.

---

## ‏10 — למה `tool_call_id` חובה

‏[סטודנטים · 10]

**על המסך:**

- ב-Parallel: כמה תוצאות בבת אחת  
- המודל חייב להתאים תוצאה לקריאה  
- ל-Trace ו-Debug: מי ביקש מה ומתי  

בלי id → בלבול בין תוצאות, במיוחד ב-Parallel.

**להקראה:**

למה tool_call_id חובה.

כי ב-Parallel חוזרות כמה תוצאות בבת אחת. בלי id המודל לא יודע איזו תוצאה שייכת לאיזו בקשה.

כי ב-Trace אתם רוצים לדעת מי ביקש מה ומתי.

כי ב-Debug של לולאה תקועה, id הוא העוגן.

בלי id — במיוחד תחת Parallel — אתם בונים מערכת שמבולבלת בהצלחה שברירית.

שמרו לוגים מובנים עם השדות: run_id, turn, tool_call_id, tool_name, ok, latency_ms, policy_decision. בלי זה Multi-Agent ו-Graphs במפגשים הבאים יהיו קופסה שחורה.

אם ספק לא נותן id — צרו id ב-Host לפני ההרצה ושמרו מיפוי. אל תזרקו את העוגן.

גם ביטול חלקי נשען על tool_call_id: אם קריאה אחת נכשלה ואחרת הצליחה באותו batch, אתם יודעים מה לשייך ל-retry.

---

# ‏חלק ד׳ — Schema Design

## ‏11 — JSON Schema לפרמטרים

‏[סטודנטים · 11]

**על המסך:**

```json
{
  "name": "get_order",
  "description": "Fetch order by id for support. Do NOT use for refunds.",
  "parameters": {
    "type": "object",
    "properties": {
      "order_id": { "type": "string", "description": "Order id, e.g. ORD-9912" },
      "fields": {
        "type": "string",
        "enum": ["status", "total", "items"],
        "description": "Which field to return"
      }
    },
    "required": ["order_id"]
  }
}
```

**להקראה:**

עכשיו Schema לדוגמה על המסך: get_order.

שימו לב לתיאור: Fetch order by id for support. Do NOT use for refunds. זה לא קישוט. זה Prompt שמקטין סיכוי שהמודל ישתמש בכלי הלא נכון.

‏order_id הוא string required. fields הוא enum. זה מצמצם הזיות.

זה הפורמט שתוכלו להעתיק לכל כלי בקורס. Name, Description, Parameters עם properties ו-required.

אפשר להגיד שה-Schema הוא טסט חוזה. אם אי אפשר לכתוב Schema חד — הכלי כנראה עמום מדי. אם Schema ארוך מדי — אולי פיצלתם לא נכון לכמה כלים.

נקרא את ה-Schema שורה־שורה כאילו זה PR.

‏name: get_order — ברור.

‏description: כולל Do NOT use for refunds — מעולה.

‏order_id: string עם דוגמה ORD-9912 — מוריד הזיות פורמט.

‏fields: enum — מצמצם פלט וטוקנים.

‏required רק order_id — fields יכול לקבל default ב-handler.

אם fields לא נשלח — handler יכול להחזיר status כברירת מחדל. תעדו את זה ב-description של fields כ-optional עם default status.

---

## ‏12 — Description = Prompt לכלי

‏[סטודנטים · 12]

**על המסך:**

המודל בוחר כלים לפי **טקסט התיאור**, לא לפי שם הקובץ בקוד.

כללי זהב:
- מתי להשתמש  
- מתי **לא** להשתמש  
- דוגמת ערך לפרמטר  
- מגבלות (support only / read-only)

**להקראה:**

‏Description הוא Prompt לכלי.

המודל לא קורא את קוד ה-Python שלכם. הוא קורא את הטקסט ששמתם ב-description של הכלי ושל הפרמטרים.

כללי זהב: מתי להשתמש. מתי לא להשתמש. דוגמת ערך. מגבלות כמו support only או read-only.

אם התיאור אומר ״helpful general tool״ — קיבלתם רולטה. אם התיאור אומר ״Use ONLY for order status; never for refunds״ — קיבלתם משמעת.

תיאור פרמטר חשוב לא פחות מתיאור הכלי. אם city בלי דוגמה, תקבלו TLV ו-Tel Aviv ו-תל אביב. אם כתוב ״City name in English, e.g. Tel Aviv״ — השתפרתם.

כשיש שני כלים דומים, התיאורים חייבים להפריד ביניהם במפורש. אחרת המודל יטיל מטבע.

תיאור רע נפוץ: ״Gets data from the system." תיאור טוב: ״Returns shipment tracking for a delivered order. Use after get_order shows status=shipped. Do not use for undelivered orders."

---

## ‏13 — enum · required · defaults

‏[סטודנטים · 13]

**על המסך:**

| טכניקה | למה |
|---|---|
|‏ `enum` | חוסם `"Celsius"` / `"C"` / `"celsius"` |
|‏ `required` | רק מה שבאמת חייב |
|‏ Optional + default בקוד | פחות הזדמנות להזיה |
|‏ `type` מדויק | פחות parse errors |

**להקראה:**

‏enum, required, ו-defaults.

‏enum חוסם וריאציות כתיב. בלי enum תקבלו Celsius ו-C ו-celsius באותו אחר צהריים.

‏required רק למה שבאמת חייב. יותר מדי required מפחיד את המודל לבחור כלי אחר, או ממציא ערכים.

‏Optional עם default בקוד — פחות הזדמנות להזיה.

טיפוס מדויק — פחות parse errors ב-Host.

‏defaults בקוד לא ב-Schema הם לעיתים עדיפים: המודל לא חייב להמציא ערך, וה-handler יודע את ברירת המחדל העסקית.

‏integer עם טווח ב-description זה טוב; עוד יותר טוב — Validate ב-Host על 1..180 גם אם המודל התעלם מהטקסט.

‏enum עם עשרות ערכים יכול להיות כבד בטוקנים. לפעמים עדיף string עם Validate עסקי ודוגמאות. הבחירה היא tradeoff — תעדו אותה.

---

## ‏14 — Schema טוב מול גרוע

‏[סטודנטים · 14]

**על המסך:**

![Schema Good vs Bad](assets/03/03-schema-good-bad.png)

| טוב | גרוע |
|---|---|
|‏ `get_order` + תיאור צר | `do_stuff` + "helpful" |
| `order_id` string required | `data: string` |
|‏ `fields` enum | `options: object` חופשי |

**להקראה:**

הדיאגרמה משווה Schema טוב לגרוע.

טוב: get_order, תיאור צר, order_id required, fields enum.

גרוע: do_stuff, helpful, data string, options object חופשי.

המודל אוהב object חופשי כי קל למלא אותו בזבל מבריק. אתם לא אוהבים את זה בפרוד, כי אין לכם חוזה לבדוק מולו.

סממן לSchema גרוע: properties עם שם data או payload או options בלי מבנה פנימי. סממן לטוב: שמות שדות שמופיעים גם ב-API האמיתי שלכם.

עוד סממן גרוע: description ארוך שמספר סיפור מוצר במקום כללי שימוש. קצר ומדויק מנצח.

בקוד ראינו do_stuff. בפרוד תראו גם run, action, execute, helper. אותה משפחה. שנו שם לפעולה עסקית אחת.

---

## ‏15 — הדגמה: שני Schemas לאותו צורך

‏[סטודנטים · 15]

**על המסך:**

תרחיש: *״הלקוח שואל על הזמנה 9912״*

**גרוע:**
```json
{ "name": "handle", "parameters": { "q": { "type": "string" } } }
```

**טוב:** `get_order` כמו בשקופית 11 + Policy: אין `refund` בלי HITL.

**להקראה:**

אותו צורך בשני Schemas.

התרחיש: הלקוח שואל על הזמנה 9912.

הגרוע: כלי בשם handle עם פרמטר q חופשי. המודל ידחוף לשם את כל השאלה, וה-handler לא יודע מה לעשות בצורה בטוחה.

הטוב: get_order כמו שראינו, ועוד Policy: אין refund בלי HITL.

כשאתם סוקרים Catalog של צוות — חפשו קודם את ה-handle ואת ה-do_stuff. שם מתחיל הכאב.

נראה מה קורה ב-handler של handle(q). מישהו יעשה if "הזמנה" in q ואז regex. זה שביר. Schema טוב דוחף מבנה לפני הקוד העסקי.

‏Policy על refund נפרד מה-Schema של get_order. אל תערבבו: Schema מתאר כלי אחד; Policy מחליטה אם מותר להפעיל כלי אחר.

אחרי שעוברים ל-get_order — כתבו טסט Host: args חסרים נדחים, enum שגוי נדחה, order תקין עובר. Schema בלי טסטים הוא מצגת.

---

# ‏חלק ה׳ — tool_choice וניתוב

## ‏16 — tool_choice

‏[סטודנטים · 16]

**על המסך:**

![tool_choice](assets/03/04-tool-choice.png)

| מצב | שימוש |
|---|---|
|‏ `auto` | ברירת מחדל |
|‏ `required` / `any` | חובה לגעת בכלי (אסור תשובה ריקה) |
|‏ named | כפיית כלי ספציפי |
|‏ `none` | טקסט בלבד — בלי קריאות |

**להקראה:**

‏tool_choice על המסך.

‏auto — המודל מחליט אם לקרוא לכלי.

‏required או any — חובה לגעת בכלי. מתאים כשאסור לענות בלי Evidence.

‏named — כפיית כלי ספציפי. מתאים לשלב קבוע ב-Workflow.

‏none — טקסט בלבד. מתאים לסיכום אחרי שיש Observations, או לשאלת הבהרה.

‏tool_choice הוא ידית שליטה של הארכיטקט, לא קישוט של ה-SDK.

‏named tool_choice שימושי בבדיקות: אתם כופים get_metrics כדי לבדוק את ה-handler בלי שהמודל יברח ל-get_logs. זה כלי הוראה וגם כלי פרוד ל-Workflow קשיח.

‏required בלי כלים רלוונטיים ב-catalog ייצור קריאות מוזרות. קודם Router, אחר כך required.

‏auto לא אומר בלי שליטה. אתם עדיין שולטים ב-catalog, ב-Router, וב-Policy. auto רק אומר שהמודל בוחר אם ומתי מתוך מה שהותר.

---

## ‏17 — מתי `none` / מתי `required`

‏[סטודנטים · 17]

**על המסך:**

- ‏`none`: סיכום אחרי Evidence, שאלת הבהרה, Escalate  
- ‏`required`: חייבים Evidence לפני תשובה (*״מה הסטטוס בפרוד?״*)  
- ‏named: שלב קבוע ב-Workflow (תמיד `get_metrics` קודם)

**להקראה:**

מתי none ומתי required.

‏none: אחרי שאספתם Evidence ואתם רוצים תשובה למשתמש בלי עוד קריאות. או Escalate. או הבהרה.

‏required: כשהשאלה דורשת מציאות. מה הסטטוס בפרוד. אל תתנו למודל להמציא.

‏named: תמיד get_metrics קודם ב-Incident מסוים, כי ככה ה-Policy שלכם.

השילוב עם מפגש 2 ברור: tool_choice הוא עוד שכבה מעל Budget ו-Stop.

דוגמה מלאה: משתמש שואל ״תסכם לי מה מצאנו״. tool_choice none. משתמש שואל ״מה CPU עכשיו״. required או auto עם כלי מדדים בcatalog. משתמש בתהליך onboarding קבוע. named create_customer_draft בשלב 2.

‏none שימושי גם אחרי POLICY deny: להסביר למשתמש שצריך אישור אדם, בלי לנסות כלי אחר מסוכן.

---

## ‏18 — Router דטרמיניסטי מול בחירת מודל

‏[סטודנטים · 18]

**על המסך:**

| קוד | מודל |
|---|---|
|‏ if intent==billing → billing tools | בוחר מתוך catalog מלא |
|‏ allow-list לפי תפקיד | גמיש יותר, יקר יותר |
| חוסם כלים מסוכנים מראש | עלול לבחור כלי מסוכן |

היברידי נפוץ: Router מצמצם catalog → מודל בוחר בפנים.

**להקראה:**

‏Router דטרמיניסטי מול בחירת מודל.

קוד יכול לצמצם: אם הכוונה billing — רק כלי billing. זה זול וצפוי.

מודל יכול לבחור מתוך catalog מלא — גמיש ויקר ופחות צפוי.

היברידי נפוץ: Router מצמצם את הרשימה, ואז המודל בוחר בתוך הרשימה המצומצמת. ככה שומרים גמישות בלי לתת למודל מאה כלים בקונטקסט.

‏Router יכול להיות קוד פשוט על כוונות, או מסווג קטן, או כללי מוצר. החשוב: הפלט שלו הוא allow-list של שמות כלים, לא תשובה למשתמש.

כשה-Router טועה ומצמצם יותר מדי — המודל לא יכול לקרוא לכלי הנכון. לכן לוגים על החלטת Router הם חובה.

‏Router גרוע: regex על מילות מפתח בלי לוג. Router טוב: מחזיר רשימת כלים + סיבת צמצום ב-Trace.

---

# ‏חלק ו׳ — Parallel מול Sequential

## ‏19 — Parallel tool calls

‏[סטודנטים · 19]

**על המסך:**

![Parallel vs Sequential](assets/03/05-parallel-vs-sequential.png)

המודל יכול לבקש כמה כלים באותה תשובה.  
ה-Host מריץ (לרוב במקביל) ומחזיר **את כל** התוצאות לפני הצעד הבא.

**להקראה:**

Parallel tool calls.

המודל יכול לבקש כמה כלים באותה תשובה. ה-Host מריץ — לעיתים במקביל — ומחזיר את כל התוצאות לפני הצעד הבא של המודל.

על המסך הצד הימני מראה get_metrics, get_logs, get_deploys ואז fan-in.

‏Parallel חוסך זמן כשהקריאות עצמאיות. הוא לא קסם. הוא חוזה תזמון שאתם חייבים להבין.

מימוש Parallel ב-Host יכול להיות threads או asyncio או סתם תור. להוראה חשוב העיקרון: אוספים את כל התוצאות לפני הצעד הבא של המודל, ושומרים ids.

ב-SDKs רבים Parallel הוא ברירת מחדל כשהמודל מחזיר כמה calls. אתם עדיין אחראים לא להריץ במקביל דברים מסוכנים. אפשר להריץ Parallel רק על כלים שמסומנים parallel_safe ב-registry.

מדדו latency של batch Parallel לפי הזמן האיטי ביותר, לא לפי סכום. זה היתרון העסקי של fan-out.

---

## ‏20 — מתי אסור Parallel

‏[סטודנטים · 20]

**על המסך:**

- תלות: `get_orders` צריך `customer_id` מ-`get_customer`  
- כתיבה לאותו משאב  
- סדר חשוב ל-Audit / כסף  
- כלי לא Idempotent + retry עיוור

**להקראה:**

מתי אסור Parallel.

כשיש תלות: get_orders צריך customer_id שחוזר מ-get_customer.

כשכותבים לאותו משאב.

כשסדר חשוב ל-Audit או לכסף.

כשהכלי לא Idempotent ויש retry עיוור.

אם אתם לא בטוחים — Sequential. Latency עדיף על מרוץ תנאים.

דוגמת כסף: get_balance ואז charge. אם תריצו Parallel — charge עלול לרוץ לפני שיש יתרה מעודכנת. Sequential חובה.

דוגמת קבצים: read config ואז write config. Parallel עלול לדרוס. Sequential חובה.

אם שני כלים קוראים אבל אחד ממלא cache גלובלי שהשני קורא — זו תלות נסתרת. Sequential או ייצוב cache לפני.

---

## ‏21 — Fan-out / Fan-in בדוגמת Incident

‏[סטודנטים · 21]

**על המסך:**

```text
fan-out: get_metrics || get_logs || get_deploys
fan-in:  observe-all → hypothesis → (optional) get_trace
```

‏Parallel חוסך latency כשהקריאות **עצמאיות**.

**להקראה:**

‏Fan-out ו-Fan-in בדוגמת Incident.

שלושה כלי קריאה במקביל. אחר כך Observation משותף. אחר כך Hypothesis. ורק אז אולי get_trace ממוקד.

זה בדיוק המקום שבו Tool Use נפגש עם Planning ממפגש 2: התוכנית אומרת מה עצמאי, וה-Host יודע להריץ Parallel בבטחה.

אחרי fan-in אל תזרקו את כל ה-JSON הגולמי חזרה למודל אם הוא ענק. סכמו ב-Host: top errors, p95 latency, last deploy id. Observation קצר = פחות טוקנים ויותר סיגנל.

‏fan-in ב-Host יכול לבחור להשמיט לוגים ארוכים ולהשאיר רק error lines. זו אחריות הנדסית, לא תפקיד המודל.

---

# ‏חלק ז׳ — Validate, Errors, Observation

## ‏22 — Validate לפני Execute

‏[סטודנטים · 22]

**על המסך:**

![Validate Execute](assets/03/06-validate-execute.png)

1. Parse JSON args  
2. Schema validate (types/enum/required)  
3. Policy (allow-list, HITL, budget)  
4. רק אז handler  

‏Args לא חוקיים → Observation של שגיאה, **לא** crash של ה-Agent.

**להקראה:**

‏Validate לפני Execute.

ארבעה שלבים: Parse, Schema validate, Policy, ורק אז handler.

‏Args לא חוקיים מחזירים Observation של שגיאה. לא מפילים את כל ה-Agent. זה מאפשר למודל לתקן קריאה במקום לסיים את התהליך בחריגה מכוערת.

הדיאגרמה על המסך היא המשמעת: אין קיצור דרך מ-tool_call ישר ל-side effect.

‏Policy באמצע Validate ו-Execute הוא המקום ל-HITL. לא אחרי שה-delete כבר רץ. לפני.

‏Validate הוא גם המקום לבדוק הרשאות משתמש: האם ה-user רשאי לראות order_id הזה. Schema לא מספיק. Authorization חי ב-Host.

‏Policy deny צריך Observation ברור: ok false, code POLICY, message needs_hitl. אחרת המודל ינסה שוב את אותו כלי.

---

## ‏23 — פורמט Observation מומלץ

‏[סטודנטים · 23]

**על המסך:**

```json
{
  "ok": true,
  "tool": "get_order",
  "data": { "status": "shipped", "total": 249.9 },
  "meta": { "latency_ms": 120 }
}
```

כישלון:
```json
{
  "ok": false,
  "tool": "get_order",
  "error": { "code": "NOT_FOUND", "message": "order 9912" }
}
```

**להקראה:**

פורמט Observation מומלץ.

הצלחה: ok true, שם הכלי, data, meta עם latency.

כישלון: ok false, error עם code ו-message קצרים.

למה מובנה? כי המודל והלוגים שלכם צריכים אותו חוזה. טקסט חופשי של שגיאה ארוכה מבלבל ומבזבז טוקנים. קוד קצר מאפשר החלטה: retry, כלי אחר, או Escalate.

שמרו על יציבות שדות ה-Observation בין גרסאות. אם שיניתם ok ל-success בלי מיגרציה — שברתם פרומפטים ולוגים. גרסאו חוזים כמו API.

‏meta.latency_ms עוזר לתקציב. meta.request_id עוזר לקורלציה עם לוגי השירות. תוסיפו מה שצריך — אבל יציב.

---

## ‏24 — Error as Observation

‏[סטודנטים · 24]

**על המסך:**

| גישה רעה | גישה טובה |
|---|---|
|‏ Exception בולע את הלולאה | מחזירים `ok:false` למודל |
| מסתירים stack בפרומפט | קוד קצר + הודעה לפעולה |
|‏ Retry עיוור על 403 | Stop / Escalate / כלי אחר |

חיבור למפגש 2: Failure Handling + Budget.

**להקראה:**

Error as Observation.

גישה רעה: Exception בולע את הלולאה, או stack ענק בפרומפט, או retry עיוור על 403.

גישה טובה: מחזירים ok false, הודעה לפעולה, וממשיכים לפי Policy.

חיבור למפגש 2: Failure Handling ו-Budget. Tool Use בלי זה הוא לולאה יקרה עם אותה שגיאה שוב ושוב.

מפת error codes קטנה עוזרת: SCHEMA, POLICY, NOT_FOUND, TIMEOUT, UPSTREAM_5XX, RATE_LIMIT. המודל והקוד יכולים להגיב אחרת לכל קוד. הודעה חופשית בלבד חוזרת לאותו בלבול.

‏RATE_LIMIT: backoff דטרמיניסטי ב-Host עדיף על תקווה שהמודל יחכה. המודל לא שעון.

---

## ‏25 — Argument Hallucination

‏[סטודנטים · 25]

**על המסך:**

תסמינים: id מומצא, enum לא קיים, יחידות שגויות, שדות חסרים ש״הושלמו״.

הגנות:
- enum + required  
- ‏Validate ב-Host  
- דוגמאות ב-description  
- לא לתת `object` חופשי בלי schema פנימי

**להקראה:**

Argument Hallucination.

תסמינים: מזהים מומצאים, ערכי enum לא קיימים, יחידות שגויות, שדות ש״הושלמו״ כי היו optional בלי משמעת.

הגנות: enum ו-required, Validate ב-Host, דוגמאות ב-description, ולא לתת object חופשי בלי schema פנימי.

כשאתם רואים באג מוזר בפרוד — בדקו קודם האם ה-arguments בכלל היו חוקיים לפני שה-handler רץ.

הזיה קלאסית: המודל ממציא order_id כי המשתמש אמר ״ההזמנה שלי״ בלי מספר. Schema required לא מציל אם המודל ממציא. לכן לפעמים עדיף לשאול הבהרה עם tool_choice none מאשר לקרוא לכלי עם id מומצא.

אפשר גם Validate עסקי: order_id חייב להתאים ל-regex, אחרת SCHEMA.

הזיה של יחידות: minutes מול seconds. enum או שם פרמטר lookback_minutes מוריד סיכון.

---

# ‏חלק ח׳ — Catalog, Cost, Safety

## ‏26 — כמה Tools בקונטקסט

‏[סטודנטים · 26]

**על המסך:**

![Tool Selection / Catalog in an Agent Loop](assets/03/08-catalog-tradeoffs.png)

כל Schema נכנס לטוקנים **בכל** קריאה.  
יותר כלים ≠ יותר חכם. לעיתים = יותר בלבול ועלות.

כלל אצבע: **מעט כלים חדים** + Router לפי תחום.

**להקראה:**

כמה Tools בקונטקסט.

כל Schema נכנס לטוקנים בכל קריאה. יותר כלים זה לא יותר אינטליגנציה. לעיתים זה יותר בלבול ויותר עלות.

כלל אצבע: מעט כלים חדים, ו-Router לפי תחום. הדיאגרמה על המסך מסכמת את ה-tradeoffs: חדות מול עמימות, סיכון מול Idempotency.

מספרים לסדר גודל: עשרות כלים עם תיאורים ארוכים יכולים לעלות אלפי טוקנים בכל סיבוב. Router שמעביר חמישה כלים רלוונטיים חוסך כסף ומעלה דיוק.

טכניקת ביניים: כלים דינמיים לפי שלב המשימה. בהתחלה רק discovery tools. אחרי שיש entity id — כלי עומק. זה Router לאורך זמן, לא רק בתחילת השיחה.

אם חייבים catalog גדול — לפחות קבצו: רק קבוצה אחת בקונטקסט בכל turn אחרי Router.

---

## ‏27 — Allow-list + Policy Gate לכלים

‏[סטודנטים · 27]

**על המסך:**

| רמת סיכון | דוגמה | מדיניות |
|---|---|---|
|‏ Read | `get_logs` | אוטומטי |
| Soft write | `restart_service` | HITL |
|‏ Hard write | `delete_resource` | אסור / שני מאשרים |
| Money | `issue_refund` | HITL + audit |

חיבור ישיר ל-Policy Gate ממפגש 2.

**להקראה:**

‏Allow-list ו-Policy Gate לכלים.

‏Read כמו get_logs — אוטומטי.

‏Soft write כמו restart — HITL.

‏Hard write כמו delete — אסור או שני מאשרים.

‏Money כמו refund — HITL ו-Audit.

זה אותו רעיון ממפגש 2, עכשיו ברמת הכלי הבודד. Catalog בלי רמות סיכון הוא רשימת משאלות, לא מערכת.

שני מאשרים ל-delete זה לא תיאוריה. בפרוד זה אומר שני אנשים או אדם + מערכת שינוי חלון. תעדו את האישור ב-Trace עם tool_call_id של הפעולה המסוכנת.

כסף + אוטומציה בלי HITL הוא הסיפור הקלאסי של כותרות עיתונים. אל תהיו הדוגמה בקורס.

---

## ‏28 — Idempotency של Tools

‏[סטודנטים · 28]

**על המסך:**

- Idempotent: `get_order`, `describe_instances`  
- לא: `charge_card`, `create_ticket` בלי idempotency key  

‏Retry בטוח רק על Idempotent (או עם key).

**להקראה:**

‏Idempotency של Tools.

‏get_order ו-describe_instances הם Idempotent. אפשר retry.

‏charge_card ו-create_ticket בלי מפתח — לא. Retry יכול לחייב פעמיים או לפתוח עשרה טיקטים.

אם חייבים retry על כתיבה — Idempotency key בצד ה-Host והשירות.

‏Idempotency key אפשר להעביר כפרמטר או לייצר ב-Host מ-hash של user+intent+window. העיקר שאותו retry לא ייצור ישות כפולה.

גם read יכול להיות לא Idempotent אם הוא מקדם cursor או מושך הודעה מתור. סמנו נכון.

---

## ‏29 — Secrets ו-PII

‏[סטודנטים · 29]

**על המסך:**

- אל תשימו מפתחות ב-Schema / ב-Description  
- אל תדפיסו secrets ב-Observation ללוג פתוח  
- ‏Redact PII ב-Trace כשצריך  
- ‏Credentials רק ב-Host env / IAM

**להקראה:**

‏Secrets ו-PII.

אל תשימו מפתחות ב-Schema או ב-Description. אל תדפיסו secrets ב-Observation ללוג פתוח. Redact PII ב-Trace כשצריך. Credentials רק ב-Host env או IAM.

‏Function Calling לא מבטל אבטחה בסיסית. הוא מגדיל את משטח ההדלפה אם אתם רשלנים בלוגים.

גם מפתחות זמניים ב-Observation הם סכנה אם הלוג נשלח לצד שלישי לניתוח. Redact לפני ship ל-log aggregator כשצריך.

‏PII ב-arguments גם מסוכן בלוגים של פרומפט. שקלו hashing של customer email ב-Trace.

---

# ‏חלק ט׳ — MCP (מבוא)

## ‏30 — למה MCP?

‏[סטודנטים · 30]

**על המסך:**

![MCP Intro](assets/03/07-mcp-intro.png)

**MCP** = פרוטוקול לכלים ניידים: אותו Server יכול לשרת Hosts שונים.  
היום: רעיון + גבולות. עומק יישום — בהמשך הקורס / בפרודקציה.

**להקראה:**

למה MCP.

על המסך: Host, Client, Server. הרעיון: כלים ניידים. אותו Server יכול לשרת Hosts שונים.

היום זה מבוא בלבד. אנחנו לא צוללים ליישום מלא. חשוב שתכירו את השם ואת הגבול: MCP לא מחליף Validate ו-Policy. הוא דרך לחשוף כלים.

למה לא צוללים היום: MCP אקוסיסטם מתפתח, והקורס רוצה קודם חוזה Function Calling יציב בראש. בלי החוזה — MCP רק מצמיד צינורות לכלים גרועים.

‏MCP מופיע בכלים כמו Claude Desktop ו-Cursor. ההיכרות היום היא כדי שתזהו את השכבה כשתפגשו אותה.

---

## ‏31 — Host · Client · Server

‏[סטודנטים · 31]

**על המסך:**

| רכיב | תפקיד |
|---|---|
|‏ Host | אפליקציית ה-Agent |
|‏ Client | מתחבר ל-Servers |
|‏ Server | חושף Tools / Resources |

‏Function Calling נשאר: המודל עדיין מציע; ה-Host עדיין מריץ.

**להקראה:**

Host, Client, Server.

‏Host — אפליקציית ה-Agent.

‏Client — מתחבר ל-Servers.

‏Server — חושף Tools ו-Resources.

‏Function Calling נשאר: המודל מציע, ה-Host מריץ. MCP משנה איך מגלים ומחברים כלים, לא את כלל הברזל של הביצוע.

אם Host שלכם כבר יודע Validate ו-Policy, חיבור MCP Server הוא תוספת discovery. אם Host לא יודע — MCP לא יציל אתכם.

‏Server שמחזיר מאה כלים בלי תיאורים טובים מחזיר אתכם לבעיית Catalog — רק עם פרוטוקול יפה מסביב.

---

## ‏32 — PinchTab כ-MCP Server לדפדפן

‏[סטודנטים · 32]

**על המסך:**

**PinchTab** = דוגמה חיה ל-MCP: Server שחושף כלי Browser ל-Host (Cursor / Claude / סוכן שלכם).

```json
{ "mcpServers": { "pinchtab": { "command": "pinchtab", "args": ["mcp"] } } }
```

כלים לדוגמה (קידומת `pinchtab_`):  
`navigate` · `snapshot` · `click` · `fill` · `get_text` · `screenshot`

Lab: [`labs/03-pinchtab-mcp/`](labs/03-pinchtab-mcp/)

**להקראה:**

עכשיו דוגמה שתראו גם מחוץ למצגת: PinchTab.

‏PinchTab‏ הוא MCP Server לדפדפן. ה-Host — למשל Cursor — מתחבר עם command pinchtab ו-args mcp. מהרגע הזה לסוכן יש כלים: navigate, snapshot, click, fill, get_text, screenshot.

שימו לב למשמעת של המפגש: המודל עדיין רק מציע. PinchTab הוא ה-Host-side executor מול Chrome. Schema של כל כלי, הרשאות domains, ו-Policy — חיים בצד של PinchTab ושלכם, לא בתוך המודל.

יש Lab תחת labs/03-pinchtab-mcp עם README לסטודנטים, סקריפט headed, ודוגמת MCP ל-Cursor. תריצו אצלכם עם חלון גלוי ותראו snap, text ו-screenshot.

‏PinchTab מוכיח ש-MCP הוא צינור לחוזים כאלה — לא קסם. אל תשתפו token מתוך config.json אם תפתחו אותו.

---

## ‏33 — הדגמה: headed browser (תריצו אצלכם)

‏[סטודנטים · 33]

**על המסך:**

```bash
cd labs/03-pinchtab-mcp
./run-headed-demo.sh
```

מה תראו:
1. ‏Chrome **גלוי** (`pinchtab server -H`) — אם השרת רץ headless, הפעילו מחדש עם `-H`  
2. ‏`nav` + `snap` → refs כמו `e5`  
3. ‏`text` + `screenshot` תחת `out/`  

אותו חוזה ב-MCP: המודל מציע `pinchtab_navigate` / `pinchtab_snapshot` — PinchTab מריץ.

זכרו: תוכן מהעמוד = untrusted · Validate/Policy עדיין חובה · אל תשתפו token מ-`~/.pinchtab/config.json`.

**להקראה:**

השקופית הזו היא הוראת הרצה.

נכנסים ל-labs/03-pinchtab-mcp ומריצים run-headed-demo.sh.

הסקריפט מעלה שרת ב-headed, יוצר session לסוכן, מנווט ל-example.com, עושה snap עם refs, מושך text, ושומר screenshot תחת out.

ב-MCP אותם שמות כלים עם קידומת pinchtab_. ההבדל הוא רק איך ה-Host מדבר עם השרת — stdio JSON-RPC במקום CLI.

שתי אזהרות חשובות: תוכן מהעמוד הוא untrusted — אל תצייתו להוראות שמוטמעות ב-HTML. ו-Validate עם allowlist לדומיינים נשאר חובה גם כשהכלי יפה.

ברירת המחדל אחרי התקנה לרוב headless — בלי `server -H` לא תראו חלון. אם השרת כבר רץ כך: `pinchtab server stop` ואז `pinchtab server -H -b`. אחרי הריצה בדקו את `out/` עם snap, text ו-screenshot.

---

# ‏חלק י׳ — דוגמאות עבודה

## ‏34 — Support Agent: Catalog

‏[סטודנטים · 34]

**על המסך:**

| Tool | Side-effect | Policy |
|---|---|---|
| `get_customer` | read | auto |
| `get_order` | read | auto |
| `create_ticket` | write | auto + idem key |
| `issue_refund` | money | HITL |

מטרה לדוגמה: *״לקוח 441 על הזמנה 9912 — סטטוס ומתי הגיע?״*

**להקראה:**

‏Support Agent — Catalog לדוגמה.

‏get_customer ו-get_order — read, אוטומטי.

‏create_ticket — write עם idempotency key.

issue_refund — money, HITL.

המטרה לדוגמה: לקוח 441 על הזמנה 9912 — סטטוס ומתי הגיע. שימו לב שאין כאן צורך ב-refund. Catalog טוב לא מציע את הכלי המסוכן כברירת מחדל לכל שאלה.

נריץ בראש את תרחיש 441/9912: get_customer → get_order → תשובה. בלי refund. אם המודל מנסה issue_refund — Policy Gate עוצרת. זה הצלחה של Catalog, לא כישלון של המודל בלבד.

‏create_ticket בלי idem key תחת retry של המודל = שלושה טיקטים לאותה בעיה. זה כאב תמיכה קלאסי.

---

## ‏35 — DevOps Agent: Catalog

‏[סטודנטים · 35]

**על המסך:**

| Tool | Parallel-safe? | Policy |
|---|---|---|
|‏ `get_metrics` | כן | auto |
|‏ `get_logs` | כן | auto |
|‏ `get_deploys` | כן | auto |
|‏ `rollback` | לא (write) | HITL |

‏Fan-out על שלושת ה-read, אחר כך החלטה על rollback.

**להקראה:**

DevOps Agent — Catalog.

‏get_metrics, get_logs, get_deploys — Parallel-safe ו-auto.

‏rollback — write, HITL, לא Parallel עם כתיבות אחרות.

הזרימה: Fan-out על שלושת ה-read, אחר כך החלטה אנושית או מדיניות על rollback. זה מחבר Tool Use ל-Incident Agent ממפגש 2.

אם get_deploys מראה שחרור לפני עשר דקות ו-get_logs מראה spike — יש Hypothesis. rollback עדיין HITL. Tool Use נכון יודע מתי לעצור לבקש אדם.

‏rollback ב-Parallel עם scale_service הוא מתכון למרוץ. כתיבות תשתית — Sequential ומאושרות.

---

## ‏36 — Anti-Patterns

‏[סטודנטים · 36]

**על המסך:**

1. כלי אחד ענק `do_anything`  
2. ‏Schema בלי enum/required  
3. ביצוע בלי Validate  
4. ‏Parallel על כתיבות תלויות  
5. ‏Catalog של 80 כלים בלי Router  
6. ‏Secrets בתוך Observation  
7. לבלבל Tool success עם Goal success (מפגש 2!)

**להקראה:**

‏Anti-Patterns — נקריא אחד אחד.

כלי אחד ענק do_anything.

‏Schema בלי enum ו-required.

ביצוע בלי Validate.

‏Parallel על כתיבות תלויות.

‏Catalog של שמונים כלים בלי Router.

‏Secrets בתוך Observation.

ולבלבל Tool success עם Goal success — מה שמפגש 2 כבר הזהיר מפניו.

אם אתם עושים Review לצוות — התחילו מהרשימה הזו. היא תופסת שמונים אחוז מהכאב.

‏Anti-pattern נוסף שלא על המסך: כפילות כלים עם שמות כמעט זהים. get_order ו-fetch_order ו-order_lookup. המודל מתפזר. אחד חזק עדיף משלושה חלשים.

‏Anti-pattern: לבלוע Observation בתוך פרומפט ענק בלי מבנה. תמיד העדיפו JSON קצר עם ok.

---

# ‏חלק יא׳ — Lab חי

## ‏37 — Lab חי: מטרה ומגבלות

‏[סטודנטים · 37]

**על המסך:**

**מטרה:** להריץ Host שמקבל `tool_calls` לפי Schema, מאמת, מריץ כלים (כולל AWS read-only), ומחזיר Observations.

מגבלות:
- ‏Read-only בלבד ל-AWS  
- פרופיל: `nashpazformatan` · אזור: `eu-north-1`  
- בלי יצירת משאבים  
- Lab: [`labs/03-tool-calling/`](labs/03-tool-calling/)

**להקראה:**

‏Lab חי — מטרה ומגבלות.

המטרה: להריץ Host שמקבל tool_calls לפי Schema, מאמת, מריץ כלים כולל AWS בקריאה בלבד, ומחזיר Observations.

מגבלות: read-only, פרופיל nashpazformatan, אזור eu-north-1, בלי יצירת משאבים. התיקייה labs/03-tool-calling.

זה לא תרגיל לסטודנטים חיים בהקלטה. אני מריץ ומסביר בקול. אתם רואים את המסך ושומעים את הפירוק.

במפגש 2 ה-Lab הדגים Re-plan. היום ה-Lab מדגים את שכבת ה-Tool עצמה. שניהם read-only בכוונה — כדי שנוכל להקליט בלי פחד.

‏[Lab חי] עכשיו עוברים למסוף. אם AWS לא זמין — עדיין תראו את echo_status ואת דחיית ה-SCHEMA. כלי AWS ייכשלו עם EXEC ברור ב-Observation, וזה גם שיעור.

הפרופיל nashpazformatan זהה למפגש 2 בכוונה — אותה סביבת הקלטה, חוקים מוכרים, בלי הפתעות IAM באמצע צילום.

---

## ‏38 — Lab חי: מה נריץ

‏[סטודנטים · 38]

**על המסך:**

```bash
cd labs/03-tool-calling
export AWS_PROFILE=nashpazformatan AWS_REGION=eu-north-1
python3 host_loop.py
```

תראו:
1. ‏Catalog עם Schemas  
2. ‏`tool_calls` מסקריפט-מודל  
3. Validate → Execute → Observe  
4. ‏Parallel של שני כלי-קריאה  
5. סיכום + Stop

**להקראה:**

מה נריץ.

הפקודות על המסך: כניסה לתיקייה, ייצוא הפרופיל והאזור, והרצת host_loop.py.

תראו Catalog עם Schemas, tool_calls מהמודל המדומה, Validate שנכשל פעם אחת בכוונה, Parallel של קריאות, וסיכום עם Stop.

שימו לב שוב: המודל המדומה לא מריץ כלום. ה-Host מריץ. זה כל המפגש במשפט אחד.

‏[Lab חי] בהרצה תראו קודם קריאה עם label=healthy שנדחית. אחר כך parallel של echo_status תקין, sts_whoami, ו-list_ec2_running. אחר כך סיכום.

אני אקריא בקול את ה-tool_call_id כדי לקבע את ההרגל.

אם sts נכשל — בדקו AWS_PROFILE. אם echo_status נדחה — זה הצפוי ב-turn הראשון. אל ״תתקנו" את ה-SCHEMA הדמו לפני ההקלטה.

---

## ‏39 — Lab חי: Debrief

‏[סטודנטים · 39]

**על המסך:**

Checklist:
- ‏[ ] המודל לא הרץ — ה-Host הרץ  
- ‏[ ] Args עברו Validate  
- ‏[ ] Parallel החזיר שני `tool_call_id`  
- ‏[ ] שגיאת Schema חזרה כ-Observation  
- ‏[ ] אין כתיבה ל-AWS

**להקראה:**

‏Debrief של ה-Lab.

‏Checklist: המודל לא הרץ — ה-Host הרץ. Args עברו Validate. Parallel החזיר שני ids או יותר. שגיאת Schema חזרה כ-Observation. אין כתיבה ל-AWS.

אם אחד מהם נכשל אצלכם אחר כך בבית — תתקנו לפני שאתם מוסיפים עוד כלים. בסיס שבור עם Catalog גדול רק מגדיל את הרעש.

אם Parallel לא נראה מקבילי בקוד — בסדר להוראה. החשוב שכמה calls באותו turn קיבלו Observations עם ids לפני שהמודל המשיך. מימוש concurrency הוא פרט הנדסי.

אחרי ה-Lab, שאלה טובה לעצמכם: איפה הייתי מוסיף HITL אם היה כלי restart. התשובה: אחרי Validate, לפני handler.

---

# ‏חלק יב׳ — הדגמות פתרון

## ‏40 — הדגמה 1 — כתיבת Schema (בעיה)

‏[סטודנטים · 40]

**על המסך:**

תרחיש: כלי לחיפוש לוגים לפי שירות וחלון זמן.

על המסך נכתוב יחד (המרצה):
- ‏Name · Description (מתי כן/לא)  
- params: `service` enum, `minutes` int, `level` enum  
- required · side-effect = read

**להקראה:**

הדגמה 1 — כתיבת Schema.

התרחיש: כלי לחיפוש לוגים לפי שירות וחלון זמן.

אנחנו לא מחכים לתשובות מהקהל. אני כותב בקול: Name search_logs. Description שאומר read-only ולא ל-deploy. params: service כ-enum, minutes כ-integer, level כ-enum. required ל-service ו-minutes. side-effect read.

המטרה בהדגמה הזו היא משמעת כתיבה, לא יצירתיות לשמה.

בהדגמה אני נמנע מ-service כ-string חופשי. enum של api/worker/payments מכריח החלטה מוצרית: אילו שירותים ה-Agent בכלל רשאי לראות.

‏minutes כ-integer ולא כמחרוזת ״last hour״ — כי Parse ו-Validate אוהבים מספרים, לא NLP בתוך args.

---

## ‏41 — הדגמה 1 — פתרון מלא

‏[סטודנטים · 41]

**על המסך:**

```json
{
  "name": "search_logs",
  "description": "Search app logs by service and time window. Read-only. Not for deploy/rollback.",
  "parameters": {
    "type": "object",
    "properties": {
      "service": { "type": "string", "enum": ["api", "worker", "payments"] },
      "minutes": { "type": "integer", "description": "Lookback window 1..180" },
      "level": { "type": "string", "enum": ["error", "warn", "info"] }
    },
    "required": ["service", "minutes"]
  }
}
```

‏Policy: auto · Idempotent: כן · Parallel-safe: כן.

**להקראה:**

הפתרון המלא על המסך.

שימו לב ל-description שאוסר deploy ו-rollback. ל-enum של service. לטווח הדקות בתיאור. ל-required.

‏Policy: auto. Idempotent: כן. Parallel-safe: כן.

זה Schema שתוכלו לשים בפרוד אחרי שתממשו handler אמיתי. החוזה כבר נכון.

אחרי Schema כזה, ה-handler יכול לקרוא למערכת לוגים אמיתית. החוזה לא משתנה. זו הנקודה: Schema יציב, מימוש מתחלף.

‏level אופציונלי עם default error ב-handler — דוגמה טובה ל-optional חכם.

---

## ‏42 — הדגמה 2 — Validate דוחה Args

‏[סטודנטים · 42]

**על המסך:**

קריאה גרועה:
```json
{ "name": "search_logs", "arguments": { "service": "billing", "minutes": "many" } }
```

תשובת Host:
```json
{ "ok": false, "error": { "code": "SCHEMA", "message": "service not in enum; minutes not int" } }
```

המודל מתקן → קריאה חוקית → Observation עם שורות לוג.

**להקראה:**

הדגמה 2 — Validate דוחה Args.

הקריאה הגרועה: service שווה billing — לא ב-enum. minutes שווה many — לא int.

ה-Host מחזיר ok false עם קוד SCHEMA.

המודל מתקן. הקריאה החוקית רצה. Observation עם שורות לוג.

זה התרחיש שאתם רוצים לתרגל: כשלון מבוקר, לא קריסה.

שימו לב שהמודל ״תיקון״ אחרי SCHEMA הוא חלק מהלולאה. בלי Observation של שגיאה — אין תיקון. לכן Error as Observation הוא פיצ׳ר, לא מבוכה.

בתיקון אחרי SCHEMA המודל חייב להישאר על אותו tool_call חדש עם id חדש. אל תמחזר ids.

---

## ‏43 — הדגמה 3 — Parallel Fan-out

‏[סטודנטים · 43]

**על המסך:**

מטרה: *״למה ה-API איטי?״*

```text
tool_calls: [get_metrics, get_logs, get_deploys]   # parallel
→ observations (3 ids)
→ hypothesis: deploy 14:02 + error spike
→ tool_choice=none → תשובה למשתמש
```

**להקראה:**

הדגמה 3 — Parallel Fan-out.

המטרה: למה ה-API איטי.

שלושה tool_calls במקביל. שלושה ids. Hypothesis. ואז tool_choice none ותשובה למשתמש.

שימו לב מה לא קרה: לא הרצנו rollback אוטומטית. אספנו Evidence. זה Tool Use בוגר.

‏tool_choice none בסוף מונע עוד סיבוב מיותר אחרי שיש מספיק Evidence. זה חוסך כסף ומקצר תשובה.

אחרי hypothesis אפשר עוד turn עם get_trace named. זה Sequential אחרי Parallel — דפוס נפוץ.

---

## ‏44 — הדגמה 4 — Design Review ל-Catalog

‏[סטודנטים · 44]

**על המסך:**

תרחיש: Agent תמיכה עם `get_order`, `get_customer`, `create_ticket`, `issue_refund`, `delete_customer`.

תשובות שנקריא:
1. **אוטומטי:** get_*  
2. **HITL:** issue_refund  
3. **אסור:** delete_customer (או שני מאשרים)  
4. ‏**Router:** support-intent בלבד → בלי כלי DevOps  
5. ‏**Idempotency key** ל-create_ticket  
6. ‏**Trace:** כל tool_call_id בלוג

**להקראה:**

הדגמה 4 — Design Review ל-Catalog.

יש get_order, get_customer, create_ticket, issue_refund, delete_customer.

אוטומטי ל-get. HITL ל-refund. אסור או שני מאשרים ל-delete_customer. Router ל-support בלי כלי DevOps. Idempotency key ל-create_ticket. Trace עם tool_call_id.

אם אתם עושים Review בעבודה — עברו על הרשימה הזו כתבנית קבועה.

‏delete_customer ב-Catalog הוא מלכודת נפוצה בדמואים. אם הוא קיים — חייב Policy קשוחה. אם לא חייבים אותו למשימה — אל תשימו אותו ב-catalog של התמיכה.

ב-Design Review שאלו גם: מי ממלא את ה-catalog בפרוד. אם כל מפתח מוסיף כלי בלי Review — Policy נשחקת.

---

## ‏45 — הדגמה 5 — Checklist על Host

‏[סטודנטים · 45]

**על המסך:**

- ‏[x] Schemas בקונטקסט  
- ‏[x] Validate לפני execute  
- ‏[x] tool_call_id בתוצאות  
- ‏[ ] Budget על מספר קריאות  
- ‏[ ] Redaction ל-PII  
- [ ] Metrics: latency/error per tool

**להקראה:**

‏Checklist על Host.

‏Schemas בקונטקסט — כן. Validate לפני execute — כן. tool_call_id — כן.

‏Budget על מספר קריאות — צריך. Redaction ל-PII — צריך. Metrics לכל כלי — צריך.

הנקודות החסרות הן העבודה שלכם אחרי המפגש. Host בלי Budget ו-Metrics יהפוך ליקר בשקט.

‏Budget על מספר קריאות לכל turn ו לכל run. בלי זה Parallel יכול להפוך ל-fan-out יקר. Metrics per tool עוזרים למצוא כלי איטי או שבור.

‏Checklist חסר נוסף: בדיקת timeout לכל handler. Tool תקוע תוקע Agent.

---

## ‏46 — סיכום

‏[סטודנטים · 46]

**על המסך:**

- ‏Tool = חוזה; המודל מציע, הקוד מריץ  
- ‏Schema טוב = Description + enum/required  
- Validate · Observation · tool_choice · Parallel  
- ‏Catalog קטן + Policy לכתיבה/כסף  
- ‏MCP = ניידות כלים · דוגמה: PinchTab browser tools  
- ‏Lab: Host אמיתי עם Validate + AWS read-only · PinchTab headed MCP  
- מפגש 4: **LangGraph לבניית Agents**

**להקראה:**

סיכום המפגש.

‏Tool הוא חוזה. המודל מציע. הקוד מריץ.

‏Schema טוב הוא Description ועוד enum ו-required.

‏Validate, Observation, tool_choice, Parallel — ארבע ידיתות שליטה.

‏Catalog קטן ועם Policy לכתיבה וכסף.

‏MCP הוא מבוא לניידות כלים, ו-PinchTab הוא הדוגמה החיה לדפדפן.

ב-Lab ראינו Host אמיתי.

משפט אחד לסיום: כל Agent רציני הוא Host עם חוזה כלים — לא צ׳אט עם תוספות. חזרה על משפט הברזל: Model proposes · Code executes · Observation returns. במפגש 4 נרכיב את החוזה הזה ל-Graphs ב-LangGraph.

---

## ‏47 — הכנה למפגש 4

‏[סטודנטים · 47]

**על המסך:**

- ציירו Graph קטן: nodes = tools/steps, edges = מעברים  
- סמנו איפה Conditional edge אחרי Observation  
- בונוס: איפה HITL נכנס כצומת

**להקראה:**

הכנה למפגש 4.

ציירו Graph קטן: צמתים הם כלים או שלבים, קשתות הן מעברים.

סמנו איפה Conditional edge אחרי Observation.

בונוס: איפה HITL נכנס כצומת.

זה יחבר את Tool Use של היום לגרפים של המפגש הבא.

בציור ה-Graph סמנו גם צמתים שהם לא Tools: למשל צומת Decide או צומת HITL. לא הכול חייב להיות function call.

במפגש 4 נראה איך Conditional edges מחליפים חלק מ-if ב-Host — אבל Validate לא ייעלם.

---

## ‏48 — תרגיל בית (אחרי ההקלטה)

‏[סטודנטים · 48]

**על המסך:**

1. ‏3 Tools מהעבודה: Name · Schema · Side-effect · HITL?  
2. כתבו Observation format לכישלון אחד  
3. סמנו מי מהם Parallel-safe  

</div>

**להקראה:**

תרגיל בית אחרי ההקלטה.

שלושה Tools מהעבודה: Name, Schema, Side-effect, והאם HITL.

כתבו Observation format לכישלון אחד.

סמנו מי Parallel-safe.

זה סוגר את המפגש. תודה שהלכתם איתי עד הסוף על החוזה שבין מודל לקוד. נתראה במפגש 4 על LangGraph.

התרגיל בבית מחבר את מה שהבאתם מהעבודה לחומר. אם אין לכם כלים בעבודה — המציאו שלושה למוצר שאתם מכירים, אבל עם Side-effect אמיתי.

שלחו לעצמכם תזכורת: אחרי התרגיל, סמנו איזה כלי מהשלושה הייתם מרשים ב-Parallel. זו בדיקת הבנה טובה.

---

</div>
