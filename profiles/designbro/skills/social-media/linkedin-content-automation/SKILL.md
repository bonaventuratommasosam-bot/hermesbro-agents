---
name: linkedin-content-automation
description: Automate LinkedIn content publishing — batch post creation, scheduling via cron, dedup tracking, and cadence management for company/personal pages.
tags: [linkedin, marketing, automation, content, social-media, cron]
triggers:
  - "publish linkedin posts"
  - "schedule linkedin content"
  - "linkedin calendar"
  - "auto-post linkedin"
  - "linkedin batch"
---

# LinkedIn Content Automation

Automate LinkedIn posting from Hermes: create posts, publish via API, schedule via cron, track what's been published.

## Prerequisites

- LinkedIn script: `<HERMES_ROOT>/shared/linkedin/linkedin.py`
- Config: `<HERMES_ROOT>/shared/linkedin/config.env` (OAuth tokens)
- Posts directory: `<HERMES_ROOT>/shared/marketing/linkedin/posts/`
- Tracker: `<HERMES_ROOT>/shared/marketing/linkedin/published.json`
- Auto-poster source: `<HERMES_ROOT>/shared/linkedin/auto-post.py`
- Auto-poster for cron: `~/.hermes/scripts/linkedin-auto-post.py` (must be real copy, not symlink)

## Key Commands

```bash
# Publish a single post (personal page)
python3 <HERMES_ROOT>/shared/linkedin/linkedin.py post "text here"

# Publish from file
python3 <HERMES_ROOT>/shared/linkedin/linkedin.py post-file /path/to/post.txt

# Publish as org (requires LINKEDIN_ORG_URN in config.env)
python3 <HERMES_ROOT>/shared/linkedin/linkedin.py post-org "text here"

# Run auto-poster (publishes next unpublished post)
python3 <HERMES_ROOT>/shared/linkedin/auto-post.py
```

## Workflow: Batch Content Creation

1. Write posts as individual `.txt` files in `<HERMES_ROOT>/shared/marketing/linkedin/posts/`
2. Naming: `P01-slug.txt`, `P02-slug.txt`, ... (sorted alphabetically = publish order)
3. Run auto-poster manually or via cron
4. Tracker (`published.json`) prevents duplicates

## Cadence

- **6x/day** is current cadence (validated 2026-06-05): two crons, staggered
- **Cron 1** (`linkedin-content-calendar`, Wannabe profile, LLM): 9:00, 12:00, 18:00
- **Cron 2** (`linkedin-auto-post`, script, queue): 10:00, 14:00, 19:00
- With 35 pre-written posts + LLM-generated posts = ~12+ days of content
- When stock runs low, create more posts proactively

## Cron Setup

**Pitfall — ALWAYS check for existing crons first**: Run `cronjob list` BEFORE creating a new LinkedIn posting cron. [REDACTED — dati personali rimossi] corrected: "esiste gia un job". If a similar job exists, UPDATE it (schedule, prompt) instead of creating a duplicate. If [REDACTED — dati personali rimossi] wants both, stagger the schedules by 1 hour.

```bash
# Queue-based auto-poster (no_agent=True)
# Script must be in ~/.hermes/scripts/ as a real file (NOT a symlink).
# Copy: cp <HERMES_ROOT>/shared/linkedin/auto-post.py ~/.hermes/scripts/linkedin-auto-post.py
cronjob create:
  schedule: "0 10,14,19 * * *"
  no_agent: true
  script: linkedin-auto-post.py

# LLM-driven content calendar (no_agent=false, Wannabe profile)
cronjob create:
  schedule: "0 9,12,18 * * *"
  profile: wannabe
  deliver: origin   # Must use 'origin' — wannabe profile has no telegram configured
```

## Post Writing Rules (HermesBro brand)

- Italian language, professional + slightly ironic
- Max 20 words per sentence
- Max 2 emoji per post
- Numbers > adjectives
- Hashtags at end: `#HermesBro #AI #PMI`
- Mix formats: text, poll questions (as text), case study, question, before/after

## Manual Batch Publishing

When [REDACTED — dati personali rimossi] says "vai avanti" / "pubblica i post" / "fai tutto":

1. Check `published.json` for last published post ID
2. Publish next unpublished post via `python3 linkedin.py post-file <path>`
3. Note the `urn:li:share:XXXXXXXX` ID returned
4. Update `published.json` with the new entry:
   ```python
   import json
   with open('published.json', 'r') as f:
       data = json.load(f)
   data['published'].append({
       'id': 'P02-slug-name',
       'share_id': 'urn:li:share:XXXXXXXX',
       'url': 'https://www.linkedin.com/feed/update/urn:li:share:XXXXXXXX',
       'date': 'YYYY-MM-DD',
       'time': 'HH:MM'
   })
   with open('published.json', 'w') as f:
       json.dump(data, f, indent=2)
   ```
5. Repeat for next posts in queue (batch of 5-6 is safe)
6. Report count published to [REDACTED — dati personali rimossi]

**Pitfall — tracker not auto-updated**: The `linkedin.py post-file` command publishes but does NOT update `published.json`. You must update it manually after each batch. Without this, the auto-poster cron may re-publish the same post.

## Content Calendar Creation

When creating a content calendar (`content-calendar.md`):
1. Scan all existing `.txt` files in `posts/` directory
2. Categorize by type: education, case-study, question, CTA, BTS, focus-bot
3. Create 2-week grid: 6 slots/day (09:00, 10:00, 12:00, 13:00, 18:00, 19:00)
4. Schedule existing posts across slots, leaving ~60% as "dynamic" for LLM-generated content
5. Format: table with Date | Time | Type | Content/Post ID | Status

## Pitfalls

- **Poll API broken**: LinkedIn API returns 422 for `shareMediaCategory: "POLL"`. Publish polls as text posts instead. (Validated 2026-06-05)
- **Org posting needs ORG_URN**: `post-org` fails without `LINKEDIN_ORG_URN` in config.env. Get it via LinkedIn org admin page or API (needs `w_organization_social` scope + admin role).
- **Token expiry**: Access token expires ~60 days. Use `python3 linkedin.py refresh` to renew. Script auto-saves new token to config.env.
- **Rate limits**: Don't publish >25 posts/day. 6x/day (dual cron) is safe.
- **No images via auto-poster**: Current pipeline is text-only. For image posts, use `post-image` or `post-file-image` manually.
- **Duplicate crons**: [REDACTED — dati personali rimossi] said "esiste gia un job" when a duplicate was created. ALWAYS `cronjob list` first.
- **Stagger dual crons**: If running 2 posting crons, offset by 1 hour to avoid same-slot double-posts.
- **Script path: NO symlinks, NO absolute paths**: The `script` field in cron jobs must be a bare filename (e.g. `linkedin-auto-post.py`). The file must exist as a REAL file in `~/.hermes/scripts/` — NOT a symlink to `<HERMES_ROOT>/shared/...`. Symlinks that resolve outside the scripts directory are blocked with "script path escapes the scripts directory via traversal". Always `cp` the script, never `ln -s`. **Two-directory trap**: Symlinks can exist in BOTH `~/.hermes/scripts/` and `~/.hermes/profiles/<name>/scripts/`. If EITHER contains a symlink that resolves outside its directory, the bare filename update fails. Fix: replace symlinks with real copies (`rm symlink && cp real-file`) in BOTH locations before updating the cron job's script field.
- **Script path: no `python3` prefix, no args**: The `script` field is a filename, not a shell command. `script: python3 auto-post.py` fails with "Script not found". `script: conversation-summary.py --hours 2` also fails. For args or multi-command sequences, create a wrapper `.sh` script.
- **Cross-profile delivery**: When a cron runs under a profile (e.g. `wannabe`) that doesn't have telegram configured, `deliver: "telegram:chat_id:thread_id"` fails with "platform 'telegram' not configured/enabled". Use `deliver: "origin"` instead — it routes output back to the profile that created the cron job, which has telegram configured.
