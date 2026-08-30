from pypdf import PdfReader

reader = PdfReader("01-digital-planners/planner_2026_6month_hyperlinked.pdf")
page = reader.pages[0]
annots = page["/Annots"]

# The dest array format is [page_index, /Fit, ...args]
# When pypdf writes add_annotation with target_page_index,
# it stores the target as a NumberObject (page index) instead of an IndirectRef to the page.
# Let's check if this works in practice - do the links resolve to actual pages?

annot = annots[0].get_object()
dest = annot.get("/Dest")
print(f"Dest: {dest}")
print(f"dest[0]: {dest[0]} (type: {type(dest[0])})")
print(f"dest[1]: {dest[1]} (type: {type(dest[1])})")

# Check all 9 links on page 0
for i, ref in enumerate(annots):
    annot = ref.get_object()
    if annot.get("/Subtype") != "/Link":
        continue
    dest = annot.get("/Dest")
    if dest and len(dest) > 0:
        target = dest[0]
        print(f"  Link {i}: target page index = {target}")

# Also check a tab link on page 5
print("\n--- Page 5 ---")
page5 = reader.pages[5]
if "/Annots" in page5:
    annots5 = page5["/Annots"]
    for i, ref in enumerate(annots5):
        annot = ref.get_object()
        if annot.get("/Subtype") != "/Link":
            continue
        dest = annot.get("/Dest")
        if dest and len(dest) > 0:
            target = dest[0]
            print(f"  Tab link {i}: target page index = {target}")
print(f"\nTotal pages: {len(reader.pages)}")

# The key question: Is the NumberObject a page index or needs to be an IndirectObject?
# In PDF spec, /Dest array should be [page_ref, /Fit, ...] where page_ref is an indirect reference
# But pypdf's add_annotation may store it differently.
# Let's check if the links actually work when opened.
