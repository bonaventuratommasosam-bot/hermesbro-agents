# Cron Watchdog Service Drift

When cron-based watchdogs check systemd services, their service list can go stale as bots are disabled/removed.

## Pattern: False Alerts from Dead Services

**Symptom**: Error-watchdog reports `DOWN: hermes-contabile.service (inactive not-found)` repeatedly.

**Cause**: The watchdog script hardcodes service names. When services are disabled or removed from the fleet, the watchdog keeps alerting on them — producing noise and masking real issues.

**Fix**: Update the `SERVICES=()` array in the watchdog script to match only currently-active services. Check with:
```bash
systemctl list-units 'hermes-*' --all --no-pager
```

**Prevention**: When disabling/removing a bot, update BOTH copies of the watchdog script:
- `~/.hermes/scripts/error-watchdog.sh`
- `~/.hermes/profiles/gribbito/scripts/error-watchdog.sh`

**Keywords**: watchdog, systemd, service-list, false-alert, error-watchdog
