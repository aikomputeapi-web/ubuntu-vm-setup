#!/bin/bash
# Faceless Video Batch Generator
# Usage: bash batch_generate.sh
# Requirements: piper (TTS), ffmpeg, curl, jq

set -e

PIPER_MODEL="en_US-amy-medium"
VIDEO_W=1080
VIDEO_H=1920
DURATION=30

generate_video() {
    local title="$1"
    local script="$2"
    local broll_keyword="$3"
    local output_name=$(echo "$title" | tr ' ' '_' | tr -dc 'a-zA-Z0-9_')
    
    echo "Generating: $title"
    
    # 1. Generate voiceover
    echo "$script" | piper --model "${PIPER_MODEL}.onnx" --output "voice_${output_name}.wav"
    
    # 2. Download B-roll (Pexels free API)
    # Get free API key from https://www.pexels.com/api/
    # PEXELS_API_KEY="your-key-here"
    # curl -s -H "Authorization: $PEXELS_API_KEY" \
    #   "https://api.pexels.com/videos/search?query=${broll_keyword}&per_page=1" | \
    #   jq -r '.videos[0].video_files[0].link' | xargs curl -o "broll_${output_name}.mp4"
    
    # 3. Create simple animated background as B-roll alternative
    ffmpeg -f lavfi -i "color=c=0x1a1a2e:s=${VIDEO_W}x${VIDEO_H}:d=${DURATION}:r=30" \
        -f lavfi -i "sine=frequency=440:duration=${DURATION}" \
        -i "voice_${output_name}.wav" \
        -filter_complex \
        "[0:v]drawtext=text='${title}':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2[v]" \
        -map "[v]" -map 2:a -c:a aac -b:a 128k \
        -t ${DURATION} "${output_name}.mp4" -y
    
    echo "Done: ${output_name}.mp4"
    rm -f "voice_${output_name}.wav"
}

# Generate all videos
generate_video "5 Productivity Tips" "These 5 tips saved me 10 hours every week. Number 1 the 2 minute rule. If it takes less than 2 minutes do it now. Number 2 time blocking. Schedule every hour. Number 3 Pomodoro technique 25 minutes work 5 minutes rest. Number 4 single task. Close all tabs. Number 5 review weekly. Follow for daily tips." "office"

generate_video "3 Passive Income Ideas" "I made 10000 in passive income last month. Idea 1 digital products. Create once sell forever. Idea 2 print on demand. Upload designs and a service handles everything. Idea 3 content creation. Build an audience monetize with ads. Follow for more." "money"

generate_video "Etsy Digital Products Truth" "Most Etsy digital product sellers are reselling free content. 80000 SVG bundles are from SVG Repo free. 150000 wall art prints are Met Museum public domain. 10000 coloring pages are AI generated. Notion templates are from the free gallery. Follow to learn more." "computer"

echo "All videos generated!"
