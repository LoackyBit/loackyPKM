#!/usr/bin/env python3
"""youtube_helper.py - Media extraction utility for YouTube videos.

Extracts transcripts, chapters, metadata and optional keyframe screenshots for the Second Brain.
Includes visual heuristic detection, network timeout/retry, and missing transcript guards.
"""

import sys
import os
import re
import time
import datetime
import subprocess
import argparse
import json
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

# Custom Exception Hierarchy
class YouTubeHelperError(Exception):
    """Base exception for YouTube helper errors."""
    pass

class TranscriptUnavailableError(YouTubeHelperError):
    """Raised when no subtitles or transcripts are available for a video."""
    pass

class VideoMetadataError(YouTubeHelperError):
    """Raised when video metadata extraction fails."""
    pass

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


def fetch_metadata_with_retry(url: str, timeout: int = 15, max_retries: int = 1, backoff: float = 2.0) -> Dict[str, Any]:
    """Fetches video metadata via yt_dlp with timeout and exponential backoff retry per D-19."""
    if yt_dlp is None:
        return {
            'title': 'Video YouTube',
            'uploader': 'Canale YouTube',
            'duration': 0,
            'chapters': [],
            'url': None
        }

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestvideo[height<=720][ext=mp4]/best[height<=720]/best',
        'socket_timeout': timeout
    }

    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Video YouTube'),
                    'uploader': info.get('uploader', 'Canale YouTube'),
                    'duration': info.get('duration', 0),
                    'chapters': info.get('chapters', []) or [],
                    'url': info.get('url')
                }
        except Exception as e:
            last_exc = e
            if attempt < max_retries:
                time.sleep(backoff * (attempt + 1))

    print(f"Warning: yt-dlp metadata extraction failed for {url}: {last_exc}", file=sys.stderr)
    return {
        'title': 'Video YouTube',
        'uploader': 'Canale YouTube',
        'duration': 0,
        'chapters': [],
        'url': None
    }


def fetch_transcript_with_retry(video_id: str, timeout: int = 15, max_retries: int = 1, backoff: float = 2.0) -> List[Dict[str, Any]]:
    """Fetches transcript snippets prioritizing Italian then English with retry per D-18, D-19."""
    if YouTubeTranscriptApi is None:
        raise TranscriptUnavailableError(f"Libreria youtube-transcript-api non disponibile per estrarre trascrizioni per {video_id}.")

    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            fetched = YouTubeTranscriptApi().fetch(video_id, languages=['it', 'en'])
            transcript_list = []
            for snippet in fetched:
                transcript_list.append({
                    'text': getattr(snippet, 'text', snippet.get('text', '') if isinstance(snippet, dict) else str(snippet)),
                    'start': getattr(snippet, 'start', snippet.get('start', 0) if isinstance(snippet, dict) else 0),
                    'duration': getattr(snippet, 'duration', snippet.get('duration', 0) if isinstance(snippet, dict) else 0)
                })
            if transcript_list:
                return transcript_list
        except Exception as e:
            last_exc = e
            if attempt < max_retries:
                time.sleep(backoff * (attempt + 1))

    raise TranscriptUnavailableError(f"Nessuna trascrizione disponibile per il video {video_id} (lingue 'it', 'en'). Dettagli: {last_exc}")


def extract_frame(stream_url: str, timestamp: float, output_path: str, timeout: int = 30) -> bool:
    """Extracts a single screenshot frame via ffmpeg fast seeking with 720p JPEG compression per D-08, D-19."""
    try:
        cmd = [
            'ffmpeg', '-y',
            '-ss', str(datetime.timedelta(seconds=int(timestamp))),
            '-i', stream_url,
            '-frames:v', '1',
            '-q:v', '2',
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=timeout)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except Exception as e:
        print(f"Frame extraction failed at timestamp {timestamp}: {e}", file=sys.stderr)
        return False


def extract_youtube_data(url: str, output_note_path: Optional[str] = None,
                         extract_frames: bool = False, force_frames: Optional[bool] = None,
                         vault_root: Optional[str] = None) -> Dict[str, Any]:
    """Extracts metadata, chapters, transcript, and optional keyframe screenshots dynamically per D-06, D-08, D-09, D-18."""
    root = get_vault_root(vault_root)
    clipboard_dir = os.path.join(root, "99 - Meta", "Clipboard")
    os.makedirs(clipboard_dir, exist_ok=True)

    video_id = get_video_id(url)
    if not video_id:
        raise ValueError(f"Invalid YouTube URL: {url}")

    # Fetch metadata
    meta = fetch_metadata_with_retry(url)
    title = meta.get('title', 'Video YouTube')
    channel = meta.get('uploader', 'Canale YouTube')
    duration = meta.get('duration', 0)
    chapters = meta.get('chapters', []) or []
    stream_url = meta.get('url')

    # Fetch transcript (Guarded: raises TranscriptUnavailableError if missing per D-18)
    transcript_list = fetch_transcript_with_retry(video_id)

    # Visual content heuristic vs explicit CLI flags
    all_chapter_titles = " ".join([ch.get('title', '') for ch in chapters if isinstance(ch, dict)])
    is_visual = is_visual_content(title, all_chapter_titles)
    if force_frames is not None:
        should_extract_frames = force_frames
    else:
        should_extract_frames = extract_frames or is_visual

    extracted_images = []
    if should_extract_frames and stream_url:
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
            ch_title = ch.get('title', f"Parte {idx + 1}") if isinstance(ch, dict) else f"Parte {idx + 1}"
            start = ch.get('start_time', 0) if isinstance(ch, dict) else 0
            end = ch.get('end_time', duration) if isinstance(ch, dict) else duration
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
        'is_visual': is_visual,
        'url': url
    }


def build_arg_parser() -> argparse.ArgumentParser:
    """Builds CLI argument parser for youtube_helper."""
    parser = argparse.ArgumentParser(description="YouTube transcript & multimedia extraction helper.")
    parser.add_argument('url', help="YouTube video URL")
    parser.add_argument('--extract-frames', action='store_true', help="Force keyframe extraction")
    parser.add_argument('--no-frames', action='store_true', help="Disable keyframe extraction")
    parser.add_argument('--json', action='store_true', help="Output results as JSON")
    parser.add_argument('--vault-root', type=str, default=None, help="Vault root directory")
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    force_frames = None
    if args.extract_frames:
        force_frames = True
    elif args.no_frames:
        force_frames = False

    try:
        data = extract_youtube_data(
            url=args.url,
            force_frames=force_frames,
            vault_root=args.vault_root
        )
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Title: {data['title']}")
            print(f"Channel: {data['channel']}")
            print(f"Visual: {data['is_visual']}")
            print(f"Transcript segments: {len(data['transcript'])}")
            print(f"Extracted frames: {len(data['extracted_images'])}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
