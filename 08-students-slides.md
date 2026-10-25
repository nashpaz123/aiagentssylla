<div dir="rtl" lang="he">

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="420" />
</p>

# ‏מפגש 8 — מצגת סטודנטים
## ‏סודות Cursor · Claude Code · Cloud · MCP

> ניהול קונטקסט, MCP (כולל Apify), קיצורי דרך, Chat מול Projects, Cloud Agents.  
> Lab קצר בסוף: משטח HTML + טלגרם (יישום, לא חזרה על מפגש 7).  
> תדריך מנהלים: [`08-exec-briefing.md`](08-exec-briefing.md)

---

# ‏חלק א׳ — מה מסתתר מאחורי המסך

_לא עוד "מה זה agent" — אלא איך שולטים במעטפת_

## ‏1 — כותרת

> פתיחה — Power features שמשנים את העבודה

<p align="center">
  <img src="assets/sprint-tech-academy-logo.png" alt="SPRINT Tech Academy" width="360" />
</p>

**‏Cursor · Claude Code · Cloud · MCP**  
הכלים שאתם כבר משתמשים בהם — עם הידיות הלא־גלויות

![Context stack](assets/08/01-context-stack.png)

---

## ‏2 — מילון למפגש

| מונח | הסבר |
|---|---|
| ‏**Context window** | כל מה שהמודל "רואה" בשיחה: הוראות, קבצים, כלים, תשובות |
| ‏**CLAUDE.md** | זיכרון פרויקט שאתם כותבים — נטען בכל סשן Claude Code |
| ‏**Auto memory** | הערות ש-Claude כותב לעצמו אחרי תיקונים שלכם |
| ‏**/compact · /context** | פקודות לניהול מילוי החלון (סיכום / בדיקה) |
| ‏**MCP** | פרוטוקול לחיבור כלים חיצוניים (Apify, DB, Slack…) |
| ‏**Apify** | ספריית Actors לגרידה/אוטומציה — מתחבר כ-MCP/plugin |
| ‏**Agent Chat** | שיחה מקומית/רגילה — משימה אחת, סגרו לפטופ = נעצר |
| ‏**Cloud Agent** | Agent על VM בענן — ממשיך בלי הלפטופ, מקביל |
| ‏**Project (Cursor)** | עבודה ארוכה עם **coordinator** + קונטקסט משותף + מנויים |
| ‏**Rules / Skills** | הוראות קבועות (`.cursor/rules`, skills, `/`) |

---

## ‏3 — הדגמת פתיחה — "מה ממלא את הקונטקסט?"

**ב-Claude Code** (בתיקיית הדמו):

```text
/context
```

רואים: `CLAUDE.md` · זיכרון · שמות כלי MCP · skills — **לפני** שהקלדתם משימה.

**ב-Cursor:** פתחו Agent Chat והצביעו על Rules / MCP ב-Customize — אותו רעיון: הקונטקסט לא ריק.

מסר: רוב "הקסם" הוא **מה שנטען אוטומטית**, לא רק הפרומפט שלכם.

---

## ‏4 — מה היום (בלי חזרה על מפגשים קודמים)

| נגלה היום | למה זה חדש |
|---|---|
| ניהול קונטקסט אמיתי | לא "יש זיכרון" — אלא `/context` / compact / rules |
| MCP + Apify | כלים מבחוץ, לא רק Read/Write בריפו |
| Chat · Cloud · Project | שלוש רמות עוצמה שונות |
| קיצורי דרך ו-`/` | עבודה מהירה כמו מקצוענים |
| Lab משטחים (קצר) | יישום: HTML + טלגרם — לא שיעור Sales Ops מחדש |

---

## ‏5 — שאלת המפגש

**שאלה:** מתי Chat מספיק, מתי Cloud, ומתי Project — ואיך מוסיפים כלי כמו Apify בלי לכתוב SDK?

| תוצר | "עובד" |
|---|---|
| `/context` מובן | יודעים מה תופס טוקנים |
| MCP מחובר | כלי חיצוני מופיע ב-Available Tools |
| הבחנת Chat / Cloud / Project | בחירה נכונה לתרחיש |
| Lab | כרטיס + הודעת טלגרם אמיתית |

---

# ‏חלק ב׳ — ניהול קונטקסט (הסוד מס׳ 1)

_החלון מתמלא — גם כשאתם לא שמים לב_

## ‏6 — מה נכנס לחלון לפני שאתם מקלידים

![Context stack](assets/08/01-context-stack.png)

| שכבה | דוגמה |
|---|---|
| הוראות פרויקט | `CLAUDE.md` · `.cursor/rules` · AGENTS.md |
| זיכרון | Auto memory (Claude) |
| קטלוג כלים | שמות MCP / skills (לא התוכן המלא עדיין) |
| אחר כך | קריאות קבצים, תשובות, תוצאות כלים |

---

## ‏7 — CLAUDE.md · Rules · Auto memory

| מנגנון | מי כותב | למה |
|---|---|---|
| `CLAUDE.md` | אתם | סטנדרטים, איך מריצים, מה אסור |
| `.claude/rules/` / `.cursor/rules` | אתם | כללים לפי נתיב/נושא |
| Auto memory | Claude | לומד מתיקונים שלכם |

טיפ: קצר ומדויק > מסמך ארוך שהמודל מתעלם ממנו.

```bash
# Claude Code — התחלה בריפו חדש
/init
/memory
```

---

## ‏8 — פקודות קונטקסט ב-Claude Code

| פקודה | מתי |
|---|---|
| `/context` | "למה זה איטי / יקר / מבולבל?" |
| `/compact` | השיחה ארוכה — סיכום מובנה, ממשיכים |
| `/clear` | משימה חדשה, בלי לגרור היסטוריה |
| `/btw` | שאלה בצד — **בלי** לזהם את הקונטקסט הראשי |
| Subagent / Task | מחקר כבד בחלון **נפרד** — חזרה רק סיכום |

---

## ‏9 — קונטקסט ב-Cursor (בלי להציף)

- `@file` / `@folder` — בחירה מכוונת, לא "תקרא הכל"  
- Rules בפרויקט — חוזרים בכל Agent  
- Notepads / Docs — הקשר יציב למשימות חוזרות  
- שיחה ארוכה מדי → Chat חדש + הפניה לכללים, לא עוד 40 הודעות  

---

## ‏10 — Subagents = קונטקסט נפרד

כש-Claude/Cursor מריצים subagent:

- הקבצים הגדולים נקראים **אצלו**  
- אליכם חוזר סיכום קצר  
- החלון הראשי נשאר פנוי למשימה  

זה הטריק: לא "עוד מודל" — אלא **בידוד קונטקסט**.

---

# ‏חלק ג׳ — כלים חיצוניים (MCP · Apify)

_הסוכן יוצא מהריפו_

## ‏11 — MCP במשפט אחד

![MCP bus](assets/08/03-mcp-tools.png)

**MCP** = אוטובוס כלים. Cursor ו-Claude Code מתחברים לשרתים שמציעים Tools / Resources / Prompts.

בלי MCP: רק קבצים וטרמינל מקומי.  
עם MCP: Apify, דאטהבייס, ברואוזר, Slack…

---

## ‏12 — חיבור Apify (דוגמה חיה)

**Claude Code:**

```text
/plugin install apify
/mcp          # Enable + Authenticate ל-plugin:apify:apify
```

**Cursor:** Customize → MCP → הוסיפו שרת (או מ-Marketplace) · אשרו OAuth אם נדרש.

פרומפט ראשון (בלי להריץ Actor יקר):

> מצא Actor טוב ל-Google Maps ב-Apify. הצג input, מחיר, ופורמט פלט — **אל תריץ עדיין**.

---

## ‏13 — כללים לכלי חיצוני

- [ ] אימות (OAuth/token) נפרד מקומי מול Cloud  
- [ ] אישור כלי לפני side-effect (גרידה / כתיבה)  
- [ ] לא לשים מפתחות ב-chat history / screenshots  
- [ ] Cloud Agents: MCP נפרד — צריך לחבר גם שם  

---

## ‏14 — הדגמה קצרה — כלי אחד שעובד

1. חברו Apify **או** MCP אחר שכבר יש לכם  
2. בקשו פעולת **קריאה בלבד**  
3. הראו בלוג/UI ששם הכלי הופיע  
4. כבו את השרת — ודאו שהסוכן מדווח שאין כלי (לא ממציא הצלחה)

---

# ‏חלק ד׳ — Chat · Cloud Agents · Projects

_שלוש רמות — לא אותו כפתור_

## ‏15 — Agent Chat (ברירת מחדל)

| מתאים | לא מתאים |
|---|---|
| תיקון קובץ / הסבר / PR קטן | מיגרציה של שבועיים |
| אתם ליד המקלדת | לפטופ סגור, CI בלילה |
| קונטקסט קצר | עשרות משימות מקבילות |

---

## ‏16 — Cloud Agents

![Chat vs Cloud vs Project](assets/08/02-chat-cloud-project.png)

- רצים על **VM בענן** (ריפו, deps, סודות, רשת)  
- אפשר רבים במקביל — הלפטופ לא חייב להיות פתוח  
- יכולים לבנות, לבדוק, לפתוח PR, להשתמש ב-MCP  
- Multi-repo: פרונט + בקאנד באותה משימה  

מתי: "תתקן CI ותפתח PR בזמן שאני בישיבה".

---

## ‏17 — Projects ב-Cursor

Project ≠ עוד Chat.

| רעיון | משמעות |
|---|---|
| Coordinator | מתכנן ומפצל — **לא** כותב את כל הקוד בעצמו |
| Agents פנימיים | מבצעים; אפשר להיכנס לכל אחד |
| Shared context | קבצים/לקחים שגדלים לאורך שבועות |
| Subscriptions | Slack / לוח זמנים / PRs — בלי שתפתחו צ׳אט |

זמין בתוכניות עם Cloud Agents (לא Free/Plus).

---

## ‏18 — מתי מה? (טבלת החלטה)

| תרחיש | בחירה |
|---|---|
| באג בקבץ אחד | **Chat** |
| PR + טסטים בזמן שאתם בחוץ | **Cloud Agent** |
| פיצ׳ר גדול / מיגרציה / ניטור חוזר | **Project** |
| גרידה חד־פעמית מ-Apify | Chat/Cloud + **MCP** |
| אותה הנחיה לכל הסטודנטים בקורס | Rules / `CLAUDE.md` |

---

## ‏19 — קיצורי דרך שחוסכים שיעור שלם

**Claude Code — הקלידו `/`:**

| | |
|---|---|
| `/plan` | תכנון לפני שינוי גדול |
| `/model` · `/effort` | מודל ועומק חשיבה |
| `/diff` · `/code-review` | לפני שיפולינג |
| `/permissions` | שערי אישור |
| `/resume` · `/rewind` | חזרה בזמן |

**Cursor:** Command Palette · פתיחת Agents Window · קיצורי Accept/Reject ל-diff · מעבר מהיר ל-MCP ב-Customize.

![Shortcuts](assets/08/04-shortcuts-map.png)

---

# ‏חלק ה׳ — Lab קצר (יישום, לא חזרה)

_אותם רעיונות → פלט למשתמש_

## ‏20 — למה בכלל Lab היום?

אחרי הכוח של המעטפת — מוודאים שיודעים **להוציא פלט**:

- כרטיס HTML בדפדפן  
- הודעת Telegram אמיתית לצ׳אט שלכם  

בחרו **מסלול אחד** בהקלטה (A או B). השני לשיעורי בית.

| מסלול | דומיין | תיקייה |
|---|---|---|
| A · Nimbus | הצעת מחיר | [`labs/08-agent-surfaces/`](labs/08-agent-surfaces/) |
| B · Atlas | קריאת שירות בבניין | [`labs/08-facility-surfaces/`](labs/08-facility-surfaces/) |

![Lab tools](assets/08/05-lab-tools.png)

---

## ‏21 — Lab — הרצה (דוגמה A)

```bash
cd labs/08-agent-surfaces
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # ANTHROPIC + TELEGRAM_*

python3 surface_claude.py reset
python3 surface_claude.py chat --lead L-SMB --message "הכן כרטיס ושלח לטלגרם שלי"
```

מסלול B: `facility_claude.py --wo WO-ELEV` ב-[`labs/08-facility-surfaces/`](labs/08-facility-surfaces/).

דמו Claude כתיבת קבצים: `demos/08-surface-opening/` או `demos/08-facility-opening/` + `./send-telegram.sh`.

---

## ‏22 — Lab — Debrief

- [ ] `/context` או Rules הוזכרו לפני ה-Lab (קונטקסט ≠ רק JSON)  
- [ ] הודעה הגיעה לטלגרם (`sent=true`)  
- [ ] HTML נפתח עם צבע לפי route/severity  
- [ ] יודעים להגיד אם המשימה הזו הייתה Chat / Cloud / Project  

---

## ‏23 — חיבור למפגש: MCP + משטח

רעיון בונוס (אם יש זמן):

1. Agent ב-Cursor עם MCP (למשל Apify קריאה בלבד)  
2. תוצאה → כתיבה ל-JSON קטן  
3. Lab/`notify` שולח סיכום לטלגרם  

מסר: **כלי חיצוני → קונטקסט → Surface**.

---

# ‏חלק ו׳ — סיכום

## ‏24 — Anti-Patterns (של מעטפות, לא של Sales)

| אנטי־דפוס | למה נשבר |
|---|---|
| שיחה אינסופית בלי `/compact` | קונטקסט מלא → טעויות + עלות |
| Project למשימת קובץ אחד | יקר ומסורבל |
| MCP בלי אימות ב-Cloud | "עובד אצלי" ≠ עובד בסוכן ענן |
| להאמין ל"שלחתי" בלי תוצאת כלי | נרטיב ≠ API |
| להעתיק מפתחות לצ׳אט | דליפה |

---

## ‏25 — סיכום

- קונטקסט מנוהל — לא "קורה מעצמו"  
- MCP (Apify וחברים) = ידיים מחוץ לריפו  
- Chat ≠ Cloud ≠ Project  
- `/` ו-Rules חוסכים שעות  
- Lab: פלט אנושי (HTML + טלגרם)  
- במפגש הבא: **Testing ו-Debugging Agents**

---

## ‏26 — הכנה למפגש 9

- איך בודקים ש-MCP באמת נקרא (לוג כלי)?  
- איך בודקים ש-send לטלגרם לא רץ בלי token?  
- רשמו 2 בדיקות שבירות לקונטקסט מלא מדי  

---

## ‏27 — תרגיל בית

1. הריצו `/context` (או הצגה מקבילה ב-Cursor) וצלמו/רשמו מה תופס הכי הרבה  
2. חברו MCP אחד (Apify מומלץ) ובצעו שאילתת קריאה בלבד  
3. כתבו ב-5 שורות: מתי הייתם בוחרים Project ולא Chat  
4. Lab: השלימו את המסלול שלא הרצתם בכיתה (A או B) · או הוסיפו `WO-CLEAN` / `valid_until`  

</div>
