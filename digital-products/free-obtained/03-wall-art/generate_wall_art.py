"""
Generate printable wall art (PDF) with various aesthetic styles.
Creates high-quality abstract, botanical, and minimalist prints
that match or exceed the quality of Etsy wall art listings.

These are original CC0 designs - free to use, sell, or modify.
Requires: reportlab, PIL (Pillow)
"""

import os
import math
import random
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, Color
from PIL import Image, ImageDraw, ImageFilter
import io

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_OUTPUT = os.path.join(OUTPUT_DIR, "Wall_Art_Collection.pdf")
PNG_DIR = os.path.join(OUTPUT_DIR, "wall-art-png")
os.makedirs(PNG_DIR, exist_ok=True)

# Print ratios (standard frame sizes)
RATIOS = {
    "2x3": (2, 3),     # 4x6, 8x12, 16x24
    "3x4": (3, 4),     # 6x8, 9x12, 12x16
    "4x5": (4, 5),     # 8x10, 16x20
    "ISO": (1, 1.414), # A4, A3 (sqrt(2))
    "Square": (1, 1),  # 8x8, 12x12
}

# Color palettes (trending in 2025-2026 wall art)
# Stored as RGB tuples for PIL compatibility
def hex_to_rgb(h):
    """Convert HexColor to RGB tuple."""
    if hasattr(h, 'red'):
        return (int(h.red * 255), int(h.green * 255), int(h.blue * 255))
    if isinstance(h, (tuple, list)):
        return tuple(h)
    return h

PALETTES = {
    "Japandi": [hex_to_rgb(HexColor(c)) for c in ["#2D2D2D", "#7A6F5D", "#C4B998", "#E8E2D5", "#F5F2ED"]],
    "Cottagecore": [hex_to_rgb(HexColor(c)) for c in ["#6B8E6B", "#A8C4A2", "#DBC5A0", "#E8D5B7", "#F5EDE0"]],
    "Coastal": [hex_to_rgb(HexColor(c)) for c in ["#3A6B8C", "#6BA8B5", "#A8D5BA", "#D4E4E8", "#F0F5F7"]],
    "Boho": [hex_to_rgb(HexColor(c)) for c in ["#8B4513", "#D2691E", "#E8B4B8", "#D4A574", "#F5DEB3"]],
    "Minimalist": [hex_to_rgb(HexColor(c)) for c in ["#1A1A1A", "#4A4A4A", "#8B8B8B", "#D5D5D5", "#FFFFFF"]],
    "DarkAcademia": [hex_to_rgb(HexColor(c)) for c in ["#2C1810", "#4A3424", "#6B4423", "#8B7355", "#C4A882"]],
    "Scandi": [hex_to_rgb(HexColor(c)) for c in ["#1C1C1C", "#6B6B6B", "#B8B8B8", "#E8E8E8", "#F8F8F8"]],
    "Vintage": [hex_to_rgb(HexColor(c)) for c in ["#3E2723", "#6D4C41", "#A1887F", "#D7CCC8", "#F5EBE0"]],
}


def generate_abstract_pillow(w, h, palette_name, seed=None):
    """Generate abstract wall art using PIL with texture/pillow-style aesthetics."""
    if seed is not None:
        random.seed(seed)
    
    palette = PALETTES[palette_name]
    img = Image.new("RGB", (w, h), palette[-1])
    draw = ImageDraw.Draw(img)
    
    style = random.choice(["circles", "stripes", "blocks", "curves", "dots", "waves", "organic"])
    
    if style == "circles":
        # Concentric circles (popular minimalist wall art)
        cx, cy = w // 2, h // 2
        max_r = min(w, h) // 2
        for i in range(8):
            r = max_r - i * (max_r // 10)
            color = palette[i % len(palette)]
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    
    elif style == "stripes":
        # Horizontal color blocking
        stripe_h = h // len(palette)
        for i, color in enumerate(palette):
            y1 = i * stripe_h
            y2 = (i + 1) * stripe_h if i < len(palette) - 1 else h
            draw.rectangle([0, y1, w, y2], fill=color)
    
    elif style == "blocks":
        # Geometric color blocks
        block_size = w // 4
        for row in range(h // block_size + 1):
            for col in range(w // block_size + 1):
                color = random.choice(palette)
                draw.rectangle(
                    [col * block_size, row * block_size, 
                     (col + 1) * block_size, (row + 1) * block_size],
                    fill=color
                )
    
    elif style == "curves":
        # Flowing curves (abstract art style)
        for i in range(30):
            points = []
            x = 0
            while x < w:
                y = h // 2 + int(math.sin(x * 0.01 + i * 0.5) * h * 0.3) + random.randint(-50, 50)
                points.append((x, y))
                x += 20
            color = palette[i % len(palette)]
            if len(points) > 2:
                draw.line(points, fill=color, width=random.randint(3, 15))
    
    elif style == "dots":
        # Dot pattern (mid-century modern style)
        dot_r = 15
        spacing = 50
        for y in range(dot_r, h, spacing):
            for x in range(dot_r, w, spacing):
                color = random.choice(palette[:-1])  # Skip background
                offset_y = y + (spacing // 2 if (x // spacing) % 2 == 1 else 0)
                draw.ellipse(
                    [x - dot_r, offset_y - dot_r, x + dot_r, offset_y + dot_r],
                    fill=color
                )
    
    elif style == "waves":
        # Landscape waves (abstract nature)
        wave_count = 12
        wave_h = h // wave_count
        for i in range(wave_count):
            color = palette[i % len(palette)]
            y_base = i * wave_h
            points = [(0, y_base)]
            for x in range(0, w + 20, 10):
                y = y_base + int(math.sin(x * 0.02 + i) * 10)
                points.append((x, y))
            points.append((w, h))
            points.append((0, h))
            draw.polygon(points, fill=color)
    
    elif style == "organic":
        # Organic shapes (Blob art)
        for i in range(5):
            cx = random.randint(0, w)
            cy = random.randint(0, h)
            color = palette[i % len(palette)]
            
            points = []
            n = 12
            base_r = random.randint(80, 200)
            for j in range(n):
                angle = 2 * math.pi * j / n
                r = base_r + random.randint(-40, 40)
                px = cx + r * math.cos(angle)
                py = cy + r * math.sin(angle)
                points.append((px, py))
            draw.polygon(points, fill=color)
    
    # Add subtle texture
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return img


def generate_botanical_print(w, h, palette_name, seed=None):
    """Generate a botanical-style art print."""
    if seed is not None:
        random.seed(seed)
    
    palette = PALETTES[palette_name]
    img = Image.new("RGB", (w, h), palette[-1])
    draw = ImageDraw.Draw(img)
    
    # Draw botanical elements
    # Branches with leaves
    num_branches = random.randint(3, 7)
    for b in range(num_branches):
        start_x = random.randint(0, w)
        start_y = random.randint(0, h)
        branch_len = random.randint(150, 300)
        angle = random.uniform(0, 2 * math.pi)
        end_x = start_x + int(branch_len * math.cos(angle))
        end_y = start_y + int(branch_len * math.sin(angle))
        
        # Draw branch
        branch_color = palette[0]  # darkest
        draw.line([(start_x, start_y), (end_x, end_y)], fill=branch_color, width=3)
        
        # Draw leaves along the branch
        num_leaves = random.randint(5, 12)
        for l in range(num_leaves):
            t = (l + 1) / (num_leaves + 1)
            lx = start_x + int((end_x - start_x) * t)
            ly = start_y + int((end_y - start_y) * t)
            
            leaf_size = random.randint(15, 35)
            leaf_angle = angle + math.pi / 2 + random.uniform(-0.5, 0.5)
            
            # Leaf as ellipse
            leaf_color = palette[random.randint(1, len(palette) - 2)]
            lx2 = lx + int(leaf_size * math.cos(leaf_angle))
            ly2 = ly + int(leaf_size * math.sin(leaf_angle))
            draw.ellipse(
                [lx - leaf_size // 4, ly - leaf_size // 2,
                 lx + leaf_size // 4, ly + leaf_size // 2],
                fill=leaf_color
            )
            # Rotate leaf by drawing a line stem
            draw.line([(lx, ly), (lx2, ly2)], fill=branch_color, width=1)
        
        # Add flowers at branch ends
        if random.random() > 0.5:
            flower_r = random.randint(15, 25)
            flower_color = palette[random.randint(2, len(palette) - 1)]
            for p in range(5):
                p_angle = 2 * math.pi * p / 5
                px = end_x + int(flower_r * math.cos(p_angle))
                py = end_y + int(flower_r * math.sin(p_angle))
                draw.ellipse(
                    [px - flower_r // 2, py - flower_r // 2,
                     px + flower_r // 2, py + flower_r // 2],
                    fill=flower_color
                )
            # Center
            draw.ellipse(
                [end_x - 5, end_y - 5, end_x + 5, end_y + 5],
                fill=palette[1]
            )
    
    return img


def generate_minimalist_quote(w, h, palette_name, seed=None):
    """Generate a minimalist quote poster."""
    if seed is not None:
        random.seed(seed)
    
    palette = PALETTES[palette_name]
    img = Image.new("RGB", (w, h), palette[-1])
    draw = ImageDraw.Draw(img)
    
    # Border
    border = 60
    draw.rectangle(
        [border, border, w - border, h - border],
        outline=palette[0],
        width=3
    )
    
    # Decorative element at top
    mid_x = w // 2
    draw.line([(mid_x - 50, 120), (mid_x + 50, 120)], fill=palette[0], width=2)
    
    # Simple shapes as decoration
    for i in range(3):
        y = 150 + i * 20
        r = 8 - i * 2
        draw.ellipse([mid_x - r, y - r, mid_x + r, y + r], fill=palette[0])
    
    return img


def save_as_png(img, filepath, dpi=300):
    """Save image as high-DPI PNG."""
    img.save(filepath, "PNG", dpi=(dpi, dpi))


if __name__ == "__main__":
    print("=" * 60)
    print("Wall Art Generator - Original CC0 Prints")
    print("=" * 60)
    
    # Generate at print quality (300 DPI)
    PRINT_W = 2400  # 8 inches at 300 DPI
    PRINT_H = 3200  # ~10.67 inches
    
    styles = [
        ("abstract", generate_abstract_pillow),
        ("botanical", generate_botanical_print),
        ("minimalist", generate_minimalist_quote),
    ]
    
    total = 0
    seed = 42
    
    for style_name, generator in styles:
        print(f"\n--- Generating {style_name} prints ---")
        for palette_name in PALETTES:
            for variant in range(3):
                seed += 1
                img = generator(PRINT_W, PRINT_H, palette_name, seed=seed)
                
                filename = f"{style_name}_{palette_name}_{variant + 1}.png"
                filepath = os.path.join(PNG_DIR, filename)
                save_as_png(img, filepath, dpi=300)
                
                file_size = os.path.getsize(filepath) / 1024
                total += 1
                print(f"  {filename} ({file_size:.0f} KB)")
    
    # Also create a PDF catalog
    print(f"\n--- Creating PDF catalog ---")
    
    # Use letter landscape for catalog
    PAGE_W, PAGE_H = landscape(letter)
    c = canvas.Canvas(PDF_OUTPUT, pagesize=landscape(letter))
    
    for style_name, generator in styles:
        for palette_name in list(PALETTES.keys())[:4]:  # First 4 palettes for PDF
            for variant in range(2):
                seed += 1
                img = generator(800, 1000, palette_name, seed=seed)
                
                # Save temp PNG for PDF embedding
                temp_path = os.path.join(PNG_DIR, f"_temp_{seed}.png")
                save_as_png(img, temp_path, dpi=150)
                
                # White background
                c.setFillColor(white)
                c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
                
                # Title
                c.setFillColor(HexColor("#2C3E50"))
                c.setFont("Helvetica-Bold", 16)
                c.drawString(40, PAGE_H - 40, f"{style_name.title()} - {palette_name}")
                c.setFont("Helvetica", 10)
                c.setFillColor(HexColor("#999999"))
                c.drawString(40, PAGE_H - 55, f"Variant {variant + 1} | CC0 | 300 DPI print-ready")
                
                # Image centered
                img_w = 350
                img_h = 440
                img_x = (PAGE_W - img_w) / 2
                img_y = (PAGE_H - img_h) / 2 - 20
                c.drawImage(temp_path, img_x, img_y, width=img_w, height=img_h)
                
                # Cleanup
                os.remove(temp_path)
                c.showPage()
    
    c.save()
    
    file_size = os.path.getsize(PDF_OUTPUT) / 1024
    print(f"\n{'=' * 60}")
    print(f"Total PNG prints generated: {total}")
    print(f"PDF catalog: {os.path.basename(PDF_OUTPUT)} ({file_size:.0f} KB)")
    print(f"PNG directory: {PNG_DIR}")
    print(f"Styles: Abstract, Botanical, Minimalist")
    print(f"Palettes: {', '.join(PALETTES.keys())}")
    print(f"Resolution: 2400x3200 px at 300 DPI (8x10.67 inch print)")
    print(f"License: CC0 - Free for commercial use, no attribution required")
