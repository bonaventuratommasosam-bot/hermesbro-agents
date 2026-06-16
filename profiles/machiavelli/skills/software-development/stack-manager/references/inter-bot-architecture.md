# Inter-Bot Communication Architecture

## Overview

All 7 bots are Hermes Agent profiles sharing one Telegram supergroup. Each has a topic/thread. Cross-bot messaging = `send_message` to another bot's topic.

## Registry

File: `<SHARED_DIR>/registry/bots.json`

| Bot | Profile | Thread ID | Telegram Username | Role |
|-----|---------|-----------|-------------------|------|
| gribbito | gribbito | DM (no thread) | @HermesRIbbitBot | Orchestrator |
| contabile | contabile | <THREAD_ID_1> | @COntabilBOT56BOT | Accountant |
| lawrenzo | lawrenzo | <THREAD_ID_2> | @LAWrenz0bot | Lawyer |
| groot | groot | <THREAD_ID_3> | @<REDACTED_BOT> | Restaurant |
| wannabe | wannabe | DM (no thread) | @Wwwannabeee_bot | Media |
| designbro | designbro | <THREAD_ID_4> | @elfroggoRATATOUILLEbot | Designer |
| el-froggo | el-froggo | <THREAD_ID_5> | @GRIBBITO_BOT | Trader |

**HERMES HUB Group** (PRIMARY): chat_id=`<GROUP_CHAT_ID>`. All bots communicate here directly.

**Telegram Group for Bot-to-Bot**: `<GROUP_INVITE_LINK>` (private). Bots must be added manually by admin.

## Message Format

Always prefix: `[FROM:BOT_NAME] message body`

Examples:
```
[FROM:CONTABILE] F24 in scadenza 30/06: €2,450 IRPEF. Prepara docs.
[FROM:EL-FROGGO] Trade chiuso: ETH +€120 (entry €2800, exit €2920). Registra P&L.
[FROM:GROOT] Evento: Degustazione Barolo sabato 15/06. Genera copy + grafica.
[FROM:WANNABE] Brief per DesignBro: post Instagram "Menu Estate 2026", palette calda.
[FROM:DESIGNBRO] Grafica pronta: <SHARED_DIR>/assets/menu-estate.png. Pubblica.
[FROM:LAWRENZO] Nuova normativa: Decreto Lavoro 2026, scadenze aggiornate CU e 770.
```

## Sending Methods

### PRIMARY: Group Chat (HERMES HUB)
All bots are in the same Telegram group. Chat ID: `<GROUP_CHAT_ID>`.
```python
send_message(target="telegram:<GROUP_CHAT_ID>", message="[FROM:GROOT] Vendite oggi €1,250")
```

### FALLBACK: Topic-based (legacy, DM supergroup)
Individual topic IDs per bot (contabile=<THREAD_ID_1>, lawrenzo=<THREAD_ID_2>, etc.).
```python
send_message(target="telegram:<OWNER_CHAT_ID>:<THREAD_ID_1>", message="[FROM:GROOT] Vendite oggi €1,250")
```

### CLI method
```bash
HERMES_PROFILE=groot /usr/local/bin/hermes send --to telegram:<GROUP_CHAT_ID> "[FROM:GROOT] Vendite oggi €1,250"
```

## 12 Paired Connections

| ID | From | To | Trigger | Action |
|----|------|----|---------|--------|
| P01 | el-froggo | contabile | Trade closed | Register P&L |
| P02 | contabile | lawrenzo | Tax deadline | Prepare compliance docs |
| P03 | groot | wannabe | New event/wine | Generate social post |
| P04 | wannabe | designbro | Post needs image | Create graphic |
| P05 | el-froggo | wannabe | Trade >€50 PnL | Create crypto content |
| P06 | designbro | groot | Design ready | Review with owner |
| P07 | lawrenzo | contabile | New regulation | Update tax rules |
| P08 | groot | contabile | Daily sales | Register as revenue |
| P09 | el-froggo | lawrenzo | Trade >€100 | Check crypto compliance |
| P10 | lawrenzo | wannabe | New PMI law | Create info post |
| P11 | wannabe | contabile | Campaign launched | Register marketing cost |
| P12 | designbro | wannabe | Design completed | Schedule publication |

## 5 Triple Chains

| ID | Chain | Description |
|----|-------|-------------|
| T01 | el-froggo → contabile → lawrenzo | Trade → P&L → compliance |
| T02 | groot → wannabe → designbro | New wine → copy → graphic |
| T03 | contabile → lawrenzo → wannabe | Deadline → docs → reminder |
| T04 | el-froggo → wannabe → designbro | Crypto → thread → infographic |
| T05 | groot → contabile → lawrenzo | Event → invoice → permits |

In triple chains, each bot does its step and forwards to the next. The initiating bot only triggers step 1.

## 3 System-Wide

| ID | Name | Description |
|----|------|-------------|
| S01 | Daily Digest | gribbito collects from all bots → summary to the owner at 20:00 |
| S02 | Error Watchdog | Script checks service health every 15min, silent when OK |
| S03 | Pipeline Completa | GROOT event → full chain through all relevant bots |

## Cron Jobs

### System-wide (on gribbito)
- `fleet-monitor` (every 30m) — health check + event routing
- `error-watchdog` (every 15m, no_agent) — `<SCRIPTS_DIR>/error-watchdog.sh`
- `daily-digest` (20:00 daily) — comprehensive summary

### Per-bot triggers
- `groot-sales-event-trigger` (19:00 daily) — sales → ContAIbile, events → Wannabe
- `lawrenzo-regulation-check` (Monday 10:00) — new regs → ContAIbile, PMI laws → Wannabe
- `wannabe-designbro-pipeline` (10:00 daily) — pending posts → DesignBro briefs
- `designbro-sync-check` (11:00 daily) — completed designs → notify originators

## Skill Files Per Bot

Each bot has 3 files in `skills/inter-bot/`:
1. `protocol.md` — Shared protocol (copied from `<SHARED_DIR>/skills/inter-bot-protocol.md`)
2. `outgoing-triggers.md` — When/how to notify other bots
3. `incoming-handler.md` — How to process messages from other bots

Plus each GOAL.md has a `## 🔗 Inter-Bot Connections` section.

## File-Based Bus (Alternative)

The file-based bus provides reliable async messaging when direct group communication fails (e.g., Telegram Privacy Mode issues). See `references/inter-bot-bus.md` for full details.

**When to use file-based bus vs direct group:**
- **File-based bus**: batch messages, non-urgent, scheduled triggers, when bots can't see each other
- **Direct group**: urgent, real-time, human-visible notifications
- **Both**: always send to group for the owner's visibility, file bus for reliability

## Pitfalls

- NEVER send a message to yourself (same bot) — Telegram ignores it
- Always include `[FROM:SENDER]` prefix
- Wannabe has no thread_id — send to `telegram:<OWNER_CHAT_ID>` (DM)
- When a bot token is rejected (InvalidToken/404), gateway retries every 5min then pauses. Fix: new token from BotFather → update `.env` → `systemctl restart hermes-<profile>.service`
- When adding new connections, update ALL files on BOTH bots (skills + GOAL.md)
- GOAL.md files start with `# Bot Name — Goal` (NOT `---` YAML frontmatter). Use `write_file` to append the `## 🔗 Inter-Bot Connections` section, NOT `patch` with `---` pattern — the fuzzy matcher won't find it.
- `bot-send.sh` reads from registry — update `bots.json` if topic IDs change
- When joining bots to a Telegram group, use `importChatInviteLink` API (not `joinChat` — that method doesn't exist in python-telegram-bot). Bots may need to be added manually by group admin if API returns 404.
- Some bot usernames are misleading: @elfroggoRATATOUILLEbot is DesignBro (old Ratatouille bot repurposed), @GRIBBITO_BOT is El Froggo. Always verify with `getMe`.
- **CRITICAL — Telegram Privacy Mode**: By default, bots in Telegram groups can ONLY see: (1) messages starting with `/` (commands), (2) replies to their messages, (3) messages that @mention them. Regular text messages are INVISIBLE to them. To fix: @BotFather → `/setprivacy` → select bot → `Disable`. Without this, inter-bot communication in a group DOES NOT WORK.
- **Group chat ID discovery**: After joining bots to a group via `importChatInviteLink`, the chat_id is NOT immediately in the gateway's channel directory. A message must be sent in the group for the gateway to register it. Ask the owner to send a test message, then grep `gateway.log` for the new chat_id.
- **Terminal secret redaction breaks inline code**: When writing Python/shell inline that reads tokens from `.env`, the redaction engine mangles string literals containing token patterns. Workaround: write scripts to files first, then execute. Or use `bash -c "source /path/.env; command"`.
