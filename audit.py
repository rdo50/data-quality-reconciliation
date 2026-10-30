
"""
Data Quality & Revenue Reconciliation Tool

Validates simulated electricity invoices against pricing
rules and identifies potential billing discrepancies.
"""

import csv
from pathlib import Path 
from decimal import Decimal

# Step 1: Load invoice and pricing data
folder = Path(__file__).resolve().parent

with open(folder / "data" / "invoices.csv", newline="") as file:
    invoices = list(csv.DictReader(file))

with open(folder / "data" / "rates.csv", newline="") as file:
    rates = list(csv.DictReader(file))

# Check that both datasets have loaded successfully
print("Invoices:", len(invoices))
print("Rates:", len(rates))
print("First invoice:", invoices[0])



# Step 2: Match invoices with pricing rules

# Create a lookup table using plan and month
rate_lookup = {}

for rate in rates:
    key = (rate["plan"], rate["effective_from"])
    rate_lookup[key] = Decimal(rate["rate_per_kwh_nzd"])

# Find the correct rate for each invoice
matched = 0

for invoice in invoices:
    key = (invoice["plan"], invoice["invoice_month"])
    rate = rate_lookup.get(key)

    if rate is None:
        print("Missing rate:", invoice["invoice_id"])
    else:
        invoice["rate_per_kwh"] = rate
        matched += 1

print("Matched invoices:", matched)
print("First invoice rate:", invoices[0].get("rate_per_kwh"))



# Step 3: Calculate expected charges and billing differences

for invoice in invoices:
    if "rate_per_kwh" not in invoice:
        continue

    usage = Decimal(invoice["usage_kwh"])
    billed = Decimal(invoice["billed_nzd"])
    rate = invoice["rate_per_kwh"]

    expected = (usage * rate).quantize(Decimal("0.01"))
    difference = billed - expected

    if difference < 0:
        status = "UNDERCHARGED"
    elif difference > 0:
        status = "OVERCHARGED"
    else:
        status = "OK"

    invoice["expected_nzd"] = expected
    invoice["difference_nzd"] = difference
    invoice["status"] = status

    print(
        invoice["invoice_id"],
        "Expected:", expected,
        "Billed:", billed,
        "Difference:", difference,
        "Status:", status
    )



# Step 4: Export reconciliation results

output_file = folder / "output" / "audit_results.csv"
output_file.parent.mkdir(exist_ok=True)

fields = [
    "invoice_id",
    "invoice_month",
    "customer_id",
    "plan",
    "usage_kwh",
    "rate_per_kwh",
    "expected_nzd",
    "billed_nzd",
    "difference_nzd",
    "status"
]

with open(output_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    for invoice in invoices:
        writer.writerow({
            field: invoice.get(field, "")
            for field in fields
        })

# Summarise billing discrepancies
exceptions = [
    invoice for invoice in invoices
    if invoice.get("status") not in ("OK", None)
]

undercharged = sum(
    (-invoice["difference_nzd"]
     for invoice in exceptions
     if invoice["status"] == "UNDERCHARGED"),
    Decimal("0.00")
)

overcharged = sum(
    (invoice["difference_nzd"]
     for invoice in exceptions
     if invoice["status"] == "OVERCHARGED"),
    Decimal("0.00")
)

print("\n--- Reconciliation Summary ---")
print("Total invoices:", len(invoices))
print("Exceptions:", len(exceptions))
print("Total undercharged: $", undercharged)
print("Total overcharged: $", overcharged)
print("Net difference: $", overcharged - undercharged)
print("Results saved to:", output_file)



# Step 5: Validate results against the sample dataset

assert matched == len(invoices), "Some invoices have no matching rate"
assert len(exceptions) == 4, "Unexpected number of exceptions"
assert undercharged == Decimal("5.00"), "Undercharge total mismatch"
assert overcharged == Decimal("2.00"), "Overcharge total mismatch"

print("Sample data validation checks passed.")
