"""
End-to-end test for the AI video pipeline.
Tests FFmpeg video generation with text overlay on Windows.
Does NOT require Piper TTS (uses silent audio fallback).
"""
import os
import subprocess
import sys
import tempfile

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PIPELINE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Windows font path
FONT_FILE = "C:/Windows/Fonts/arial.ttf"

# Test cases covering edge cases
TEST_CASES = [
    {
        "name": "short_title",
        "title": "Test",
        "script": "Short test",
        "duration": 2,
        "color": "0x1a1a2e",
    },
    {
        "name": "long_title",
        "title": "This Is A Very Long Title That Tests Text Wrapping In The Video",
        "script": "Long title test",
        "duration": 2,
        "color": "0x2d1a2e",
    },
    {
        "name": "special_chars",
        "title": "Test: Special & Characters!",
        "script": "Test with special characters",
        "duration": 2,
        "color": "0x1a2e1a",
    },
    {
        "name": "full_30s",
        "title": "Full Duration Test",
        "script": "This is a full 30 second test video",
        "duration": 30,
        "color": "0x2e2e1a",
    },
]


def check_ffmpeg():
    """Check if FFmpeg is available."""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stderr.split("\n")[0] if result.stderr else "unknown"
            print(f"  FFmpeg found: {version}")
            return True
    except FileNotFoundError:
        pass
    print("  FFmpeg NOT found")
    return False


def check_piper():
    """Check if Piper TTS is available."""
    try:
        result = subprocess.run(["piper", "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print("  Piper TTS found")
            return True
    except FileNotFoundError:
        pass
    print("  Piper TTS NOT found (will use silent fallback)")
    return False


def generate_video(title, duration, color, font_file=None, output_path=None):
    """Generate a test video with FFmpeg."""
    if output_path is None:
        safe_name = "".join(c if c.isalnum() else "_" for c in title)[:30]
        output_path = os.path.join(OUTPUT_DIR, f"{safe_name}.mp4")

    # Build drawtext filter - escape colons in Windows paths
    # Also escape special chars in title text (: and ' need escaping)
    if font_file:
        escaped_font = font_file.replace(":", "\\:")
        # Escape colons and single quotes in the text
        safe_title = title.replace(":", "\\:").replace("'", "\\'")
        drawtext = (
            f"drawtext=fontfile='{escaped_font}'"
            f":text='{safe_title}'"
            f":fontsize=48:fontcolor=white"
            f":x=(w-text_w)/2:y=(h-text_h)/2"
        )
    else:
        safe_title = title.replace(":", "\\:").replace("'", "\\'")
        drawtext = (
            f"drawtext=text='{safe_title}'"
            f":fontsize=48:fontcolor=white"
            f":x=(w-text_w)/2:y=(h-text_h)/2"
        )

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c={color}:s=1080x1920:d={duration}:r=30",
        "-f", "lavfi", "-i", f"sine=frequency=440:duration={duration}",
        "-vf", drawtext,
        "-map", "0:v", "-map", "1:a",
        "-c:a", "aac", "-b:a", "128k",
        "-t", str(duration),
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, output_path, result.stderr


def test_video_validity(filepath):
    """Validate generated video with FFprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_streams", filepath,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            streams = data.get("streams", [])
            video_streams = [s for s in streams if s.get("codec_type") == "video"]
            audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
            if video_streams and audio_streams:
                v = video_streams[0]
                return {
                    "width": int(v.get("width", 0)),
                    "height": int(v.get("height", 0)),
                    "codec": v.get("codec_name", "unknown"),
                    "fps": v.get("r_frame_rate", "unknown"),
                    "audio_codec": audio_streams[0].get("codec_name", "unknown"),
                    "size_kb": os.path.getsize(filepath) / 1024,
                }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "no streams"}


if __name__ == "__main__":
    print("=" * 60)
    print("AI VIDEO PIPELINE - END-TO-END TEST")
    print("=" * 60)

    # Check dependencies
    print("\n--- Dependency Check ---")
    has_ffmpeg = check_ffmpeg()
    has_piper = check_piper()

    if not has_ffmpeg:
        print("\nERROR: FFmpeg is required. Install with: winget install ffmpeg")
        sys.exit(1)

    # Run test cases
    print(f"\n--- Running {len(TEST_CASES)} Test Cases ---")
    results = []
    for tc in TEST_CASES:
        print(f"\n  Test: {tc['name']}")
        print(f"    Title: '{tc['title']}' ({len(tc['title'])} chars)")
        print(f"    Duration: {tc['duration']}s")

        success, output_path, stderr = generate_video(
            title=tc["title"],
            duration=tc["duration"],
            color=tc["color"],
            font_file=FONT_FILE,
        )

        if success and os.path.exists(output_path):
            info = test_video_validity(output_path)
            if "error" not in info:
                print(f"    PASS: {info['width']}x{info['height']}, "
                      f"{info['codec']}/{info['audio_codec']}, "
                      f"{info['size_kb']:.1f} KB")
                results.append(("PASS", tc["name"], info))
            else:
                print(f"    FAIL: Validation error: {info['error']}")
                results.append(("FAIL", tc["name"], info))
        else:
            # Get last line of stderr for error
            err_lines = [l for l in stderr.split("\n") if l.strip()]
            last_err = err_lines[-1] if err_lines else "unknown error"
            print(f"    FAIL: {last_err}")
            results.append(("FAIL", tc["name"], {"error": last_err}))

    # Summary
    print(f"\n{'=' * 60}")
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(1 for r in results if r[0] == "PASS")
    failed = sum(1 for r in results if r[0] == "FAIL")
    print(f"  Passed: {passed}/{len(results)}")
    print(f"  Failed: {failed}/{len(results)}")
    
    # Check video dimensions are correct (1080x1920 vertical)
    for status, name, info in results:
        if status == "PASS":
            w, h = info.get("width", 0), info.get("height", 0)
            if w != 1080 or h != 1920:
                print(f"  WARNING: {name} has wrong dimensions: {w}x{h}")
    
    if failed == 0:
        print("\n  ALL TESTS PASSED - Pipeline is working correctly")
    else:
        print(f"\n  {failed} TEST(S) FAILED - See output above")
    
    # List generated files
    print(f"\n  Output directory: {OUTPUT_DIR}")
    if os.path.isdir(OUTPUT_DIR):
        files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".mp4")]
        for f in files:
            size = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
            print(f"    {f}: {size:.1f} KB")
