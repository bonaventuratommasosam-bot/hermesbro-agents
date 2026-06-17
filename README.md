# HermesBro Agents

**9 open-source AI agents for business.** Native Hermes Profile Distributions — one command install.

## What is this?

Specialized AI agents built on [Hermes Agent](https://hermes-agent.nousresearch.com). Each agent is a complete **Profile Distribution** — SOUL, GOAL, skills, cron jobs, domain config — installable with a single command.

Use them as-is, customize them for clients, or fork them for your own business.

## Install (native Hermes)

```bash
hermes profile install github.com/bonaventuratommasosam-bot/hermesbro-<agent> --alias
```

Hermes handles everything: clone, manifest check, env var detection, .env.EXAMPLE generation, cron preview. Then copy `.env.EXAMPLE` to `.env`, fill in your keys, and start:

```bash
hermes -p <agent> gateway start
```

## The Fleet

| Agent | Install | Role |
|-------|---------|------|
| **Groot** | `github.com/bonaventuratommasosam-bot/hermesbro-groot` | Restaurant brigade: inventory, shopping list, food cost |
| **Contabile** | `github.com/bonaventuratommasosam-bot/hermesbro-contabile` | Accounting: revenues, costs, margins, VAT tracking |
| **Wannabe** | `github.com/bonaventuratommasosam-bot/hermesbro-wannabe` | Content & media: posts, threads, campaigns |
| **DesignBro** | `github.com/bonaventuratommasosam-bot/hermesbro-designbro` | Visual identity: logos, palettes, brand kits |
| **Ducato** | `github.com/bonaventuratommasosam-bot/hermesbro-ducato` | Finance: portfolio analysis, crypto, stock screening |
| **El-froggo** | `github.com/bonaventuratommasosam-bot/hermesbro-el-froggo` | Fleet coordination: routing, priorities, pulse reports |
| **Lawrenzo** | `github.com/bonaventuratommasosam-bot/hermesbro-lawrenzo` | Legal: contracts, HACCP, GDPR compliance |
| **Sentinel** | `github.com/bonaventuratommasosam-bot/hermesbro-sentinel` | Security audit: vulnerability scanning, pentesting |
| **Machiavelli** | `github.com/bonaventuratommasosam-bot/hermesbro-machiavelli` | Multi-agent orchestrator: DAG dispatch, workflows |

Each repo has its own README with full docs: features, requirements, setup, examples, config reference.

## Requirements

- [Hermes Agent](https://hermes-agent.nousresearch.com) v0.16.0+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- DeepSeek API key (or any supported LLM provider)
- Agent-specific services (Google Sheets for Groot, etc.)

## Business Model

- **Code**: MIT License — free, open, forkable
- **Service**: We sell setup, customization, and managed bots
  - Pre-trained agent configuration for your domain
  - Custom training and skill development
  - Ongoing support and maintenance
- **Contact**: [hermesbro.cloud](https://hermesbro.cloud)

## Built with

- [Hermes Agent](https://hermes-agent.nousresearch.com) — open-source AI agent framework
- DeepSeek V4 Pro
- Telegram Bot API

## License

MIT — see [LICENSE](LICENSE)
