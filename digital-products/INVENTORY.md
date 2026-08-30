# Inventory — every file in digital-products, what it is, and whether to trust it

*Generated 2026-08-30 from filesystem + header reads. Row counts are exact.*

## Top-level

| File | Size | Rows / Pages | Provenance | Verdict |
|------|------|--------------|------------|---------|
| `MASTER_CATALOG.csv` | 12 KB | 14 rows | Built 2026-08-30 from beachhead + underdog + archetype + STATUS.md | ★ The sell list. Tiers 1-4, color-coded in .xlsx. |
| `MASTER_CATALOG.xlsx` | 20 KB | 14 + 7 + 37 rows, 4 sheets | Same source; Sheet1 Master, Sheet2 Evidence, Sheet3 Niche Scores, Sheet4 Beachheads | ★ Start here (print-ready, filtered, landscape). |
| `README.md` | 10 KB | — | Written 2026-08-30 as folder map + how-to | Map + policy + "shops without huge history" explainer. |
| `INVENTORY.md` | — | — | This file | File-by-file audit. |
| `etsy.db` | 28 KB | SQLite | `etsy_recon.py` sync-API recon (early pipeline) | Superseded by `etsy-scraper/` Camoufox runs. |
| `etsy_recon.py` | 11 KB | — | `search`/`expand`/`score` subcommands, stdlib SQLite | Working but not used for the beachhead study. |
| `seeds.txt` | 222 B | 10 lines | Seed keywords (wall art svg, digital planner, lightroom preset, ...) | Input to early recon. |
| `sites.txt` | 2.4 KB | ~30 lines | Marketplace list (aftcra, etsy, creativefabrica, ...) | Reference, not scraped. |

---

## etsy-scraper/ — raw research

| File | Size | Rows | What | Keep? |
|------|------|------|------|-------|
| `etsy_digital_products.csv/.xlsx` | 449 KB / 173 KB | **137** | Base scrape: title, price, shop, shop_sales, rating, review_count, recent_sales badge, description, tags, url | ✅ Base truth. Source for `listings_free_alternatives.csv`. Scraped 2026-08-30 via Camoufox. |
| `etsy_underdogs.csv/.xlsx` | 24 KB / 931 KB | **108** | Underdogs ranked by `underdog_score = daily_demand / (shop_lifetime/1000)` — "sells fast despite tiny shop" | ✅ The "shops without huge history" file. Filter `recent_sales >= min-recent AND shop_sales <= max-shop`. |
| `opportunity_niches.csv/.xlsx` | 958 KB / 341 KB | **292** | Niche entrenchment study: planner / coloring / wall-art / spreadsheet | ✅ Source for `niche_opportunity_scores.csv`. Median shop sales per niche. |
| `templates_designs.csv/.xlsx` | 1.4 MB / 472 KB | **435** | Template-focused sweep (canva/ebook/instagram/logo/resume etc.) | ✅ Separate sweep; not in MASTER but available. |
| `ai_money_guides.csv + _a/_b/_c/_d + _merged` | 269-931 KB | **91** (65 kept) | AI money-guide sweep: 10 keywords, 1 page each, 12-listing cap | ✅ Source for `ai-guide-teardown/`. 65 kept, 26 dropped. |
| `etsy_sheets_upload.csv` | 58 KB | 137 | Copy of `etsy_digital_products.csv` formatted for Google Sheets upload | Dupe — safe to ignore. |
| `etsy_scrape.py` | 16 KB | — | Camoufox scraper (see README for WAF notes) | ✅ Working scraper. `etsy-scrape "adhd planner" --pages 3` |
| `etsy_underdog.py` | 13 KB | — | `etsy-underdog` ranker + niche gatekeeping printer | ✅ `etsy-underdog --max-shop 2000 --min-recent 5` |
| `merge_parts.py` / `to_gsheet.py` | 5.8 / 2.3 KB | — | Merge checkpoint parts + Sheets formatter | Utility. |
| `parts/` | ~1 MB | 29 CSVs | Checkpoint saves from killed batch runs (`ai__*`, `tpl__*`) | Duplicated into merged files — safe to archive. |
| `proxies.txt` | 188 B | 1 line | `user:pass@host:port` (InstantProxies) — gitignored | Needed only at volume. |
| `README.md` | 2.9 KB | — | WAF table (curl→403, Playwright→blank, Camoufox→pass), flags, columns | ✅ Read before scraping. |

---

## free-alternatives-research/ — analysis

| File | Size | Rows | What | Keep? |
|------|------|------|------|-------|
| `listings_free_alternatives.csv/.xlsx` | 102 KB / 27 KB | **137** | Every listing → 14 archetypes, free_equivalent, diy_difficulty, verdict | ✅ Source for "96% have free equivalent" claim. 3 scams flagged. |
| `beachhead_listings.csv` | 20 KB | **37** | Beachheads: listings with live daily buyers from shops <5k lifetime sales | ✅ ★ Best new-seller signal. |
| `niche_opportunity_scores.csv` | 553 B | **7** | Niche ranking: coloring 20%@1450, planner-adhd 15%@2400, wall-art 14%@6800, spreadsheet 11%@6450, planner 10%@20150 | ✅ The "where to enter" table. |
| `opportunity_analysis.xlsx` | 380 KB | — | Workbook version of beachheads + scores | ✅ Formatted twin of the two CSVs. |
| `summary_by_archetype.csv` | 471 B | **14** | Archetype counts: svg-bundle 24, notion 24, canva 23, planner 22, ... | ✅ Quick archetype census. |
| `build_findings.py` / `score_opportunities.py` | 14 / 4.8 KB | — | Regenerators: archetype regex + beachhead scorer | ✅ Rerunnable. |
| `README.md` | 11 KB | — | Headline 96%, per-archetype table, two corrections (planners entrenched; 2025-06-10 policy) | ✅ ★ Must-read before selling. |

---

## ai-guide-teardown/ — AI money-guide teardown

| File | Size | Rows | What | Keep? |
|------|------|------|------|-------|
| `ai_guides_catalog.csv` | 172 KB | 91 → 65 kept | Raw scrape of AI money guides (see SUMMARY.md for dedup logic) | ✅ Source catalog. |
| `improvement_matrix.csv/.xlsx` | 18 / 13 KB | 65 | Per-guide: prescribed_monthly_usd, swappable_tools, locked_platforms, replacements, stale_methods | ✅ Basis for "$0 stack vs $154/mo" claim. |
| `score_improvements.py` | 6.3 KB | — | Scores improvement_matrix | ✅ Rerunnable. |
| `SUMMARY.md` | 12 KB | — | 65 kept ranked by daily buyers; tool frequency table (YouTube 29, Etsy 28, ChatGPT 22, Claude 15, ...) | ✅ Read for the "98% PDFs, 1 ships software" insight. |
| `method-obsolescence.md` | 9.4 KB | — | Why prompt-engineering era guides are stale; context-engineering + agentic/MCP shift | ✅ Read before writing the video pipeline listing. |
| `replacement-stack.md` | 6.6 KB | — | $0 replacements: Buffer→APIs+cron, Claude→free tier/local, Cloudinary→ffmpeg, InVideo→ffmpeg+MoviePy | ✅ The cost edge. |

---

## products/ — curated, verified products (honest STATUS.md)

*Each folder has product files + generator + STATUS.md. Statuses as assessed 2026-08-30 by opening files, not by free-obtained/README claims.*

| Folder | Status | Price | Files | Honest verdict |
|--------|--------|-------|-------|----------------|
| `2026-hyperlinked-digital-planner/` | **READY** | $6-12 | `planner_2026_6month_hyperlinked.pdf` (222p) + `generate_planner.py` + `STATUS.md` | ✅ 222p, 1114 links, 8 bookmarks, correct Jan 2026 grid. Original generation → Etsy-compliant. Needs cover + 12-mo variant. |
| `ultimate-budget-tracker/` | NEAR-READY | $4-8 | `Ultimate_Budget_Tracker_Template.xlsx` (6 sheets, 3 charts, 80 formulas) + generator | Hollow Income (A1:D7, 0 formulas) + Expenses (A1:F13, 0). Dashboard carries logic. Fix tabs. |
| `digital-product-ideas-guide/` | NEAR-READY | $2-5 | `Digital_Product_Ideas_Guide.md` (data-driven) | Beats static "100k ideas" PDFs — ranks 71 hot products by real sales. Needs charts. |
| `faceless-video-pipeline/` | STRONGEST CONCEPT | $15-35 | 5 scripts + `batch_generate.sh` + `generate_pipeline.py` + ffmpeg pipeline | Category is 98% PDFs; one ships software. Needs clean-machine proof run. Read method-obsolescence.md first. |
| `bold-easy-coloring-book/` | **NOT LISTABLE** | — | `Free_Coloring_Pages_Bundle.pdf` (50p) + generator | Rejected: 113-115 identical hexagon tilings per page, rendered as plain grid. Rebuild with real line art. Best beachhead (20%) deserves better. |
| `public-domain-wall-art/` | MIXED | $3-10 | 60 Met CC0 (`met-wall-art/`) + 72 `wall-art-png/` + `Wall_Art_Collection.pdf` | 60 Mets are genuine (need curation by theme); 72 PNGs are coloured rectangles (discard). Do not bulk-dump as "150k bundle" (2025-06-10 policy). |
| `canva-style-svg-templates/` | UNVERIFIED | — | 104 SVGs (8 palettes) + `FREE_ALTERNATIVES.md` | Not visually inspected; treat as suspect. Reselling Canva stock is blocked; only original SVGs count. |
| `svg-icon-bundle/` | NOT LISTABLE AS-IS | — | 334 SVGs (286 Iconify MIT/ISC + 48 themed) | Downloaded Iconify set; reselling it is the restricted route per 2025-06-10. Keep 20 originals. |
| `custom-personalized-generators/` | NOT A PRODUCT | — | 3 generators + 15 SVGs + 2 reports (birth flower, abundance, book illustration) | Commission listings sell labour ($22-162), not files. Not a replacement. Park. |

`products/README.md` documents the above table plus verification method and suggested work order.

---

## free-obtained/ — bulk source material (generators + downloaded CC0)

*This is where the "137 of 137 covered" claim comes from. It describes category coverage, not sellable products. See `products/` for what actually lists. This tree is source material; most of it is not a listing.*

| Folder | What | Generator | Output | Sellable? |
|--------|------|-----------|--------|-----------|
| `01-digital-planners/` | Digital planners | `generate_planner.py` (reportlab+pypdf) | `planner_2026_6month_hyperlinked.pdf` 223p, hyperlinked | Source for `products/2026-hyperlinked-digital-planner/` (the good one) |
| `02-svg-bundles/` | SVG bundles | `download_iconify.py` + `generate_themed_svgs.py` | `svg-bundles/` 334 SVGs (286 Iconify + 48 themed: Christian/Halloween/Fall/Floral/Sarcastic) | Download set not listable; 48 themed originals are base |
| `03-wall-art/` | Wall art | `download_met_art.py` + `generate_wall_art.py` | `met-wall-art/` 60 CC0 Met images + `wall-art-png/` 72 generated + `Wall_Art_Collection.pdf` | Mets genuine; rectangles rejected |
| `04-coloring-pages/` | Coloring pages | `generate_coloring.py` | `Free_Coloring_Pages_Bundle.pdf` 50p | Rejected tiling — rebuild |
| `05-spreadsheet-trackers/` | Trackers | `generate_tracker.py` | `Ultimate_Budget_Tracker_Template.xlsx` 6 sheets | Source for `products/ultimate-budget-tracker/` (hollow tabs) |
| `06-notion-templates/` | Notion | n/a (curated links) | `FREE_ALTERNATIVES.md` — 24 listings → free Notion gallery | Links, not a product — must build original template |
| `07-canva-templates/` | Canva | `generate_templates.py` | 104 SVGs + `FREE_ALTERNATIVES.md` | Unverified; Canva-stock resale blocked |
| `08-plr-mrr-bundles/` | PLR/MRR | n/a (curated) | `FREE_SOURCES.md` — 7 free PLR sites | PLR resale as-is now restricted (2025-06-10) |
| `09-ai-video-pipeline/` | AI video | `generate_pipeline.py` + `batch_generate.sh` | 5 scripts + pipeline | Source for `products/faceless-video-pipeline/` |
| `10-digital-product-ideas/` | Ideas guide | `generate_ideas.py` | `Digital_Product_Ideas_Guide.md` (137 listings → 71 hot) | Source for `products/digital-product-ideas-guide/` |
| `11-custom-personalized/` | Custom | 3 generators | 15 SVGs + 2 reports | Generators, not products |
| `README.md` | — | — | Per-category method + `Cost if bought on Etsy $1,495 → Our cost $0` table | Documents coverage, not readiness |

Plus root validators: `validate_all.py`, `deep_validate.py`, `concrete_evidence.py`, `quick_check.py`.

---

## What to do next (priority order from MASTER_CATALOG)

1. **List the planner** — `products/2026-hyperlinked-digital-planner/` — cover art, 12-month, Mon/Sun. Generator makes variants free.
2. **Deepen the tracker** — real Income/Expenses formulas, 12 monthly tabs, Google Sheets version.
3. **Rebuild the coloring book** — real line art (coloring is the best beachhead: 20% @ 1,450). Current PDF is rejected.
4. **Prove the video pipeline** — clean-machine end-to-end run, then package ($15-35, the only runnable-code listing in a PDF category).
5. **Curate the wall art** — 60 Mets into 6 themed sets of 10, 300 DPI, correct ratios; discard rectangles.
6. **Park the rest** until 1-5 are done. Do not list anything from Tier 4 (`MASTER_CATALOG` red).

---

*If you change anything, regenerate `MASTER_CATALOG` via the script that built it (see `MASTER_CATALOG.csv` header) and re-run validators in `free-obtained/`.*
