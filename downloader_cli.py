#!/usr/bin/env python3
"""
🎬 Command-Line Video Downloader - Offline Version
Simple CLI tool for downloading videos without web interface
"""

import yt_dlp
import argparse
import os
import sys
import shutil
from pathlib import Path

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    return shutil.which("ffmpeg") is not None

def print_banner():
    """Print banner"""
    print("""
╔═══════════════════════════════════════════════╗
║  🎬 Offline Video Downloader CLI              ║
║  Download videos from YouTube & other sites   ║
╚═══════════════════════════════════════════════╝
    """)

def download_video(url, quality, output_dir):
    """Download video with specified quality"""
    
    quality_map = {
        "best": "bestvideo+bestaudio/best",
        "8k": "bestvideo[height<=4320]+bestaudio/best",
        "6k": "bestvideo[height<=4320]+bestaudio/best",
        "4k": "bestvideo[height<=2160]+bestaudio/best",
        "1080": "bestvideo[height<=1080]+bestaudio/best",
        "720": "bestvideo[height<=720]+bestaudio/best",
        "480": "bestvideo[height<=480]+bestaudio/best",
        "basic": "best[ext=mp4]/best",
        "audio": "bestaudio/best",
    }
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📥 Downloading in {quality.upper()} quality...")
    print(f"📁 Save location: {output_dir}")
    
    ydl_opts = {
        "format": quality_map.get(quality.lower(), "best"),
        "outtmpl": os.path.join(output_dir, "%(title).50s_%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "progress_hooks": [progress_hook],
        "quiet": False,
        "no_warnings": True,
    }
    
    if check_ffmpeg():
        ydl_opts["ffmpeg_location"] = shutil.which("ffmpeg")
        print(f"✅ FFmpeg found at: {shutil.which('ffmpeg')}")
        
        if quality.lower() not in ["basic", "audio"]:
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }]
    else:
        print("⚠️  FFmpeg not found - high quality downloads may fail!")
    
    if quality.lower() == "audio":
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("\n⏳ Processing...")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"\n✅ Download successful!")
            print(f"📄 File: {os.path.basename(filename)}")
            print(f"📁 Location: {filename}")
            return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def progress_hook(d):
    """Show download progress"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').replace('%', '').strip()
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\r📊 Progress: {percent:>5}% | Speed: {speed:>10} | ETA: {eta:>8}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\r✅ Download finished!                                                 ")

def main():
    parser = argparse.ArgumentParser(
        description="🎬 Offline Video Downloader - Download videos from the web",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://youtube.com/watch?v=... -q 4k
  %(prog)s https://youtube.com/watch?v=... -q 1080 -o ~/Videos
  %(prog)s https://youtube.com/watch?v=... -q audio
        """
    )
    
    parser.add_argument("url", help="Video URL")
    parser.add_argument(
        "-q", "--quality",
        choices=["best", "8k", "6k", "4k", "1080", "720", "480", "basic", "audio"],
        default="4k",
        help="Video quality (default: 4k)"
    )
    parser.add_argument(
        "-o", "--output",
        default=str(Path.home() / "Downloads" / "VideoDownloader"),
        help="Output directory (default: ~/Downloads/VideoDownloader)"
    )
    
    args = parser.parse_args()
    
    print_banner()
    print(f"📎 URL: {args.url}")
    print(f"🎯 Quality: {args.quality.upper()}")
    print(f"📁 Output: {args.output}")
    print("─" * 50)
    
    success = download_video(args.url, args.quality, args.output)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
