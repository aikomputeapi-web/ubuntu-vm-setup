"""
Custom Children's Book Illustration Generator
=============================================
Etsy listing #32: "Custom Children's Book Illustration, Whimsical Hand Drawn Artwork
for Stories, Covers or Authors - Vintage Style Scene, Digital Download"
Original shop: NireValleyArt (4.2k sales, $162.05)

This product sells custom hand-drawn illustrations for children's book authors.
The original is a commissioned illustration service.

Our free equivalent: A Python generator that creates whimsical, vintage-style
children's book illustration SVGs in multiple scene templates. The generator
produces:
1. Book cover illustrations with customizable title and character
2. Interior scene illustrations (forest, meadow, underwater, night sky)
3. Character templates (animals, children) in a vintage hand-drawn style
4. A story page layout with text area and illustration area

Usage:
    python generate_illustration.py
    python generate_illustration.py --scene forest --title "The Little Acorn"
    python generate_illustration.py --scene meadow --title "Bunny's Garden" --character rabbit
"""

import os
import sys
import math
import random

random.seed(42)

# ============================================================
# Scene templates with whimsical vintage-style illustrations
# ============================================================

def draw_forest_scene(W, H, palette) -> str:
    """Draw a whimsical forest scene."""
    svg = []

    # Sky gradient
    svg.append(f'<rect width="{W}" height="{H}" fill="{palette["sky"]}"/>')

    # Sun/moon
    svg.append(f'<circle cx="{W*0.8}" cy="{H*0.2}" r="40" fill="{palette["sun"]}" opacity="0.6"/>')
    svg.append(f'<circle cx="{W*0.8}" cy="{H*0.2}" r="30" fill="{palette["sun"]}" opacity="0.8"/>')

    # Distant hills
    svg.append(f'<path d="M 0,{H*0.55} Q {W*0.25},{H*0.35} {W*0.5},{H*0.5} T {W},{H*0.45} L {W},{H} L 0,{H} Z" fill="{palette["hill_far"]}" opacity="0.5"/>')
    svg.append(f'<path d="M 0,{H*0.62} Q {W*0.3},{H*0.45} {W*0.6},{H*0.58} T {W},{H*0.55} L {W},{H} L 0,{H} Z" fill="{palette["hill_near"]}" opacity="0.6"/>')

    # Trees (layered, vintage storybook style)
    tree_positions = [(0.15, 0.75), (0.35, 0.78), (0.55, 0.72), (0.75, 0.76), (0.92, 0.80)]
    for tx, ty in tree_positions:
        x = W * tx
        y = H * ty
        tree_h = 80 + random.randint(-20, 20)
        # Tree trunk
        svg.append(f'<rect x="{x-5}" y="{y-20}" width="10" height="{tree_h//2}" fill="{palette["trunk"]}" rx="2"/>')
        # Tree foliage (layered circles for vintage look)
        for layer, (r, opacity) in enumerate([(35, 0.6), (28, 0.75), (20, 0.9)]):
            ox = random.randint(-5, 5)
            oy = random.randint(-5, 5)
            svg.append(f'<circle cx="{x+ox}" cy="{y-tree_h//2+oy}" r="{r}" fill="{palette["foliage"]}" opacity="{opacity}"/>')

    # Ground
    svg.append(f'<rect x="0" y="{H*0.8}" width="{W}" height="{H*0.2}" fill="{palette["ground"]}" opacity="0.7"/>')

    # Mushrooms (whimsical details)
    for mx, my in [(0.2, 0.85), (0.5, 0.88), (0.8, 0.82)]:
        x, y = W * mx, H * my
        svg.append(f'<rect x="{x-3}" y="{y-8}" width="6" height="12" fill="{palette["trunk"]}" rx="2"/>')
        svg.append(f'<ellipse cx="{x}" cy="{y-8}" rx="12" ry="8" fill="{palette["mushroom"]}" opacity="0.8"/>')
        svg.append(f'<circle cx="{x-4}" cy="{y-10}" r="2" fill="#FFFFFF" opacity="0.6"/>')
        svg.append(f'<circle cx="{x+3}" cy="{y-8}" r="1.5" fill="#FFFFFF" opacity="0.5"/>')

    # Fireflies / sparkles
    for _ in range(15):
        fx = random.randint(50, int(W)-50)
        fy = random.randint(int(H*0.3), int(H*0.7))
        r = random.uniform(1, 3)
        svg.append(f'<circle cx="{fx}" cy="{fy}" r="{r:.1f}" fill="{palette["sparkle"]}" opacity="{random.uniform(0.3, 0.8):.1f}"/>')

    return "\n".join(svg)


def draw_meadow_scene(W, H, palette) -> str:
    """Draw a whimsical meadow scene."""
    svg = []

    svg.append(f'<rect width="{W}" height="{H}" fill="{palette["sky"]}"/>')

    # Sun
    svg.append(f'<circle cx="{W*0.2}" cy="{H*0.2}" r="35" fill="{palette["sun"]}" opacity="0.7"/>')
    # Sun rays (whimsical)
    for i in range(8):
        angle = (2 * math.pi * i) / 8
        x1 = W*0.2 + math.cos(angle) * 45
        y1 = H*0.2 + math.sin(angle) * 45
        x2 = W*0.2 + math.cos(angle) * 60
        y2 = H*0.2 + math.sin(angle) * 60
        svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{palette["sun"]}" stroke-width="3" opacity="0.4"/>')

    # Rolling hills
    svg.append(f'<path d="M 0,{H*0.5} Q {W*0.3},{H*0.4} {W*0.6},{H*0.48} Q {W*0.8},{H*0.42} {W},{H*0.5} L {W},{H} L 0,{H} Z" fill="{palette["hill"]}"/>')

    # Flowers
    for _ in range(25):
        fx = random.randint(20, int(W)-20)
        fy = random.randint(int(H*0.5), int(H*0.85))
        # Stem
        svg.append(f'<line x1="{fx}" y1="{fy}" x2="{fx}" y2="{fy+20}" stroke="{palette["stem"]}" stroke-width="1.5"/>')
        # Flower petals
        petal_color = random.choice(palette["flowers"])
        for p in range(5):
            angle = (2 * math.pi * p) / 5
            px = fx + math.cos(angle) * 5
            py = fy + math.sin(angle) * 5
            svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="{petal_color}" opacity="0.8"/>')
        # Center
        svg.append(f'<circle cx="{fx}" cy="{fy}" r="2" fill="{palette["flower_center"]}" opacity="0.9"/>')

    # Butterflies
    for _ in range(5):
        bx = random.randint(50, int(W)-50)
        by = random.randint(int(H*0.3), int(H*0.6))
        wing_color = random.choice(palette["flowers"])
        # Wings
        svg.append(f'<ellipse cx="{bx-5}" cy="{by}" rx="6" ry="4" fill="{wing_color}" opacity="0.7"/>')
        svg.append(f'<ellipse cx="{bx+5}" cy="{by}" rx="6" ry="4" fill="{wing_color}" opacity="0.7"/>')
        svg.append(f'<line x1="{bx}" y1="{by-4}" x2="{bx}" y2="{by+4}" stroke="#333333" stroke-width="1"/>')

    return "\n".join(svg)


def draw_underwater_scene(W, H, palette) -> str:
    """Draw a whimsical underwater scene."""
    svg = []

    # Water gradient background
    svg.append(f'<rect width="{W}" height="{H}" fill="{palette["water"]}"/>')

    # Light rays from surface
    svg.append(f'<polygon points="0,0 {W*0.3},0 {W*0.15},{H}" fill="{palette["light"]}" opacity="0.1"/>')
    svg.append(f'<polygon points="{W*0.5},0 {W*0.7},0 {W*0.6},{H}" fill="{palette["light"]}" opacity="0.08"/>')

    # Water surface line
    svg.append(f'<path d="M 0,5 Q {W*0.1},15 {W*0.2},5 T {W*0.4},5 T {W*0.6},5 T {W*0.8},5 T {W},5" fill="none" stroke="{palette["light"]}" stroke-width="2" opacity="0.4"/>')

    # Seaweed
    for sx in [0.1, 0.3, 0.5, 0.7, 0.9]:
        x = W * sx
        base_y = H * 0.9
        svg.append(f'<path d="M {x},{base_y} Q {x-15},{base_y-50} {x},{base_y-80} Q {x+15},{base_y-110} {x},{base_y-140}" fill="none" stroke="{palette["seaweed"]}" stroke-width="3" opacity="0.5"/>')

    # Sand at bottom
    svg.append(f'<ellipse cx="{W/2}" cy="{H}" rx="{W/1.5}" ry="40" fill="{palette["sand"]}" opacity="0.6"/>')

    # Bubbles
    for _ in range(20):
        bx = random.randint(30, int(W)-30)
        by = random.randint(int(H*0.2), int(H*0.9))
        r = random.uniform(2, 8)
        svg.append(f'<circle cx="{bx}" cy="{by}" r="{r:.1f}" fill="none" stroke="{palette["light"]}" stroke-width="1" opacity="0.3"/>')
        svg.append(f'<circle cx="{bx-r*0.3:.1f}" cy="{by-r*0.3:.1f}" r="{r*0.3:.1f}" fill="{palette["light"]}" opacity="0.2"/>')

    # Fish (simple whimsical)
    for _ in range(4):
        fx = random.randint(60, int(W)-60)
        fy = random.randint(int(H*0.3), int(H*0.7))
        fish_color = random.choice(palette["fish"])
        direction = random.choice([-1, 1])
        # Body
        svg.append(f'<ellipse cx="{fx}" cy="{fy}" rx="20" ry="10" fill="{fish_color}" opacity="0.7"/>')
        # Tail
        tail_x = fx - 20 * direction
        svg.append(f'<polygon points="{tail_x},{fy} {tail_x-15*direction},{fy-10} {tail_x-15*direction},{fy+10}" fill="{fish_color}" opacity="0.7"/>')
        # Eye
        svg.append(f'<circle cx="{fx+8*direction}" cy="{fy-3}" r="2" fill="#333333" opacity="0.6"/>')

    return "\n".join(svg)


def draw_night_sky_scene(W, H, palette) -> str:
    """Draw a whimsical night sky scene."""
    svg = []

    # Night sky
    svg.append(f'<rect width="{W}" height="{H}" fill="{palette["sky"]}"/>')

    # Moon
    svg.append(f'<circle cx="{W*0.75}" cy="{H*0.25}" r="50" fill="{palette["moon"]}" opacity="0.8"/>')
    svg.append(f'<circle cx="{W*0.75+15}" cy="{H*0.25-10}" r="50" fill="{palette["sky"]}" opacity="0.9"/>')
    # Moon glow
    svg.append(f'<circle cx="{W*0.75}" cy="{H*0.25}" r="65" fill="{palette["moon"]}" opacity="0.1"/>')

    # Stars
    for _ in range(50):
        sx = random.randint(10, int(W)-10)
        sy = random.randint(10, int(H*0.6))
        r = random.uniform(0.5, 2.5)
        svg.append(f'<circle cx="{sx}" cy="{sy}" r="{r:.1f}" fill="{palette["star"]}" opacity="{random.uniform(0.4, 1.0):.1f}"/>')

    # Big stars (4-pointed)
    for _ in range(8):
        sx = random.randint(50, int(W)-50)
        sy = random.randint(30, int(H*0.5))
        size = random.uniform(3, 6)
        svg.append(f'<path d="M {sx},{sy-size} L {sx+size*0.3},{sy-size*0.3} L {sx+size},{sy} L {sx+size*0.3},{sy+size*0.3} L {sx},{sy+size} L {sx-size*0.3},{sy+size*0.3} L {sx-size},{sy} L {sx-size*0.3},{sy-size*0.3} Z" fill="{palette["star"]}" opacity="0.8"/>')

    # Hills silhouette
    svg.append(f'<path d="M 0,{H*0.65} Q {W*0.2},{H*0.55} {W*0.4},{H*0.62} Q {W*0.6},{H*0.5} {W*0.8},{H*0.6} Q {W*0.9},{H*0.55} {W},{H*0.62} L {W},{H} L 0,{H} Z" fill="{palette["hills"]}"/>')

    # Trees silhouette
    for tx in [0.1, 0.25, 0.55, 0.8, 0.95]:
        x = W * tx
        y = H * 0.7
        svg.append(f'<polygon points="{x-10},{y} {x},{y-60} {x+10},{y}" fill="{palette["trees"]}"/>')
        svg.append(f'<rect x="{x-3}" y="{y}" width="6" height="20" fill="{palette["trees"]}"/>')

    # Fireflies / glowing dots near ground
    for _ in range(15):
        fx = random.randint(20, int(W)-20)
        fy = random.randint(int(H*0.65), int(H*0.95))
        svg.append(f'<circle cx="{fx}" cy="{fy}" r="2" fill="{palette["firefly"]}" opacity="0.8"/>')
        svg.append(f'<circle cx="{fx}" cy="{fy}" r="4" fill="{palette["firefly"]}" opacity="0.2"/>')

    return "\n".join(svg)


# Scene palettes
SCENE_PALETTES = {
    "forest": {
        "sky": "#D4E8D4", "sun": "#F5E6A8", "hill_far": "#A8C8A0", "hill_near": "#8FB87F",
        "ground": "#6B9C5B", "trunk": "#8B6F47", "foliage": "#5C8A4C", "mushroom": "#D45D5D",
        "sparkle": "#FFEE88",
    },
    "meadow": {
        "sky": "#C8E0F0", "sun": "#FFD75E", "hill": "#8FCC6B",
        "stem": "#5C8A5C", "flowers": ["#E85E8A", "#F2C849", "#7B6BCC", "#FFFFFF", "#FF8A50"],
        "flower_center": "#F2C849",
    },
    "underwater": {
        "water": "#4A90C4", "light": "#E0F0FF", "seaweed": "#3A7C5A", "sand": "#E8D8A8",
        "fish": ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95A5CC"],
    },
    "night": {
        "sky": "#1A1A3E", "moon": "#F5E6A8", "star": "#FFFFFF",
        "hills": "#2A2A4E", "trees": "#1E1E38", "firefly": "#FFEE88",
    },
}

SCENE_DRAWERS = {
    "forest": draw_forest_scene,
    "meadow": draw_meadow_scene,
    "underwater": draw_underwater_scene,
    "night": draw_night_sky_scene,
}


def generate_book_cover(scene: str, title: str, subtitle: str = "") -> str:
    """Generate a children's book cover illustration SVG."""
    W, H = 800, 1000
    palette = SCENE_PALETTES.get(scene, SCENE_PALETTES["forest"])
    drawer = SCENE_DRAWERS.get(scene, draw_forest_scene)

    svg = [f'<?xml version="1.0" encoding="UTF-8"?>']
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

    # Scene illustration
    svg.append(drawer(W, H, palette))

    # Title overlay (vintage style)
    # Title background card
    svg.append(f'<rect x="60" y="40" width="{W-120}" height="120" fill="#FFFFFF" opacity="0.85" rx="10"/>')
    svg.append(f'<rect x="65" y="45" width="{W-130}" height="110" fill="none" stroke="#D5CFC7" stroke-width="1" rx="8"/>')

    # Title text
    svg.append(f'<text x="{W/2}" y="90" text-anchor="middle" font-family="Georgia, serif" font-size="24" fill="#2C3E50" font-weight="bold">{title}</text>')
    if subtitle:
        svg.append(f'<text x="{W/2}" y="120" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#888888" font-style="italic">{subtitle}</text>')

    # Decorative corners
    for cx, cy in [(70, 50), (W-70, 50), (70, H-50), (W-70, H-50)]:
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="#D5CFC7"/>')

    # Author placeholder
    svg.append(f'<text x="{W/2}" y="{H-30}" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#AAAAAA">by Your Name Here</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def generate_story_page(scene: str, page_text: str, page_num: int) -> str:
    """Generate a story page layout with text area and illustration."""
    W, H = 800, 1000
    palette = SCENE_PALETTES.get(scene, SCENE_PALETTES["forest"])
    drawer = SCENE_DRAWERS.get(scene, draw_forest_scene)

    svg = [f'<?xml version="1.0" encoding="UTF-8"?>']
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

    # Top: illustration (top 65%)
    svg.append(f'<clipPath id="illus-clip-{page_num}">')
    svg.append(f'<rect x="0" y="0" width="{W}" height="{int(H*0.65)}"/>')
    svg.append(f'</clipPath>')
    svg.append(f'<g clip-path="url(#illus-clip-{page_num})">')
    svg.append(drawer(W, int(H*0.65), palette))
    svg.append(f'</g>')

    # Divider line
    svg.append(f'<line x1="40" y1="{int(H*0.66)}" x2="{W-40}" y2="{int(H*0.66)}" stroke="#D5CFC7" stroke-width="1"/>')
    svg.append(f'<circle cx="{W/2}" cy="{int(H*0.66)}" r="3" fill="#D5CFC7"/>')

    # Bottom: text area
    svg.append(f'<text x="60" y="{int(H*0.75)}" font-family="Georgia, serif" font-size="14" fill="#2C3E50">{page_text[:60]}</text>')
    # Word wrap simple
    words = page_text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if len(test_line) <= 55:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    for i, line in enumerate(lines[:6]):
        svg.append(f'<text x="60" y="{int(H*0.75) + i*22}" font-family="Georgia, serif" font-size="14" fill="#2C3E50">{line}</text>')

    # Page number
    svg.append(f'<text x="{W/2}" y="{H-20}" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="#CCCCCC">- {page_num} -</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def generate_character_template(character: str) -> str:
    """Generate a simple character template SVG."""
    W, H = 400, 500
    svg = [f'<?xml version="1.0" encoding="UTF-8"?>']
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    svg.append(f'<rect width="{W}" height="{H}" fill="#FAF7F0"/>')

    cx, cy = W/2, H*0.35

    if character in ("rabbit", "bunny"):
        # Rabbit body
        svg.append(f'<ellipse cx="{cx}" cy="{cy+60}" rx="50" ry="65" fill="#F5E6D8" stroke="#D4C4B0" stroke-width="2"/>')
        # Head
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="#F5E6D8" stroke="#D4C4B0" stroke-width="2"/>')
        # Ears
        svg.append(f'<ellipse cx="{cx-15}" cy="{cy-55}" rx="10" ry="35" fill="#F5E6D8" stroke="#D4C4B0" stroke-width="2"/>')
        svg.append(f'<ellipse cx="{cx+15}" cy="{cy-55}" rx="10" ry="35" fill="#F5E6D8" stroke="#D4C4B0" stroke-width="2"/>')
        # Inner ears
        svg.append(f'<ellipse cx="{cx-15}" cy="{cy-55}" rx="4" ry="25" fill="#F0C4B0"/>')
        svg.append(f'<ellipse cx="{cx+15}" cy="{cy-55}" rx="4" ry="25" fill="#F0C4B0"/>')
        # Eyes
        svg.append(f'<circle cx="{cx-12}" cy="{cy-5}" r="5" fill="#333333"/>')
        svg.append(f'<circle cx="{cx+12}" cy="{cy-5}" r="5" fill="#333333"/>')
        svg.append(f'<circle cx="{cx-10}" cy="{cy-7}" r="2" fill="#FFFFFF"/>')
        svg.append(f'<circle cx="{cx+14}" cy="{cy-7}" r="2" fill="#FFFFFF"/>')
        # Nose
        svg.append(f'<path d="M {cx-4},{cy+8} L {cx+4},{cy+8} L {cx},{cy+12} Z" fill="#E85E8A"/>')
        # Mouth
        svg.append(f'<path d="M {cx},{cy+12} Q {cx-5},{cy+18} {cx-8},{cy+15} M {cx},{cy+12} Q {cx+5},{cy+18} {cx+8},{cy+15}" fill="none" stroke="#333333" stroke-width="1.5"/>')
        label = "Bunny"
    elif character in ("bear", "teddy"):
        # Bear body
        svg.append(f'<ellipse cx="{cx}" cy="{cy+60}" rx="55" ry="60" fill="#C4956C" stroke="#A07850" stroke-width="2"/>')
        # Head
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="42" fill="#C4956C" stroke="#A07850" stroke-width="2"/>')
        # Ears
        svg.append(f'<circle cx="{cx-30}" cy="{cy-30}" r="15" fill="#C4956C" stroke="#A07850" stroke-width="2"/>')
        svg.append(f'<circle cx="{cx+30}" cy="{cy-30}" r="15" fill="#C4956C" stroke="#A07850" stroke-width="2"/>')
        svg.append(f'<circle cx="{cx-30}" cy="{cy-30}" r="8" fill="#D4A574"/>')
        svg.append(f'<circle cx="{cx+30}" cy="{cy-30}" r="8" fill="#D4A574"/>')
        # Muzzle
        svg.append(f'<ellipse cx="{cx}" cy="{cy+10}" rx="20" ry="15" fill="#E8D0A8"/>')
        # Eyes
        svg.append(f'<circle cx="{cx-12}" cy="{cy-5}" r="4" fill="#333333"/>')
        svg.append(f'<circle cx="{cx+12}" cy="{cy-5}" r="4" fill="#333333"/>')
        # Nose
        svg.append(f'<ellipse cx="{cx}" cy="{cy+6}" rx="4" ry="3" fill="#333333"/>')
        # Mouth
        svg.append(f'<path d="M {cx},{cy+10} Q {cx-4},{cy+16} {cx-7},{cy+13} M {cx},{cy+10} Q {cx+4},{cy+16} {cx+7},{cy+13}" fill="none" stroke="#333333" stroke-width="1.5"/>')
        label = "Bear"
    else:  # generic child
        # Body
        svg.append(f'<rect x="{cx-30}" y="{cy+30}" width="60" height="80" rx="15" fill="#7B5EA7" stroke="#5C4B8A" stroke-width="2"/>')
        # Head
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="#F5D4B0" stroke="#D4B490" stroke-width="2"/>')
        # Hair
        svg.append(f'<path d="M {cx-35},{cy-10} Q {cx},{cy-45} {cx+35},{cy-10} Q {cx+25},{cy-25} {cx},{cy-30} Q {cx-25},{cy-25} {cx-35},{cy-10}" fill="#5C4B3A"/>')
        # Eyes
        svg.append(f'<circle cx="{cx-12}" cy="{cy}" r="5" fill="#333333"/>')
        svg.append(f'<circle cx="{cx+12}" cy="{cy}" r="5" fill="#333333"/>')
        svg.append(f'<circle cx="{cx-10}" cy="{cy-2}" r="2" fill="#FFFFFF"/>')
        svg.append(f'<circle cx="{cx+14}" cy="{cy-2}" r="2" fill="#FFFFFF"/>')
        # Cheeks
        svg.append(f'<circle cx="{cx-18}" cy="{cy+10}" r="6" fill="#F0A0A0" opacity="0.5"/>')
        svg.append(f'<circle cx="{cx+18}" cy="{cy+10}" r="6" fill="#F0A0A0" opacity="0.5"/>')
        # Smile
        svg.append(f'<path d="M {cx-8},{cy+12} Q {cx},{cy+20} {cx+8},{cy+12}" fill="none" stroke="#333333" stroke-width="2"/>')
        label = "Child"

    # Label
    svg.append(f'<text x="{W/2}" y="{H-30}" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#2C3E50">{label} Character Template</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Children's Book Illustration SVGs")
    parser.add_argument("--scene", type=str, default="forest", choices=list(SCENE_PALETTES.keys()),
                        help="Scene type: forest, meadow, underwater, night")
    parser.add_argument("--title", type=str, default="The Little Adventurer",
                        help="Book title for cover")
    parser.add_argument("--subtitle", type=str, default="A Whimsical Tale",
                        help="Book subtitle")
    parser.add_argument("--character", type=str, default="rabbit",
                        choices=["rabbit", "bear", "child"],
                        help="Character type for character template")

    args = parser.parse_args()

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)

    # Generate all 4 scene covers
    for scene in SCENE_PALETTES.keys():
        cover = generate_book_cover(scene, args.title, args.subtitle)
        path = os.path.join(out_dir, f"book_cover_{scene}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(cover)
        print(f"Generated: {path}")

    # Generate story pages (one per scene)
    sample_text = "Once upon a time, in a land filled with wonder and magic, there lived a small but brave little creature who dreamed of adventure beyond the meadow."
    for i, scene in enumerate(SCENE_PALETTES.keys()):
        page = generate_story_page(scene, sample_text, i + 1)
        path = os.path.join(out_dir, f"story_page_{scene}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"Generated: {path}")

    # Generate character templates
    for char in ["rabbit", "bear", "child"]:
        char_svg = generate_character_template(char)
        path = os.path.join(out_dir, f"character_{char}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(char_svg)
        print(f"Generated: {path}")

    print(f"\nDone! {len(SCENE_PALETTES)} covers + {len(SCENE_PALETTES)} story pages + 3 character templates generated.")


if __name__ == "__main__":
    main()
