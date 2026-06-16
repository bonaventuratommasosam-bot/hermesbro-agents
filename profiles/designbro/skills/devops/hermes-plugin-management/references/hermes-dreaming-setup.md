# Hermes Dreaming Plugin — Patching Reference

## What it is
Hermes Dreaming (v0.3.0 → v0.4.0) is a plugin for reviewable self-improvement.
Scans memory/skills/facts, proposes changes as artifact bundles, validates, and applies with backup.

GitHub: https://github.com/asimons81/hermes-dreaming

## Installation
```bash
cd /tmp && git clone https://github.com/asimons81/hermes-dreaming
cd hermes-dreaming && git checkout v0.4.0
hermes plugins install file:///tmp/hermes-dreaming --enable
```

## Patches Applied (for OpenGateway + mimo models)

### 1. responses.create → chat.completions.create
File: `src/hermes_dreaming/providers.py` line ~262
```python
# Before
response = client.responses.create(model=self.model, input=prompt, temperature=0)
text = getattr(response, "output_text", "").strip()

# After
import httpx as _httpx
client = OpenAI(api_key=self.api_key, base_url=self.base_url,
    http_client=_httpx.Client(headers={"Accept-Encoding": "identity"}))
response = client.chat.completions.create(model=self.model,
    messages=[{"role": "user", "content": prompt}], temperature=0, max_tokens=16384)
msg = response.choices[0].message if response.choices else None
text = (msg.content or "").strip()
if not text and msg and hasattr(msg, 'reasoning') and msg.reasoning:
    text = msg.reasoning.strip()
```

### 2. Prompt hardening (same file, _build_prompt method)
Added to prompt:
- Line numbers in source block (so model references exact lines)
- Explicit provenance format: `full_path:line_number` (no ranges)
- Size limits per target_kind (memory: 240 chars/4 lines, user: 220/4)
- Max ONE proposal per target_path
- Max 3 proposals total
- policy_flags must be non-empty list
- target_path must be RELATIVE to live_root

### 3. Line numbering in source block
```python
def _numbered(content, path):
    lines = content.splitlines()
    numbered = [f"{i+1}: {line}" for i, line in enumerate(lines)]
    return '\n'.join(numbered)
source_block = "\n\n".join(f"### {source.path}\n{_numbered(source.content, source.path)}" for source in sources)
```

## Usage
```bash
# Review (generates artifact with proposals)
hermes dreaming review \
  --live-root <HERMES_ROOT>/profiles/gribbito \
  --source <HERMES_ROOT>/profiles/gribbito/memories \
  --provider openai \
  --model "mimo-v2.5" \
  --api-key "$OPENGATEWAY_API_KEY" \
  --base-url "<GATEWAY_URL>" \
  --artifact-root /root/.dreaming/artifacts

# Summarize proposals
hermes dreaming summarize <artifact-path>

# Approve and apply
hermes dreaming approve <artifact-path> all
hermes dreaming apply <artifact-path> --live-root <HERMES_ROOT>/profiles/gribbito --backup-root /root/.dreaming/backups

# Or reject
hermes dreaming reject <artifact-path> <proposal-id> --reason "..."
```

## Model choice
- `mimo-v2.5` (non-reasoning): works, fast, generates valid JSON
- `mimo-v2.5-pro` (reasoning): timeouts, content=null issues, avoid for structured output
- `mimo-v2-flash`: too weak, returns "no actionable triggers"

## Policy limits (from policy.py)
```python
TARGET_POLICY = {
    "memory": {"max_chars": 240, "max_lines": 4, "total_chars": 4000},
    "user": {"max_chars": 220, "max_lines": 4, "total_chars": 4000},
    "skill": {"max_chars": 900, "max_lines": 24, "total_chars": 12000},
    "fact": {"max_chars": 320, "max_lines": 12, "total_chars": 12000},
}
RUN_POLICY = {"max_changes": 3, "max_adds": 1, "max_new_chars": 250, "max_targets": 3}
```

## Cron setup for nightly reviews

`hermes dreaming install-cron` is LIMITED — only supports `--mode status-digest|inbox-digest` and `--schedule`. It does NOT run actual reviews with custom providers.

For a proper nightly review cron, use Hermes cron instead:

```
cronjob action=create, name=dreaming-review, schedule="0 3 * * *", prompt:
  Run: hermes dreaming review --recent 10 --live-root <HERMES_ROOT>/profiles/gribbito \
    --source <HERMES_ROOT>/profiles/gribbito/memories \
    --provider openai --model mimo-v2.5 \
    --api-key $KEY --base-url $URL \
    --artifact-root /root/.dreaming/artifacts
  If staged + proposals > 0 + low-risk + confidence >= 0.8: auto-approve and apply.
  Report in Italian.
```

Key: the prompt must be self-contained (no session context in cron runs).

## Memory format requirement
Dreaming tracks provenance by line number. Memory files MUST use newline-separated entries, NOT `§` separators (which collapse everything to 2-3 lines).
