# Inter-Bot File-Based Bus

## Overview

File-based async messaging layer for inter-bot communication. Required because **Telegram bots cannot see messages from other bots in groups** — this is a platform-level Bot API limitation, not a privacy mode issue. Even with privacy disabled, Bot A's messages are invisible to Bot B. Only human user messages are delivered to bots.

The bus works around this: Bot A writes to filesystem → cron dispatches to group via Bot A's own Telegram API token → Bot A's message appears in group (but only humans see it). The receiving bot processes the message via its own cron jobs checking the filesystem inbox, NOT by reading the group.

**Why not just use send_message between bots?** Because the receiving bot's gateway will never see the message — Telegram doesn't deliver bot-to-bot. The filesystem is the only reliable channel.

## Architecture

```
Bot A                    Cron (5min)              Bot B
  │                        │                        │
  ├─ bus-send.py ──► inbox/botB/msg.json            │
  │                        │                        │
  │                  bus-dispatch.py                 │
  │                  reads inbox ──►                 │
  │                  send to group ──►               │
  │                  move to processed/              │
  │                        │                        │
  │                  Bot B gateway ◄── group message  │
```

## Directory Structure

```
<SHARED_DIR>/bus/
├── inbox/
│   ├── contabile/
│   ├── lawrenzo/
│   ├── groot/
│   ├── wannabe/
│   ├── designbro/
│   └── el-froggo/
├── outbox/
│   └── (same structure)
└── processed/
    └── (same structure)
```

## Scripts

### bus-send.py
- Path: `<SHARED_DIR>/scripts/bus-send.py`
- Usage: `python3 bus-send.py send <from> <to> <content> [type]`
- Creates `{timestamp}_{from}_{type}.json` in `inbox/{to}/`
- JSON fields: from, to, content, type, timestamp

### bus-dispatch.py
- Path: `<SHARED_DIR>/scripts/bus-dispatch.py`
- Usage: `python3 bus-dispatch.py`
- Reads all inbox dirs, sends to HERMES HUB group (`<GROUP_CHAT_ID>`)
- Moves processed messages to `processed/` dir
- Silent when no messages (no_agent cron pattern)

## Cron Job

- Profile: gribbito
- Schedule: every 5 min
- Script: `bus-dispatch.py` (no_agent)
- Deliver: local (silent when empty)
- **Status**: REMOVED. Re-enable when inter-bot comms are actively needed. File-based bus is the ONLY reliable inter-bot mechanism.

## Message Types

- `event` — calendar/operational events (GROOT → Wannabe)
- `design` — design briefs (Wannabe → DesignBro)
- `sales` — daily sales (GROOT → ContAIbile) — ⚠️ NOT YET IMPLEMENTED
- `trade` — trade notifications (El Froggo → ContAIbile)
- `compliance` — legal updates (LAWrenzo → others)
- `content` — content requests (Wannabe → others)
- `report` — status reports (any bot → gribbito)

## Pitfalls

- **Bus is one-way**: sender writes to receiver's inbox. Receiver processes from group message, not from file.
- **5 min delay**: max latency from cron interval. For urgent messages, use direct `send_message` instead.
- **No read receipts**: processed dir is for audit only, not for confirmation.
- **Dispatcher is no_agent**: runs script only, no LLM. Script must exit 0 and print nothing when empty.
- **Inbox dirs must exist**: created by `bus-send.py` on first write, but dispatcher assumes they exist.
- **Filename collision**: two messages from same bot in same second = overwrite. Use `{timestamp}_{from}_{type}.json` with full ISO timestamp (includes seconds).
- **Group chat ID**: dispatcher sends to `<GROUP_CHAT_ID>` (HERMES HUB). If group changes, update the script.
