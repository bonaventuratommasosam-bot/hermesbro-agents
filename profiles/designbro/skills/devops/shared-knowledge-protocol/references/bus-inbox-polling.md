# Bus Inbox Polling — Setup Guide

## Problem

`bus-send.py` writes messages to `<HERMES_ROOT>/shared/bus/inbox/<bot>/`, but bots have no automatic mechanism to read them. Messages accumulate unread.

## Solution: Cron-based polling

Each bot that receives bus messages needs a cron job that periodically checks its inbox.

### Step 1: Create the polling script

Create at `<HERMES_ROOT>/profiles/<bot>/scripts/check-bus-inbox.sh`:

```bash
#!/bin/bash
# check-bus-inbox.sh — Poll bus inbox for unread messages
BOT_NAME="<bot>"
INBOX_DIR="<HERMES_ROOT>/shared/bus/inbox/${BOT_NAME}"
SEND_SCRIPT="<HERMES_ROOT>/shared/scripts/bus-send.py"

# Check for unread messages
messages=$(python3 "$SEND_SCRIPT" check "$BOT_NAME" 2>&1)

# Exit silently if no messages
if echo "$messages" | grep -q "No messages for"; then
    exit 0
fi

# Process each message
echo "$messages" | while IFS= read -r line; do
    if [[ -z "$line" ]]; then continue; fi
    
    # Extract sender from format: [from] (type) message
    sender=$(echo "$line" | grep -oP '^\[\K[^\]]+')
    message=$(echo "$line" | sed 's/^\[[^]]*\] ([^)]*) //')
    
    # Mark as read (extract msg id from inbox files)
    for f in "${INBOX_DIR}"/*.json; do
        [ -f "$f" ] || continue
        msg_id=$(basename "$f" .json)
        python3 "$SEND_SCRIPT" read "$BOT_NAME" "$msg_id"
    done
    
    # Output for cron delivery
    echo "[BUS from:${sender}] ${message}"
done
```

### Step 2: Register as Hermes cron job

```bash
hermes cron add \
  --name "check-bus-inbox" \
  --schedule "*/5 * * * *" \
  --script "scripts/check-bus-inbox.sh" \
  --no-agent \
  --profile <bot>
```

Or via cronjob tool:
```
cronjob create:
  schedule: "*/5 * * * *"
  script: "scripts/check-bus-inbox.sh"
  no_agent: true
  profile: "<bot>"
  name: "check-bus-inbox"
```

### Step 3: Update GOAL.md

Add to the bot's GOAL.md:
```markdown
## Bus Messages
- [FROM:gribbito] -> execute requested tasks
- [FROM:sentinel] -> respond to security alerts
- [FROM:frank] -> handle infra requests
```

### Step 4: Verify

1. Send a test message: `python3 bus-send.py send gribbito <bot> "test" "info"`
2. Wait for cron cycle (max 5 min)
3. Check if message was processed: `python3 bus-send.py check <bot>` should show "No messages"

## Pitfalls

- **Script path for no_agent crons:** Resolves under `~/.hermes/profiles/<profile>/scripts/`, NOT `<HERMES_ROOT>/shared/scripts/`. Either copy the script or symlink.
- **Silent exit:** When no messages, script MUST exit with code 0 and produce no stdout. Otherwise cron delivers empty/error messages to Telegram.
- **Mark as read:** Always call `bus-send.py read` after processing. Otherwise messages pile up and get re-processed.
- **JSON parsing:** Bus messages are JSON. Use `jq` or Python to parse, don't regex the raw file.

## Current Status (2026-06-01)

- [x] gribbito: has inbox, NO polling cron
- [ ] frank: has inbox, NO polling cron
- [ ] contabile: has inbox, NO polling cron
- [ ] sentinel: has inbox, NO polling cron
- [ ] All other bots: NO polling cron
