# Bus Message Protocol

## Directory Structure
```
<HERMES_ROOT>/shared/bus/
├── inbox/<bot_name>/    # Messages waiting to be read
├── outbox/              # Outgoing queue
└── processed/           # Read messages archived here
```

## Message Format (JSON)
```json
{
  "id": "groot-1717171717000",
  "from": "groot",
  "to": "contabile",
  "type": "sales",
  "message": "Vendite giornaliere: 450 EUR, 12 coperti.",
  "timestamp": "2026-05-31T19:00:00Z",
  "read": false
}
```

## Known Bot Names
- `groot` — Vineria manager (this bot)
- `contabile` — Accounting/bookkeeping
- `wannabe` — Social media / marketing

## Type Values
- `sales` — Revenue data
- `event` — Upcoming events, new products
- `info` — General information
- `alert` — Urgent notifications

## Checking for Responses
```bash
python3 <HERMES_ROOT>/shared/scripts/bus-check.py groot
```
Returns unread messages in groot's inbox, or empty if none.
