---
name: shared-knowledge-protocol
description: >
  Shared Knowledge Layer — fleet-wide memory for all Hermes bots.
  Solves the "agents as strangers" problem: facts, decisions, preferences
  propagate across all profiles via <HERMES_ROOT>/shared/knowledge/.
triggers:
  - "shared knowledge"
  - "fleet memory"
  - "cross-bot knowledge"
  - "knowledge sync"
  - "remember across bots"
---

# Shared Knowledge Protocol

## Overview

Every Hermes bot shares a common knowledge layer at `<HERMES_ROOT>/shared/knowledge/`. This ensures that when one bot learns something, all bots benefit.

## Architecture

```
<HERMES_ROOT>/shared/knowledge/
├── facts.md            # Stable facts about [REDACTED — dati personali rimossi], environment, business
├── decisions.md        # Key decisions with reasoning (not just outcomes)
├── preferences.md      # User preferences discovered by any bot
├── gold-examples.md    # Exemplary outputs that set the quality bar (NEW 2026-06-07)
├── ownership.md        # Bot ownership map, escalation rules, decision authority matrix
├── feedback.md         # Feedback loops and outcome tracking
├── market-context.md   # Market intelligence and competitive context
├── conversations.md    # Auto-generated summary of recent conversations (every 2h)
├── shared-facts.md     # Legacy shared facts (pre-migration)
├── digests/            # Daily session digests (auto-generated)
├── FRANK-README.md     # Frank's integration guide
└── (auto-synced to each profile's shared-knowledge.md)
```

**Sync priority**: Core files (facts, decisions, preferences) are always included in full. Conversations.md is supplementary — truncated to fit within 8,000 char budget.

**Knowledge maturity model** (maps to agent-knowledge tweet framework):
1. Source-of-truth → facts.md ✅
2. Workflows/SOPs → skills (64+ in GBrain + Hermes) ✅
3. Gold examples → gold-examples.md + gold-example-log.py ✅
4. Decision logs → decisions.md + decision-log.py ✅
5. Ownership map → ownership.md (bot→vertical→scope→escalation + authority matrix) ✅
6. Customer context → market-context.md + customer-log.py ✅
7. Permissions/boundaries → ownership.md escalation rules ✅
8. Feedback loops → feedback.md + feedback-log.py ✅

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `knowledge-sync.py` | Copy shared knowledge to all profiles | Runs every 30min via cron |
| `fact-log.py` | Add a fact | `python3 fact-log.py <bot> "<fact>" [section]` |
| `decision-log.py` | Add a decision | `python3 decision-log.py <bot> "<decision>" "<reasoning>" [category]` |
| `preference-log.py` | Add a preference | `python3 preference-log.py <bot> "<preference>" [category]` |
| `gold-example-log.py` | Log an exemplary output | `python3 gold-example-log.py <bot> "<category>" "<description>" "<why_good>" ["<file_path>"]` |
| `customer-log.py` | Log customer intelligence | `python3 customer-log.py <bot> "<type>" "<target>" "<note>"` — types: feedback, competitor, sales, win, loss, pain, segment |
| `feedback-log.py` | Log outcomes/lessons | `python3 feedback-log.py <bot> "<type>" "<description>" "<detail>"` — types: worked, failed, lesson, correction, metric, qa |
| `skill-sync.py` | Sync skills from gribbito to all profiles | Runs every 6h via cron |
| `session-digest.py` | Extract insights from sessions | Runs daily at 23:00 via cron |
| `conversation-summary.py` | Summarize recent conversations | Runs every 2h via cron |
| `frank-knowledge.sh` | Wrapper for Frank to read/write knowledge | `frank-knowledge.sh read/fact/decision/preference` |

All scripts are at `<HERMES_ROOT>/shared/scripts/`.

## How to Use (per bot)

### At session start
The bot's context automatically includes `shared-knowledge.md` (synced every 30min). No action needed.

### During a session — when you learn something

**New fact about [REDACTED — dati personali rimossi] or the environment:**
```
python3 <HERMES_ROOT>/shared/scripts/fact-log.py <your_bot_name> "[REDACTED — dati personali rimossi] prefers X" "User ([REDACTED — dati personali rimossi])"
```

**New preference discovered:**
```
python3 <HERMES_ROOT>/shared/scripts/preference-log.py <your_bot_name> "Always use dark theme" "Technical"
```

**Key decision made:**
```
python3 <HERMES_ROOT>/shared/scripts/decision-log.py <your_bot_name> "Use SQLite for X" "VPS constraints" "Architecture"
```

**Exceptional output produced (gold example):**
```
python3 <HERMES_ROOT>/shared/scripts/gold-example-log.py <your_bot_name> "<category>" "<description>" "<why_good>" ["<file_path>"]
```
Categories: Copy & Messaging, Landing Pages & Design, Code & Technical, Client Communication, Strategy & Analysis, Reports & Documentation
When to log: [REDACTED — dati personali rimossi] says "perfetto"/"esattamente"/"questo sì", a mail converts, a post performs, copy that works, clean reusable code patterns.
Before writing copy/pages/code/comms — CHECK gold-examples.md for reference examples first.

**Customer intelligence (feedback, competitor intel, sales notes, win/loss):**
```
python3 <HERMES_ROOT>/shared/scripts/customer-log.py <your_bot_name> "<type>" "<target>" "<note>"
```
Types: feedback, competitor, sales, win, loss, pain, segment
Subsections: Positive Signals, Pain Points, Churn Reasons, Win Notes (auto-mapped by type)

**Feedback loop (what worked, what failed, lessons, corrections):**
```
python3 <HERMES_ROOT>/shared/scripts/feedback-log.py <your_bot_name> "<type>" "<description>" "<detail>"
```
Types: worked, failed, lesson, correction, metric, qa
When to log: after completing significant work, when [REDACTED — dati personali rimossi] corrects output, when a pattern repeats (good or bad).

### Direct script calls (preferred)
Call the logger scripts directly during a session. Writes are immediate.

```bash
# Example: ContAIbile discovers a preference
python3 <HERMES_ROOT>/shared/scripts/preference-log.py contabile "[REDACTED — dati personali rimossi] wants F24 in PDF format" "Technical"
```

## Sections / Categories

**Facts:** User ([REDACTED — dati personali rimossi]), Environment, Business, Technical
**Decisions:** Architecture, Business, Security, Workflow, Infrastructure, Marketing
**Preferences:** Communication, Work Style, Technical

## Cron Jobs

| Job | Schedule | Script |
|-----|----------|--------|
| `knowledge-sync` | every 30m | `knowledge-sync.py` |
| `skill-sync` | `0 */6 * * *` | `skill-sync.py` |
| `session-digest` | `0 23 * * *` | `session-digest-all.py` |
| `conversation-summary` | every 2h | `conversation-summary.py` |

## Rules

1. **Read shared-knowledge.md at session start** — it's auto-injected, just use it
2. **Write when you learn** — don't wait, log facts/decisions/preferences immediately
3. **Don't duplicate** — check if the fact already exists before logging
4. **Include reasoning** for decisions — not just the outcome
5. **Use the right category** — helps other bots find relevant knowledge
6. **Gribbito is source of truth for skills** — skills sync FROM gribbito TO all others
7. **Call scripts directly** — no need for bus messages, just run the Python scripts

## Frank Integration

Frank is a Hermes profile at `<HERMES_ROOT>/profiles/frank/` with Telegram bot `@FrankkkkbbbbBOt`.

**Profile structure:**
- `config.yaml` — model: mimo-v2.5-pro via OpenGateway
- `GOAL.md` — handles bus messages from gribbito, sentinel, machiavelli
- `.env` — BOT_TOKEN, ADMIN_CHAT_ID, OPENGATEWAY_KEY
- Bus inbox: `<HERMES_ROOT>/shared/bus/inbox/frank/`

**Communication channels:**
- Bus messaging: ✅ (send via `bus-send.py send <from> frank "msg"`)
- Shared knowledge: ✅ (read/write to `<HERMES_ROOT>/shared/knowledge/`)
- Telegram: ✅ (responds to [REDACTED — dati personali rimossi] directly at chat_id <ADMIN_CHAT_ID>)

**⚠️ Critical gap (as of 2026-06-01):** Frank (and other bots) have bus inboxes but NO cron job or hook to poll them. Messages land in the inbox directory but the bot never reads them unless a session explicitly calls `bus-send.py check frank`. To fix: create a cron job that polls the inbox — see `references/bus-inbox-polling.md`.

## Pitfalls

- `fact-log.py` and friends use shell escaping — avoid quotes inside the fact text
- Knowledge files are markdown — don't break the format with malformed entries
- Session digest reads from `state.db` — if a profile has no sessions, no digest is generated
- Skills synced from gribbito get a `.skill-sync-hash` marker — user-customized skills (without marker) are never overwritten
- **Memory limit**: MEMORY.md is capped at 2,200 chars. At 99%+, consolidate before adding. The shared knowledge layer exists precisely to avoid stuffing everything into per-profile memory.
- **Action over interrogation**: When [REDACTED — dati personali rimossi] gives an ambiguous instruction (short word like "Al", unclear target), try executing with the best interpretation first rather than asking multiple clarifying questions. Ask ONCE at most. If no match, do the task with available resources. "Stop" = stop asking, start doing. [REDACTED — dati personali rimossi] gets frustrated when the agent keeps asking instead of acting.
- **Gribbito is source of truth for skills**: skill-sync only goes FROM gribbito TO others. If another bot creates a skill, manually copy it to gribbito first.
- **Cron script path**: `no_agent=True` cron jobs look for scripts in `~/.hermes/scripts/` (NOT `~/.hermes/profiles/<profile>/scripts/` and NOT `<HERMES_ROOT>/shared/scripts/`). Symlinks are BLOCKED — the cron system resolves them and rejects any that escape the scripts directory ("script path escapes the scripts directory via traversal"). Absolute paths are also rejected. FIX: `cp` the script to `~/.hermes/scripts/` as a real file, then reference just the filename in the cron job. Example: `cp <HERMES_ROOT>/shared/scripts/knowledge-sync.py ~/.hermes/scripts/knowledge-sync.py`. Also, the `script` field must be ONLY the filename — no `python3` prefix, no arguments. If you need args, create a wrapper `.sh` script. Tested 2026-06-06: all 5 shared-knowledge cron jobs were broken by symlinks.
- **SQLite session schema**: `sessions.started_at` is REAL (epoch), not ISO string. `messages.role` is 'user'/'assistant'/'tool'. Filter `role IN ('user', 'assistant')` to skip tool noise. See `references/session-db-schema.md`.
- **Knowledge sync budget**: MAX_CHARS=8000. Core files (facts, decisions, preferences) always included in full. Conversations.md truncated to fit. If core exceeds budget, conversations are dropped entirely.
- **Verify before building**: When asked to create knowledge infrastructure (new files, new scripts), CHECK if the file/script already exists first. `gold-examples.md` and `ownership.md` both existed before being "created" — the template was there but empty. Always `ls` + `cat` before writing. Don't duplicate structure that's already in place.
- **Gold examples are READ, not just written**: Before drafting copy, landing pages, code patterns, or client comms — CHECK gold-examples.md for reference examples. The value is in the consumption, not just the logging.
- **Search engines block VPS IPs**: DuckDuckGo (`duckduckgo_search` package) often returns empty results from VPS. Google/Bing/Brave trigger CAPTCHAs in browser. For finding specific tweets or web content: try `curl` against FxTwitter API (`https://api.fxtwitter.com/status/{id}`), use `xurl search` if configured, or ask the user for the URL/handle directly. Don't burn 5+ attempts on search engines that are blocking you — pivot fast.
- **Twitter thread → article research pattern**: When a tweet references an article/thread: (1) FxTwitter API for tweet text + quote, (2) extract article URL from tweet, (3) `web_extract` the article, (4) look for author's GitHub via `github.com/{handle}` or web search `site:github.com {author_name}`, (5) if no GitHub found, check author's linked sites for repos/docs. Don't assume the author has a GitHub — many content creators don't.

## References

- `references/implementation-details.md` — data flow diagrams, file formats, script internals, cron schedule
- `references/session-db-schema.md` — SQLite schema for Hermes session/message tables, query patterns
- `references/inter-bot-communication-models.md` — bus messaging vs shared knowledge, communication matrix, Frank limitations
- `references/eval-loop.md` — 6-step eval loop methodology (gold standards → judge skill → test suite → regression → production monitoring). Extends the knowledge maturity model with quality gating.
