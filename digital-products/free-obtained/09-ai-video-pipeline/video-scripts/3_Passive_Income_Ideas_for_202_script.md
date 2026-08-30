# 3 Passive Income Ideas for 2026

## Niche: finance
## Duration: ~30s

## Full Script

I made $10,000 in passive income last month. Here's how:

Idea 1: Digital products. Create once, sell forever. Templates, planners, ebooks.
Idea 2: Print on demand. Upload designs, a service handles printing and shipping.
Idea 3: Content creation. Build an audience, monetize with ads and sponsorships.

Save this video. Start with idea 1 today. Follow for more.

## Production Notes
- Voice: en_US-amy-medium (Piper TTS, free)
- B-roll keywords: money, laptop, freedom, beach, success
- Music mood: inspirational
- Format: 1080x1920 (9:16 vertical)
- Source B-roll from: pexels.com (free API)

## FFmpeg Assembly Command (reference)
```bash
# 1. Generate voiceover with Piper TTS
echo "I made $10,000 in passive income last month. Here's how: Idea 1: Digital products. Create once, sell forever. Templates, planners, ebooks.
Idea 2: Print on demand. Upload designs, a service handles printing and shipping.
Idea 3: Content creation. Build an audience, monetize with ads and sponsorships. Save this video. Start with idea 1 today. Follow for more." | \
  piper --model en_US-amy-medium.onnx --output voiceover.wav

# 2. Download B-roll from Pexels API
# curl "https://www.pexels.com/videos/search/money/" 

# 3. Combine with FFmpeg
ffmpeg -i broll.mp4 -i voiceover.wav -i music.mp3 \
  -filter_complex "[0:v]scale=1080:1920,setsar=1[v]" \
  -map "[v]" -map 1:a -map 2:a -c:a aac -shortest \
  -t 30 output.mp4
```
