---
name: error-memory
description: >
  Structured error memory for tool failures. Record, search, and learn from
  tool errors across sessions. Use after any tool failure that took non-trivial
  debugging to resolve.
triggers:
  - tool fails and is resolved via fallback or retry with different approach
  - user says "remember this error" / "ricorda questo errore"
  - same error seen in different session
---

## When to Record (auto — no user prompt needed)

Record an error memory entry when ALL of these are true:
1. A tool call failed (non-trivial — not a typo or transient network blip)
2. You diagnosed the root cause OR found a working fallback
3. The fix/cause would help a future session avoid the same problem

**Do NOT record**: trivial typos, missing args fixed on first retry, transient network errors, one-off permission issues.

**Trigger keywords from user** (must record immediately):
- "remember this error", "ricorda", "memorizza errore", "non dimenticare"

## Structured Format

Save to memory with this exact structure:

```
ERROR: [tool_name] — [short description]
- Symptom: what happened (exact error or behavior)
- Cause: root cause (if confirmed)
- Fix: action that resolved it (or "unresolved" if abandoned)
- Outcome: resolved / failed / abandoned
- Keywords: tool_name, error_type, context_tags
```

### Example

```
ERROR: web_extract — DuckDuckGo backend cannot extract URLs
- Symptom: Returns "DuckDuckGo (ddgs) is a search-only backend and cannot extract URL content"
- Cause: web_extract uses DuckDuckGo which is search-only, not a content extractor
- Fix: Use curl + terminal or browser_navigate instead for URL content extraction
- Outcome: resolved
- Keywords: web_extract, duckduckgo, extraction, fallback_curl
```

## How to Search

When a tool behaves unexpectedly:
1. Check memory first — search for the tool name + error symptom
2. If hit found → apply the known fix directly, skip re-diagnosis
3. If no hit → diagnose normally, then record the result

## Outcome States

- **resolved**: fix worked, record the solution
- **failed**: strategy confirmed non-working after verification (reproducible failure)
- **abandoned**: 3+ approaches tried, none worked, record what was tried + what remains

## Pitfall Archive

See `references/cron-watchdog-drift.md` for the service-list drift pattern (watchdog alerting on disabled bots).
See `references/cron-script-path-resolution.md` for cron script symlink/path errors (blocked scripts, path traversal).

## Auto-Cleanup

Entries with outcome "resolved" where the fix is now standard knowledge
(e.g., a well-documented API change) can be removed after 90 days.
Entries with outcome "failed" stay permanently — they prevent repeated mistakes.
