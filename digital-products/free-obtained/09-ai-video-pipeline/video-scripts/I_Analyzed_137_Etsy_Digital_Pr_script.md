# I Analyzed 137 Etsy Digital Products — Here's What I Found

## Niche: research
## Duration: ~30s

## Full Script

I scraped 137 top-selling Etsy digital products and the results are shocking:

79% of listings have a free equivalent available online.
17% are free to use but not free to resell due to licensing.
3 listings are outright scams selling fake Canva Pro accounts.
Only 3 out of 137 are genuinely non-substitutable commission work.
The most lucrative category? Digital planners at 35 sales per day.

Full breakdown in my free guide. Follow for the link.

## Production Notes
- Voice: en_US-amy-medium (Piper TTS, free)
- B-roll keywords: data, computer, chart, money, analysis
- Music mood: suspense
- Format: 1080x1920 (9:16 vertical)
- Source B-roll from: pexels.com (free API)

## FFmpeg Assembly Command (reference)
```bash
# 1. Generate voiceover with Piper TTS
echo "I scraped 137 top-selling Etsy digital products and the results are shocking: 79% of listings have a free equivalent available online.
17% are free to use but not free to resell due to licensing.
3 listings are outright scams selling fake Canva Pro accounts.
Only 3 out of 137 are genuinely non-substitutable commission work.
The most lucrative category? Digital planners at 35 sales per day. Full breakdown in my free guide. Follow for the link." | \
  piper --model en_US-amy-medium.onnx --output voiceover.wav

# 2. Download B-roll from Pexels API
# curl "https://www.pexels.com/videos/search/data/" 

# 3. Combine with FFmpeg
# Windows: use -vf drawtext with fontfile='C\:/Windows/Fonts/arial.ttf'
# Linux/Mac: fontconfig handles fonts automatically (omit fontfile)
ffmpeg -y \
  -f lavfi -i "color=c=0x1a1a2e:s=1080x1920:d=30:r=30" \
  -f lavfi -i "sine=frequency=440:duration=30" \
  -i voiceover.wav \
  -vf "drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='I Analyzed 137 Etsy Digital Products — Here's What I Found':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
  -map 0:v -map 2:a -c:a aac -b:a 128k \
  -t 30 output.mp4

# Note: On Linux/Mac, remove fontfile='...' from the drawtext filter
# Note: Escape colons in text with \: and single quotes with \'
```
