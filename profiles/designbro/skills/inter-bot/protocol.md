---
name: inter-bot-protocol
description: "Inter-bot communication protocol for Hermes fleet. Send/receive messages between bots."
triggers:
  - "send to another bot"
  - "notify other bot"
  - "inter-bot message"
  - "bot-to-bot"
  - "fleet communication"
tools:
  - terminal
  - read_file
  - send_message
---

# Inter-Bot Communication Protocol

## Architecture

All bots are Hermes profiles sharing one Telegram supergroup (chat <ADMIN_CHAT_ID>). Each bot has its own topic/thread. Cross-bot messaging = send message to another bot's topic.

## Bot Registry

Registry file: `<HERMES_ROOT>/shared/registry/bots.json`

| Bot | Profile | Thread ID | Role |
|-----|---------|-----------|------|
| gribbito | gribbito | (DM) | Orchestrator |
| contabile | contabile | 31680 | Accountant |
| lawrenzo | lawrenzo | 31683 | Lawyer |
| groot | groot | 31674 | Restaurant |
| wannabe | wannabe | (check dir) | Media |
| designbro | designbro | 31677 | Designer |
| el-froggo | el-froggo | 31671 | Trader |

## Sending a Message to Another Bot

### Method 1: send_message tool (preferred)
```
send_message(target="telegram:<ADMIN_CHAT_ID>:31680", message="[FROM:GROOT] Nuovo evento sabato: Degustazione Barolo. Genera post social.")
```

### Method 2: hermes send CLI
```bash
HERMES_PROFILE=gribbito <HERMES_BIN> send --to telegram:<ADMIN_CHAT_ID>:31680 "message"
```

### Method 3: bot-send.sh helper
```bash
<HERMES_ROOT>/shared/scripts/bot-send.sh gribbito contabile "F24 scade venerdì"
```

## Message Format Convention

Always prefix inter-bot messages with `[FROM:<SENDER>]` so the receiving bot can identify the source:

```
[FROM:CONTABILE] F24 in scadenza il 30/06: €2,450 IRPEF. Preparare F24 e documentazione.
[FROM:EL-FROGGO] Trade chiuso: ETH +€120 (entry €2800, exit €2920). Registra P&L.
[FROM:GROOT] Evento: Degustazione Barolo sabato 15/06. Genera copy + grafica.
[FROM:WANNABE] Brief per DesignBro: post Instagram "Menu Estate 2026", palette calda, foto piatto.
[FROM:DESIGNBRO] Grafica pronta: <HERMES_ROOT>/shared/assets/menu-estate-2026.png. Pubblica.
[FROM:LAWRENZO] Nuova normativa: Decreto Lavoro 2026, scadenze aggiornate per CU e 770.
```

## Receiving Messages from Other Bots

When you receive a message starting with `[FROM:<BOT>]`:
1. Identify the sender
2. Parse the request/data
3. Execute the required action
4. If the action triggers another connection, forward to the next bot

## Connection Map (who sends what to whom)

See `<HERMES_ROOT>/shared/registry/bots.json` for full connection map.

### Paired Connections
- **P01** el-froggo → contabile: Trade closed → register P&L
- **P02** contabile → lawrenzo: Tax deadline → prepare compliance docs
- **P03** groot → wannabe: New event/wine → generate social post
- **P04** wannabe → designbro: Post needs image → create graphic
- **P05** el-froggo → wannabe: Significant trade → create content
- **P06** designbro → groot: Design ready → show to owner
- **P07** lawrenzo → contabile: New regulation → update tax rules
- **P08** groot → contabile: Daily sales → generate invoices
- **P09** el-froggo → lawrenzo: Large trade → check compliance
- **P10** lawrenzo → wannabe: New PMI law → create informational post
- **P11** wannabe → contabile: Campaign launched → register marketing cost
- **P12** designbro → wannabe: Design completed → schedule publication

### Triple Chains
- **T01** el-froggo → contabile → lawrenzo: Trade → register → compliance
- **T02** groot → wannabe → designbro: New wine → copy → graphic
- **T03** contabile → lawrenzo → wannabe: Deadline → docs → reminder
- **T04** el-froggo → wannabe → designbro: Crypto → thread → infographic
- **T05** groot → contabile → lawrenzo: Event → invoice → permits

## Pitfalls
- NEVER send a message to yourself (same bot) — Telegram ignores it
- Always include [FROM:SENDER] prefix — otherwise the receiving bot won't know it's inter-bot
- Keep messages concise — they appear as Telegram messages
- Use Italian — all bots communicate in Italian with [REDACTED — dati personali rimossi]
