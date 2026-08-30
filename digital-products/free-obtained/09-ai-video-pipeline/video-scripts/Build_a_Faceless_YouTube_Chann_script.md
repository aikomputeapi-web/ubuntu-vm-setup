# Build a Faceless YouTube Channel in 7 Days

## Niche: content-creation
## Duration: ~30s

## Full Script

Day 1 to Day 7 of building a faceless channel from scratch:

Day 1: Pick a niche you can talk about for 100 videos.
Day 2: Set up your Canva account for thumbnails and graphics.
Day 3: Write your first 5 video scripts using ChatGPT.
Day 4: Record voiceovers using free TTS tools.
Day 5: Source B-roll from Pexels and Pixabay.
Day 6: Edit in CapCut or DaVinci Resolve, both free.
Day 7: Upload your first video. Consistency beats perfection.

Subscribe for the full journey. Link to free tools in bio.

## Production Notes
- Voice: en_US-amy-medium (Piper TTS, free)
- B-roll keywords: studio, editing, youtube, growth, chart
- Music mood: motivational
- Format: 1080x1920 (9:16 vertical)
- Source B-roll from: pexels.com (free API)

## FFmpeg Assembly Command (reference)
```bash
# 1. Generate voiceover with Piper TTS
echo "Day 1 to Day 7 of building a faceless channel from scratch: Day 1: Pick a niche you can talk about for 100 videos.
Day 2: Set up your Canva account for thumbnails and graphics.
Day 3: Write your first 5 video scripts using ChatGPT.
Day 4: Record voiceovers using free TTS tools.
Day 5: Source B-roll from Pexels and Pixabay.
Day 6: Edit in CapCut or DaVinci Resolve, both free.
Day 7: Upload your first video. Consistency beats perfection. Subscribe for the full journey. Link to free tools in bio." | \
  piper --model en_US-amy-medium.onnx --output voiceover.wav

# 2. Download B-roll from Pexels API
# curl "https://www.pexels.com/videos/search/studio/" 

# 3. Combine with FFmpeg
# Windows: use -vf drawtext with fontfile='C\:/Windows/Fonts/arial.ttf'
# Linux/Mac: fontconfig handles fonts automatically (omit fontfile)
ffmpeg -y \
  -f lavfi -i "color=c=0x1a1a2e:s=1080x1920:d=30:r=30" \
  -f lavfi -i "sine=frequency=440:duration=30" \
  -i voiceover.wav \
  -vf "drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='Build a Faceless YouTube Channel in 7 Days':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
  -map 0:v -map 2:a -c:a aac -b:a 128k \
  -t 30 output.mp4

# Note: On Linux/Mac, remove fontfile='...' from the drawtext filter
# Note: Escape colons in text with \: and single quotes with \'
```
