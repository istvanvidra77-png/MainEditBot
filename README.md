# MainEditBot (VideoEditBot fork)

A lightweight video editing bot skeleton (fork of VideoEditBot). Includes:
- Editor/videoEditor.py — core editing utilities (moviepy-based).
- combiner.py — concatenate videos and add background audio.
- discordBot.py — simple Discord bot to accept attachments and run jobs.
- func_helper.py — helper utilities.
- config.json.template — example configuration.

Requirements:
- Python 3.8+
- FFmpeg installed and on PATH
- See requirements.txt for Python packages

Quick start:
1. Install system dependencies (ffmpeg). See install.txt.
2. Create and activate a venv, then:
   pip install -r requirements.txt
   or see "pip install stuff.txt"
3. Copy config.json.template -> config.json and fill your DISCORD token (or set env var DISCORD_TOKEN).
4. Run the bot:
   python discordBot.py
5. In Discord, use command `!edit` with video attachments to combine them.

Notes:
- This is a starting point. Production usage should add checks, sanitization, size limits, timeouts and persistent job queues.
- For large files prefer using streaming upload and a background worker system.
