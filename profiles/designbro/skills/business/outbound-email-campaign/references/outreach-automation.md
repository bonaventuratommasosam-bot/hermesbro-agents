# Outreach Automation Pipeline — HermesBro

## Production System (live since 2026-06-06)

### Architecture
```
leads-active.csv → outreach-engine.py → Postfix → OpenDKIM → Recipient MX
                      ↓                                    ↓
               sent-tracker.json                    DKIM signed
                      ↓
              Report → Telegram
```

### Key Files
| File | Purpose |
|------|---------|
| `<HERMES_ROOT>/shared/marketing/email/outreach-engine.py` | Main orchestrator |
| `<HERMES_ROOT>/shared/marketing/email/templates/*.txt` | Email templates per sequence step |
| `<HERMES_ROOT>/shared/marketing/email/sent-tracker.json` | Per-lead tracking (steps done, timestamps) |
| `<HERMES_ROOT>/shared/marketing/email/last-report.txt` | Last run report |
| `<HERMES_ROOT>/shared/marketing/outreach/leads-active.csv` | Active lead list |

### How It Works
1. Reads `leads-active.csv` (columns: name, company, sector, email, sequence, notes)
2. For each lead, determines next action based on sequence and timing
3. Sequences: `outreach` (3-step, 3-day gaps), `ristorazione` (1-step), `commercialisti` (1-step)
4. Sends batch of 10 emails with 35-second delays between sends
5. Updates `sent-tracker.json` with what was sent
6. Outputs report (delivered to Telegram via cron)

### Cron Job
- **Job ID:** `105585124a36`
- **Schedule:** `0 10 * * *` (daily at 10:00)
- **Deliver:** telegram:<ADMIN_CHAT_ID>:32638

### Commands
```bash
# Dry run (simulate, no sends)
python3 outreach-engine.py --dry-run

# Check status
python3 outreach-engine.py --status

# Add new leads from CSV
python3 outreach-engine.py --add-leads new-leads.csv

# Run manually (sends real emails)
python3 outreach-engine.py
```

### Template Format
Plain text files in `<HERMES_ROOT>/shared/marketing/email/templates/`:
```
Subject: Line with {nome} placeholder

Body text with {nome}, {azienda}, {settore} placeholders.
```

### Adding New Sequences
Edit `SEQUENCES` dict in `outreach-engine.py`:
```python
SEQUENCES = {
    "outreach": ["outreach-1.txt", "outreach-2.txt", "outreach-3.txt"],
    "ristorazione": ["ristorazione-1.txt"],
    "commercialisti": ["commercialisti-1.txt"],
    "new-seq": ["new-1.txt", "new-2.txt"],
}
```
Then set `sequence` column in CSV to the sequence name.

### Verified Deliverability (2026-06-06)
- FROM: `hermesbro10@hermesbro.cloud`
- SPF: `v=spf1 ip4:194.146.12.219 include:_spf.aruba.it ~all`
- DKIM: signing via OpenDKIM on port 8891
- Gmail: `status=sent` confirmed
- Rate: 35s between sends, 10 per batch
