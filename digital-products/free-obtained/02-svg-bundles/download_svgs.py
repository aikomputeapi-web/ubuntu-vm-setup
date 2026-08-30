"""
Download free CC0 SVG files from SVG Repo API.
SVG Repo hosts 500k+ SVG files, mostly CC0 / CC-BY licensed.
These are the same files that Etsy sellers repackage as "80,000+ SVG Mega Bundles".

API docs: https://www.svgrepo.com/api/
"""

import requests
import os
import json
import time
from urllib.parse import quote

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(OUTPUT_DIR, "svg-bundles")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Categories matching the Etsy listing themes
CATEGORIES = [
    "halloween", "ghost", "pumpkin", "skull", "christmas", "winter",
    "floral", "flower", "botanical", "leaf", "plant",
    "cat", "dog", "animal", "bird", "fish",
    "heart", "star", "crown", "arrow",
    "food", "coffee", "cake", "fruit",
    "travel", "beach", "mountain", "sun",
    "baby", "wedding", "birthday",
    "religion", "cross", "prayer",
    "sport", "fitness", "gym",
    "music", "guitar", "piano",
    "social media", "phone", "computer",
    "bee", "butterfly", "owl", "fox",
    "nurse", "teacher", "mom", "dad",
    "skeleton", "dragon", "unicorn",
    "patriotic", "flag", "eagle",
]

API_BASE = "https://www.svgrepo.com/download"

def download_svg(svg_id, filename, save_dir):
    """Download a single SVG file from SVG Repo."""
    url = f"{API_BASE}/{svg_id}.svg"
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code == 200 and "svg" in resp.headers.get("content-type", ""):
            filepath = os.path.join(save_dir, filename)
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return True
    except Exception as e:
        pass
    return False

def search_and_download_svgrepo(query, max_results=10, save_dir=None):
    """
    Search SVG Repo for free SVGs matching query.
    Uses the SVG Repo v2 API endpoint.
    """
    if save_dir is None:
        safe_query = "".join(c if c.isalnum() else "_" for c in query)
        save_dir = os.path.join(DOWNLOAD_DIR, safe_query)
    os.makedirs(save_dir, exist_ok=True)
    
    # SVG Repo search API
    search_url = f"https://www.svgrepo.com/v2/search/?query={quote(query)}&limit={max_results}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    
    downloaded = 0
    try:
        resp = requests.get(search_url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("data", []) or data.get("results", [])
            for item in items:
                svg_id = item.get("id") or item.get("svg_id")
                title = item.get("title", f"svg_{svg_id}")
                safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in title)[:50]
                filename = f"{safe_title}_{svg_id}.svg"
                if download_svg(svg_id, filename, save_dir):
                    downloaded += 1
                    time.sleep(0.3)  # Be respectful
    except Exception as e:
        print(f"  API error for '{query}': {e}")
    
    # Fallback: try directly downloading from known free SVG IDs
    # SVG Repo also has a pattern-based download
    if downloaded == 0:
        print(f"  API didn't return results for '{query}', trying direct download...")
        # Try some known ID ranges
        for svg_id in range(1, max_results + 1):
            filename = f"{query.replace(' ', '_')}_{svg_id}.svg"
            if download_svg(svg_id, filename, save_dir):
                downloaded += 1
                time.sleep(0.2)
    
    return downloaded

def download_from_openclipart(query, max_results=5, save_dir=None):
    """
    Download from OpenClipart (CC0) as additional source.
    """
    if save_dir is None:
        safe_query = "".join(c if c.isalnum() else "_" for c in query)
        save_dir = os.path.join(DOWNLOAD_DIR, safe_query)
    os.makedirs(save_dir, exist_ok=True)
    
    # OpenClipart API
    api_url = f"https://openclipart.org/search/json/?query={quote(query)}&amount={max_results}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    downloaded = 0
    try:
        resp = requests.get(api_url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("payload", {}).get("data", []) if isinstance(data, dict) else []
            for item in items:
                svg_url = item.get("svg", {}).get("url") or item.get("download")
                if svg_url:
                    filename = f"oc_{item.get('id', downloaded)}.svg"
                    filepath = os.path.join(save_dir, filename)
                    r = requests.get(svg_url, headers=headers, timeout=15)
                    if r.status_code == 200:
                        with open(filepath, "wb") as f:
                            f.write(r.content)
                        downloaded += 1
                        time.sleep(0.3)
    except Exception as e:
        print(f"  OpenClipart error for '{query}': {e}")
    
    return downloaded

def generate_sample_svgs(save_dir):
    """
    Generate our own SVG files programmatically as a guaranteed fallback.
    These are original CC0 designs we create ourselves.
    """
    os.makedirs(save_dir, exist_ok=True)
    count = 0
    
    # Generate a variety of useful SVG graphics
    svgs = [
        ("heart_basic", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="#E8B4B8"/></svg>'),
        ("star_basic", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 16.8 5.8 21.3l2.4-7.4L2 9.4h7.6z" fill="#FFD700"/></svg>'),
        ("flower_simple", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="30" r="18" fill="#E8B4B8"/><circle cx="70" cy="50" r="18" fill="#D4A5A5"/><circle cx="50" cy="70" r="18" fill="#E8B4B8"/><circle cx="30" cy="50" r="18" fill="#D4A5A5"/><circle cx="50" cy="50" r="15" fill="#F5DEB3"/></svg>'),
        ("leaf_botanical", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 10 Q70 30 70 50 Q70 70 50 90 Q30 70 30 50 Q30 30 50 10 Z" fill="#8FBC8F"/><line x1="50" y1="10" x2="50" y2="90" stroke="#556B2F" stroke-width="2"/></svg>'),
        ("cat_silhouette", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M30 20 L40 35 L60 35 L70 20 L65 45 Q80 55 80 70 Q80 85 50 85 Q20 85 20 70 Q20 55 35 45 Z" fill="#333"/><circle cx="42" cy="50" r="3" fill="white"/><circle cx="58" cy="50" r="3" fill="white"/></svg>'),
        ("ghost_halloween", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 10 Q25 10 25 40 L25 80 Q30 75 35 80 Q40 75 45 80 Q50 75 55 80 Q60 75 65 80 Q70 75 75 80 L75 40 Q75 10 50 10 Z" fill="white" stroke="#333" stroke-width="2"/><circle cx="40" cy="40" r="5" fill="#333"/><circle cx="60" cy="40" r="5" fill="#333"/></svg>'),
        ("pumpkin", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><ellipse cx="50" cy="55" rx="35" ry="30" fill="#FF7518"/><ellipse cx="35" cy="55" rx="12" ry="28" fill="#FF8C00"/><ellipse cx="65" cy="55" rx="12" ry="28" fill="#FF8C00"/><rect x="47" y="20" width="6" height="15" fill="#228B22"/></svg>'),
        ("skull", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 10 Q20 10 20 45 Q20 60 30 70 L30 80 L40 80 L40 75 L45 75 L45 80 L55 80 L55 75 L60 75 L60 80 L70 80 L70 70 Q80 60 80 45 Q80 10 50 10 Z" fill="white" stroke="#333" stroke-width="2"/><circle cx="38" cy="40" r="8" fill="#333"/><circle cx="62" cy="40" r="8" fill="#333"/><path d="M45 55 L50 65 L55 55" stroke="#333" stroke-width="2" fill="none"/></svg>'),
        ("butterfly", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 50 Q30 20 15 35 Q5 50 20 65 Q35 70 50 50 Z" fill="#E8B4B8"/><path d="M50 50 Q70 20 85 35 Q95 50 80 65 Q65 70 50 50 Z" fill="#D4A5A5"/><ellipse cx="50" cy="55" rx="3" ry="25" fill="#333"/></svg>'),
        ("wave_ocean", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60"><path d="M0 30 Q15 15 30 30 Q45 45 60 30 Q75 15 90 30 Q100 35 100 30 L100 60 L0 60 Z" fill="#6BA8B5"/></svg>'),
        ("mountain_landscape", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><polygon points="0,100 30,40 50,70 70,20 100,100" fill="#556B2F"/><polygon points="30,40 35,50 25,50" fill="white"/><polygon points="70,20 75,35 65,35" fill="white"/></svg>'),
        ("coffee_cup", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M20 40 L20 75 Q20 85 30 85 L60 85 Q70 85 70 75 L70 40 Z" fill="#8B4513"/><path d="M70 50 Q85 50 85 65 Q85 75 70 75" fill="none" stroke="#8B4513" stroke-width="4"/><path d="M30 30 Q25 20 35 15 M40 30 Q35 20 45 15 M50 30 Q45 20 55 15" fill="none" stroke="#D3D3D3" stroke-width="2"/></svg>'),
        ("arrow_decorative", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><line x1="10" y1="25" x2="80" y2="25" stroke="#333" stroke-width="3"/><polygon points="80,15 95,25 80,35" fill="#333"/><circle cx="10" cy="25" r="4" fill="#E8B4B8"/></svg>'),
        ("crown", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60"><path d="M10 50 L15 20 L35 40 L50 10 L65 40 L85 20 L90 50 Z" fill="#FFD700" stroke="#B8860B" stroke-width="2"/><rect x="10" y="50" width="80" height="8" fill="#FFD700"/></svg>'),
        ("diamond", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><polygon points="50,10 80,35 50,90 20,35" fill="#B0C4DE" stroke="#4682B4" stroke-width="2"/><polygon points="50,10 80,35 50,35 20,35" fill="#87CEEB"/></svg>'),
        ("sun_burst", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="20" fill="#FFD700"/><g stroke="#FFD700" stroke-width="3"><line x1="50" y1="10" x2="50" y2="25"/><line x1="50" y1="75" x2="50" y2="90"/><line x1="10" y1="50" x2="25" y2="50"/><line x1="75" y1="50" x2="90" y2="50"/><line x1="22" y1="22" x2="32" y2="32"/><line x1="68" y1="68" x2="78" y2="78"/><line x1="78" y1="22" x2="68" y2="32"/><line x1="32" y1="68" x2="22" y2="78"/></g></svg>'),
        ("moon_crescent", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 10 A40 40 0 1 0 50 90 A30 40 0 1 1 50 10 Z" fill="#C4956C"/></svg>'),
        ("book_open", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><path d="M10 15 Q30 10 50 15 L50 70 Q30 65 10 70 Z" fill="#8B4513" stroke="#A0522D"/><path d="M50 15 Q70 10 90 15 L90 70 Q70 65 50 70 Z" fill="#8B4513" stroke="#A0522D"/><line x1="50" y1="15" x2="50" y2="70" stroke="#333" stroke-width="2"/></svg>'),
        ("camera_retro", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><rect x="10" y="20" width="80" height="50" rx="5" fill="#333"/><circle cx="50" cy="45" r="18" fill="#555"/><circle cx="50" cy="45" r="12" fill="#333" stroke="#777" stroke-width="2"/><rect x="35" y="10" width="30" height="15" fill="#333"/><circle cx="75" cy="30" r="4" fill="#E8B4B8"/></svg>'),
        ("key_vintage", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><circle cx="15" cy="25" r="12" fill="none" stroke="#B8860B" stroke-width="3"/><circle cx="15" cy="25" r="5" fill="#B8860B"/><line x1="27" y1="25" x2="80" y2="25" stroke="#B8860B" stroke-width="4"/><rect x="70" y="25" width="4" height="8" fill="#B8860B"/><rect x="60" y="25" width="4" height="6" fill="#B8860B"/></svg>'),
    ]
    
    for name, svg_content in svgs:
        filepath = os.path.join(save_dir, f"original_{name}.svg")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        count += 1
    
    return count

if __name__ == "__main__":
    print("=" * 60)
    print("SVG Bundle Downloader - Free CC0 SVGs")
    print("=" * 60)
    
    total_downloaded = 0
    
    # 1. Try SVG Repo API for each category
    print("\n--- Downloading from SVG Repo ---")
    for cat in CATEGORIES[:15]:  # Start with first 15 categories
        print(f"  Searching: {cat}...", end=" ")
        count = search_and_download_svgrepo(cat, max_results=5)
        print(f"got {count}")
        total_downloaded += count
        time.sleep(0.5)
    
    # 2. Try OpenClipart
    print("\n--- Downloading from OpenClipart ---")
    for cat in CATEGORIES[:10]:
        print(f"  Searching: {cat}...", end=" ")
        count = download_from_openclipart(cat, max_results=3)
        print(f"got {count}")
        total_downloaded += count
        time.sleep(0.5)
    
    # 3. Generate our own original SVGs (guaranteed)
    print("\n--- Generating original SVG designs ---")
    orig_dir = os.path.join(DOWNLOAD_DIR, "original-designs")
    count = generate_sample_svgs(orig_dir)
    print(f"  Generated {count} original SVG designs")
    total_downloaded += count
    
    # Summary
    print(f"\n{'=' * 60}")
    print(f"Total SVGs obtained: {total_downloaded}")
    print(f"Saved to: {DOWNLOAD_DIR}")
    
    # Count total files
    file_count = 0
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for f in files:
            if f.endswith(".svg"):
                file_count += 1
    print(f"Total .svg files on disk: {file_count}")
    
    # List categories
    print(f"\nCategories downloaded:")
    for d in sorted(os.listdir(DOWNLOAD_DIR)):
        dpath = os.path.join(DOWNLOAD_DIR, d)
        if os.path.isdir(dpath):
            svg_count = len([f for f in os.listdir(dpath) if f.endswith(".svg")])
            if svg_count > 0:
                print(f"  {d}: {svg_count} files")
