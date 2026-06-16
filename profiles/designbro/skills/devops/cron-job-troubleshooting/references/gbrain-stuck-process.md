# gBrain Stuck Process Pattern

## Symptom
- `bun /root/.bun/bin/gbrain get <checkpoint>` running at 100% CPU for hours/days
- Consumes 3-4GB RAM (available memory drops significantly)
- Process owned by `hermes-bot` user

## Detection
```bash
ps aux | grep 'gbrain' | grep -v grep
# Look for: high CPU time (2000+ minutes), state Rl (running+locked)
```

## Fix
```bash
kill -9 <PID>  # Force kill — gbrain doesn't respond to SIGTERM
```

## Prevention
- gbrain `get` on large checkpoints can hang indefinitely
- Consider adding a timeout wrapper: `timeout 60 gbrain get <checkpoint>`
- Monitor with error-watchdog.sh (already checks service health)

## Impact
- Frees 3-4GB RAM immediately
- No data loss — gbrain checkpoint data is stored in the PGLite database, not in the running process
