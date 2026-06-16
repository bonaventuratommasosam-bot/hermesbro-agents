# OpenAlice Integration Plan

## Overview

OpenAlice (https://github.com/TraderAlice/OpenAlice) is an AI trading agent covering equities, crypto, commodities, forex, and macro. 4.5k+ stars, AGPL-3.0 license, active development (938 commits, 24 tags).

Integration target: **Ducato** — the finance expert bot in the Hermes Bots lineup.

## Key Features

### Trading
- **Unified Trading Account (UTA)** — multiple brokers (CCXT, Alpaca, IB) in one workspace
- **Trading-as-Git** — stage orders, commit with message, push to execute. Full audit trail
- **Guard pipeline** — pre-execution safety checks (max position size, cooldown, symbol whitelist)
- **Account snapshots** — periodic state capture with equity curve visualization

### Research & Analysis
- **Market data** — equity, crypto, commodity, currency, macro via OpenBB engine
- **Fundamental research** — company profiles, financial statements, ratios, analyst estimates
- **News** — RSS collection with archive search

### Automation
- **Cron scheduling** — cron expressions, intervals, one-shot timestamps
- **Heartbeat** — periodic timer with active-hours filtering
- **Webhooks** — inbound event triggers (planned)

### Interfaces
- **Web UI** — chat with SSE streaming, portfolio dashboard
- **Workspace** — per-task directory + git repo + persistent terminal session
- **Telegram** — mobile access with trading panel
- **MCP server** — tool exposure for external agents

## Tech Stack

- TypeScript (pnpm monorepo, Turborepo)
- Node.js 22
- React (Vite) frontend
- Docker support (Debian 13)
- Claude Agent SDK + Vercel AI SDK

## Architecture

Two long-lived processes:

1. **Alice Process** — agent runtime, research domain (market data, analysis, news), workspace launcher, user surfaces. Does NOT hold broker credentials.
2. **UTA Service** — broker connections, Trading-as-Git state machine, guards, FX, snapshots. Owns the *doing*.

**Pitfall**: Alice and UTA run on same host today (Docker or pnpm dev). UTA is designed to detach later (run on separate device with broker keys).

## Config Files

All in `data/config/` as JSON with Zod validation:

| File | Purpose |
|------|---------|
| `engine.json` | Trading pairs, tick interval, timeframe |
| `agent.json` | Max steps, evolution mode, tool permissions |
| `ai-provider.json` | Active AI provider, switchable at runtime |
| `accounts.json` | Trading accounts with broker config |
| `connectors.json` | Web/MCP server ports |
| `telegram.json` | Telegram bot credentials |
| `market-data.json` | Data backend, provider API keys |
| `news.json` | RSS feeds, fetch interval |
| `heartbeat.json` | Enable/disable, interval, active hours |

## Integration Steps

### Phase 1: Setup (Week 1)
```bash
cd <USER_HOME>/ai-stack/ducato
git clone https://github.com/TraderAlice/OpenAlice.git openalice
cd openalice
pnpm install
cp .env.example .env  # Configure API keys
pnpm dev  # Test on http://localhost:5173
```

### Phase 2: Hermes Integration (Week 2)
- Create MCP server bridge to expose OpenAlice tools to Hermes
- Register MCP tools in ducato profile config
- Integrate with inter-bot protocol (filesystem bus)
- Create cron jobs: market monitor, daily briefing, alerts

### Phase 3: Trading Live (Week 3-4)
- Configure Guard pipeline (max position size, cooldown)
- Setup CCXT for crypto (Binance/Bybit)
- Setup Alpaca for US equities (paper trading)
- Enable Trading-as-Git for audit trail
- Approval workflow: every trade requires the owner's OK

### Phase 4: Production (Week 5+)
- Docker deployment on VPS
- Backup and recovery plan
- Performance monitoring
- Strategy backtesting

## API Keys Needed

- **AI Provider**: OpenRouter (already configured) or Claude API key
- **Broker (crypto)**: Binance/Bybit API keys
- **Broker (equities)**: Alpaca API keys (free paper trading)
- **Market Data**: OpenBB (free base) or premium providers
- **Telegram**: Bot token (already configured for Ducato)

## Security Considerations

1. **Paper trading first** — test everything with virtual funds
2. **Approval workflow** — every trade requires explicit OK
3. **Position limits** — max 5% portfolio per position
4. **Stop loss** — always configured
5. **Diversification** — no overexposure on single asset
6. **API keys** — never commit, only in `.env` and `data/config/`

## References

- **Repo**: https://github.com/TraderAlice/OpenAlice
- **Docs**: https://openalice.ai/docs
- **DeepWiki**: https://deepwiki.com/TraderAlice/OpenAlice
- **Discord**: https://discord.gg/zf4STmrQd8
- **Full prompt for Frank**: `<PLANS_DIR>/openalice-integration-prompt.md`
