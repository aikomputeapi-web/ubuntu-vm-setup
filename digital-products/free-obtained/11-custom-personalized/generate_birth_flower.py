"""
Birth Flower Family Bouquet Generator
=====================================
Etsy listing #30: "Birth Flower Family Bouquet Personalized Watercolor Birth Flower Print"
Original shop: PopOfInk (27.3k sales, $22.50)

This product sells personalized watercolor-style prints where each family member's
birth month flower is arranged in a bouquet. The original is hand-illustrated by
an artist on commission.

Our free equivalent: A Python generator that creates personalized birth flower
bouquet SVG prints using botanical line-art flowers for each birth month. The
user inputs family member names and birth months, and gets a printable SVG with
each flower labeled and arranged in a decorative bouquet layout.

Usage:
    python generate_birth_flower.py
    python generate_birth_flower.py --names "Mom:3,Dad:7,Kid1:11,Kid2:5"
    python generate_birth_flower.py --names "Alice:1,Bob:6,Charlie:9" --style watercolor
"""

import os
import sys
import math
import random
from dataclasses import dataclass
from typing import List, Tuple

# ============================================================
# Birth month flower data (botanical reference)
# ============================================================

BIRTH_FLOWERS = {
    1: {
        "name": "Carnation",
        "latin": "Dianthus caryophyllus",
        "symbolism": "Love, fascination, distinction",
        "colors": ["#E8A0BF", "#F2C4D0", "#D4839C", "#B85C7E"],
        "petals": 24,
        "petal_shape": "ruffled",
    },
    2: {
        "name": "Violet",
        "latin": "Viola odorata",
        "symbolism": "Loyalty, faithfulness, modesty",
        "colors": ["#7B5EA7", "#9B7FCA", "#6B4E8D", "#8A6BAE"],
        "petals": 5,
        "petal_shape": "heart",
    },
    3: {
        "name": "Daffodil",
        "latin": "Narcissus",
        "symbolism": "Rebirth, new beginnings, hope",
        "colors": ["#F2C849", "#FFD75E", "#E8B832", "#FFEE88"],
        "petals": 6,
        "petal_shape": "trumpet",
    },
    4: {
        "name": "Daisy",
        "latin": "Bellis perennis",
        "symbolism": "Innocence, purity, new beginnings",
        "colors": ["#FFFFFF", "#F0F0F0", "#FFEEEE", "#E8E8E8"],
        "petals": 12,
        "petal_shape": "spoke",
    },
    5: {
        "name": "Lily of the Valley",
        "latin": "Convallaria majalis",
        "symbolism": "Sweetness, humility, return of happiness",
        "colors": ["#FFFFFF", "#F8F8FF", "#E8E8F0", "#F0F0FF"],
        "petals": 6,
        "petal_shape": "bell",
    },
    6: {
        "name": "Rose",
        "latin": "Rosa",
        "symbolism": "Love, passion, beauty",
        "colors": ["#D14B6E", "#E8678A", "#B83E5E", "#F07A9A"],
        "petals": 32,
        "petal_shape": "spiral",
    },
    7: {
        "name": "Larkspur",
        "latin": "Delphinium",
        "symbolism": "Positivity, dignity, grace",
        "colors": ["#7B6BCC", "#9B8BDC", "#5B4BAC", "#8B7BC4"],
        "petals": 5,
        "petal_shape": "spur",
    },
    8: {
        "name": "Gladiolus",
        "latin": "Gladiolus",
        "symbolism": "Strength, integrity, infatuation",
        "colors": ["#E85E8A", "#F0789A", "#D04E7A", "#F0889E"],
        "petals": 6,
        "petal_shape": "blade",
    },
    9: {
        "name": "Aster",
        "latin": "Symphyotrichum",
        "symbolism": "Love, wisdom, faith",
        "colors": ["#9B6BCA", "#B88EDC", "#7B5BAA", "#AC7BC4"],
        "petals": 20,
        "petal_shape": "star",
    },
    10: {
        "name": "Marigold",
        "latin": "Tagetes",
        "symbolism": "Passion, creativity, remembrance",
        "colors": ["#E88420", "#F29933", "#D07510", "#FFA040"],
        "petals": 16,
        "petal_shape": "pompon",
    },
    11: {
        "name": "Chrysanthemum",
        "latin": "Chrysanthemum",
        "symbolism": "Loyalty, friendship, joy",
        "colors": ["#D4A544", "#E8B850", "#C49534", "#FFCC55"],
        "petals": 40,
        "petal_shape": "spider",
    },
    12: {
        "name": "Narcissus",
        "latin": "Narcissus tazetta",
        "symbolism": "Hope, wealth, good wishes",
        "colors": ["#FFD75E", "#FFE888", "#E8C832", "#FFEE99"],
        "petals": 6,
        "petal_shape": "cluster",
    },
}

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

random.seed(42)


@dataclass
class FamilyMember:
    name: str
    birth_month: int  # 1-12

    @property
    def flower(self):
        return BIRTH_FLOWERS[self.birth_month]

    @property
    def month_name(self):
        return MONTH_NAMES[self.birth_month - 1]


def parse_family(family_str: str = None) -> List[FamilyMember]:
    """Parse family members from string or use defaults."""
    if family_str:
        members = []
        for part in family_str.split(","):
            part = part.strip()
            if ":" in part:
                name, month = part.rsplit(":", 1)
                members.append(FamilyMember(name.strip(), int(month)))
        if members:
            return members

    # Default sample family
    return [
        FamilyMember("Mom", 3),
        FamilyMember("Dad", 7),
        FamilyMember("Emma", 11),
        FamilyMember("Liam", 5),
    ]


def draw_flower_svg(cx: float, cy: float, scale: float, flower_data: dict, transform: str = "") -> str:
    """Draw a single flower as SVG paths/elements."""
    colors = flower_data["colors"]
    num_petals = flower_data["petals"]
    primary = colors[0]
    secondary = colors[1] if len(colors) > 1 else colors[0]
    accent = colors[2] if len(colors) > 2 else colors[0]

    svg_parts = [f'<g transform="translate({cx:.1f},{cy:.1f}) scale({scale:.2f}) {transform}">']

    # Stem
    svg_parts.append(f'<line x1="0" y1="0" x2="0" y2="80" stroke="#5C8A5C" stroke-width="2" opacity="0.6"/>')

    # Leaves on stem
    svg_parts.append(f'<path d="M 0,30 Q -15,25 -20,35 Q -12,38 0,35" fill="#6B9C5B" opacity="0.5"/>')
    svg_parts.append(f'<path d="M 0,50 Q 15,45 20,55 Q 12,58 0,55" fill="#5C8B4B" opacity="0.5"/>')

    # Petals
    petal_radius = 30
    for i in range(num_petals):
        angle = (2 * math.pi * i) / num_petals
        px = math.cos(angle) * petal_radius
        py = math.sin(angle) * petal_radius
        rotation = math.degrees(angle)

        if flower_data["petal_shape"] == "ruffled":
            # Wavy-edged petals
            svg_parts.append(
                f'<path d="M 0,0 Q {px*0.6},{py*0.6} {px},{py} '
                f'Q {px*1.1+5},{py*0.9+3} {px*0.85},{py*0.85} '
                f'Q {px*0.5+3},{py*0.5} 0,0 Z" '
                f'fill="{primary}" opacity="{0.75 + 0.25 * math.sin(i)}"/>'
            )
        elif flower_data["petal_shape"] == "heart":
            # Heart-shaped petals (violet)
            svg_parts.append(
                f'<path d="M 0,0 C {px*0.3},{py*0.3} {px*0.7+8},{py*0.7} {px},{py} '
                f'C {px*0.7-8},{py*0.7} {px*0.3},{py*0.3} 0,0 Z" '
                f'fill="{primary}" opacity="0.8"/>'
            )
        elif flower_data["petal_shape"] == "trumpet":
            # Trumpet/daffodil petals
            svg_parts.append(
                f'<ellipse cx="{px*0.6}" cy="{py*0.6}" rx="8" ry="16" '
                f'transform="rotate({rotation} {px*0.6} {py*0.6})" '
                f'fill="{primary}" opacity="0.85"/>'
            )
        elif flower_data["petal_shape"] == "spoke":
            # Daisy spoke petals
            svg_parts.append(
                f'<ellipse cx="{px*0.65}" cy="{py*0.65}" rx="5" ry="14" '
                f'transform="rotate({rotation} {px*0.65} {py*0.65})" '
                f'fill="{primary}" opacity="0.9"/>'
            )
        elif flower_data["petal_shape"] == "spiral":
            # Rose spiral petals
            inner_r = 10 + math.sin(i * 0.5) * 5
            svg_parts.append(
                f'<circle cx="{px*0.5}" cy="{py*0.5}" r="{inner_r}" '
                f'fill="{primary}" opacity="{0.6 + 0.4 * (i / num_petals)}"/>'
            )
        else:
            # Generic rounded petals
            svg_parts.append(
                f'<ellipse cx="{px*0.6}" cy="{py*0.6}" rx="7" ry="12" '
                f'transform="rotate({rotation} {px*0.6} {py*0.6})" '
                f'fill="{primary}" opacity="0.8"/>'
            )

    # Center of flower
    svg_parts.append(f'<circle cx="0" cy="0" r="8" fill="{accent}" opacity="0.7"/>')
    svg_parts.append(f'<circle cx="0" cy="0" r="4" fill="{secondary}" opacity="0.9"/>')

    svg_parts.append('</g>')
    return "\n".join(svg_parts)


def generate_bouquet_svg(members: List[FamilyMember], title: str = "Our Family Birth Flower Bouquet") -> str:
    """Generate the full SVG for a family birth flower bouquet."""
    n = len(members)

    # Canvas: portrait orientation like a print
    W, H = 800, 1100
    cx = W / 2
    bouquet_cy = H // 2 - 50

    svg = [f'<?xml version="1.0" encoding="UTF-8"?>']
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

    # Background
    svg.append(f'<rect width="{W}" height="{H}" fill="#FAF7F0"/>')

    # Decorative border frame
    svg.append(f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#D5CFC7" stroke-width="2" rx="10"/>')
    svg.append(f'<rect x="30" y="30" width="{W-60}" height="{H-60}" fill="none" stroke="#E8E6E0" stroke-width="1" rx="8"/>')

    # Title
    svg.append(f'<text x="{cx}" y="80" text-anchor="middle" font-family="Georgia, serif" font-size="28" fill="#2C3E50" font-weight="bold">{title}</text>')
    svg.append(f'<line x1="200" y1="95" x2="{W-200}" y2="95" stroke="#E8B4B8" stroke-width="2"/>')

    # Bouquet wrapping (decorative cone)
    svg.append(f'<path d="M {cx-180},{bouquet_cy+40} L {cx},{H-120} L {cx+180},{bouquet_cy+40} Z" fill="#F0EDE8" stroke="#D5CFC7" stroke-width="1" opacity="0.6"/>')

    # Arrange flowers in a bouquet (fan layout)
    angle_spread = min(100, 20 * n)  # degrees of fan
    for i, member in enumerate(members):
        # Position in fan
        if n == 1:
            angle = 90  # straight up
        else:
            angle = 90 + (i - (n - 1) / 2) * (angle_spread / (n - 1))

        rad = math.radians(angle)
        dist = 60 + (i % 2) * 20  # slight variation
        fx = cx + math.cos(rad) * dist * 0.5
        fy = bouquet_cy - math.sin(rad) * dist * 0.5
        flower_scale = 1.0 + 0.1 * (n - i) / n
        rotation = angle - 90  # rotate flower to face outward

        flower_data = member.flower
        svg.append(draw_flower_svg(fx, fy, flower_scale * 1.5, flower_data, f"rotate({rotation})"))

    # Labels below each flower
    label_y = H - 180
    label_spacing = min(150, 600 / max(n, 1))
    start_x = cx - (n - 1) * label_spacing / 2

    for i, member in enumerate(members):
        lx = start_x + i * label_spacing
        # Color swatch
        svg.append(f'<circle cx="{lx-50}" cy="{label_y-5}" r="6" fill="{member.flower["colors"][0]}" opacity="0.7"/>')
        # Name
        svg.append(f'<text x="{lx}" y="{label_y}" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#2C3E50" font-weight="bold">{member.name}</text>')
        # Flower name
        svg.append(f'<text x="{lx}" y="{label_y+18}" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="#888888" font-style="italic">{member.flower["name"]}</text>')
        # Birth month
        svg.append(f'<text x="{lx}" y="{label_y+34}" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="#AAAAAA">{member.month_name}</text>')

    # Bottom info
    svg.append(f'<text x="{cx}" y="{H-60}" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="#CCCCCC">Personalized Birth Flower Bouquet - Free Open Source Edition</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def generate_info_card(members: List[FamilyMember]) -> str:
    """Generate a printable info card with flower symbolism for each family member."""
    W, H = 800, 1000
    cx = W / 2

    svg = [f'<?xml version="1.0" encoding="UTF-8"?>']
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

    # Background
    svg.append(f'<rect width="{W}" height="{H}" fill="#FAF7F0"/>')
    svg.append(f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#D5CFC7" stroke-width="2" rx="10"/>')

    # Title
    svg.append(f'<text x="{cx}" y="70" text-anchor="middle" font-family="Georgia, serif" font-size="26" fill="#2C3E50" font-weight="bold">Flower Meanings</text>')
    svg.append(f'<line x1="250" y1="85" x2="{W-250}" y2="85" stroke="#E8B4B8" stroke-width="2"/>')

    # Card for each family member
    card_h = min(120, (H - 150) / len(members))
    for i, member in enumerate(members):
        cy = 120 + i * card_h
        flower = member.flower

        # Card background
        svg.append(f'<rect x="50" y="{cy}" width="{W-100}" height="{card_h-10}" fill="white" stroke="#E8E6E0" stroke-width="1" rx="8"/>')

        # Color indicator
        svg.append(f'<rect x="65" y="{cy+15}" width="8" height="{card_h-40}" rx="4" fill="{flower["colors"][0]}" opacity="0.7"/>')

        # Name
        svg.append(f'<text x="90" y="{cy+25}" font-family="Georgia, serif" font-size="16" fill="#2C3E50" font-weight="bold">{member.name}</text>')

        # Flower name
        svg.append(f'<text x="90" y="{cy+45}" font-family="Georgia, serif" font-size="13" fill="#555555">{flower["name"]} ({flower["latin"]})</text>')

        # Birth month
        svg.append(f'<text x="90" y="{cy+62}" font-family="Georgia, serif" font-size="11" fill="#999999">{member.month_name} Birth Flower</text>')

        # Symbolism
        svg.append(f'<text x="90" y="{cy+80}" font-family="Georgia, serif" font-size="11" fill="#777777" font-style="italic">Symbolizes: {flower["symbolism"]}</text>')

    # Footer
    svg.append(f'<text x="{cx}" y="{H-50}" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="#CCCCCC">Birth Flower Reference Card - Free Open Source Edition</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Birth Flower Family Bouquet SVG prints")
    parser.add_argument("--names", type=str, default=None,
                        help='Family members as "Name:Month,Name:Month" (month 1-12)')
    parser.add_argument("--title", type=str, default="Our Family Birth Flower Bouquet",
                        help="Title for the print")
    parser.add_argument("--output", type=str, default=None,
                        help="Output directory")

    args = parser.parse_args()
    members = parse_family(args.names)

    # Output directory
    out_dir = args.output or os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)

    # Generate bouquet SVG
    svg_content = generate_bouquet_svg(members, args.title)
    bouquet_path = os.path.join(out_dir, "birth_flower_bouquet.svg")
    with open(bouquet_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated: {bouquet_path}")
    print(f"  Family members: {len(members)}")
    for m in members:
        print(f"    {m.name}: {m.flower['name']} ({m.month_name})")

    # Generate info card
    card_content = generate_info_card(members)
    card_path = os.path.join(out_dir, "birth_flower_info_card.svg")
    with open(card_path, "w", encoding="utf-8") as f:
        f.write(card_content)
    print(f"Generated: {card_path}")

    print(f"\nDone! Two SVG prints created for {len(members)} family members.")


if __name__ == "__main__":
    main()
