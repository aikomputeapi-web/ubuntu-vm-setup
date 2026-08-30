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
# Windows: use -vf drawtext with fontfile='C\:/Windows/Fonts/arial.ttf'
# Linux/Mac: fontconfig handles fonts automatically (omit fontfile)
ffmpeg -y \
  -f lavfi -i "color=c=0x1a1a2e:s=1080x1920:d=30:r=30" \
  -f lavfi -i "sine=frequency=440:duration=30" \
  -i voiceover.wav \
  -vf "drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='5 Productivity Tips That Changed My Life':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
  -map 0:v -map 2:a -c:a aac -b:a 128k \
  -t 30 output.mp4

# Note: On Linux/Mac, remove fontfile='...' from the drawtext filter
# Note: Escape colons in text with \: and single quotes with \'
```
