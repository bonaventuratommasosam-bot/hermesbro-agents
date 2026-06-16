---
name: gstack
description: "GStack integration for Hermes Agent — use gstack skills (review, cso, investigate, ship, qa, health, autoplan, office-hours) directly from Hermes. GStack is installed at ~/.claude/skills/gstack/."
version: 1.0.0
triggers:
  - gstack
  - code review
  - security audit
  - ship this
  - qa test
  - health check
  - office hours
  - autoplan
  - investigate
  - root cause
  - debug this
  - cso
---

# GStack Integration for Hermes

GStack (v1.44.0.0) is installed at `~/.claude/skills/gstack/`. It's a collection of 53 workflow skills for software development. Each skill is a detailed markdown playbook.

## How to invoke

Read the full SKILL.md for the requested skill, then follow its steps using Hermes tools (terminal, read_file, search_files, browser, etc.).

```bash
SKILL_DIR=~/.claude/skills/gstack
# Read a skill:
cat $SKILL_DIR/<skill-name>/SKILL.md
```

## Available Skills (most useful)

### Planning
- **office-hours** — YC-style product brainstorming. Six forcing questions.
- **autoplan** — Run CEO → design → eng → DX review pipeline automatically.
- **plan-ceo-review** — CEO-level review of a feature idea.
- **plan-eng-review** — Architecture lock: data flow, edge cases, tests.
- **plan-design-review** — Design quality audit (0-10 per dimension).

### Code Quality
- **review** — Pre-landing PR review. SQL safety, LLM trust boundaries, side effects.
- **cso** — Security audit: OWASP Top 10, STRIDE, secrets archaeology, supply chain.
- **investigate** — Root-cause debugging. Four phases: investigate → analyze → hypothesize → implement.
- **health** — Code quality dashboard: type checker, linter, tests, dead code.

### Shipping
- **ship** — Full ship workflow: test, review, bump VERSION, update CHANGELOG, commit, push, PR.
- **land-and-deploy** — Merge PR, wait for CI, deploy, verify production health.
- **qa** — QA test a web app, find bugs, fix them, re-verify.
- **canary** — Post-deploy monitoring loop.

### Memory & Context
- **learn** — Manage project learnings across sessions.
- **context-save** / **context-restore** — Save and resume working context.
- **retro** — Weekly retro with shipping streaks.
- **sync-gbrain** — Keep gbrain current with repo code.

### Browser
- **browse** — Headless Chromium for QA testing (~100ms/command).
- **scrape** — Pull data from a web page.
- **design-review** — Live-site visual audit + fix loop.

## Preamble handling

GStack skills have a `## Preamble` bash block meant for Claude Code. In Hermes, SKIP the preamble — use Hermes tools directly instead:
- `$B` (Bash) → `terminal()`
- `$D` (Read) → `read_file()`
- Grep/Glob → `search_files()`
- AskUserQuestion → `clarify()`
- Edit/Write → `write_file()` / `patch()`
- WebSearch → `web_search()`

## GStack bin tools

GStack has standalone binaries at `~/.claude/skills/gstack/bin/`:

```bash
# Update check
~/.claude/skills/gstack/bin/gstack-update-check

# Config
~/.claude/skills/gstack/bin/gstack-config get <key>

# Repo mode detection
~/.claude/skills/gstack/bin/gstack-repo-mode

# Security dashboard
~/.claude/skills/gstack/bin/gstack-security-dashboard

# Learnings search
~/.claude/skills/gstack/bin/gstack-learnings-search <query>

# GBrain integration
~/.claude/skills/gstack/bin/gstack-gbrain-detect
~/.claude/skills/gstack/bin/gstack-gbrain-sync
```

## GBrain Integration

GStack has built-in gbrain awareness. The `sync-gbrain` skill keeps the knowledge graph current with repo code:

```bash
# Detect if gbrain is available
~/.claude/skills/gstack/bin/gstack-gbrain-detect

# Sync current repo to gbrain
~/.claude/skills/gstack/bin/gstack-gbrain-sync
```

Use after `ship` or `land-and-deploy` to capture what changed in the knowledge graph.

## Pitfalls

- GStack skills assume Claude Code's tool set. Translate: `$B` → terminal, `$D` → read_file.
- Skills reference `.claude/` directory in repos — on Hermes, use `~/.claude/skills/gstack/`.
- The preamble bash block is Claude Code-specific. Skip it, run the actual skill steps.
- `AskUserQuestion` → use `clarify()` in Hermes.
- Skills that need `Agent` (sub-agent) → use `delegate_task()` in Hermes.
- The `browse` skill needs the gstack browse binary. Check `~/.claude/skills/gstack/browse/dist/browse`.
- `ship` and `land-and-deploy` need git repos with proper remote configured.
- GStack has 53+ skills — read the SKILL.md for the specific one needed rather than guessing from the name.
