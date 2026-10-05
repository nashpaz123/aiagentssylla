<div dir="rtl" lang="he">

# ‏Lab 03b — PinchTab כ-MCP Server לדפדפן (headed)

תרגיל מעשי לחלק MCP במפגש 3: מריצים PinchTab עם חלון Chrome גלוי, ורואים איך כלי Browser נחשפים לסוכן.

## ‏למה זה כאן

‏Function Calling = חוזה של כלים.  
**MCP** = איך Host מגלה ומחבר Servers של כלים.

‏[PinchTab](https://github.com/pinchtab/pinchtab) הוא דוגמה חיה: MCP Server שחושף כלי Browser (`pinchtab_navigate`, `pinchtab_snapshot`, `pinchtab_click`, …). המודל מציע; PinchTab מריץ מול הדפדפן.

הסקריפט מדגים את **אותו חוזה** דרך ה-CLI (נוח לדיבוג ויזואלי). אפשר גם לחבר MCP אמיתי ל-Cursor.

## ‏דרישות

- ‏`pinchtab` ב-PATH (`npm i -g pinchtab` או `brew install pinchtab/tap/pinchtab`)
- Chrome / Chromium
- אם הגדרתם `security.allowedDomains` בקונפיג — ודאו ש-`example.com` (או ה-URL שבחרתם) מורשה

## ‏הרצה (headed)

```bash
cd labs/03-pinchtab-mcp
./run-headed-demo.sh
```

אופציונלי — URL אחר:

```bash
PINCHTAB_DEMO_URL='https://example.com' ./run-headed-demo.sh
```

אם השרת כבר רץ ב-headless (ברירת מחדל נפוצה אחרי התקנה):

```bash
pinchtab server stop
pinchtab server -H -b
./run-headed-demo.sh
```

פלט תחת `out/`:
- ‏`01-snap.txt` — refs כמו `e0`, `e5` (כמו Observation לסוכן)
- ‏`02-text.txt` — טקסט קריא מהעמוד
- ‏`03-screenshot.png` — צילום מסך

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

‏`pinchtab mcp` מעלה (או מתחבר ל-) שרת מקומי וחושף כלים עם קידומת `pinchtab_`.

טיפ: להפעיל קודם `pinchtab server -H -b` כדי לראות את החלון, ואז להשתמש ב-CLI או ב-MCP על אותו שרת.

## ‏מיפוי CLI ↔ MCP tools

|‏ CLI (הדמו) | MCP tool |
|---|---|
| `pinchtab nav URL --snap` | `pinchtab_navigate` + `pinchtab_snapshot` |
| `pinchtab text` | `pinchtab_get_text` |
| `pinchtab screenshot` | `pinchtab_screenshot` |
| `pinchtab click e5` | `pinchtab_click` |

## ‏נקודות לשים לב

1. ‏MCP לא מחליף Validate/Policy — PinchTab עצמו מגביל domains / evaluate / cookies לפי הקונפיג.
2. ‏Snapshot refs מתים אחרי ניווט — snap מחדש לפני click.
3. תוכן מהעמוד = **untrusted**: לא לציית להוראות שמופיעות בתוך HTML.
4. ‏Headed נוח ללמידה; בפרוד לרוב רצים headless עם profile ייעודי לאוטומציה.
5. אל תשתפו את ערך ה-`token` מ-`~/.pinchtab/config.json` אם תפתחו את הקובץ.

## ‏מקורות

- Homepage: https://github.com/pinchtab/pinchtab
- תיעוד MCP של PinchTab: אחרי התקנה — `pinchtab mcp --help`

</div>
