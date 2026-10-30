# Electricity Billing & Revenue Assurance — Mini Audit

A small, **fictional learning project** for a graduate analyst portfolio. **Not affiliated with Meridian Energy**. All customer identifiers, bills and pricing rules are invented.

## Business question

Did the sample electricity invoices apply the correct per-kWh rate? If not, which customers may need a billing correction, and what is the overall revenue difference?

## Model assumptions / limitations

- Electricity usage is measured in kWh and billed at the applicable plan's flat rate.
- An invoice's price is chosen by `plan` and `invoice_month`. September and October have different prices to simulate a price update.
- All billed and expected amounts are **NZD, excluding GST**.
- This deliberately simplified model excludes fixed daily charges, discounts, GST, time-of-use rates and meter readings. It is **not a model of Meridian's actual pricing or New Zealand electricity regulations**.
- For money calculations in Python, prefer `decimal.Decimal`. For SQL, round to cents when reporting.
- Difference = **billed - expected**; negative = undercharge, positive = overcharge.

## Files

- `data/rates.csv` — sample plan prices for September and October 2026.
- `data/invoices.csv` — sample invoices, including deliberate exceptions to find.
- `load_to_sqlite.py` — ready-to-run helper that loads both CSVs into `billing_demo.sqlite`.
- `queries.sql` — starter query + SQL exercise prompts (complete these yourself).
- `audit.py` — Python task outline (complete this yourself).
- `output/` — save `audit_results.csv`, charts and reports here.

## Fast route: 2 hours (Excel + SQL)

1. **Excel (45–60 minutes):** Open both CSVs. Use lookup to match the plan/month rate to each invoice, calculate `expected_nzd`, `difference_nzd`, and `status`, filter mismatches, and make a summary with counts and totals.
2. **SQL (35–45 minutes):** Run `python load_to_sqlite.py`, then complete `queries.sql` in a SQLite editor (or VS Code SQLite extension). Use `JOIN`, `ROUND`, `CASE`, `GROUP BY`.
3. **Explain findings (15–20 minutes):** Write 3–5 sentences in English about any exceptions, their total impact and one improvement idea.

## Full route: 3–5 hours (plus Python & GitHub)

4. **Python (60–90 minutes):** Finish `audit.py` and export `output/audit_results.csv`.
5. **QA checks (15–25 minutes):** Confirm a valid invoice is labelled OK, an undercharge is negative, an overcharge is positive, and a price change uses the October rate.
6. **Portfolio (20–30 minutes):** Document how you tested it, add a screenshot of the Excel summary or a one-page results report, and push to GitHub. Never include real customer details.

## Self-check (only check after trying)

- Total invoices: **12**.
- **4** invoices have intentionally incorrect billed amounts.
- Deliberate exceptions: **INV004, INV005, INV008, INV011**.
- Undercharges total **NZD 5.00**, overcharges total **NZD 2.00**.
- Net billing difference (billed minus expected): **NZD -3.00**.
- The October rate increase would add **NZD 13.70** in total to the seven October sample invoices versus old rates, **holding October kWh constant**.

## Interview story (only say what you completed)

"I built a small fictional electricity billing audit using Excel, SQL and Python. I compared billed amounts against plan rates, investigated pricing exceptions and summarised the potential revenue impact. The exercise helped me understand pricing updates, reconciliation and data quality checks, which are central to this analyst role."
