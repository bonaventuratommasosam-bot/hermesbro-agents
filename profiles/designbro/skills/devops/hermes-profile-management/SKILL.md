---
name: hermes-profile-management
description: >
  Manage Hermes Agent profiles: identity, SOUL.md customization, renaming, and lifecycle.
  Covers profile structure, personality writing, and safe rename procedures.
version: 1.0
author: Hermes
metadata:
  hermes:
    tags: [devops, profiles, soul, personality, infrastructure]
---

# Hermes Profile Management

Manage Hermes Agent profiles: identity, SOUL.md customization, renaming, and lifecycle.

## When to Use

- Creating, renaming, or deleting Hermes profiles
- Customizing SOUL.md personality files
- Debugging profile-related confusion (wrong bot responding, wrong personality)
- Migrating profile references across skill files

## Critical Identity Rule

**Hermes (root `<HERMES_ROOT>/SOUL.md`) is the main assistant.** Named profiles are SEPARATE entities.

```
<HERMES_ROOT>/
├── SOUL.md                    ← Main Hermes (the assistant, braccio destro)
└── profiles/
    ├── gribbito/              ← GribbitO (main, dev+security) — SOUL.md: Fisher+Groucho+JARVIS
    ├── el-froggo/             ← El Froggo (crypto trading, Base chain) — SEPARATE bot, own Telegram identity
    ├── contabile/             ← ContAIbile (commercialista)
    ├── lawrenzo/              ← LAWrenzo (assistente legale)
    ├── groot/                 ← Groot (vineria)
    ├── wannabe/               ← Wannabe (marketing/content)
    ├── designbro/             ← DesignBro (design)
    ├── ducato/                ← Ducato (finanza)
    ├── machiavelli/           ← Machiavelli (clone di gribbitO, politica/scacchi/social media)
    └── sentinel/              ← Sentinel (security audit, on-chain, smart contract)
```

**PITFALL**: Never assume a profile named after a trading bot is "you" (Hermes). Hermes is the DEFAULT profile (`<HERMES_ROOT>/SOUL.md`). Named profiles are SEPARATE entities. [REDACTED — dati personali rimossi] was frustrated when I confused my identity with El Froggo's — twice.

**Identity map** (as of 2026-05-28):
- **Hermes / GribbitO** (`gribbito`) = [REDACTED — dati personali rimossi]'s main assistant. SOUL.md inspired by Fisher + Groucho + JARVIS. Absorbed: dev-agent, security-auditor, gribbito-agent (all consolidated 2026-05-28). Capabilities: dev (Python/JS/Solidity, TDD), security (vuln scan, smart contract audit), general assistant.
- **El Froggo** (`el-froggo`) = SEPARATE crypto trading bot. Own Telegram bot token, own X account (@FroggoEl18782), Virtuals Protocol offerings. NEVER merge into gribbito — [REDACTED — dati personali rimossi] explicitly corrected this (2026-05-28). Has own GOAL.md, cron jobs (Wallet Monitor, Alpha Scanner, Signal Tracker), data/signals, cache.
- **ContAIbile** (`contabile`) = commercialista AI. SOUL.md: Luca Pacioli + Mario Draghi + Gordon Ramsay.
- **LAWrenzo** (`lawrenzo`) = assistente legale. SOUL.md: Cesare Romiti + Harvey Specter + Horace Rumpole + Saul Goodman.
- **Groot** (`groot`) = vineria/chef AI ([REDACTED — dati personali rimossi]).
- **Wannabe** (`wannabe`) = marketing/content AI.
- **DesignBro** (`designbro`) = designer AI. SOUL.md: Fortunato Depero + Bruno Munari + Milton Glaser.
- **Ducato** (`ducato`) = esperto di finanza AI. SOUL.md: Warren Buffett + Nassim Taleb + Rocco Casalino. Covers: investimenti personali, financial planning, corporate finance, analisi macro. Path: `/home/[REDACTED — dati personali rimossi]/ai-stack/ducato/`.
- **Machiavelli** (`mach`) = clone di GribbitO con focus su politica, scacchi, social media analysis. Creato 2026-05-30. Copiati tutti i 42 skill, cron, memories da GribbitO.
- **Sentinel** (`sentinel`) = security auditor per smart contract e on-chain. SkillSpector installato per scan skill. Path: `/home/[REDACTED — dati personali rimossi]/ai-stack/agents/sentinel/`. Creato 2026-05-30.
- Old profiles `dev-agent`, `security-auditor`, `gribbito-agent` were CONSOLIDATED into `gribbito` on 2026-05-28. Do not recreate them.
- **el-froggo is SEPARATE** — own Telegram bot, own product identity. Do NOT merge into gribbito.

## SOUL.md Customization

SOUL.md is loaded fresh each message — no restart needed.

### Writing Personality Prompts

When the user asks for a personality inspired by real figures:
1. Research the figure's core philosophy and methods
2. Extract 3-5 transferable traits relevant to the agent's role
3. Write concrete behavioral rules, not vague adjectives
4. Include example dialogue lines
5. Add a "philosophy" section with memorable quotes

### Template Structure

```markdown
# [Agent Name] — [One-line identity]

[2-3 sentence origin story / inspiration]

## [Influence 1] gave you [trait]
[Concrete behavioral rule with example]

## [Influence 2] gave you [trait]
[Concrete behavioral rule with example]

## Communication Style
- [Specific rule]
- [Example output format]

## Rules (NEVER BREAK)
- [Hard constraint]
- [Hard constraint]

## Philosophy
*"Memorable quote that captures the essence"*
```

## Profile Renaming Checklist

Before renaming a profile, ALL of these must be updated:

1. **Skill files**: `grep -r "old-profile-name" ~/.hermes/skills/ --include="*.md"`
2. **Config files**: Check `config.yaml`, `.env` in the profile directory
3. **Cron jobs**: `hermes cron list` — check if any reference the profile
4. **Gateway state**: Stop gateway before renaming: `hermes gateway stop --profile old-name`
5. **Session references**: Old sessions may reference the profile (acceptable, don't touch history)
6. **Other profiles' skills**: Cross-references between profiles

### Safe Rename Procedure (tested 2026-05-27)

```bash
# 1. Stop the gateway
hermes gateway stop --profile old-name

# 2. Find ALL references (skip session JSONs — they're historical)
grep -r "old-name" ~/.hermes/ --include="*.md" --include="*.yaml" --include="*.yml" --include="*.json" 2>/dev/null | grep -v "/sessions/"

# 3. Rename the directory
mv ~/.hermes/profiles/old-name ~/.hermes/profiles/new-name

# 4. Update all references in active files (skills, plans, memories)
for f in $(grep -rl "old-name" ~/.hermes/skills/ ~/.hermes/plans/ ~/.hermes/memories/ --include="*.md" --include="*.yaml" --include="*.yml" 2>/dev/null); do
  sed -i 's/old-name/new-name/g' "$f"
done

# 5. Verify no stale references remain
grep -r "old-name" ~/.hermes/skills/ ~/.hermes/plans/ ~/.hermes/memories/ 2>/dev/null

# 6. Restart gateway
hermes gateway start --profile new-name
```

**PITFALL**: Hermes may auto-recreate deleted profile directories. If you `rm -rf` a profile while Hermes is running, empty dirs may reappear. This is harmless — just delete them again or ignore.

## Dashboard Management

```bash
# Check status
hermes dashboard --status

# Stop
hermes dashboard --stop

# Start (localhost only, secure — default)
hermes dashboard --port 9119

# Start (background, accessible from network — requires OAuth or --insecure)
hermes dashboard --port 9119 --host 0.0.0.0 --no-open --skip-build
```

**PITFALL**: `--host 0.0.0.0` REQUIRES OAuth authentication unless `--insecure` is passed. Without OAuth configured, the dashboard refuses to bind to non-localhost addresses. Two options:

1. **`--insecure`** — No auth, direct access. ⚠️ Exposes API keys to anyone on the network. Only for trusted LAN/VPN.
   ```bash
   hermes dashboard --port 9119 --host 0.0.0.0 --insecure --no-open --skip-build
   ```

2. **OAuth via Nous Portal** — Secure, requires `client_id`:
   ```bash
   # Interactive wizard (requires TTY — does NOT work from agent terminal)
   hermes setup --portal

   # Manual config (works non-interactively)
   hermes config set dashboard.oauth.client_id "agent:YOUR_CLIENT_ID"
   hermes dashboard --port 9119 --host 0.0.0.0 --no-open --skip-build
   ```
   To get the client_id: go to https://portal.nousresearch.com, create an account, create an "Agent Instance", copy the `client_id` (format: `agent:01HXYZ...`). The config key is `dashboard.oauth.client_id` in `config.yaml`.

**PITFALL**: `hermes setup --portal` is an interactive wizard that requires a real TTY. It does NOT work when run from the agent's terminal tool (even with pty=true). The user must either run it manually via SSH, or you can set the config key directly with `hermes config set dashboard.oauth.client_id "..."`.

**PITFALL**: Don't use `nohup` or shell background wrappers. Use `terminal(background=true)` so Hermes can track the process. `nohup ... &` will be rejected with an error.

**PITFALL**: The `--skip-build` flag is useful for quick restarts. Without it, the dashboard rebuilds the web UI which can take time.

## GOAL.md — Operational Objectives

SOUL.md defines WHO the agent is (personality, voice, values). GOAL.md defines WHAT the agent does (objectives, metrics, scope, constraints). Both live in the profile root.

```
~/.hermes/profiles/el-froggo/
├── SOUL.md    ← personality (Micky Malka style, community tone)
└── GOAL.md    ← objectives (trading signals, risk scanner, metrics)
```

### When to write a GOAL.md

- Agent has a clear mission beyond "help the user" (trading, marketing, coding)
- Agent runs autonomously via cron jobs and needs self-contained instructions
- Agent has measurable targets (hit rate, revenue, subscriber count)
- Agent has explicit "what I am NOT" boundaries

### Template Structure

```markdown
# [Agent] — Goal

[One paragraph: who you are and what you do]

## Your position
[What you manage, who you report to, what's in scope]

## What you do daily
[Concrete recurring tasks grouped by category]

## How you work
[Receive → Decompose → Delegate → Execute → Report]

## Priorities (ordered)
1. [Most important]
2. [Second]
3. [Third]

## What you NEVER do
[Hard constraints — things outside your scope]

## How you measure success
[Specific metrics with targets]

## Objective (12 months)
[Concrete milestones]
```

### SOUL.md vs GOAL.md

| | SOUL.md | GOAL.md |
|---|---|---|
| Purpose | Personality, voice, values | Objectives, scope, metrics |
| Tone | Narrative, philosophical | Operational, concrete |
| Changes | Rarely (personality is stable) | Quarterly (goals evolve) |
| Example | "You see through narratives" | "Hit rate >60% on trading signals" |

**PITFALL**: Don't merge GOAL into SOUL or vice versa. They serve different audiences: SOUL.md is read by the agent's LLM to shape behavior; GOAL.md is read to define scope and targets. Mixing them dilutes both.

### Existing GOAL.md files (as of 2026-05-31)

- `<HERMES_ROOT>/GOAL.md` — Hermes (orchestrator, business operations)
- `<HERMES_ROOT>/profiles/contabile/GOAL.md` — ContAIbile (accounting, proattivo)
- `<HERMES_ROOT>/profiles/lawrenzo/GOAL.md` — LAWrenzo (legal, proattivo)
- `<HERMES_ROOT>/profiles/groot/GOAL.md` — Groot (vineria)
- `<HERMES_ROOT>/profiles/designbro/GOAL.md` — DesignBro (design, integrazione Wannabe)
- `<HERMES_ROOT>/profiles/el-froggo/GOAL.md` — El Froggo (trading signals, risk scanner, Base chain)
- `<HERMES_ROOT>/profiles/mach/GOAL.md` — Machiavelli (politica, scacchi, social media)
- `<HERMES_ROOT>/profiles/wannabe/GOAL.md` — Wannabe (marketing/content)
- `<HERMES_ROOT>/profiles/ducato/GOAL.md` — Ducato (finanza, trading blockchain, Edge MCP)
- `<HERMES_ROOT>/profiles/sentinel/GOAL.md` — Sentinel (security guardian, threat monitoring)
- Note: gribbito has no GOAL.md (orchestrator, not needed)

## Profile Consolidation (Merging Profiles)

**⚠️ BEFORE YOU MERGE — ask: does this profile have its own product identity?**

Profiles that are **product-level bots** (own Telegram bot token, own X/social account, own offerings, distinct persona for a separate audience) MUST NOT be merged into the main profile. [REDACTED — dati personali rimossi] corrected this explicitly (2026-05-28): El Froggo has its own Telegram bot token, @FroggoEl18782 on X, Virtuals Protocol offerings, and distinct cron jobs — it is a separate product, not a variant of gribbito.

**Merge-safe profiles**: utility/role profiles that serve [REDACTED — dati personali rimossi] directly (dev-agent, security-auditor, gribbito-agent) — these have no external-facing identity and can be absorbed.

**Never merge without explicit confirmation**: profiles with their own Telegram bot token, external social accounts, or customer-facing offerings. When in doubt, ASK [REDACTED — dati personali rimossi] first.

When multiple profiles should be absorbed into one (e.g. dev-agent + security-auditor → gribbito), follow this order:

### Step 1: Inventory what moves
```bash
# Skills diff — what does the source have that the target doesn't?
diff <(ls ~/.hermes/profiles/target/skills/ | sort) <(ls ~/.hermes/profiles/source/skills/ | sort) | grep "^>"

# .env comparison — any unique env vars?
diff ~/.hermes/profiles/target/.env ~/.hermes/profiles/source/.env

# Cron jobs — any jobs to migrate?
ls ~/.hermes/profiles/source/cron/
cat ~/.hermes/profiles/source/cron/jobs.json 2>/dev/null
```

### Step 2: Copy skills
```bash
cd ~/.hermes/profiles
for skill in $(diff <(ls target/skills/ | sort) <(ls source/skills/ | sort) | grep "^>" | awk '{print $2}'); do
  cp -rn source/skills/$skill target/skills/
done
```
**PITFALL**: Use `cp -rn` (no-clobber) to avoid overwriting existing skills in the target.

### Step 3: Merge .env
If the source has env vars the target doesn't, append them. If they share the same keys with different values, the target's values usually win (they're the primary profile).

### Step 4: Update SOUL.md
Write a new SOUL.md for the target that incorporates the absorbed profiles' capabilities. Structure:
```markdown
# [Agent] — [Identity]

## Core Identity
[existing personality]

## [Absorbed Role 1] Capabilities
[transferred capabilities from source SOUL.md]

## [Absorbed Role 2] Capabilities
[transferred capabilities from source SOUL.md]

## Personality / Style
[merged personality traits]

## Constraints
[union of all constraints]
```
**PITFALL**: Don't just append the source SOUL.md sections — rewrite as a cohesive whole. The merged SOUL.md should read as one identity, not a Frankenstein of parts.

### Step 5: Migrate cron jobs
If the source had cron jobs, recreate them under the target profile via `hermes cron create --profile target`.

### Step 6: Verify no running processes
```bash
ps aux | grep "source-profile-name" | grep -v grep
```
If a gateway is running for the source, stop it first.

### Step 7: Preserve persona as skill (if the absorbed profile had a distinct identity)
If the absorbed profile had a unique persona (like El Froggo's crypto frog identity), save it as a skill under the target profile so the persona can be activated when needed:
```bash
mkdir -p ~/.hermes/profiles/target/skills/<source-persona-name>
# Write a SKILL.md with: identity, rules, tools, goals, "what I am NOT"
# Copy any persona-specific data dirs (signals, caches, etc.)
```
This preserves the persona's knowledge without maintaining a separate profile. The persona can be invoked by loading the skill.

### Step 8: Delete source profiles
```bash
rm -rf ~/.hermes/profiles/source-profile
```

### Step 9: Update memory and references
- Update memory to reflect the consolidation
- Grep across remaining profiles' skills for references to the deleted profile name
- Update any nginx configs, systemd units, or cron jobs that referenced the old profile

**PITFALL**: Forgetting to update memory means future sessions will reference deleted profiles as if they still exist. This causes confusion when doing `ls ~/.hermes/profiles/`.

## Bot Not Responding — Diagnostic Checklist

When [REDACTED — dati personali rimossi] says "non risponde" or "X non funziona", follow this exact sequence:

### Step 1: Check service status
```bash
systemctl status hermes-<profile>.service
```
Look for: `active (running)` vs `failed` vs `inactive (dead)` vs `disabled`.

### Step 2: Check logs for root cause
```bash
journalctl -u hermes-<profile>.service --since "5 min ago" --no-pager
```

**Scan for these exact error patterns (in priority order):**

| Log pattern | Root cause | Fix |
|---|---|---|
| `No messaging platforms enabled` | Missing `TELEGRAM_BOT_TOKEN` in profile `.env` | Add `TELEGRAM_BOT_TOKEN=<token>` to `~/.hermes/profiles/<name>/.env` |
| `No user allowlists configured` | Missing `TELEGRAM_ALLOWED_USERS` in profile `.env` | Add `TELEGRAM_ALLOWED_USERS=<ADMIN_CHAT_ID>` ([REDACTED — dati personali rimossi]'s chat ID) |
| `Telegram bot token already in use` | Another process is using the same token | Kill the other process or use a different token |
| `Unauthorized` / `401` | Token expired or revoked | Validate with `curl -s "https://api.telegram.org/bot<TOKEN>/getMe"`, get new token from BotFather if needed |
| `Failed to parse JSONRPC` (MCP EVM) | EVM MCP server prints startup text before JSON-RPC | Non-blocking — cosmetic error, ignore |

### Step 3: Enable and restart
```bash
systemctl enable --now hermes-<profile>.service
```

### Step 4: Verify Telegram connection
After restart, confirm Telegram connected:
```bash
journalctl -u hermes-<profile>.service --since "30 sec ago" --no-pager | grep -iE "telegram|platform|enabled|connected|running"
```
The key line to look for is the ABSENCE of `"No messaging platforms enabled"` — that means Telegram is connected.

### Common misconfiguration: `BOT_TOKEN` vs `TELEGRAM_BOT_TOKEN`

**PITFALL**: Standalone gold bots use `BOT_TOKEN` in their `.env`. Hermes profiles require `TELEGRAM_BOT_TOKEN`. When copying tokens from `/home/[REDACTED — dati personali rimossi]/ai-stack/<bot>-gold/.env` to a Hermes profile `.env`, the variable name MUST be renamed. If you just copy-paste, the gateway starts but Telegram is invisible — "No messaging platforms enabled".

```bash
# WRONG (standalone convention):
BOT_TOKEN=895404...

# RIGHT (Hermes profile convention):
TELEGRAM_BOT_TOKEN=895404...
```

**Also required**: `TELEGRAM_ALLOWED_USERS=<[REDACTED — dati personali rimossi]_chat_id>` — without this, all messages are denied even if the token is correct.

**Validated 2026-06-05**: El Froggo reactivation — had `BOT_TOKEN` (from gold), no `TELEGRAM_ALLOWED_USERS`. Fixed both → bot responded.

## Temporarily Disabling a Profile

When [REDACTED — dati personali rimossi] says "disattiva X temporaneamente" or "spegni X per ora":

```bash
# 1. Stop the systemd service + disable auto-start
systemctl stop hermes-<profile> && systemctl disable hermes-<profile>

# 2. Verify it's dead
ps aux | grep 'hermes --profile <profile>' | grep -v grep
# Should return nothing
```

**PITFALL**: `hermes -p <profile> gateway stop` refuses to run from inside the gateway ("Refusing to stop the gateway from inside the gateway process"). You MUST use `systemctl stop` or `kill <PID>` externally.

**PITFALL**: Killing the process alone (`kill <PID>`) is NOT enough if a systemd service exists — systemd will restart it within seconds. Always check for and disable the systemd service: `systemctl list-units | grep hermes-<profile>`. Tested 2026-06-03: Frank process respawned after SIGTERM until systemd service was stopped+disabled.

**PITFALL**: `systemctl disable` does NOT stop a running service — it only prevents auto-start on boot. You MUST `stop` first, then `disable`.

To re-enable: `systemctl enable --now hermes-<profile>`

## Profile Lifecycle

### Creating a New Bot Profile (Full Workflow)

When [REDACTED — dati personali rimossi] asks to create a new bot profile (e.g. "crea un nuovo profile per..."), follow this exact sequence:

```bash
# 1. Create the profile
hermes profile create <name>

# 2. Copy config from gold standard (contabile)
cp ~/.hermes/profiles/contabile/config.yaml ~/.hermes/profiles/<name>/config.yaml

# 3. Copy .env (API keys)
cp ~/.hermes/profiles/contabile/.env ~/.hermes/profiles/<name>/.env

# 4. Copy unified channel_directory.json
cp ~/.hermes/profiles/gribbito/channel_directory.json ~/.hermes/profiles/<name>/channel_directory.json

# 5. Create ai-stack directory
mkdir -p /home/[REDACTED — dati personali rimossi]/ai-stack/<name>/
```

Then write the SOUL.md following the 3-personality-merge pattern (see `references/bot-personality-pattern.md` in [REDACTED — dati personali rimossi]-stack-manager).

**After creation:**
- Add to `[REDACTED — dati personali rimossi]-stack-manager` bot inventory
- Update memory with new bot name and path
- Gateway starts stopped — `hermes gateway start --profile <name>` when ready
- Add bot to HERMES HUB group manually via Telegram
- Update `AGENT_META` in hermes-dashboard `main.py` if dashboard integration needed

**Pitfall**: Always copy config from `contabile` (the gold standard), not from gribbito. Gribbito's config has dev-specific settings that other bots don't need.

### Cloning an Existing Profile (Exact Copy)

When [REDACTED — dati personali rimossi] says "fotocopia di GribbitO" or "clone di X", copy EVERYTHING from the source profile:

```bash
# 1. Create directory structure
mkdir -p ~/.hermes/profiles/<new>/{audio_cache,bin,cache,cron,hooks,image_cache,logs,mcp-tokens,memories,pairing,plugins,sandboxes,scripts,sessions,skills,state-snapshots}

# 2. Copy config + identity files
cp ~/.hermes/profiles/<source>/config.yaml ~/.hermes/profiles/<new>/
cp ~/.hermes/profiles/<source>/.env ~/.hermes/profiles/<new>/
cp ~/.hermes/profiles/<source>/auth.json ~/.hermes/profiles/<new>/
cp ~/.hermes/profiles/<source>/SOUL.md ~/.hermes/profiles/<new>/

# 3. Copy all data directories
for dir in audio_cache bin cache cron hooks image_cache logs mcp-tokens memories pairing plugins sandboxes scripts sessions skills state-snapshots; do
  cp -r ~/.hermes/profiles/<source>/$dir/* ~/.hermes/profiles/<new>/$dir/ 2>/dev/null
done

# 4. Copy state database (session history)
cp ~/.hermes/profiles/<source>/state.db* ~/.hermes/profiles/<new>/

# 5. Copy metadata files
for f in .skills_prompt_snapshot.json .skip_upstream_prompt .update_check channel_directory.json gateway_state.json processes.json auth.lock; do
  cp ~/.hermes/profiles/<source>/$f ~/.hermes/profiles/<new>/ 2>/dev/null
done

# 6. Customize SOUL.md (optional — rename identity)
sed -i 's/<Source Name>/<New Name>/g' ~/.hermes/profiles/<new>/SOUL.md
```

**When to clone vs create fresh:**
- Clone: [REDACTED — dati personali rimossi] wants an identical copy with same tools, skills, personality (e.g., Machiavelli = clone of GribbitO)
- Create fresh: [REDACTED — dati personali rimossi] wants a new bot with different personality/role (use contabile as template)

**Pitfall**: Cloning copies session history (state.db). If [REDACTED — dati personali rimossi] wants a clean start, delete the cloned state.db after creation.

**Tested 2026-05-30**: Created Machiavelli as clone of GribbitO. All 42 skills, config, .env, memories, cron copied successfully.

**Pitfall**: The new profile's gateway is `stopped` by default. Don't forget to start it when [REDACTED — dati personali rimossi] asks to go live.

### Creating a Profile (Minimal)
```bash
hermes profile create <name>
```

### Deleting a Profile
1. Stop its gateway
2. Remove cron jobs that reference it (`hermes cron list`)
3. Update skill files that reference it (grep + sed)
4. Delete: `rm -rf ~/.hermes/profiles/<name>`
5. **Verify it's gone**: `ls ~/.hermes/profiles/` — Hermes may auto-recreate empty dirs. Delete again if needed.
6. Update memory to reflect the change

## SOUL.md Compliance (output quality gate)

SOUL.md rules are not just documentation — they are ACTIVE CONSTRAINTS on every response. The most common failure mode: getting excited about a task and producing verbose, emoji-heavy output that violates SOUL.md.

**Before sending any long-form output (>5 sentences), check:**
1. Are sentences short? ("Ogni parola deve meritare il suo posto")
2. Are there decorative emojis? (Remove all except ✅ ❌ ⚠️)
3. Is the tone minimalista? ("Fatto. Nessun errore." when things go well)
4. Would [REDACTED — dati personali rimossi] need to tell me to re-read SOUL.md? (If yes, rewrite)

**PITFALL**: Task excitement causes SOUL.md amnesia. When ideating, planning, or producing business documents, the default instinct is to write walls of text with emojis. Override this instinct. [REDACTED — dati personali rimossi] has explicitly corrected this behavior — treat it as a hard constraint, not a suggestion.

**PITFALL**: Don't produce markdown tables on Telegram — use bullet lists instead. Telegram has no table syntax.

## Resolving Standalone vs Gateway Process Conflicts

When a bot migrates from standalone FastAPI to a Hermes profile, the old process often keeps running alongside the new gateway — causing duplicate messages, port conflicts, or split state.

### Detection

```bash
# Step 1: Check systemd services FIRST (root cause of restarts)
systemctl list-units --type=service | grep -iE '(groot|lawrenzo|wannabe|contabile|ratatouille|<botname>)'

# Step 2: Find all bot-related processes
ps aux | grep -E '(bot|fastapi|uvicorn|gunicorn|python.*main|hermes)' | grep -v grep
```

Look for pairs like:
- `python -m groot_telegram.main` (old standalone) + `hermes --profile groot gateway run` (new)
- `python main.py` (old) + `hermes --profile lawrenzo gateway run` (new)
- `groot.service` + `hermes-groot.service` (two systemd units fighting)

### Safe Resolution — Systemd-First Approach

1. **Check systemd**: `systemctl list-units --type=service | grep <botname>` — identify old vs Hermes service units
2. **Verify the Hermes profile exists**: `ls ~/.hermes/profiles/<name>/`
3. **Confirm the Hermes gateway is running**: `ps aux | grep 'hermes --profile <name>'`
4. **Stop + disable the OLD systemd service**: `systemctl stop <old>.service && systemctl disable <old>.service`
5. **Verify**: `ps aux | grep <name> | grep -v grep` — only the Hermes gateway should remain
6. **If the old process STILL appears**: the service file may have `Restart=always`. Use `systemctl mask <old>.service` — this symlinks the unit to `/dev/null`, preventing any start even if another unit tries to trigger it.
7. **If mask fails with "File already exists"**: remove the service file first, then mask:
   ```bash
   rm -f /etc/systemd/system/<old>.service
   systemctl daemon-reload
   systemctl mask <old>.service
   ```
   Tested 2026-05-28: `wannabe.service` had a leftover file that blocked masking.

**PITFALL**: `systemctl disable` does NOT stop a running service — it only prevents auto-start on boot. You MUST `stop` first, then `disable`. If the service has `Restart=always`, even stop+disable won't prevent restarts on next trigger — use `mask` (symlinks to /dev/null) which is stronger than disable. Tested 2026-05-28: groot.service kept respawning after stop+disable, mask was needed.

**PITFALL**: Never kill a standalone process if no Hermes profile exists for that bot — you'll leave it completely dead. This happened with wannabe-bot: killed the standalone, discovered no Hermes profile existed, bot went offline entirely. Always verify the profile directory and gateway process FIRST.

### Bulk Cleanup

When multiple bots need migration, scan ALL at once for both systemd services and PIDs. Include related services (web dashboards, backup scripts, helper processes) — not just the main bot service. Example from a real session (2026-05-28):
- groot: old standalone kept restarting via `groot.service` (Restart=always). PID kill didn't work. Had to `systemctl stop + disable` the service.
- lawrenzo: same pattern — `lawrenzo.service` auto-restarted the standalone alongside `hermes-lawrenzo.service`
- wannabe: `wannabe.service` was the only bot running (no Hermes profile). Killing it took the bot offline entirely.

## Telegram Thread Management

When consolidating Telegram topics into a single thread (e.g. "ingloba tutti i thread in uno solo"):

1. Clean `channel_directory.json` on **ALL** profiles (not just gribbito)
2. Update **ALL** cron job `deliver` targets — both explicit thread refs and `origin`
3. Leave `local` deliveries alone (they don't touch Telegram)

Full procedure: `references/telegram-thread-consolidation.md`

**PITFALL**: Each profile has its own `channel_directory.json`. Updating only gribbito leaves 6 profiles pointing at stale threads. Tested 2026-05-29: had to batch-update all 7 profiles.

## Reference Files

- `references/systemd-service-mapping.md` — maps each bot to its old/old and Hermes systemd service names (as of 2026-05-28).
- `references/telegram-thread-consolidation.md` — step-by-step procedure for unifying Telegram thread delivery across all profiles and cron jobs.

## Batch Profile Updates

When updating multiple profiles (e.g., channel_directory.json, config changes), use `execute_code` with a loop instead of manual copy-paste:

```python
from hermes_tools import write_file
import json

# Example: update channel_directory.json on all profiles
data = {"entries": [...]}  # unified config
for profile in ["contabile", "lawrenzo", "wannabe", "groot", "designbro", "el-froggo", "ducato"]:
    write_file(f"<HERMES_ROOT>/profiles/{profile}/channel_directory.json", json.dumps(data, indent=2))
```

**Pitfall**: `execute_code` imports from `hermes_tools`, not Python stdlib. Use `from hermes_tools import write_file, read_file, terminal` etc.

### Deploying a Skill Across All Profiles

When [REDACTED — dati personali rimossi] says "applica X a tutti i profili" for a skill, follow this sequence:

1. **Check what exists**: scan target profiles for the skill directory
2. **Copy skill directory**: SKILL.md + `scripts/` + `references/` + `templates/`
3. **Make scripts profile-agnostic**: if a script hardcodes a profile path (e.g., `env_path = '<HERMES_ROOT>/profiles/gribbito/.env'`), either:
   - Accept profile as CLI argument (preferred — one shared script)
   - Create per-profile copies with hardcoded paths
4. **Check credentials**: verify required credential files exist in each target profile (e.g., `.env` tokens, OAuth JSON). Don't assume they're shared.
5. **Verify**: run a `--check` or equivalent on at least one target profile

```python
import os, shutil

profiles = ['el-froggo', 'contabile', 'lawrenzo', 'groot', 'wannabe', 'designbro', 'ducato']
base = '<HERMES_ROOT>/profiles'
src = os.path.join(base, 'gribbito', 'skills', 'category', 'skill-name')

# Read source files
with open(os.path.join(src, 'SKILL.md')) as f:
    skill_content = f.read()

for p in profiles:
    dest = os.path.join(base, p, 'skills', 'category', 'skill-name')
    os.makedirs(os.path.join(dest, 'scripts'), exist_ok=True)
    with open(os.path.join(dest, 'SKILL.md'), 'w') as f:
        f.write(skill_content)
    # Copy scripts, references, templates...
```

**Pitfall — `skill_manage` does NOT support cross-profile edits.** `skill_manage(action='patch'|'edit'|'create')` only works for skills in the active profile. To edit another profile's SKILL.md, use the `write_file` tool with `cross_profile=True` directly on the file path. The cross-profile write guard will block by default — pass `cross_profile=True` only after the user explicitly directs you to edit another profile. Tested 2026-05-29: installed `image-viz` skill on designbro from gribbito session using `write_file(cross_profile=True)`.

**Pitfall — `write_file(cross_profile=True)` is the only reliable cross-profile skill install.** `patch` tool with `cross_profile=True` also works for targeted edits. `terminal()` bypasses the guard entirely but is less clean. Prefer `write_file` for full file creation, `patch` for surgical edits. Both require explicit user direction. Tested 2026-05-29.

**Pitfall**: Google OAuth tokens are profile-scoped. Each profile needs its own `google_token.json` — copying from another profile won't work if that token is also expired. The `google_client_secret.json` CAN be shared. Always run `setup.py --check` after deploying google-workspace to verify auth status.

**Pitfall**: Skills that require auth (google-workspace, xurl, spotify, etc.) are NOT ready just because the SKILL.md and scripts are copied. Each profile needs its own credential setup. After deploying an auth-dependent skill, always run the skill's auth check command (e.g. `setup.py --check`, `xurl auth status`) on the target profile. If auth fails, walk the user through the OAuth flow for that specific profile. Tested 2026-05-29: deployed google-workspace to groot, token was expired, required full re-auth via browser flow.

**Pitfall — `cross_profile=True` required for skill writes**: `write_file` and `skill_manage(action='create')` are blocked by the cross-profile soft guard when targeting another profile's skills directory. You MUST pass `cross_profile=True` to `write_file`. The `skill_manage` tool does NOT accept `cross_profile` — it only edits the active profile's skills. For deploying skills to other profiles, use `write_file(path, content, cross_profile=True)`. Tested 2026-05-29: deploying image-viz skill to designbro.

**Pitfall — heredoc with `&` in terminal**: `cat > file << 'EOF'` blocks containing `&` (ampersand) get interpreted as background operators by the terminal tool, causing the command to fail or be flagged for approval. Use `write_file` tool instead of terminal heredocs when the content contains `&`. Tested 2026-05-29.

**Pitfall — OAuth code exchange varies by tool**: Google OAuth allows manual code exchange after the fact (`setup.py --auth-code "the_code"`). xurl OAuth does NOT — the callback must hit the running xurl process in real-time (PKCE verifier is held in memory, no `--auth-code` equivalent). If port 8080 cannot be opened on the VPS, the only option for xurl is having the user SSH in and run `xurl auth oauth2 --app NAME` directly. Tested 2026-05-29: spent 6 attempts trying to make xurl remote OAuth work before realizing the port was blocked.

## Adding MCP Servers to a Profile

MCP servers are profile-level config. Each profile has its own `mcp_servers:` section in `config.yaml`. Adding to one profile does NOT make it available in others.

### From npm/npx (most common)

```bash
hermes mcp add server-name -p <profile> --command npx --args '-y' --args '@scope/package-name'
```

### From local code (GitHub clone)

```bash
# 1. Clone the repo
git clone https://github.com/org/repo.git /opt/repo-name
cd /opt/repo-name && npm install

# 2. Add to profile
hermes mcp add server-name -p <profile> --command node --args /opt/repo-name/index.js
```

### Verifying

```bash
hermes mcp list -p <profile>        # list configured servers
hermes mcp test <name> -p <profile> # test connection + discover tools
```

**PITFALL**: `hermes mcp add` requires interactive Y/N confirmation to enable discovered tools. There is no `--yes` flag. For non-interactive usage, pipe stdin: `echo "Y" | hermes mcp add ...`. Tested 2026-05-30.

**PITFALL**: MCP servers added to `~/.hermes/config.yaml` (default profile) are NOT visible in profiles that define their own `mcp_servers:` section. Profile-level config replaces default config entirely for that key. Always add MCP servers to the specific profile that needs them. Tested 2026-05-29.

### Adding MCP HTTP Servers Manually

For MCP servers using HTTP transport (e.g. RootAI/Edge, remote endpoints), edit `config.yaml` directly. The `hermes mcp add` CLI is designed for stdio (npx/node) servers.

```yaml
# In the profile's config.yaml, under mcp_servers:
mcp_servers:
  openalice:
    url: http://127.0.0.1:47332/mcp
    enabled: true
  edge:                              # <-- add new server here
    url: https://mcp.rootai.wtf/mcp
    enabled: true
    transport: http
```

**PITFALL — sed inserts in wrong sections**: Using `sed -i '/pattern/a\new_line' config.yaml` to add MCP servers can match the same pattern in MULTIPLE sections (e.g. `enabled: true` appears in mcp_servers, tts, stt, plugins, etc.). This caused 4 duplicate Edge MCP blocks in Ducato's config. Fix: use Python to surgically insert only in the `mcp_servers:` section, or use sed with address ranges that constrain to the correct block:
```bash
sed -i '/^mcp_servers:/,/^[a-z]/ { /^  openalice:/,/^[a-z]/ { /^    enabled: true$/a\  edge:\n    url: https://mcp.rootai.wtf/mcp\n    enabled: true\n    transport: http } }' config.yaml
```
Tested 2026-05-31: had to clean up 3 duplicate blocks with Python after bad sed insertion.

**PITFALL**: The default MCP transport is `stdio` (runs a local command). For remote HTTP endpoints, you MUST specify `transport: http`. Without it, Hermes tries to spawn a local process and fails. Tested 2026-05-31: Edge MCP on Ducato.

### Inter-Bot GOAL.md Target Management

All bots' GOAL.md files contain a `Target bots:` line listing every other bot. When adding a new bot to the fleet, update ALL existing GOAL.md files:

```bash
cd <HERMES_ROOT>/profiles && for bot in contabile lawrenzo wannabe groot designbro el-froggo ducato; do
  f="$bot/GOAL.md"
  if grep -q "Target bots:" "$f" 2>/dev/null; then
    if grep -q "newbot" "$f" 2>/dev/null; then
      echo "✅ $bot: already has newbot"
    else
      sed -i 's/el-froggo/el-froggo, newbot/' "$f"
      echo "✅ $bot: added newbot"
    fi
  fi
done
```

Also create a GOAL.md for the new bot with matching structure (Inter-Bot Connections + Bus section). Use existing GOAL.md as template.

**PITFALL**: The `Target bots:` line grows over time. Keep alphabetical-ish ordering. The bus-send.py script accepts any bot name — no registration needed. Tested 2026-05-31: added Ducato and Sentinel to all 7 bots.

## Telegram Bot Token Rotation

When [REDACTED — dati personali rimossi] provides a new Telegram bot token for a profile:

1. **Find the `.env`**: `~/.hermes/profiles/<name>/.env` — look for `TELEGRAM_BOT_TOKEN=`
2. **Patch the token**: use the `patch` tool to replace the old value with the new one
3. **Restart the gateway**:
   ```bash
   # Check current status
   hermes gateway status --profile <name>
   
   # If running, it will pick up .env changes on restart
   # Use background mode (hermes gateway restart tends to timeout)
   hermes gateway run --profile <name>   # with terminal(background=true)
   ```
4. **Verify**: `hermes gateway status --profile <name>` — confirm PID is live

**PITFALL**: `hermes gateway restart --profile <name>` often times out (180s+). `hermes profile restart <name>` doesn't exist. Preferred approach: `systemctl restart hermes-<name>` and verify with `systemctl status hermes-<name>` after 5s. Tested 2026-05-29.

**PITFALL**: Don't paste the token in chat responses — it's a secret. Acknowledge the update without echoing the full token.

## Pitfalls

- **Don't delete profiles that cron jobs reference** — check `hermes cron list` first
- **Don't rename a profile while its gateway is running** — stop it first
- **SOUL.md changes ARE instant** — SOUL.md is loaded fresh each message. However, after bulk edits (personality rewrites, multi-file updates), restarting the gateway ensures clean state. Use `systemctl restart hermes-<profile>.service` — NOT `hermes gateway restart -p <profile>` which tends to timeout (180s+). Tested 2026-05-28: gateway restart picked up new personalities correctly.
- **`hermes gateway restart` timeout** — The `hermes gateway restart -p <profile>` command frequently times out after 180s. Preferred: `systemctl restart hermes-<profile>`. Check with `systemctl status hermes-<profile>` after 5s. Tested 2026-05-29: el-froggo restart timed out via hermes CLI but worked instantly via systemctl.
- **`hermes profile restart` doesn't exist** — There is no `hermes profile restart` command. The valid subcommands are: list, use, create, delete, describe, show, alias, rename, export, import, install, update, info. Use `systemctl restart` instead. Tested 2026-05-29.
- **Shared resources** — some things (like xurl credentials in `~/.xurl/`) are global across profiles. Renaming a profile doesn't break these.
- **Session JSONs are historical** — never mass-rename in `/sessions/` directories. They're logs, not config.
- **Hermes auto-recreates profile dirs** — if you `rm -rf` a profile while Hermes is running, empty dirs may reappear. Harmless but confusing.
- **Cross-profile skill references** — skills in one profile may reference another profile's name. Always grep across ALL profiles when renaming.
- **Consolidation: use `cp -rn`** — `cp -r` without `-n` overwrites existing skills in the target. If the target already has a skill with the same name, it's probably newer/better. Use no-clobber.
- **Consolidation: merge .env carefully** — source and target often share the same API keys but with different values. Target's values usually win since it's the primary profile.
- **Consolidation: preserve persona before deleting** — if the source profile has a distinct identity, save it as a skill under the target BEFORE deleting the source. Once `rm -rf` runs, the GOAL.md and persona knowledge is gone. Tested 2026-05-28: had to restore el-froggo from scratch after merging it — all files had to be recreated from conversation history since the originals were deleted.
- **NEVER merge product-level bots** — If a profile has its own Telegram bot token, external social accounts (X, etc.), customer-facing offerings, or distinct audience, it is a SEPARATE PRODUCT, not a merge candidate. [REDACTED — dati personali rimossi] corrected this when I merged el-froggo into gribbito (2026-05-28): el-froggo has its own Telegram bot, @FroggoEl18782 on X, Virtuals Protocol offerings, and independent cron jobs. Merging destroyed the gateway, cron jobs, and bot token routing. Restoration required recreating the entire profile from conversation history. Only merge "utility" profiles that serve [REDACTED — dati personali rimossi] directly with no external-facing identity.
- **Consolidation: rewrite SOUL.md, don't append** — a merged SOUL.md should read as one cohesive identity, not concatenated fragments from multiple profiles.
- **Cross-profile cron delivery** — When a cron job runs under a profile (e.g. `wannabe`) that doesn't have telegram configured, `deliver: "telegram:chat_id:thread_id"` fails with "platform 'telegram' not configured/enabled". Use `deliver: "origin"` instead — it routes output back through the originating profile's configured channels. Tested 2026-06-06: linkedin-content-calendar under wannabe had this exact failure.
- **Cron script paths: NO symlinks** — The `script` field in `no_agent=True` cron jobs must be a real file in `~/.hermes/scripts/`. Symlinks that resolve outside the scripts directory are blocked ("script path escapes the scripts directory via traversal"). Absolute paths are also rejected ("Script path must be relative to ~/.hermes/scripts/"). Always `cp` scripts, never `ln -s`. Tested 2026-06-06: knowledge-sync, skill-sync, session-digest all failed due to symlinks to `<HERMES_ROOT>/shared/scripts/`.
