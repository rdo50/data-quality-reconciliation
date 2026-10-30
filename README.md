
# Data Quality & Revenue Reconciliation Tool

## Overview

A Python-based practice project that checks simulated
electricity invoices against pricing rules and identifies
billing discrepancies.

The project focuses on data quality, business rule
validation, financial reconciliation and reporting.

## Technologies

- Python 3
- CSV data processing
- Decimal for financial calculations

## Business Problem

How can billing records be checked against applicable
pricing rules to identify incorrect charges and
potential revenue impacts?

## Features

- Load invoice and pricing datasets from CSV files
- Match pricing rules by plan and invoice month
- Calculate expected charges
- Identify undercharged and overcharged invoices
- Export reconciliation results to CSV
- Perform sample-specific validation checks

## Results

Analysed 12 simulated invoices and identified
4 billing discrepancies.

| Metric | Result |
|---|---:|
| Total invoices | 12 |
| Correct invoices | 8 |
| Billing exceptions | 4 |
| Total undercharged | NZ$5.00 |
| Total overcharged | NZ$2.00 |
| Net difference | -NZ$3.00 |

Reporting undercharges and overcharges separately
provides a clearer picture of billing accuracy than
relying on the net difference alone.

## How to Run

Requires Python 3. No external packages are needed.

```bash
python audit.py
```

The reconciliation results are exported to:

`output/audit_results.csv`

## Project Structure

- `audit.py` — Python reconciliation script
- `data/invoices.csv` — Simulated billing records
- `data/rates.csv` — Simulated pricing rules
- `output/audit_results.csv` — Generated results

## Assumptions and Limitations

- All data is fictional.
- Pricing follows a simplified per-kWh model.
- GST, fixed charges and discounts are excluded.
- Pricing is matched using plan and invoice month.
- Validation assertions apply to the sample dataset.
- This is a learning project, not a production system.

## Future Improvements

- Add SQL-based reconciliation
- Improve missing-data and error handling
- Introduce automated unit tests
- Visualise findings using Power BI
