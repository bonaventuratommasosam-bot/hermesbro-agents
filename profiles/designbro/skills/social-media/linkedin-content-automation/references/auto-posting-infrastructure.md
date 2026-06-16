# Auto-Posting Infrastructure (LinkedIn)

## Pattern: Dedup-Tracked Auto-Poster

When content is pre-written as numbered .txt files (P01-slug.txt, P02-slug.txt...), use a dedup-tracked auto-poster to publish one post per cron tick.

### Files

| File | Purpose |
|------|---------|
| `<HERMES_ROOT>/shared/linkedin/auto-post.py` | Source script (copy to `~/.hermes/scripts/linkedin-auto-post.py` for cron use) |
| `~/.hermes/scripts/linkedin-auto-post.py` | Cron-resident copy (real file, NOT symlink) |
| `<HERMES_ROOT>/shared/linkedin/linkedin.py` | LinkedIn API wrapper (called by auto-post.py) |
| `<HERMES_ROOT>/shared/marketing/linkedin/published.json` | Tracker: `{published: [{file, date, output}]}` |
| `<HERMES_ROOT>/shared/marketing/linkedin/posts/*.txt` | Post content files, sorted alphabetically = publish order |

### How It Works

1. Script scans `posts/` directory for `P*.txt` files
2. Compares against `published.json` to find unpublished
3. Publishes the FIRST unpublished file (sorted by name)
4. Appends to tracker with file name, date, and LinkedIn response
5. Exits (one post per run)

### Cron Setup

```
schedule: "0 10,14,19 * * *"
no_agent: true
script: linkedin-auto-post.py
```

The script must be a real file in `~/.hermes/scripts/` (not a symlink).
Copy it: `cp <HERMES_ROOT>/shared/linkedin/auto-post.py ~/.hermes/scripts/linkedin-auto-post.py`

### Running Out of Posts

When all posts are published, the script prints "No unpublished posts remaining." and exits silently. Monitor the count:
```bash
# Check remaining
python3 -c "import json; t=json.load(open('published.json')); print(f'{len(t[\"published\"])} published')"
# Count total available
ls posts/P*.txt | wc -l
```

When stock runs low, create more posts proactively. With 3x/day cadence, 35 posts = ~12 days.

### Extending for New Months

1. Write new posts as P36-slug.txt, P37-slug.txt, etc. (or reset numbering)
2. No need to update tracker — it's dedup by filename
3. If resetting (new month), archive old published.json and start fresh

### Pitfalls

- **No images**: Current auto-poster is text-only. For image posts, use `post-file-image` manually or extend the script.
- **File order matters**: Posts publish in alphabetical order by filename. Use P01-, P02- prefix for explicit ordering.
- **Tracker is append-only**: To re-publish a post, remove its entry from published.json.
