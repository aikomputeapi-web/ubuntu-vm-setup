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
# Windows: use -vf drawtext with fontfile='C\:/Windows/Fonts/arial.ttf'
# Linux/Mac: fontconfig handles fonts automatically (omit fontfile)
ffmpeg -y \
  -f lavfi -i "color=c=0x1a1a2e:s=1080x1920:d=30:r=30" \
  -f lavfi -i "sine=frequency=440:duration=30" \
  -i voiceover.wav \
  -vf "drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='3 Passive Income Ideas for 2026':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
  -map 0:v -map 2:a -c:a aac -b:a 128k \
  -t 30 output.mp4

# Note: On Linux/Mac, remove fontfile='...' from the drawtext filter
# Note: Escape colons in text with \: and single quotes with \'
```
