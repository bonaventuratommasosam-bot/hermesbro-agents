# Telegram Thread Consolidation

When [REDACTED — dati personali rimossi] says "ingloba tutti i thread in uno solo" or similar — unify all Telegram topic/thread delivery into a single thread.

## Procedure

### Step 1 — Identify target thread
The current session's thread_id is the target. Check the session context or ask [REDACTED — dati personali rimossi].

### Step 2 — Clean channel_directory.json on ALL profiles
Each profile has `~/.hermes/profiles/<name>/channel_directory.json`. ALL must be updated.

Keep only:
- DM entry without thread: `{"id": "<chat_id>", "name": "...", "type": "dm", "thread_id": null}`
- Unified thread entry: `{"id": "<chat_id>:<thread_id>", "name": "... / Main Thread", "type": "dm", "thread_id": "<thread_id>"}`
- Group entry (if applicable): `{"id": "<group_id>", "name": "HERMES HUB", "type": "group", "thread_id": null}`

Remove all other topic entries. Use `execute_code` with `from hermes_tools import write_file` to batch-update all profiles.

### Step 3 — Update ALL cron jobs
Run `cronjob(action='list')` to get all jobs. Update every job that has an explicit `deliver` target:
- Jobs with `deliver: "telegram:<chat_id>:<old_thread>"` → change to `telegram:<chat_id>:<new_thread>`
- Jobs with `deliver: "origin"` → change to explicit `telegram:<chat_id>:<new_thread>` for consistency
- Jobs with `deliver: "local"` → leave as-is (they don't send to Telegram)

### Step 4 — Verify
Run `cronjob(action='list')` again and confirm no job references an old thread_id.

## Pitfalls

- **Forgetting other profiles**: Each profile has its OWN channel_directory.json. If you only update gribbito, the other 6 profiles still reference old threads. Always update ALL 7+ profiles.
- **`origin` deliveries are fragile**: They depend on where the job was created from. After thread consolidation, pin them to the explicit target.
- **`local` jobs are fine**: Jobs delivering to `local` (like groot-sales-event-trigger, lawrenzo-regulation-check, wannabe-designbro-pipeline, designbro-sync-check) don't touch Telegram — leave them alone.
- **execute_code needs imports**: `write_file` must be imported from `hermes_tools`, it's not available as a bare builtin.
