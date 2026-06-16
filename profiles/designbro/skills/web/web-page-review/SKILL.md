---
name: web-page-review
description: "Review websites for legitimacy, design quality, copy, pricing, SEO, and technical health. Structured audit for landing pages, SaaS sites, and client properties."
version: 1.0.0
author: gribbito
tags: [web, review, audit, landing-page, seo, design, legitimacy]
metadata:
  hermes:
    trigger: "review this site, is this site real, check this website, audit this page, landing page review, is this legit, a cosa serve, what does this do, parallelo con, how does this compare, vs, comparison with"
---

# Web Page Review

Structured review of websites covering legitimacy, design, copy, pricing, SEO, and technical health. Use when [REDACTED — dati personali rimossi] shares a URL and asks "is this real?" or "what do you think?"

---

## Review Framework

### 1. Legitimacy Check (when asked "is this real?")

Run these in parallel:

```bash
# Company background
web_search("[company name] founder CEO funding raised")
web_search("[company name] scam review complaints")

# Domain/registration
whois [domain]

# If crypto/token related
web_search("[token name] [ticker] crypto token listed")
# Check CoinGecko, CoinMarketCap, Coinbase listings
```

**Green flags:**
- Real founders with LinkedIn profiles
- VC funding (TechCrunch, Crunchbase coverage)
- Regulatory licenses (MAS, FCA, SEC, etc.)
- SOC 2 / ISO certifications
- Listed on major exchanges/platforms
- Physical address, real team page

**Red flags:**
- No identifiable founders
- Only crypto Twitter hype, no press
- Copied content from other sites
- No terms/privacy policy
- Recently registered domain with no history
- "Too good to be true" returns

### 2. Design Quality

Check programmatically:

```javascript
// In browser console
(() => {
  const s = getComputedStyle(document.body);
  const colors = new Set();
  document.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.color !== 'rgb(0, 0, 0)') colors.add(cs.color);
    if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'rgb(255, 255, 255)')
      colors.add('bg:' + cs.backgroundColor);
  });
  return {
    bgColor: s.backgroundColor,
    font: s.fontFamily,
    colorCount: colors.size,
    colors: [...colors].slice(0, 15),
    svgs: document.querySelectorAll('svg').length,
    images: document.querySelectorAll('img').length,
    viewport: document.querySelector('meta[name="viewport"]')?.content,
    smoothScroll: getComputedStyle(document.documentElement).scrollBehavior,
    htmlSizeKB: Math.round(document.documentElement.outerHTML.length / 1024)
  };
})()
```

**Evaluate:**
- Color palette: cohesive? Too many colors (>10 = messy)?
- Typography: professional font? Consistent sizing?
- Responsive: viewport meta present?
- Images: present? Optimized? Alt text?
- Animations: tasteful or missing?
- Dark/light: consistent theme?

### 3. Copy Quality

**Check:**
- Hero: clear value proposition in <10 words?
- CTA: single clear action above the fold?
- Features: benefit-focused (not feature-focused)?
- Social proof: testimonials, logos, numbers?
- Language: matches target audience?
- Typos/grammar: any errors?

### 4. Pricing Review

**Check:**
- Clear tiers (3 is standard)?
- Anchor pricing (middle tier highlighted)?
- Feature differentiation clear?
- Free trial / freemium?
- Hidden costs mentioned?
- Competitor comparison possible?

### 5. SEO & Meta

```bash
# Check meta tags
curl -sL "https://example.com" | grep -oP '<meta[^>]*>'

# Check OG tags
curl -sL "https://example.com" | grep -i "og:" | head -10

# Check robots.txt and sitemap
curl -sL "https://example.com/robots.txt"
curl -sL "https://example.com/sitemap.xml"

# Check llms.txt (new standard)
curl -sL "https://example.com/llms.txt"
```

**Evaluate:**
- Title tag: <60 chars, includes brand?
- Meta description: <160 chars, compelling?
- OG tags: title, description, image?
- Favicon: present?
- robots.txt: present?
- sitemap.xml: present?
- llms.txt: present? (forward-looking)

### 6. Technical Health

```bash
# Response headers
curl -sI "https://example.com"

# SSL check
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Page size
curl -sL "https://example.com" | wc -c

# Performance hint (number of external resources)
curl -sL "https://example.com" | grep -c 'src="http\|href="http'
```

**Evaluate:**
- HTTPS: valid cert?
- Cache headers: appropriate? (static = long cache, dynamic = no-cache)
- Page size: <500KB ideal for landing page
- External requests: too many? (CDN, fonts, analytics)
- Security headers: X-Frame-Options, CSP, HSTS?

---

## Output Template

```
## Review: [SITE NAME]

**URL:** https://example.com
**Date:** YYYY-MM-DD

### Legitimacy
- Company: [real/shady/unknown]
- Founders: [names if found]
- Funding: [amount, investors]
- Regulation: [licenses]

### Design — X/10
- [observations]

### Copy — X/10
- [observations]

### Pricing — X/10
- [observations]

### SEO — X/10
- [observations]

### Technical — X/10
- [observations]

### Bottom line
[1-2 sentence verdict]

### Action items (if relevant)
1. [fix]
2. [fix]
```

---

## GitHub Repository Review (when [REDACTED — dati personali rimossi] shares a github.com link)

Repo evaluation is different from website review — focus on **adoption fit**, not design.

### Extraction Method
GitHub blocks `web_extract` — use `curl` on raw README instead:
```bash
curl -sL https://raw.githubusercontent.com/OWNER/REPO/main/README.md | head -200
```
If README is long, also `tail -200` for the bottom half (contributing, license, changelog).

### Assessment Framework

**1. Identity & Trust**
- Is the name misleading? ("Anthropic X" when not from Anthropic = red flag)
- Real author? Check profile, other repos, contribution history
- Organization-backed or solo?

**2. Traction Signals**
- Stars + forks (1k+ stars = notable, 10k+ = major)
- Issues/PR activity — open vs closed ratio, response time
- Last commit — weeks = active, months = stale, years = abandoned
- Release cadence

**3. Content Quality**
- README substance vs marketing fluff
- Real examples or just descriptions?
- Documentation quality (wiki, CONTRIBUTING.md, SECURITY.md)
- Code samples — do they actually work?

**4. License & Compatibility**
- Apache 2.0 / MIT = safe for commercial use
- GPL = copyleft — viral, may affect our code
- No license = assume proprietary, do NOT use
- Check LICENSE file, not just README badge

**5. Security & Supply Chain**
- Check for `install` scripts in package.json / setup.py
- Look for `curl | bash` patterns in install instructions
- Evaluate dependency count — fewer is better
- For npm: check weekly downloads, maintainer count

**6. Platform Fit**
- Compatible with our stack? (Hermes Agent, Python, Node)
- Does it require infrastructure we don't have?
- Does it overlap with something we already use?

### Output Template
```
## Repo Review: [NAME]
**URL:** https://github.com/...
**Stars/Forks:** Xk / Xk
**License:** [type]
**Last active:** [date]

### What it is (2-3 lines)
### Strengths
### Concerns
### Bottom line — adopt / watch / skip
```

---

## Parallel Security Code Audit (MUST DO for [REDACTED — dati personali rimossi]'s own sites)

When [REDACTED — dati personali rimossi] asks to audit a site he owns (hermesbro.cloud, any bot landing page), ALWAYS run both audits in parallel via `delegate_task`:

1. **Web review** (browser + curl): design, copy, SEO, headers
2. **Security code audit** (read_file + terminal): secrets, XSS vectors, SRI, external resources, nginx config

Use `delegate_task` with batch tasks array — both run concurrently, results come back together. This is faster and more thorough than sequential.

Common findings on [REDACTED — dati personali rimossi]'s static landing pages:
- Missing security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- CDN scripts without SRI (supply chain risk)
- Cache-Control: no-store on static pages (should be max-age=3600)
- robots.txt/sitemap.xml returning HTML due to Nginx try_files fallback
- Inline event handlers that would break a strict CSP
- Fake/generated data presented as real metrics

## Quick Purpose Summary (when asked "a cosa serve?" / "what does this do?")

NOT a full audit. Give a 3-5 line answer:
- What it is (1 sentence)
- Who it's for (target user/customer)
- Core value proposition
- Realistic assessment (product vs manifesto vs vaporware)

Keep it direct. [REDACTED — dati personali rimossi] doesn't want a sales pitch — he wants to know if it's real.

## Competitive Comparison (when asked "parallelo con X?" / "how does this compare?")

When [REDACTED — dati personali rimossi] asks for a comparison between two products:

1. **Search both** — web_search for each product's background, funding, traction
2. **Structure the comparison:**
   - Brief recap of each (2-3 lines)
   - Similarities (shared narrative, market, tech approach)
   - Key differences (business model, stage, credibility)
   - Verdict: which is more real/interesting
3. **Keep it tight** — [REDACTED — dati personali rimossi] wants signal, not a Gartner report
4. **Score realism** — manifesto vs MVP vs live product

---

## Pitfalls

- **Don't over-investigate minor sites** — if [REDACTED — dati personali rimossi] just wants a quick "is this real?", 2-3 web searches suffice. Full audit only when asked.
- **Respect [REDACTED — dati personali rimossi]'s design taste** — he doesn't want replicas of other sites. When reviewing his own pages, focus on what's missing (images, animations, meta tags) rather than comparing to references.
- **Cache headers on static landing pages** — `no-store, no-cache` is wrong for static HTML. Use `max-age=3600` or similar. Flag this when you see it.
- **Single-file landing pages** — check file size. >50KB for a landing page HTML is heavy. Look for inline CSS/JS that could be external.
- **Crypto sites require extra skepticism** — check exchange listings, team identity, contract address. Many "legitimate-looking" sites are fronts.
- **GitHub blocks web_extract** — always use `curl -sL https://raw.githubusercontent.com/OWNER/REPO/main/README.md` for README content. Browser navigate works but is slower for simple content retrieval.
- **Nginx try_files fallback** — when checking `robots.txt` and `sitemap.xml`, if they return HTML content instead of expected formats, the Nginx `try_files` directive is falling back to `index.html`. Flag this: the files need to be created as actual static files, not routed through the SPA fallback.
- **Chart.js fake data** — if a page generates random data (`Math.random()`) and displays it as real metrics (uptime, performance), flag it as misleading even if not a technical vulnerability. Trust issue.
- **CSP vs inline handlers** — when recommending security fixes, check for `onclick`, `onmouseover`, `onload` etc. BEFORE recommending CSP. A strict CSP blocks inline event handlers. Two options: (1) migrate handlers to `addEventListener` first, then add CSP; or (2) use `'unsafe-inline'` in `script-src` which weakens CSP. Always flag this ordering dependency in action items — "add CSP" without "remove inline handlers" will break the page.
- **Nginx `add_header` inheritance** — `add_header` in a `location` block REPLACES all server-level headers. When adding location-specific headers (e.g., Cache-Control for `/agents/`), repeat the security headers too. Common mistake: adding `Cache-Control` in a location block and losing CSP/HSTS.
- **Community projects with big-org names** — "Anthropic X", "Google Y", "OpenAI Z" in repo names are often community projects, not official. Always check the actual org/author before assuming affiliation.
