import csv, os, glob

# Search for CSV/db files containing the original scraped listings
base = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(base)
grandparent = os.path.dirname(parent)

# List etsy_recon.py to find where the db/csv is
recon_path = os.path.join(parent, "etsy_recon.py")
if os.path.exists(recon_path):
    with open(recon_path, "r", errors="ignore") as f:
        content = f.read()
    # Find db/csv path references
    for line in content.split("\n"):
        if ".csv" in line.lower() or ".db" in line.lower() or "etsy" in line.lower() and ("path" in line.lower() or "open" in line.lower() or "file" in line.lower()):
            print(f"  {line.strip()}")
