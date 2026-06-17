# LinkedIn Company Page + Developer App Setup

## Company Page Creation

URL: https://www.linkedin.com/company/setup/new/

Fields:
- **Company Name:** HermesBro
- **Tagline:** 5 bot AI specializzati per il tuo business. Uno per ogni esigenza.
- **Industry:** Technology, Information and Internet
- **Company size:** 2-10 employees
- **Company type:** Privately Held
- **Founded:** 2025
- **Headquarters:** Torino, Piedmont, Italy
- **Website:** https://YOUR_VPS_HOST/hermesbro/
- **Email:** info@hermesbro.com

### About Section (use this copy)

HermesBro è la piattaforma di 5 bot AI specializzati, ognuno progettato per risolvere un problema reale del tuo business.

📊 ContAIbile — Contabilità intelligente: fatture, spese, bilanci senza stress
⚖️ LAWrenzo — Assistente legale: contratti, normative, compliance
🌿 GROOT — Ristorazione: menu digitali, prenotazioni, ordini
📱 Wannabe — Social media manager AI: contenuti, calendario, analytics
🎨 DesignBro — Grafica su misura: loghi, template, brand identity

Niente buzzword. Niente promesse vuote. Bot che funzionano, per imprenditori che agiscono.

🔗 YOUR_VPS_HOST/hermesbro/
📧 info@hermesbro.com

### Specialties (copy-paste)

```
Artificial Intelligence
Business Automation
Chatbot
Social Media Management
Accounting Software
Legal Tech
Graphic Design
SaaS
Italian Market
SME Tools
```

### Culture Values (optional section)

- Direct — Dritto al punto, zero filtri
- Capable — Competenza reale, non marketing fuffa
- Loyal — Dalla parte dell'utente, sempre
- Human — Tecnologia che parla come una persona

### Assets needed

- Logo PNG: `<HERMES_ROOT>/shared/marketing/linkedin/logo.png` (800x800)
- Banner PNG: `<HERMES_ROOT>/shared/marketing/linkedin/banner.png` (1584x396)
- About text: see above or `<HERMES_ROOT>/shared/marketing/linkedin-page.md`

### Content Calendar (first 5 posts)

| Day | Type | Theme |
|---|---|---|
| Lun | Carousel | Feature spotlight (un bot alla volta) |
| Mer | Testo + immagine | Case study / risultato cliente |
| Ven | Reel/video | Behind the scenes / demo live |

Launch posts: `<HERMES_ROOT>/shared/marketing/linkedin/post-{1..5}.txt`

### CTA Button

- Primary: "Visita il sito web" → YOUR_VPS_HOST/hermesbro/
- Secondary: "Contattaci" (not "Prova gratis" — no self-serve yet)

## Developer App Creation

URL: https://www.linkedin.com/developers/

Steps:
1. Click "Create App"
2. **App name:** HermesBro
3. **LinkedIn Page:** Select the HermesBro company page (MUST exist first)
4. **Privacy policy URL:** `https://YOUR_VPS_HOST/hermesbro/privacy-policy.html`
5. **App logo:** Upload logo.png
6. Accept terms → Create app
7. Go to Auth tab → Add redirect URL: `http://localhost:8089/callback`
8. Note Client ID and Client Secret
9. Run OAuth flow: `python3 <HERMES_ROOT>/shared/linkedin/linkedin.py auth`

## OAuth Scopes

- `openid` — OpenID Connect
- `profile` — Basic profile info
- `email` — Email address
- `w_member_social` — Post to personal profile ✅ (currently active)
- `w_organization_social` — Post to company page ⚠️ (RESTRICTED, needs LinkedIn approval)

## Posting

```bash
# Personal profile (currently works)
python3 <HERMES_ROOT>/shared/linkedin/linkedin.py post "text here"

# Company page (BLOCKED until ORG_URN configured)
python3 <HERMES_ROOT>/shared/linkedin/linkedin.py post-org "text here"

# From file (preferred for cron jobs)
python3 <HERMES_ROOT>/shared/linkedin/linkedin.py post-file /path/to/post.txt
```

## Config Location

`<HERMES_ROOT>/shared/linkedin/config.env` — credentials template
`<HERMES_ROOT>/shared/linkedin/linkedin.py` — full OAuth + posting script
`<HERMES_ROOT>/shared/linkedin/SETUP.md` — step-by-step guide
