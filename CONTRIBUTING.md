# Contributing to HermesBro

Thank you for helping grow the HermesBro open-source agent ecosystem.

## Ways to contribute

- **New agent template** for a domain we don't cover (HR, healthcare, logistics)
- **Improve SOUL.md or skills** on an existing agent repo
- **Italian / English localization** for agent profiles and Telegram copy
- **Tests and CI** — smoke tests, setup scripts, Docker compose
- **Documentation** — README examples, setup guides, architecture notes
- **Bug reports** via GitHub Issues (one issue per repo)

## Where to open issues / PRs

| Contribution type | Target repo |
|-------------------|-------------|
| Shared skills, templates, cross-agent docs | **hermesbro-agents** (this repo) |
| Bug or feature on a specific agent | That agent's repo (`hermesbro-groot`, `hermesbro-contabile`, …) |
| Brand-new custom agent from scratch | [hermes-agent-factory](https://github.com/bonaventuratommasosam-bot/hermes-agent-factory) |
| Landing site, deploy, storefront | `hermesbro-agents` with label `site` |

## Setup

```bash
# 1. Fork + clone this repo (or the agent repo you are changing)
git clone https://github.com/<you>/hermesbro-agents.git
cd hermesbro-agents

# 2. Install Hermes Agent
pip install hermes-agent

# 3. Install an agent profile to test locally
hermes profile install github.com/bonaventuratommasosam-bot/hermesbro-contabile --alias contabile
```

Read each agent repo's README for agent-specific env vars and services.

## Agent structure

Each agent is distributed as a **Hermes Profile Distribution** in its own repo:

```
hermesbro-<agent>/
├── SOUL.md          # Personality, instructions, constraints
├── GOAL.md          # Objectives (where applicable)
├── skills/          # Tool integrations (.md skill files)
├── distribution.yaml
├── setup.sh / setup.py
└── README.md
```

The legacy `profiles/` folder in this monorepo is **deprecated** — see [profiles/DEPRECATED.md](profiles/DEPRECATED.md).

## Pull request process

1. Create a branch: `feat/your-feature` or `fix/short-description`
2. Make changes and **test locally**:
   ```bash
   hermes -p <agent> gateway start
   ```
3. Open a PR against `main` with:
   - What changed and why
   - How to test (commands, Telegram steps)
   - Screenshots or terminal output if UI/Telegram-facing
4. CI checks must pass (when configured)
5. One maintainer approval required before merge

## Good first issues

Look for the **`good first issue`** label on [hermesbro-agents issues](https://github.com/bonaventuratommasosam-bot/hermesbro-agents/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

Typical starter tasks:

- Translate a `SOUL.md` to English (or Italian)
- Add example outputs to an agent README
- Docker Compose for a 3-agent demo stack
- Single-command `setup.sh` for first-time contributors
- GitHub Actions smoke test workflow

## Code standards

- Python 3.12+ where applicable
- Follow Hermes Profile Distribution layout (`SOUL.md`, `skills/`, `.env.EXAMPLE`)
- **Never commit secrets** — use `.env.EXAMPLE` only
- MIT license: contributions are under the same license as the target repo

## Community

- **Site:** [hermesbro.cloud/contribute.html](https://hermesbro.cloud/contribute.html)
- **Organization:** [bonaventuratommasosam-bot](https://github.com/bonaventuratommasosam-bot)

## Code of conduct

Be respectful. No spam, no untested bulk PRs. Maintainers decide merge timing and scope.
