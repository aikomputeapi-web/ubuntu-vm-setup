"""
Verify planner links work using PyMuPDF (fitz), which resolves links
the same way a real PDF viewer does.
"""
import fitz  # PyMuPDF
import os

BASE = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(BASE, "01-digital-planners", "planner_2026_6month_hyperlinked.pdf")
doc = fitz.open(pdf_path)

total_pages = len(doc)
total_links = 0
valid_internal = 0
invalid_internal = 0
external_links = 0
target_pages = set()

for page_idx in range(total_pages):
    page = doc[page_idx]
    links = page.get_links()
    for link in links:
        total_links += 1
        kind = link.get("kind")
        if kind == fitz.LINK_GOTO:
            target = link.get("page")
            if target is not None and 0 <= target < total_pages:
                valid_internal += 1
                target_pages.add(target)
            else:
                invalid_internal += 1
                if invalid_internal <= 5:
                    print(f"  INVALID: page {page_idx} -> target {target}")
        elif kind == fitz.LINK_URI:
            external_links += 1

print(f"Total pages: {total_pages}")
print(f"Total links: {total_links}")
print(f"Valid internal links (GOTO): {valid_internal}")
print(f"Invalid internal links: {invalid_internal}")
print(f"External links: {external_links}")
print(f"Unique target pages: {len(target_pages)}")
print(f"Target pages: {sorted(target_pages)}")

# Verify the links point to the correct sections
# Index should be page 0, months=1, weekly=2, daily=7, notes=219
expected = {0: "index", 1: "months", 2: "weekly", 7: "daily", 219: "notes"}
print("\nExpected section targets:")
for pg, name in expected.items():
    found = pg in target_pages
    print(f"  {name} (page {pg}): {'FOUND' if found else 'MISSING'}")

if invalid_internal == 0 and valid_internal > 1000:
    print("\n[EVIDENCE PASS] All planner links resolve to valid pages")
else:
    print(f"\n[EVIDENCE FAIL] {invalid_internal} links have invalid targets")

doc.close()
