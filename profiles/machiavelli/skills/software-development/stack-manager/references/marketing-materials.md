# Marketing Materials — Created 2026-05-29

Full marketing suite created from multi-bot brainstorming session. All files at `<SHARED_DIR>/marketing/`.

## Inventory (26 files, ~350KB)

### Starter Kit (`starter-kit.md`)
- 3 pricing tiers: Starter €49, Business €149, Enterprise €249
- Launch offer: €99/mese for first 10 PMI (2 bots, free setup, 30d support)
- Pitch scripts for Telegram/LinkedIn DM outreach (Italian)
- ROI comparison vs traditional consultants
- FAQ with objection handling

### GDPR/Fiscal Audit (`audit/`)
- `audit-questionnaire.md` — 15 yes/no questions, 5 categories, scoring 0-15
- `audit-report-template.md` — compliance score 0-100, GDPR article refs, estimated fines
- `audit-landing-copy.md` — landing page copy "La tua PMI è a norma? Scoprilo in 5 minuti."

### Legal Templates (`templates-legali/`) — 10 files
- privacy-policy.md, informativa-cookie.md, contratto-fornitura.md, nda.md
- lettera-incarico.md, regolamento-interno.md, dpa.md, clausola-recesso.md
- contratto-consulenza.md, termini-servizio.md
- All Italian law compliant (GDPR, Codice Civile, Codice del Consumo)
- Each has [PLACEHOLDER] fields + LAWrenzo branding footer

### Brand Identity (`brand/`)
- `brand-identity.md` — palette (company + 6 bots), typography, tone of voice, logo concepts
- `social-templates.md` — 10 post templates (Bot in Azione, Lo sapevi?, Prima/Dopo, Case Study)
- `content-calendar.md` — 30-day LinkedIn calendar, 3 posts/week

### Landing Page (`landing/index.html`) — 48KB, production-ready
- Dark theme, responsive, animations (IntersectionObserver)
- 10 sections: Hero, Problema, Team, Come Funziona, ROI Calculator, Pricing, Testimonials, FAQ, CTA
- Interactive savings calculator slider

### Pitch Deck (`pitch-deck/index.html`) — 24KB, slide-based
- 10 slides with keyboard/click/swipe navigation
- SVG node graph showing inter-bot ecosystem
- Dark theme, mobile-responsive

### Outreach (`outreach/`)
- `commercialisti-outreach.md` — Telegram/LinkedIn/email + day 3/7 follow-ups
- `coworking-outreach.md` — email + workshop proposal + agenda
- `pmi-outreach.md` — 4 segment-specific LinkedIn templates (ristoranti, negozi, studi, e-commerce)
- `referral-program.md` — referral code system (HERM-[NOME]-[4CIFRE]), shareable templates

### LinkedIn Company Page (`linkedin-page.md` + `linkedin/`)
- Company page setup guide: name, tagline, about (~1850 chars), 20 specialties, company info
- 5 launch posts ready to publish (lancio, problema/soluzione, team, caso studio, CTA)
- `linkedin/banner.html` — 1584×396 banner (HTML, screenshot to use as image)
- `linkedin/logo.html` — 300×300 circular logo (HTML, screenshot to use as image)
- `linkedin/banner.png` — 1584×396 banner (PNG, generated with Pillow)
- `linkedin/logo.png` — 800x800 circular logo (PNG, generated with Pillow)
- `linkedin/banner.jpg` — JPEG version for Telegram API sendPhoto
- `linkedin/logo.jpg` — JPEG version for Telegram API sendPhoto
- **Pitfall**: Image generation (FAL) may be unavailable. Use Pillow fallback: `pip install Pillow --break-system-packages`. Generate PNGs programmatically, then convert to JPG for Telegram.
- **Pitfall**: `send_message` with `MEDIA:` prefix does NOT deliver photos as native Telegram images. Use `<SHARED_DIR>/scripts/send-photo.py` (direct Bot API sendPhoto endpoint).

## Usage Notes
- All content in Italian, professional but warm tone
- Zero-budget approach (organic only)
- Torino-centric positioning
- Templates have [PLACEHOLDER] fields for personalization
- Landing page and pitch deck are standalone HTML files (no dependencies)
- Brand palette: dark #1a1a2e, accent #e94560, per-bot colors defined
- LinkedIn banner/logo are HTML files — open in browser, screenshot for upload
- Pillow-generated PNGs: logo (800x800), banner (1584x396) — also available as JPG for Telegram
- LinkedIn API integration: `<SHARED_DIR>/linkedin/` (linkedin.py, linkedin-oauth.py, config.env, SETUP.md)
- Privacy policy hosted at: `<PRIVACY_POLICY_URL>`
- Photo sending script: `<SHARED_DIR>/scripts/send-photo.py` (direct Telegram Bot API)
