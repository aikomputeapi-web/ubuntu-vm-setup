# AI Faceless Video Pipeline — Free & Self-Hosted

Replaces the Etsy listing "1500+ AI Reels Bundle" ($2.04).

## What This Contains

- `video-scripts/` — 5 complete faceless video scripts with production notes
- `batch_generate.sh` — Batch processing script for automated video generation

## Free Tools Used

| Component | Tool | Cost | Notes |
|---|---|---|---|
| Script writing | ChatGPT Free / Gemini Free | $0 | Or use local Ollama |
| Voice synthesis | Piper TTS | $0 | Runs offline, no API |
| B-roll footage | Pexels API | $0 | Free API key |
| B-roll (backup) | Pixabay API | $0 | No key needed |
| Video editing | FFmpeg | $0 | Command-line, fully scriptable |
| Captions | whisper.cpp | $0 | Local transcription |
| Background music | Pixabay Music | $0 | CC0 tracks |
| Thumbnail design | Canva Free | $0 | Free tier sufficient |

## Quick Start

1. Install Piper TTS: `pip install piper-tts`
2. Install FFmpeg: `winget install ffmpeg` (Windows) or `apt install ffmpeg` (Linux)
3. Run: `bash batch_generate.sh`
4. Output: MP4 videos ready for TikTok/Instagram/YouTube Shorts

## Scaling to 1500+ Videos

The Etsy listing claims "1500+ AI Reels". Here's how to match that for free:

1. Use ChatGPT to generate 100 topic ideas per niche (10 niches = 1000 scripts)
2. Each script runs through the pipeline automatically
3. Total time: ~1 minute per video = 16 hours for 1000 videos
4. Total cost: $0.00
