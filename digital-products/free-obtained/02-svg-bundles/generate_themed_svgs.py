"""
Generate themed SVG packs matching specific Etsy listings.
Creates original CC0 SVG designs for: Bible/Christian, Halloween, Fall/Autumn,
Floral/Botanical, Pokemon-style, and Sarcastic/Funny designs.
"""
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
THEMED_DIR = os.path.join(OUTPUT_DIR, "svg-bundles", "themed-packs")
os.makedirs(THEMED_DIR, exist_ok=True)

def save_svg(name, content, subfolder=""):
    d = os.path.join(THEMED_DIR, subfolder) if subfolder else THEMED_DIR
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{name}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

# Christian/Bible SVG pack (matches "100 Bible Verse SVG Bundle")
def generate_christian_pack():
    """Original Christian-themed SVG designs (CC0)."""
    d = "christian-faith"
    count = 0
    
    items = [
        ("cross_simple", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="42" y="10" width="16" height="80" fill="#8B4513"/><rect x="25" y="30" width="50" height="16" fill="#8B4513"/></svg>'),
        ("cross_celtic", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="#4A3424" stroke-width="4"/><rect x="42" y="15" width="16" height="70" fill="none" stroke="#4A3424" stroke-width="4"/><rect x="20" y="42" width="60" height="16" fill="none" stroke="#4A3424" stroke-width="4"/><circle cx="50" cy="50" r="8" fill="#E8C468"/></svg>'),
        ("dove_peace", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><path d="M20 50 Q30 20 60 25 Q70 15 75 20 Q65 35 70 45 Q60 55 45 55 Q35 60 20 50 Z" fill="white" stroke="#666" stroke-width="1.5"/><circle cx="72" cy="22" r="2" fill="#333"/><path d="M60 28 Q65 25 68 28" fill="none" stroke="#FFD700" stroke-width="2"/></svg>'),
        ("fish_ichthys", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 60"><path d="M10 30 Q30 5 60 30 Q30 55 10 30 Z M55 30 Q70 15 90 5 L100 30 L90 55 Q70 45 55 30" fill="none" stroke="#2C3E50" stroke-width="3"/></svg>'),
        ("bible_book", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><rect x="15" y="10" width="70" height="60" rx="3" fill="#8B4513" stroke="#5C3D2E" stroke-width="2"/><rect x="20" y="15" width="60" height="50" fill="#F5EBE0"/><line x1="50" y1="15" x2="50" y2="65" stroke="#8B4513" stroke-width="2"/><text x="35" y="42" font-size="10" fill="#8B4513" font-family="serif">HOLY</text><text x="57" y="42" font-size="10" fill="#8B4513" font-family="serif">BIBLE</text><rect x="48" y="10" width="4" height="60" fill="#E8C468"/></svg>'),
        ("praying_hands", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100"><path d="M30 90 L25 50 Q25 35 35 30 Q40 25 45 30 L50 50 L55 30 Q60 25 65 30 Q70 35 60 55 L50 90 Z" fill="#D4A574" stroke="#8B5E3C" stroke-width="1.5"/><path d="M40 70 L45 70 L45 50 L40 50 Z" fill="#8B5E3C" opacity="0.3"/></svg>'),
        ("angel_wings", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80"><path d="M60 40 Q40 20 20 25 Q30 35 25 50 Q35 45 40 55 Q50 45 55 50 Z" fill="white" stroke="#999" stroke-width="1"/><path d="M60 40 Q80 20 100 25 Q90 35 95 50 Q85 45 80 55 Q70 45 65 50 Z" fill="white" stroke="#999" stroke-width="1"/><text x="60" y="75" text-anchor="middle" font-size="12" fill="#C49B6C">✝</text></svg>'),
        ("church_building", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="25" y="40" width="50" height="55" fill="#8B7355" stroke="#5C3D2E" stroke-width="2"/><polygon points="20,42 50,15 80,42" fill="#6B4423" stroke="#5C3D2E" stroke-width="2"/><rect x="46" y="5" width="8" height="15" fill="#4A3424"/><rect x="40" y="60" width="20" height="35" fill="#5C3D2E"/><circle cx="50" cy="35" r="6" fill="#E8C468" stroke="#4A3424" stroke-width="1.5"/><text x="50" y="39" text-anchor="middle" font-size="8" fill="#4A3424">✝</text></svg>'),
        ("hearts_faith", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 90 L20 55 Q10 40 15 30 Q25 15 35 25 Q42 15 50 25 Q58 15 65 25 Q75 15 85 30 Q90 40 80 55 Z" fill="#E8B4B8"/><text x="50" y="55" text-anchor="middle" font-size="20" fill="#8B5E5A">✝</text></svg>'),
        ("olive_branch", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60"><path d="M10 30 Q30 25 50 30 Q70 35 90 30" fill="none" stroke="#556B2F" stroke-width="3"/><ellipse cx="25" cy="22" rx="6" ry="3" fill="#6B8E6B" transform="rotate(-20 25 22)"/><ellipse cx="35" cy="35" rx="6" ry="3" fill="#6B8E6B" transform="rotate(25 35 35)"/><ellipse cx="55" cy="24" rx="6" ry="3" fill="#6B8E6B" transform="rotate(-15 55 24)"/><ellipse cx="65" cy="36" rx="6" ry="3" fill="#6B8E6B" transform="rotate(20 65 36)"/><ellipse cx="80" cy="25" rx="6" ry="3" fill="#6B8E6B" transform="rotate(-25 80 25)"/><circle cx="88" cy="28" r="4" fill="#556B2F"/></svg>'),
    ]
    
    for name, svg in items:
        save_svg(name, svg, d)
        count += 1
    return count

# Halloween SVG pack (matches "Halloween SVG Mega Bundle 2000+")
def generate_halloween_pack():
    """Original Halloween-themed SVG designs (CC0)."""
    d = "halloween"
    count = 0
    
    items = [
        ("ghost_cute", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120"><path d="M50 10 Q25 10 25 40 L25 100 Q30 95 35 100 Q40 95 45 100 Q50 95 55 100 Q60 95 65 100 Q70 95 75 100 L75 40 Q75 10 50 10 Z" fill="white" stroke="#D5CFC7" stroke-width="2"/><circle cx="38" cy="45" r="6" fill="#333"/><circle cx="62" cy="45" r="6" fill="#333"/><path d="M42 60 Q50 68 58 60" fill="none" stroke="#333" stroke-width="2"/></svg>'),
        ("pumpkin_jack", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 100"><ellipse cx="60" cy="60" rx="45" ry="35" fill="#FF7518"/><ellipse cx="40" cy="60" rx="15" ry="32" fill="#FF8C00"/><ellipse cx="80" cy="60" rx="15" ry="32" fill="#FF8C00"/><rect x="55" y="15" width="10" height="20" fill="#228B22"/><polygon points="60,25 55,10 65,10" fill="#FF6347"/><polygon points="45,55 55,55 50,50" fill="#333"/><polygon points="65,55 75,55 70,50" fill="#333"/><path d="M45 70 Q50 75 55 73 Q60 75 65 73 Q70 75 75 70" fill="none" stroke="#333" stroke-width="3"/></svg>'),
        ("bat_flying", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 60"><path d="M60 30 Q55 20 50 25 Q40 15 25 20 Q35 10 15 15 Q20 5 5 10 Q15 15 10 25 Q25 20 35 25 Q45 15 50 25 L60 30 Q70 25 75 15 Q85 15 90 25 Q100 20 115 25 Q105 15 110 5 Q95 5 100 15 Q85 10 75 20 Q70 15 65 25 Q65 25 60 30" fill="#2C2C2C"/></svg>'),
        ("spider_web", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><g stroke="#999" stroke-width="1" fill="none"><line x1="50" y1="50" x2="50" y2="5"/><line x1="50" y1="50" x2="95" y2="20"/><line x1="50" y1="50" x2="95" y2="80"/><line x1="50" y1="50" x2="50" y2="95"/><line x1="50" y1="50" x2="5" y2="80"/><line x1="50" y1="50" x2="5" y2="20"/><path d="M50 20 Q70 25 75 50"/><path d="M50 35 Q65 38 68 50"/><path d="M50 15 Q75 22 85 50 Q85 75 50 85 Q15 75 15 50 Q25 22 50 15"/><path d="M50 30 Q60 32 65 50"/></g></svg>'),
        ("witch_hat", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><ellipse cx="50" cy="75" rx="40" ry="10" fill="#4A0033"/><path d="M20 75 Q25 50 40 25 Q50 5 55 25 Q65 50 80 75 Z" fill="#2D0033"/><rect x="15" y="70" width="70" height="12" fill="#E8C468"/><rect x="15" y="82" width="70" height="3" fill="#C49500"/><circle cx="35" cy="76" r="4" fill="#FFD700"/></svg>'),
        ("skull_jolly", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 10 Q20 10 20 45 Q20 58 28 65 L28 78 L38 78 L38 72 L42 72 L42 78 L58 78 L58 72 L62 72 L62 78 L72 78 L72 65 Q80 58 80 45 Q80 10 50 10 Z" fill="#F5F0E8" stroke="#CCC" stroke-width="1"/><ellipse cx="38" cy="42" rx="8" ry="10" fill="#333"/><ellipse cx="62" cy="42" rx="8" ry="10" fill="#333"/><polygon points="45,58 50,65 55,58" fill="#333"/><line x1="38" y1="65" x2="38" y2="72" stroke="#333" stroke-width="2"/><line x1="42" y1="65" x2="42" y2="72" stroke="#333" stroke-width="2"/><line x1="46" y1="65" x2="46" y2="72" stroke="#333" stroke-width="2"/><line x1="54" y1="65" x2="54" y2="72" stroke="#333" stroke-width="2"/><line x1="58" y1="65" x2="58" y2="72" stroke="#333" stroke-width="2"/><line x1="62" y1="65" x2="62" y2="72" stroke="#333" stroke-width="2"/></svg>'),
        ("cauldron", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><path d="M15 35 Q15 65 50 65 Q85 65 85 35 Z" fill="#2D2D2D"/><ellipse cx="50" cy="35" rx="35" ry="8" fill="#1A1A1A"/><ellipse cx="50" cy="33" rx="30" ry="5" fill="#4A0080" opacity="0.5"/><rect x="10" y="32" width="80" height="6" fill="#333"/><circle cx="30" cy="25" r="6" fill="#9370DB" opacity="0.4"/><circle cx="50" cy="20" r="5" fill="#9370DB" opacity="0.4"/><circle cx="65" cy="28" r="4" fill="#9370DB" opacity="0.4"/></svg>'),
        ("candle_spooky", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 100"><rect x="22" y="40" width="16" height="55" fill="#E8E2D5"/><rect x="22" y="40" width="16" height="5" fill="#C4B998"/><path d="M30 40 Q25 30 30 15 Q35 30 30 40" fill="#FFD700"/><path d="M30 35 Q27 28 30 20 Q33 28 30 35" fill="#FFA500"/><circle cx="30" cy="25" r="3" fill="#FFFFFF" opacity="0.3"/></svg>'),
        ("haunted_house", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 100"><rect x="30" y="45" width="60" height="55" fill="#2D2D2D"/><polygon points="25,48 60,20 95,48" fill="#1A1A1A"/><rect x="50" y="10" width="12" height="15" fill="#1A1A1A"/><rect x="48" y="8" width="16" height="4" fill="#4A0033"/><rect x="45" y="60" width="12" height="20" fill="#FFD700" opacity="0.3"/><rect x="65" y="60" width="12" height="20" fill="#FFD700" opacity="0.3"/><circle cx="80" cy="55" r="3" fill="#FF0000" opacity="0.5"/><polygon points="30,100 0,100 20,80" fill="#1A1A1A"/><polygon points="90,100 120,100 100,80" fill="#1A1A1A"/></svg>'),
        ("candy_corn", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 80"><polygon points="30,5 50,75 10,75" fill="#FFD700"/><polygon points="30,5 35,75 25,75" fill="#FFFFFF"/><polygon points="25,75 35,75 30,75" fill="#FF6347"/><polygon points="30,5 50,75 40,75" fill="#FF8C00"/></svg>'),
        ("mummy", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100"><ellipse cx="40" cy="35" rx="22" ry="25" fill="#E8E2D5"/><g stroke="#D5CFC7" stroke-width="4" fill="none"><path d="M20 20 Q40 15 60 20"/><path d="M18 30 Q40 35 62 30"/><path d="M20 40 Q40 45 60 40"/><path d="M18 50 Q40 55 62 50"/><path d="M20 60 Q40 65 60 60"/><path d="M25 70 Q40 75 55 70"/></g><circle cx="33" cy="35" r="4" fill="#006400"/><circle cx="47" cy="35" r="4" fill="#006400"/></svg>'),
        ("vampire_bat", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><ellipse cx="50" cy="40" rx="15" ry="18" fill="#1A1A1A"/><polygon points="38,25 35,10 45,20" fill="#1A1A1A"/><polygon points="62,25 65,10 55,20" fill="#1A1A1A"/><path d="M50 40 Q30 20 10 30 L20 50 Q35 45 45 50 Z" fill="#1A1A1A"/><path d="M50 40 Q70 20 90 30 L80 50 Q65 45 55 50 Z" fill="#1A1A1A"/><circle cx="45" cy="38" r="3" fill="#FF0000"/><circle cx="55" cy="38" r="3" fill="#FF0000"/><path d="M45 50 L47 55 L49 50 L51 55 L53 50 L55 55" fill="#FFFFFF"/></svg>'),
        ("potion_bottle", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100"><rect x="32" y="8" width="16" height="12" fill="#5C3D2E"/><path d="M30 20 Q15 35 20 50 L20 85 Q20 95 60 95 L60 85 Q65 50 50 20 Z" fill="#4A6B4A" stroke="#3A5A3A" stroke-width="2"/><ellipse cx="40" cy="40" rx="15" ry="8" fill="#6B8E6B" opacity="0.5"/><circle cx="35" cy="55" r="3" fill="#90EE90" opacity="0.3"/><circle cx="45" cy="65" r="2" fill="#90EE90" opacity="0.3"/></svg>'),
    ]
    
    for name, svg in items:
        save_svg(name, svg, d)
        count += 1
    return count

# Fall/Autumn SVG pack (matches "Fall svg bundle, Fall svg")
def generate_fall_pack():
    """Original Fall/Autumn-themed SVG designs (CC0)."""
    d = "fall-autumn"
    count = 0
    
    items = [
        ("maple_leaf", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 10 L45 25 L30 20 L35 35 L20 35 L30 45 L15 50 L30 55 L25 70 L40 60 L50 90 L60 60 L75 70 L70 55 L85 50 L70 45 L80 35 L65 35 L70 20 L55 25 Z" fill="#D2691E" stroke="#8B4513" stroke-width="1"/><line x1="50" y1="50" x2="50" y2="95" stroke="#8B4513" stroke-width="3"/></svg>'),
        ("oak_leaf", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100"><path d="M40 10 Q30 15 25 10 Q20 15 15 25 Q10 30 15 35 Q10 40 15 45 Q10 50 20 55 Q15 65 25 70 Q30 75 40 90 Q50 75 55 70 Q65 65 60 55 Q65 50 60 45 Q65 40 60 35 Q65 30 60 25 Q55 15 50 10 Q45 15 40 10 Z" fill="#CD853F" stroke="#8B5E3C" stroke-width="1"/><line x1="40" y1="50" x2="40" y2="95" stroke="#8B5E3C" stroke-width="2"/></svg>'),
        ("acorn", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 80"><ellipse cx="30" cy="35" rx="18" ry="20" fill="#D4A574"/><path d="M12 25 Q12 15 20 12 Q30 8 40 12 Q48 15 48 25 Q48 30 40 28 Q30 25 20 28 Q12 30 12 25" fill="#5C3D2E"/><line x1="30" y1="55" x2="30" y2="75" stroke="#8B5E3C" stroke-width="2"/><path d="M28 75 L25 72 M32 75 L35 72" stroke="#8B5E3C" stroke-width="1"/></svg>'),
        ("pumpkin_fall", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><ellipse cx="50" cy="50" rx="38" ry="28" fill="#D2691E"/><ellipse cx="33" cy="50" rx="12" ry="26" fill="#CD853F"/><ellipse cx="67" cy="50" rx="12" ry="26" fill="#CD853F"/><rect x="47" y="18" width="6" height="15" fill="#556B2F"/><path d="M50 22 Q55 15 60 18" fill="none" stroke="#556B2F" stroke-width="2"/></svg>'),
        ("wheat_bundle", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100"><g fill="#D4A574"><ellipse cx="30" cy="20" rx="3" ry="8"/><ellipse cx="40" cy="18" rx="3" ry="8"/><ellipse cx="50" cy="20" rx="3" ry="8"/><ellipse cx="32" cy="35" rx="3" ry="8"/><ellipse cx="40" cy="33" rx="3" ry="8"/><ellipse cx="48" cy="35" rx="3" ry="8"/><line x1="30" y1="25" x2="25" y2="85" stroke="#C49B6C" stroke-width="2"/><line x1="40" y1="23" x2="40" y2="90" stroke="#C49B6C" stroke-width="2"/><line x1="50" y1="25" x2="55" y2="85" stroke="#C49B6C" stroke-width="2"/></g><path d="M20 85 Q40 80 60 85" fill="none" stroke="#8B5E3C" stroke-width="3"/></svg>'),
        ("mug_cocoa", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><path d="M20 25 L20 60 Q20 75 40 75 L55 75 Q75 75 75 60 L75 25 Z" fill="#F5EBE0"/><path d="M75 35 Q90 35 90 50 Q90 65 75 60" fill="none" stroke="#F5EBE0" stroke-width="5"/><ellipse cx="47" cy="25" rx="27" ry="5" fill="#8B5E3C"/><circle cx="38" cy="23" r="4" fill="#F5F5F5"/><circle cx="50" cy="21" r="3" fill="#F5F5F5"/><circle cx="58" cy="24" r="3" fill="#F5F5F5"/></svg>'),
        ("scarecrow", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100"><polygon points="10,90 40,30 70,90" fill="#D4A574"/><rect x="35" y="40" width="10" height="50" fill="#8B5E3C"/><circle cx="40" cy="25" r="15" fill="#F5EBE0"/><circle cx="35" cy="23" r="3" fill="#333"/><circle cx="45" cy="23" r="3" fill="#333"/><path d="M33 30 Q40 33 47 30" fill="none" stroke="#333" stroke-width="1.5"/><polygon points="20,25 35,15 30,30" fill="#D4A574"/><polygon points="60,25 45,15 50,30" fill="#D4A574"/></svg>'),
        ("corn_cob", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 100"><ellipse cx="30" cy="40" rx="15" ry="35" fill="#FFD700"/><g fill="#FFA500"><circle cx="22" cy="20" r="3"/><circle cx="30" cy="18" r="3"/><circle cx="38" cy="20" r="3"/><circle cx="20" cy="30" r="3"/><circle cx="28" cy="28" r="3"/><circle cx="36" cy="30" r="3"/><circle cx="40" cy="40" r="3"/><circle cx="20" cy="42" r="3"/><circle cx="30" cy="40" r="3"/><circle cx="22" cy="52" r="3"/><circle cx="30" cy="50" r="3"/><circle cx="38" cy="52" r="3"/><circle cx="25" cy="62" r="3"/><circle cx="35" cy="62" r="3"/></g><path d="M15 10 Q20 5 25 15 M35 15 Q40 5 45 10" fill="none" stroke="#556B2F" stroke-width="3"/></svg>'),
        ("muxu_leaf", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><path d="M50 10 Q70 25 75 40 Q70 55 50 70 Q30 55 25 40 Q30 25 50 10 Z" fill="#B8860B"/><line x1="50" y1="10" x2="50" y2="70" stroke="#8B4513" stroke-width="2"/><path d="M50 25 Q60 30 65 40" fill="none" stroke="#8B4513" stroke-width="1"/><path d="M50 25 Q40 30 35 40" fill="none" stroke="#8B4513" stroke-width="1"/><path d="M50 45 Q60 50 65 55" fill="none" stroke="#8B4513" stroke-width="1"/><path d="M50 45 Q40 50 35 55" fill="none" stroke="#8B4513" stroke-width="1"/></svg>'),
    ]
    
    for name, svg in items:
        save_svg(name, svg, d)
        count += 1
    return count

# Floral/Botanical SVG pack (matches "Fall Png Bundle, Fall vibes png")
def generate_floral_pack():
    """Original floral/botanical SVG designs (CC0)."""
    d = "floral-botanical"
    count = 0
    
    items = [
        ("rose_simple", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80"><circle cx="40" cy="35" r="20" fill="#E8B4B8"/><path d="M30 35 Q35 25 40 35 Q45 25 50 35" fill="none" stroke="#C49B6C" stroke-width="2"/><circle cx="40" cy="35" r="10" fill="#D4A5A5"/><circle cx="40" cy="35" r="5" fill="#8B5E5A"/><path d="M40 55 L38 70 M40 55 L42 70" stroke="#556B2F" stroke-width="2"/><path d="M35 60 Q25 65 20 55" fill="#6B8E6B" stroke="#556B2F" stroke-width="1"/><path d="M45 60 Q55 65 60 55" fill="#6B8E6B" stroke="#556B2F" stroke-width="1"/></svg>'),
        ("sunflower", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="18" fill="#4A3424"/><g fill="#FFD700"><ellipse cx="50" cy="20" rx="8" ry="18"/><ellipse cx="50" cy="80" rx="8" ry="18"/><ellipse cx="20" cy="50" rx="18" ry="8"/><ellipse cx="80" cy="50" rx="18" ry="8"/><ellipse cx="30" cy="30" rx="14" ry="8" transform="rotate(-45 30 30)"/><ellipse cx="70" cy="30" rx="14" ry="8" transform="rotate(45 70 30)"/><ellipse cx="30" cy="70" rx="14" ry="8" transform="rotate(45 30 70)"/><ellipse cx="70" cy="70" rx="14" ry="8" transform="rotate(-45 70 70)"/></g><circle cx="50" cy="50" r="14" fill="#3D2B1E"/></svg>'),
        ("tulip", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 100"><path d="M30 10 Q15 10 12 30 Q12 40 20 35 Q25 40 30 35 Q35 40 40 35 Q48 40 48 30 Q45 10 30 10" fill="#E8B4B8"/><path d="M22 35 Q25 30 30 35 Q35 30 38 35" fill="#D4A5A5"/><line x1="30" y1="35" x2="28" y2="90" stroke="#556B2F" stroke-width="3"/><path d="M28 60 Q15 55 12 70" fill="#6B8E6B" stroke="#556B2F" stroke-width="1.5"/></svg>'),
        ("daisy_chain", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 60"><g><circle cx="30" cy="30" r="6" fill="#FFD700"/><g fill="white"><circle cx="30" cy="18" r="6"/><circle cx="42" cy="30" r="6"/><circle cx="30" cy="42" r="6"/><circle cx="18" cy="30" r="6"/></g></g><g><circle cx="70" cy="30" r="6" fill="#FFD700"/><g fill="white"><circle cx="70" cy="18" r="6"/><circle cx="82" cy="30" r="6"/><circle cx="70" cy="42" r="6"/><circle cx="58" cy="30" r="6"/></g></g><path d="M36 30 Q50 25 64 30" fill="none" stroke="#556B2F" stroke-width="2"/></svg>'),
        ("eucalyptus_branch", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60"><path d="M5 30 Q30 25 55 30 Q80 35 95 30" fill="none" stroke="#556B2F" stroke-width="2"/><ellipse cx="15" cy="22" rx="5" ry="9" fill="#8FBC8F" transform="rotate(-20 15 22)"/><ellipse cx="25" cy="35" rx="5" ry="9" fill="#8FBC8F" transform="rotate(25 25 35)"/><ellipse cx="40" cy="24" rx="5" ry="9" fill="#8FBC8F" transform="rotate(-15 40 24)"/><ellipse cx="50" cy="36" rx="5" ry="9" fill="#8FBC8F" transform="rotate(20 50 36)"/><ellipse cx="65" cy="24" rx="5" ry="9" fill="#8FBC8F" transform="rotate(-20 65 24)"/><ellipse cx="75" cy="36" rx="5" ry="9" fill="#8FBC8F" transform="rotate(15 75 36)"/><ellipse cx="88" cy="26" rx="4" ry="8" fill="#8FBC8F" transform="rotate(-25 88 26)"/></svg>'),
        ("wreath_botanical", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="35" fill="none" stroke="#556B2F" stroke-width="12" opacity="0.5"/><g fill="#6B8E6B"><ellipse cx="50" cy="10" rx="8" ry="4"/><ellipse cx="80" cy="25" rx="4" ry="8"/><ellipse cx="90" cy="50" rx="8" ry="4"/><ellipse cx="80" cy="75" rx="4" ry="8"/><ellipse cx="50" cy="90" rx="8" ry="4"/><ellipse cx="20" cy="75" rx="4" ry="8"/><ellipse cx="10" cy="50" rx="8" ry="4"/><ellipse cx="20" cy="25" rx="4" ry="8"/></g><g fill="#E8B4B8"><circle cx="50" cy="10" r="4"/><circle cx="80" cy="25" r="3"/><circle cx="20" cy="75" r="3"/></g></svg>'),
    ]
    
    for name, svg in items:
        save_svg(name, svg, d)
        count += 1
    return count

# Sarcastic/Funny SVG pack (matches "Funny Sarcastic SVG Quotes Bundle")
def generate_sarcastic_pack():
    """Original sarcastic/funny SVG quote designs (CC0)."""
    d = "sarcastic-funny"
    count = 0
    
    quotes = [
        ("well_that_didnt", 'Well, That Didn\'t Go As Planned', "react", "sarcasm"),
        ("not_today", 'Not Today, Satan', "angry", "attitude"),
        ("coffee_first", 'But First, Coffee', "casual", "coffee"),
        ("nap_time", 'I Need A Nap', "center", "nap"),
        ("send_help", 'Send Help And Snacks', "middle", "snacks"),
        ("adulting_hard", 'Adulting Is Hard', "top", "adulting"),
        ("too_old", "I'm Too Old For This", "middle", "age"),
        ("bless_your_heart", 'Bless Your Heart', "center", "southern"),
        ("did_i_say_that", "I Never Said I Was Smart", "bottom", "honest"),
        ("hide_snacks", 'I\'m Hiding Snacks. Don\'t Tell My Kids', "middle", "parenting"),
    ]
    
    for name, quote, position, theme in quotes:
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400"><rect width="800" height="400" fill="#1A1A1A"/><text x="400" y="200" text-anchor="middle" font-family="Arial Black, sans-serif" font-size="42" fill="#E8B4B8" font-weight="bold">{quote.upper()}</text><text x="400" y="280" text-anchor="middle" font-family="Helvetica, sans-serif" font-size="20" fill="#666">— that\'s the shirt —</text></svg>'
        save_svg(name, svg, d)
        count += 1
    return count

if __name__ == "__main__":
    print("=" * 60)
    print("Themed SVG Pack Generator")
    print("Original CC0 designs matching specific Etsy listings")
    print("=" * 60)
    
    total = 0
    
    print("\n--- Christian/Faith Pack ---")
    c = generate_christian_pack()
    print(f"  Generated {c} designs")
    total += c
    
    print("\n--- Halloween Pack ---")
    c = generate_halloween_pack()
    print(f"  Generated {c} designs")
    total += c
    
    print("\n--- Fall/Autumn Pack ---")
    c = generate_fall_pack()
    print(f"  Generated {c} designs")
    total += c
    
    print("\n--- Floral/Botanical Pack ---")
    c = generate_floral_pack()
    print(f"  Generated {c} designs")
    total += c
    
    print("\n--- Sarcastic/Funny Pack ---")
    c = generate_sarcastic_pack()
    print(f"  Generated {c} designs")
    total += c
    
    print(f"\n{'=' * 60}")
    print(f"Total themed SVGs: {total}")
    print(f"Saved to: {THEMED_DIR}")
    print(f"License: CC0")
