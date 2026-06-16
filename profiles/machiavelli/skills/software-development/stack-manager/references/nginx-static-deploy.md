# Nginx Static Site Deployment on the VPS

## Problem

The 443 server block has `deny all` except localhost for the default `/` location.
When adding a new public-facing static site (e.g. landing page), you must explicitly
add `allow all;` in the new location block.

## Pattern

```nginx
location /your-path/ {
    allow all;
    alias <USER_HOME>/ai-stack/your-site/;
    index index.html;
    try_files $uri $uri/ /your-path/index.html;
}
location = /your-path {
    return 301 /your-path/;
}
```

## Steps

1. Create directory: `mkdir -p <USER_HOME>/ai-stack/your-site/`
2. Place `index.html` there
3. Add location block to `/etc/nginx/sites-enabled/stack` INSIDE the 443 server block (before the final `}`)
4. `nginx -t` to validate
5. `nginx -s reload` to apply
6. Test: `curl -sk https://127.0.0.1/your-path/ -H "Host: <DOMAIN>" | head`

## Pitfalls

- `alias` requires trailing slash on both the location and the path
- `try_files` fallback must use the full path (e.g. `/your-path/index.html`)
- Must add `allow all;` — otherwise inherits `deny all` from parent server block
- Don't append blindly after the last `}` — must be INSIDE the server block
- Always `nginx -t` before reload
- Use `sed -i` or write to temp file + cp, not `>>` append (risks placing location outside server block)

## Existing Deployments

- `/ratatouille/` → `<USER_HOME>/ai-stack/ratatouille/landing/`
- `/hub/` → `<USER_HOME>/ai-stack/ai-agent-hub/web/`
- `/bots/` → `<USER_HOME>/ai-stack/hermes-bots-landing/` (Hermes Bots landing page)
- `/hermes/` → proxy to localhost:9119 (basic auth protected)

## HermesBro.cloud (Separate Nginx Config)

hermesbro.cloud has its OWN nginx config at `/etc/nginx/sites-enabled/hermesbro.cloud`,
separate from the stack config. Root = `<NGINX_ROOT_DIR>/` (NOT `<NGINX_HTML_DIR>/`).

Deploy pattern:
```bash
# HTML
cp landing.html <NGINX_ROOT_DIR>/index.html

# Static assets (images, PFPs, etc.)
mkdir -p <NGINX_ROOT_DIR>/bot-profiles/
cp *.png <NGINX_ROOT_DIR>/bot-profiles/

# Permissions
chmod 644 <NGINX_ROOT_DIR>/**/*.html <NGINX_ROOT_DIR>/**/*.png
chown www-data:www-data <NGINX_ROOT_DIR>/**/*.html <NGINX_ROOT_DIR>/**/*.png
```

Verify: `curl -sI https://hermesbro.cloud/bot-profiles/image.png` must return `Content-Type: image/png`.
If it returns `text/html`, the path is wrong (catch-all rewrite serves index.html).

## Landing Page URLs

- Hermes Bots: https://<DOMAIN>/bots/
- HermesBro: https://hermesbro.cloud (root: <NGINX_ROOT_DIR>/)
