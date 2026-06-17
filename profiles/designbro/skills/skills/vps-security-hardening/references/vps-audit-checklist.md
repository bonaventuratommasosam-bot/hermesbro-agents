# VPS Security Audit — Quick Checklist

Read-only audit commands. No modifications — just reporting.

## 1. SSH Hardening
```bash
grep -E "^(Port|PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|PermitEmptyPasswords|X11Forwarding|MaxAuthTries|AllowUsers)" /etc/ssh/sshd_config
```
**Target:** `PermitRootLogin prohibit-password`, `PasswordAuthentication no`, `X11Forwarding no`

## 2. Firewall
```bash
ufw status verbose 2>/dev/null || iptables -L -n --line-numbers | head -30
```
**Target:** `Status: active`, `Default: deny (incoming)`, minimal open ports

## 3. Fail2ban
```bash
systemctl is-active fail2ban && fail2ban-client status
```
**Target:** Active, at least sshd jail

## 4. Open Ports
```bash
ss -tlnp | grep -v "127.0.0" | grep LISTEN
```
**Target:** Only expected services (nginx 80/443, SSH 22, app ports)

## 5. Nginx Security Headers
```bash
nginx -T 2>/dev/null | grep -E "(X-Frame-Options|X-Content-Type|X-XSS-Protection|Content-Security-Policy|Strict-Transport|server_tokens)" | sort -u
```
**Target:** All 6 headers + `server_tokens off`

## 6. SSL Certificates
```bash
for domain in example.com app.example.com api.example.com; do
  echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | openssl x509 -noout -enddate
done
```
**Target:** All certs valid, none expiring within 30 days

## 7. System Updates
```bash
apt list --upgradable 2>/dev/null | grep -v "^$"
```
**Target:** 0 upgradable packages

## 8. Sensitive Files
```bash
find /home/[REDACTED — dati personali rimossi] -name ".env" -not -path "*/venv/*" 2>/dev/null
```
**Target:** All `.env` files have `600` permissions

## 9. SSH Keys
```bash
ls -la /root/.ssh/
```
**Target:** `authorized_keys` present, no unexpected keys

## 10. Running Services
```bash
systemctl list-units --type=service | grep -iE '(hermes|nginx|ssh|fail2ban)'
```
**Target:** All expected services active

## Scoring Guide

| Score | Criteria |
|-------|----------|
| 90-100 | All checks pass, no warnings |
| 80-89 | 1-2 medium issues (X11, updates pending) |
| 70-79 | Missing fail2ban or security headers |
| 60-69 | Password auth enabled, missing firewall |
| <60 | Critical issues (root password login, no firewall) |

## Common Fixes

| Issue | Fix |
|-------|-----|
| X11Forwarding yes | `sed -i 's/^X11Forwarding yes/X11Forwarding no/' /etc/ssh/sshd_config && systemctl restart ssh` |
| .env too open | `chmod 600 /path/to/.env` |
| Updates pending | `apt update && apt upgrade -y` |
| Missing headers | Add to nginx vhost: see `references/nginx-security-headers.md` |
| Old kernels | `apt autoremove -y` |
| New kernel available | Reboot VPS (services auto-restart via systemd) |

**Pitfall:** The SSH service is `ssh.service` on Ubuntu, NOT `sshd.service`. Use `systemctl restart ssh`. Tested 2026-05-31.

**Pitfall:** After a VPS reboot, all systemd-enabled services auto-restart. Verify with `systemctl list-unit-files | grep enabled | grep hermes` BEFORE rebooting. If a service is `disabled`, it won't auto-start. Tested 2026-05-31: all 12 Hermes services were enabled.
