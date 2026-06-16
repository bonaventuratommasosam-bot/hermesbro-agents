# Nginx Health Check Debugging

## Health Check False Positive Pattern

When a health check reports a service "down" but `systemctl` shows it running, the root cause is almost always the **check method**, not the service.

### Common Failure: HTTP 000 with Svc=OK

Symptom: health check reports `Svc=OK | Port=OK | HTTP=000` — service is up, port is listening, but HTTP check fails.

Root causes (in order of likelihood):

1. **Public URL from localhost** — health check curls `https://domain.tld/health` from the server itself. This exits via the public IP and re-enters, subject to:
   - Hairpin NAT failures (ISP/router doesn't support it reliably)
   - Transient network stack blips
   - DNS resolution delays
   - TLS handshake timeouts on loopback

2. **Rate limiting** — if nginx has `limit_req_zone` and the check endpoint shares a zone, repeated checks can hit the limit (HTTP 429 or connection drop).

3. **Upstream timeout** — if the check URL proxies to a backend (e.g., `/api/health` → FastAPI), a slow or crashed backend returns 502/504, but sometimes curl itself times out → HTTP 000.

### Fix: Use Localhost

```python
# WRONG — exits and re-enters server
check_url("https://hermesbro.cloud/health")

# RIGHT — stays local, no NAT/DNS/TLS overhead
check_url("http://127.0.0.1/health")
```

If the check must validate the full stack (nginx + TLS + routing), use localhost with the correct `Host` header:
```bash
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/health -H 'Host: hermesbro.cloud'
```

### Fix: Add Retry Logic

A single HTTP failure should not trigger an alert. Retry 2-3 times with 2-3 second delays:

```python
def check_url_with_retry(url, attempts=3, delay=3):
    for i in range(attempts):
        result = check_url(url)
        if result["healthy"]:
            return result
        if i < attempts - 1:
            time.sleep(delay)
    return result  # all attempts failed
```

### Fix: Distinguish Fixable vs Unfixable

If `Svc=OK` but `HTTP=000`, the service restart won't help. The alert message should not say "Auto-fix FAILED" when no fix was attempted. Better: "Nginx service UP but HTTP check failing — possible network/TLS issue".

## Nginx Config Pitfalls

### Conflicting Server Name Warnings

```
nginx[PID]: conflicting server name "domain.tld" on 0.0.0.0:80, ignored
```

Cause: Two `server {}` blocks declare the same `server_name` on the same port. One is silently ignored.

Common scenarios:
- Duplicate blocks in the same file (e.g., port 80 redirect + port 443 both declare `server_name domain.tld www.domain.tld` — this is actually fine, they're on different ports)
- Same domain configured in two different files under `sites-enabled/`
- A file in `sites-enabled/` duplicates a block in `nginx.conf`

**Diagnosis:**
```bash
grep -rn "server_name.*domain.tld" /etc/nginx/sites-enabled/ /etc/nginx/conf.d/ /etc/nginx/nginx.conf
```

### Direct Files vs Symlinks in sites-enabled

`sites-enabled/` should contain **symlinks** to `sites-available/`. A direct file in `sites-enabled/`:
- Won't survive `nginx -t` + reinstall workflows
- Can't be disabled with `rm symlink` and re-enabled later
- Gets lost if someone runs cleanup scripts

**Check:**
```bash
ls -la /etc/nginx/sites-enabled/
# Should show: file -> /etc/nginx/sites-available/file
# NOT: -rw-r--r-- ... file (direct file)
```

**Fix:**
```bash
mv /etc/nginx/sites-enabled/domain.conf /etc/nginx/sites-available/domain.conf
ln -s /etc/nginx/sites-available/domain.conf /etc/nginx/sites-enabled/domain.conf
```

### Rate Limit Zones and Health Endpoints

If health check endpoints share a `limit_req_zone` with API endpoints, frequent health checks (every 1-5 min) can trigger rate limiting, especially with `burst=5`.

**Fix:** Put health endpoints in a separate location without rate limiting:
```nginx
location = /health {
    return 200 '{"status":"ok"}';
    add_header Content-Type application/json;
    # No limit_req here
}
```

## Diagnostic Commands Quick Reference

```bash
# Is nginx running?
systemctl is-active nginx

# Is it listening?
ss -ltnp | grep ':443\|:80'

# Test config
nginx -t

# Recent errors
journalctl -u nginx --no-pager -n 20

# Check specific endpoint locally
curl -sv -o /dev/null -w '%{http_code}' http://127.0.0.1/health

# Check from public IP (tests hairpin NAT)
curl -sv -o /dev/null -w '%{http_code}' https://domain.tld/health --connect-timeout 5

# Find conflicting server names
grep -rn "server_name" /etc/nginx/sites-enabled/

# Find non-symlink files in sites-enabled
find /etc/nginx/sites-enabled/ -type f ! -type l
```
