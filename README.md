# HermesBro — 11 open-source AI agents for business

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Hermes Agent](https://img.shields.io/badge/Built%20on-Hermes%20Agent-blue)](https://github.com/NousResearch/hermes-agent)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

> A fleet of 11 specialized AI agents you can fork, customize, and deploy on **your own VPS**. Accounting, legal, design, trading, security, education, orchestration — no vendor lock-in. Bring your own LLM API keys. Built on [Hermes Agent](https://github.com/NousResearch/hermes-agent) by NousResearch.

**Site:** [hermesbro.cloud](https://hermesbro.cloud) · **Org:** [bonaventuratommasosam-bot](https://github.com/bonaventuratommasosam-bot)

---

## What is HermesBro?

HermesBro is an open-source ecosystem of business AI agents. Each agent is a **Hermes Profile Distribution** — `SOUL.md`, skills, cron jobs, and domain config — installable with one command. Run on Telegram or CLI. **MIT license** — use in commercial projects freely.

- **No vendor lock-in** — deploy on your VPS, your keys, your data
- **No black box** — every agent has a public GitHub repo you can audit and fork
- **Optional managed deploy** — [HermesBro OS](https://hermesbro.cloud/os/) if you don't want to run infrastructure

---

## Quick start (5 steps)

```bash
# 1. Install Hermes Agent (v0.16.0+)
pip install hermes-agent

# 2. Install your first agent (example: ContAIbile)
hermes profile install github.com/bonaventuratommasosam-bot/hermesbro-contabile --alias contabile

# 3. Configure environment
cd ~/.hermes/profiles/contabile
cp .env.EXAMPLE .env
# Add TELEGRAM_BOT_TOKEN + DEEPSEEK_API_KEY (or your LLM provider)

# 4. Start the gateway
hermes -p contabile gateway start

# 5. Message your bot on Telegram
```

**Example output (ContAIbile):**

```
User: Calcola il margine operativo: ricavi 45k, costi 32k
ContAIbile: Margine operativo: 28,9%. Costo del lavoro al 34% — sopra la media
di settore (30%). Suggerisco di rivedere i turni del weekend.
```

---

## Agent roster

| Agent | Domain | Repo | Best for |
|-------|--------|------|----------|
| **ContAIbile** | Accounting | [hermesbro-contabile](https://github.com/bonaventuratommasosam-bot/hermesbro-contabile) | Invoicing, expense tracking, VAT, F24 |
| **LAWrenzo** | Legal | [hermesbro-lawrenzo](https://github.com/bonaventuratommasosam-bot/hermesbro-lawrenzo) | Contracts, GDPR, compliance, deadlines |
| **GROOT** | Operations / Kitchen | [hermesbro-groot](https://github.com/bonaventuratommasosam-bot/hermesbro-groot) | Food cost, inventory, shopping list, HACCP |
| **Wannabe** | Social Media | [hermesbro-wannabe](https://github.com/bonaventuratommasosam-bot/hermesbro-wannabe) | Editorial calendar, copy, campaigns |
| **DesignBro** | Design | [hermesbro-designbro](https://github.com/bonaventuratommasosam-bot/hermesbro-designbro) | Brand identity, logos, palettes, assets |
| **DUCATO** | Finance / Trading | [hermesbro-ducato](https://github.com/bonaventuratommasosam-bot/hermesbro-ducato) | Market analysis, portfolios, scenarios |
| **El Froggo** | DeFi / Fleet | [hermesbro-el-froggo](https://github.com/bonaventuratommasosam-bot/hermesbro-el-froggo) | Fleet pulse, routing, Base chain ops |
| **Sentinel** | Security | [hermesbro-sentinel](https://github.com/bonaventuratommasosam-bot/hermesbro-sentinel) | SSL audit, smart contracts, pentest |
| **FRANK** | Development | [hermesbro-mrrobot](https://github.com/bonaventuratommasosam-bot/hermesbro-mrrobot) | Code, DevOps, dependency audit, deploy |
| **Machiavelli** | Orchestration | [hermesbro-machiavelli](https://github.com/bonaventuratommasosam-bot/hermesbro-machiavelli) | Multi-agent DAG, workflows, debate |
| **Study** | Education | [study](https://github.com/bonaventuratommasosam-bot/study) | AI tutor — Feynman, Montessori, exam prep |

Install any agent:

```bash
hermes profile install github.com/bonaventuratommasosam-bot/hermesbro-<agent> --alias <name>
```

Each repo has its own README: features, requirements, setup, examples.

---

## Ecosystem

| Project | Description |
|---------|-------------|
| [hermes-agent-factory](https://github.com/bonaventuratommasosam-bot/hermes-agent-factory) | Generate custom Hermes profiles from an interview |
| [study](https://github.com/bonaventuratommasosam-bot/study) | Open-source AI tutor (11th fleet agent) |
| [Skills hub](https://hermesbro.cloud/skills.html) | 117+ shared Hermes skills |
| [War Room](https://hermesbro.cloud/warroom.html) | Live Machiavelli orchestration demo |

> **Note:** `profiles/` in this repo is **deprecated**. Use per-agent repos above. See [profiles/DEPRECATED.md](profiles/DEPRECATED.md).

---

## Requirements

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) v0.16.0+
- Telegram Bot Token ([@BotFather](https://t.me/BotFather)) for Telegram mode
- LLM API key (DeepSeek, OpenAI, Anthropic, or any supported provider)
- Agent-specific services where noted (e.g. Google Sheets for GROOT)

---

## Why open source?

- **No vendor lock-in** — your VPS, your rules
- **You control API keys and data** — nothing phones home to HermesBro
- **MIT license** — fork, sell services, embed in products

Managed deploy (optional): [hermesbro.cloud/os](https://hermesbro.cloud/os/) — pay-per-deploy on Base Chain, same MIT code underneath.

---

## Built with

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) by NousResearch
- [Base](https://base.org) chain integration (payments, on-chain verify)
- Hyperliquid PRO engine (trading agents — see `hermesbro-ducato` / trading-bot services)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Good first issues are labeled **`good first issue`**.

- Site & docs: [hermesbro.cloud/contribute.html](https://hermesbro.cloud/contribute.html)
- Bug on one agent → open issue on that agent's repo
- Cross-cutting skill/template → PR here on `hermesbro-agents`

---

## License

MIT — see [LICENSE](LICENSE). Each agent repo is MIT as well.
