# Mass Cron Job Fix Workflow

When [REDACTED — dati personali rimossi] says "sistema tutto" or multiple cron jobs are broken, use this workflow.

## Step 1: Inventory

```bash
# List all jobs, identify errors
# Use cronjob(action='list') — look for last_status: "error" and enabled: false
```

## Step 2: Check scripts exist

```bash
# Find all script paths referenced by broken jobs
for script in knowledge-sync.py linkedin-auto-post.py outreach-engine.py; do
  find ~/.hermes -name "$script" 2>/dev/null
done
```

## Step 3: Copy missing scripts to profile dirs

```bash
# Scripts must be in the PROFILE's scripts dir, not just ~/.hermes/scripts/
cp <HERMES_ROOT>/scripts/linkedin-auto-post.py ~/.hermes/profiles/gribbito/scripts/
cp <HERMES_ROOT>/scripts/outreach-engine.py ~/.hermes/profiles/gribbito/scripts/
```

## Step 4: Test each script manually

```bash
cd ~/.hermes/profiles/gribbito/scripts/
python3 knowledge-sync.py          # Should output "Synced..."
python3 session-digest-all.py      # Should auto-detect profile
bash error-watchdog.sh             # Should be silent (exit 0)
python3 conversation-summary.py    # Should generate summary
```

## Step 5: Fix cron job configs

```python
# Fix script paths with args
cronjob(action='update', job_id='xxx', script='conversation-summary.py')

# Then resume all fixed jobs
cronjob(action='resume', job_id='xxx')
```

## Step 6: Check for stuck processes

```bash
# gbrain or other tools can get stuck at 100% CPU
ps aux | grep -E 'gbrain|hermes' | grep -v grep | awk '$3 > 50 {print $2, $11, $12}'

# Kill stuck processes
kill -9 <PID>
```

## Step 7: Verify

```bash
# Confirm all jobs are scheduled
cronjob(action='list')  # Check enabled: true, state: scheduled
free -h  # Confirm memory freed
```
