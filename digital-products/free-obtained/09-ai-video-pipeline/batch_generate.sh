#!/bin/bash
# Faceless Video Batch Generator (Cross-platform: Windows WSL/Linux/Mac)
# Usage: bash batch_generate.sh
# Requirements: ffmpeg (required), piper TTS (optional - falls back to silent)
# Tested on: Windows 11 + FFmpeg 8.1 (gyan.dev build) + Python 3.12

set -e

# Detect platform for font path
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OS" == "Windows_NT" ]]; then
    FONT_FILE="C:/Windows/Fonts/arial.ttf"
else
    FONT_FILE=""  # Linux/Mac: fontconfig handles this automatically
fi

PIPER_MODEL="en_US-amy-medium"
VIDEO_W=1080
VIDEO_H=1920
DURATION=30
OUTPUT_DIR="output"
mkdir -p "$OUTPUT_DIR"

generate_video() {
    local title="$1"
    local script="$2"
    local broll_keyword="$3"
    local output_name=$(echo "$title" | tr ' ' '_' | tr -dc 'a-zA-Z0-9_')
    local output_path="${OUTPUT_DIR}/${output_name}.mp4"
    
    echo "Generating: $title"
    
    # Check if Piper TTS is available
    local voice_audio=""
    if command -v piper &>/dev/null; then
        echo "  Using Piper TTS for voiceover..."
        echo "$script" | piper --model "${PIPER_MODEL}.onnx" --output "${OUTPUT_DIR}/voice_${output_name}.wav"
        voice_audio="-i ${OUTPUT_DIR}/voice_${output_name}.wav"
    else
        echo "  Piper TTS not found, generating with tone fallback..."
        voice_audio=""
    fi
    
    # Build drawtext filter with fontfile if on Windows
    local drawtext_filter=""
    if [[ -n "$FONT_FILE" ]]; then
        drawtext_filter="drawtext=fontfile='${FONT_FILE}':text='${title}':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2"
    else
        drawtext_filter="drawtext=text='${title}':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2"
    fi
    
    # Generate video with animated background
    if [[ -n "$voice_audio" ]]; then
        ffmpeg -y \
            -f lavfi -i "color=c=0x1a1a2e:s=${VIDEO_W}x${VIDEO_H}:d=${DURATION}:r=30" \
            -f lavfi -i "sine=frequency=440:duration=${DURATION}" \
            -i "${OUTPUT_DIR}/voice_${output_name}.wav" \
            -vf "${drawtext_filter}" \
            -map 0:v -map 2:a -c:a aac -b:a 128k \
            -t ${DURATION} "$output_path" 2>/dev/null
        rm -f "${OUTPUT_DIR}/voice_${output_name}.wav"
    else
        ffmpeg -y \
            -f lavfi -i "color=c=0x1a1a2e:s=${VIDEO_W}x${VIDEO_H}:d=${DURATION}:r=30" \
            -f lavfi -i "sine=frequency=440:duration=${DURATION}" \
            -vf "${drawtext_filter}" \
            -map 0:v -map 1:a -c:a aac -b:a 128k \
            -t ${DURATION} "$output_path" 2>/dev/null
    fi
    
    echo "  Done: $output_path"
}

# Generate all videos
generate_video "5 Productivity Tips" "These 5 tips saved me 10 hours every week. Number 1 the 2 minute rule. If it takes less than 2 minutes do it now. Number 2 time blocking. Schedule every hour. Number 3 Pomodoro technique 25 minutes work 5 minutes rest. Number 4 single task. Close all tabs. Number 5 review weekly. Follow for daily tips." "office"

generate_video "3 Passive Income Ideas" "I made 10000 in passive income last month. Idea 1 digital products. Create once sell forever. Idea 2 print on demand. Upload designs and a service handles everything. Idea 3 content creation. Build an audience monetize with ads. Follow for more." "money"

generate_video "Etsy Digital Products Truth" "Most Etsy digital product sellers are reselling free content. 80000 SVG bundles are from SVG Repo free. 150000 wall art prints are Met Museum public domain. 10000 coloring pages are AI generated. Notion templates are from the free gallery. Follow to learn more." "computer"

echo ""
echo "All videos generated in ${OUTPUT_DIR}/"
ls -la "${OUTPUT_DIR}"/*.mp4 2>/dev/null || echo "No MP4 files found"
