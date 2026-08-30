import os, glob, xml.etree.ElementTree as ET

base = os.path.dirname(os.path.abspath(__file__))
svgs = glob.glob(os.path.join(base, "*.svg"))
md = glob.glob(os.path.join(base, "*.md"))
print(f"SVGs: {len(svgs)}, MDs: {len(md)}")
ok = 0
err = 0
for f in sorted(svgs):
    try:
        tree = ET.parse(f)
        root = tree.getroot()
        vb = root.get("viewBox")
        elems = list(root.iter())
        size = os.path.getsize(f)
        print(f"  {os.path.basename(f)}: {size}B, viewBox={vb}, elements={len(elems)}")
        ok += 1
    except Exception as e:
        print(f"  {os.path.basename(f)}: ERROR {e}")
        err += 1
print(f"Valid: {ok}, Errors: {err}")
for f in md:
    size = os.path.getsize(f)
    lines = open(f, "r", errors="ignore").read().count("\n")
    print(f"  {os.path.basename(f)}: {size}B, {lines} lines")
