# 5 Productivity Tips That Changed My Life

## Niche: self-improvement
## Duration: ~30s

## Full Script

These 5 tips saved me 10 hours every week:

Number 1: The 2-minute rule. If it takes less than 2 minutes, do it now.
Number 2: Time blocking. Schedule every hour including breaks.
Number 3: The Pomodoro technique. 25 minutes work, 5 minutes rest.
Number 4: Single-task. Close all tabs. One thing at a time.
Number 5: Review weekly. Every Sunday, plan the next 7 days.

Follow for daily productivity tips. Which one will you try first?

## Production Notes
- Voice: en_US-amy-medium (Piper TTS, free)
- B-roll keywords: office, working, clock, planning, success
- Music mood: upbeat
- Format: 1080x1920 (9:16 vertical)
- Source B-roll from: pexels.com (free API)

## FFmpeg Assembly Command (reference)
```bash
# 1. Generate voiceover with Piper TTS
echo "These 5 tips saved me 10 hours every week: Number 1: The 2-minute rule. If it takes less than 2 minutes, do it now.
Number 2: Time blocking. Schedule every hour including breaks.
Number 3: The Pomodoro technique. 25 minutes work, 5 minutes rest.
Number 4: Single-task. Close all tabs. One thing at a time.
Number 5: Review weekly. Every Sunday, plan the next 7 days. Follow for daily productivity tips. Which one will you try first?" | \
  piper --model en_US-amy-medium.onnx --output voiceover.wav

# 2. Download B-roll from Pexels API
# curl "https://www.pexels.com/videos/search/office/" 

# 3. Combine with FFmpeg
ffmpeg -i broll.mp4 -i voiceover.wav -i music.mp3 \
  -filter_complex "[0:v]scale=1080:1920,setsar=1[v]" \
  -map "[v]" -map 1:a -map 2:a -c:a aac -shortest \
  -t 30 output.mp4
```
