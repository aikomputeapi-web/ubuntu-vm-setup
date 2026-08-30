"""
Download public domain wall art from the Metropolitan Museum of Art Open Access API.
The Met has ~492,000 CC0 images available through their public API.

These are the same public-domain images that Etsy sellers repackage as
"150,000+ Printable Wall Art Bundle" for $1-8.

API docs: https://metmuseum.github.io/
"""

import requests
import os
import time
import json

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(OUTPUT_DIR, "met-wall-art")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

MET_API = "https://collectionapi.metmuseum.org/public/collection/v1"

# Departments to pull from (high-quality art)
DEPARTMENTS = [
    "American Decorative Arts",
    "Asian Art", 
    "European Paintings",
    "Photographs",
    "Modern Art",
]

# Search terms for popular wall art categories
SEARCH_TERMS = [
    "botanical", "landscape", "portrait", "abstract",
    "vintage", "flowers", "ocean", "mountains",
    "birds", "butterfly", "Japanese", "Impressionism",
]

def search_met(query, department=None, has_images=True, max_results=10):
    """Search the Met collection API."""
    params = {
        "hasImages": str(has_images).lower() if has_images else "false",
        "q": query,
    }
    if department:
        params["department"] = department
    
    url = f"{MET_API}/search"
    try:
        resp = requests.get(url, params=params, timeout=20,
                           headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code == 200:
            data = resp.json()
            object_ids = data.get("objectIDs", []) or []
            return object_ids[:max_results]
    except Exception as e:
        print(f"  Search error: {e}")
    return []

def get_object(object_id, save_dir):
    """Get a single object's metadata and download its image."""
    url = f"{MET_API}/objects/{object_id}"
    try:
        resp = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return False
        
        obj = resp.json()
        
        # Check if it has an image and is public domain
        primary_image = obj.get("primaryImage")
        is_public_domain = obj.get("isPublicDomain", False)
        
        if not primary_image or not is_public_domain:
            return False
        
        # Create a meaningful filename
        title = obj.get("title", f"met_{object_id}")
        artist = obj.get("artistDisplayName", "unknown")
        date = obj.get("objectDate", "")
        
        # Sanitize
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title)[:40]
        safe_artist = "".join(c if c.isalnum() or c in " -_" else "" for c in artist)[:30]
        filename = f"{safe_title}_{safe_artist}_{object_id}.jpg"
        
        # Save metadata
        meta = {
            "objectID": obj.get("objectID"),
            "title": obj.get("title"),
            "artist": obj.get("artistDisplayName"),
            "date": obj.get("objectDate"),
            "department": obj.get("department"),
            "medium": obj.get("medium"),
            "dimensions": obj.get("dimensions"),
            "image": primary_image,
            "license": "CC0 - Metropolitan Museum of Art Open Access",
            "met_url": obj.get("objectURL"),
        }
        
        meta_path = os.path.join(save_dir, filename.replace(".jpg", ".json"))
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        
        # Download the image (use the original URL, not thumbnail)
        img_resp = requests.get(primary_image, timeout=30, 
                               headers={"User-Agent": "Mozilla/5.0"})
        if img_resp.status_code == 200 and len(img_resp.content) > 5000:
            img_path = os.path.join(save_dir, filename)
            with open(img_path, "wb") as f:
                f.write(img_resp.content)
            return True
    
    except Exception as e:
        pass
    
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Met Museum Open Access - Wall Art Downloader")
    print("All images are CC0 (public domain)")
    print("=" * 60)
    
    total_downloaded = 0
    
    for term in SEARCH_TERMS:
        print(f"\n--- Searching: {term} ---")
        save_dir = os.path.join(DOWNLOAD_DIR, term.replace(" ", "_"))
        os.makedirs(save_dir, exist_ok=True)
        
        object_ids = search_met(term, max_results=8)
        print(f"  Found {len(object_ids)} objects")
        
        downloaded = 0
        for oid in object_ids:
            if get_object(oid, save_dir):
                downloaded += 1
                total_downloaded += 1
                print(f"  Downloaded object {oid}")
            time.sleep(0.5)  # Be respectful to API
        
        print(f"  Downloaded {downloaded} images for '{term}'")
    
    # Summary
    print(f"\n{'=' * 60}")
    print(f"Total Met images downloaded: {total_downloaded}")
    print(f"Saved to: {DOWNLOAD_DIR}")
    
    # Count files
    img_count = 0
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for f in files:
            if f.endswith(".jpg"):
                img_count += 1
    print(f"Total .jpg files on disk: {img_count}")
    print("License: CC0 - Metropolitan Museum of Art Open Access Initiative")
    print("Usage: Free for commercial and non-commercial use, no attribution required")
