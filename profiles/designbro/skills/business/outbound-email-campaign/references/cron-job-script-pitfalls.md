# Cron Job Script Pitfalls

When setting up `no_agent=True` cron jobs with scripts, several non-obvious failure modes exist.

## Pitfall 1: Symlinks Blocked by Path Resolution

**Symptom:** `Blocked: script path resolves outside the scripts directory`

**Cause:** Hermes cron resolves symlinks via `os.path.realpath()` before checking if the path is inside the allowed scripts directory. Symlinks in `~/.hermes/profiles/<profile>/scripts/` that point to `<HERMES_ROOT>/shared/scripts/` get resolved to the real path, which is outside the profile scripts dir → blocked.

**Fix:** Copy the script file instead of symlinking:
```bash
# WRONG — symlink gets resolved and blocked
ln -s <HERMES_ROOT>/shared/scripts/knowledge-sync.py ~/.hermes/profiles/gribbito/scripts/knowledge-sync.py

# RIGHT — copy the file
cp <HERMES_ROOT>/shared/scripts/knowledge-sync.py ~/.hermes/scripts/knowledge-sync.py
```

**Keywords:** cron, symlink, path-resolution, blocked, scripts directory

## Pitfall 2: Script Path Must Be Just a Filename

**Symptom:** `Script path must be relative to ~/.hermes/scripts/` or `Script path escapes the scripts directory via traversal`

**Cause:** The `script` field in cron jobs must be a bare filename (e.g., `outreach-engine.py`), NOT:
- An absolute path (`<HERMES_ROOT>/shared/scripts/foo.py`)
- A relative path with directories (`scripts/foo.py`)
- A command with arguments (`conversation-summary.py --hours 2`)
- A command prefix (`python3 /path/to/script.py`)

**Fix:**
```bash
# Copy script to the canonical location
cp <HERMES_ROOT>/shared/marketing/email/outreach-engine.py ~/.hermes/scripts/outreach-engine.py

# Update cron job with just the filename
# script: "outreach-engine.py"
```

If the script needs arguments, create a wrapper `.sh` file:
```bash
# ~/.hermes/scripts/run-summary.sh
#!/bin/bash
python3 ~/.hermes/scripts/conversation-summary.py --hours 2
```

**Keywords:** cron, script-path, filename-only, arguments, traversal

## Pitfall 3: Profile Scripts vs Global Scripts

**Two script directories exist:**
- `~/.hermes/scripts/` — canonical location for cron scripts (global)
- `~/.hermes/profiles/<profile>/scripts/` — profile-specific

Cron jobs resolve scripts from `~/.hermes/scripts/`. The profile scripts dir can interfere if it contains symlinks that resolve outside. When updating scripts, update BOTH locations if both exist:
```bash
cp script.py ~/.hermes/scripts/script.py
cp script.py ~/.hermes/profiles/gribbito/scripts/script.py
```

## Pitfall 4: Profile Lacks Messaging Platform

**Symptom:** `platform 'telegram' not configured/enabled`

**Cause:** Cron job has `deliver: telegram:chat_id` but runs under a profile (e.g., `wannabe`) that doesn't have Telegram configured in its `config.yaml`.

**Fix:** Change deliver to `origin` so it routes through the main profile's messaging:
```yaml
# WRONG — wannabe profile has no telegram
deliver: telegram:<ADMIN_CHAT_ID>:32638

# RIGHT — routes through main profile
deliver: origin
```

**Keywords:** cron, deliver, telegram, profile, messaging

## Quick Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `script path resolves outside` | Symlink resolved to external path | Copy file, don't symlink |
| `script path must be relative` | Absolute path in script field | Use bare filename |
| `script path escapes via traversal` | Filename matches a symlink that resolves outside | Remove symlink from profile dir, use copy |
| `Script not found: X --args` | Arguments baked into script field | Move args to wrapper .sh |
| `platform 'telegram' not configured` | Profile missing telegram config | Use `deliver: origin` |
