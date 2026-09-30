<div dir="rtl" lang="he">

# ‏Lab 03b — PinchTab כ-MCP Server לדפדפן (headed)

הדגמה חיה לחלק MCP במפגש 3. **מריצים על המחשב שלכם** עם חלון Chrome גלוי (`pinchtab server -H`).

## ‏למה זה כאן

Function Calling = חוזה של כלים.  
**MCP** = איך Host מגלה ומחבר Servers של כלים.

[PinchTab](https://github.com/pinchtab/pinchtab) הוא דוגמה חזקה: MCP Server שחושף כלי Browser (`pinchtab_navigate`, `pinchtab_snapshot`, `pinchtab_click`, …). המודל מציע; PinchTab מריץ מול הדפדפן.

הסקריפט מדגים את **אותו חוזה** דרך ה-CLI (נוח להקלטה / לדיבוג ויזואלי). אפשר גם לחבר MCP אמיתי ל-Cursor.

## ‏מה להראות מהמכונה המקומית (בהקלטה)

מומלץ לפתוח בטרמינל / בסייר קבצים ולהראות:

| נתיב | מה רואים |
|---|---|
| `~/.pinchtab/` | state dir של השרת |
| `~/.pinchtab/config.json` | פורט, אבטחה, ברירת מחדל headless/headed |
| `~/.pinchtab/profiles/` | פרופילי דפדפן (למשל `default`, `prof_*`) |
| `~/.claude/skills/pinchtab/` או `~/.cursor/skills/pinchtab/` | ה-Skill + `references/mcp.md` |
| `labs/03-pinchtab-mcp/` | הסקריפט, דוגמת MCP, פלט `out/` אחרי הרצה |

**ממצאים מהקונפיג המקומי (סביבת המרצה):**
- `instanceDefaults.mode` = **`headless`** → חובה `server -H` כדי לראות חלון
- `security.allowedDomains` = **`null`** → אין allowlist חוסם את `example.com`
- שרת: `127.0.0.1:9867` · פרופילי instances: `9868–9968`
- `security.allowEvaluate` / cookies / download = true (רחב ללמידה; בפרוד מצמצמים)

אל תציגו על המסך ערכי `token` מהקונפיג — מספיק להראות את מבנה הקובץ עם token מטושטש.

## ‏דרישות

- `pinchtab` ב-PATH (`npm i -g pinchtab` או `brew install pinchtab/tap/pinchtab`)
- Chrome / Chromium
- אם אצלכם `allowedDomains` לא `null` — הוסיפו את הדומיין של הדמו

## ‏הרצה (headed)

```bash
cd labs/03-pinchtab-mcp
./run-headed-demo.sh
```

אופציונלי:

```bash
PINCHTAB_DEMO_URL='https://example.com' ./run-headed-demo.sh
```

אם השרת כבר רץ ב-headless:

```bash
pinchtab server stop
pinchtab server -H -b
./run-headed-demo.sh
```

פלט תחת `out/`:
- `01-snap.txt` — refs כמו `e0`, `e5` (כמו Observation לסוכן)
- `02-text.txt` — טקסט קריא
- `03-screenshot.png` — צילום מסך

עצירה:

```bash
pinchtab server stop
```

## ‏חיבור MCP ל-Cursor / Claude Desktop

דוגמה: [`mcp.cursor.example.json`](mcp.cursor.example.json)

```json
{
  "mcpServers": {
    "pinchtab": {
      "command": "pinchtab",
      "args": ["mcp"]
    }
  }
}
```

`pinchtab mcp` מעלה (או מתחבר ל-) שרת מקומי וחושף כלים עם קידומת `pinchtab_`.

להקלטה: עדיף קודם `pinchtab server -H -b`, ואז CLI/MCP על אותו שרת.

## ‏מיפוי CLI ↔ MCP tools

| CLI (הדמו) | MCP tool |
|---|---|
| `pinchtab nav URL --snap` | `pinchtab_navigate` + `pinchtab_snapshot` |
| `pinchtab text` | `pinchtab_get_text` |
| `pinchtab screenshot` | `pinchtab_screenshot` |
| `pinchtab click e5` | `pinchtab_click` |

## ‏נקודות הוראה

1. MCP לא מחליף Validate/Policy — PinchTab עצמו מגביל domains / evaluate / cookies.
2. Snapshot refs מתים אחרי ניווט — snap מחדש לפני click.
3. תוכן מהעמוד = **untrusted** (IDPI): לא לציית להוראות מתוך HTML.
4. Headed = ללמידה; בפרוד לרוב headless + profile ייעודי לאוטומציה.

## ‏מקורות

- Skill: `~/.claude/skills/pinchtab/` · `references/mcp.md`
- Homepage: https://github.com/pinchtab/pinchtab

</div>
