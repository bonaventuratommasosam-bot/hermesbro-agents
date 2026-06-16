#!/usr/bin/env python3
"""
LinkedIn Auto-Poster per HermesBro.
Pubblica il prossimo post non ancora pubblicato dalla directory posts/.
Traccia cosa è già stato pubblicato in published.json.
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

POSTS_DIR = Path("<HERMES_ROOT>/shared/marketing/linkedin/posts")
TRACKER = Path("<HERMES_ROOT>/shared/marketing/linkedin/published.json")
LINKEDIN_SCRIPT = Path("<HERMES_ROOT>/shared/linkedin/linkedin.py")

def load_tracker():
    if TRACKER.exists():
        return json.loads(TRACKER.read_text())
    return {"published": []}

def save_tracker(tracker):
    TRACKER.write_text(json.dumps(tracker, indent=2))

def main():
    tracker = load_tracker()
    published_files = {p["file"] for p in tracker["published"]}
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")

    # Get all post files sorted by name (P01, P02, ...)
    all_posts = sorted(POSTS_DIR.glob("P*.txt"))
    unpublished = [p for p in all_posts if p.name not in published_files]

    if not unpublished:
        print(f"[{now}] No unpublished posts remaining.")
        return

    # Publish the next one
    post_file = unpublished[0]
    post_text = post_file.read_text().strip()

    print(f"[{now}] Publishing {post_file.name}...")

    result = subprocess.run(
        ["python3", str(LINKEDIN_SCRIPT), "post", post_text],
        capture_output=True, text=True, timeout=30
    )

    if result.returncode == 0:
        output = result.stdout.strip()
        tracker["published"].append({
            "file": post_file.name,
            "date": today,
            "output": output
        })
        save_tracker(tracker)
        print(f"OK: {output}")
        print(f"Remaining: {len(unpublished) - 1} posts")
    else:
        print(f"ERR: {result.stderr.strip()}")

if __name__ == "__main__":
    main()
