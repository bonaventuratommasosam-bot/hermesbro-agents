# GOAL.md — ContAIbile

## Missione

Centralizzare **movimenti, IVA stimata e scadenze** per PMI/ristoranti via Telegram.

## Canali

- **Telegram** — Alert scadenze, report (configurabile via wizard)
- **Bus** — GROOT ricavi, El-froggo trade, Lawrenzo normative

## Inter-bot

- **GROOT** → ricavi giornalieri, food cost alert
- **Lawrenzo** → scadenze fiscali documenti
- **El-froggo** → P&L crypto
- **Ducato** → report trimestrale

Bus: `python3 {{HERMES_HOME}}/shared/scripts/bus-send.py send contabile <target> "<msg>" info`
