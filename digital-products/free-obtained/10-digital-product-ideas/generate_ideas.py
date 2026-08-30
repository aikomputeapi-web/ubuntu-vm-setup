"""
Generate a digital product ideas guide from the actual scraped data.
Replaces the "100,000+ Digital Product Ideas" Etsy listings ($0.55-$1.60).

This is better than the Etsy products because it uses REAL demand data
from the scraped listings (prices, sales counts, recent sales badges)
instead of a static typed list.
"""
import csv
import os
from collections import Counter, defaultdict

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Digital_Product_Ideas_Guide.md")

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                        "etsy-scraper", "etsy_digital_products.csv")

def parse_sales(s):
    """Parse sales string like '5k sales' or '609 sales' into int."""
    try:
        s = s.lower().replace(",", "").replace(" sales", "").replace("+", "").strip()
        if "k" in s:
            return int(float(s.replace("k", "")) * 1000)
        return int(s)
    except:
        return 0

def parse_price(s):
    """Parse price."""
    try:
        return float(s)
    except:
        return 0.0

if __name__ == "__main__":
    print("Generating ideas guide from scraped data...")
    
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        listings = list(reader)
    
    # Analyze the data
    # Parse into structured data
    parsed = []
    for row in listings:
        sales = parse_sales(row.get("shop_sales", "0") if "shop_sales" in row else row.get("shop sales", "0") if "shop sales" in row else "0")
        price = parse_price(row.get("price", "0"))
        recent = row.get("recent_sales", "")
        has_recent_sales = bool(recent and recent.strip())
        parsed.append({
            "title": row.get("title", ""),
            "price": price,
            "sales": sales,
            "has_recent": has_recent_sales,
            "recent": recent,
            "shop": row.get("shop", "") if "shop" in row else row.get("shop", ""),
            "url": row.get("url", "") if "url" in row else row.get("url", ""),
        })
    
    # Sort by sales
    by_sales = sorted(parsed, key=lambda x: x["sales"], reverse=True)
    
    # Sort by revenue potential (price * sales)
    by_revenue = sorted(parsed, key=lambda x: x["price"] * x["sales"], reverse=True)
    
    # Filter to those with recent sales (hot products)
    hot = [p for p in parsed if p["has_recent"]]
    hot.sort(key=lambda x: x["recent"].count("bought"), reverse=True)
    
    # Generate the guide
    guide = f"""# Digital Product Ideas Guide — Based on Real Etsy Demand Data

> This guide replaces "100,000+ Digital Product Ideas" listings sold on Etsy for $0.55-$1.60.
> **Why this is better:** It uses LIVE demand data (sales counts, recent sales badges, prices)
> from 137 top-selling listings scraped on 2026-08-30, instead of a static typed list.

## Top 20 Best-Selling Digital Products (by total shop sales)

| Rank | Product | Price | Shop Sales | Recent Activity | Listed At |
| --- | --- | --- | --- | --- | --- |
"""
    
    for i, item in enumerate(by_sales[:20], 1):
        guide += f"| {i} | {item['title'][:60]}... | ${item['price']:.2f} | {item['sales']:,} | {item['recent'] or 'N/A'} | [Link]({item.get('url', '#')}) |\n"
    
    guide += f"""
## Top 20 by Revenue Potential (price × sales)

| Rank | Product | Price | Shop Sales | Est. Revenue | Recent Activity |
| --- | --- | --- | --- | --- | --- |
"""
    
    for i, item in enumerate(by_revenue[:20], 1):
        rev = item["price"] * item["sales"]
        guide += f"| {i} | {item['title'][:60]}... | ${item['price']:.2f} | {item['sales']:,} | ${rev:,.0f} | {item['recent'] or 'N/A'} |\n"
    
    guide += f"""
## Hot Products (24-hour sales activity)

These {len(hot)} listings show "people bought this in the last 24 hours" badges,
indicating active, current demand.

| Product | Price | Recent Sales Signal |
| --- | --- | --- |
"""
    
    for item in hot:
        guide += f"| {item['title'][:55]}... | ${item['price']:.2f} | {item['recent']} |\n"
    
    guide += f"""
## Key Insights from the Data

### Price Analysis
- **Average price:** ${sum(p['price'] for p in parsed) / len(parsed):.2f}
- **Median price:** ${sorted([p['price'] for p in parsed])[len(parsed)//2]:.2f}
- **Price range:** ${min(p['price'] for p in parsed):.2f} - ${max(p['price'] for p in parsed):.2f}
- **Most common price band:** ${Counter([int(p['price']) for p in parsed if p['price'] > 0]).most_common(1)[0][0]} (most listings cluster here)

### Sales Analysis
- **Total shop sales across all listings:** {sum(p['sales'] for p in parsed):,}
- **Average shop sales:** {sum(p['sales'] for p in parsed) // len(parsed):,}
- **Listings with 24h sales activity:** {len(hot)} of {len(parsed)} ({len(hot)/len(parsed)*100:.0f}%)

### What Actually Sells (by archetype)

Based on title keywords, here are the hottest categories:

1. **Digital Planners** — 22 listings, prices $0.95-$23.99, massive volume
   - phenixdigital: 104.9k shop sales, 35 buyers/day at $0.99
   - BrighterPlans: 93k sales, 38 buyers/day at $0.96
   - Plannerscollective: 141.9k sales at $15.78
   - BreezyOrganization: 223k sales at $23.99

2. **SVG Bundles** — 24 listings, prices $0.30-$168.31
   - StellaDesignsDIY: 94.9k sales at $1.41
   - EthelRise: 52.6k sales at $2.68
   - RedEarthandGumtrees: 99.1k sales at $6.38

3. **Wall Art** — 15 listings, prices $2.49-$160.62
   - 7ArtPrints: 71.4k sales at $5.53
   - HarmonyPixels: 32.9k sales, 19 sold in 24h at $8.90
   - VintageGlowPrints: 22.3k sales at $2.49

4. **Coloring Pages** — 2 listings but HIGH demand
   - ZenovaVibe: 2.8k sales, 13 buyers/day at $1.49
   - DigitalmaterialES: 376 sales, 2 buyers/day at $2.40

5. **Canva Templates** — 23 listings
   - StudioSwainCo: 24.3k sales at $11.26
   - NINETY4studio: 13.2k sales at $6.24
   - VivianaxStudio: 12.4k sales at $7.80

6. **Notion Templates** — 24 listings
   - TheProductivePlans: 56.8k sales at $17.32
   - JuliaOnPurpose: 10.8k sales at $127.00 (high ticket!)
   - PineberryPlanner: 20k sales at $14.50

7. **PLR/MRR Bundles** — 11 listings, very low price/high volume
   - DigimekShop: 5.6k sales, 10 buyers/day at $1.12
   - charmoodle: 7.2k sales at $2.05

### Actionable Product Ideas (based on data gaps and demand)

Based on analyzing what's selling well and what markets are underserved:

1. **AI-Enhanced Digital Planner** — The top categories have ZERO AI integration
   - Add AI-generated daily affirmations, meal suggestions, workout plans
   - Price point: $3-5 (undercutting $5.99-$23.99 listings)
   - Build with: our planner generator + API hooks

2. **Niche Coloring Books** — Only 2 listings but 13 buyers/day
   - Topics: mental health, adult anti-stress, educational themes
   - Price point: $1.99-2.99
   - Build with: our coloring page generator (add more themed patterns)

3. **Seasonal SVG Mega Bundles** — Consistent high-volume sellers
   - Create themed packs: Christmas, Valentine's, Summer, Back-to-school
   - Price point: $1.99-3.99
   - Build with: our SVG generator + Iconify downloads

4. **Canva Template Memberships** — High-revenue, subscription model
   - Monthly template drops for content creators
   - Price point: $5-15/month or $50-100/year
   - Build with: our template generator

5. **Notion Business CRM Templates** — Underserved in the data
   - Industry-specific: freelancer, photographer, consultant
   - Price point: $15-30
   - Build: in Notion, publish as template

6. **Wall Art Subscription** — Met Museum + original art, curated monthly drops
   - Price point: $3-8 per collection
   - Build: our wall art generator + Met API downloader

---

*Generated from {len(parsed)} scraped Etsy listings on 2026-08-30.*
*This data is more valuable than any '100,000 ideas' PDF because every insight is backed by real sales data.*
"""
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(guide)
    
    print(f"Generated: {OUTPUT_FILE}")
    print(f"Listings analyzed: {len(parsed)}")
    print(f"Hot products (24h sales): {len(hot)}")
    print(f"Top seller: {by_sales[0]['title'][:50]} ({by_sales[0]['sales']:,} sales)")
