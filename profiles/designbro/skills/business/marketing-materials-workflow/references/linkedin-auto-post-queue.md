# LinkedIn Auto-Post Script (Queue-Based Publishing)

**Script**: `<HERMES_ROOT>/shared/linkedin/auto-post.py`
**Language**: Python 3 (stdlib only, no deps)
**Cron**: `linkedin-auto-post` — `no_agent=True`, schedule `0 10,14,19 * * *`

## How It Works

1. Globs all `P*.txt` files in the posts directory
2. Reads `published.json` tracker to find what's already published
3. Picks the first unpublished file (sorted alphabetically)
4. Publishes via `linkedin.py post-file <path>`
5. Appends to `published.json` with date + output
6. Prints result for cron delivery

## File Structure

```
<HERMES_ROOT>/shared/marketing/linkedin/
├── posts/                      # Post queue directory
│   ├── P01-intro-azienda.txt
│   ├── P02-problem-solution.txt
│   ├── P03-case-study-ristorante.txt
│   ├── ...
│   └── P35-cta-prova-gratuita.txt
├── published.json              # Tracker (auto-managed)
└── editorial-calendar-luglio.md # Calendar reference (not used by script)
```

## published.json Format

```json
{
  "published": [
    {
      "file": "P01-intro-azienda.txt",
      "date": "2026-06-05",
      "scheduled": "2026-07-01",
      "output": "Post published! ID: urn:li:share:..."
    }
  ]
}
```

## Adding New Posts

1. Create `P36-{slug}.txt` in the posts directory
2. Script auto-discovers on next run
3. No config changes needed

## Queue Exhaustion

When all posts are published, script prints:
"No unpublished posts remaining in <HERMES_ROOT>/shared/marketing/linkedin/posts/"
With `deliver: local`, this goes to [REDACTED — dati personali rimossi]'s chat as a notification.

## Dual-Cron Pattern

Two LinkedIn crons run simultaneously with staggered schedules:
- `linkedin-content-calendar` (Wannabe profile, LLM): 9:00, 12:00, 18:00
- `linkedin-auto-post` (script, queue): 10:00, 14:00, 19:00

Total: 6 posts/day. Each cron is independent — no shared state.

## Post Naming Convention

`P{NN}-{kebab-case-slug}.txt`

- NN = zero-padded sequence number (01, 02, ..., 35)
- slug = short descriptive name
- Content = plain text, no frontmatter, no metadata
- Max length: 1300 chars (LinkedIn limit for text posts)

## Pitfalls

- Script uses `subprocess.run` → if linkedin.py fails, error is captured in tracker
- No retry logic — if publish fails, the post stays "unpublished" and retries next run
- Posts publish in alphabetical order by filename → P01 before P02
- If you rename/move a .txt file, update published.json to match the new filename
