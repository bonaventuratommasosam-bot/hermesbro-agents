# Cron Script Path Resolution Errors

When cron `no_agent` jobs fail with path-related errors, the root cause is usually one of three issues.

## Pattern 1: Symlink Path Traversal Block

**Symptom:** `Blocked: script path resolves outside the scripts directory (<HERMES_ROOT>/profiles/gribbito/scripts): 'knowledge-sync.py'`

**Root Cause:** Hermes cron uses `os.path.realpath()` to resolve symlinks. If a symlink in `~/.hermes/profiles/<profile>/scripts/` points to `<HERMES_ROOT>/shared/scripts/`, the resolved path is outside the allowed directory → blocked.

**Verified on:** YOUR_VPS_ID, 2026-06-06. Affected: knowledge-sync, skill-sync, session-digest, conversation-summary.

**Fix:** Replace symlinks with real copies:
```bash
rm ~/.hermes/profiles/gribbito/scripts/knowledge-sync.py
cp <HERMES_ROOT>/shared/scripts/knowledge-sync.py ~/.hermes/scripts/knowledge-sync.py
cp <HERMES_ROOT>/shared/scripts/knowledge-sync.py ~/.hermes/profiles/gribbito/scripts/knowledge-sync.py
```

## Pattern 2: Script Field Format Error

**Symptom:** `Script path must be relative to ~/.hermes/scripts/` or `Script not found: <HERMES_ROOT>/scripts/python3 /path/to/script.py`

**Root Cause:** The `script` field was set to a command string instead of a bare filename. Common mistakes:
- `"python3 <HERMES_ROOT>/shared/linkedin/auto-post.py"` → treated as literal filename
- `"conversation-summary.py --hours 2"` → arguments treated as part of filename
- `"<HERMES_ROOT>/shared/scripts/foo.py"` → absolute path rejected

**Fix:** Script field = bare filename only. Script must exist in `~/.hermes/scripts/`. For arguments, create a wrapper `.sh` file.

## Pattern 3: Profile Scripts Dir Interference

**Symptom:** `Script path escapes the scripts directory via traversal` even with a bare filename.

**Root Cause:** The same filename exists as a symlink in the profile scripts dir that resolves outside. The cron system checks the profile dir first, finds the symlink, resolves it, and blocks.

**Fix:** Remove the symlink from the profile scripts dir. Keep only real copies in both `~/.hermes/scripts/` and `~/.hermes/profiles/<profile>/scripts/`.

## Diagnostic Commands

```bash
# Check if a script is a symlink
file ~/.hermes/profiles/gribbito/scripts/knowledge-sync.py

# Check where symlinks point
ls -la ~/.hermes/profiles/gribbito/scripts/

# Verify script exists in canonical location
ls -la ~/.hermes/scripts/outreach-engine.py
```
