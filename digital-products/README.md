# Digital Products — Master Index

**One folder, 137 scraped listings, 14 products evaluated, 1 ready to sell. This README is the map.**

> **Start here:** open [`MASTER_CATALOG.xlsx`](./MASTER_CATALOG.xlsx) (or `.csv`) — 14 rows, color-coded by tier, with every item you should and should not sell, why, at what price, and what to do next. This README explains how the folder got there and where everything lives.

---

## TL;DR — What to sell

| Tier | Color | Count | What | Action |
|------|-------|-------|------|--------|
| **1 — SELL NOW** | 🟩 Green | 1 | `2026 Hyperlinked Digital Planner` — 222 pages, 1114 links, verified | List today; generate 12-mo + Mon/Sun variants |
| **2 — NEAR-READY** | 🟨 Yellow | 3 | `Ultimate Budget Tracker` · `Digital Product Ideas Guide` · `Faceless Video Pipeline` | 1-2 days each to finish |
| **3 — BUILD NEXT** | 🟦 Blue | 5 | `Bold & Easy Coloring Book` (rebuild) · `ADHD Planner line` · `ADHD+Coloring bundle` · `Curated Wall Art sets` · `Original Notion Template` | Best beachhead opportunities — not yet built properly |
| **4 — DO NOT SELL** | 🟥 Red | 5 | `Canva Lifetime` (scam) · `SVG mega-bundle resale` · `PLR/MRR bulk` · `Canva template resale` · `Custom-service generators` | Policy/scam risk — documented, do not list |

**Total catalog value if bought on Etsy: ~$1,495 → your cost: $0 (all built from scratch or curated from CC0/MIT sources).**

---

## Folder map

```
digital-products/
├── MASTER_CATALOG.csv / .xlsx  ← ★ START HERE: 14-row prioritized sell list
│                                  (Sheet 1: Master, Sheet 2: Evidence, Sheet 3: Niche Scores, Sheet 4: 37 Beachheads)
├── README.md                   ← you are here
├── INVENTORY.md                ← full file-by-file inventory with row counts and provenance
│
├── etsy-scraper/               ← 01 — RAW RESEARCH (292 listings across 10+ sweeps)
│   ├── etsy_digital_products.csv/.xlsx   137 listings — the base scrape (2026-08-30)
│   ├── etsy_underdogs.csv/.xlsx          108 underdogs — sells fast despite tiny shops (underdog_score)
│   ├── opportunity_niches.csv/.xlsx      292 listings — niche entrenchment study
│   ├── templates_designs.csv             435 template listings (separate sweep)
│   ├── ai_money_guides.csv/.xlsx + parts/ 91 AI money guides (teardown source)
│   ├── etsy_scrape.py / etsy_underdog.py  Camoufox scraper + underdog ranker
│   ├── README.md                          WAF notes, usage, --max-shop / --min-recent flags
│   └── parts/                             checkpoint CSVs from killed batch runs
│
├── free-alternatives-research/ ← 02 — ANALYSIS (is it free? can you DIY it?)
│   ├── listings_free_alternatives.csv/.xlsx  137 rows — every listing bucketed into 14 archetypes
│   ├── beachhead_listings.csv                 37 beachheads — live daily buyers from <5k-sale shops
│   ├── niche_opportunity_scores.csv           7 niches ranked by beachhead rate + median shop sales
│   ├── summary_by_archetype.csv               14 archetypes counted
│   ├── opportunity_analysis.xlsx              (beachheads + scores workbook)
│   └── README.md                              ★ Key insight: coloring 20% beachhead @ 1,450 median vs planner 10% @ 20,150
│
├── ai-guide-teardown/          ← 03 — AI GUIDE TEARDOWN (65 guides → why PDFs lose to runnable code)
│   ├── ai_guides_catalog.csv           91 raw → 65 kept AI money guides
│   ├── improvement_matrix.csv/.xlsx    65 rows — swappable tools, replacements, stale methods, improvement_score
│   ├── SUMMARY.md                      Top 65 ranked by daily buyers
│   ├── method-obsolescence.md          Why prompt-engineering era guides are stale
│   └── replacement-stack.md            $0 stack (Kokoro-82M, ffmpeg, Pexels API) vs $40-154/mo competitor
│
├── products/                   ← 04 — CURATED PRODUCTS (honest STATUS.md per product)
│   ├── 2026-hyperlinked-digital-planner/  READY — 222p, 1114 links
│   ├── ultimate-budget-tracker/           NEAR-READY — 6 sheets, 80 formulas (hollow tabs)
│   ├── digital-product-ideas-guide/       NEAR-READY — data-driven, not a static list
│   ├── faceless-video-pipeline/           STRONGEST CONCEPT — runnable code, needs proof run
│   ├── bold-easy-coloring-book/           NOT LISTABLE — hexagon tiling (needs rebuild)
│   ├── public-domain-wall-art/            MIXED — 60 real Met CC0 (good) + 72 rectangles (reject)
│   ├── canva-style-svg-templates/         UNVERIFIED — 104 SVGs not visually inspected
│   ├── svg-icon-bundle/                   NOT LISTABLE AS-IS — Iconify download resale
│   ├── custom-personalized-generators/    NOT A PRODUCT — labour, not a file
│   └── README.md                          Verdict table + how each verdict was verified
│
├── free-obtained/              ← 05 — BULK SOURCE MATERIAL (the generators + downloaded CC0)
│   ├── 01-digital-planners/               generate_planner.py + 223p PDF
│   ├── 02-svg-bundles/                    334 SVGs (286 Iconify MIT/ISC + 48 themed)
│   ├── 03-wall-art/                       60 Met CC0 + 72 generated PNGs + Wall_Art_Collection.pdf
│   ├── 04-coloring-pages/                 generate_coloring.py + 50p PDF (rejected tiling)
│   ├── 05-spreadsheet-trackers/           generate_tracker.py + Ultimate_Budget_Tracker_Template.xlsx
│   ├── 06-notion-templates/               FREE_ALTERNATIVES.md (links, not a product)
│   ├── 07-canva-templates/                104 SVGs + FREE_ALTERNATIVES.md
│   ├── 08-plr-mrr-bundles/                FREE_SOURCES.md (7 free PLR sites)
│   ├── 09-ai-video-pipeline/              5 scripts + batch generator + ffmpeg pipeline
│   ├── 10-digital-product-ideas/          Digital_Product_Ideas_Guide.md (data-driven)
│   ├── 11-custom-personalized/            3 generators + 15 SVGs + 2 reports
│   └── README.md                          Full per-category method + reusability table
│
├── etsy.db / etsy_recon.py / seeds.txt / sites.txt  ← 06 — original recon scaffolding
```

---

## How to use this

**1. Decide what to sell:** open `MASTER_CATALOG.xlsx` → Sheet 1 (`MASTER - What To Sell`) is filtered by `Tier`. Green = sell now, Yellow = finish, Blue = build next, Red = avoid. Sheet 2 has the full evidence paragraph per row; Sheet 3 is the niche ranking; Sheet 4 is the 37 beachheads with price/daily-buyers/shop-sales.

**2. List the ready product:** `products/2026-hyperlinked-digital-planner/` — run `generate_planner.py` for variants, add cover art, disclose AI if used, list at $6-12.

**3. Finish the near-ready ones:** each `STATUS.md` in `products/` tells you the exact gap and the fix command. Tracker = add formulas; Ideas Guide = add charts; Video Pipeline = prove it runs end-to-end.

**4. Build the best next product:** `MASTER_CATALOG` Tier 3 row 1 is `Bold & Easy Coloring Book` — **20% beachhead, median shop 1,450 sales** (14× less entrenched than planners). The current file is rejected tiling; rebuild with real line art (30-40 unique pages).

**5. Read the why:** `free-alternatives-research/README.md` explains the beachhead concept and the two corrections (planners are entrenched; Etsy 2025-06-10 now requires *original design* — PLR/Canva-stock/SVG-aggregation resale as-is risks removal/suspension). `ai-guide-teardown/method-obsolescence.md` explains why the faceless video pipeline is the outlier.

---

## Key finding you asked about — "shops without huge history"

That phrase maps directly to **`etsy-scraper/etsy_underdogs.csv`** and **`free-alternatives-research/beachhead_listings.csv`**.

- **Underdog score** = daily buyers per 1,000 lifetime shop sales. Top legitimate example: `ADHD Digital Planner` at $3.95 doing 5/day from a shop with **62 lifetime sales** (underdog_score 20.0). The top 2 overall are scams (Canva Lifetime scams doing 12/day from 52 sales — marked `DO NOT SELL` in the master).
- **Beachhead** = listing with live `N people bought this in last 24 hours` badge from a shop with **<5,000 lifetime sales**. `niche_opportunity_scores.csv` ranks niches by beachhead rate:
  - **coloring 20% @ 1,450 median** — best new-seller niche
  - **planner-adhd 15% @ 2,400** — the ADHD qualifier is the strongest single signal
  - **planner (general) 10% @ 20,150** — most entrenched, avoid as first listing
- Run yourself: `etsy-underdog --max-shop 2000 --min-recent 5` or `etsy-underdog --scrape "adhd planner" --pages 2`.

---

## Policy you must not ignore

**Etsy Creativity Standards — updated 10 June 2025** — added digital downloads. Items must be based on the seller's **original design**; reselling PLR files, Canva stock templates, or aggregated CC0 bundles **as-is** risks listing removal; repeated/large-scale breaches risk shop suspension. AI-generated work must be disclosed and requires the seller's own creative input (`Designed by a seller`, not `Made by a seller`). This is why `MASTER_CATALOG` marks SVG aggregation, PLR repackaging, and Canva-stock resale as `DO NOT SELL AS-IS` even though incumbents do it.

Sources: documented in `free-alternatives-research/README.md` and `ai-guide-teardown/method-obsolescence.md`.

---

## Raw counts

| File | Rows | What |
|------|------|------|
| `etsy-scraper/etsy_digital_products.csv` | 137 | Base scrape (titles, prices, shop_sales, recent_sales badge) |
| `etsy-scraper/etsy_underdogs.csv` | 108 | Underdogs ranked by underdog_score |
| `etsy-scraper/opportunity_niches.csv` | 292 | Niche entrenchment sweep (planner/coloring/wall-art/spreadsheet) |
| `etsy-scraper/templates_designs.csv` | 435 | Template-focused sweep |
| `etsy-scraper/ai_money_guides.csv` | 91 | AI money guides (65 kept after dedup) |
| `free-alternatives-research/listings_free_alternatives.csv` | 137 | Archetype + free-equivalent verdict per listing |
| `free-alternatives-research/beachhead_listings.csv` | 37 | Live-buyer beachheads (<5k shop) |
| `MASTER_CATALOG.csv` | 14 | ★ Prioritized sell / do-not-sell list |

---

*Generated 2026-08-30. All scrapes via Camoufox (anti-detect Firefox) against DataDome; `etsy.db` holds the recon SQLite. See `etsy-scraper/README.md` for scraper flags and `products/*/STATUS.md` for per-product verification.*
