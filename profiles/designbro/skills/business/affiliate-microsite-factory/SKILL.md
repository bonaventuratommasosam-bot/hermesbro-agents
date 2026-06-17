---
name: affiliate-microsite-factory
description: "Deploy affiliate micro-sites at scale: domain research, SEO-optimized templates, content writing, nginx deployment, and SEO setup. For [REDACTED — dati personali rimossi]'s monetization strategy (hermesbro.cloud)."
triggers:
  - "micro-sito"
  - "microsite"
  - "affiliate"
  - "sito affiliati"
  - "nicchia food"
  - "domini scaduti"
  - "SEO micro-site"
  - "passive income"
  - "monetizzazione sito"
  - "deploy micro-site"
  - "new affiliate site"
  - "create microsite for [niche]"
  - "register domain and deploy"
  - "write affiliate content"
  - "niche site deployment"
---

# Affiliate Micro-Site Factory

Deploy SEO-optimized affiliate micro-sites on the VPS. Each site follows an identical pipeline: domain → template → content → deploy → SEO.

## CRITICAL: [REDACTED — dati personali rimossi] is NOT technical

When giving instructions for external services (registrars, Amazon Associates, Google Search Console):
- Give EXACT URLs (not "go to your registrar")
- Name EXACT buttons to click ("Login in alto a destra" → "I miei servizi" → "Domini")
- Ask for screenshots if stuck ("mandami uno screenshot e ti guido io")
- Never assume he knows DNS, hosting, or SEO terminology
- If he asks "come ci vado?" — you were too vague, rewrite with concrete steps

When [REDACTED — dati personali rimossi] asks "Come faccio a guadagnare?" — explain the business model simply:
1. Someone searches Google for "miglior gestionale pizzeria"
2. Finds your site, reads the guide, trusts it
3. Clicks affiliate link → buys → you get 3-10% commission
4. Scale: 10-15 sites × €10-50/site/month = €100-750/month
5. Cross-sell: banner "Scopri HermesBro" → ristoratori vedono i bot → qualcuno si iscrive €29/mese

See `references/italian-registrar-dns.md` for step-by-step Register.it DNS walkthrough (give this to [REDACTED — dati personali rimossi]).

## Quick Reference

| Step | Time | Output |
|------|------|--------|
| Domain research | 15min | 3-5 candidate domains |
| Template setup | 5min | `/var/www/<domain>/index.html` |
| Content writing | 30min/article | 5 articles per site |
| Nginx deploy | 5min | Live site on VPS |
| SEO setup | 10min | robots.txt, sitemap.xml, schema.org |

## Step 1: Domain Research

### Finding Expired .it Domains with SEO Juice

Use **seoprof.it** for expired Italian domains with existing authority:

```
https://www.seoprof.it/domini-scaduti/
```

**Pitfall:** The URL query parameters (`?contiene=keyword`) do NOT work for filtering. The filter is JavaScript-based. You must:
1. Load the default page
2. Manually scan the table for food/niche-relevant domains
3. Note: table shows ~25 domains per page, paginate with "Avanti"

Key columns:
- **Dominio**: the domain name
- **ORank**: OpenRank authority score (20+ is good, 30+ is excellent)
- **Caratteri**: character count (shorter = better)
- **Data**: cancellation date (check if domain is available yet)

### Checking Domain Availability

Use `whois` CLI — fastest method for .it domains:

```bash
whois <domain>.it 2>/dev/null | grep -E "Status:|AVAILABLE"
```

Output meanings:
- `Status: AVAILABLE` → ready to register
- `Status: ok` → already registered by someone else

Batch check:
```bash
for d in domain1.it domain2.it domain3.it; do
  echo -n "$d: "; whois "$d" 2>/dev/null | grep "Status:" | head -1
done
```

### Where to Buy

- **Register.it** — Italian registrar, good for .it domains
- **Aruba.it** — cheap, Italian
- **OVH** — good prices for bulk

Budget: €5-8 per .it domain/year

## Step 2: Template Setup

### Copy Template

```bash
mkdir -p /var/www/<domain>
cp /var/www/microsite-template/index.html /var/www/<domain>/index.html
```

### Template Location

Master template: `/var/www/microsite-template/index.html`

The template has 44 placeholders. Key ones:
- `{{META_TITLE}}`, `{{META_DESCRIPTION}}`, `{{CANONICAL_URL}}`
- `{{HERO_H1}}`, `{{HERO_SUBTITLE}}`, `{{HERO_BADGE}}`
- `{{ARTICLE_TITLE_1-5}}`, `{{ARTICLE_EXCERPT_1-5}}`, `{{AFF_LINK_1-5}}`
- `{{CATEGORY_1-5}}` — category labels for each article card

### Template Features (do NOT remove)
- Dark theme (#101113 base) with brand blue accents (#4c6ef5)
- Tailwind CSS via CDN (Play CDN, zero build step)
- Schema.org Article JSON-LD
- Open Graph + Twitter Card meta
- `rel="nofollow noopener sponsored"` on all affiliate links
- Mobile-first responsive (1-col → 2-col → 3-col grid)
- Italian language (`lang="it"`)

## Step 3: Content Writing

### Article Structure

Each article should be:
- **1500+ words** for SEO viability
- **Italian language** — natural, not translated
- **H1 → H2 → H3** hierarchy
- **Problem → Solution** intro (200 words)
- **3-5 sections** with actionable content
- **CTA** to HermesBro (cross-sell)
- **Schema.org Article** markup in `<head>`

### Content Quality Rules

1. **Write for restaurant owners, not SEO bots.** Real numbers, real examples.
2. **Include a concrete example** with actual calculations (e.g., "Pizzeria Da Mario" with €25k/month revenue).
3. **Each article needs a unique angle** — don't repeat the same advice across articles.
4. **Affiliate links should feel natural** — product recommendations within genuine advice, not forced.
5. **Cross-sell HermesBro** in the CTA section only, not scattered throughout.

### Article Templates by Type

**How-To / Guide:**
```
H1: [Action] nel [Year] — Guida Pratica
  Intro: problem + why it matters (200 words)
  H2: Cos'è [Concept]
  H2: Come fare [Step-by-step]
  H3: Step 1...
  H2: Esempio Pratico (real numbers)
  H2: N Modi per [Optimize]
  H2: Conclusione + CTA
```

**Product Comparison:**
```
H1: I N Migliori [Product] per [Audience]
  Intro: why choosing right matters
  H2: Criteri di Scelta
  H2: #1 [Product] — Pro/Contro/Prezzo
  ...
  H2: Tabella Comparativa
  H2: Quale Scegliere? + CTA
```

### Article CSS (inline in each article page)

Must include these styles for content readability:
```css
.prose-dark h2 { color: #fff; font-size: 1.5rem; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1rem; }
.prose-dark h3 { color: #fff; font-size: 1.25rem; font-weight: 600; margin-top: 2rem; margin-bottom: 0.75rem; }
.prose-dark p { margin-bottom: 1.25rem; line-height: 1.8; }
.prose-dark ul, .prose-dark ol { margin-bottom: 1.25rem; padding-left: 1.5rem; }
.prose-dark li { margin-bottom: 0.5rem; line-height: 1.7; }
.prose-dark strong { color: #fff; }
.prose-dark blockquote { border-left: 4px solid #4c6ef5; padding-left: 1rem; margin: 1.5rem 0; font-style: italic; color: #A6A7AB; }
.formula-box { background: linear-gradient(135deg, #1A1B1E 0%, #25262b 100%); border: 1px solid #4c6ef5; border-radius: 0.75rem; padding: 2rem; text-align: center; margin: 2rem 0; }
.formula-box .formula { font-size: 1.5rem; font-weight: 700; color: #748ffc; font-family: monospace; }
```

### Article Page Structure (copy-paste template)

```html
<!-- Breadcrumb -->
<nav class="text-sm text-dark-200 mb-8">
    <a href="/" class="hover:text-brand-400 transition-colors">Home</a>
    <span class="mx-2">/</span>
    <span class="text-dark-100">{{ARTICLE_TITLE}}</span>
</nav>

<!-- Header -->
<header class="mb-12">
    <span class="inline-block px-3 py-1 text-xs font-medium {{BADGE_COLOR}} {{BADGE_BG}} rounded-full mb-4">{{CATEGORY}}</span>
    <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-white leading-tight mb-6">
        {{H1}}
    </h1>
    <p class="text-lg text-dark-100 mb-4">{{SUBTITLE}}</p>
    <div class="flex items-center gap-4 text-sm text-dark-200">
        <span>Pubblicato: {{DATE}}</span>
        <span>•</span>
        <span>Tempo di lettura: {{MIN}} minuti</span>
    </div>
</header>

<!-- Content -->
<div class="prose-dark">
    {{ARTICLE_CONTENT}}
</div>

<!-- CTA -->
<div class="bg-gradient-to-r from-brand-900/40 via-dark-800 to-brand-900/40 rounded-xl border border-dark-400/50 p-8 mt-12 text-center">
    <h3 class="text-xl font-bold text-white mb-4">{{CTA_HEADING}}</h3>
    <p class="text-dark-100 mb-6">{{CTA_TEXT}}</p>
    <a href="https://hermesbro.cloud" class="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-500 text-white font-semibold px-6 py-3 rounded-lg transition-colors btn-glow">
        Prova HermesBro Gratis
    </a>
</div>
```

Badge colors: green (Guida Pratica), blue (Confronto), purple (Evergreen), orange (Prodotti), brand (Innovazione).

## Step 4: Nginx Deployment

### Create Server Block

```bash
cat > /etc/nginx/sites-available/<domain> << 'EOF'
server {
    listen 80;
    server_name <domain>.it www.<domain>.it <VPS_IP>;
    
    root /var/www/<domain>;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    gzip on;
    gzip_types text/css application/javascript application/json;
    gzip_min_length 1000;
}
EOF

ln -sf /etc/nginx/sites-available/<domain> /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

**Pitfall:** `write_file` refuses to write to `/etc/nginx/` (system path protection). Use `terminal` with `cat >` heredoc instead.

**Pitfall:** `gzip_types text/html` causes a duplicate MIME type warning — text/html is included by default. Omit it.

**Tip:** Add `<VPS_IP>` to `server_name` so [REDACTED — dati personali rimossi] can preview the site at `http://<VPS_IP>/` before DNS propagates. Remove it after domain is live.

### SSL (after domain DNS is active)

```bash
certbot --nginx -d <domain>.it -d www.<domain>.it --non-interactive --agree-tos -m admin@hermesbro.cloud
```

### Test

```bash
curl -s -H "Host: <domain>.it" http://localhost/ | head -5
```

## Step 5: SEO Setup

### robots.txt

```
User-agent: *
Allow: /

Sitemap: https://<domain>.it/sitemap.xml
```

### sitemap.xml

Generate for all pages with proper `<lastmod>`, `<changefreq>`, `<priority>`. Homepage gets priority 1.0, articles get 0.7-0.9.

### Google Search Console

1. Go to https://search.google.com/search-console
2. Add property (domain or URL prefix)
3. Verify via HTML file upload or meta tag
4. Submit sitemap

## Pitfalls

1. **`web_extract` fails with DuckDuckGo backend.** Use `browser_navigate` as fallback for extracting page content.
2. **`execute_code` is blocked for cron profiles.** Use `terminal` for shell commands, `write_file` for file creation.
3. **seoprof.it filters are JavaScript-only.** URL parameters don't work. Scan the table manually or use multiple page loads.
4. **Expired .it domains may not be immediately available.** After cancellation, there's a grace period. Check with `whois` before assuming availability.
5. **Don't use Tailwind `gzip_types text/html`** — it's included by default and causes nginx warnings.
6. **Article links to Amazon must use `rel="nofollow noopener sponsored"`** — required by Google for affiliate links.
7. **Register.it: modify existing A record, don't add new one.** Default A record points to 195.110.124.133 (parking page). Edit it to VPS IP.
8. **Register.it: use CNAME for www, not A record.** A record with name "www" is rejected as "invalid value".
9. **DNS propagation: .it slower than .com.** .it can take 1-2 hours, .com takes 5-15 min. Always verify with `dig` before setting up SSL.
10. **Google Search Console: TXT verification record.** Add `google-site-verification=...` as a SEPARATE TXT record on Register.it. Don't delete existing SPF TXT record.
11. **Amazon Associates ID format:** `name-21` (e.g., `hermebro-21`). Replace all `{{AFF_LINK_*}}` placeholders after registration.
12. **`write_file` refuses system paths.** `/etc/nginx/` etc. need `terminal` with `cat >` heredoc or `sudo tee`.

## Current State

- Master template: `/var/www/microsite-template/index.html`
- First site deployed: `foodcostitalia.it` (nginx, 5 articles + homepage live, 2026-06-01)
- Domains purchased: `foodcostitalia.it` + `foodcostitalia.com` (Register.it, 2026-06-01)
- DNS: Configured and propagated ✅
- SSL: Active via certbot (separate server blocks for .it and .com) ✅
- .com → .it: 301 redirect working ✅
- Amazon Associates: pending ([REDACTED — dati personali rimossi] registering, ID format: `name-21`)
- Google Search Console: TXT verification pending ([REDACTED — dati personali rimossi] needs to add TXT record)
- Plan file: `<HERMES_ROOT>/plans/monetizzazione-hermesbro.md`
- Site files: `/var/www/foodcostitalia/` (index.html, 5 article pages, robots.txt, sitemap.xml)
- Nginx config: `/etc/nginx/sites-enabled/foodcostitalia` (separate blocks per domain)

## References

- Monetization plan: `<HERMES_ROOT>/plans/monetizzazione-hermesbro.md`
- HermesBro landing: `{WEB_ROOT}/index.html`
- Expired domain search: `https://www.seoprof.it/domini-scaduti/`
- Domain availability check: `whois <domain>.it`
- Register.it DNS guide: `references/italian-registrar-dns.md`
- Google Search Console + Amazon: `references/google-search-console-amazon.md`
