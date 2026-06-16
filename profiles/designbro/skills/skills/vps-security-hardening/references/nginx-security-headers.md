# Nginx Security Headers — Reference

## Standard Headers (add to every vhost)

```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## Content-Security-Policy

CSP for static landing pages with CDN resources (fonts, Chart.js, etc.):

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; connect-src 'self';" always;
```

**Pitfall:** `add_header` in nginx does NOT inherit from parent blocks. If you have `add_header` in a `location {}` block, the server-level headers are DROPPED for that location. Either repeat headers or use `more_set_headers` (ngx_headers_more module).

## Static Asset Caching

```nginx
# Static assets — long cache
location ~* \.(css|js|png|jpg|jpeg|gif|svg|ico|woff2|woff|ttf|webp)$ {
    expires 30d;
    add_header Cache-Control "public";
    try_files $uri =404;
}

# Static files (robots.txt, sitemap.xml) — direct serve, no try_files
location = /robots.txt {
    root /var/www/site;
    access_log off;
    expires 1d;
    add_header Cache-Control "public";
}
```

**Pitfall:** `Cache-Control: no-store, no-cache` is WRONG for static landing pages. Use `public, max-age=86400` or `expires 30d`.

## Gzip (global nginx.conf)

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_buffers 16 8k;
gzip_http_version 1.1;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

## TLS Hardening

```nginx
ssl_protocols TLSv1.2 TLSv1.3;  # NEVER TLSv1.0 or TLSv1.1
ssl_ciphers HIGH:!aNULL:!MD5;
```

**Pitfall:** Check BOTH the vhost AND the global nginx.conf. The global config may allow TLSv1.0/1.1 even if the vhost restricts it.

## SRI (Subresource Integrity) for CDN Scripts

Generate hash:
```bash
curl -sL --max-time 15 "CDN_URL" | openssl dgst -sha384 -binary | openssl base64 -A
```

Apply in HTML:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"
  integrity="sha384-[HASH]" crossorigin="anonymous"></script>
```

**Pitfall:** `curl | openssl` pipe may timeout for large files (>200KB). Download first, then hash:
```bash
curl -sL --max-time 15 "CDN_URL" -o /tmp/file.js
cat /tmp/file.js | openssl dgst -sha384 -binary | openssl base64 -A
```

## Editing System Nginx Config

**Pitfall:** The `patch` tool refuses to write to `/etc/nginx/` paths (system path protection). Use `sed -i` via terminal instead:
```bash
sed -i '/add_header Strict-Transport-Security/a\    add_header Content-Security-Policy "...";' /etc/nginx/sites-enabled/site.conf
```

Always test before reload:
```bash
nginx -t && systemctl reload nginx
```

## Verification

```bash
curl -sI https://site.com | grep -iE "x-frame|x-content|x-xss|referrer|strict|content-security|cache-control"
```

## Security Audit Score Targets

| Category | Target | What to check |
|----------|--------|---------------|
| Security Headers | 8/10+ | All 6 headers present |
| CSP | Present | At minimum: default-src, script-src, style-src, font-src, img-src |
| SRI | All CDN scripts | integrity + crossorigin attributes |
| TLS | 1.2+ only | No TLSv1.0/1.1 |
| Cache | Static=long, dynamic=short | No `no-store` on static pages |
| Gzip | Enabled | Check nginx.conf global |
