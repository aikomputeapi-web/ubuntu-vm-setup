import csv, os, sys

# Fix Windows encoding
sys.stdout.reconfigure(encoding="utf-8")

base = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(os.path.dirname(base), "free-alternatives-research", "listings_free_alternatives.csv")

with open(csv_path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total listings: {len(rows)}")
print(f"Columns: {list(rows[0].keys())}")

# The verdict column tells us if a free equivalent was found
# Check verdicts
from collections import Counter
verdicts = Counter(row.get("verdict", "") for row in rows)
print(f"\nVerdict distribution: {dict(verdicts)}")

# Print all 137 titles with their verdict and free_equivalent
print("\n=== ALL 137 LISTINGS ===")
for i, row in enumerate(rows):
    title = row.get("title", "")[:70]
    verdict = row.get("verdict", "")[:30]
    free_eq = row.get("free_equivalent", "")[:60]
    print(f"  {i+1:3d}. [{verdict:30s}] {title}")
    if free_eq:
        print(f"       free_eq: {free_eq}")
