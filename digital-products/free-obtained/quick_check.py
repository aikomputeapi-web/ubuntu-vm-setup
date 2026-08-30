"""Quick check: planner link count and coloring page content."""
from pypdf import PdfReader

# Planner links
print("=== PLANNER LINKS ===")
reader = PdfReader("01-digital-planners/planner_2026_6month_hyperlinked.pdf")
total_links = 0
pages_with_links = 0
for i in range(len(reader.pages)):
    page = reader.pages[i]
    count = 0
    if "/Annots" in page:
        annots = page["/Annots"]
        if annots:
            for annot_ref in annots:
                try:
                    annot = annot_ref.get_object()
                    if annot.get("/Subtype") == "/Link":
                        count += 1
                        total_links += 1
                except:
                    pass
            if count > 0:
                pages_with_links += 1
                if i < 5:
                    print(f"  Page {i}: {count} links")
print(f"Total: {total_links} links on {pages_with_links} of {len(reader.pages)} pages")

# Coloring page content check
print("\n=== COLORING PAGE CONTENT ===")
reader2 = PdfReader("04-coloring-pages/Free_Coloring_Pages_Bundle.pdf")
for page_idx in [0, 10, 25, 49]:
    page = reader2.pages[page_idx]
    content = page.get_contents()
    data = content.get_data()
    text = data.decode("latin-1", errors="ignore") if isinstance(data, bytes) else str(data)
    # Count PDF drawing operators
    moveto = text.count(" m\n") + text.count(" m ")
    lineto = text.count(" l\n") + text.count(" l ")
    curveto = text.count(" c\n") + text.count(" c ")
    rect = text.count(" re\n") + text.count(" re ")
    circle = text.count(" re f")  # rectangle fill
    total_ops = moveto + lineto + curveto + rect
    print(f"  Page {page_idx+1}: m={moveto}, l={lineto}, c={curveto}, re={rect}, total_draw_ops={total_ops}, content_len={len(text)}")
