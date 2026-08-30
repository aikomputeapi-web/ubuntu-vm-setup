import sqlite3, os, json

base = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(base)
db_path = os.path.join(parent, "etsy.db")

if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
    # Try etsy_recon dir
    alt_path = os.path.join(parent, "etsy-scraper", "etsy.db")
    if os.path.exists(alt_path):
        db_path = alt_path
    else:
        # Search for it
        import glob
        results = glob.glob(os.path.join(parent, "**", "etsy.db"), recursive=True)
        print(f"Search results: {results}")
        if results:
            db_path = results[0]

print(f"Using DB: {db_path}")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# List tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print(f"Tables: {tables}")

for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    print(f"\nTable {table}: {count} rows")
    cur.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cur.fetchall()]
    print(f"  Columns: {cols}")

# Get all listings
for table in tables:
    cur.execute(f"SELECT * FROM {table} LIMIT 5")
    rows = cur.fetchall()
    print(f"\n--- Sample from {table} ---")
    for row in rows:
        print(f"  {row[:5]}...")  # First 5 fields

conn.close()
