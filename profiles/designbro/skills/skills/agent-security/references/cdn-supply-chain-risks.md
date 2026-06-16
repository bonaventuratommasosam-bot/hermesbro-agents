# CDN Supply Chain Risks

## What to Check

When reviewing HTML files, search for `<script>` and `<link>` tags loading from CDNs:

```bash
grep -n 'cdn.jsdelivr.net\|cdnjs.cloudflare.com\|unpkg.com\|ajax.googleapis.com' /path/to/file.html
```

For each CDN resource found:
1. Check if `integrity` attribute is present (SRI hash)
2. Check if `crossorigin="anonymous"` is present
3. Check if version is pinned (e.g., `@4.4.7` vs `@latest`)

## Common Findings

| CDN Resource | Typical Issue |
|---|---|
| Chart.js | Loaded without SRI in most landing pages |
| Bootstrap | Often `@latest` — unpinned |
| jQuery | Legacy sites use very old versions |
| Google Fonts | `@import` loads multiple sub-resources without SRI |

## Remediation

**Option 1 — Add SRI:**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"
  integrity="sha384-HASH_HERE"
  crossorigin="anonymous"></script>
```
Generate hash: `openssl dgst -sha384 -binary file.js | openssl base64 -A`

**Option 2 — Self-host:**
Download the file, serve from same origin. Eliminates CDN trust dependency.

**Option 3 — CSP with CDN allowlist:**
```
script-src 'self' https://cdn.jsdelivr.net;
```
Doesn't prevent CDN compromise but limits attack surface to allowed CDNs only.

## Google Fonts Special Case

`@import url('https://fonts.googleapis.com/...')` loads a CSS file which in turn loads multiple font files from `fonts.gstatic.com`. Each is a separate trust boundary. SRI is not practical for Google Fonts because the CSS content changes. Options:
- Accept the risk with CSP restrictions
- Self-host fonts (download woff2 files, serve locally)
- Use `font-display: swap` to prevent FOIT
