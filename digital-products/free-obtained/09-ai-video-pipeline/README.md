# AI Faceless Video Pipeline — Free & Self-Hosted

Replaces the Etsy listing "1500+ AI Reels Bundle" ($2.04).

## What This Contains

- `video-scripts/` — 5 complete faceless video scripts with production notes
- `batch_generate.sh` — Batch processing script for automated video generation
- `test_pipeline.py` — End-to-end test script (4 test cases, all passing)
- `generate_pipeline.py` — Generator that creates scripts, batch file, and README

## Tested Configuration

This pipeline has been **end-to-end tested** on:
- **OS:** Windows 11
- **FFmpeg:** 8.1 (gyan.dev full build)
- **Python:** 3.12.3
- **Piper TTS:** Not installed (pipeline uses silent fallback with tone)

Test results: 4/4 test cases PASS (short title, long title, special characters, full 30s duration).

## Free Tools Used

| Component | Tool | Cost | Notes |
|---|---|---|---|
| Script writing | ChatGPT Free / Gemini Free | $0 | Or use local Ollama |
| Voice synthesis | Piper TTS | $0 | Runs offline, no API. Optional - pipeline falls back to tone audio |
| B-roll footage | Pexels API | $0 | Free API key |
| B-roll (backup) | Pixabay API | $0 | No key needed |
| Video editing | FFmpeg | $0 | Command-line, fully scriptable |
| Captions | whisper.cpp | $0 | Local transcription (FFmpeg 8.1 includes whisper support) |
| Background music | Pixabay Music | $0 | CC0 tracks |
| Thumbnail design | Canva Free | $0 | Free tier sufficient |

## Quick Start

1. Install FFmpeg: `winget install ffmpeg` (Windows) or `apt install ffmpeg` (Linux)
2. (Optional) Install Piper TTS: `pip install piper-tts`
3. Run the test: `python test_pipeline.py`
4. Run batch generation: `bash batch_generate.sh`
5. Output: MP4 videos (1080x1920, 9:16 vertical) in `output/` directory

## Windows Notes

On Windows, FFmpeg's `drawtext` filter requires an explicit `fontfile` path.
The batch script auto-detects Windows and uses `C:/Windows/Fonts/arial.ttf`.
On Linux/Mac, fontconfig handles fonts automatically (no fontfile needed).

Special characters in titles (`:`, `'`) must be escaped in the drawtext filter.
The test script handles this automatically.

## Test Cases

The `test_pipeline.py` script tests 4 edge cases:

| Test | Description | Status |
|---|---|---|
| short_title | 4-character title | PASS |
| long_title | 63-character title | PASS |
| special_chars | Title with `:` and `&` | PASS |
| full_30s | Full 30-second duration | PASS |

## Scaling to 1500+ Videos

The Etsy listing claims "1500+ AI Reels". Here's how to match that for free:

1. Use ChatGPT to generate 100 topic ideas per niche (10 niches = 1000 scripts)
2. Each script runs through the pipeline automatically
3. Total time: ~1 minute per video = 16 hours for 1000 videos
4. Total cost: $0.00
