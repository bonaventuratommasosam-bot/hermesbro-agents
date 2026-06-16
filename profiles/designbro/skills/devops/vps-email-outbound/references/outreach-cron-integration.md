# Outreach Engine — Cron Integration

The outreach engine runs as a `no_agent=True` cron job.

## Cron setup

```python
cronjob(
    action='create',
    name='hermesbro-outreach',
    schedule='0 10 * * *',       # daily at 10:00
    script='outreach-engine.py', # bare filename in ~/.hermes/scripts/
    no_agent=True,
    deliver='telegram:CHAT_ID:THREAD_ID'
)
```

**Critical:** The script must be in `~/.hermes/scripts/outreach-engine.py` (not a symlink, not an absolute path).

## Sequence logic

The engine tracks each lead's progress through its sequence:
- `sent-tracker.json` stores per-lead state (sequence name, steps done, last sent date)
- Each run: finds leads where `next_step < len(sequence_templates)` AND `days_since_last_send >= DAYS_BETWEEN_STEPS`
- Sends up to `BATCH_SIZE` emails with `DELAY_SECONDS` between each
- Reports results to delivery target (Telegram)

## Adding leads

```bash
# Prepare CSV with columns: name,company,sector,email,sequence,notes
# sequence maps to SEQUENCES dict (e.g., "outreach" = 3-step, "ristorazione" = 1-step)

python3 outreach-engine.py --add-leads new-leads.csv
```

## Template format

Plain `.txt` files in `templates/` dir:
```
Subject: {nome}, e se avessi un team...

Body with {nome}, {azienda}, {settore} placeholders.
```

## Monitoring

- `--status` shows campaign state
- `--dry-run` simulates without sending
- Cron report arrives on Telegram after each run
- Check `/var/log/mail.log` for delivery status
