# AI Agent Infrastructure — Competitive Landscape

Last updated: 2026-05-30

When [REDACTED — dati personali rimossi] shares an external project link asking "is this better?", use this as
a quick-reference map plus the evaluation checklist below.

## Tier 1 — Production-ready, actively maintained

| Project | Stars | What it is | Overlap with Hermes |
|---|---|---|---|
| **PAI** (danielmiessler/Personal_AI_Infrastructure) | 14.5K | Life OS: 45 skills, 171 workflows, Pulse dashboard, DA identity, ISA framework, Algorithm v6.3 | High — memory, skills, identity, goal-tracking. Biggest real competitor. |
| **SkillNet** (zjunlp/SkillNet) | 792 | 500K+ community skill marketplace, search/install/evaluate | Medium — skill discovery. Already integrated via MCP. |
| **AutoGPT** | 170K+ | Autonomous agent loop | Low — different philosophy (autonomous vs personal) |
| **LangGraph** | 10K+ | Agent orchestration framework | Low — framework, not personal OS |

## Tier 2 — Promising but early

| Project | Stars | What it is | Status |
|---|---|---|---|
| **ODEI** (odei-ai) | 0 | "Personal AI Operating System" — World Model graph, governance loop, 7-layer model | Vaporware. All repos created 2026-05-26, 1 commit each, zero code. Nice website (api.odei.ai) with 3D World Model visualization. Only 1 contributor (Zer0H1ro, Budapest). |

## Vaporware Detection Checklist

When evaluating any external project, check ALL of these before recommending:

1. **Code exists?** — Look for actual source files, not just README/LICENSE/SECURITY.md
2. **Commit history** — 1-2 commits = showcase, not software. Look for 50+ commits
3. **Stars/forks** — 0 stars + 0 forks + < 1 week old = not worth integrating
4. **Contributors** — 1 person = risk. Look for 3+ active contributors
5. **Install path** — Can you `pip install`, `npm install`, or `curl | bash`? If not, it's a concept
6. **Issues/PRs** — Real projects have open issues and merged PRs
7. **"Intentionally minimal"** — This phrase in a README is a red flag. It means "we haven't built it yet"

## Hermes vs The Field — What We Already Have

Hermes's architecture already covers much of what these projects promise:

| Capability | Hermes equivalent | Notes |
|---|---|---|
| World Model / Knowledge Graph | memory.md + session_search + Curator | Text-based, searchable, persistent |
| Governance Loop | SOUL.md + cron jobs + skill lifecycle | Observe→Decide→Act→Verify via cron |
| Skill System | SKILL.md + community/ + GEPA optimization | More mature than most competitors |
| Identity / DA | Profile system (8 profiles) + SOUL.md | Per-bot personality + tools |
| Goal Tracking | todo tool + key-decisions skill + plans/ | Manual but functional |
| Memory Consolidation | Curator (7d check, 30d stale, 90d archive) | Automated lifecycle |

## Evaluation Protocol for "Is This Better?"

When [REDACTED — dati personali rimossi] asks about an external project:

1. Check the repo — real code or vaporware?
2. Check stars/activity/contributors — is anyone using it?
3. Check install path — can we run it today?
4. Map to Hermes capabilities — what would we gain?
5. Give honest verdict: adopt / watch / skip

**Always give a direct verdict, not a feature list.** [REDACTED — dati personali rimossi] wants to know if it's worth his time.
