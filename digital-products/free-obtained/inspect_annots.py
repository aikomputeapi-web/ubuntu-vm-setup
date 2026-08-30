from pypdf import PdfReader

reader = PdfReader("01-digital-planners/planner_2026_6month_hyperlinked.pdf")
page = reader.pages[0]
if "/Annots" in page:
    annots = page["/Annots"]
    for i, ref in enumerate(annots[:3]):
        annot = ref.get_object()
        print(f"Annot {i}:")
        print(f"  Subtype: {annot.get('/Subtype')}")
        print(f"  Rect: {annot.get('/Rect')}")
        dest = annot.get("/Dest")
        print(f"  Dest: {dest}")
        print(f"  Dest type: {type(dest)}")
        if dest and hasattr(dest, "keys"):
            print(f"  Dest keys: {list(dest.keys())}")
        action = annot.get("/A")
        print(f"  Action: {action}")
        print()
