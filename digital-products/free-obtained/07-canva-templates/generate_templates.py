"""
Generate Canva-alternative template files as SVG and HTML.
These are original CC0 templates that replace Canva-dependent Etsy listings.
Users can open these in any browser, edit the SVG, and export to PNG/PDF.

Covers: social media posts, Instagram carousels, invitations, business cards,
matchbook posters, magazine covers, wedding websites, and portfolio templates.
"""
import os
import math
from reportlab.lib.colors import HexColor

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(OUTPUT_DIR, "templates")
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# Instagram post: 1080x1080
# Instagram story: 1080x1920
# Business card: 1050x600 (3.5x2 at 300dpi)
# Carousel slide: 1080x1350
# Invitation: 1080x1080
# Magazine cover: 1080x1380

PALETTES = {
    "blush": ["#F8E2E7", "#E8B4B8", "#D4A5A5", "#8B5E5A", "#3D2B2B"],
    "sage": ["#E8F0E5", "#B8D8BA", "#8FBC8F", "#5A7D5A", "#2D3E2D"],
    "navy_gold": ["#1A1A2E", "#16213E", "#E8C468", "#C4956C", "#F5F2ED"],
    "boho": ["#F5EBE0", "#D4A574", "#C49B6C", "#8B5E3C", "#5C3D2E"],
    "minimalist": ["#FAFAFA", "#E5E5E5", "#999999", "#4A4A4A", "#1A1A1A"],
    "coastal": ["#F0F5F7", "#D4E4E8", "#6BA8B5", "#3A6B8C", "#1C2D3A"],
    "dark_academia": ["#F5EBE0", "#C4A882", "#8B7355", "#4A3424", "#2C1810"],
    "cottagecore": ["#F5EDE0", "#E8D5B7", "#DBC5A0", "#A8C4A2", "#6B8E6B"],
}

ICONS_SVG = {
    "heart": 'M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z',
    "star": "M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 16.8 5.8 21.3l2.4-7.4L2 9.4h7.6z",
    "flower": "M50 10 Q70 30 70 50 Q70 70 50 90 Q30 70 30 50 Q30 30 50 10 Z",
    "leaf": "M50 10 Q70 30 70 50 Q70 70 50 90 Q30 70 30 50 Q30 30 50 10",
}

def svg_header(w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'

def svg_footer():
    return '</svg>'

def generate_instagram_post(palette_name, template_type="quote"):
    """Generate Instagram post template (1080x1080)."""
    colors = PALETTES[palette_name]
    W, H = 1080, 1080
    
    if template_type == "quote":
        svg = f'''{svg_header(W, H)}
<defs>
  <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" style="stop-color:{colors[0]}"/>
    <stop offset="100%" style="stop-color:{colors[1]}"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<!-- Decorative border -->
<rect x="40" y="40" width="{W-80}" height="{H-80}" fill="none" stroke="{colors[3]}" stroke-width="3" rx="20"/>
<!-- Quote marks -->
<text x="120" y="280" font-family="Georgia, serif" font-size="180" fill="{colors[2]}" opacity="0.4">"</text>
<!-- Main quote text -->
<text x="540" y="480" text-anchor="middle" font-family="Georgia, serif" font-size="52" fill="{colors[4]}" font-weight="bold">Your Quote Here</text>
<text x="540" y="540" text-anchor="middle" font-family="Georgia, serif" font-size="52" fill="{colors[4]}" font-weight="bold">Second Line</text>
<!-- Divider -->
<line x1="440" y1="600" x2="640" y2="600" stroke="{colors[2]}" stroke-width="3"/>
<!-- Attribution -->
<text x="540" y="680" text-anchor="middle" font-family="Helvetica, sans-serif" font-size="28" fill="{colors[3]}">— Author Name —</text>
<!-- Bottom branding -->
<text x="540" y="960" text-anchor="middle" font-family="Helvetica, sans-serif" font-size="22" fill="{colors[2]}">@yourbrand</text>
{svg_footer()}'''
    
    elif template_type == "product":
        svg = f'''{svg_header(W, H)}
<rect width="{W}" height="{H}" fill="{colors[0]}"/>
<!-- Top accent bar -->
<rect x="0" y="0" width="{W}" height="12" fill="{colors[2]}"/>
<!-- Product placeholder -->
<rect x="340" y="120" width="400" height="400" fill="{colors[1]}" rx="20" stroke="{colors[3]}" stroke-width="2"/>
<text x="540" y="340" text-anchor="middle" font-family="Helvetica" font-size="60" fill="{colors[3]}">PRODUCT</text>
<!-- Product name -->
<text x="540" y="620" text-anchor="middle" font-family="Georgia, serif" font-size="44" fill="{colors[4]}" font-weight="bold">Product Name Here</text>
<!-- Price badge -->
<circle cx="540" cy="720" r="60" fill="{colors[2]}"/>
<text x="540" y="735" text-anchor="middle" font-family="Helvetica" font-size="32" fill="white" font-weight="bold">$29</text>
<!-- CTA -->
<rect x="390" y="850" width="300" height="60" fill="{colors[3]}" rx="30"/>
<text x="540" y="888" text-anchor="middle" font-family="Helvetica" font-size="24" fill="white">SHOP NOW</text>
<rect x="0" y="{H-12}" width="{W}" height="12" fill="{colors[2]}"/>
{svg_footer()}'''
    
    elif template_type == "checklist":
        svg = f'''{svg_header(W, H)}
<rect width="{W}" height="{H}" fill="{colors[0]}"/>
<!-- Header -->
<rect x="60" y="60" width="{W-120}" height="120" fill="{colors[2]}" rx="15"/>
<text x="540" y="130" text-anchor="middle" font-family="Georgia, serif" font-size="44" fill="white" font-weight="bold">5 WAYS TO...</text>
<!-- Checklist items -->
'''
        y = 240
        for i in range(5):
            svg += f'''<!-- Item {i+1} -->
<rect x="100" y="{y}" width="40" height="40" fill="none" stroke="{colors[3]}" stroke-width="3" rx="8"/>
<text x="170" y="{y+32}" font-family="Helvetica" font-size="32" fill="{colors[4]}">Checklist item {i+1}</text>
<line x1="170" y1="{y+55}" x2="900" y2="{y+55}" stroke="{colors[1]}" stroke-width="1"/>
'''
            y += 130
        svg += f'''<text x="540" y="{H-60}" text-anchor="middle" font-family="Helvetica" font-size="24" fill="{colors[2]}">@yourhandle</text>
{svg_footer()}'''
    
    return svg

def generate_instagram_carousel(palette_name, num_slides=5):
    """Generate a multi-slide Instagram carousel template (1080x1350 each)."""
    colors = PALETTES[palette_name]
    W, H = 1080, 1350
    slides = []
    
    # Slide 1: Cover
    slides.append(f'''{svg_header(W, H)}
<defs><linearGradient id="g1" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" style="stop-color:{colors[1]}"/><stop offset="100%" style="stop-color:{colors[3]}"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#g1)"/>
<text x="540" y="500" text-anchor="middle" font-family="Georgia, serif" font-size="64" fill="white" font-weight="bold">5 TIPS FOR</text>
<text x="540" y="580" text-anchor="middle" font-family="Georgia, serif" font-size="64" fill="white" font-weight="bold">YOUR TOPIC</text>
<rect x="440" y="650" width="200" height="4" fill="{colors[4]}"/>
<text x="540" y="720" text-anchor="middle" font-family="Helvetica" font-size="28" fill="{colors[0]}" opacity="0.8">Swipe to read →</text>
<text x="540" y="{H-80}" text-anchor="middle" font-family="Helvetica" font-size="22" fill="{colors[0]}">@yourbrand</text>
{svg_footer()}''')
    
    # Slides 2-4: Content
    for i in range(1, num_slides - 1):
        slides.append(f'''{svg_header(W, H)}
<rect width="{W}" height="{H}" fill="{colors[0]}"/>
<!-- Header bar -->
<rect x="0" y="0" width="{W}" height="80" fill="{colors[2]}"/>
<text x="540" y="52" text-anchor="middle" font-family="Georgia, serif" font-size="32" fill="white" font-weight="bold">Tip {i}: Title Here</text>
<!-- Content area -->
<rect x="80" y="140" width="{W-160}" height="{H-280}" fill="{colors[1]}" rx="20" opacity="0.3"/>
<!-- Number -->
<circle cx="540" cy="350" r="80" fill="{colors[2]}"/>
<text x="540" y="385" text-anchor="middle" font-family="Georgia, serif" font-size="80" fill="white" font-weight="bold">{i}</text>
<!-- Description -->
<text x="540" y="550" text-anchor="middle" font-family="Helvetica" font-size="32" fill="{colors[4]}">Your tip description</text>
<text x="540" y="600" text-anchor="middle" font-family="Helvetica" font-size="32" fill="{colors[4]}">goes here, multiline</text>
<!-- Slide indicator -->
<text x="540" y="{H-100}" text-anchor="middle" font-family="Helvetica" font-size="20" fill="{colors[2]}">{i} / {num_slides-2}</text>
{svg_footer()}''')
    
    # Last slide: CTA
    slides.append(f'''{svg_header(W, H)}
<rect width="{W}" height="{H}" fill="{colors[3]}"/>
<text x="540" y="500" text-anchor="middle" font-family="Georgia, serif" font-size="56" fill="white" font-weight="bold">Follow for more!</text>
<rect x="390" y="600" width="300" height="70" fill="{colors[4]}" rx="35"/>
<text x="540" y="648" text-anchor="middle" font-family="Helvetica" font-size="28" fill="white" font-weight="bold">FOLLOW @yourbrand</text>
<text x="540" y="780" text-anchor="middle" font-family="Helvetica" font-size="24" fill="{colors[0]}">Save this post for later</text>
<text x="540" y="{H-80}" text-anchor="middle" font-family="Helvetica" font-size="20" fill="{colors[0]}">© Your Brand 2026</text>
{svg_footer()}''')
    
    return slides

def generate_business_card(palette_name, side="front"):
    """Generate business card template (1050x600 = 3.5x2 at 300dpi)."""
    colors = PALETTES[palette_name]
    W, H = 1050, 600
    
    if side == "front":
        return f'''{svg_header(W, H)}
<defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:{colors[3]}"/><stop offset="100%" style="stop-color:{colors[4]}"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<!-- Accent line -->
<rect x="0" y="588" width="{W}" height="12" fill="{colors[2]}"/>
<!-- Name -->
<text x="525" y="220" text-anchor="middle" font-family="Georgia, serif" font-size="42" fill="white" font-weight="bold">YOUR NAME</text>
<!-- Title -->
<text x="525" y="270" text-anchor="middle" font-family="Helvetica" font-size="22" fill="{colors[2]}">Your Title | Your Business</text>
<!-- Contact -->
<text x="525" y="380" text-anchor="middle" font-family="Helvetica" font-size="18" fill="white">your@email.com | (555) 123-4567</text>
<text x="525" y="420" text-anchor="middle" font-family="Helvetica" font-size="18" fill="white">www.yourwebsite.com</text>
{svg_footer()}'''
    else:
        return f'''{svg_header(W, H)}
<rect width="{W}" height="{H}" fill="{colors[0]}"/>
<!-- Logo placeholder -->
<rect x="425" y="200" width="200" height="200" fill="none" stroke="{colors[3]}" stroke-width="4" rx="16"/>
<text x="525" y="310" text-anchor="middle" font-family="Georgia, serif" font-size="48" fill="{colors[3]}" font-weight="bold">LOGO</text>
<rect x="0" y="0" width="12" height="{H}" fill="{colors[2]}"/>
{svg_footer()}'''

def generate_wedding_invitation(palette_name):
    """Generate wedding invitation template (1080x1080)."""
    colors = PALETTES[palette_name]
    W, H = 1080, 1080
    
    return f'''{svg_header(W, H)}
<rect width="{W}" height="{H}" fill="{colors[0]}"/>
<!-- Floral border (decorative) -->
<rect x="50" y="50" width="{W-100}" height="{H-100}" fill="none" stroke="{colors[2]}" stroke-width="2" rx="15"/>
<rect x="65" y="65" width="{W-130}" height="{H-130}" fill="none" stroke="{colors[1]}" stroke-width="1" rx="12"/>
<!-- Top decoration -->
<text x="540" y="200" text-anchor="middle" font-family="Helvetica" font-size="22" fill="{colors[3]}">TOGETHER WITH THEIR FAMILIES</text>
<!-- Names -->
<text x="540" y="340" text-anchor="middle" font-family="Georgia, serif" font-size="64" fill="{colors[4]}" font-weight="bold">Jane &amp; John</text>
<!-- Divider -->
<line x1="390" y1="400" x2="690" y2="400" stroke="{colors[2]}" stroke-width="2"/>
<!-- Date -->
<text x="540" y="480" text-anchor="middle" font-family="Helvetica" font-size="28" fill="{colors[3]}">SATURDAY, JUNE 14, 2026</text>
<text x="540" y="530" text-anchor="middle" font-family="Helvetica" font-size="28" fill="{colors[3]}">AT FOUR O'CLOCK</text>
<!-- Venue -->
<text x="540" y="620" text-anchor="middle" font-family="Georgia, serif" font-size="32" fill="{colors[4]}">The Garden Venue</text>
<text x="540" y="660" text-anchor="middle" font-family="Helvetica" font-size="24" fill="{colors[3]}">123 Garden Street, City, State</text>
<!-- RSVP -->
<rect x="420" y="760" width="240" height="50" fill="{colors[2]}" rx="25"/>
<text x="540" y="793" text-anchor="middle" font-family="Helvetica" font-size="20" fill="white">RSVP by May 1st</text>
<!-- Bottom -->
<text x="540" y="920" text-anchor="middle" font-family="Georgia" font-size="36" fill="{colors[2]}">&amp;</text>
<text x="540" y="980" text-anchor="middle" font-family="Helvetica" font-size="18" fill="{colors[3]}">Reception to follow</text>
{svg_footer()}'''

def generate_birthday_invitation(palette_name, theme="general"):
    """Generate birthday invitation template (1080x1080)."""
    colors = PALETTES[palette_name]
    W, H = 1080, 1080
    
    return f'''{svg_header(W, H)}
<defs><radialGradient id="bg" cx="50%" cy="50%" r="70%">
<stop offset="0%" style="stop-color:{colors[1]}"/><stop offset="100%" style="stop-color:{colors[0]}"/></radialGradient></defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<!-- Confetti -->
<circle cx="200" cy="150" r="12" fill="{colors[2]}"/>
<circle cx="850" cy="120" r="15" fill="{colors[3]}"/>
<circle cx="150" cy="800" r="10" fill="{colors[3]}"/>
<circle cx="900" cy="700" r="14" fill="{colors[2]}"/>
<rect x="300" y="100" width="20" height="20" fill="{colors[3]}" transform="rotate(45 310 110)"/>
<rect x="750" y="850" width="18" height="18" fill="{colors[2]}" transform="rotate(30 759 859)"/>
<!-- Title -->
<text x="540" y="300" text-anchor="middle" font-family="Georgia, serif" font-size="32" fill="{colors[3]}">YOU'RE INVITED TO</text>
<!-- Birthday person name -->
<text x="540" y="440" text-anchor="middle" font-family="Georgia, serif" font-size="72" fill="{colors[4]}" font-weight="bold">BIRTHDAY</text>
<text x="540" y="510" text-anchor="middle" font-family="Georgia, serif" font-size="56" fill="{colors[4]}" font-weight="bold">PARTY!</text>
<!-- Details -->
<text x="540" y="640" text-anchor="middle" font-family="Helvetica" font-size="28" fill="{colors[3]}">Join us to celebrate</text>
<text x="540" y="680" text-anchor="middle" font-family="Georgia, serif" font-size="40" fill="{colors[4]}">[Name's] Special Day</text>
<!-- When & Where -->
<text x="540" y="780" text-anchor="middle" font-family="Helvetica" font-size="24" fill="{colors[3]}">Saturday, March 15, 2026 at 2:00 PM</text>
<text x="540" y="820" text-anchor="middle" font-family="Helvetica" font-size="24" fill="{colors[3]}">Party Venue, 123 Main Street</text>
<!-- RSVP -->
<text x="540" y="920" text-anchor="middle" font-family="Helvetica" font-size="22" fill="{colors[2]}">RSVP: your@email.com</text>
{svg_footer()}'''

def generate_matchbook_poster(palette_name):
    """Generate matchbook poster (couple photo collage template, 1080x1080)."""
    colors = PALETTES[palette_name]
    W, H = 1080, 1080
    
    svg = f'''{svg_header(W, H)}
<rect width="{W}" height="{H}" fill="{colors[0]}"/>
<rect x="80" y="80" width="{W-160}" height="{H-160}" fill="none" stroke="{colors[3]}" stroke-width="4" rx="8"/>
'''
    pw, ph = 320, 200
    sx, sy = 130, 130
    for r in range(3):
        for c in range(2):
            x = sx + c * (pw + 60)
            y = sy + r * (ph + 70)
            svg += f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="{colors[1]}" stroke="{colors[2]}" stroke-width="2" rx="4"/>\n'
            svg += f'<text x="{x+pw//2}" y="{y+ph//2}" text-anchor="middle" font-family="Helvetica" font-size="18" fill="{colors[3]}" opacity="0.5">PHOTO {r*2+c+1}</text>\n'
    svg += f'<text x="540" y="{H-120}" text-anchor="middle" font-family="Georgia, serif" font-size="32" fill="{colors[4]}" font-weight="bold">OUR STORY</text>\n'
    svg += svg_footer()
    return svg


if __name__ == "__main__":
    print("=" * 60)
    print("Canva-Alternative Template Generator")
    print("Original CC0 templates - no Canva account needed")
    print("=" * 60)
    
    total = 0
    
    for palette in PALETTES:
        # Instagram posts
        for template_type in ["quote", "product", "checklist"]:
            svg = generate_instagram_post(palette, template_type)
            fname = f"ig_post_{template_type}_{palette}.svg"
            with open(os.path.join(TEMPLATE_DIR, fname), "w", encoding="utf-8") as f:
                f.write(svg)
            total += 1
        
        # Instagram carousel (3 slides per palette)
        slides = generate_instagram_carousel(palette, num_slides=5)
        for i, slide in enumerate(slides):
            fname = f"ig_carousel_slide{i+1}_{palette}.svg"
            with open(os.path.join(TEMPLATE_DIR, fname), "w", encoding="utf-8") as f:
                f.write(slide)
            total += 1
        
        # Business cards (front + back)
        for side in ["front", "back"]:
            svg = generate_business_card(palette, side)
            fname = f"business_card_{side}_{palette}.svg"
            with open(os.path.join(TEMPLATE_DIR, fname), "w", encoding="utf-8") as f:
                f.write(svg)
            total += 1
        
        # Wedding invitation
        svg = generate_wedding_invitation(palette)
        with open(os.path.join(TEMPLATE_DIR, f"wedding_invitation_{palette}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        total += 1
        
        # Birthday invitation
        svg = generate_birthday_invitation(palette)
        with open(os.path.join(TEMPLATE_DIR, f"birthday_invitation_{palette}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        total += 1
        
        # Matchbook poster
        svg = generate_matchbook_poster(palette)
        with open(os.path.join(TEMPLATE_DIR, f"matchbook_poster_{palette}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        total += 1
    
    # Generate usage guide
    guide = """# Canva-Alternative Templates

These are original CC0 SVG templates that replace Canva-dependent Etsy listings.
No Canva account needed — open in any browser, edit the text/colors, export to PNG/PDF.

## How to Use

1. Open any .svg file in a text editor (Notepad, VS Code, etc.)
2. Change text values (look for `<text>` tags)
3. Change colors by editing the hex color codes (e.g., `#E8B4B8`)
4. Open in a browser to preview
5. Right-click → Save as, or use a free tool (Inkscape, Photopea, Figma)

## Template Types

| Template | Size | Etsy Listings Covered |
|---|---|---|
| Instagram Post (Quote) | 1080x1080 | Social media template bundles |
| Instagram Post (Product) | 1080x1080 | Product marketing templates |
| Instagram Post (Checklist) | 1080x1080 | Content creator kits |
| Instagram Carousel (5 slides) | 1080x1350 | Carousel template bundles |
| Business Card (Front+Back) | 1050x600 | Business card templates |
| Wedding Invitation | 1080x1080 | Wedding invitation suites |
| Birthday Invitation | 1080x1080 | Birthday invitation templates |
| Matchbook Poster | 1080x1080 | Couple photo collage templates |

## Color Palettes Available

Blush, Sage, Navy/Gold, Boho, Minimalist, Coastal, Dark Academia, Cottagecore

## Free Tools for Editing SVGs

- [Inkscape](https://inkscape.org) — Free, open-source vector editor
- [Photopea](https://www.photopea.com) — Free, browser-based
- [Figma](https://www.figma.com) — Free for individuals
- [SVG Viewer](https://www.svgviewer.dev) — Quick browser preview
- Any text editor — SVGs are just XML text files

## License
All templates are CC0 (Public Domain). Free for commercial use, no attribution required.
"""
    guide_path = os.path.join(TEMPLATE_DIR, "README.md")
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(guide)
    
    print(f"\nGenerated {total} templates in {len(PALETTES)} palettes")
    print(f"Saved to: {TEMPLATE_DIR}")
    print(f"Templates: IG Posts, IG Carousels, Business Cards, Invitations, Matchbook Posters")
    print(f"License: CC0 - Free for commercial use")
