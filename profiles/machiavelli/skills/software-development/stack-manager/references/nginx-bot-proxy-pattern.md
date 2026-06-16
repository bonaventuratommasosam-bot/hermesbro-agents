# Nginx Reverse Proxy Pattern for New Bots

When deploying a new bot on the VPS, add its nginx config to `/etc/nginx/sites-enabled/stack` in the SSL server block (port 443).

## Template

```nginx
# {Bot Name} — webhook + dashboard
location /{bot-path}/webhook/ {
    proxy_pass http://127.0.0.1:{port}/webhook/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
location /{bot-path}/ {
    proxy_pass http://127.0.0.1:{port}/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
location = /{bot-path} {
    return 301 /{bot-path}/;
}
```

## Steps

1. Edit `/etc/nginx/sites-enabled/stack` — insert block in SSL server (443)
2. Test: `nginx -t`
3. Reload: `systemctl reload nginx`
4. Set `WEBHOOK_HOST=https://<DOMAIN>/{bot-path}` in bot's `.env`
5. Restart bot: `systemctl restart {bot-name}`

## Current Bot Routes

| Bot | Path | Port |
|-----|------|------|
| Ratatouille | /ratatouille/ | 8084 |
| Wannabe Bot | /wannabe/ | 8093 |
| LAWrenzo | /lawrenzo/ | 8086 |
| Hermes Dashboard | /hermes/ | 9119 |

## Pitfall

The nginx config has TWO server blocks (port 80 redirect + port 443 SSL). Always add bot routes to the 443 block only. The port 80 block just redirects to HTTPS.

When using `sed` or Python to edit the config programmatically, be careful with the two occurrences of similar comment headers (e.g. "Hermes Dashboard — API" appears in both blocks). Target the second occurrence (SSL block) specifically.
