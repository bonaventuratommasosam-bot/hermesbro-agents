# Hermes Session DB Schema

Each profile has a `state.db` (SQLite) at `<HERMES_ROOT>/profiles/<bot>/state.db`.

## Tables

### sessions
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,              -- e.g. "20260531_215800_abc123"
    source TEXT NOT NULL,             -- "telegram", "cli", "cron", "gateway"
    user_id TEXT,                     -- Telegram chat_id
    model TEXT,                       -- e.g. "mimo-v2.5-pro"
    started_at REAL NOT NULL,         -- epoch timestamp (NOT ISO string)
    ended_at REAL,                    -- epoch timestamp
    title TEXT,                       -- auto-generated session title
    message_count INTEGER DEFAULT 0,
    tool_call_count INTEGER DEFAULT 0,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    estimated_cost_usd REAL,
    FOREIGN KEY (parent_session_id) REFERENCES sessions(id)
);
```

### messages
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    role TEXT NOT NULL,               -- 'user', 'assistant', 'tool'
    content TEXT,                     -- message text
    tool_call_id TEXT,
    tool_calls TEXT,                  -- JSON array of tool calls
    tool_name TEXT,
    timestamp REAL NOT NULL,          -- epoch timestamp
    token_count INTEGER,
    platform_message_id TEXT          -- Telegram message_id
);
```

## Query Patterns

### Recent sessions (last N hours)
```sql
SELECT id, title, started_at, source, message_count
FROM sessions
WHERE started_at > strftime('%s', 'now') - (N * 3600)
ORDER BY started_at DESC LIMIT 10;
```

### Session messages (user/assistant only, skip tool noise)
```sql
SELECT role, content, timestamp
FROM messages
WHERE session_id = ? AND role IN ('user', 'assistant')
ORDER BY timestamp ASC;
```

### Count sessions per source
```sql
SELECT source, count(*) FROM sessions GROUP BY source;
```

## Pitfalls

- `started_at` is REAL (epoch seconds), NOT ISO string. Use `time.strftime('%Y-%m-%d %H:%M', time.gmtime(started_at))` for display.
- `role='tool'` messages are usually noise (raw tool output). Filter them out when summarizing.
- Session IDs are `YYYYMMDD_HHMMSS_<hex>` format — not UUIDs.
- `title` is often NULL for cron sessions.
- FTS5 indexes exist on messages for full-text search: use `messages_fts` table for keyword search.
