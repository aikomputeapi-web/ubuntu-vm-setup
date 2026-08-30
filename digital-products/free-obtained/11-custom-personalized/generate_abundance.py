"""
Abundance Energetic Artwork Generator
=====================================
Etsy listing #31: "Complete Advanced Package for Abundance: Charged Digital Artwork + Personal Report & Energetic Transmissions"
Original shop: Blisstatic (19.8k sales, $135.04)

This product sells "charged digital artwork" with a personalized abundance report
and "energetic transmissions." The original is a spiritual/wellness service product.

Our free equivalent: A Python generator that creates mandala-style abundance
artwork SVGs with personalized affirmation reports based on the user's name and
intentions. Each mandala is unique (seeded by name) and comes with a printable
report containing abundance affirmations and reflection prompts.

Usage:
    python generate_abundance.py
    python generate_abundance.py --name "Sarah" --intention "prosperity"
    python generate_abundance.py --name "John" --intention "health" --seed 12345
"""

import os
import sys
import math
import random
import hashlib
from datetime import datetime

# ============================================================
# Abundance themes and affirmations
# ============================================================

ABUNDANCE_THEMES = {
    "prosperity": {
        "colors": ["#D4AF37", "#FFD700", "#B8860B", "#FFCC44", "#DAA520"],
        "symbol": "lotus",
        "affirmations": [
            "Abundance flows to me naturally and effortlessly.",
            "I am worthy of financial prosperity and abundance.",
            "Every day, in every way, I am becoming more abundant.",
            "I attract wealth, success, and opportunity with ease.",
            "My income is constantly increasing.",
            "I am open to receiving unlimited abundance from the universe.",
        ],
        "prompts": [
            "What would I do if money were no object?",
            "Where in my life do I already experience abundance?",
            "What limiting beliefs about money am I ready to release?",
            "How can I create more value for others today?",
        ],
    },
    "health": {
        "colors": ["#4CAF50", "#81C784", "#388E3C", "#66BB6A", "#A5D6A7"],
        "symbol": "leaf",
        "affirmations": [
            "My body is strong, healthy, and full of vitality.",
            "Every cell in my body vibrates with health and energy.",
            "I nourish my body with love and care.",
            "Healing energy flows through every part of me.",
            "I am grateful for my healthy, vibrant body.",
            "Perfect health is my natural state of being.",
        ],
        "prompts": [
            "What does vibrant health look like for me?",
            "How can I honor my body today?",
            "What health habit am I ready to embrace?",
            "What does my body need right now?",
        ],
    },
    "love": {
        "colors": ["#E91E63", "#F06292", "#C2185B", "#EC407A", "#F48FB1"],
        "symbol": "heart",
        "affirmations": [
            "I am worthy of deep, unconditional love.",
            "Love flows to me and through me effortlessly.",
            "My heart is open to giving and receiving love.",
            "I attract loving, supportive, and kind people into my life.",
            "I am surrounded by love in all its forms.",
            "I radiate love and it returns to me multiplied.",
        ],
        "prompts": [
            "How do I show love to myself?",
            "What relationships bring me the most joy?",
            "How can I be more loving today?",
            "What does my heart truly desire?",
        ],
    },
    "success": {
        "colors": ["#2196F3", "#64B5F6", "#1565C0", "#42A5F5", "#90CAF9"],
        "symbol": "star",
        "affirmations": [
            "I am capable of achieving extraordinary success.",
            "Every challenge is an opportunity for growth.",
            "I trust my abilities and take bold action.",
            "Success is my natural state.",
            "I am unstoppable in pursuing my goals.",
            "The universe supports my success in all endeavors.",
        ],
        "prompts": [
            "What does success mean to me, truly?",
            "What is my next bold step forward?",
            "Who am I becoming through this journey?",
            "What am I ready to achieve?",
        ],
    },
    "peace": {
        "colors": ["#9C27B0", "#BA68C8", "#7B1FA2", "#AB47BC", "#CE93D8"],
        "symbol": "mandala",
        "affirmations": [
            "I am at peace with myself and the world.",
            "Calm and tranquility fill my mind and body.",
            "I release all tension and embrace serenity.",
            "Inner peace is my foundation and my strength.",
            "I choose peace over worry, love over fear.",
            "Stillness within me creates harmony around me.",
        ],
        "prompts": [
            "Where in my body do I feel peace?",
            "What brings me a sense of deep calm?",
            "What am I ready to let go of?",
            "How can I create more stillness in my day?",
        ],
    },
}


def name_to_seed(name: str) -> int:
    """Convert a name to a deterministic seed for reproducible artwork."""
    return int(hashlib.md5(name.encode()).hexdigest(), 16) % (2**32)


def draw_mandala(cx: float, cy: float, radius: float, colors: list, symbol: str, layers: int = 5) -> str:
    """Draw a mandala-style artwork as SVG."""
    svg_parts = [f'<g transform="translate({cx:.1f},{cy:.1f})">']

    # Outer rings
    for r in range(layers, 0, -1):
        ring_radius = radius * (r / layers)
        color = colors[r % len(colors)]
        opacity = 0.15 + 0.1 * r

        # Ring
        svg_parts.append(f'<circle cx="0" cy="0" r="{ring_radius:.1f}" fill="none" stroke="{color}" stroke-width="1.5" opacity="{opacity}"/>')

        # Petals/elements on each ring
        num_elements = 6 + r * 2  # more elements on outer rings
        for i in range(num_elements):
            angle = (2 * math.pi * i) / num_elements
            ex = math.cos(angle) * ring_radius
            ey = math.sin(angle) * ring_radius

            elem_color = colors[(i + r) % len(colors)]
            elem_size = 4 + (radius / layers) * 0.15

            if symbol == "lotus":
                # Lotus petals
                svg_parts.append(
                    f'<path d="M {ex:.1f},{ey:.1f} '
                    f'c {math.cos(angle)*3:.1f},{math.sin(angle)*3:.1f} '
                    f'{math.cos(angle)*elem_size:.1f},{math.sin(angle)*elem_size:.1f} '
                    f'0,0 Z" fill="{elem_color}" opacity="0.6"/>'
                )
            elif symbol == "star":
                # Star points
                px = ex + math.cos(angle) * elem_size
                py = ey + math.sin(angle) * elem_size
                svg_parts.append(
                    f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
                    f'stroke="{elem_color}" stroke-width="2" opacity="0.7"/>'
                )
            elif symbol == "heart":
                # Heart shapes
                svg_parts.append(
                    f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{elem_size:.1f}" '
                    f'fill="{elem_color}" opacity="0.5"/>'
                )
            elif symbol == "leaf":
                # Leaf shapes
                rotation = math.degrees(angle)
                svg_parts.append(
                    f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{elem_size:.1f}" ry="{elem_size*1.5:.1f}" '
                    f'transform="rotate({rotation:.1f} {ex:.1f} {ey:.1f})" '
                    f'fill="{elem_color}" opacity="0.5"/>'
                )
            else:
                # Default: circles
                svg_parts.append(
                    f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{elem_size:.1f}" '
                    f'fill="{elem_color}" opacity="0.5"/>'
                )

    # Center
    svg_parts.append(f'<circle cx="0" cy="0" r="15" fill="{colors[0]}" opacity="0.8"/>')
    svg_parts.append(f'<circle cx="0" cy="0" r="8" fill="{colors[-1]}" opacity="0.9"/>')
    svg_parts.append(f'<circle cx="0" cy="0" r="3" fill="#FFFFFF" opacity="0.8"/>')

    # Geometric overlay
    num_geo = 12
    geo_radius = radius * 0.6
    for i in range(num_geo):
        angle = (2 * math.pi * i) / num_geo
        x1 = math.cos(angle) * geo_radius
        y1 = math.sin(angle) * geo_radius
        angle2 = (2 * math.pi * (i + 1)) / num_geo
        x2 = math.cos(angle2) * geo_radius
        y2 = math.sin(angle2) * geo_radius
        svg_parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{colors[i % len(colors)]}" stroke-width="1" opacity="0.3"/>'
        )

    svg_parts.append('</g>')
    return "\n".join(svg_parts)


def generate_artwork_svg(name: str, intention: str, seed: int = None) -> str:
    """Generate the abundance artwork SVG."""
    if seed is None:
        seed = name_to_seed(name)
    random.seed(seed)

    theme = ABUNDANCE_THEMES.get(intention, ABUNDANCE_THEMES["prosperity"])
    colors = theme["colors"]
    symbol = theme["symbol"]

    W, H = 1000, 1000
    cx, cy = W // 2, H // 2
    mandala_radius = min(W, H) * 0.4

    svg = [f'<?xml version="1.0" encoding="UTF-8"?>']
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

    # Background with gradient effect
    svg.append(f'<defs>')
    svg.append(f'<radialGradient id="bg-grad" cx="50%" cy="50%" r="50%">')
    svg.append(f'<stop offset="0%" stop-color="{colors[0]}" stop-opacity="0.15"/>')
    svg.append(f'<stop offset="50%" stop-color="{colors[2]}" stop-opacity="0.05"/>')
    svg.append(f'<stop offset="100%" stop-color="#FAFAFA" stop-opacity="0"/>')
    svg.append(f'</radialGradient>')
    svg.append(f'</defs>')

    svg.append(f'<rect width="{W}" height="{H}" fill="#0F0F0F"/>')
    svg.append(f'<rect width="{W}" height="{H}" fill="url(#bg-grad)"/>')

    # Outer decorative border
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{mandala_radius+40}" fill="none" stroke="{colors[0]}" stroke-width="0.5" opacity="0.3"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{mandala_radius+60}" fill="none" stroke="{colors[1]}" stroke-width="0.5" opacity="0.2"/>')

    # Generate mandala
    layers = random.randint(4, 7)
    svg.append(draw_mandala(cx, cy, mandala_radius, colors, symbol, layers))

    # Name text at bottom
    svg.append(f'<text x="{cx}" y="{H-60}" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="{colors[0]}" opacity="0.8">{name}</text>')
    svg.append(f'<text x="{cx}" y="{H-35}" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{colors[1]}" opacity="0.5" letter-spacing="3">ABUNDANCE · {intention.upper()}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def generate_personal_report(name: str, intention: str, seed: int = None) -> str:
    """Generate a personal abundance report as markdown."""
    if seed is None:
        seed = name_to_seed(name)
    random.seed(seed)

    theme = ABUNDANCE_THEMES.get(intention, ABUNDANCE_THEMES["prosperity"])

    # Select 4 affirmations randomly but deterministically
    affirmations = random.sample(theme["affirmations"], min(4, len(theme["affirmations"])))
    prompts = random.sample(theme["prompts"], min(3, len(theme["prompts"])))

    date_str = datetime.now().strftime("%B %d, %Y")

    report = f"""# Personal Abundance Report

## Prepared for: {name}
### Intention: {intention.title()}
### Date: {date_str}

---

## Your Abundance Mandala

Your personalized mandala artwork was generated using a unique energetic signature
derived from your name. The geometric patterns and colors are specifically attuned
to your intention of **{intention}**.

### Color Resonance

The colors in your mandala are:
"""
    for i, color in enumerate(theme["colors"]):
        report += f"- **{color}** — Resonance layer {i+1}\n"

    report += f"""
### Symbol: {theme['symbol'].title()}

The {theme['symbol']} symbol woven throughout your mandala represents the energy of
{intention}. Each layer of the mandala corresponds to a different aspect of your
abundance journey.

---

## Your Personal Affirmations

These affirmations are your daily companions. Speak them aloud each morning:

"""
    for i, aff in enumerate(affirmations, 1):
        report += f"{i}. {aff}\n"

    report += f"""
---

## Reflection Prompts

Take time to journal on these questions:

"""
    for i, prompt in enumerate(prompts, 1):
        report += f"{i}. {prompt}\n"

    report += f"""
---

## Your Abundance Practice

1. **Morning Ritual**: Display your mandala artwork where you can see it each morning.
2. **Affirmation Practice**: Choose one affirmation each day and repeat it 21 times.
3. **Evening Reflection**: Journal on one prompt each evening.
4. **Gratitude**: Write down three things you are grateful for before sleep.

---

## Numerological Note

Your unique seed value is **{seed}**. This mathematical signature ensures your
mandala artwork is uniquely yours and cannot be replicated by chance.

---

*This report is a free, open-source alternative to paid abundance coaching products.
It is intended for personal reflection and inspiration, not as a substitute for
professional advice.*
"""
    return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Abundance Energetic Artwork + Personal Report")
    parser.add_argument("--name", type=str, default="Friend", help="Name for personalization")
    parser.add_argument("--intention", type=str, default="prosperity",
                        choices=list(ABUNDANCE_THEMES.keys()),
                        help="Abundance intention theme")
    parser.add_argument("--seed", type=int, default=None, help="Override the name-based seed")

    args = parser.parse_args()
    seed = args.seed or name_to_seed(args.name)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)

    # Generate artwork
    svg_content = generate_artwork_svg(args.name, args.intention, seed)
    svg_path = os.path.join(out_dir, f"abundance_artwork_{args.intention}.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated: {svg_path}")

    # Generate report
    report = generate_personal_report(args.name, args.intention, seed)
    report_path = os.path.join(out_dir, f"abundance_report_{args.intention}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Generated: {report_path}")

    print(f"\nName: {args.name}")
    print(f"Intention: {args.intention}")
    print(f"Seed: {seed}")


if __name__ == "__main__":
    main()
