# SkillSpector Integration Reference

NVIDIA SkillSpector — security scanner for AI agent skills. Detects 64 vulnerability patterns across 16 categories.

## Installation

```bash
cd /home/[REDACTED — dati personali rimossi]/ai-stack/agents/sentinel
git clone https://github.com/nvidia/skillspector.git
cd skillspector
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## JSON Output Field Mappings

SkillSpector's JSON output uses these field names (NOT what you'd expect):

```
skill.name          → skill name (NOT "skill_name")
skill.source        → source path
skill.scanned_at    → ISO timestamp
risk_assessment.score    → 0-100 risk score
risk_assessment.severity → CRITICAL|HIGH|MEDIUM|LOW
risk_assessment.recommendation → DO_NOT_INSTALL|INSTALL_WITH_CAUTION|SAFE_TO_INSTALL
components[]        → array of files (NOT "components_count")
  .path, .type, .lines, .executable, .size_bytes
issues[]            → array of vulnerabilities
  .id               → category (E1, E2, E3, EA2, MP2, etc.) (NOT "rule_id")
  .severity         → CRITICAL|HIGH|MEDIUM|LOW
  .message          → description (sometimes "title" instead)
  .location         → "file:line"
  .confidence       → 0-100
  .remediation      → fix suggestion
```

## Return Code Semantics

```bash
skillspector scan /path/to/skill --format json --no-llm
echo $?  # 0 = no issues, 1 = issues found, ≥2 = real error
```

**Critical**: Return code 1 is SUCCESS (issues found). Only treat ≥2 as failure.

```python
# Correct handling
if result.returncode not in [0, 1]:
    raise RuntimeError(f"SkillSpector failed: {result.stderr}")
```

## Subprocess Pattern (Python venv tools)

```python
cmd = f"source {venv_path}/bin/activate && skillspector scan {target} --format json --no-llm"
result = subprocess.run(
    ["bash", "-c", cmd],
    capture_output=True, text=True, timeout=300
)
```

**Pitfall**: Don't pass the command as a list `["bash", "-c", f"source..."]` with the source+skillspector as separate args — the whole thing must be one string after `-c`.

## LLM Provider Setup

### OpenAI (default)
```bash
export OPENAI_API_KEY=sk-***...
export SKILLSPECTOR_PROVIDER=openai
```

### Anthropic
```bash
export ANTHROPIC_API_KEY=sk-ant-***...
export SKILLSPECTOR_PROVIDER=anthropic
```

### NVIDIA Build
```bash
export NVIDIA_INFERENCE_KEY=nvapi-***...
export SKILLSPECTOR_PROVIDER=nv_build
```

### Local LLM (Ollama/vLLM)
```bash
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_API_KEY=ollama
export SKILLSPECTOR_PROVIDER=openai
```

## Vulnerability Categories (16)

| ID | Category | What it detects |
|----|----------|-----------------|
| E1 | External Transmission | Data sent to external URLs |
| E2 | Env Variable Harvesting | Reading sensitive env vars |
| E3 | File System Enumeration | Scanning filesystem beyond scope |
| EA2 | Autonomous Decision Making | No human-in-the-loop for destructive ops |
| MP2 | Context Window Stuffing | Padding/stuffing attack patterns |
| ... | + 11 more | See SkillSpector docs for full list |

## Risk Scoring

- **80-100 (CRITICAL)**: DO NOT INSTALL — prompt injection, data exfiltration, privilege escalation
- **60-79 (HIGH)**: DO NOT INSTALL — significant security concerns
- **40-59 (MEDIUM)**: INSTALL WITH CAUTION — review before use
- **20-39 (LOW)**: Minor issues, generally safe
- **0-19 (SAFE)**: No significant issues

## Sentinel Integration Files

```
/home/[REDACTED — dati personali rimossi]/ai-stack/agents/sentinel/
├── skill_scanner.py          # Core scanner (SkillScanner class)
├── sentinel_skill_guard.py   # Pre-install checks, watch mode, reports
├── scan-skill.sh             # Quick static scan wrapper
├── scan-skill-llm.sh         # LLM-enhanced scan wrapper
├── skill_scanner_config.env  # Configuration
├── skillspector/             # NVIDIA SkillSpector (git submodule)
└── reports/                  # Scan results (JSON)
```

## Example: Scan a GitHub Skill

```bash
# Static analysis (fast, no API key needed)
./scan-skill.sh https://github.com/user/skill --no-llm

# With LLM analysis (more accurate, needs API key)
./scan-skill-llm.sh https://github.com/user/skill --provider openai

# Generate JSON report
python3 skill_scanner.py /path/to/skill --json --output report.json
```

## Security Skills Will Score CRITICAL

Skills that discuss attack patterns, vulnerability scanning, or security testing will naturally score high because SkillSpector detects those patterns as potential threats. This is expected — `agent-security` itself scores 100/100 CRITICAL. Don't block security skills based solely on the score; use judgment.
