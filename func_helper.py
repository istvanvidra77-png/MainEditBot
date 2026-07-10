# func_helper.py
# Utility helpers for downloading, file safety and subprocess runs (lightweight).

import aiohttp
import asyncio
from pathlib import Path
import logging
import shutil
import os

log = logging.getLogger("func_helper")
log.setLevel(logging.INFO)


async def download_attachment(attachment, dest_path):
    """
    Download a discord.Attachment-like object to dest_path.
    Expects that attachment has a .url attribute and .filename
    """
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    url = getattr(attachment, "url", None)
    if not url:
        # Fallback: try reading attachment object as file (Discord library exposes .read())
        try:
            data = await attachment.read()
            dest_path.write_bytes(data)
            return str(dest_path)
        except Exception:
            raise ValueError("Attachment has no URL and could not be read.")
    log.info("Downloading %s -> %s", url, dest_path)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Failed to download {url}: {resp.status}")
            data = await resp.read()
            dest_path.write_bytes(data)
    return str(dest_path)


def ensure_dir(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


def safe_filename(name):
    keepchars = (" ", ".", "_", "-")
    return "".join(c for c in name if c.isalnum() or c in keepchars).rstrip()


def which(program):
    """Simple cross-platform which()"""
    return shutil.which(program)


def run_subprocess(cmd, cwd=None, timeout=None):
    import subprocess
    log.info("Running subprocess: %s", cmd)
    p = subprocess.run(cmd, shell=True, cwd=cwd, timeout=timeout, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr
