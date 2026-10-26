<div dir="rtl" lang="he" style="text-align: right; unicode-bidi: plaintext;">

# ‏דמו 08B — Atlas Facility (מעבר ל-Nimbus)

קריאות שירות לבניין → כרטיס HTML + שליחה לטלגרם.  
**לא** הצעות מחיר / הזמנות לקוח.

```bash
cd demos/08-facility-opening
cp .env.example .env   # או העתיקו מ-08-surface-opening
./run-claude.sh reset
./run-claude.sh hvac && ./send-telegram.sh
./run-claude.sh elev && ./send-telegram.sh
```

‏Lab המלא: [`labs/08-facility-surfaces/`](../../labs/08-facility-surfaces/)

</div>
