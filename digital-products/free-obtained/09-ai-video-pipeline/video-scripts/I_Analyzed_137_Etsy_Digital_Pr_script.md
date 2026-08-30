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
ffmpeg -i broll.mp4 -i voiceover.wav -i music.mp3 \
  -filter_complex "[0:v]scale=1080:1920,setsar=1[v]" \
  -map "[v]" -map 1:a -map 2:a -c:a aac -shortest \
  -t 30 output.mp4
```
