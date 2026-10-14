# Cursor variant — paste into Agent chat with this folder open

You are demonstrating Session 6 Memory (Store file = long-term memory).

## Turn A (new refund 99)
Customer C-99: "אני רוצה החזר על 99 שקל."
Read policy.md. Write/update out/store.json. Reply in Hebrew. route must be auto.

## Turn B (status) — new Agent chat OR continue
Customer C-99: "מה הסטטוס של הבקשה שלי?"
Read out/store.json only. Quote amount/route/status. If file empty → no memory.

## Turn C (new refund 101)
Customer C-101: "אני רוצה החזר על 101 שקל."
Update store without deleting C-99. route must be hitl / pending_human.

Optional: delete C-99 from store and re-ask status → must say no memory.
