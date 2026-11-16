# Data Models & Schema Specifications

## 1. Companies
- `id` (INTEGER, Primary Key)
- `name` (TEXT)
- `tally_guid` (TEXT, Unique)
- `books_from` (DATE)
- `last_sync_at` (TIMESTAMP)

## 2. Ledgers (Accounts, Customers, Vendors, Banks)
- `id` (INTEGER, Primary Key)
- `tally_guid` (TEXT, Unique)
- `company_name` (TEXT)
- `name` (TEXT)
- `parent_group` (TEXT) - e.g., 'Sundry Debtors', 'Sundry Creditors', 'Bank Accounts', 'Cash-in-hand', 'Sales Accounts', 'Indirect Expenses'
- `opening_balance` (DECIMAL)
- `closing_balance` (DECIMAL)
- `contact_person` (TEXT)
- `phone` (TEXT)
- `email` (TEXT)
- `gstin` (TEXT)
- `state` (TEXT)
- `updated_at` (TIMESTAMP)

## 3. Vouchers (Transactions)
- `id` (INTEGER, Primary Key)
- `tally_guid` (TEXT, Unique)
- `voucher_number` (TEXT)
- `voucher_type` (TEXT) - 'Sales', 'Purchase', 'Receipt', 'Payment', 'Journal', 'Contra'
- `date` (DATE)
- `party_ledger_name` (TEXT)
- `amount` (DECIMAL)
- `narration` (TEXT)
- `is_cancelled` (BOOLEAN)
- `created_at` (TIMESTAMP)

## 4. Voucher Items & Entries (Line Items)
- `id` (INTEGER, Primary Key)
- `voucher_id` (INTEGER, FK to Vouchers)
- `ledger_name` (TEXT)
- `amount` (DECIMAL) - Positive (Debit) / Negative (Credit)
- `item_name` (TEXT, Nullable)
- `quantity` (DECIMAL, Nullable)
- `rate` (DECIMAL, Nullable)

## 5. Bills Outstanding (Receivables & Payables Aging)
- `id` (INTEGER, Primary Key)
- `bill_type` (TEXT) - 'RECEIVABLE' or 'PAYABLE'
- `party_name` (TEXT)
- `bill_name` (TEXT) - Bill / Ref No.
- `bill_date` (DATE)
- `due_date` (DATE)
- `bill_amount` (DECIMAL)
- `pending_amount` (DECIMAL)
- `overdue_days` (INTEGER)
- `aging_bucket` (TEXT) - '0-30', '31-60', '61-90', '90+'

## 6. Sync Logs
- `id` (INTEGER, Primary Key)
- `status` (TEXT) - 'SUCCESS', 'FAILED', 'IN_PROGRESS'
- `records_synced` (INTEGER)
- `message` (TEXT)
- `timestamp` (TIMESTAMP)
