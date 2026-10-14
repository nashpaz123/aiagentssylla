Work ONLY in this folder. Use the `support` subagent (or act as support if Task is unavailable).

Customer **C-99** says: "מה הסטטוס של הבקשה שלי?"

1. Read `out/store.json` (and only that for memory).
2. If C-99 is missing → say in Hebrew you have no memory / ask them to open a new request.
3. If present → answer in Hebrew with amount, route, and status from the file.

Do not invent a profile. Do not modify policy.md.
