---
name: stack-manager
description: Manage the AI bot stack — deployment, architecture, business plan, bot inventory, and inter-bot coordination on the VPS.
triggers:
  - "bot stack"
  - "hermes bots"
  - "deploy bot"
  - "bot status"
  - "contabile"
  - "designbro"
  - "lawrenzo"
  - "wannabe"
  - "media manager"
  - "business plan"
  - "inter-bot"
  - "bot communication"
  - "fleet"
---

# AI Bot Stack Manager

## Overview

The owner runs a multi-bot AI stack on a VPS (11 GiB RAM, 6 cores). The business sells customized Hermes bots per industry vertical.

## Bot Inventory

### ✅ Active Bots

1. **ContAIbile** — Accounting + Crypto
   - Path: `<USER_HOME>/ai-stack/contabile/`
   - Port: 8090
   - Status: Operational (gold standard for code quality)
   - Service: `hermes --profile contabile gateway run`
   - Features: double-entry bookkeeping, IVA, F24, FIFO crypto, Quadro RT, web dashboard

2. **LAWrenzo** — Legal Docs AI
   - Path: `<USER_HOME>/ai-stack/lawrenzo-v2/` (v2 restructure)
   - Port: 8091 API, 8086 web
   - Status: Operational
   - Service: `hermes --profile lawrenzo gateway run`
   - 36 doc types, validator score ≥ 70, PDF via WeasyPrint

3. **Wannabe Bot** — Media Manager
   - Path: `<USER_HOME>/ai-stack/wannabe-bot/`
   - Port: 8093
   - Status: Deployed
   - Service: `hermes --profile wannabe gateway run`
   - Personality: Gary Vaynerchuk + David Ogilvy + Seth Godin
   - 13 tools, 4 cron jobs

4. **DesignBro** — Graphic Design Assistant
   - Path: `<USER_HOME>/ai-stack/designbro/`
   - Port: 8094
   - Status: Deployed
   - Service: `hermes --profile designbro gateway run`
   - Token: <TOKEN_PLACEHOLDER>
   - Personality: Fortunato Depero + Bruno Munari + Milton Glaser
   - Inter-bot: receives from Wannabe (P04), sends to GROOT (P06) and Wannabe (P12)

5. **GROOT** — Vineria Manager
   - Path: `<USER_HOME>/ai-stack/groot/`
   - Status: Deployed
   - Service: `hermes --profile groot gateway run`
   - Personality: Bourdain + Cannavacciuolo + Bottura
   - CLI: `cd <USER_HOME>/ai-stack/groot && source venv/bin/activate && python3 cli.py <tool>` (venv required)
   - Inter-bot: sends to Wannabe (P03), ContAIbile (P08), receives from DesignBro (P06)
   - Limitations: no sales tracking, no events calendar, no wine inventory

6. **El Froggo** — Crypto Trading Agent (Virtuals Protocol)
   - Status: ✅ Active (token regenerated)
   - Profile: `el-froggo`
   - Username: @GRIBBITO_BOT
   - MCP: EVM (Base chain) + RootEdge (DEX search, trending, news, Fear & Greed, Hyperliquid)
   - Inter-bot: sends to ContAIbile (P01), Wannabe (P05), LAWrenzo (P09)

7. **Ducato** — Finance Expert AI
   - Path: `<USER_HOME>/ai-stack/ducato/`
   - Status: ✅ Operational (running as Hermes gateway)
   - Service: `hermes --profile ducato gateway run`
   - Personality: Warren Buffett + Nassim Taleb + Rocco Casalino
   - Focus: investimenti personali, financial planning, corporate finance, analisi macro
   - GOAL.md: ✅ (created)

### Profile Status

All bots run as Hermes gateway processes (`hermes --profile <name> gateway run`):
- **gribbito**: active (main agent, orchestrator)
- **contabile**: active (accountant)
- **lawrenzo**: active (lawyer)
- **wannabe**: active (media manager)
- **groot**: active (vineria manager)
- **designbro**: active (graphic designer)
- **ducato**: active (finance expert)
- **el-froggo**: active (trader)

**Pitfall**: Old standalone systemd services are **dead/unused**. All bots now run as Hermes gateway processes. To check if a bot is alive, use `pgrep -f "hermes.*--profile <name> gateway"` — NOT `systemctl is-active`.

## Architecture Standard (ContAIbile pattern)

Every bot MUST follow this structure:

```
bot-name/
├── main.py              # FastAPI + Telegram webhook + web dashboard
├── core/
│   ├── brain.py         # Conversational brain (tool-calling loop)
│   ├── config.py        # Config from .env + YAML
│   ├── handlers.py      # Telegram handlers
│   ├── tools.py         # Tool definitions (OpenAI function calling format)
│   ├── scheduler.py     # Scheduled tasks
│   └── [domain]_tools.py
├── storage/
│   └── db.py            # SQLite
├── tests/
├── web/templates/       # Jinja2 dashboard
├── init_db.py           # Schema + seed
├── .env.example
└── requirements.txt
```

**Key rules:**
- FastAPI webhook (NOT polling)
- SQLite (NOT Postgres/MongoDB)
- OpenAI function calling format for tools
- mimo-v2.5-pro via OpenGateway
- Accept-Encoding: identity (fix gzip issue)
- Tests after EVERY modification

## Marketing Strategy (zero budget)

Key channels: WhatsApp demo, SEO italiano, LinkedIn outreach, associazioni categoria (FIPE, ODCEC).
Marketing materials location: `<SHARED_DIR>/marketing/`
LinkedIn API integration: `<SHARED_DIR>/linkedin/`
Target anno 1: 50-100 clienti, MRR €2.000-5.000.

## LLM Stack

- Primary: mimo-v2.5-pro via OpenGateway
- Fallback: Venice AI + OpenRouter
- Max budget: $4 OpenRouter
- OpenGateway gzip pitfall: body says gzip but isn't — use `Accept-Encoding: identity`

## Logo & Brand Assets

- Brand identity: `<SHARED_DIR>/marketing/brand/brand-identity.md`
- Content calendar: `<SHARED_DIR>/marketing/brand/content-calendar.md`
- Bot PFP source: `<SHARED_DIR>/marketing/bot-profiles/pixel/pfp-*.png`
- HermesBro site: hermesbro.cloud (root: <NGINX_ROOT_DIR>/)

## Inter-Bot Communication Architecture

All bots are Hermes profiles in the same Telegram supergroup, each with its own topic/thread. Cross-bot messaging = send message to another bot's topic.

**Group chat**: "HERMES HUB", chat_id=`<GROUP_CHAT_ID>` (PRIMARY for inter-bot comms).

**File-Based Bus**: This is the ONLY reliable inter-bot communication mechanism on Telegram. Direct group messaging between bots does NOT work.

Architecture:
```
Bot A runs: bus-send.py send <from> <to> "<msg>" <type>
  → writes JSON to <SHARED_DIR>/bus/inbox/<to>/<id>.json

Cron (gribbito, every 5 min): bus-dispatch.py
  → reads all inboxes
  → sends formatted messages to HERMES HUB group via Telegram API
  → marks as read, moves to processed/
```

Scripts:
- `bus-send.py` — writes JSON messages to bot-specific inbox dirs
- `bus-dispatch.py` — reads inboxes, forwards to HERMES HUB group, moves to processed
- `bus-check.py` — reads inbox for a specific bot (for cron jobs)
- All scripts: `<SHARED_DIR>/scripts/`

Cron: gribbito every 5 min runs `bus-dispatch.py` (no_agent=True)
Inbox: `<SHARED_DIR>/bus/inbox/{bot-name}/`
Processed: `<SHARED_DIR>/bus/processed/`
Message types: info, event, deadline, trade, design, regulation, sales, alert

**12 paired connections** + **5 triple chains** + **3 system-wide** (daily digest, error watchdog, pipeline). Full details in `references/inter-bot-architecture.md`.

## Profile Creation Checklist

When creating a new Hermes profile (e.g., Ducato):

```bash
# 1. Create profile
hermes profile create <name>

# 2. Write SOUL.md (personality + competencies + limits)

# 3. Copy config from existing profile
cp <PROFILES_DIR>/contabile/config.yaml <PROFILES_DIR>/<name>/config.yaml

# 4. Copy .env (API keys)
cp <PROFILES_DIR>/contabile/.env <PROFILES_DIR>/<name>/.env

# 5. Copy unified channel_directory.json
cp <PROFILES_DIR>/gribbito/channel_directory.json <PROFILES_DIR>/<name>/channel_directory.json

# 6. Create ai-stack directory
mkdir -p <USER_HOME>/ai-stack/<name>

# 7. Update memory (bot lineup, profile list)
memory(action="replace", content="...")
```
