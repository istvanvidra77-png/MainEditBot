# discordBot.py
# Simple Discord bot entrypoint that accepts attachments and triggers video tasks.
# Requires: discord.py (v1.7+ or 2.x), asyncio, moviepy installed.
# Set DISCORD_TOKEN env var or use config.json.

import os
import json
import asyncio
import logging
from pathlib import Path
from discord.ext import commands
from func_helper import download_attachment, ensure_dir
from Editor.videoEditor import VideoEditor
from combiner import combine_videos

log = logging.getLogger("discordbot")
log.setLevel(logging.INFO)

# Load config
CFG_PATH = Path("config.json")
if CFG_PATH.exists():
    with open(CFG_PATH, "r") as f:
        cfg = json.load(f)
else:
    cfg = {}
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") or cfg.get("discord_token")
OUTPUT_DIR = cfg.get("output_dir", "output")
TMP_DIR = cfg.get("temp_dir", "temp")

bot = commands.Bot(command_prefix="!", intents=None)


@bot.event
async def on_ready():
    log.info("Bot ready as %s", bot.user)


@bot.command(name="edit", help="Upload attachments with this command to trigger a simple combine job.")
async def edit(ctx):
    # Simple handler: download attachments, concatenate them
    if not ctx.message.attachments:
        await ctx.send("Please attach one or more video files to concatenate.")
        return

    ensure_dir(TMP_DIR)
    editor = VideoEditor(temp_dir=TMP_DIR, output_dir=OUTPUT_DIR)

    saved = []
    for att in ctx.message.attachments:
        local = Path(TMP_DIR) / att.filename
        await download_attachment(att, local)
        saved.append(str(local))

    await ctx.send(f"Downloaded {len(saved)} files, starting combine...")
    loop = asyncio.get_running_loop()
    try:
        out_name = f"combined_{ctx.message.id}.mp4"
        out_path = Path(OUTPUT_DIR) / out_name
        # run combine in thread to avoid blocking
        result = await loop.run_in_executor(None, combine_videos, saved, str(out_path))
        await ctx.send(f"Completed: {out_path.name}", file=discord.File(str(out_path)))
    except Exception as e:
        log.exception("Error during edit task")
        await ctx.send(f"An error occurred: {e}")


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        log.error("DISCORD_TOKEN not set in env or config.json")
        print("Set DISCORD_TOKEN env or add to config.json and re-run.")
    else:
        bot.run(DISCORD_TOKEN)
