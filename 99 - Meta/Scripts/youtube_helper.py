#!/usr/bin/env python3
# youtube_helper.py - Estrae trascrizioni, metadati e cattura frame dai video YouTube per l'AI Second Brain.

import sys
import os
import re
import datetime
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

# Parole chiave che indicano contenuto visivo rilevante (demo, codice, interfacce, slide, schemi)
VISUAL_KEYWORDS = [
    'demo', 'tutorial', 'install', 'setup', 'config', 'code', 'coding', 'program',
    'screen', 'interface', 'ui', 'ux', 'design', 'schema', 'diagram', 'architecture',
    'chart', 'graph', 'slide', 'presentation', 'walkthrough', 'how to', 'how-to',
    'guida', 'installazione', 'configurazione', 'codice', 'programmazione', 'schermata',
    'interfaccia', 'diagramma', 'architettura', 'schema', 'esempio pratico', 'dimostrazione',
]

def is_visual_content(title: str, chapter_title: str = '') -> bool:
    """Determina se il contenuto e' visivo (vale la pena estrarre frame) basandosi sul titolo."""
    text = (title + ' ' + chapter_title).lower()
    return any(kw in text for kw in VISUAL_KEYWORDS)

def get_video_id(url):
    match = re.search(r'(?:v=|/|embed/|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
    return match.group(1) if match else None

def extract_frame(stream_url, timestamp, output_path):
    """Estrae un singolo frame velocemente a partire da un timestamp usando il seek rapido di ffmpeg."""
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
        print(f"Errore estrazione frame: {e}", file=sys.stderr)
        return False



def main():
    if len(sys.argv) < 3:
        print("Uso: python3 youtube_helper.py <url> <path_nota>")
        sys.exit(1)

    url = sys.argv[1]
    note_path = sys.argv[2]

    if not os.path.exists(note_path):
        print(f"Errore: la nota grezza '{note_path}' non esiste più.", file=sys.stderr)
        sys.exit(1)

    video_id = get_video_id(url)

    if not video_id:
        print("Errore: URL YouTube non valido", file=sys.stderr)
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    clipboard_dir = os.path.join(vault_root, "99 - Meta/Clipboard")
    os.makedirs(clipboard_dir, exist_ok=True)

    # 1. Estrazione metadati e stream URL con yt-dlp
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestvideo[height<=480][ext=mp4]/best[height<=480]/best'
    }

    print(f"Estrazione metadati per il video {video_id}...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video YouTube')
            channel = info.get('uploader', 'Canale YouTube')
            duration = info.get('duration', 0)
            chapters = info.get('chapters', [])
            stream_url = info.get('url')
        except Exception as e:
            print(f"Errore yt-dlp: {e}", file=sys.stderr)
            sys.exit(1)

    # 2. Estrazione trascrizione
    print("Estrazione trascrizione audio...")
    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['it', 'en'])
    except Exception as e:
        print(f"Impossibile estrarre trascrizione per {video_id}: {e}", file=sys.stderr)
        transcript_list = []

    # 3. Generazione capitoli e cattura frame (solo se il contenuto e' visivo)
    raw_content = []
    extracted_images = []  # Traccia i file immagine effettivamente creati

    # Valuta se il video in generale ha contenuto visivo rilevante dal titolo
    video_is_visual = is_visual_content(title)

    # Se non ci sono capitoli, dividiamo il video in 4 parti
    if not chapters and duration > 0:
        step = duration / 4
        chapters = [
            {
                'title': f"Parte {i+1}",
                'start_time': i * step,
                'end_time': (i+1) * step
            } for i in range(4)
        ]

    if video_is_visual:
        print(f"Contenuto visivo rilevato — avvio estrazione frame per i {len(chapters)} capitoli...")
    else:
        print(f"Video discorsivo rilevato — estrazione frame saltata per risparmiare spazio.")

    for idx, ch in enumerate(chapters):
        if not os.path.exists(note_path):
            print("Nota rimossa dall'utente durante l'estrazione. Abort.", file=sys.stderr)
            sys.exit(1)
            
        ch_title = ch.get('title', f"Parte {idx+1}")
        start = ch.get('start_time', 0)
        end = ch.get('end_time', duration)

        target_time = start + 10 if (end - start) > 20 else (start + (end - start) / 2)

        # Filtra i sottotitoli appartenenti a questo capitolo
        ch_text = []
        for entry in transcript_list:
            if start <= entry.start < end:
                ch_text.append(entry.text)

        raw_content.append(f"## {ch_title}\n")

        # Estrai frame SOLO se il video o il capitolo ha contenuto visivo rilevante
        chapter_is_visual = video_is_visual or is_visual_content(title, ch_title)
        if chapter_is_visual and stream_url:
            safe_title = re.sub(r'[^a-zA-Z0-9]', '_', ch_title).lower()[:15]
            img_name = f"{video_id}_{idx}_{safe_title}.jpg"
            img_path = os.path.join(clipboard_dir, img_name)
            print(f"Cattura screenshot capitolo {idx+1}: '{ch_title}' a {int(target_time)}s...")
            has_frame = extract_frame(stream_url, target_time, img_path)
            if has_frame:
                extracted_images.append(img_path)
                raw_content.append(f"![[{img_name}]]\n")

        raw_content.append(" ".join(ch_text) + "\n")

    # 4. Aggiorna la nota grezza in 03 - Inbox
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    updated_yaml = (
        f"---\n"
        f"ready: true\n"
        f"title: \"{title}\"\n"
        f"date: {date_str}\n"
        f"tags: [youtube, transcript, raw]\n"
        f"macro_area: \"\"\n"
        f"video_url: \"{url}\"\n"
        f"channel: \"{channel}\"\n"
        f"---\n"
        f"[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[{title}]]\n\n"
        f"# \U0001f3a5 {title}\n\n"
        f"- **Canale**: {channel}\n"
        f"- **Video URL**: {url}\n\n"
        f"---\n"
        + "\n".join(raw_content)
    )

    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(updated_yaml)

    frames_msg = f"{len(extracted_images)} screenshot salvati" if extracted_images else "nessun screenshot (video discorsivo)"
    print(f"Nota grezza aggiornata con successo con trascrizione e {frames_msg}.")


if __name__ == "__main__":
    main()
