---
name: affiliate-microsite-deploy
description: Deploy affiliate micro-sites on the VPS — domain, nginx, SSL, content, SEO. Repeatable workflow for the foodcostitalia.it pattern.
triggers:
  - micro-site deployment
  - affiliate site setup
  - new niche site
  - deploy microsite
---

# Affiliate Micro-Site Deployment

Repeatable workflow to launch a new affiliate micro-site on [REDACTED — dati personali rimossi]'s VPS.

## Prerequisites

- Domain registered ([REDACTED — dati personali rimossi] handles on Register.it)
- DNS A record → `194.146.12.219` (VPS IP)
- Template at `/var/www/microsite-template/index.html`

## Steps

### 1. Domain & DNS

After [REDACTED — dati personali rimossi] registers the domain on Register.it:
- He needs to go to DNS zone editor and set:
  - A record: `@` → `194.146.12.219`
  - CNAME: `www` → domain.tld
- Register.it quirk: **edit existing A record** (don't add new one — duplicate A records fail)
- Register.it quirk: some domains have no active DNS zone — must first enable "Usa i DNS di Register.it" under DNS config
- DNS propagation: .it domains take 15-60 min. Verify with `dig +short DOMAIN A @ns1.register.it`
- [REDACTED — dati personali rimossi] struggles with registrar UIs — give exact click-by-click instructions

### 2. Verify DNS Propagation

```bash
dig +short DOMAIN A @8.8.8.8
dig +short DOMAIN A @ns1.register.it  # check authoritative NS directly
```

### 3. Nginx Config

```nginx
server {
    listen 80;
    server_name DOMAIN www.DOMAIN;
    root /var/www/SITENAME;
    index index.html;
    location / { try_files $uri $uri/ /index.html; }
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ { expires 30d; }
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    gzip on;
    gzip_types text/css application/javascript application/json;
    gzip_min_length 1000;
}
```

Save to `/etc/nginx/sites-available/SITENAME`, symlink to sites-enabled, test with `nginx -t && systemctl reload nginx`.

### 4. SSL (Let's Encrypt)

```bash
certbot --nginx -d DOMAIN -d www.DOMAIN --non-interactive --agree-tos --email admin@DOMAIN --redirect
```

For multiple domains on same site, run certbot per domain then fix nginx config to use separate server blocks with correct cert paths. See `/etc/nginx/sites-enabled/foodcostitalia` for the pattern.

### 5. Content

- Copy template → `/var/www/SITENAME/index.html`
- Replace all `{{PLACEHOLDER}}` values
- Write 5 article pages (1200+ words each, Italian, SEO-optimized)
- Each article needs: Schema.org Article JSON-LD, OG meta, canonical URL, prose-dark content, CTA to hermesbro.cloud
- Add `robots.txt` and `sitemap.xml`

### 6. SEO Files

- `robots.txt`: `User-agent: * / Allow: / / Sitemap: https://DOMAIN/sitemap.xml`
- `sitemap.xml`: all pages with priority and changefreq

## Template Placeholders

See `/var/www/microsite-template/index.html` for the full list. Key ones:
- `{{META_TITLE}}`, `{{META_DESCRIPTION}}`, `{{CANONICAL_URL}}`
- `{{HERO_H1}}`, `{{HERO_SUBTITLE}}`, `{{HERO_BADGE}}`
- `{{ARTICLE_TITLE_1-5}}`, `{{ARTICLE_EXCERPT_1-5}}`, `{{AFF_LINK_1-5}}`

## Architecture: .com redirect to .it

When [REDACTED — dati personali rimossi] registers both .com and .it:
- .it = primary (serves content, SEO canonical)
- .com = redirect 301 → .it (preserves SEO juice)
- Each domain gets its own SSL cert via certbot
- Separate nginx server blocks per domain

See `references/nginx-multidomain-ssl.md` for the nginx config pattern.

## Google Search Console + Amazon Associates

See `references/google-search-console-amazon.md` for step-by-step walkthroughs [REDACTED — dati personali rimossi] can follow.

## Step 7: Google Search Console

### TXT Record Verification (Register.it)

Google requires a TXT record in DNS to verify domain ownership:

1. Go to https://search.google.com/search-console
2. Add property → **Domain** type → enter `domain.it`
3. Google shows a TXT record value like `google-site-verification=ABC123...`
4. **Don't close the Google page** — you need the exact value

Then add the TXT record on Register.it:
1. Login → I miei domini → click domain → **Modifica zona DNS**
2. Click **Aggiungi** (or "Add record")
3. Tipo: **TXT**
4. Nome: **@** (or leave empty)
5. Valore: paste the full `google-site-verification=...` string
6. TTL: **3600**
7. **Salva**

Wait 5-15 min, then click **Verifica** on Google Search Console.

**Pitfall:** Register.it may already have a TXT SPF record (`v=spf1 ...`). Don't delete it — the verification TXT is a separate record.

### After Verification

1. Submit sitemap: `https://domain.it/sitemap.xml`
2. Request indexing for homepage
3. Repeat for `.com` if it redirects to `.it` (Google sees them as separate properties)

## Step 8: Amazon Associates

### Registration
- Go to https://programma-affiliazione.amazon.it
- Register with the site URL (`https://domain.it`)
- Amazon reviews the site (needs real content, not placeholder)
- ID format: `name-21` (e.g., `hermebro-21`)

### Replacing Affiliate Links
After getting the ID, replace all `{{AFF_LINK_*}}` placeholders in articles:
- Product links: `https://www.amazon.it/dp/ASIN?tag=name-21`
- Search links: `https://www.amazon.it/s?k=keyword&tag=name-21`
- All links must have `rel="nofollow noopener sponsored"` (template already includes this)

## Checklist

- [ ] Domain registered + DNS propagated
- [ ] Nginx config live
- [ ] SSL active (check with `curl -sk -o /dev/null -w "%{http_code}" https://DOMAIN/`)
- [ ] Homepage loads with correct title
- [ ] robots.txt + sitemap.xml
- [ ] Google Search Console: add property, verify TXT, submit sitemap
- [ ] Amazon Associates: register, get affiliate ID, replace {{AFF_LINK_*}} placeholders
