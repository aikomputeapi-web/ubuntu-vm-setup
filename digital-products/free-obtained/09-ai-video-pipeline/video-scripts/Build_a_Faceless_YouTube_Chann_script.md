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
ffmpeg -i broll.mp4 -i voiceover.wav -i music.mp3 \
  -filter_complex "[0:v]scale=1080:1920,setsar=1[v]" \
  -map "[v]" -map 1:a -map 2:a -c:a aac -shortest \
  -t 30 output.mp4
```
