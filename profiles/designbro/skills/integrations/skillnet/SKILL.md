---
name: skillnet
description: |
  Search, install, and evaluate AI agent skills from SkillNet's 500K+ community library.
  Use when: you need a skill that doesn't exist locally, want to discover community best practices,
  or need to evaluate skill quality before installing. Complements local Hermes skills with
  community knowledge. Works via CLI (skillnet command) and MCP tools (mcp_skillnet_*).
metadata:
  hermes:
    tags: [skills, marketplace, evaluation, discovery, integrations]
    related_skills: [hermes-agent-skill-authoring, gepa-skill-evolution]
---

# SkillNet — Community Skill Search & Install

Search 500K+ community skills from SkillNet. Install with one command. Evaluate quality before deploying.

## When to Use

- User asks for a capability that doesn't exist as a local skill
- Curator needs to find community skills as fallback
- You want to evaluate a skill's quality before installing
- You need to discover best practices for a specific domain
- Research phase: what skills exist for X?

## Prerequisites

- `skillnet` CLI installed via pip (`pip install --break-system-packages skillnet-ai`)
- MCP server `skillnet` configured in config.yaml (node /opt/skillnet-mcp/index.js)
- No API key needed for search & download
- API key needed only for create/evaluate/analyze (optional)

## Quick Reference

### Search (CLI)

```bash
# Keyword search
skillnet search "pdf extraction" --limit 5

# Semantic search (AI-powered)
skillnet search "analyze financial reports" --mode vector --threshold 0.8

# Filter by category
skillnet search "web scraping" --category Development --sort-by stars
```

### Search (MCP — prefer this in agent context)

```
mcp_skillnet_search_skills: { q: "pdf extraction", limit: 5 }
mcp_skillnet_search_skills: { q: "analyze charts", mode: "vector", threshold: 0.8 }
```

### Import Best Skill (MCP)

```
mcp_skillnet_import_best_skill: { topic: "pdf parsing" }
```

This searches, picks the highest-rated skill, downloads it, and returns full content.

### Download & Install

```bash
# From GitHub URL
skillnet download "https://github.com/anthropics/skills/tree/main/skills/skill-creator" --target-dir ~/.hermes/profiles/gribbito/skills/community/

# Via MCP
mcp_skillnet_download_skill: { url: "https://github.com/...", target_dir: "~/.hermes/profiles/gribbito/skills/community/" }
```

### Get Rules Only (MCP — token-friendly)

```
mcp_skillnet_get_skill_rules: { url: "https://github.com/..." }
```

Extracts only rules/instructions, no boilerplate. Good for quick assessment.

### Evaluate Quality (5D)

```bash
# CLI
skillnet evaluate "https://github.com/anthropics/skills/tree/main/skills/skill-creator"

# MCP
mcp_skillnet_evaluate_skill: { target: "/path/to/local/skill" }
```

Returns: Safety, Completeness, Executability, Maintainability, Cost-Awareness — each rated Good/Average/Poor.

### Analyze Relationships

```bash
# CLI
skillnet analyze ~/.hermes/profiles/gribbito/skills/

# MCP
mcp_skillnet_analyze_skills: { skills_dir: "~/.hermes/profiles/gribbito/skills/" }
```

Discovers: similar_to, belong_to, compose_with, depend_on relationships.

## 5D Evaluation — Quality Gate

Before installing any community skill, evaluate it:

| Dimension | What it checks | Red flags |
|---|---|---|
| Safety | Destructive actions, safeguards, scope limits | Dangerous ops without guards |
| Completeness | Steps, inputs/outputs, edge cases | Missing core steps, vague |
| Executability | Can agent actually run this? | Non-actionable, unspecified deps |
| Maintainability | Modularity, coupling, adaptability | Overly broad, tight coupling |
| Cost-Awareness | Time/compute/money mindfulness | Wasteful, no limits |

**Rule: Never install a community skill with any dimension rated "Poor" without manual review.**

See `references/5d-evaluation.md` for full criteria and decision matrix.

## Curator Integration

When the Curator finds no local skill for a task:

1. Search SkillNet with `mcp_skillnet_search_skills`
2. Pick top result by stars + evaluation
3. Get rules with `mcp_skillnet_get_skill_rules` (token-efficient)
4. If rules look good, download with `mcp_skillnet_download_skill`
5. Install to `~/.hermes/profiles/gribbito/skills/community/`
6. Skill becomes available in next session

## Categories

SkillNet organizes skills into:
- Development, AIGC, Research, Science, Productivity, Security, DevOps

Use `--category` filter to narrow results.

## Competitive Landscape

See `references/competitive-landscape.md` for the current map of AI agent infrastructure
projects (PAI, ODEI, AutoGPT, etc.), vaporware detection checklist, and Hermes capability mapping.
Use when [REDACTED — dati personali rimossi] shares an external project link asking "is this better?"

## Pitfalls

- **Quality varies wildly**: Community skills range from excellent to garbage. Always evaluate before installing.
- **Stars ≠ quality**: Popular skills may not fit your use case. Check evaluation scores.
- **Vaporware is common**: Many "AI agent" GitHub orgs publish beautiful READMEs and landing pages with zero actual code. Always check commit count, contributor count, and install path before recommending. See `references/competitive-landscape.md` for the detection checklist.
- **Don't list features — give a verdict**: When [REDACTED — dati personali rimossi] asks "is X better?", he wants a direct adopt/watch/skip recommendation, not a feature comparison table. Lead with the answer.
- **`skillnet evaluate` requires a real OpenAI API key**: The `evaluate`, `create`, and `analyze` commands use the OpenAI SDK and hit `api.openai.com` by default. Proxy providers (OpenGateway, LiteLLM, etc.) return 401 or connection errors. The `BASE_URL` env var is supported but proxy compatibility is poor. **Workaround**: Use the prompt-based evaluation script (`scripts/evaluate_skill_prompt.py`) which uses the agent's own LLM instead.
- **Search/download work without API key**: `skillnet search` and `skillnet download` use the public SkillNet REST API and need no credentials.
- **`skillnet` CLI installed via pip**: `pip install --break-system-packages skillnet-ai` (v0.0.18). Lives in `~/.local/bin/skillnet`. PEP 668 blocks bare `pip install` on Debian/Ubuntu — use `--break-system-packages` flag. The MCP server (node) works independently but health check + evaluate/create/analyze tools require the CLI.
- **Install location**: Always install to `skills/community/` subdirectory to keep community skills separate from custom ones.
- **MCP tools need restart**: After adding MCP server config, restart the agent/session to discover new tools.
- **MCP health check depends on CLI**: `mcp_skillnet_health_check` and the evaluate/create/analyze tools spawn the `skillnet` CLI as a subprocess. If the CLI isn't installed, you get `spawn skillnet ENOENT`. Search and download tools work fine without it (they use the node HTTP client directly).
- **CLI vs MCP**: Prefer MCP tools in agent context (they return structured JSON). Use CLI for manual exploration.
- **`os.path.expanduser("~")` breaks under cron**: When scripts run as cron jobs in the gribbito profile, `HOME` resolves to the wannabe profile's home (`<HERMES_ROOT>/profiles/wannabe/home`), not `/root`. Any script using `Path(os.path.expanduser("~/.hermes/..."))` will produce a nonexistent path and silently find zero results. **Fix**: Use absolute paths (`Path("<HERMES_ROOT>/profiles/gribbito/skills")`) in all scripts that may be invoked by cron. This applies to `quality_report_cron.py`, `evaluate_skills.py`, and any future cron-targeted scripts.
