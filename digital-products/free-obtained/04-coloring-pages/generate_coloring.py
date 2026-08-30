"""
Generate printable coloring pages PDFs.
Etsy sellers offer "10,000+ Coloring Pages Bundle" for $1.49.
These are trivially reproducible: we generate line-art patterns programmatically.

Also downloads free coloring pages from Monday Mandala (free CC0 coloring pages).
Requires: reportlab, requests
"""

import os
import math
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_OUTPUT = os.path.join(OUTPUT_DIR, "Free_Coloring_Pages_Bundle.pdf")

PAGE_W, PAGE_H = letter  # 612 x 792

def draw_mandala(c, cx, cy, radius, layers=5):
    """Draw a mandala pattern for coloring."""
    n_petals = 8
    for layer in range(layers):
        r = radius * (layer + 1) / layers
        petal_r = r * 0.3
        
        # Outer circle
        c.setStrokeColor(black)
        c.setLineWidth(0.8)
        c.circle(cx, cy, r, stroke=1, fill=0)
        
        # Petals
        for i in range(n_petals):
            angle = 2 * math.pi * i / n_petals + layer * math.pi / n_petals
            px = cx + r * 0.7 * math.cos(angle)
            py = cy + r * 0.7 * math.sin(angle)
            c.circle(px, py, petal_r * 0.5, stroke=1, fill=0)
        
        # Connecting lines
        if layer > 0:
            for i in range(n_petals):
                angle = 2 * math.pi * i / n_petals + layer * math.pi / n_petals
                x1 = cx + (r * 0.3) * math.cos(angle)
                y1 = cy + (r * 0.3) * math.sin(angle)
                x2 = cx + r * math.cos(angle)
                y2 = cy + r * math.sin(angle)
                c.line(x1, y1, x2, y2)
    
    # Center
    c.circle(cx, cy, radius * 0.15, stroke=1, fill=0)

def draw_geometric_pattern(c, page_num):
    """Draw various geometric patterns for coloring."""
    c.saveState()
    
    if page_num % 6 == 0:
        # Mandala
        draw_mandala(c, PAGE_W/2, PAGE_H/2, 200, layers=6)
    elif page_num % 6 == 1:
        # Tessellation - hexagons
        hex_r = 40
        for row in range(8):
            for col in range(7):
                x = 60 + col * hex_r * 1.8
                y = 60 + row * hex_r * 1.6
                if row % 2 == 1:
                    x += hex_r * 0.9
                points = []
                for i in range(6):
                    angle = math.pi / 3 * i + math.pi / 6
                    px = x + hex_r * math.cos(angle)
                    py = y + hex_r * math.sin(angle)
                    points.append((px, py))
                p = c.beginPath()
                p.moveTo(*points[0])
                for pt in points[1:]:
                    p.lineTo(*pt)
                p.close()
                c.setLineWidth(0.8)
                c.drawPath(p, stroke=1, fill=0)
                # Inner hexagon
                for i in range(6):
                    angle = math.pi / 3 * i + math.pi / 6
                    ix = x + hex_r * 0.5 * math.cos(angle)
                    iy = y + hex_r * 0.5 * math.sin(angle)
                    if i == 0:
                        p2 = c.beginPath()
                        p2.moveTo(ix, iy)
                    else:
                        p2.lineTo(ix, iy)
                try:
                    p2.close()
                    c.drawPath(p2, stroke=1, fill=0)
                except:
                    pass
    elif page_num % 6 == 2:
        # Circle grid pattern
        spacing = 60
        for row in range(10):
            for col in range(9):
                x = 60 + col * spacing
                y = 60 + row * spacing
                if row % 2 == 1:
                    x += spacing / 2
                # Outer circle
                c.setLineWidth(0.8)
                c.circle(x, y, 20, stroke=1, fill=0)
                # Inner patterns
                c.circle(x, y, 12, stroke=1, fill=0)
                c.circle(x, y, 5, stroke=1, fill=0)
                # Petals
                for i in range(4):
                    angle = math.pi / 2 * i
                    px = x + 16 * math.cos(angle)
                    py = y + 16 * math.sin(angle)
                    c.circle(px, py, 6, stroke=1, fill=0)
    elif page_num % 6 == 3:
        # Zentangle-style patterns
        # Draw a large frame
        c.setLineWidth(1)
        c.roundRect(50, 50, PAGE_W - 100, PAGE_H - 100, 10, stroke=1, fill=0)
        c.roundRect(60, 60, PAGE_W - 120, PAGE_H - 120, 8, stroke=1, fill=0)
        
        # Section dividers
        mid_x = PAGE_W / 2
        mid_y = PAGE_H / 2
        c.line(mid_x, 60, mid_x, PAGE_H - 60)
        c.line(60, mid_y, PAGE_W - 60, mid_y)
        
        # Pattern quadrants
        # TL: waves
        for i in range(5):
            y = mid_y - 40 - i * 50
            p = c.beginPath()
            p.moveTo(70, y)
            for x in range(70, int(mid_x - 10), 20):
                p.curveTo(x + 5, y + 15, x + 15, y + 15, x + 20, y)
            c.drawPath(p, stroke=1, fill=0)
        
        # TR: checkerboard pattern
        cb_size = 25
        for row in range(6):
            for col in range(5):
                x = mid_x + 20 + col * cb_size
                y = mid_y + 20 + row * cb_size
                c.rect(x, y, cb_size, cb_size, stroke=1, fill=0)
                if (row + col) % 2 == 0:
                    c.circle(x + cb_size/2, y + cb_size/2, cb_size/3, stroke=1, fill=0)
        
        # BL: diamonds
        for row in range(4):
            for col in range(5):
                x = 90 + col * 50
                y = 90 + row * 50
                c.saveState()
                c.translate(x, y)
                c.rotate(45)
                c.rect(-15, -15, 30, 30, stroke=1, fill=0)
                c.rect(-8, -8, 16, 16, stroke=1, fill=0)
                c.restoreState()
        
        # BR: floral
        for row in range(3):
            for col in range(4):
                fx = mid_x + 50 + col * 60
                fy = 100 + row * 60
                # Petals
                for i in range(6):
                    angle = math.pi / 3 * i
                    px = fx + 15 * math.cos(angle)
                    py = fy + 15 * math.sin(angle)
                    c.circle(px, py, 8, stroke=1, fill=0)
                c.circle(fx, fy, 6, stroke=1, fill=0)
                
    elif page_num % 6 == 4:
        # Abstract flowing lines
        c.setLineWidth(0.7)
        for i in range(15):
            y = 80 + i * 45
            p = c.beginPath()
            p.moveTo(50, y)
            ctrl1_x = 150 + random.randint(-30, 30)
            ctrl1_y = y + random.randint(-20, 20)
            ctrl2_x = 300 + random.randint(-30, 30)
            ctrl2_y = y + random.randint(-20, 20)
            end_x = PAGE_W - 50
            end_y = y + random.randint(-10, 10)
            p.curveTo(ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, end_x, end_y)
            c.drawPath(p, stroke=1, fill=0)
        
        # Add circles at intersections
        for i in range(20):
            x = random.randint(80, int(PAGE_W - 80))
            y = random.randint(80, int(PAGE_H - 80))
            r = random.randint(10, 25)
            c.circle(x, y, r, stroke=1, fill=0)
    else:
        # Stars and celestial pattern
        c.setLineWidth(0.8)
        # Large central star
        def draw_star(c, cx, cy, r, points=5):
            p = c.beginPath()
            outer_r = r
            inner_r = r * 0.4
            for i in range(points * 2):
                angle = math.pi / points * i - math.pi / 2
                radius = outer_r if i % 2 == 0 else inner_r
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                if i == 0:
                    p.moveTo(x, y)
                else:
                    p.lineTo(x, y)
            p.close()
            c.drawPath(p, stroke=1, fill=0)
        
        draw_star(c, PAGE_W/2, PAGE_H/2, 120, 5)
        draw_star(c, PAGE_W/2, PAGE_H/2, 80, 6)
        draw_star(c, PAGE_W/2, PAGE_H/2, 40, 8)
        
        # Scattered small stars
        random.seed(42)
        for _ in range(30):
            x = random.randint(60, int(PAGE_W - 60))
            y = random.randint(60, int(PAGE_H - 60))
            draw_star(c, x, y, random.randint(15, 30), random.choice([5, 6, 8]))
        
        # Half moons
        for _ in range(8):
            x = random.randint(60, int(PAGE_W - 60))
            y = random.randint(60, int(PAGE_H - 60))
            c.circle(x, y, 25, stroke=1, fill=0)
            c.circle(x + 10, y, 25, stroke=1, fill=0)
    
    c.restoreState()

def draw_flower_pattern(c, cx, cy, size):
    """Draw a detailed flower for coloring."""
    # Center circle
    c.circle(cx, cy, size * 0.15, stroke=1, fill=0)
    c.circle(cx, cy, size * 0.08, stroke=1, fill=0)
    
    # Petals (two layers)
    for layer in range(2):
        n_petals = 8
        petal_radius = size * (0.35 if layer == 0 else 0.5)
        offset = math.pi / n_petals * layer
        for i in range(n_petals):
            angle = 2 * math.pi * i / n_petals + offset
            px = cx + petal_radius * math.cos(angle)
            py = cy + petal_radius * math.sin(angle)
            c.circle(px, py, size * 0.18, stroke=1, fill=0)
    
    # Outer ring
    c.circle(cx, cy, size * 0.6, stroke=1, fill=0)

def draw_animal_outline(c, animal_type, cx, cy, size):
    """Draw simple animal outlines for coloring."""
    c.setLineWidth(1.2)
    
    if animal_type == "cat":
        # Simple cat outline
        c.circle(cx, cy, size * 0.35, stroke=1, fill=0)  # head
        # Ears (triangles)
        p = c.beginPath()
        p.moveTo(cx - size * 0.3, cy + size * 0.3)
        p.lineTo(cx - size * 0.4, cy + size * 0.5)
        p.lineTo(cx - size * 0.2, cy + size * 0.35)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        p = c.beginPath()
        p.moveTo(cx + size * 0.3, cy + size * 0.3)
        p.lineTo(cx + size * 0.4, cy + size * 0.5)
        p.lineTo(cx + size * 0.2, cy + size * 0.35)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        # Eyes
        c.circle(cx - size * 0.12, cy + size * 0.05, size * 0.05, stroke=1, fill=0)
        c.circle(cx + size * 0.12, cy + size * 0.05, size * 0.05, stroke=1, fill=0)
        # Nose
        p = c.beginPath()
        p.moveTo(cx - size * 0.04, cy - size * 0.08)
        p.lineTo(cx + size * 0.04, cy - size * 0.08)
        p.lineTo(cx, cy - size * 0.12)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        # Whiskers
        c.setLineWidth(0.5)
        c.line(cx - size * 0.15, cy - size * 0.15, cx - size * 0.35, cy - size * 0.2)
        c.line(cx - size * 0.15, cy - size * 0.1, cx - size * 0.35, cy - size * 0.1)
        c.line(cx + size * 0.15, cy - size * 0.15, cx + size * 0.35, cy - size * 0.2)
        c.line(cx + size * 0.15, cy - size * 0.1, cx + size * 0.35, cy - size * 0.1)
        
    elif animal_type == "butterfly":
        # Body
        c.ellipse(cx - size * 0.03, cy - size * 0.25, 
                  cx + size * 0.03, cy + size * 0.25, stroke=1, fill=0)
        # Wings
        c.ellipse(cx - size * 0.4, cy - size * 0.05, 
                  cx - size * 0.05, cy + size * 0.35, stroke=1, fill=0)
        c.ellipse(cx + size * 0.05, cy - size * 0.05, 
                  cx + size * 0.4, cy + size * 0.35, stroke=1, fill=0)
        c.ellipse(cx - size * 0.35, cy - size * 0.4, 
                  cx - size * 0.05, cy - size * 0.05, stroke=1, fill=0)
        c.ellipse(cx + size * 0.05, cy - size * 0.4, 
                  cx + size * 0.35, cy - size * 0.05, stroke=1, fill=0)
        # Wing patterns
        c.circle(cx - size * 0.22, cy + size * 0.15, size * 0.06, stroke=1, fill=0)
        c.circle(cx + size * 0.22, cy + size * 0.15, size * 0.06, stroke=1, fill=0)
        c.circle(cx - size * 0.2, cy - size * 0.22, size * 0.05, stroke=1, fill=0)
        c.circle(cx + size * 0.2, cy - size * 0.22, size * 0.05, stroke=1, fill=0)
        # Antennae
        c.setLineWidth(0.5)
        c.line(cx, cy + size * 0.25, cx - size * 0.1, cy + size * 0.4)
        c.line(cx, cy + size * 0.25, cx + size * 0.1, cy + size * 0.4)
        c.circle(cx - size * 0.1, cy + size * 0.4, size * 0.02, stroke=1, fill=0)
        c.circle(cx + size * 0.1, cy + size * 0.4, size * 0.02, stroke=1, fill=0)

if __name__ == "__main__":
    random.seed(42)
    c = canvas.Canvas(PDF_OUTPUT, pagesize=letter)
    
    NUM_PAGES = 25  # Generate 25 coloring pages
    
    print(f"Generating {NUM_PAGES} coloring pages...")
    
    for page_num in range(NUM_PAGES):
        # White background
        c.setFillColor(white)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        
        # Set drawing color to black lines
        c.setStrokeColor(black)
        
        if page_num < 12:
            # Geometric/abstract patterns
            draw_geometric_pattern(c, page_num)
        elif page_num < 18:
            # Flower patterns
            cols, rows = 2, 3
            for r in range(rows):
                for col in range(cols):
                    cx = PAGE_W * (0.25 + col * 0.5)
                    cy = PAGE_H * (0.8 - r * 0.3)
                    draw_flower_pattern(c, cx, cy, 80)
        elif page_num < 22:
            # Animal outlines
            animals = ["cat", "butterfly"]
            for i, animal in enumerate(animals):
                cx = PAGE_W * (0.3 + i * 0.4)
                cy = PAGE_H * 0.5
                draw_animal_outline(c, animal, cx, cy, 150)
            # Add decorative border
            c.setLineWidth(1)
            c.roundRect(30, 30, PAGE_W - 60, PAGE_H - 60, 15, stroke=1, fill=0)
        else:
            # Mixed: mandala + decorative elements
            draw_mandala(c, PAGE_W/2, PAGE_H/2, 220, layers=7)
            # Corner decorations
            for cx, cy in [(50, 50), (PAGE_W-50, 50), (50, PAGE_H-50), (PAGE_W-50, PAGE_H-50)]:
                draw_flower_pattern(c, cx, cy, 40)
        
        # Page number
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor("#999999"))
        c.drawCentredString(PAGE_W / 2, 20, f"Coloring Page {page_num + 1} / {NUM_PAGES}")
        
        c.showPage()
    
    c.save()
    
    file_size = os.path.getsize(PDF_OUTPUT) / 1024
    print(f"Generated: {PDF_OUTPUT}")
    print(f"Pages: {NUM_PAGES}")
    print(f"Size: {file_size:.1f} KB")
    print(f"Patterns: Mandala, Geometric, Floral, Animals, Zentangle, Abstract")
