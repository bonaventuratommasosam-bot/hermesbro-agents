---
name: hermes-dreaming-setup
description: Install, patch, and configure hermes-dreaming plugin for custom OpenAI-compatible providers (OpenGateway, local LLMs). Covers provider patching, prompt tuning, memory format, and troubleshooting.
triggers:
  - hermes dreaming setup
  - hermes dreaming configure
  - dreaming plugin
  - dreaming review not working
  - dreaming malformed JSON
  - dreaming provenance error
---

# Hermes Dreaming — Setup & Configuration

## When to use this skill
Setting up hermes-dreaming plugin with a custom OpenAI-compatible endpoint (OpenGateway, vLLM, local models). NOT for vanilla OpenAI/Anthropic setup.

## Install / Upgrade

```bash
# From local clone
cd /tmp && git clone <repo-url> hermes-dreaming
cd hermes-dreaming && git checkout v0.4.0  # or latest tag
hermes plugins install file:///tmp/hermes-dreaming --enable

# Upgrade (remove + reinstall, update doesn't pick up local changes)
hermes plugins remove hermes-dreaming
hermes plugins install file:///tmp/hermes-dreaming --enable
hermes gateway restart
```

## Reference files
- `references/open gateway-patches.py` — provider patches for OpenGateway/mimo compatibility
- `references/policy-limits.md` — target_policy and run_policy limits for validation

## Pitfall 1: OpenAI SDK `responses.create` vs `chat.completions`

The default provider uses `client.responses.create()` which doesn't work with most OpenAI-compatible endpoints. Patch to `chat.completions.create`:

```python
# File: <plugin-dir>/src/hermes_dreaming/providers.py
# Replace the generate() body around line 260:

import httpx as _httpx
client = OpenAI(api_key=self.api_key, base_url=self.base_url, http_client=_httpx.Client(headers={"Accept-Encoding": "identity"}))
prompt = self._build_prompt(sources, context)
response = client.chat.completions.create(model=self.model, messages=[{"role": "user", "content": prompt}], temperature=0, max_tokens=16384)
msg = response.choices[0].message if response.choices else None
text = (msg.content or "").strip()
if not text and msg and hasattr(msg, 'reasoning') and msg.reasoning:
    text = msg.reasoning.strip()
```

## Pitfall 2: Gzip decoding error (OpenGateway)

OpenGateway returns gzipped responses that the default OpenAI SDK can't decode. Fix: force `Accept-Encoding: identity` via custom httpx client (shown above).

## Pitfall 3: Reasoning models return `content=null`

Models like `mimo-v2.5-pro` (reasoning) put output in `message.reasoning` field, not `message.content`. The fallback `hasattr(msg, 'reasoning')` handles this. BUT reasoning models are slow (300s+ timeout). **Use non-reasoning variants** (`mimo-v2.5` not `mimo-v2.5-pro`) for faster results.

## Pitfall 4: Provenance validation is strict

The LLM must return provenance as EXACT `full_path:line_number` strings matching the source headers. Common failures:
- Relative paths (`memories/USER.md:3` instead of `/root/.../USER.md:3`)
- Ranges (`path:3-4` instead of `path:3`)
- Missing line numbers

**Fix**: Add line numbers to the source block in `_build_prompt`:
```python
def _numbered(content, path):
    lines = content.splitlines()
    return '\n'.join(f"{i+1}: {line}" for i, line in enumerate(lines))
source_block = "\n\n".join(f"### {source.path}\n{_numbered(source.content, source.path)}" for source in sources)
```

## Pitfall 5: Policy limits are tight

TARGET_POLICY limits per entry:
- memory: 240 chars, 4 lines
- user: 220 chars, 4 lines
- fact: 320 chars, 12 lines
- skill: 900 chars, 24 lines

RUN_POLICY: max 3 changes, max 1 add, max 250 new chars, max 3 targets.

Each entry MUST start with `-` (bullet). `policy_flags` must be non-empty list.

Add these constraints explicitly to the prompt or the LLM will overshoot.

## Pitfall 6: Dedupe conflicts

If the LLM generates multiple proposals for the same `target_path` with different content, validation fails with "conflicting proposals". Tell the LLM: "Generate at most ONE proposal per target_path."

## Pitfall 7: `target_path` must be relative

The LLM tends to use absolute paths for `target_path`. The prompt already says "memory.md for memory, user.md for user" but reinforce: "target_path must be RELATIVE to live_root, NEVER absolute."

## Memory file format

Dreaming reads `memories/MEMORY.md` and `memories/USER.md`. Format must be one entry per line (plain newlines), NOT `§` separators. The `§` format was a GribbitO convention that breaks Dreaming's line-number-based provenance tracking.

## Recommended prompt additions

Add these to `_build_prompt` in the provider:
```
"CRITICAL: Generate at most ONE proposal per target_path. If multiple changes are needed for the same file, combine them into a single proposal.\n"
"STRICT SIZE LIMITS per proposed_text: memory max 240 chars/4 lines, user max 220 chars/4 lines, fact max 320 chars/12 lines, skill max 900 chars/24 lines. Each entry must start with a dash (-). Max 3 proposals total. Be very concise.\n"
"IMPORTANT: target_path must be RELATIVE to live_root (e.g. user.md, memory.md, facts.jsonl, skills/name.md). NEVER use absolute paths for target_path.\n"
"Policy_flags must be a non-empty list of strings like ['auto-generated'].\n"
```

## Quick test

```bash
hermes dreaming review \
  --live-root <HERMES_ROOT>/profiles/gribbito \
  --source <HERMES_ROOT>/profiles/gribbito/memories \
  --provider openai \
  --model "mimo-v2.5" \
  --api-key "<key>" \
  --base-url "<GATEWAY_URL>" \
  --artifact-root /root/.dreaming/artifacts
```

Expected: `status: staged, proposals: N, validation: valid`

## Auto-approve & apply (cron workflow)

When running as a cron job (no user present), auto-approve low-risk proposals and apply:

```bash
# Approve all proposals
hermes dreaming approve <artifact-dir> all

# Apply to live root
hermes dreaming apply <artifact-dir> --live-root <HERMES_ROOT>/profiles/gribbito
```

Auto-approval criteria for cron: all proposals with confidence >= 0.8 AND risk == "low". Higher-risk proposals should be left for human review.

## Pitfall 8: Provenance mismatch with `--recent` source bundles

When using `--recent` (session harvests), the source path is the absolute path of the generated harvest file (e.g. `/root/.dreaming/artifacts/_sources/recent-sessions.md`). The LLM tends to use just the basename (`recent-sessions.md:16`) which fails validation. Fix: tell the LLM in the prompt to use the EXACT path shown after `###` in each source header, copying it verbatim including the full absolute path.

## OpenGateway model routing

OpenGateway uses provider-specific paths: `/v1/xiaomi-mimo`, `/v1/stepfun`, etc. Each path only accepts models from that provider. Model name format: `provider/model` or bare `model-name`.
- xiaomi-mimo path: only `xiaomi/mimo-*` or `mimo-*`
- List models: `GET /v1/<provider>/models` with `Authorization: Bearer <key>`
