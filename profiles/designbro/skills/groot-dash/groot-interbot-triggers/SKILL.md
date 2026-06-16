---
name: groot-interbot-triggers
description: "Inter-bot trigger system for Groot: bus messaging, cron triggers, data source gaps"
---

# Inter-Bot Trigger System — Groot

## Bus System

Messages pass via filesystem at `<HERMES_ROOT>/shared/bus/`.

**Send a message:**
```bash
python3 <HERMES_ROOT>/shared/scripts/bus-send.py send <from> <to> "<message>" <type>
```
- `from` / `to`: bot names (groot, contabile, wannabe, etc.)
- `type`: info, sales, event, alert, etc.

**Check inbox:**
```bash
python3 <HERMES_ROOT>/shared/scripts/bus-check.py <bot_name>
```

## Cron Triggers

### 1. Daily Sales → ContAIbile
- **Target**: contabile, **Type**: sales
- **Format**: `Vendite giornaliere: {totale EUR}, {dettaglio}. Registra come ricavi.`
- **Gap**: ⚠️ No sales tracking in groot CLI. No `get_vendite`. Magazzino tracks stock, not revenue.

### 2. Upcoming Events → Wannabe
- **Target**: wannabe, **Type**: event
- **Format**: `Evento: {nome} il {data}. Genera copy per social.`
- **Gap**: ⚠️ No event calendar. `get_promemoria` is daily reminders only.

### 3. New Wines → Wannabe
- **Target**: wannabe, **Type**: event
- **Format**: `Nuovo vino: {nome}. Crea post social.`
- **Gap**: ⚠️ BAR category nearly empty (only `Acqua brillante: 1pz`). No wine catalog.

## Data Sources That DO Exist

| Tool | Tracks |
|------|--------|
| `get_magazzino` | Stock levels by category |
| Google Sheets `1opcBpP8ejktG2ApIK8X678FSTKICzSHMRTizAhomiPU` | Same, primary source |
| `get_lista_spesa` | Shopping list |
| `get_promemoria` | Daily reminders (not events) |
| `get_menu` | Dishes and prices |
| `get_report` | Combined overview |

## References
- `references/bus-protocol.md` — Bus message format, directory structure, bot names
- **Detailed analysis**: `software-development/[REDACTED — dati personali rimossi]-stack-manager/references/groot-interbot-triggers.md` — Full worksheet inventory, Google Calendar status, CLI venv requirements, enablement steps

## Pitfalls

1. **Google Sheets auth in cron context**: `google_api.py` may fail auth even when token exists at `~/.hermes/profiles/groot/google_token.json`. Use CLI fallback.
2. **All 3 triggers return [SILENT]** until sales tracking, event calendar, and wine catalog are implemented.
3. **Bus directory structure**: inbox/<bot>/, outbox/, processed/ — messages are JSON files.
4. **⚠️ Bus inbox gap (no auto-polling):** Messages written via `bus-send.py` land in `<HERMES_ROOT>/shared/bus/inbox/<bot>/` but NO bot has a cron job to read them. Groot's triggers write messages that sit unread. Fix: create a polling cron for each bot that receives bus messages. See `shared-knowledge-protocol/references/bus-inbox-polling.md` for setup template.
