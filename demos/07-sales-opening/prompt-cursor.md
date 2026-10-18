# Cursor — הדגמת פתיחה מפגש 7 (Sales Ops)

פתחו את `demos/07-sales-opening/` בצ׳אט Agent והדביקו שלב־שלב.

## Turn A — SMB (צפוי auto)

```
קרא policy.md ואת L-SMB מ-crm/leads.json.
צור הצעת מחיר ב-out/quotes.json לפי המדיניות (הנחה 5% → auto).
עדכן stage של L-SMB, כתוב טיוטת מייל בעברית ל-out/email_draft.md (אל תשלח).
סכם בעברית עם המספרים.
```

## Turn B — Enterprise (צפוי HITL)

```
טפל ב-L-ENT בלי למחוק את L-SMB מה-quotes.
הנחה 18% → pending_manager. עדכן CRM + quotes. טיוטה שמציינת שממתינים למנהל.
```

## Turn C — בלי מייל (blocked)

```
טפל ב-L-NOMAIL. אסור להמציא מייל. route=blocked / need_email.
```
