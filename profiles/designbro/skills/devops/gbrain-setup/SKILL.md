---
name: gbrain-setup
description: >
  Install, configure, and maintain GBrain (garrytan/gbrain) — knowledge graph
  and memory layer for AI agents. Covers PGLite local setup, embedding providers,
  search modes, skill scaffolding, knowledge graph wiring, and recurring maintenance.
triggers:
  - gbrain
  - knowledge graph
  - brain init
  - gbrain install
  - gbrain config
  - gbrain skillpack
  - gbrain dream
  - gbrain doctor
  - gbrain search
  - memory layer
  - shared memory for agents
---

# GBrain Setup & Configuration

GBrain = knowledge graph + memory layer for AI agents. Repo: `garrytan/gbrain`.
Gives agents persistent, searchable, self-wiring memory across sessions.

## When to Use

- Setting up gBrain on a new VPS or profile
- Connecting gBrain as MCP server to Hermes bots
- Importing knowledge from existing sources (shared knowledge, bot profiles, plans, marketing)
- Configuring automated capture from cron jobs
- Running dream/brainstorm/think queries
- WASM init errors or corrupted brain recovery

## Prerequisites

- **bun** (Bun runtime) — usually pre-installed at `~/.bun/bin/bun`
- **OPENAI_API_KEY** — for embeddings (`text-embedding-3-small`, 1536d)
- **ANTHROPIC_API_KEY** (optional) — needed for `gbrain dream`, `gbrain autopilot`, subagent features
- **mcp** Python package (`pip install mcp`) — needed if gbrain runs as MCP server for Hermes integration

## Installation (from cloned repo — preferred)

The `bun install -g` path can silently skip postinstall hooks. Use the clone path:

```bash
export PATH="$HOME/.bun/bin:$PATH"
cd /home/[REDACTED — dati personali rimossi]/ai-stack/gbrain
bun install && bun link        # registers 'gbrain' CLI globally
gbrain --version               # verify
```

Ensure bun PATH persists:
```bash
grep -q '.bun/bin' ~/.bashrc || echo 'export PATH="$HOME/.bun/bin:$PATH"' >> ~/.bashrc
```

## Initialization

```bash
cd /home/[REDACTED — dati personali rimossi]/ai-stack/gbrain-brain   # brain workspace dir
gbrain init --pglite                    # PGLite = no server, no Docker, 2 seconds
```

This auto-detects API keys from environment and picks embedding model.
Output shows: embedding model, expansion model, chat model.

## Search Mode (MANDATORY user prompt — Step 3.5)

After init, MUST present this cost matrix to the user and ask which mode:

```
Costo per-query @ 10K queries/mese:

                  Haiku 4.5     Sonnet 4.6    Opus 4.7
                  ($1/M)        ($3/M)        ($5/M)
  conservative    $40/mo        $120/mo       $200/mo
  balanced        $100/mo       $300/mo       $500/mo
  tokenmax        $200/mo       $600/mo       $1,000/mo
```

- **conservative** — 4K budget, no LLM expansion, 10 chunks. Cheapest.
- **balanced** — 12K budget, 25 chunks. Middle ground.
- **tokenmax** (default) — no limit, LLM expansion ON, 50 chunks. Best quality.

Apply choice:
```bash
gbrain config set search.mode <mode>
```

## Core Operations (Capture / Query / Think / Brainstorm)

### Capture (input content)
```bash
gbrain capture "Trade chiuso: ETH +12%, funding rate negativo" --type note --source el-froggo
gbrain capture "Decision: hedged BTC position via put options" --type event --source trading
```

### Query (hybrid search — use this, not `search`)
```bash
gbrain query "quali trade hanno funzionato meglio questo mese"
```

### Think (temporal questions — grounded in timeline)
```bash
gbrain think "quando abbiamo cambiato strategia su Base"
```

### Brainstorm (bisociative idea generation)
```bash
gbrain brainstorm "come hedge una posizione long ETH con budget limitato" --save
gbrain lsd "perché la maggior parte dei trader retail perde soldi" --save
```
`lsd` = Lateral Synaptic Drift: inverted-judge brainstorm rewarding counter-intuitive ideas.

### Graph operations
```bash
gbrain link people/el-froggo projects/hermes-fleet --type "member_of"
gbrain graph-query people/el-froggo --depth 2
gbrain backlinks concepts/defi-strategies
```

## Knowledge Graph Wiring

After init, backfill the typed-link graph:
```bash
gbrain extract links --source db
gbrain extract timeline --source db
gbrain stats                    # verify links > 0 (0 is OK for fresh brain)
```

## Skill Scaffolding

GBrain ships 43-64 skills. Scaffold into the brain workspace:

```bash
cd /home/[REDACTED — dati personali rimossi]/ai-stack/gbrain          # MUST be in gbrain repo root
gbrain skillpack scaffold --all --workspace /home/[REDACTED — dati personali rimossi]/ai-stack/gbrain-brain/brain
```

## Knowledge Import

Organize source files into the brain directory structure before importing:

```
brain/
├── people/         # Person entities
├── companies/      # Company entities
├── concepts/       # Shared knowledge, decisions, facts
├── projects/       # Project docs
├── ideas/          # Ideas and brainstorming
├── infrastructure/ # VPS, ports, configs
├── bots/           # Bot SOUL.md + GOAL.md files
├── marketing/      # Brand, outreach, templates, content calendars
├── plans/          # Strategic plans
└── templates-legali/ # Legal templates
```

Import + embed:
```bash
gbrain import /path/to/brain/ --no-embed   # import first (fast, no API cost)
gbrain embed --stale                        # then embed (uses API credits)
```

Wire the knowledge graph (for brains with existing content):
```bash
gbrain extract links --source db
gbrain extract timeline --source db
gbrain stats    # verify pages > 0, embedded > 0
```

**VPS knowledge sources ([REDACTED — dati personali rimossi]'s setup):**
- Shared knowledge: `<HERMES_ROOT>/shared/knowledge/` (7 files)
- Plans: `<HERMES_ROOT>/plans/` (10 files)
- Bot profiles: `<HERMES_ROOT>/profiles/<bot>/{SOUL,GOAL}.md` (12 bots)
- Marketing: `<HERMES_ROOT>/shared/marketing/` (34 files — brand, outreach, templates, LinkedIn, audit)
- Infrastructure: ai-stack root docs, brain workspace docs

## Connect to Hermes Bot via MCP

GBrain can run as an MCP server (`gbrain serve`) inside any Hermes bot. Add to the bot's profile config:

```yaml
# ~/.hermes/profiles/<bot>/config.yaml
mcp_servers:
  gbrain:
    command: /root/.bun/bin/gbrain
    args:
    - serve
    env:
      OPENAI_API_KEY: <actual-key>
      PATH: /root/.bun/bin:/usr/local/bin:/usr/bin:/bin
    timeout: 120
    connect_timeout: 60
```

Restart the bot:
```bash
systemctl restart hermes-<bot>
```

Verify gBrain subprocess is running:
```bash
systemctl status hermes-<bot>   # look for 'gbrain serve' in CGroup tree
```

Tools appear as `mcp_gbrain_*` (search, query, think, graph-query, etc.).

**Important:** Profile-level `mcp_servers` REPLACES default config entirely. Must add gBrain to each bot's profile config individually. (See native-mcp skill pitfall.)

## Health Check

```bash
gbrain doctor --json            # full health report
gbrain stats                    # page/chunk/link counts
gbrain config show              # current configuration
```

## Maintenance (recurring)

- **Sync + embed** (every 15min): `gbrain sync --repo ~/brain && gbrain embed --stale`
- **Dream cycle** (nightly): `gbrain dream` — 8-phase overnight maintenance
- **Weekly**: `gbrain doctor --json && gbrain embed --stale`
- **Upgrade**: `cd ~/gbrain && git pull && bun install && gbrain apply-migrations --yes`

## Cron Automation

### Dream cycle (nightly compaction)
Schedule at 03:00. Runs: sync → embed → dream → stats.
Dream phases: lint, backlinks, sync, synthesize, extract, extract_facts, resolve_symbol_edges, patterns, recompute_emotional_weight, consolidate, propose_takes, grade_takes, calibration_profile, embed, orphans, schema-suggest, purge.
Without ANTHROPIC_API_KEY: synthesize and some advanced phases skip. Core phases still work.

### Auto-capture from bot cron jobs
Append `gbrain capture` steps to existing cron job prompts:
```
Dopo aver completato il task, cattura nel knowledge graph:
terminal: export PATH="$HOME/.bun/bin:$PATH" && gbrain capture "{riassunto}" --type note --source <botname>
```

### Daily summary capture
Schedule at 23:00. Read bot's daily output files, capture summary into brain.

## Pitfalls

1. **`bun install -g` skips postinstall** — use clone + `bun install && bun link` instead
2. **`gbrain skillpack scaffold` needs `--workspace`** — auto-detection fails without it. Run from gbrain repo root.
3. **Config key `agent.use_gateway_loop` does NOT exist** in v0.40.2.0 despite doctor warning suggesting it. The subagent warning is informational only — `gbrain search`, `gbrain think`, `gbrain query` work without Anthropic.
4. **No ANTHROPIC_API_KEY** = `gbrain dream` and `gbrain autopilot` won't work. Core search/think/query are fine with just OpenAI.
5. **bun not in PATH** — check `~/.bun/bin/bun` exists before reinstalling. Add to .bashrc if missing.
6. **Python yaml.dump exposes secrets** — when adding MCP config via Python, `$OPENAI_API_KEY` in the command line gets shell-expanded to the actual key. Either use a placeholder or read from env at runtime. The dumped YAML will contain the literal key value.
7. **Gateway restart needed for MCP config** — editing `mcp_servers:` in a profile config does NOT take effect until `systemctl restart hermes-<profile>`. No hot-reload. The restart may briefly log `telegram.error.Conflict` if the bot was active — the new process takes over cleanly.
8. **`gbrain serve` MCP verification** — test the MCP server directly: `echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | gbrain serve`. Should return serverInfo with version.
9. **PGLite WASM init error** — `gbrain init --pglite` can fail with WASM instantiation errors (fetch failed, invalid URL) if the brain dir exists but is corrupted or incomplete. Fix: delete the brain dir and reinit with explicit embedding params:
   ```bash
   rm -rf /root/.gbrain/brain.pglite
   gbrain init --pglite --embedding-model openai:text-embedding-3-small --embedding-dimensions 1536
   ```
   The `--embedding-model` + `--embedding-dimensions` flags bypass auto-detection which can trigger the WASM error.
10. **`gbrain sources add` re-triggers WASM bug** — on some setups, adding sources during init triggers the same WASM error. Workaround: init without sources, import separately with `gbrain import <dir>`.
11. **`gbrain capture` vs `gbrain put`** — `capture` is the unified entrypoint (inline, file, stdin, routes to inbox). `put` writes directly to a slug. Prefer `capture` for agent workflows.
12. **Orphan pages** — Fresh imports create orphan pages. They resolve over time as the agent writes linked content. Don't panic about `orphans: 131`.
13. **Link extraction on import** — `gbrain extract links --source db` may return 0 links if imported markdown lacks frontmatter with entity references. This is normal — auto-link populates the graph as the agent writes pages going forward.

## [REDACTED — dati personali rimossi]'s Setup (reference)

- Repo: `/home/[REDACTED — dati personali rimossi]/ai-stack/gbrain/` (v0.40.2.0)
- Brain: `/root/.gbrain/brain.pglite` (PGLite)
- Workspace: `/home/[REDACTED — dati personali rimossi]/ai-stack/gbrain-brain/brain/`
- Embedding: `openai:text-embedding-3-small` (1536d)
- Chat/Expansion: `litellm:mimo-v2.5-pro`
- Search mode: `tokenmax`
- Skills: 64 scaffolded
- No ANTHROPIC_API_KEY — dream/autopilot disabled
- **Knowledge imported:** 131 pages, 454 chunks, 448 embedded
- **MCP connected to:** El Froggo (verified working, 2026-06-05)
- **El Froggo config:** `<HERMES_ROOT>/profiles/el-froggo/config.yaml` has `mcp_servers.gbrain`
- CLI: `~/.bun/bin/gbrain` (PATH in .bashrc)
