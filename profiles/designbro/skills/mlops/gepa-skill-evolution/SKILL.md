---
name: gepa-skill-evolution
description: >
  Use GEPA (Genetic-Pareto Prompt Evolution) to optimize Hermes Agent skills 
  offline. Evolves skills through execution traces, not GPU training. $2-10 per run.
version: 1.0.0
author: gribbito
tags: [gepa, optimization, skills, evolution, dspy]
triggers:
  - "optimize skill"
  - "evolve skill"
  - "GEPA"
  - "skill improvement"
  - "self-evolution"
---

# GEPA Skill Evolution

## Overview

GEPA (Genetic-Pareto Prompt Evolution) optimizes skills offline by reading execution traces and proposing targeted improvements. No GPU required. $2-10 per optimization run.

**Location**: `/root/hermes-agent-self-evolution/`
**Hermes repo**: `/usr/local/lib/hermes-agent/`

## Prerequisites

```bash
cd /root/hermes-agent-self-evolution
source .venv/bin/activate
export HERMES_AGENT_REPO=/usr/local/lib/hermes-agent
```

## How It Works

1. Read current skill from Hermes repo
2. Generate evaluation dataset (synthetic or from session history)
3. Run GEPA optimizer: read traces → find failures → generate variants
4. Evaluate with LLM-as-judge + rubrics
5. Constraint gates: 100% tests pass, skills <15KB, no semantic drift
6. Best variant → PR (never direct commit)

## Usage

### Evolve a Single Skill

```bash
cd /root/hermes-agent-self-evolution
source .venv/bin/activate

# Synthetic eval data (default)
python -m evolution.skills.evolve_skill \
    --skill [REDACTED — dati personali rimossi]-stack-manager \
    --iterations 10 \
    --eval-source synthetic

# Real session history
python -m evolution.skills.evolve_skill \
    --skill [REDACTED — dati personali rimossi]-stack-manager \
    --iterations 10 \
    --eval-source sessiondb
```

### Evolve Multiple Skills

```bash
# List available skills
ls ~/.hermes/profiles/gribbito/skills/

# Run evolution for each
for skill in [REDACTED — dati personali rimossi]-stack-manager hermes-profile-management marketing-materials-workflow; do
    python -m evolution.skills.evolve_skill \
        --skill $skill \
        --iterations 5 \
        --eval-source synthetic
done
```

## Evaluation Sources

- **synthetic**: Generates test cases via Claude Opus (default, works out of box)
- **sessiondb**: Uses real session history from SQLite (more accurate, needs sessions)
- **golden**: Hand-curated test sets (best quality, needs manual creation)

## Constraint Gates

Every evolved variant must pass:
- Full test suite: `pytest tests/ -q` must pass 100%
- Size limits: Skills ≤15KB
- Caching compatibility: No mid-conversation changes
- Semantic preservation: Must not drift from original purpose
- PR review: All changes go through human review

## Cost

- ~$2-10 per optimization run (API calls only)
- No GPU required
- Uses DSPy + GEPA engine

## When to Use

- When a skill has low performance or frequent errors
- After collecting 10+ sessions with the skill
- Before fine-tuning (RL/GRPO) — GEPA is cheaper
- When Curator flags a skill for improvement

## Pitfalls

- GEPA generates PRs, not direct commits — review before merging
- Synthetic eval data may not reflect real usage patterns
- Start with 5 iterations, increase if results are promising
- Always verify evolved skills still work with your specific setup

## References

- GitHub: https://github.com/NousResearch/hermes-agent-self-evolution
- Paper: ICLR 2026 Oral
- License: MIT
