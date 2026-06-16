# Inter-Bot Communication Models

## Two Communication Channels

### 1. Bus Messaging (Hermes profiles)
- **Tool:** `<HERMES_ROOT>/shared/scripts/bus-send.py`
- **Requires:** Target bot must be a Hermes profile in `<HERMES_ROOT>/profiles/`
- **Requires:** Target bot must have GOAL.md to process incoming messages
- **Latency:** Immediate write, but READ depends on polling mechanism (see below)
- **Profiles with inbox:** contabile, designbro, el-froggo, frank, gribbito, groot, lawrenzo, wannabe

**Usage:**
```bash
python3 <HERMES_ROOT>/shared/scripts/bus-send.py send <from> <to> "<message>" [type]
python3 <HERMES_ROOT>/shared/scripts/bus-send.py check <bot>
python3 <HERMES_ROOT>/shared/scripts/bus-send.py read <bot> <msg_id>
```

### 2. Shared Knowledge Files (all bots)
- **Path:** `<HERMES_ROOT>/shared/knowledge/`
- **Works for:** ALL bots, including external ones
- **Latency:** Up to 30min (sync cycle)
- **No profile required** — just read/write files

## ⚠️ Bus Inbox Gap (Critical)

**Problem:** Bus messaging writes JSON files to `<HERMES_ROOT>/shared/bus/inbox/<bot>/`, but no bot has a mechanism to automatically read them. Messages pile up unread.

**Root cause:** No cron job or hook polls the inbox. GOAL.md references `[FROM:xxx]` handlers but nothing triggers the check.

**Fix:** Each bot that needs to receive bus messages must have a cron job or script that:
1. Runs `bus-send.py check <bot>` periodically
2. Reads messages, marks them as read
3. Executes actions based on `[FROM:xxx]` in GOAL.md
4. Sends responses via bus-send.py or Telegram

**Template:** See `references/bus-inbox-polling.md`

## Communication Matrix (updated 2026-06-01)

| From → To | Bus Message | Shared Knowledge |
|-----------|-------------|------------------|
| gribbito → contabile | ✅ | ✅ |
| gribbito → frank | ✅ (profile exists) | ✅ |
| frank → gribbito | ✅ | ✅ |
| gribbito → sentinel | ✅ | ✅ |
| gribbito → any bot | ✅ (if profile exists) | ✅ |

## Limitations

- **Bus messaging** is one-way. No built-in response mechanism — target must explicitly reply via its own bus-send.py call or shared knowledge write.
- **No auto-polling** — messages sit in inbox until a cron/session reads them. This is the #1 gap.
- **Shared knowledge** is eventually consistent (30min sync). Not suitable for urgent requests.
- **No real-time chat** between bots. All communication is asynchronous file-based.

## Best Practices

1. **For urgent tasks:** Use bus messaging (immediate inbox write) + set up polling cron on target
2. **For cross-cutting info:** Use shared knowledge (visible to all)
3. **For tasks needing response:** Write task via bus, ensure target has polling cron
4. **New bot setup:** Always create a bus inbox polling cron alongside the profile
