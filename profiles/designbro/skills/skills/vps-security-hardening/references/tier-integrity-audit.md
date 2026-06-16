# Tier Integrity Audit — Reference

## Context
After implementing knowledge tier isolation (personal/business/shared), need automated monitoring to detect permission drift, unauthorized access, and system health issues.

## Script Location
`<HERMES_ROOT>/scripts/audit-tier.sh` (Python, despite .sh extension)

## Cron
```
*/10 * * * * python3 <HERMES_ROOT>/scripts/audit-tier.sh
```

## Log Format
JSONL at `/var/log/hermesbro-audit.jsonl`. Each line:
```json
{"ts": "ISO8601", "check": "name", "status": "ok|warn|alert|critical", "detail": "description"}
```

## Checks Implemented
1. **tier-perms** — verifies directory ownership/permissions on personal/, business/, shared/
2. **tier-files** — detects unauthorized files (root-owned in business, non-root in personal)
3. **luks-mount** — checks /mnt/hermesbro-encrypted is mounted, attempts auto-remount if not
4. **svc** — counts active hermes-*.service units vs expected count
5. **env** — scans all .env files for mode != 600
6. **checksum** — SHA256 of critical knowledge files, warns on unexpected changes

## Alert Routing
- `warn` → log only
- `alert` → log + Telegram message to <FOUNDER>
- `critical` → log + Telegram + auto-remount attempt (for LUKS)

## Pitfalls
- **Exclusion list**: services intentionally stopped (e.g., hermes-bus-watcher) must be in the exclusion list, otherwise they trigger false alerts every 10 min.
- **First run**: baseline checksum generation should NOT alert. Script must detect "no baseline file exists" and create it silently.
- **Token sharing**: if two bots share a Telegram token, one will be down. The audit counts "N/13 up" but can't distinguish intentional vs broken. Always verify the `inactive` service before assuming it's a problem.
- **Log rotation**: JSONL grows indefinitely. Add logrotate or periodic truncation.
