# Outreach Automation Script

**Script**: `<HERMES_ROOT>/shared/linkedin/outreach.py`
**Language**: Python 3 (stdlib only, no deps)

## Commands

```bash
python3 <HERMES_ROOT>/shared/linkedin/outreach.py status    # Campaign stats
python3 <HERMES_ROOT>/shared/linkedin/outreach.py batch     # Next 20 targets with auto-generated messages
python3 <HERMES_ROOT>/shared/linkedin/outreach.py batch 10  # Custom batch size
python3 <HERMES_ROOT>/shared/linkedin/outreach.py add /path/to/targets.csv
python3 <HERMES_ROOT>/shared/linkedin/outreach.py template ristorante  # Show template for sector
```

## Target CSV Format

File: `<HERMES_ROOT>/shared/marketing/outreach/targets.csv`

```csv
name,company,sector,linkedin_url,email,notes
Marco Rossi,Trattoria da Marco,ristorante,,,"Pizzeria Torino centro, 40 coperti"
```

Sectors: ristorante, studio, negozio, ecommerce, generico

## Auto-Generated Messages

For each target, the script generates TWO messages based on sector:

**Connection Request** (<300 chars, LinkedIn limit):
- ristorante → GROOT pitch ([REDACTED — dati personali rimossi], prenotazioni)
- studio → LAWrenzo/ContAIbile pitch (contratti, fatture)
- negozio → Wannabe pitch (social media)
- ecommerce → Team AI pitch (supporto 24/7)
- generico → HermesBro intro (6 bot, prova gratis)

**DM After Acceptance** (longer, with CTA):
- Problem statement for the sector
- Bot solution
- CTA: demo gratuita 20 min su Telegram

## Tracker CSV

File: `<HERMES_ROOT>/shared/marketing/outreach/campaign-tracker.csv`

Auto-created with columns: date, channel, contact_name, company, sector, status, message_sent, notes

Statuses: sent → connected → call → trial → paying

## Daily Limits

- Connection requests: 20/day (LinkedIn safe limit)
- DMs after acceptance: unlimited (but pace naturally)

## Integration with LinkedIn

Messages are TEXT ONLY — the script prints them for copy-paste. [REDACTED — dati personali rimossi] sends manually.
Future: integrate with linkedin.py for automated connection requests (requires additional API scopes).
