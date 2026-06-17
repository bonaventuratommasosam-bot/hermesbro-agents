# Shared Knowledge Layer — Implementation Reference

## Data Flow

```
Bot discovers fact/preference/decision
  │
  ├─ Option A: CLI script (preferred)
  │   python3 fact-log.py contabile "[REDACTED — dati personali rimossi] wants X" "User ([REDACTED — dati personali rimossi])"
  │   → appends to <HERMES_ROOT>/shared/knowledge/facts.md
  │
  └─ Option B: Session digest (automated)
      session-digest.py runs daily at 23:00
      → reads state.db sessions
      → extracts patterns (decision markers, preference markers)
      → saves to knowledge/digests/{bot}-{date}.md

  Conversation summary (automated)
      conversation-summary.py runs every 2h
      → reads state.db sessions from all profiles
      → generates conversations.md with recent chat summaries
      → Frank and other bots can read recent context

Knowledge files (facts.md, decisions.md, preferences.md, conversations.md)
  │
  knowledge-sync.py (every 30min)
  │
  └─→ <HERMES_ROOT>/profiles/{bot}/shared-knowledge.md
      (auto-injected into every profile's context at session start)
```

## File Formats

### facts.md
```markdown
## User ([REDACTED — dati personali rimossi])
- [2026-05-31] [gribbito] [REDACTED — dati personali rimossi]'s Telegram: <USER>, chat_id <ADMIN_CHAT_ID>

## Environment
- [2026-05-31] [gribbito] VPS: YOUR_VPS_ID, 11 GiB RAM, 6 cores
```

### decisions.md
```markdown
## Architecture
- [2026-05-31] [gribbito] | SQLite for all storage | VPS constraints, simplicity
```

### preferences.md
```markdown
## Communication
- [2026-05-31] [gribbito] Italiano per conversazione, inglese per codice
```

## Script Details

### knowledge-sync.py
- Reads all 4 knowledge files (facts, decisions, preferences, conversations)
- Core files (facts, decisions, preferences) always included in full
- Conversations.md truncated to fit within 8,000 char budget
- Writes to each profile's `shared-knowledge.md` with header
- 10 profiles: gribbito + contabile + lawrenzo + groot + wannabe + designbro + el-froggo + ducato + sentinel + machiavelli

### conversation-summary.py
- Reads state.db from all profiles (last N hours, default 2)
- Extracts user/assistant messages (skips tool noise)
- Generates <HERMES_ROOT>/shared/knowledge/conversations.md
- Format: per-session summaries with title, date, key exchanges
- Used by Frank and other bots to see recent fleet activity

### session-digest.py
- Reads `state.db` from a profile
- Looks for decision markers: deciso, decidiamo, implementiamo, decided, let's go with
- Looks for preference markers: preferisco, mi piace, prefer, better if
- Saves digest to `knowledge/digests/{bot}-{date}.md`

### skill-sync.py
- Scans gribbito's skills/ for SKILL.md modified in last 24h
- Copies to all other profiles with `.skill-sync-hash` marker
- Never overwrites user-customized skills (no marker = skip)
- Log: `<HERMES_ROOT>/shared/logs/skill-sync.log`

## Cron Jobs

| Name | Schedule | Script | Type |
|------|----------|--------|------|
| knowledge-sync | every 30m | knowledge-sync.py | no_agent |
| skill-sync | 0 */6 * * * | skill-sync.py | no_agent |
| session-digest | 0 23 * * * | session-digest-all.py | no_agent |
| conversation-summary | every 2h | conversation-summary.py --hours 2 | no_agent |
