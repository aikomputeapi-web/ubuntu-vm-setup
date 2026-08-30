import csv, os, sys
sys.stdout.reconfigure(encoding="utf-8")

base = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(os.path.dirname(base), "free-alternatives-research", "listings_free_alternatives.csv")

with open(csv_path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Listings 30-32 are the ones with free_equivalent = No
print("=== THE 3 MISSING LISTINGS ===\n")
for i, row in enumerate(rows):
    if row.get("free_equivalent") == "No":
        print(f"Listing #{i+1}:")
        print(f"  Title: {row['title']}")
        print(f"  Archetype: {row['archetype']}")
        print(f"  Verdict: {row['verdict']}")
        print(f"  DIY Difficulty: {row['diy_difficulty']}")
        print(f"  DIY Notes: {row['diy_notes']}")
        print(f"  Price: {row['price']}")
        print(f"  Shop: {row['shop']}")
        print(f"  Shop Sales: {row['shop_sales']}")
        print(f"  URL: {row['url']}")
        print()
