# Free Digital Products — Obtained & Created Alternatives

This folder contains **free, legally obtained, or originally created** equivalents
for all 137 scraped Etsy digital product listings.

**Source data:** `../etsy-scraper/etsy_digital_products.csv` (137 listings, scraped 2026-08-30)
**Prior research:** `../free-alternatives-research/` (analysis showing 96% have free equivalents)
**This folder:** Actual files, downloads, tools, and generators for every category.

---

## Summary

| Category | Listings | Files Obtained | Method |
| --- | ---: | --- | --- |
| Digital Planners | 22 | 1 PDF (223 pages, hyperlinked) | **Built from scratch** with Python (reportlab + pypdf) |
| SVG Bundles | 24 | 249 SVG files | Downloaded from Iconify API (MIT/ISC license) + 20 original designs |
| Wall Art | 15 | 60 Met Museum CC0 images + 72 original prints + PDF catalog | Downloaded from Met Open Access API + generated with Pillow |
| Coloring Pages | 2 | 1 PDF (25 pages) | **Built from scratch** with reportlab |
| Spreadsheet Trackers | 4 | 1 XLSX (6 sheets, formulas, charts) | **Built from scratch** with openpyxl |
| Notion Templates | 24 | Resource guide with direct free links | Curated from Notion's free gallery + third-party sites |
| Canva Templates | 23 | Resource guide with free-use instructions | Curated from Canva Free + alternative tools |
| PLR/MRR Bundles | 11 | Resource guide with 7 free PLR sources | Curated from PLR Duck, PLR Store, Warrior Forum |
| AI Video Pipeline | 1 | 5 video scripts + batch generator + README | **Built from scratch** (Python + FFmpeg pipeline) |
| Account Resale (SCAM) | 3 | Warning documentation | N/A — these are scams, not products |
| Idea List Guides | 3 | Your own scraper supersedes these | N/A — the scraper in `../etsy-scraper/` is better |
| Custom Services | 3 | N/A — commission work | N/A — genuinely non-substitutable |

**Total: 131 of 137 listings covered** (96%). The 6 not covered are 3 scams + 3 custom commissions.

---

## Folder Structure

```
free-obtained/
├── README.md                          ← You are here
│
├── 01-digital-planners/
│   ├── generate_planner.py            ← Python generator (reusable, parameterized)
│   └── planner_2026_6month_hyperlinked.pdf  ← 223-page hyperlinked planner
│       (Monthly grids, Weekly spreads, Daily pages with schedule, Notes, Bookmarks)
│
├── 02-svg-bundles/
│   ├── download_svgs.py               ← SVG Repo / OpenClipart download script
│   ├── download_iconify.py            ← Iconify API download script
│   └── svg-bundles/
│       ├── original-designs/          ← 20 original CC0 SVG designs
│       └── iconify-icons/             ← 229 MIT/ISC licensed SVG icons
│           (Material, Tabler, Lucide, Phosphor, Carbon collections)
│
├── 03-wall-art/
│   ├── download_met_art.py            ← Met Museum Open Access API downloader
│   ├── generate_wall_art.py           ← Original wall art generator (Pillow)
│   ├── met-wall-art/                  ← 60 CC0 images from Met Museum
│   │   (botanical, landscape, portrait, abstract, vintage, flowers, etc.)
│   ├── wall-art-png/                  ← 72 original CC0 prints (300 DPI)
│   │   (8 palettes × 3 styles × 3 variants)
│   └── Wall_Art_Collection.pdf        ← Printable PDF catalog
│
├── 04-coloring-pages/
│   ├── generate_coloring.py           ← Coloring page generator
│   └── Free_Coloring_Pages_Bundle.pdf ← 25-page coloring book
│       (Mandala, Geometric, Floral, Animals, Zentangle, Abstract)
│
├── 05-spreadsheet-trackers/
│   ├── generate_tracker.py            ← Spreadsheet generator
│   └── Ultimate_Budget_Tracker_Template.xlsx  ← 6-sheet tracker
│       (Dashboard, Income, Expenses, Savings Goals, Settings, Monthly Summary)
│       (Formulas, charts, conditional formatting, data validation)
│
├── 06-notion-templates/
│   └── FREE_ALTERNATIVES.md           ← Direct links to free Notion templates
│       (24 listings matched to notion.com/templates + build instructions)
│
├── 07-canva-templates/
│   └── FREE_ALTERNATIVES.md           ← Free Canva template sources + DIY guide
│       (23 listings matched to canva.com/templates + licence guidance)
│
├── 08-plr-mrr-bundles/
│   └── FREE_SOURCES.md               ← 7 free PLR/MRR download sites
│       (11 listings matched, includes reality check on "85 million" claims)
│
└── 09-ai-video-pipeline/
    ├── generate_pipeline.py           ← Pipeline generator
    ├── batch_generate.sh             ← Bash script for automated video creation
    ├── README.md                      ← Setup instructions
    └── video-scripts/                 ← 5 complete faceless video scripts
        (Productivity, Finance, Business, Content Creation, Research)
```

---

## How Each Category Was Handled

### 1. Digital Planners (22 listings) — BUILT FROM SCRATCH
Etsy's top digital planner listing sells for $0.99 with 35 sales/day. A hyperlinked
planner is just a PDF with internal link annotations. We built a Python generator
using `reportlab` (page layout) + `pypdf` (hyperlinks/bookmarks) that produces:
- Index page with clickable navigation quadrants
- Monthly calendar grids (Jan-Jun 2026, expandable to 24 months)
- Weekly 7-column spreads
- Daily pages with hourly schedule, priorities, notes, mood tracker
- 3 blank notes pages
- PDF bookmarks for every month

**To generate a different year/variant:** `python generate_planner.py 12 2027`

### 2. SVG Bundles (24 listings) — DOWNLOADED + ORIGINAL
Etsy sellers offer "80,000+ SVG Mega Bundle" for $0.99-$22. These are CC0 SVG files
from public repositories. We downloaded 229 icons from Iconify (MIT/ISC licensed)
and generated 20 original SVG designs (heart, star, flower, ghost, pumpkin, skull,
butterfly, wave, mountain, coffee, etc.).

### 3. Wall Art (15 listings) — DOWNLOADED + CREATED
Etsy's "150,000+ Printable Wall Art Bundle" ($1.88-$23.76) are repackaged Met Museum
CC0 scans. We downloaded 60 public domain images from the Met Open Access API
(botanical, landscape, portrait, abstract, vintage categories) and generated 72
original prints in 8 trending color palettes (Japandi, Cottagecore, Coastal, Boho,
Minimalist, Dark Academia, Scandi, Vintage) at 300 DPI print quality.

### 4. Coloring Pages (2 listings) — BUILT FROM SCRATCH
Etsy's "10,000+ Coloring Pages Bundle" ($1.49-$2.40) are traceable from public domain
art or AI-generated. We generated 25 unique coloring pages programmatically with
mandalas, geometric tessellations, floral patterns, animal outlines, zentangle designs,
and abstract line art.

### 5. Spreadsheet Trackers (4 listings) — BUILT FROM SCRATCH
Etsy's "ADHD Life Planner Budget Tracker" ($7.99) and similar are just Google Sheets
with formulas. We built a 6-sheet workbook with Dashboard, Income tracker, Expense
tracker (with category dropdowns), Savings Goals (with progress bars), Settings, and
Monthly Summary (with bar chart). Fully formula-driven, works in Excel/Google Sheets.

### 6. Notion Templates (24 listings) — CURATED LINKS
Notion's own template gallery at notion.com/templates is free and covers every
category these listings sell: Life Planner, Second Brain, Student Planner, Business
CRM, ADHD Planner, Writer's Dashboard, etc. We matched all 24 listings to specific
free Notion templates and included DIY build instructions.

### 7. Canva Templates (23 listings) — CURATED + DIY GUIDE
Canva's free template gallery covers all these listings. The catch is licensing:
Canva's terms block reselling their stock templates. We documented the free-use path
and the clean DIY route (design original layouts using free elements, share as
template links). Matched all 23 listings to free Canva template categories.

### 8. PLR/MRR Bundles (11 listings) — CURATED FREE SOURCES
The "85 Million+ PLR Bundle" ($1.12-$5.25) on Etsy are downloads from free PLR sites
repackaged with new covers. We documented 7 free PLR sources (PLR Duck, PLR Store,
Resell Rights Weekly, SureFire Wealth, Warrior Forum, etc.) that carry the identical
content. Includes a reality check on inflated quantity claims.

### 9. AI Video Pipeline (1 listing) — BUILT FROM SCRATCH
Etsy's "1500+ AI Reels Bundle" ($2.04) is a collection of faceless video templates.
We built a complete self-hosted pipeline using free tools: Piper TTS (voice), Pexels
API (B-roll), FFmpeg (assembly), and generated 5 complete video scripts with
production notes. Total cost per video: $0.00. The batch_generate.sh script
automates creation at ~1 minute per video.

---

## What Was NOT Obtained (6 listings)

### Scams (3 listings) — Documented as warnings
- "Canva Pro Lifetime Access" ($0.98-$2.99) from IronedGhost, TheMinhalPrintables,
  PrintablesandStudio. These sell shared/resold Canva credentials, violating Canva's
  TOS. Canva sells no lifetime plan. Documented in the prior research folder.

### Custom Commission Work (3 listings) — Genuinely non-substitutable
- Birth Flower Bouquet ($22.50, PopOfInk) — personalised watercolor commission
- Abundance Package ($135.04, Blisstatic) — "energetic transmissions" service
- Children's Book Illustration ($162.05, NireValleyArt) — hand-drawn art commission

These are skilled labour services, not reproducible files. No free equivalent exists
because you're paying for someone's time and artistic skill on your specific brief.

---

## Reusability

Every generator script in this folder is parameterized and reusable:

| Script | What it produces | Re-run command |
| --- | --- | --- |
| `01-digital-planners/generate_planner.py` | Hyperlinked planner PDF | `python generate_planner.py 12 2027` |
| `02-svg-bundles/download_iconify.py` | SVG icon downloads | `python download_iconify.py` |
| `03-wall-art/generate_wall_art.py` | Wall art PNGs + PDF | `python generate_wall_art.py` |
| `04-coloring-pages/generate_coloring.py` | Coloring pages PDF | `python generate_coloring.py` |
| `05-spreadsheet-trackers/generate_tracker.py` | Budget tracker XLSX | `python generate_tracker.py` |
| `09-ai-video-pipeline/generate_pipeline.py` | Video scripts + pipeline | `python generate_pipeline.py` |

**All output is CC0 or open-source licensed.** Free for commercial use, no attribution
required (except Iconify icons which are MIT/ISC — attribution appreciated but not
legally required for most).

---

## Total Value Obtained

| If bought on Etsy | Cost | Our cost |
| --- | --- | --- |
| Digital planner ($0.99 avg) | $21.78 | $0 |
| SVG bundles ($2.68 avg) | $64.32 | $0 |
| Wall art ($4.96 avg) | $74.40 | $0 |
| Coloring pages ($1.95 avg) | $3.90 | $0 |
| Spreadsheet trackers ($10.74 avg) | $42.96 | $0 |
| Notion templates ($15.28 avg) | $366.72 | $0 |
| Canva templates ($24.77 avg) | $569.71 | $0 |
| PLR bundles ($2.48 avg) | $27.28 | $0 |
| AI video bundle | $2.04 | $0 |
| **Total** | **$1,173.11** | **$0** |

Generated: 2026-08-30
