<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 8 — מצגת סטודנטים
## ‏Cursor · Claude Code · משטחי פלט (UI / Telegram)

> **משך משוער:** ~2.5–3.5 שעות (מילון + הדגמות חיות + Lab + Surfaces).  
> בלי Copilot — רק **Cursor** ו-**Claude Code** + Lab עם `ANTHROPIC_API_KEY`.  
> דגש: פלט **יפה** למשתמש (HTML בדפדפן · הודעת Telegram) — לא רק לוג בטרמינל.  
> תדריך מנהלים: [`08-exec-briefing.md`](08-exec-briefing.md)

---

# ‏חלק א׳ — פתיחה והדגמה

_מאיפה המשתמש רואה את הסוכן?_

## ‏1 — כותרת

> פתיחה — Coding agents + Surfaces

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="360" />
</p>

**‏Cursor · Claude Code · משטחי פלט**  
מעטפות שמריצות agents — ו-runtime שמוציא כרטיס HTML / הודעת טלגרם

![Coding agents + surfaces](assets/08/01-coding-agents-surfaces.png)

---

## ‏2 — מילון למפגש

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

---

## ‏3 — הדגמת פתיחה — HTML + טיוטת Telegram

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

---

## ‏4 — מה ראינו — פירוק

| מה ראינו | מושג |
|---|---|
| כרטיס בדפדפן | Surface / UI |
| SMB ירוק · ENT ענבר | אותו pipeline, מסר לפי route |
| `telegram.txt` בלי שליחה | Draft ≠ Send |
| Claude Code הרצה agent שכתב קבצים | מעטפת CLI + coding agent |

---

## ‏5 — מה היום (+ חזרה)

| נבנה היום | כבר למדנו |
|---|---|
| Cursor מול Claude Code כמעטפות | מפגש 5–7: demos עם Claude Code |
| HTML + Telegram כמשטחים | מפגש 3: כלים / observations |
| Lab שולח (אופציונלי) לטלגרם | מפגש 7: Draft ≠ Send למייל |
| כללי סודות לבוט | מפגש 6: לא לשמור סודות ב-Store |

יעד: **~2.5–3.5 שעות**, הרבה הדגמות חיות.

---

## ‏6 — שאלת המפגש + תוצרים

**שאלה:** איפה המשתמש רואה את תוצר הסוכן — ומה אסור שיישלח בלי שער?

| תוצר | "עובד" |
|---|---|
| כרטיס HTML | נפתח בדפדפן, מספרים נכונים |
| טיוטת TG | קובץ לפני שליחה |
| שליחה (אופציונלי) | רק עם env + בקשה מפורשת |
| הבחנה מעטפת IDE / מעטפת CLI / runtime | יודעים מתי מה |

---

# ‏חלק ב׳ — מעטפות שמריצות Agents

_Cursor ו-Claude Code ≠ הכלים; הם מריצים את ה-agent_

## ‏7 — למה לא Copilot במפגש הזה

הסילבוס מזכיר Copilot — **בהקלטה שלנו:** Cursor + Claude Code כמעטפות בלבד.

| שכבה | מה זה באמת | תפקיד אצלנו |
|---|---|---|
| Cursor | מעטפת IDE | מריצה Agent שעורכת ריפו / UI |
| Claude Code | מעטפת CLI | מריצה Agent בהדגמות `claude -p` |
| Anthropic API | מודל + tool-use | Runtime agent ב-Lab |
| Tools | Read/Write/`send_telegram`… | הפעולות שה-agent קורא להן |

![Cursor vs Claude](assets/08/04-cursor-vs-claude.png)

---

## ‏8 — Cursor כמעטפת (IDE host)

- אתם פותחים צ׳אט **Agent** — Cursor מריץ את ה-agent  
- Diff לפני Accept — האדם בשער  
- Rules (`.cursor/rules`) מגבילים/מכוונים את ה-agent  
- מתאים לשיפור CSS/HTML של הכרטיס  

הדגמה קצרה: פתחו `prompt-cursor.md` ב-Cursor ושפרו מרווחים ב-`briefing.html` **בלי** לשנות מספרים.

---

## ‏9 — Claude Code כמעטפת (CLI host)

```bash
claude -p "$(cat prompt-smb.md)" \
  --setting-sources project,local \
  --allowedTools "Read,Write,Edit,Glob,Grep,Task"
```

- `claude` = מעטפת; ה-agent בפנים משתמש ב-Tools ברשימה  
- `run-claude.sh` = חזרתיות להקלטה  
- subagent `surface` ב-`.claude/agents/` — עדיין בתוך אותה מעטפת  
- stream-json + filter — רואים קריאות כלי (Write) בזמן אמת  

---

## ‏10 — Coding agent ≠ Runtime agent

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

## ‏11 — מה זה Surface ולמה אכפת

טרמינל טוב למפתחים. AE ומנהל רוצים:

- כרטיס ויזואלי (HTML)  
- דחיפה לנייד (Telegram)  

![Quote to surface](assets/08/02-quote-to-surface.png)

---

## ‏12 — Pipeline: Quote → HTML → TG → Send?

1. `get_quote`  
2. `render_html_card` → `out/briefing.html`  
3. `render_telegram_message` → `out/telegram.txt`  
4. `send_telegram` — **רק** אם ביקשו + יש token  

---

## ‏13 — HTML card — עקרונות

- קובץ יחיד · CSS פנימי · `dir="rtl"`  
- צבע לפי `route` (auto/hitl/blocked)  
- כותרת + טבלה + פוטר "טיוטה פנימית"  
- מספרים **רק** מה-JSON  

---

## ‏14 — Telegram כמשטח

![Telegram surface](assets/08/03-telegram-surface.png)

| רכיב | תפקיד |
|---|---|
| Bot token | זהות הבוט (סוד) |
| Chat ID | לאן שולחים |
| `sendMessage` | Side-effect ברשת |

בלי env → הכלי מחזיר שגיאה ברורה — **לא** `sent=true` מזויף.

---

## ‏15 — Draft ≠ Send (חוזר ממפגש 7)

| כלי | רשת? |
|---|---|
| `render_telegram_message` | לא |
| `send_telegram` | כן |

אותו עיקרון כמו טיוטת מייל במפגש 7 — ערוץ אחר.

---

## ‏16 — סודות והגדרות

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export TELEGRAM_BOT_TOKEN=123:ABC...   # אופציונלי
export TELEGRAM_CHAT_ID=...            # אופציונלי
```

- לא בקוד · לא ב-git · לא בצילום מסך  
- Chat ID: `getUpdates` אחרי הודעה לבוט  

---

## ‏17 — Guardrails למשטחים

- [ ] מספרים מכלי/JSON בלבד  
- [ ] HTML לא מריץ JS חיצוני לא מבוקר בדמו  
- [ ] אין שליחה בלי בקשה מפורשת  
- [ ] אין token בלוגים  
- [ ] PII — לא לצ׳אט ציבורי  

---

## ‏18 — Anti-Patterns

| אנטי־דפוס | למה נשבר |
|---|---|
| "הסוכן ידפיס יפה בטרמינל" | המשתמש לא שם |
| שליחה אוטומטית לכל render | ספאם / דליפה |
| Token ב-repo | פריצה |
| HTML עם מספרים מהפרומפט | מחיר ישן/בדוי |
| לערבב Copilot כחובה | לא במסלול שלנו |

---

## ‏19 — Checklist לפני פיילוט Surface

- [ ] יש קובץ draft לפני send  
- [ ] יש HTML שנפתח בלי שרת  
- [ ] יש הפרדת Coding / Runtime  
- [ ] יש env מתועד לטלגרם  
- [ ] יש תרחיש SMB מול ENT ויזואלית  

---

# ‏חלק ד׳ — Lab

_הרבה הרצות — רואים כרטיס וטלגרם_

## ‏20 — Lab — מטרה

תיקייה: [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/)

דורש **`ANTHROPIC_API_KEY`**.  
טלגרם אמיתי: `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`.

![Lab tools](assets/08/05-lab-tools.png)

לידים: `L-SMB` · `L-ENT` · `L-UPSELL`

---

## ‏21 — Lab — מה נריץ

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

---

## ‏22 — Lab — Debrief

- [ ] ראיתי כרטיס ירוק ל-SMB וענבר ל-ENT  
- [ ] `telegram.txt` נוצר לפני שליחה  
- [ ] בלי token — שגיאה מפורשת, לא הצלחה מזויפת  
- [ ] עם token — הודעה בנייד + `TOOL -> send_telegram`  
- [ ] Upsell מסומן בכרטיס/טיוטה  

---

# ‏חלק ה׳ — הדגמות נוספות וסיכום

## ‏23 — הדגמה — Cursor משפר UI

1. פתחו `out/briefing.html` אחרי Lab  
2. ב-Cursor: "שפר טיפוגרפיה ומרווחים בלי לשנות מספרים"  
3. רעננו בדפדפן  

מסר: מעטפת Cursor מריצה coding agent שמשפר Surface; ה-runtime agent מזין נתונים.

---

## ‏24 — הדגמה — כפתורים שמשנים פלט

| שינוי | תוצאה ויזואלית |
|---|---|
| `L-SMB` | ירוק / approved |
| `L-ENT` | ענבר / pending_manager |
| `L-UPSELL` | ירוק + תווית upsell |
| בקשת send בלי env | error בלוג |
| בקשת send עם env | הודעה בטלגרם |

---

## ‏25 — באג: "נשלח" בלי token

סימפטום: המודל כותב "שלחתי לטלגרם" אבל אין הודעה.  
בדיקה: אין `TOOL -> send_telegram` או הכלי החזיר `missing_telegram_env`.  
תיקון: האמת בתוצאת הכלי בלבד; הפרומפט אוסר להצהיר sent בלי `sent=true`.

---

## ‏26 — Design Review — "נשלח כל הצעה לטלגרם של הלקוח"

| שאלה | החלטה |
|---|---|
| למי הצ׳אט? | פנימי ל-AE/מנהל קודם |
| מתי send? | אחרי render + אישור |
| מה בתוכן? | בלי PII מיותר |
| Audit? | לוג HTTP + lead_id |

---

## ‏27 — ROI קצר למשטחים

| למי | ערך |
|---|---|
| AE | כרטיס מוכן + התראה בנייד |
| מנהל | רואה HITL בלי לפתוח CRM |
| מפתח | אותו סוכן — ערוצים שונים |

---

## ‏28 — סיכום

- Cursor / Claude Code = **מעטפות** שמריצות agents (לא "הכלים")  
- Surface = HTML / Telegram / UI  
- Coding agent ≠ Runtime agent  
- Draft ≠ Send  
- Lab: כרטיס + טיוטה + שליחה אופציונלית  
- במפגש הבא: **Testing ו-Debugging Agents**

---

## ‏29 — הכנה למפגש 9

- חשבו: איך בודקים ש-HTML מכיל את הסכום הנכון?  
- איך בודקים ש-send לא רץ בלי token?  
- רשמו 2 בדיקות שבירות שתרצו לראות בלוג  

---

## ‏30 — תרגיל בית

1. הוסיפו שדה `valid_until` ל-JSON והציגו ב-HTML  
2. הוסיפו כלי `render_markdown_report` לקובץ `out/report.md`  
3. תעדו ב-README איך משיגים `TELEGRAM_CHAT_ID`  
4. בונוס: כפתור CSS ל-HITL שמציג "ממתין למנהל" בגדול  

</div>
