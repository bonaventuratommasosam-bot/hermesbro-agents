# HermesBro Agents

**Open-source AI agents for business.** Pre-trained, customizable, ready to deploy.

## What is this?

9 specialized AI agents built on [Hermes Agent](https://hermes-agent.nousresearch.com). Each agent is a complete Hermes profile with identity (SOUL), mission (GOAL), tools, scripts, and documentation.

Use them as-is, customize them for your clients, or fork them for your own business.

## The Fleet

| Agent | Role | Best for |
|-------|------|----------|
| **Groot** | Restaurant brigade | Inventory, shopping lists, food cost, team coordination |
| **Contabile** | Accounting PMI | Transactions, VAT tracking, deadlines, invoices |
| **Wannabe** | R&D Lab | Experiments, skill testing, feature proposals |
| **DesignBro** | Visual identity | Logos, palettes, typography, brand kits |
| **Ducato** | Finance | Portfolio analysis, break-even, runway scenarios |
| **El-froggo** | Fleet lead | Founder coordination, pulse reports, escalation |
| **Lawrenzo** | Legal | Contracts, GDPR, regulatory compliance |
| **Sentinel** | Security audit | Smart contract audit, VPS security scoring |
| **Machiavelli** | Orchestrator | Multi-agent workflows, DAG dispatch, briefings |

## Structure

```
hermesbro-agents/
├── profiles/
│   ├── groot/          # Restaurant brigade bot
│   │   ├── SOUL.md     # Identity & personality
│   │   ├── GOAL.md     # Mission, flows, triggers
│   │   ├── README.md   # Agent-specific docs
│   │   └── skills/     # Skills & scripts
│   ├── contabile/      # Accounting PMI bot
│   ├── wannabe/        # R&D lab bot
│   ├── designbro/      # Visual identity bot
│   ├── ducato/         # Finance analysis bot
│   ├── el-froggo/      # Fleet lead bot
│   ├── lawrenzo/       # Legal bot
│   ├── sentinel/       # Security audit bot
│   └── machiavelli/    # Orchestrator bot
├── docs/               # General documentation
├── scripts/            # Shared utilities
└── LICENSE
```

## Quick Start

Each agent requires:

1. **Hermes Agent** installed (see [docs](https://hermes-agent.nousresearch.com/docs))
2. A Telegram bot token (from [@BotFather](https://t.me/BotFather))
3. An LLM API key (OpenRouter, Google AI, etc.)
4. Profile-specific config (documented in each agent's README)

```bash
# 1. Clone the repo
git clone https://github.com/bonaventuratommasosam-bot/hermesbro-agents.git
cd hermesbro-agents/profiles/groot

# 2. Run the setup wizard
bash setup_wizard.sh
# or use the automated deploy:
python3 configure_brigata.py

# 3. Start the agent
hermes -p groot serve
```

## Business Model

- **Code**: MIT License — free, open, forkable
- **Service**: We sell pre-trained, customized bots
  - Setup & configuration per client
  - Custom training for specific use cases
  - Ongoing support & maintenance
- **Contact**: [hermesbro.cloud](https://hermesbro.cloud)

## Requirements

- Python 3.10+
- Hermes Agent ([install guide](https://hermes-agent.nousresearch.com/docs/getting-started/installation))
- Telegram Bot API token
- LLM provider key (Gemini free tier works for most agents)

## License

MIT — see [LICENSE](LICENSE)

## Built with

- [Hermes Agent](https://hermes-agent.nousresearch.com) — open-source AI agent framework
- Telegram Bot API
- DeepSeek V4 Pro — core inference engine (via OpenRouter)
