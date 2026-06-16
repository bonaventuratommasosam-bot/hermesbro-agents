# Nginx Security Headers — Template & Workflow

## CSP Template for Static Landing Pages

When adding CSP to a static HTML site that uses Chart.js + Google Fonts:

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; connect-src 'self';" always;
```

**Key decisions:**
- `'unsafe-inline'` in `script-src` — required when page has `<script>` blocks without nonces. For pages with inline event handlers (`onclick`, `onmouseover`), this is mandatory. Remove if all JS is external + nonced.
- `'unsafe-inline'` in `style-src` — required when page has inline `style=` attributes or `<style>` blocks (common in single-file landing pages).
- `https://cdn.jsdelivr.net` — whitelists Chart.js CDN. Add other CDNs as needed.
- `https://fonts.googleapis.com` + `https://fonts.gstatic.com` — required for Google Fonts `@import`.
- `data:` in `font-src` — some font loading techniques use data: URIs.
- `https:` in `img-src` — allows images from any HTTPS source (common for landing pages with external images).
- `connect-src 'self'` — restricts fetch/XHR to same origin only.

## Full Security Headers Block

```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; connect-src 'self';" always;
```

## SRI Hash Generation

```bash
# Generate SRI hash for a CDN resource
curl -sL "https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js" | openssl dgst -sha384 -binary | openssl base64 -A

# Result: sha384-BASE64HASH
# Apply:
# <script src="..." integrity="sha384-BASE64HASH" crossorigin="anonymous"></script>
```

**Pitfall:** The `crossorigin="anonymous"` attribute is REQUIRED for SRI to work. Without it, the browser skips integrity verification silently.

## CSP Debugging

When CSP blocks legitimate resources:
1. Open browser DevTools → Console
2. Look for `Refused to load/connect/apply because it violates the following Content Security Policy directive: ...`
3. Add the blocked origin to the appropriate directive
4. Common fixes:
   - Google Fonts CSS blocked → add to `style-src`
   - Google Fonts font files blocked → add to `font-src`
   - Inline script blocked → add `'unsafe-inline'` to `script-src` (or use nonces)
   - Inline style blocked → add `'unsafe-inline'` to `style-src`

## Nginx Config Pitfalls

- **`add_header` in location blocks overrides server-level headers** — if a `location` block has its own `add_header`, it replaces ALL server-level `add_header` directives. You must repeat the security headers in each location block that has custom headers.
- **`try_files` fallback** — `try_files $uri $uri/ /index.html` causes robots.txt, sitemap.xml, security.txt to serve HTML. Create dedicated `location = /robots.txt` blocks with direct `root` serve.
- **Cache-Control on static HTML** — use `no-cache` (revalidate) not `no-store` (never cache). For static assets (CSS/JS/images), use `max-age=86400` (1 day) or `max-age=2592000` (30 days).
