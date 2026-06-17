---
name: outbound-email-campaign
description: "Plan, build, and execute outbound cold email campaigns: lead research, sector-specific templates, ESP setup, sending infrastructure, compliance."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [business, email, outbound, sales, leads, marketing]
    related_skills: [himalaya, marketing-materials-workflow, affiliate-microsites]
---

# Outbound Email Campaign

## When to use
- Setting up cold email outreach for a product/service
- Building lead lists by sector
- Writing sector-specific email templates
- Configuring email sending infrastructure (ESP setup)
- Running drip/outbound campaigns

## Campaign structure

### 1. Define target sectors
Pick 3-5 sectors that match the product. For each sector:
- Specific pain points (what keeps them up at night)
- Product/bot that solves it
- Value proposition in 1 sentence

### 2. Build lead list (200+ contacts)
See `references/lead-research.md` for full methodology.

Summary:
- **Google Maps** scraping (Outscraper ~$10/1000) — volume leads
- **LinkedIn Sales Navigator + Apollo.io** — decision-maker contacts
- **PagineGialle** — Italian local businesses with email
- Filter: has website (has digital budget), active reviews, NOT large chains
- Target: 40 leads per sector, 5 cities per sector
- CSV format: `nome,cognome,azienda,settore,email,telefono,sito_web,citta,fonte,stato`

### 3. Write email templates
One template per sector, max 150 words. Structure:
- **Subject line**: question about their specific pain point
- **Opening**: reference their sector pain (1 sentence)
- **Body**: what the product does, 3 bullet points
- **Social proof**: 1 line (e.g. "Partiamo da 99 euro/mese")
- **CTA**: "Prenota una demo di 15 minuti"
- **Signature**: "Nome | Azienda" + website

See `references/email-templates.md` for 5 Italian sector templates (ristoranti, studi legali, e-commerce, startup, PMI).

### 4. Set up sending infrastructure
**CRITICAL: ESP signup requires MANUAL action.** All major ESPs (SendGrid, Resend, Mailgun, Brevo) have CAPTCHA/bot detection on signup pages. Automated browser signup will fail.

**Workflow:**
1. Ask user to create account manually on chosen ESP
2. User provides API key after email verification
3. Configure sending script with API key
4. Verify sender domain/email on ESP

**ESP comparison (free tiers):**

| ESP | Free limit | Needs credit card | Notes |
|-----|-----------|-------------------|-------|
| Brevo (ex-Sendinblue) | 300/day | No | Best free tier for cold outreach |
| SendGrid | 100/day | No | Good deliverability |
| Resend | 100/day | No | Developer-friendly, simple API |
| Mailgun | first 30 days | **Yes** | Not suitable for free startup |

**Recommended**: Brevo (300/day free, no card, good for Italian market).

**Alternative**: VPS Postfix + OpenDKIM as local SMTP. Works well for non-Gmail recipients. With proper DKIM signing + SPF DNS record, deliverability is acceptable for first batches. See `references/postfix-dkim-setup.md` for the exact configuration steps tested on YOUR_VPS_ID.

### 5. Sending best practices
- **Volume ramp**: Start with 20/day, increase by 10/day each week
- **Timing**: Tuesday-Thursday, 9-11 AM target timezone
- **Personalization**: Always use {nome} and reference their sector
- **Follow-up**: 1st follow-up after 3 days, 2nd after 7 days, then stop
- **Unsubscribe**: Always include opt-out link/text (GDPR compliant)
- **Domain warmup**: New sending domains need 2-4 weeks of gradual volume increase
- **SPF/DKIM/DMARC**: Must be configured on sending domain for deliverability

### 6. GDPR compliance (Italian market)
- Include opt-out in every email
- Don't email contacts who already have competing solutions declared
- Legitimate interest basis for B2B cold outreach (Italian law permits this)
- Keep records of consent basis

## Cron Pitfalls for Outreach Scripts
The outreach-engine runs as a `no_agent=True` cron job. Key rules:
- Script field = just filename (`outreach-engine.py`), NOT absolute path
- No arguments in script field (create wrapper `.sh` if needed)
- Scripts must live in `~/.hermes/scripts/` (copy from shared, don't symlink)
- `deliver: origin` if the profile lacks Telegram config
- See `references/cron-job-script-pitfalls.md` for full error cheat sheet

## Verified Outreach Workflow (validated 2026-06-06)

When researching business targets for outreach:

### Step 1: Research via web search
Search for real businesses by sector + city. Use `web` toolset with `delegate_task` for parallel research across categories.

### Step 2: ALWAYS verify URLs
Subagent-researched URLs are frequently wrong (expired domains, incorrect TLDs, redirects to unrelated sites). **NEVER trust a URL without verifying.**

```bash
# Verify each URL returns HTTP 200
curl -sI -o /dev/null -w "%{http_code}" --max-time 5 "https://example.com"
```

- 200 = working, include in verified list
- 301/302 = redirect, follow and check final destination
- 000 = unreachable, discard or mark as "URL da verificare manualmente"
- 403/404 = broken, discard

### Step 3: Scrape contact info
For verified URLs, scrape homepage + contact page for email addresses:
```bash
curl -s "https://example.com" | grep -oiE '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}' | head -5
```

### Step 4: Output verified CSV
Save to `<HERMES_ROOT>/shared/marketing/outreach/verified-targets-YYYY-MM-DD.csv`
Format: `name,company,sector,website,email,notes`
Mark all entries with ✅ in notes to indicate verified status.

**Target**: 20-30 verified targets per batch (not 200+ — quality over volume for initial outreach).

## Email Template Storage

Sector-specific templates go to `<HERMES_ROOT>/shared/marketing/outreach/email-templates-italian.md`.
Use placeholders: `[NOME]`, `[AZIENDA]`, `[SETTORE]`.
Keep under 150 words per email. Italian business tone — direct, no corporate fluff.

## Pitfalls

### Unverified outreach URLs
Subagent-researched business URLs have ~40% failure rate (wrong domains, dead links, redirects to unrelated sites). ALWAYS verify with curl before adding to outreach CSV. A single batch of 18 targets from a subagent returned 7 broken URLs (39% failure rate). This wastes outreach time and damages sender reputation if emails bounce.

### Replacing production content without approval
**NEVER** replace a live website/page without explicit user approval, even if you back it up first. [REDACTED — dati personali rimossi]'s reaction: "torna assolutamente al sito che avevamo prima" — immediate revert demanded. Always deploy new content to a staging path and ask before switching.

### Automated ESP signup
All ESPs block automated signup (Cloudflare Turnstile, reCAPTCHA). Don't waste time trying browser automation or curl — ask the user to sign up manually and provide the API key.

### Sending from VPS directly
Postfix + OpenDKIM on VPS works for Gmail and all major providers **when properly configured**. Requirements:
- SPF DNS TXT record pointing to VPS IP
- DKIM signing via OpenDKIM (verify with `opendkim-testkey -d DOMAIN -s mail -vv`)
- FROM address MUST use the domain with SPF/DKIM (e.g. `name@hermesbro.cloud`), NEVER a Gmail/external address — Gmail always rejects unauthenticated senders via Postfix relay
- Verified working 2026-06-06 on YOUR_VPS_ID: `status=sent` to Gmail with DKIM signature

Check logs: `grep "DKIM-Signature field added" /var/log/mail.log`

See `references/postfix-dkim-setup.md` for config. See `references/outreach-automation.md` for the production pipeline.

### SMTPUTF8 bounce (ProtonMail, some providers)
Email addresses MUST be lowercased before sending. Uppercase chars (e.g. `contact@example.com`) trigger SMTPUTF8 requirement. ProtonMail does not support SMTPUTF8 → email bounces. Always `.strip().lower()` all email addresses in the sending script.

### Missing SPF record
Gmail rejects emails from domains without SPF. After setting up Postfix, add DNS TXT record:
```
v=spf1 ip4:<VPS_IP> ip6:<VPS_IPv6> ~all
```
Without this, Gmail returns `550-5.7.26 ... SPF did not pass`. Other providers (ProtonMail, Outlook, custom domains) may accept without SPF but deliverability is still better with it.

### Sending script location
Production pipeline: `<HERMES_ROOT>/shared/marketing/email/outreach-engine.py` — sequence-based, rate-limited, per-lead tracking, cron-automated. See `references/outreach-automation.md` for full docs.

Legacy script at `/root/hermes-landing/outbound/send_campaign.py`. Features: rate limiting (30s between emails), dedup tracking via `sent.json`, batch size 20, template auto-selection by sector, dry-run mode.

### Volume too high too fast
Sending 100+ emails on day 1 from a new domain = instant spam folder. Always ramp volume gradually.
