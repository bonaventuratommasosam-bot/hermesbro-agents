#!/usr/bin/env python3
"""Batch send JPG photos to Telegram. Loads token once for speed.

Usage:
    python3 batch-send.py CHAT_ID /path/to/directory/ [caption_prefix]

Args:
    CHAT_ID: Telegram chat ID (numeric)
    directory: path containing .jpg files
    caption_prefix: optional prefix for captions (e.g. "Bot: ")

Reads TELEGRAM_BOT_TOKEN from ~/.hermes/profiles/designbro/.env
Sends all .jpg files in the directory, sorted alphabetically.
0.4s delay between sends to avoid rate limits.
"""
import os, sys, time, requests

def get_token():
    """Read token from .env without dotenv (avoids redaction filter issues)."""
    with open("<HERMES_ROOT>/profiles/designbro/.env") as f:
        for line in f:
            if line.startswith("TELEGRAM_"):
                return line.strip().split("=", 1)[1]
    raise ValueError("TELEGRAM token not found in .env")

TOKEN = get_token()
CHAT_ID = sys.argv[1]
PHOTO_DIR = sys.argv[2]
CAPTION_PREFIX = sys.argv[3] if len(sys.argv) > 3 else ""

photos = sorted([f for f in os.listdir(PHOTO_DIR) if f.endswith('.jpg')])
print(f"Sending {len(photos)} photos from {PHOTO_DIR}...", flush=True)

sent = 0
for i, fname in enumerate(photos, 1):
    path = os.path.join(PHOTO_DIR, fname)
    caption = f"{CAPTION_PREFIX}{fname.replace('.jpg','')}" if CAPTION_PREFIX else fname.replace('.jpg','')
    with open(path, 'rb') as f:
        resp = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"photo": f},
            timeout=30
        )
    ok = resp.json().get("ok", False)
    sent += 1 if ok else 0
    print(f"{i}/{len(photos)}: {fname} - {'ok' if ok else 'FAIL'}", flush=True)
    time.sleep(0.4)

print(f"\nDone: {sent}/{len(photos)}", flush=True)
