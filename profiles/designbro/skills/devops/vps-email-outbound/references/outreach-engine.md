# Outreach Engine — Production Pipeline

## Overview
Sequence-based email outreach engine with per-lead tracking, rate limiting, and cron automation.

## Key Files
| File | Purpose |
|------|---------|
| `<HERMES_ROOT>/shared/marketing/email/outreach-engine.py` | Main orchestrator |
| `<HERMES_ROOT>/shared/marketing/email/templates/*.txt` | Email templates per sequence step |
| `<HERMES_ROOT>/shared/marketing/email/sent-tracker.json` | Per-lead tracking |
| `<HERMES_ROOT>/shared/marketing/outreach/leads-active.csv` | Active lead list |

## Sequences
- `outreach`: 3-step (day 0, +3, +6) — commercialisti/avvocati/coworking
- `ristorazione`: 1-step — ristoranti
- `commercialisti`: 1-step — studio commercialista

## Template Format
```
Subject: Line with {nome} placeholder

Body with {nome}, {azienda}, {settore} placeholders.
```

## Commands
```bash
python3 outreach-engine.py --dry-run    # Simulate
python3 outreach-engine.py --status     # Show status
python3 outreach-engine.py --add-leads FILE  # Add leads
python3 outreach-engine.py              # Send batch
```

## Cron Job
- Job ID: `105585124a36`
- Schedule: `0 10 * * *` (daily 10:00)
- Script must be in `~/.hermes/scripts/outreach-engine.py` (copy, not symlink)
- Deliver: `telegram:<ADMIN_CHAT_ID>:32638`
