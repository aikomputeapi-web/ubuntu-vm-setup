# 11 - Custom Personalized Products

Free open-source alternatives for 3 Etsy listings that were originally commissioned
custom-service products (hand-illustrated art, personalized spiritual artwork,
custom children's book illustrations). These products were the only listings in the
137 scraped set that had no free equivalent available online.

Instead of finding free alternatives, we built **generators** that produce similar-
quality customizable products for free.

## Generators

### 1. Birth Flower Family Bouquet (Listing #30)
**Original:** PopOfInk (27.3k sales, $22.50) - Personalized watercolor birth flower prints
**Our tool:** `generate_birth_flower.py` - Creates personalized SVG bouquet prints using
botanical flower data for each birth month (12 flowers with proper symbolism data).

```bash
# Default family
python generate_birth_flower.py

# Custom family (Name:Month,Name:Month)
python generate_birth_flower.py --names "Mom:3,Dad:7,Emma:11,Liam:5" --title "Our Family"
```

**Output:** 2 SVGs (bouquet print + flower info card)
- 12 birth month flowers with accurate botanical data (Latin names, symbolism)
- Customizable names, birth months, and title
- Bouquet layout with labeled flowers and decorative frame

### 2. Abundance Energetic Artwork (Listing #31)
**Original:** Blisstatic (19.8k sales, $135.04) - "Charged" digital artwork + personal report
**Our tool:** `generate_abundance.py` - Creates mandala-style artwork SVGs with
personalized abundance reports based on name and intention.

```bash
# Default
python generate_abundance.py

# Custom
python generate_abundance.py --name "Sarah" --intention prosperity
python generate_abundance.py --name "John" --intention health --seed 12345
```

**Output:** 1 SVG artwork + 1 markdown report per intention
- 5 intention themes: prosperity, health, love, success, peace
- Unique mandala seeded by name (deterministic, reproducible)
- Personalized report with affirmations and reflection prompts

### 3. Custom Children's Book Illustration (Listing #32)
**Original:** NireValaryArt (4.2k sales, $162.05) - Custom hand-drawn book illustrations
**Our tool:** `generate_illustration.py` - Creates whimsical vintage-style children's book
illustration SVGs in 4 scene templates with character templates.

```bash
# Generate all scenes
python generate_illustration.py

# Custom title
python generate_illustration.py --title "The Brave Little Bunny" --character rabbit
```

**Output:** 4 book covers + 4 story pages + 3 character templates = 11 SVGs
- 4 scenes: forest, meadow, underwater, night sky
- 3 character templates: rabbit, bear, child
- Story page layout with illustration area + text area
- Vintage storybook art style with layered elements

## Output

All generated files are in the `output/` subfolder:
- 15 SVG prints (all valid, with viewBox)
- 2 markdown reports
- 3 Python generators
