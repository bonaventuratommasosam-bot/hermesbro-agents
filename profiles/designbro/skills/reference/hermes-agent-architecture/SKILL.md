---
name: hermes-agent-architecture
description: >
  Reference: Hermes Agent architecture, learning loop, memory tiers, 
  skills evolution, GEPA, profiles, cron. Source: Avi Chawla / Akshay Pachaar 
  "Hermes Agent Masterclass" (2026-05-13).
version: 1.0.0
author: gribbito
tags: [hermes, architecture, reference, self-evolution]
---

# Hermes Agent Architecture Reference

## Core Architecture

- Single `AIAgent` class in `run_agent.py` — CLI, gateway, batch, IDE all route into same core loop
- ReAct-style synchronous loop: build system prompt → check compression → API call → tool calls → loop
- 90 turns hard cap per task (shared with subagents)
- 6 terminal backends: local, Docker, SSH, Modal, Daytona, Singularity (config change only)
- Works with any model via translation layer (3 API formats)
- Swap Claude → GPT → Gemini → local Ollama with one command

## Identity Layer: SOUL.md

- Lives at `~/.hermes/SOUL.md`, slot #1 in system prompt
- Hand-authored, static — defines personality, tone, communication style, hard limits
- All memory and skills happen through the lens of this identity
- SOUL.md = fixed frame. Memory + skills = moving parts inside it.

## Three-Tier Memory

### Tier 1: Markdown Files (always in context)
- `MEMORY.md` (2,200 chars max) — agent's notes: environment, conventions, tool quirks, lessons
- `USER.md` (1,375 chars max) — user profile: name, preferences, skill level, avoidances
- Injected as frozen snapshot at session start
- Mid-session writes persist to disk but won't appear until next session
- At ~80% capacity, agent consolidates (merges related entries into denser versions)

### Tier 2: Session Search (unlimited, on-demand)
- Every conversation stored in SQLite with FTS5
- Requires active search + LLM summarization
- Critical facts → Tier 1. Everything else → searchable on demand.

### Tier 3: External Memory Providers (8 plugins)
- Only one active at a time
- Auto-prefetch before each turn, sync after each response, extract on session end
- Never replaces built-in memory — runs alongside

## Self-Evolving Skills

### Structure
- SKILL.md files with YAML frontmatter
- Progressive disclosure:
  - Level 0: names + descriptions only (~3k tokens for full catalog)
  - Level 1: full skill content loaded when needed
  - Level 2: drill into specific reference files

### Creation Triggers (autonomous via `skill_manage`)
- Complex task completed (5+ tool calls)
- Hit errors/dead ends, found working path
- User corrected approach
- Discovered non-trivial workflow

### Loop: Problem → solve → save SKILL.md → next time load proven procedure

### Garbage Collection (Curator)
- Runs on inactivity check (not cron): 7 days since last run + 2+ hours idle
- Automatic transitions (deterministic):
  - 30 days unused → stale
  - 90 days unused → archived
- LLM review (up to 8 iterations): keep / patch / consolidate / archive
- Only touches agent-authored skills (never bundled/hub)
- Never auto-deletes — worst case: archive to `~/.hermes/skills/.archive/`
- Pre-pass: tar.gz snapshot of entire skills directory
- Pin critical skills: `hermes curator pin <skill>` (protects from archive/delete, patches still allowed)

## GEPA (Genetic-Pareto Prompt Evolution)

- NOT in Hermes runtime — companion repo: `NousResearch/hermes-agent-self-evolution`
- Offline optimization pipeline
- Problem: agent self-congratulation (always thinks it did well)
- Solution: read execution traces → understand failures → generate improvements

### Pipeline
1. Read current skill from Hermes repo
2. Generate evaluation dataset (synthetic via Claude Opus, real session history from SQLite, or golden sets)
3. Run optimizer: read traces → find failures → generate candidate variants
4. Evaluate with LLM-as-judge + rubrics (not binary pass/fail)
5. Constraint gates: 100% test suite pass, skills <15KB, caching compatible, no semantic drift
6. Best variant → PR against Hermes repo (never direct commit)

- No GPU required. Cost: ~$2-10 per optimization run.
- Try GEPA before fine-tuning (RL/GRPO).

## Profiles (Multi-Agent)

- Fully isolated instances: config, memory, skills, sessions, SOUL.md
- Share nothing by default
- Each needs its own Telegram bot token (one connection per token)
- Create: `hermes profile create <name> --clone`
- Gateway setup per profile: `hermes -p <name> gateway setup`

### Shared Knowledge Layer (added 2026-05-31)

Profiles are isolated by default, but a Shared Knowledge Layer bridges them:
- `<HERMES_ROOT>/shared/knowledge/` — facts.md, decisions.md, preferences.md
- Auto-synced to each profile as `shared-knowledge.md` every 30min
- Event-driven bus watcher (systemd, 30s poll) routes knowledge events in near-real-time
- Skill sync from gribbito (source of truth) to all profiles every 6h
- Session digest extracts insights from sessions daily at 23:00
- Full protocol: see `shared-knowledge-protocol` skill

## Cron Jobs

- Built-in scheduler, gateway daemon ticks every 60s
- Runs in isolated agent sessions
- Survives restarts, stored in `~/.hermes/cron/jobs.json`
- English → cron syntax conversion
- Delivery to any messaging platform
- Skill attachment: `--skill <name>`
- Job chaining: one cron's output → next cron's input via `context_from`

### Patterns
- One-shot: `30m`, ISO timestamp
- Recurring: `every 2h`, `0 9 * * 1-5`
- Skill-loaded: attach skill before running prompt
- Chained: context_from another job ID

### no_agent Script Jobs — Pitfall

When `no_agent=True`, the `script` field is a **relative filename** resolved under `~/.hermes/scripts/`. It is NOT a shell command string.

**WRONG** (treated as filename, fails with "Script not found"):
```
script: "cd <HERMES_ROOT>/shared/linkedin && python3 linkedin.py post-file <HERMES_ROOT>/shared/marketing/linkedin/post-1.txt"
```

**CORRECT** (create a `.sh` wrapper in `~/.hermes/scripts/`, reference by filename only):
1. Create `~/.hermes/scripts/linkedin-post-1.sh`:
   ```bash
   #!/bin/bash
   cd <HERMES_ROOT>/shared/linkedin && python3 linkedin.py post-file <HERMES_ROOT>/shared/marketing/linkedin/post-1.txt
   ```
2. `chmod +x ~/.hermes/scripts/linkedin-post-1.sh`
3. Set `script: "linkedin-post-1.sh"` in the cron job (no path prefix, just the filename)

**Key rules:**
- Scripts MUST live in `~/.hermes/scripts/` — absolute paths are rejected
- Scripts MUST be executable (`chmod +x`)
- The `script` field is just the filename, not a path
- For multi-command workflows, use a `.sh` wrapper with `cd` + the actual command

## Skills Hub

- 687 skills across 18 categories
- 87 built-in, 79 optional, 16 from Anthropic, 505 from LobeHub
- Custom taps: `hermes skills tap add yourname/repo`
- Install: `hermes skills install yourname/repo/<skill>`

## Key Takeaways for GribbitO

1. **Memory consolidation is critical** — at 80% capacity, merge related entries
2. **Skills should be created proactively** — after complex tasks, save the approach
3. **Curator should run** — check if it's active, pin critical skills
4. **GEPA can optimize skills offline** — consider for Hermes Bots skills
5. **Profiles are the right multi-agent pattern** — we already do this correctly
6. **Cron chaining** — use context_from for multi-stage automations
7. **Progressive disclosure** — skill catalog stays cheap, load full content on demand

## Patterns from Agenvoy (2026-05-29)

Analyzed pardnchiu/Agenvoy (Go, 139★) — personal AI agent with similar architecture. Key patterns worth considering:

- **Error Memory**: Structured records (tool_name, keywords, symptom, cause, action, outcome: resolved|failed|abandoned). Auto-triggered on tool failure + fallback resolution. 3-month TTL with refresh on search hit. More structured than our unstructured MEMORY.md approach.
- **Dispatcher Routing**: Dedicated model classifies task → routes to best-fit worker (Claude for code, GPT for research, Gemini for video). Task-type chains with version-axis tiebreaker. We do manual model switching.
- **Key Decisions Binding**: Summary context with `key_decisions` field that is explicitly "locked in — do not re-litigate unless user reopens". Prevents re-deciding settled questions.
- **Lazy-load format reference**: `telegram_format` tool loads HTML rules once per session instead of hardcoding in system prompt.

Full analysis: see `references/competitive-analysis-agenvoy.md` in [REDACTED — dati personali rimossi]-stack-manager skill.
