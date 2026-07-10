# combiner.py
# Functions to combine/concatenate videos and optionally add background music.

from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from pathlib import Path
import logging

log = logging.getLogger("combiner")
log.setLevel(logging.INFO)


def combine_videos(video_paths, output_path, method="concatenate", fps=24, remove_audio=False):
    """
    Combine video files into one output file.
    - video_paths: list of file paths (strings or Path objects)
    - output_path: destination path (string or Path)
    - method: 'concatenate' for linear concatenation (default)
    """
    video_paths = [str(p) for p in video_paths]
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    log.info("Combining %d clips into %s", len(video_paths), out)

    clips = []
    for p in video_paths:
        c = VideoFileClip(p)
        if remove_audio:
            c = c.without_audio()
        clips.append(c)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(str(out), codec="libx264", audio_codec="aac", fps=fps)

    # close clips
    for c in clips:
        c.close()
    final.close()
    return str(out)


def add_background_music(video_path, music_path, output_path, music_volume=0.6, music_start=0):
    """Adds background music to a video (mix)."""
    video_path = str(video_path)
    music_path = str(music_path)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    log.info("Adding background music %s to %s -> %s", music_path, video_path, out)

    with VideoFileClip(video_path) as v:
        bg = AudioFileClip(music_path).volumex(music_volume).set_start(music_start)
        # make bg same length as v
        bg = bg.set_duration(v.duration)
        final = v.set_audio(bg)
        final.write_videofile(str(out), codec="libx264", audio_codec="aac")
    return str(out)
