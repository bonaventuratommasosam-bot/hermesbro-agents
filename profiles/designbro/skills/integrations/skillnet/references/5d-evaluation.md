# 5D Evaluation Criteria — SkillNet

Reference for evaluating community skills before installation.

## Dimensions

### 1. Safety
- **Good**: Destructive actions avoided by default, safety checks present, scope limits defined
- **Average**: Some safeguards but gaps exist
- **Poor**: Dangerous actions without safeguards, encourages unsafe tool usage

**Special rules:**
- If `allowed_tools` grants broader permissions than needed → reduce by 1 level
- Health/medical skills without disclaimers → max Average

### 2. Completeness
- **Good**: Clear goal + steps + I/O, prerequisites mentioned, edge cases covered
- **Average**: Mostly complete but missing some details
- **Poor**: Too vague, missing core steps, unclear what "done" means

**Special rules:**
- Missing input validation → at most Average
- Critical formula errors → usually Poor
- Placeholder-only implementations → usually Poor

### 3. Executability
- **Good**: Concrete actions/artifacts, minimal ambiguity, scripts run successfully
- **Average**: Mostly executable with minor issues
- **Poor**: Non-actionable steps, depends on unspecified systems

**Special rules:**
- No scripts ≠ Poor for instruction-only skills
- Placeholder arguments in scripts → prefer Average
- Critical code errors → must be Poor
- Trivially successful scripts (echo/print only) → not strong evidence

### 4. Maintainability
- **Good**: Narrow modular scope, clear I/O, low coupling, configurable
- **Average**: Reasonable but could be cleaner
- **Poor**: Overly broad, tightly coupled, unclear adaptation path

### 5. Cost-Awareness
- **Good (lightweight)**: Inherently low-cost, no heavy operations
- **Good (heavy)**: Explicit batching/limits/caching/scope control
- **Average**: Acceptable cost profile
- **Poor**: Wasteful workflows without acknowledging limits

## Decision Matrix

| Safety | Completeness | Executability | Maintainability | Cost | Action |
|---|---|---|---|---|---|
| Good | Good | Good | Good | Good | ✅ Install directly |
| Good | Good | Good | Avg | Good | ✅ Install, minor tweaks |
| Any Poor | — | — | — | — | ⚠️ Manual review required |
| — | Poor | — | — | — | ⚠️ Likely skip |
| — | — | Poor | — | — | ⚠️ Won't work, skip |
| Avg | Avg | Avg | Avg | Avg | ⚠️ Usable but not ideal |

## Usage

```bash
# CLI
skillnet evaluate <url-or-path>

# MCP
mcp_skillnet_evaluate_skill: { target: "<url-or-path>" }
```

Returns JSON with each dimension: `{ "level": "Good|Average|Poor", "reason": "..." }`
