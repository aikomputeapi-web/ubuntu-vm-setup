import os, re, sys
from pypdf import PdfReader

BASE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(BASE, "04-coloring-pages", "Free_Coloring_Pages_Bundle.pdf")
print(f"Path: {p}")
print(f"Exists: {os.path.exists(p)}")

reader = PdfReader(p)
total = len(reader.pages)
print(f"Pages: {total}")

blank = 0
low = 0
for i, page in enumerate(reader.pages):
    content = page.get_contents()
    if content:
        try:
            data = content.get_data()
            text = data.decode("latin-1", errors="ignore") if isinstance(data, bytes) else str(data)
            moveto = len(re.findall(r' m[\n\s]', text))
            lineto = len(re.findall(r' l[\n\s]', text))
            curveto = len(re.findall(r' c[\n\s]', text))
            rect = len(re.findall(r' re[\n\s]', text))
            total_ops = moveto + lineto + curveto + rect
            if total_ops < 5:
                blank += 1
                if i < 5:
                    print(f"  Page {i+1}: BLANK ({total_ops} ops)")
            elif total_ops < 20:
                low += 1
                if i < 5:
                    print(f"  Page {i+1}: Low ({total_ops} ops)")
            else:
                if i < 5:
                    print(f"  Page {i+1}: OK ({total_ops} ops)")
        except Exception as e:
            print(f"  Page {i+1}: EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            blank += 1
    else:
        print(f"  Page {i+1}: No content")
        blank += 1

print(f"\nBlank: {blank}, Low: {low}")
