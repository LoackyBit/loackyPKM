#!/usr/bin/env python3
"""youtube_helper.py - Media extraction utility for YouTube videos.

Extracts transcripts, chapters, metadata and optional keyframe screenshots for the Second Brain.
"""

import sys
import os
import re
import datetime
import subprocess
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

# Keywords indicating visual content (diagrams, UI, code, architecture)
VISUAL_KEYWORDS = [
    'demo', 'tutorial', 'install', 'setup', 'config', 'code', 'coding', 'program',
    'screen', 'interface', 'ui', 'ux', 'design', 'schema', 'diagram', 'architecture',
    'chart', 'graph', 'slide', 'presentation', 'walkthrough', 'how to', 'how-to',
    'guida', 'installazione', 'configurazione', 'codice', 'programmazione', 'schermata',
    'interfaccia', 'diagramma', 'architettura', 'schema', 'esempio pratico', 'dimostrazione'
]


def get_vault_root(start_path: Optional[str] = None) -> str:
    """Dynamically resolves the root path of the Second Brain vault."""
    if start_path:
        return os.path.abspath(start_path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, "..", ".."))


def is_visual_content(title: str, chapter_title: str = '') -> bool:
    """Evaluates whether video content contains relevant visual demonstrations."""
    text = (title + ' ' + chapter_title).lower()
    return any(kw in text for kw in VISUAL_KEYWORDS)


def get_video_id(url: str) -> Optional[str]:
    """Extracts 11-character YouTube video ID from URL string."""
    match = re.search(r'(?:v=|/|embed/|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
    return match.group(1) if match else None


def extract_frame(stream_url: str, timestamp: float, output_path: str) -> bool:
    """Extracts a single screenshot frame via ffmpeg fast seeking."""
    try:
        cmd = [
            'ffmpeg', '-y',
            '-ss', str(datetime.timedelta(seconds=int(timestamp))),
            '-i', stream_url,
            '-frames:v', '1',
            '-q:v', '2',
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except Exception as e:
        print(f"Frame extraction failed at timestamp {timestamp}: {e}", file=sys.stderr)
        return False


def extract_youtube_data(url: str, output_note_path: Optional[str] = None,
                         extract_frames: bool = False, vault_root: Optional[str] = None) -> Dict[str, Any]:
    """Extracts metadata, chapters, transcript, and optional keyframe screenshots dynamically."""
    root = get_vault_root(vault_root)
    clipboard_dir = os.path.join(root, "99 - Meta", "Clipboard")
    os.makedirs(clipboard_dir, exist_ok=True)

    video_id = get_video_id(url)
    if not video_id:
        raise ValueError(f"Invalid YouTube URL: {url}")

    title = "Video YouTube"
    channel = "YouTube"
    duration = 0
    chapters = []
    stream_url = None

    if yt_dlp is not None:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'bestvideo[height<=480][ext=mp4]/best[height<=480]/best'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Video YouTube')
                channel = info.get('uploader', 'Canale YouTube')
                duration = info.get('duration', 0)
                chapters = info.get('chapters', [])
                stream_url = info.get('url')
        except Exception as e:
            print(f"Warning: yt-dlp metadata extraction failed for {url}: {e}", file=sys.stderr)

    transcript_list = []
    if YouTubeTranscriptApi is not None:
        try:
            transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['it', 'en'])
        except Exception as e:
            print(f"Warning: Transcript unavailable for {video_id}: {e}", file=sys.stderr)

    extracted_images = []
    if extract_frames and stream_url:
        video_is_visual = is_visual_content(title)
        if not chapters and duration > 0:
            step = duration / 4
            chapters = [
                {
                    'title': f"Parte {i + 1}",
                    'start_time': i * step,
                    'end_time': (i + 1) * step
                } for i in range(4)
            ]

        for idx, ch in enumerate(chapters):
            ch_title = ch.get('title', f"Parte {idx + 1}")
            start = ch.get('start_time', 0)
            end = ch.get('end_time', duration)
            target_time = start + 10 if (end - start) > 20 else (start + (end - start) / 2)

            safe_title = re.sub(r'[^a-zA-Z0-9]', '_', ch_title).lower()[:15]
            img_name = f"{video_id}_{idx}_{safe_title}.jpg"
            img_path = os.path.join(clipboard_dir, img_name)

            if extract_frame(stream_url, target_time, img_path):
                extracted_images.append(img_path)

    return {
        'video_id': video_id,
        'title': title,
        'channel': channel,
        'duration': duration,
        'chapters': chapters,
        'transcript': transcript_list,
        'extracted_images': extracted_images,
        'url': url
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_helper.py <url> [--extract-frames]")
        sys.exit(1)

    url = sys.argv[1]
    extract_frames = "--extract-frames" in sys.argv

    try:
        data = extract_youtube_data(url, extract_frames=extract_frames)
        print(f"Title: {data['title']}")
        print(f"Channel: {data['channel']}")
        print(f"Transcript segments: {len(data['transcript'])}")
        print(f"Extracted frames: {len(data['extracted_images'])}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
