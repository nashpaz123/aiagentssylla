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
> **Lab A:** [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/) · **Lab B:** [`labs/08-facility-surfaces/`](labs/08-facility-surfaces/)

> מספור 1…30. תוויות **[…]** בלהקראה — ניווט למרצה, לא מקריאים. **בלי Copilot.**

---

# ‏הנחיות למרצה

- מקריאים את בלוק **להקראה** במלואו.
- **`[סטודנטים · N]`** — גללו למספר N.
- **`[תדריך מנהלים]`** — [`08-exec-briefing.md`](08-exec-briefing.md) אחרי שקף 1–2 ובסיכום ROI.
- **`[הדגמה חיה]`** שקף 3: `./run-claude.sh` + פתיחת HTML בדפדפן.
- **`[Lab חי]`** שקפים 21–22: `surface_claude.py` + Telegram עם שליחה אמיתית.
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
מילון, הדגמת פתיחה חיה, הבחנות Coding מול Runtime, Lab עם Anthropic ושליחת טלגרם אמיתית לצ׳אט שלכם, באגים ו-Design Review. הרבה מסכים חיים.
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
| ‏**Tool** | פעולה שה-agent קורא לה (Read/Write, `render_html_card`, `notify_telegram`…) |
| ‏**Surface** | משטח פלט לאדם: HTML, Telegram, UI — לא טרמינל בלבד |
| ‏**Bot token** | סוד של בוט טלגרם — לא בקוד ובלא git |
| ‏**Chat ID** | יעד השליחה בטלגרם |
| ‏**notify_telegram** | כלי שכותב הודעה **ושולח** לצ׳אט הפנימי (המרצה/AE) |
| ‏**Briefing card** | כרטיס HTML עם מספרים + route/severity + צבע |
| ‏**צ׳אט פנימי** | טלגרם שלכם / AE / מנהל מתקנים — כן שולחים |
| ‏**Nimbus** | דומיין מכירות (הצעות מחיר) — Lab A |
| ‏**Atlas Facility** | דומיין ניהול מתקנים (קריאות שירות) — Lab B · לא הזמנות לקוח |

**להקראה:**

**[מילון]**
הדגש היום: Cursor ו-Claude Code הם **מעטפות** (hosts) שמריצות agents — לא הכלים עצמם. ה-Tools הם Read/Write או `notify_telegram`. Coding agent רץ בתוך המעטפת; Runtime agent רץ באפליקציה שלכם.

---


## ‏3 — הדגמת פתיחה — HTML + טיוטת Telegram

[סטודנטים · 3]

**על המסך:**

תיקייה: `demos/08-surface-opening/` · **Claude Code** (או Cursor · `prompt-cursor.md`)

```bash
cd demos/08-surface-opening
cp .env.example .env   # חד־פעמי: TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
./run-claude.sh reset
./run-claude.sh smb
./send-telegram.sh            # שולח אליכם לטלגרם
# פתחו out/briefing.html בדפדפן
./run-claude.sh enterprise && ./send-telegram.sh
```

- קלט: `data/sample_quote.json` · מפרט: `surface-spec.md`  
- HTML בדפדפן + **הודעה אמיתית** בטלגרם

**להקראה:**

**[הדגמה חיה]**
הכינו `.env` מראש. אחרי `./run-claude.sh smb` הריצו `./send-telegram.sh` ותראו את הטלפון על המסך (או צילום). אחר כך enterprise + send. אמרו: זה צ׳אט פנימי שלכם — המוצר הוא שליחה אמיתית.
**הרצה:** env → reset → smb → send-telegram → browser → enterprise → send

---


## ‏4 — מה ראינו — פירוק

[סטודנטים · 4]

**על המסך:**

| מה ראינו | מושג |
|---|---|
| כרטיס בדפדפן | Surface / UI |
| SMB ירוק · ENT ענבר | אותו pipeline, מסר לפי route |
| `./send-telegram.sh` אחרי הדמו | שליחה אמיתית לצ׳אט שלכם |
| Claude Code הרצה agent שכתב קבצים | מעטפת CLI + coding agent |

**להקראה:**

**[פירוק]**
ארבע שורות — ארבעה חוזים. Surface, route ויזואלי, draft, coding agent.

---


## ‏5 — מה היום (+ חזרה)

[סטודנטים · 5]

**על המסך:**

| נבנה היום | כבר למדנו |
|---|---|
| Cursor מול Claude Code כמעטפות | מפגש 5–7: demos עם Claude Code |
| HTML + Telegram כמשטחים | מפגש 3: כלים / observations |
| Lab A Nimbus + Lab B Atlas (Facility) | מפגש 7: שערי כסף על אותם מספרים |
| כללי סודות לבוט | מפגש 6: לא לשמור סודות ב-Store |

יעד: **~2.5–3.5 שעות**, הרבה הדגמות חיות.

**להקראה:**

**[מפה]**
היום ארוך במכוון בדוגמאות. חזרה קצרה בלבד למפגשים קודמים.

---


## ‏6 — שאלת המפגש + תוצרים

[סטודנטים · 6]

**על המסך:**

**שאלה:** איפה המשתמש רואה את תוצר הסוכן — ואיך מגיעה התראה לנייד?

| תוצר | "עובד" |
|---|---|
| כרטיס HTML | נפתח בדפדפן, מספרים נכונים |
| טלגרם | הודעה מגיעה לצ׳אט שלכם |
| `notify_telegram` / `send-telegram.sh` | `sent=true` בלוג / API |
| הבחנה מעטפת IDE / מעטפת CLI / runtime | יודעים מתי מה |

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
| Tools | Read/Write/`notify_telegram`… | הפעולות שה-agent קורא להן |

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
3. `notify_telegram` → כותב `telegram.txt` **ושולח** לצ׳אט הפנימי

**להקראה:**

**[Pipeline]**
שלושה שלבים: get_quote → HTML → notify_telegram (כותב ושולח).

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


## ‏14 — Telegram כמשטח (עם שליחה)

[סטודנטים · 14]

**על המסך:**

![Telegram surface](assets/08/03-telegram-surface.png)

| רכיב | תפקיד |
|---|---|
| Bot token | זהות הבוט (סוד ב-`.env`) |
| Chat ID | **הצ׳אט שלכם** — יעד השליחה |
| `notify_telegram` / `send-telegram.sh` | `sendMessage` אמיתי |

בלי env → כישלון ברור. עם env → ההודעה חייבת להגיע לנייד.

**להקראה:**

**[Telegram]**
Token + Chat ID שלכם. בלי זה Lab לא רץ. עם זה — ההודעה חייבת להגיע.

---


## ‏15 — פנימי כן · לקוח סופי לא

[סטודנטים · 15]

**על המסך:**

| ערוץ | שולחים? |
|---|---|
| טלגרם פנימי (מרצה / AE) | **כן** — זה המוצר של המפגש |
| HTML briefing | כן (קובץ / דפדפן) |
| מייל/הודעה ללקוח הסופי | לא אוטומטית (מפגש 7: Draft ≠ Send למייל) |

**להקראה:**

**[פנימי כן]**
מפרידים: טלגרם פנימי שולחים; מייל ללקוח ממפגש 7 נשאר עם שער.

---


## ‏16 — סודות והגדרות

[סטודנטים · 16]

**על המסך:**

```bash
cp .env.example .env
# ANTHROPIC_API_KEY=...
# TELEGRAM_BOT_TOKEN=...
# TELEGRAM_CHAT_ID=...   # הצ׳אט האישי שלכם
```

- לא בקוד · לא ב-git · לא בצילום מסך  
- Chat ID: שלחו Start לבוט → `getUpdates` → `chat.id`

**להקראה:**

**[סודות]**
הקריאו את שלושת ה-export. אל תציגו token אמיתי בהקלטה — השתמשו ב-placeholder או בצילום מטושטש.

---


## ‏17 — Guardrails למשטחים

[סטודנטים · 17]

**על המסך:**

- [ ] מספרים מכלי/JSON בלבד  
- [ ] HTML לא מריץ JS חיצוני לא מבוקר בדמו  
- [ ] שליחה לצ׳אט פנימי עובדת בהקלטה  
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
| שליחה ללקוח סופי בלי שער | ספאם / דליפה — צ׳אט פנימי כן |
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

- [ ] יש HTML שנפתח בלי שרת  
- [ ] יש `.env` עם token + chat id שלכם  
- [ ] הודעת SMB מגיעה לטלגרם  
- [ ] יש הפרדת Coding / Runtime  
- [ ] יש תרחיש SMB מול ENT **או** HVAC מול ELEV ויזואלית  

---

# ‏חלק ד׳ — Lab

_הרבה הרצות — רואים כרטיס וטלגרם_

**להקראה:**

**[Checklist]**
שער כניסה ל-Lab.

---


## ‏20 — Lab — שני דומיינים (גיוון)

[סטודנטים · 20]

**על המסך:**

אותו דפוס משטחים · **שני עולמות עסקיים**:

| Lab | דומיין | תיקייה | מזהים |
|---|---|---|---|
| **A · Nimbus** | מכירות / הצעות מחיר | [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/) | `L-SMB` · `L-ENT` · `L-UPSELL` |
| **B · Atlas** | ניהול מתקנים / קריאות שירות | [`labs/08-facility-surfaces/`](labs/08-facility-surfaces/) | `WO-HVAC` · `WO-ELEV` · `WO-ACCESS` |

דורש **`ANTHROPIC_API_KEY`** + **`TELEGRAM_*`** בשניהם.

![Lab tools](assets/08/05-lab-tools.png)

מסר: Surface לא "שייך" רק ל-CRM מכירות — אותו pipeline עובד על Work Orders בבניין.

**להקראה:**

**[שני דומיינים]**
Nimbus = מכירות. Atlas = מתקנים. אותו pipeline — get → HTML → notify. אמרו: Surface לא שייך רק ל-CRM.

---


## ‏21 — Lab A (Nimbus) — מה נריץ

[סטודנטים · 21]

**על המסך:**

```bash
cd labs/08-agent-surfaces
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # מלאו ANTHROPIC + TELEGRAM_*

python3 surface_claude.py reset
python3 surface_claude.py chat --lead L-SMB --message "הכן כרטיס HTML ושלח סיכום לטלגרם שלי"
# פתחו out/briefing.html — ובדקו את הטלפון

python3 surface_claude.py chat --lead L-ENT --message "הכן כרטיס ושלח — ממתין למנהל"
python3 surface_claude.py chat --lead L-UPSELL --message "הכן כרטיס ושלח ללקוח קיים (upsell)"
python3 surface_claude.py notify --lead L-SMB   # שליחה חוזרת בלי LLM
python3 surface_claude.py show
```

**להקראה:**

**[Lab A חי]**
`.env` מלא. SMB עם שליחה — בדקו נייד. ENT, UPSELL, ואז `notify` בלי LLM.

---


## ‏22 — Lab A — Debrief

[סטודנטים · 22]

**על המסך:**

- [ ] ראיתי כרטיס ירוק ל-SMB וענבר ל-ENT  
- [ ] הודעות הגיעו לטלגרם האישי  
- [ ] בלוג: `TOOL -> notify_telegram` עם `sent=true`  
- [ ] בלי `.env` — כישלון ברור, לא "נשלח" מזויף  
- [ ] Upsell מסומן בכרטיס/הודעה

**להקראה:**

**[Debrief A]**
עברו על הצ׳קליסט. הדגישו sent=true מהכלי.

---


## ‏23 — Lab B (Atlas) — קריאות שירות

[סטודנטים · 23]

**על המסך:**

תיקייה: [`labs/08-facility-surfaces/`](labs/08-facility-surfaces/) · דמו: [`demos/08-facility-opening/`](demos/08-facility-opening/)

**לא הזמנות לקוח** — מיזוג, מעלית, בקרת כניסה.

| מזהה | חומרה | צבע |
|---|---|---|
| `WO-HVAC` | `open` | כחול |
| `WO-ELEV` | `sla_breach` | אדום |
| `WO-ACCESS` | `blocked` | ענבר |

כלים: `get_work_order` · `render_html_card` · `notify_telegram`

**להקראה:**

**[Lab B Atlas]**
החליפו הקשר: אין מחירים. קריאות שירות בבניין. חומרה open/sla_breach/blocked.

---


## ‏24 — Lab B — מה נריץ

[סטודנטים · 24]

**על המסך:**

```bash
cd labs/08-facility-surfaces
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # או העתיקו מ-Lab A

python3 facility_claude.py reset
python3 facility_claude.py chat --wo WO-HVAC --message "הכן כרטיס ושלח התראה למנהל מתקנים"
python3 facility_claude.py chat --wo WO-ELEV --message "חריגת SLA — שלח עכשיו"
python3 facility_claude.py notify --wo WO-ACCESS
```

דמו קצר (Claude Code): `demos/08-facility-opening/` → `./run-claude.sh hvac|elev` → `./send-telegram.sh`

**להקראה:**

**[Lab B חי]**
הרצו WO-HVAC ואז WO-ELEV (אדום). אופציונלי: דמו Claude ב-demos/08-facility-opening.

---


## ‏25 — Lab B — Debrief

[סטודנטים · 25]

**על המסך:**

- [ ] אין מחירים / מושבים — זה לא Nimbus  
- [ ] כרטיס אדום ל-`WO-ELEV` (חריגת SLA)  
- [ ] טלגרם עם `Atlas Facility`  
- [ ] אותו דפוס: get → HTML → notify  

---

# ‏חלק ה׳ — הדגמות נוספות וסיכום

**להקראה:**

**[Debrief B]**
וידאו שאין שדות מכירה. אותו notify_telegram — דומיין אחר.

---


## ‏26 — הדגמה — Cursor משפר UI

[סטודנטים · 26]

**על המסך:**

1. פתחו `out/briefing.html` אחרי Lab  
2. ב-Cursor: "שפר טיפוגרפיה ומרווחים בלי לשנות מספרים"  
3. רעננו בדפדפן  

מסר: מעטפת Cursor מריצה coding agent שמשפר Surface; ה-runtime agent מזין נתונים.

**להקראה:**

**[Cursor UI]**
שפרו HTML של אחד הדומיינים בלי לגעת במספרים/SLA.

---


## ‏27 — הדגמה — כפתורים שמשנים פלט

[סטודנטים · 27]

**על המסך:**

| שינוי | תוצאה ויזואלית |
|---|---|
| `L-SMB` (Nimbus) | ירוק / approved |
| `L-ENT` (Nimbus) | ענבר / pending_manager |
| `WO-HVAC` (Atlas) | כחול / open |
| `WO-ELEV` (Atlas) | אדום / sla_breach |
| בלי `.env` | error ברור |
| עם `.env` | הודעה בטלגרם |

**להקראה:**

**[כפתורים]**
הראו גם L-* וגם WO-* — אותו עיקרון: קלט שונה → צבע שונה.

---


## ‏28 — באג: "נשלח" בלי אישור API

[סטודנטים · 28]

**על המסך:**

סימפטום: המודל כותב "שלחתי" אבל אין הודעה בנייד.  
בדיקה: אין `notify_telegram` עם `sent=true`, או `last_send.json` עם כשל.  
תיקון: האמת בתוצאת הכלי בלבד — לא בנרטיב המודל.

**להקראה:**

**[סיכום]**
מעטפה ≠ כלי. Agent ≠ Surface. טלגרם פנימי = שולחים. בלי Copilot.
**[סיום רמז]** במפגש 9 — Testing.

---


## ‏29 — Design Review — למי שולחים?

[סטודנטים · 29]

**על המסך:**

| שאלה | החלטה במפגש |
|---|---|
| למי הצ׳אט? | **פנימי** — המרצה / AE (כן שולחים) |
| ללקוח הסופי? | לא אוטומטית מהבוט הזה |
| מה בתוכן? | מספרים מה-Quote, בלי PII מיותר |
| Audit? | `telegram.txt` + `last_send.json` / לוג HTTP |

**להקראה:**

**[הכנה ל-9]**
בדיקות ישברו HTML ו-send — תנו רמז למפגש הבא.

---


## ‏30 — ROI קצר למשטחים

[סטודנטים · 30]

**על המסך:**

| למי | ערך |
|---|---|
| AE / מנהל מתקנים | כרטיס מוכן + התראה בנייד |
| מנהל | רואה HITL / חריגת SLA בלי לפתוח מערכת |
| מפתח | אותו דפוס Surface — דומיינים שונים |

**להקראה:**

**[בית]**
ארבע משימות קצרות. בונוס ויזואלי ל-HITL.
**[סיום]**
תודה. במפגש 9 — Testing ו-Debugging Agents.

---


## ‏31 — סיכום

[סטודנטים · 31]

**על המסך:**

- Cursor / Claude Code = **מעטפות** שמריצות agents (לא "הכלים")  
- Surface = HTML / Telegram / UI  
- Coding agent ≠ Runtime agent  
- טלגרם פנימי = **שולחים**; לקוח סופי ≠ אוטומטי  
- Lab A (Nimbus) + Lab B (Atlas Facility) — אותו Surface, דומיינים שונים  
- במפגש הבא: **Testing ו-Debugging Agents**

**להקראה:**

**[סיכום]**
מעטפה ≠ כלי. Agent ≠ Surface. טלגרם פנימי = שולחים. בלי Copilot.
**[סיום רמז]** במפגש 9 — Testing.

---


## ‏32 — הכנה למפגש 9

[סטודנטים · 32]

**על המסך:**

- חשבו: איך בודקים ש-HTML מכיל את הסכום הנכון?  
- איך בודקים ש-send לא רץ בלי token?  
- רשמו 2 בדיקות שבירות שתרצו לראות בלוג

**להקראה:**

**[הכנה ל-9]**
בדיקות ישברו HTML ו-send — תנו רמז למפגש הבא.

---


## ‏33 — תרגיל בית

[סטודנטים · 33]

**על המסך:**

1. Lab A: הוסיפו שדה `valid_until` ל-JSON והציגו ב-HTML  
2. Lab B: הוסיפו קריאה `WO-CLEAN` (ניקיון) עם severity=`open`  
3. תעדו ב-README איך משיגים `TELEGRAM_CHAT_ID`  
4. בונוס: כלי `render_markdown_report` → `out/report.md` באחד הדומיינים  

</div>

**להקראה:**

**[בית]**
ארבע משימות קצרות. בונוס ויזואלי ל-HITL.
**[סיום]**
תודה. במפגש 9 — Testing ו-Debugging Agents.

---


</div>
