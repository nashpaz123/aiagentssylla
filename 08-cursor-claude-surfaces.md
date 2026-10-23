<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 8 — Cursor · Claude Code · משטחי פלט
## ‏קובץ מרצה (תסריט מלא להקלטה)

> **משך מיועד:** ~2.5–3.5 שעות **הקלטה רצופה** — דגש על הדגמות חיות (HTML בדפדפן + טלגרם)  
> **קהל בהקלטה:** אין זמן עבודה לסטודנטים חיים  
> **מצגת סטודנטים:** [`08-students-slides.md`](08-students-slides.md)  
> **תדריך מנהלים:** [`08-exec-briefing.md`](08-exec-briefing.md)  
> **הדגמת פתיחה:** [`demos/08-surface-opening/`](demos/08-surface-opening/)  
> **Lab:** [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/)

> מספור 1…30. תוויות **[…]** בלהקראה — ניווט למרצה, לא מקריאים. **בלי Copilot.**

---

# ‏הנחיות למרצה

- מקריאים את בלוק **להקראה** במלואו.
- **`[סטודנטים · N]`** — גללו למספר N.
- **`[תדריך מנהלים]`** — [`08-exec-briefing.md`](08-exec-briefing.md) אחרי שקף 1–2 ובסיכום ROI.
- **`[הדגמה חיה]`** שקף 3: `./run-claude.sh` + פתיחת HTML בדפדפן.
- **`[Lab חי]`** שקפים 21–22: `surface_claude.py` + אופציונלי Telegram.
- הכינו מראש: `ANTHROPIC_API_KEY`; אם אפשר — `TELEGRAM_*` לבדיקת שליחה חיה.
- כל בלוק קוד אצל המרצה מופיע גם אצל הסטודנטים.

---


## ‏1 — כותרת

[סטודנטים · 1]

**על המסך:**

> פתיחה — Coding agents + Surfaces

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="360" />
</p>

**‏Cursor · Claude Code · משטחי פלט**  
מעטפות שמריצות agents — ו-runtime שמוציא כרטיס HTML / הודעת טלגרם

![Coding agents + surfaces](assets/08/01-coding-agents-surfaces.png)

**להקראה:**

**[פתיחה]**
שלום למפגש השמיני. הסילבוס דיבר על Cursor ו-Copilot — אצלנו בלי Copilot. היום: Cursor ו-Claude Code כמעטפות שמריצות coding agents, ואז הדבר שהמנהלים באמת רואים — משטח פלט: כרטיס HTML וטלגרם.
**[מה על המסך]**
שלושה עמודים: מעטפת Cursor, מעטפת Claude Code, ו-Surfaces.
**[איך בנוי]**
מילון, הדגמת פתיחה חיה, הבחנות Coding מול Runtime, Lab עם Anthropic ושליחת טלגרם אופציונלית, באגים ו-Design Review. הרבה מסכים חיים.
**[חיבור]**
מפגש 7 נתן מדיניות ושערי כסף. היום אותם מספרים יורדים למשטח שבן אדם פותח בלי לקרוא לוג.


---


## ‏2 — מילון למפגש

[סטודנטים · 2]

**על המסך:**

| מונח | הסבר |
|---|---|
| ‏**Agent host / מעטפת** | סביבה שמריצה agent: מודל + לולאה + כלים (לא הכלי עצמו) |
| ‏**Cursor** | מעטפת ב-IDE: מריצה Agent עם diff, rules, MCP — אתם מאשרים שינויים |
| ‏**Claude Code** | מעטפת ב-CLI: `claude -p`, subagents, הרצות מוקלטות לתיקייה |
| ‏**Coding agent** | ה-agent שרץ *בתוך* Cursor/Claude Code ומשנה קבצים בריפו |
| ‏**Runtime agent** | Agent באפליקציה שלכם מול API (`surface_claude.py` + Anthropic) |
| ‏**Tool** | פעולה שה-agent קורא לה (Read/Write, `render_html_card`, `send_telegram`…) |
| ‏**Surface** | משטח פלט לאדם: HTML, Telegram, UI — לא טרמינל בלבד |
| ‏**Bot token** | סוד של בוט טלגרם — לא בקוד ובלא git |
| ‏**Chat ID** | יעד השליחה בטלגרם |
| ‏**Draft ≠ Send** | כתיבת `telegram.txt` ≠ `sendMessage` לרשת |
| ‏**Briefing card** | כרטיס HTML עם מספרים + route + צבע |

**להקראה:**

**[מילון]**
הדגש היום: Cursor ו-Claude Code הם **מעטפות** (hosts) שמריצות agents — לא הכלים עצמם. ה-Tools הם Read/Write או `send_telegram`. Coding agent רץ בתוך המעטפת; Runtime agent רץ באפליקציה שלכם.


---


## ‏3 — הדגמת פתיחה — HTML + טיוטת Telegram

[סטודנטים · 3]

**על המסך:**

תיקייה: `demos/08-surface-opening/` · **Claude Code** (או Cursor · `prompt-cursor.md`)

```bash
cd demos/08-surface-opening
./run-claude.sh reset
./run-claude.sh smb           # L-SMB → out/briefing.html + telegram.txt
# פתחו את out/briefing.html בדפדפן
./run-claude.sh enterprise    # L-ENT → עיצוב hitl
cat out/telegram.txt
```

- קלט: `data/sample_quote.json` · מפרט: `surface-spec.md`  
- פלט יפה למשתמש — לא `print` בלבד  
- שליחה אמיתית לטלגרם = Lab (עם token)

**להקראה:**

**[הדגמה חיה]**
‏`cd demos/08-surface-opening && ./run-claude.sh reset && ./run-claude.sh smb`. פתחו HTML בדפדפן על המסך. אחר כך enterprise — צבע ענבר. הראו telegram.txt. אמרו: עדיין לא שלחנו לטלגרם.
**הרצה:** 1) reset 2) smb + browser 3) enterprise 4) cat telegram.txt 5) Cursor: prompt-cursor.md


---


## ‏4 — מה ראינו — פירוק

[סטודנטים · 4]

**על המסך:**

| מה ראינו | מושג |
|---|---|
| כרטיס בדפדפן | Surface / UI |
| SMB ירוק · ENT ענבר | אותו pipeline, מסר לפי route |
| `telegram.txt` בלי שליחה | Draft ≠ Send |
| Claude Code כתב קבצים | Coding agent על תיקיית דמו |

**להקראה:**

**[פירוק]**
ארבע שורות — ארבעה חוזים. Surface, route ויזואלי, draft, coding agent.


---


## ‏5 — מה היום (+ חזרה)

[סטודנטים · 5]

**על המסך:**

| נבנה היום | כבר למדנו |
|---|---|
| Cursor מול Claude Code | מפגש 5–7: demos עם Claude Code |
| HTML + Telegram כמשטחים | מפגש 3: כלים / observations |
| Lab שולח (אופציונלי) לטלגרם | מפגש 7: Draft ≠ Send למייל |
| כללי סודות לבוט | מפגש 6: לא לשמור סודות ב-Store |

יעד: **~2.5–3.5 שעות**, הרבה הדגמות חיות.

**להקראה:**

**[מפה]**
היום ארוך במכוון בדוגמאות. חזרה קצרה בלבד למפגשים קודמים.


---


## ‏6 — שאלת המפגש + תוצרים

[סטודנטים · 6]

**על המסך:**

**שאלה:** איפה המשתמש רואה את תוצר הסוכן — ומה אסור שיישלח בלי שער?

| תוצר | "עובד" |
|---|---|
| כרטיס HTML | נפתח בדפדפן, מספרים נכונים |
| טיוטת TG | קובץ לפני שליחה |
| שליחה (אופציונלי) | רק עם env + בקשה מפורשת |
| הבחנה Cursor/Claude | יודעים מתי מה |

---

# ‏חלק ב׳ — מעטפות שמריצות Agents

_Cursor ו-Claude Code ≠ הכלים; הם מריצים את ה-agent_

**להקראה:**

**[שאלה]**
איפה רואים את הסוכן, ומה אסור שיישלח בלי שער. התוצרים בטבלה — נחזור בסיכום.


---


## ‏7 — למה לא Copilot במפגש הזה

[סטודנטים · 7]

**על המסך:**

הסילבוס מזכיר Copilot — **בהקלטה שלנו:** Cursor + Claude Code כמעטפות בלבד.

| שכבה | מה זה באמת | תפקיד אצלנו |
|---|---|---|
| Cursor | מעטפת IDE | מריצה Agent שעורכת ריפו / UI |
| Claude Code | מעטפת CLI | מריצה Agent בהדגמות `claude -p` |
| Anthropic API | מודל + tool-use | Runtime agent ב-Lab |
| Tools | Read/Write/`send_telegram`… | הפעולות שה-agent קורא להן |

![Cursor vs Claude](assets/08/04-cursor-vs-claude.png)

**להקראה:**

**[מעטפות]**
שקיפות על Copilot. הטבלה: Host / Agent / Tools / API. אל תגידו "Cursor הוא כלי" — תגידו "Cursor מריץ agent שמשתמש בכלים".


---


## ‏8 — Cursor כמעטפת (IDE host)

[סטודנטים · 8]

**על המסך:**

- אתם פותחים צ׳אט **Agent** — Cursor מריץ את ה-agent  
- Diff לפני Accept — האדם בשער  
- Rules (`.cursor/rules`) מגבילים/מכוונים את ה-agent  
- מתאים לשיפור CSS/HTML של הכרטיס  

הדגמה קצרה: פתחו `prompt-cursor.md` ב-Cursor ושפרו מרווחים ב-`briefing.html` **בלי** לשנות מספרים.

**להקראה:**

**[Cursor host]**
אתם מדברים עם Agent; Cursor הוא המעטפת שמריצה אותו ומציגה diff. הדגימו שיפור עיצוב בלי לשנות מספרים.


---


## ‏9 — Claude Code כמעטפת (CLI host)

[סטודנטים · 9]

**על המסך:**

```bash
claude -p "$(cat prompt-smb.md)" \
  --setting-sources project,local \
  --allowedTools "Read,Write,Edit,Glob,Grep,Task"
```

- `claude` = מעטפת; ה-agent בפנים משתמש ב-Tools ברשימה  
- `run-claude.sh` = חזרתיות להקלטה  
- subagent `surface` ב-`.claude/agents/` — עדיין בתוך אותה מעטפת  
- stream-json + filter — רואים קריאות כלי (Write) בזמן אמת

**להקראה:**

**[Claude Code host]**
‏`claude -p` מריץ agent עם allowlist של Tools. `run-claude.sh` חוזר בהקלטה. subagent עדיין בתוך אותה מעטפת.


---


## ‏10 — Coding agent ≠ Runtime agent

[סטודנטים · 10]

**על המסך:**

שניהם **agents**. ההבדל: באיזו מעטפת הם רצים ומה המטרה.

| | Coding (בתוך Cursor/Claude Code) | Runtime (באפליקציה) |
|---|---|---|
| מעטפת | IDE / CLI | הקוד שלכם + Anthropic |
| מתי | פיתוח / דמו בניה | שימוש אצל AE |
| Tools | קבצי ריפו (Read/Write/…) | `get_quote` · `render_*` · `send_*` |
| סודות | לא בקומיט | env בזמן ריצה |
| דוגמה | `demos/08-…` | `labs/08-…/surface_claude.py` |

---

# ‏חלק ג׳ — Surfaces

_HTML וטלגרם כערוצי פלט_

**להקראה:**

**[Coding ≠ Runtime]**
שניהם agents. ההבדל: מעטפת ומטרה. Coding בונה קבצים; Runtime מגיש Surface למשתמש.


---


## ‏11 — מה זה Surface ולמה אכפת

[סטודנטים · 11]

**על המסך:**

טרמינל טוב למפתחים. AE ומנהל רוצים:

- כרטיס ויזואלי (HTML)  
- דחיפה לנייד (Telegram)  

![Quote to surface](assets/08/02-quote-to-surface.png)

**להקראה:**

**[Surface]**
AE לא יקרא JSON. כרטיס וטלגרם הם המוצר מבחינתו.


---


## ‏12 — Pipeline: Quote → HTML → TG → Send?

[סטודנטים · 12]

**על המסך:**

1. `get_quote`  
2. `render_html_card` → `out/briefing.html`  
3. `render_telegram_message` → `out/telegram.txt`  
4. `send_telegram` — **רק** אם ביקשו + יש token

**להקראה:**

**[Pipeline]**
ארבעה שלבים בקול. השליחה היא הרביעית והמסוכנת.


---


## ‏13 — HTML card — עקרונות

[סטודנטים · 13]

**על המסך:**

- קובץ יחיד · CSS פנימי · `dir="rtl"`  
- צבע לפי `route` (auto/hitl/blocked)  
- כותרת + טבלה + פוטר "טיוטה פנימית"  
- מספרים **רק** מה-JSON

**להקראה:**

**[HTML]**
קובץ יחיד, RTL, צבע לפי route, מספרים מה-JSON. פתחו דוגמה חיה אם יש.


---


## ‏14 — Telegram כמשטח

[סטודנטים · 14]

**על המסך:**

![Telegram surface](assets/08/03-telegram-surface.png)

| רכיב | תפקיד |
|---|---|
| Bot token | זהות הבוט (סוד) |
| Chat ID | לאן שולחים |
| `sendMessage` | Side-effect ברשת |

בלי env → הכלי מחזיר שגיאה ברורה — **לא** `sent=true` מזויף.

**להקראה:**

**[Telegram]**
Token ו-Chat ID. בלי env — שגיאה. אל תזייפו sent.


---


## ‏15 — Draft ≠ Send (חוזר ממפגש 7)

[סטודנטים · 15]

**על המסך:**

| כלי | רשת? |
|---|---|
| `render_telegram_message` | לא |
| `send_telegram` | כן |

אותו עיקרון כמו טיוטת מייל במפגש 7 — ערוץ אחר.

**להקראה:**

**[Draft≠Send]**
חזרו על מפגש 7. ערוץ אחר, אותו חוק.


---


## ‏16 — סודות והגדרות

[סטודנטים · 16]

**על המסך:**

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export TELEGRAM_BOT_TOKEN=123:ABC...   # אופציונלי
export TELEGRAM_CHAT_ID=...            # אופציונלי
```

- לא בקוד · לא ב-git · לא בצילום מסך  
- Chat ID: `getUpdates` אחרי הודעה לבוט

**להקראה:**

**[סודות]**
הקריאו את שלושת ה-export. אל תציגו token אמיתי בהקלטה — השתמשו ב-placeholder או בצילום מטושטש.


---


## ‏17 — Guardrails למשטחים

[סטודנטים · 17]

**על המסך:**

- [ ] מספרים מכלי/JSON בלבד  
- [ ] HTML לא מריץ JS חיצוני לא מבוקר בדמו  
- [ ] אין שליחה בלי בקשה מפורשת  
- [ ] אין token בלוגים  
- [ ] PII — לא לצ׳אט ציבורי

**להקראה:**

**[Guardrails]**
עברו תיבה-תיבה כמו go/no-go.


---


## ‏18 — Anti-Patterns

[סטודנטים · 18]

**על המסך:**

| אנטי־דפוס | למה נשבר |
|---|---|
| "הסוכן ידפיס יפה בטרמינל" | המשתמש לא שם |
| שליחה אוטומטית לכל render | ספאם / דליפה |
| Token ב-repo | פריצה |
| HTML עם מספרים מהפרומפט | מחיר ישן/בדוי |
| לערבב Copilot כחובה | לא במסלול שלנו |

**להקראה:**

**[Anti]**
השורה על טרמינל כואבת למפתחים — ולכן חשובה. Token ב-repo — סיפור קצר.


---


## ‏19 — Checklist לפני פיילוט Surface

[סטודנטים · 19]

**על המסך:**

- [ ] יש קובץ draft לפני send  
- [ ] יש HTML שנפתח בלי שרת  
- [ ] יש הפרדת Coding / Runtime  
- [ ] יש env מתועד לטלגרם  
- [ ] יש תרחיש SMB מול ENT ויזואלית  

---

# ‏חלק ד׳ — Lab

_הרבה הרצות — רואים כרטיס וטלגרם_

**להקראה:**

**[Checklist]**
שער כניסה ל-Lab.


---


## ‏20 — Lab — מטרה

[סטודנטים · 20]

**על המסך:**

תיקייה: [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/)

דורש **`ANTHROPIC_API_KEY`**.  
טלגרם אמיתי: `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`.

![Lab tools](assets/08/05-lab-tools.png)

לידים: `L-SMB` · `L-ENT` · `L-UPSELL`

**להקראה:**

**[Lab מטרה]**
Anthropic חובה. טלגרם אופציונלי אבל מרשים בהקלטה אם מוכן מראש.


---


## ‏21 — Lab — מה נריץ

[סטודנטים · 21]

**על המסך:**

```bash
cd labs/08-agent-surfaces
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

python3 surface_claude.py reset
python3 surface_claude.py chat --lead L-SMB --message "הכן כרטיס HTML וטיוטת טלגרם להצעה"
# פתחו out/briefing.html בדפדפן

python3 surface_claude.py chat --lead L-ENT --message "הכן כרטיס — הדגש שממתין למנהל"
python3 surface_claude.py chat --lead L-UPSELL --message "הכן כרטיס וטיוטה ללקוח קיים (upsell)"

# אופציונלי — שליחה:
# export TELEGRAM_BOT_TOKEN=...
# export TELEGRAM_CHAT_ID=...
python3 surface_claude.py chat --lead L-SMB --message "שלח את הסיכום לטלגרם עכשיו"
python3 surface_claude.py show
```

**להקראה:**

**[Lab חי]**
הריצו SMB, פתחו HTML, ENT, UPSELL, ואם יש token — send. עצרו על TOOL.
**הרצה:** venv + key → reset → SMB → browser → ENT → UPSELL → send אופציונלי → show


---


## ‏22 — Lab — Debrief

[סטודנטים · 22]

**על המסך:**

- [ ] ראיתי כרטיס ירוק ל-SMB וענבר ל-ENT  
- [ ] `telegram.txt` נוצר לפני שליחה  
- [ ] בלי token — שגיאה מפורשת, לא הצלחה מזויפת  
- [ ] עם token — הודעה בנייד + `TOOL -> send_telegram`  
- [ ] Upsell מסומן בכרטיס/טיוטה  

---

# ‏חלק ה׳ — הדגמות נוספות וסיכום

**להקראה:**

**[Debrief]**
ענו אתם על התיבות בקול.


---


## ‏23 — הדגמה — Cursor משפר UI

[סטודנטים · 23]

**על המסך:**

1. פתחו `out/briefing.html` אחרי Lab  
2. ב-Cursor: "שפר טיפוגרפיה ומרווחים בלי לשנות מספרים"  
3. רעננו בדפדפן  

מסר: מעטפת Cursor מריצה coding agent שמשפר Surface; ה-runtime agent מזין נתונים.

**להקראה:**

**[Cursor חי]**
מעטפת IDE מריצה coding agent שמשפר Surface; ה-runtime מזין מספרים.


---


## ‏24 — הדגמה — כפתורים שמשנים פלט

[סטודנטים · 24]

**על המסך:**

| שינוי | תוצאה ויזואלית |
|---|---|
| `L-SMB` | ירוק / approved |
| `L-ENT` | ענבר / pending_manager |
| `L-UPSELL` | ירוק + תווית upsell |
| בקשת send בלי env | error בלוג |
| בקשת send עם env | הודעה בטלגרם |

**להקראה:**

**[כפתורים]**
טבלה ויזואלית — אותו Lab, תוצאות שונות.


---


## ‏25 — באג: "נשלח" בלי token

[סטודנטים · 25]

**על המסך:**

סימפטום: המודל כותב "שלחתי לטלגרם" אבל אין הודעה.  
בדיקה: אין `TOOL -> send_telegram` או הכלי החזיר `missing_telegram_env`.  
תיקון: האמת בתוצאת הכלי בלבד; הפרומפט אוסר להצהיר sent בלי `sent=true`.

**להקראה:**

**[באג]**
סימפטום / בדיקה / תיקון. האמת בתוצאת הכלי.


---


## ‏26 — Design Review — "נשלח כל הצעה לטלגרם של הלקוח"

[סטודנטים · 26]

**על המסך:**

| שאלה | החלטה |
|---|---|
| למי הצ׳אט? | פנימי ל-AE/מנהל קודם |
| מתי send? | אחרי render + אישור |
| מה בתוכן? | בלי PII מיותר |
| Audit? | לוג HTTP + lead_id |

**להקראה:**

**[Design Review]**
אל תשלחו ללקוח הסופי קודם. צ׳אט פנימי + שער.


---


## ‏27 — ROI קצר למשטחים

[סטודנטים · 27]

**על המסך:**

| למי | ערך |
|---|---|
| AE | כרטיס מוכן + התראה בנייד |
| מנהל | רואה HITL בלי לפתוח CRM |
| מפתח | אותו סוכן — ערוצים שונים |

**להקראה:**

**[ROI]**
שלושה קהלים — משפט לכל אחד.


---


## ‏28 — סיכום

[סטודנטים · 28]

**על המסך:**

- Cursor / Claude Code = **מעטפות** שמריצות agents (לא "הכלים")  
- Surface = HTML / Telegram / UI  
- Coding agent ≠ Runtime agent  
- Draft ≠ Send  
- Lab: כרטיס + טיוטה + שליחה אופציונלית  
- במפגש הבא: **Testing ו-Debugging Agents**

**להקראה:**

**[סיכום]**
מעטפה ≠ כלי. Agent ≠ Surface. Draft ≠ Send. בלי Copilot.
**[סיום רמז]** במפגש 9 — Testing.


---


## ‏29 — הכנה למפגש 9

[סטודנטים · 29]

**על המסך:**

- חשבו: איך בודקים ש-HTML מכיל את הסכום הנכון?  
- איך בודקים ש-send לא רץ בלי token?  
- רשמו 2 בדיקות שבירות שתרצו לראות בלוג

**להקראה:**

**[הכנה ל-9]**
בדיקות ישברו HTML ו-send — תנו רמז למפגש הבא.


---


## ‏30 — תרגיל בית

[סטודנטים · 30]

**על המסך:**

1. הוסיפו שדה `valid_until` ל-JSON והציגו ב-HTML  
2. הוסיפו כלי `render_markdown_report` לקובץ `out/report.md`  
3. תעדו ב-README איך משיגים `TELEGRAM_CHAT_ID`  
4. בונוס: כפתור CSS ל-HITL שמציג "ממתין למנהל" בגדול  

</div>

**להקראה:**

**[בית]**
ארבע משימות קצרות. בונוס ויזואלי ל-HITL.
**[סיום]**
תודה. במפגש 9 — Testing ו-Debugging Agents.


---


</div>
