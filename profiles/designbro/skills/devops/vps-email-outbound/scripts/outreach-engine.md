# Outreach Engine — Production Sending Script

Production script at `<HERMES_ROOT>/shared/marketing/email/outreach-engine.py` (also copied to `~/.hermes/scripts/outreach-engine.py` for cron).

## Features
- Sequence-based: multiple email steps per lead with configurable delays
- Per-lead tracking in `sent-tracker.json` (prevents re-sending)
- Rate limiting (35s between sends)
- Template personalization ({nome}, {azienda}, {settore})
- Sector-specific template routing
- Dry-run mode, status mode, add-leads mode
- Cron-automated (daily 10:00, reports to Telegram)

## Usage
```bash
python3 outreach-engine.py              # Send batch
python3 outreach-engine.py --dry-run    # Simulate
python3 outreach-engine.py --status     # Show campaign status
python3 outreach-engine.py --add-leads FILE.csv  # Import leads
```

## Key config (top of script)
```python
FROM_EMAIL = "hermesbro10@hermesbro.cloud"  # MUST match SPF/DKIM domain
BATCH_SIZE = 10          # emails per cron run
DELAY_SECONDS = 35       # between sends (IP warm-up)
DAYS_BETWEEN_STEPS = 3   # gap between sequence emails
```

## Template format
Plain text files in `templates/` dir:
```
Subject: Line with {nome} placeholder

Body with {nome}, {azienda}, {settore} placeholders.
```

## Lead CSV format
```csv
name,company,sector,email,sequence,notes
```
`sequence` maps to `SEQUENCES` dict in script (e.g., "outreach" = 3-step, "ristorazione" = 1-step).
