# Security Tools Installation Guide

## Required Tools

Install these security tools on any VPS for comprehensive monitoring:

```bash
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
  lynis \
  rkhunter \
  chkrootkit \
  clamav \
  clamav-daemon \
  aide \
  nmap \
  nikto \
  net-tools
```

## Post-Installation Configuration

### AIDE (File Integrity Monitoring)

Create `/etc/aide/aide.conf`:

```
database_in=file:/var/lib/aide/aide.db
database_out=file:/var/lib/aide/aide.db.new
database_new=file:/var/lib/aide/aide.db.new
gzip_dbout=yes

FIPSR = p+i+n+u+g+s+m+c+acl+selinux+xattrs+sha256
NORMAL = FIPSR
CONTENT = sha256

/etc NORMAL
/boot NORMAL
/bin NORMAL
/sbin NORMAL
/usr/bin NORMAL
/usr/sbin NORMAL
/etc/passwd CONTENT
/etc/shadow CONTENT
/etc/group CONTENT
/etc/sudoers CONTENT
/etc/ssh/sshd_config CONTENT
/etc/cron.d NORMAL
/etc/cron.daily NORMAL

!/var/log
!/var/spool
!/var/cache
!/var/lib/clamav
!/var/lib/aide
!/tmp
!/run
!/proc
!/sys
!/dev
```

Initialize: `aide --init --config=/etc/aide/aide.conf`
Copy database: `cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db`

### ClamAV

Fix log permissions if needed:
```bash
chown -R clamav:clamav /var/log/clamav/
chmod 755 /var/log/clamav/
```

Update: `freshclam`

### rkhunter

Update: `rkhunter --update`

## Quick Audit Script

Create `/usr/local/bin/quick-audit.sh`:

```bash
#!/bin/bash
# Quick Security Audit - use for daily monitoring
# lynis is slow (timeout), use this for fast scans

echo "=== Network Status ==="
ss -tuln | grep LISTEN

echo "=== Failed Login Attempts (24h) ==="
journalctl _COMM=sshd --since "24 hours ago" 2>/dev/null | grep -i "failed" | wc -l

echo "=== Disk Usage ==="
df -h | grep -E "^/dev"

echo "=== Firewall Status ==="
ufw status 2>&1

echo "=== Rootkit Quick Check ==="
rkhunter --check --skip-keypress --report-warnings-only 2>&1 | tail -10
```

## Full Audit Script

Create `/usr/local/bin/full-audit.sh` (with lynis, run weekly):

```bash
#!/bin/bash
# Full Security Audit - run weekly, not daily (lynis is slow)
lynis audit system --quick --no-colors 2>&1 | grep -E "(Hardening|Warning|Suggestion)"
aide --check --config=/etc/aide/aide.conf 2>&1 | tail -20
clamscan -r /home --infected --remove 2>&1 | tail -10
```

## Pitfalls

- **lynis timeout**: lynis audit takes 5+ minutes. Use `quick-audit.sh` for daily, `full-audit.sh` for weekly.
- **ClamAV log permissions**: freshclam fails if `/var/log/clamav/` is not owned by clamav user.
- **AIDE config required**: `aide --init` fails without `--config` flag pointing to config file.
- **rkhunter WEB_CMD**: If `WEB_CMD` is set to `/bin/false` in config, update fails. Ignore warning.
