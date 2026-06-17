# Outbound Email Campaign

## Overview
Cold email campaign targeting Italian businesses across 5 sectors. Templates at `/root/hermes-landing/outbound/templates/`.

## Sending Infrastructure

**Provider**: SendGrid (free tier: 100 emails/day)
**Sender**: contact@example.com
**Fallback**: Mailgun (100/day free)
**Himalaya CLI**: `himalaya v1.2.0` installed, NOT configured (needs `~/.config/himalaya/config.toml`)
**VPS SMTP**: Blocked by Gmail (no SPF/DKIM) — must use transactional service

### SendGrid Setup (pending — [REDACTED — dati personali rimossi] must complete manually)
1. Create account at signup.sendgrid.com (email: contact@example.com, password generated 2026-06-03)
2. Verify sender email (check ProtonMail inbox for confirmation)
3. Generate API key (Settings → API Keys)
4. Configure: `SENDGRID_API_KEY` in env or himalaya config

**Pitfall — Cloudflare CAPTCHA**: SendGrid's signup form has a Cloudflare Turnstile CAPTCHA in an iframe. Browser automation CANNOT solve it (CDP error on iframe ref click). [REDACTED — dati personali rimossi] must complete signup manually. Provide him with: email, password, and step-by-step instructions. Don't waste time trying to automate it.

## Contact Form API

Backend endpoint added to HermesBro multitenant backend:
- **Route**: `POST /api/contact`
- **Body**: `{name, email, company, message}`
- **DB**: `contacts` table (id, name, email, company, message, created_at)
- **Response**: `{status: "ok", message: "Messaggio ricevuto, ti contatteremo presto"}`
- **Validation**: name required, email must contain @

## Templates (5 sectors)

| Sector | File | Product | Pain Points |
|--------|------|---------|-------------|
| Ristoranti | `ristoranti.md` | ContAIbile | [REDACTED — dati personali rimossi] fuori controllo, sprechi, porzioni non standard |
| Studi legali | `studi-legali.md` | LAWrenzo | tempo su attività ripetitive, scadenze, redazione atti |
| E-commerce | `e-commerce.md` | Team bot 24/7 | richieste clienti non risposte, ordini persi |
| Startup | `startup.md` | Team scalabile | budget limitato, impossibile assumere per ogni funzione |
| PMI generica | `pmi-generica.md` | Automazione | software enterprise costoso, concorrenza digitalizza |

## Template Structure
Each template: ~120 words, Italian, direct tone, sector-specific pain points, CTA "Prenota una demo di 15 minuti", signed "[REDACTED — dati personali rimossi] | HermesBots". Placeholders: `{nome}` (business name) and `{link}` (booking link).

## Lead Research (200 leads target)

40 leads per sector. Sources:
1. **Google Maps scraping** (Outscraper/Aify, ~$10/1000) — search by category + city (Milano, Roma, Torino, Napoli, Bologna)
2. **LinkedIn Sales Navigator** + Apollo.io — filter by title (Proprietario/CEO/Fondatore), size 1-50, Italia
3. **PagineGialle** — manual scraping, often has direct email

### Quality Filters
- Must have website (has digital budget)
- Recent reviews (active business)
- No large chains (unreachable decision-makers)
- Email verified (NeverBounce/ZeroBounce)

### CSV Format
`nome,cognome,azienda,settore,email,telefono,sito_web,citta,fonte,stato`

### Workflow
1. Week 1: Google Maps for all 5 sectors (160 contacts)
2. Week 2: LinkedIn for premium (40 contacts with direct decision-maker)
3. Verify all emails before sending
4. Remove duplicates, closed businesses, contacts without email

### GDPR
- Include opt-out in every email
- Don't send to businesses that already have declared AI bots
- Prioritize businesses without visible chatbot on their site

## Sending Cadence
20 emails/day (not all at once). Track opens/replies. Follow up after 5 days if no response.

## Full Guide
`/root/hermes-landing/outbound/templates/leads-ricerca.md`
