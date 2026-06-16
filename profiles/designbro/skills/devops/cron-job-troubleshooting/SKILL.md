---
name: cron-job-troubleshooting
description: "Troubleshoot Hermes cron job failures — script path resolution, symlink blocking, delivery errors, and common misconfigurations."
version: 1.0.0
author: gribbito
tags: [cron, troubleshooting, hermes, scripts, debugging]
related_skills: [hermes-agent, vps-email-outbound]
---

# Cron Job Troubleshooting

## References

- `references/mass-fix-workflow.md` — step-by-step for "sistema tutto" mass-fix scenarios
- `references/gbrain-stuck-process.md` — gbrain get hanging at 100% CPU

## When to use

- Cron job shows `status: error` with "script failed" or "script not found"
- "Blocked: script path resolves outside the scripts directory"
- "Script path escapes the scripts directory via traversal"
- "platform 'telegram' not configured/enabled" delivery errors
- Script runs fine manually but fails in cron

## How cron script resolution works

The `script` field in `no_agent=True` cron jobs resolves as a **filename**. Cron checks two directories in order:

1. `~/.hermes/profiles/<profile>/scripts/` — profile-specific (profile from job's `profile` field, defaults to scheduler's profile)
2. `~/.hermes/scripts/` — shared fallback

Symlinks that resolve outside the scripts directory are blocked by the security check.

### The 4 rules

1. **Bare filename only** — `my-script.py`, NOT `<HERMES_ROOT>/scripts/my-script.py` (absolute paths rejected) and NOT `python3 my-script.py` (treated as literal filename)
2. **No args in script field** — `conversation-summary.py --hours 2` tries to find a file literally named `conversation-summary.py --hours 2`. Embed defaults in the script itself or use a wrapper `.sh`
3. **No `python3` prefix** — `python3 /path/to/foo.py` is treated as one literal filename
4. **Symlinks blocked** — if a script is a symlink pointing outside the scripts directory, cron blocks it with "resolves outside the scripts directory". Replace with a real copy

### Where to put scripts

**Profile-specific:** `~/.hermes/profiles/<profile>/scripts/` — primary resolution path for that profile's cron jobs.
**Shared fallback:** `~/.hermes/scripts/` — checked if not found in profile dir.

Always copy scripts (don't symlink) to the profile's scripts dir. The profile is determined by the cron job's `profile` field.

## Common failure patterns

### Pattern 1: Symlink blocked

```
Blocked: script path resolves outside the scripts directory (<HERMES_ROOT>/profiles/gribbito/scripts): 'knowledge-sync.py'
```

**Cause:** `knowledge-sync.py` is a symlink to `<HERMES_ROOT>/shared/scripts/knowledge-sync.py`. Cron resolves the symlink and sees the real path is outside the allowed directory.

**Fix:**
```bash
# Remove symlink, copy real file
rm ~/.hermes/profiles/gribbito/scripts/knowledge-sync.py
cp ~/.hermes/shared/scripts/knowledge-sync.py ~/.hermes/profiles/gribbito/scripts/knowledge-sync.py

# Also copy to the primary scripts dir
cp ~/.hermes/shared/scripts/knowledge-sync.py ~/.hermes/scripts/knowledge-sync.py
```

### Pattern 2: Script field has args or `python3`

```
Script not found: <HERMES_ROOT>/profiles/gribbito/scripts/python3 <HERMES_ROOT>/shared/linkedin/auto-post.py
```

**Cause:** `script` field was set to `"python3 <HERMES_ROOT>/shared/linkedin/auto-post.py"`. The entire string is treated as a filename.

**Fix:**
```bash
# Copy script to standard location
cp <HERMES_ROOT>/shared/linkedin/auto-post.py ~/.hermes/scripts/linkedin-auto-post.py

# Update cron job to use bare filename
# cronjob(action='update', job_id='...', script='linkedin-auto-post.py')
```

### Pattern 3: Args embedded in filename (no python3 prefix)

```
Script not found: <HERMES_ROOT>/profiles/gribbito/scripts/conversation-summary.py --hours 2
```

**Cause:** `script` field set to `"conversation-summary.py --hours 2"`. Unlike Pattern 2, there's no `python3` prefix — just bare args after the filename. Cron treats the WHOLE string as the filename.

**Fix:**
```bash
# Option A: Update cron job to bare filename, script uses default values
# cronjob(action='update', job_id='xxx', script='conversation-summary.py')

# Option B: Create a wrapper script with args baked in
cat > ~/.hermes/profiles/gribbito/scripts/conversation-summary-2h.sh << 'EOF'
#!/bin/bash
python3 ~/.hermes/profiles/gribbito/scripts/conversation-summary.py --hours 2
EOF
chmod +x ~/.hermes/profiles/gribbito/scripts/conversation-summary-2h.sh
# cronjob(action='update', job_id='xxx', script='conversation-summary-2h.sh')
```

### Pattern 4: Script requires positional args that cron doesn't pass

```
Usage: session-digest.py <bot_name> [--days N]
```

**Cause:** Script requires a positional argument (e.g., bot_name) but the cron job invokes it with no args. Script exits 1.

**Fix:** Modify the script to auto-detect the value:
```python
# At top of script, add auto-detection:
import os

def get_current_profile():
    profile = os.environ.get("HERMES_PROFILE")
    if profile:
        return profile
    script_path = os.path.dirname(os.path.abspath(__file__))
    if "/profiles/" in script_path:
        parts = script_path.split("/profiles/")
        if len(parts) > 1:
            candidate = parts[1].split("/")[0]
            if os.path.isdir(os.path.join(PROFILES_DIR, candidate)):
                return candidate
    return "gribbito"  # fallback default

# Then in main():
bot_name = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else get_current_profile()
```

### Pattern 5: Column name mismatch after schema migration

```
Error reading sessions: no such column: created_at
```

**Cause:** Script queries `created_at` but the sessions table schema uses `started_at`. Happens after Hermes updates that change the DB schema.

**Fix:**
```bash
# Check actual schema
sqlite3 ~/.hermes/profiles/gribbito/state.db ".schema sessions"

# Fix the column reference in the script
# Old: WHERE created_at > ? ORDER BY created_at
# New: WHERE started_at > ? ORDER BY started_at
```

### Pattern 6: Absolute path rejected

```
Script path must be relative to ~/.hermes/scripts/. Got absolute or home-relative path
```

**Cause:** `script` field was set to an absolute path like `<HERMES_ROOT>/shared/scripts/foo.py`.

**Fix:** Copy the file to `~/.hermes/scripts/` and use bare filename.

### Pattern 7: Delivery error — platform not configured

```
delivery error: platform 'telegram' not configured/enabled
```

**Cause:** Cron job runs under a profile (e.g., `wannabe`) that doesn't have Telegram configured, but `deliver` is set to `telegram:chat_id:thread_id`.

**Fix:** Change `deliver` to `"origin"` (routes through the scheduler's profile, which has Telegram) or configure the platform in the target profile.

### Pattern 8: Telegram delivery — "Chat not found"

```
delivery error: platform 'telegram' not configured/enabled
```

**Cause A:** The bot running the cron job is NOT a member of the target Telegram group/channel. The invite link alone is insufficient — the bot account must be added to the group manually.

**Fix A:** Add the bot to the group via Telegram UI (Members → Add Member → search bot). Then send any message in the group, run `getUpdates` to capture the correct `chat_id`.

**Cause B:** Wrong chat_id format. A plain positive number (e.g. `<CHAT_ID>`) is not a valid supergroup ID.

**Fix B:** Supergroup IDs are always negative (`-100...`). If using threads/topics, format as `chat_id:thread_id`. Get the real IDs by:
1. Adding the bot to the group
2. Sending a test message in the group
3. Running: `curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates" | jq '.result[-1].message.chat'`

**PITFALL:** Adding the bot before configuring the invite link is not enough — the bot must be physically in the member list. Check with: `curl -s "https://api.telegram.org/bot<TOKEN>/getChat?chat_id=<ID>"` — if it returns 400, the bot isn't recognized as a member.

**PITFALL:** If using a shared Hermes gateway, the cron job's `deliver` target must match the same bot token that's in the group. A cron job sending through bot A won't reach a group that only has bot B.

### Pattern 9: Script exits non-zero (legitimate)

```
Status: script failed
Script exited with code 1
```

**This is NOT a cron config issue.** The script ran but detected a problem (e.g., watchdog found services down). Check the stdout in the error message for the actual cause.

## Pitfalls

- **Script must be executable** — `chmod +x` on .sh scripts. Python scripts can work without +x if invoked by the cron runner, but `chmod +x` is safer.
- **DB schema changes break scripts** — when Hermes updates change column names in `state.db`, any script querying that table breaks. Always check `.schema sessions` before assuming column names.
- **Stale cron output can mislead** — the error output stored in `~/.hermes/profiles/<profile>/cron/output/JOB_ID/` shows the LAST failure, not the current state. A script fixed since then may work fine — test manually before assuming it's still broken.
- **"sistema tutto" pattern** — when asked to fix everything: (1) `cronjob list` to get all jobs, (2) check `last_status: error` jobs, (3) read their output logs, (4) diagnose each failure pattern below, (5) fix scripts first, then resume jobs.

## Debugging checklist

```bash
# 1. Check if script exists in the right place
ls -la ~/.hermes/scripts/SCRIPT_NAME

# 2. Check if it's a symlink
file ~/.hermes/scripts/SCRIPT_NAME
readlink ~/.hermes/scripts/SCRIPT_NAME

# 3. Test manually
python3 ~/.hermes/scripts/SCRIPT_NAME

# 4. Check cron output logs
ls -lt ~/.hermes/profiles/PROFILE/cron/output/JOB_ID/
cat ~/.hermes/profiles/PROFILE/cron/output/JOB_ID/LATEST.md

# 5. Check mail log for delivery
grep "status=sent\|status=bounced\|DKIM" /var/log/mail.log | tail -10
```

## Updating a cron job's script field

```python
# WRONG — absolute path
cronjob(action='update', job_id='xxx', script='<HERMES_ROOT>/shared/scripts/foo.py')

# WRONG — args in filename
cronjob(action='update', job_id='xxx', script='foo.py --hours 2')

# WRONG — python3 in field
cronjob(action='update', job_id='xxx', script='python3 foo.py')

# RIGHT — bare filename
cronjob(action='update', job_id='xxx', script='foo.py')
```
