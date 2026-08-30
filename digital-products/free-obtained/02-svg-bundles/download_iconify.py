"""
Download free SVG icons from Iconify API.
Iconify provides 200,000+ icons from 150+ open-source icon sets.
All icons are open source (MIT, Apache 2.0, etc.)
No API key needed, no rate limits on individual icon downloads.

This supplements our original SVG designs with real downloaded icons.
"""
import requests, os, time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg-bundles", "iconify-icons")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Icon collections to download from (all open source)
COLLECTIONS = {
    "mdi": {"name": "Material Design Icons", "license": "MIT", "limit": 50},
    "tabler": {"name": "Tabler Icons", "license": "MIT", "limit": 50},
    "lucide": {"name": "Lucide Icons", "license": "ISC", "limit": 50},
    "ph": {"name": "Phosphor Icons", "license": "MIT", "limit": 50},
    "heroicons": {"name": "Heroicons", "license": "MIT", "limit": 30},
    "carbon": {"name": "IBM Carbon Icons", "license": "MIT", "limit": 30},
    "fluent": {"name": "Fluent UI Icons", "license": "MIT", "limit": 30},
    "majesticons": {"name": "Majesticons", "license": "MIT", "limit": 30},
    "gala": {"name": "Gala Icons", "license": "MIT", "limit": 30},
    "iconoir": {"name": "Iconoir", "license": "MIT", "limit": 30},
}

headers = {"User-Agent": "Mozilla/5.0"}

# Curated popular icon names per collection
POPULAR_ICONS = [
    "heart", "star", "home", "user", "settings", "search", "check", "close",
    "plus", "minus", "arrow-right", "arrow-left", "chevron-down", "chevron-up",
    "bell", "mail", "phone", "calendar", "clock", "map-pin", "camera", "image",
    "music", "play", "pause", "stop", "volume", "download", "upload", "trash",
    "edit", "copy", "share", "link", "eye", "eye-off", "lock", "unlock",
    "bookmark", "tag", "flag", "award", "trophy", "target", "rocket", "bolt",
    "fire", "leaf", "sun", "moon", "cloud", "droplet", "wind", "thermometer",
    "coffee", "pizza", "apple", "car", "bike", "plane", "ship", "rocket",
    "shopping-cart", "gift", "credit-card", "dollar", "wallet", "chart",
    "book", "pen", "pencil", "ruler", "scissors", "paint-brush", "palette",
    "key", "shield", "crown", "diamond", "gem", "anchor", "compass",
    "ghost", "skull", "pumpkin", "bat", "cat", "dog", "bird", "fish",
    "butterfly", "flower", "tree", "mountain", "wave", "star",
]

total = 0
print("=" * 60)
print("Iconify SVG Downloader - 200k+ Open Source Icons")
print("=" * 60)

for col_key, col_info in COLLECTIONS.items():
    print(f"\n--- {col_info['name']} ({col_key}) | License: {col_info['license']} ---")
    count = 0
    
    for icon_name in POPULAR_ICONS[:col_info["limit"]]:
        svg_url = f"https://api.iconify.design/{col_key}/{icon_name}.svg"
        try:
            r = requests.get(svg_url, headers=headers, timeout=10)
            if r.status_code == 200 and "<svg" in r.text[:50]:
                filename = f"{col_key}_{icon_name}.svg"
                filepath = os.path.join(OUTPUT_DIR, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(r.text)
                count += 1
                total += 1
        except:
            pass
        time.sleep(0.05)  # Minimal delay, API is very permissive
    
    print(f"  Downloaded: {count} icons")

# Summary
print(f"\n{'=' * 60}")
print(f"Total SVG icons downloaded: {total}")
print(f"Saved to: {OUTPUT_DIR}")
print(f"Licenses: MIT, ISC, Apache 2.0 (all open source)")
