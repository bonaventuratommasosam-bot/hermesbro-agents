# HermesBro Design System (from hermesbro.cloud)

## Source of Truth
The LIVE site at https://hermesbro.cloud is the canonical design reference.
Always `curl -sL https://hermesbro.cloud` to get current CSS/HTML before building materials.

## Color Palette
```css
--ink: #0a0a0f;          /* Main background */
--surface: #fafaf9;      /* Light surface (rarely used) */
--muted: #71717a;        /* Secondary text */
--gold: #d4a853;         /* PRIMARY accent — signature color */
--gold-dark: #b8922e;    /* Darker gold for hover/secondary */
--radius: 16px;          /* Standard border-radius */
```

## Typography
```css
--mono: 'JetBrains Mono', monospace;   /* Labels, tags, badges */
--sans: 'Inter', -apple-system, sans-serif;  /* Body, headings */
```
- Weights: 300-900 (Inter), 400-600 (JetBrains Mono)
- Headings: font-weight 800, letter-spacing -0.02em
- Labels: font-family mono, 11px, uppercase, letter-spacing 3px

## Logo
SVG line-art mark (freccia/linea d'oro). NOT a PNG image.
```html
<svg viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M80 20 C60 35, 25 50, 20 80 C18 92, 30 95, 40 88 C55 78, 65 65, 80 55" stroke="#d4a853" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <path d="M80 20 C100 35, 135 50, 140 80 C142 92, 130 95, 120 88 C105 78, 95 65, 80 55" stroke="#d4a853" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <path d="M80 55 L80 140" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-linecap="round"/>
  <circle cx="80" cy="48" r="8" stroke="#d4a853" stroke-width="2" fill="none"/>
  <path d="M50 65 C58 58, 68 52, 80 48" stroke="rgba(212,168,83,0.4)" stroke-width="1" fill="none"/>
  <path d="M110 65 C102 58, 92 52, 80 48" stroke="rgba(212,168,83,0.4)" stroke-width="1" fill="none"/>
  <path d="M30 75 L18 72" stroke="rgba(212,168,83,0.3)" stroke-width="1" stroke-linecap="round"/>
  <path d="M130 75 L142 72" stroke="rgba(212,168,83,0.3)" stroke-width="1" stroke-linecap="round"/>
</svg>
```
For page headers, use a small version (32×32px).

## Bot Profile Pictures (pfps)
**Source**: `https://hermesbro.cloud/bot-profiles/pixel-*.png`
**DO NOT** use local copies — download fresh from the live site.

### CSS (exact from site)
```css
.product-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  margin-bottom: 12px;
  border: 1px solid rgba(255,255,255,0.1);
}
```

### Product Card CSS
```css
.product-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--radius);  /* 16px */
  padding: 20px 14px;
  text-align: center;
}
.product-tag {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--gold);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
```

## Background Effects
```css
/* Mesh gradient (subtle) */
background:
  radial-gradient(ellipse at 20% 30%, rgba(37,99,235,0.06) 0%, transparent 50%),
  radial-gradient(ellipse at 70% 20%, rgba(212,168,83,0.05) 0%, transparent 50%),
  radial-gradient(ellipse at 50% 60%, rgba(37,99,235,0.04) 0%, transparent 50%);
```

## Customer-Facing Bot Roster (10 bots — from live site)
| Bot | Tag | Description |
|-----|-----|-------------|
| ContAIbile | Contabilità | Fatturazione, spese, report mensili |
| LAWrenzo | Legale | Analisi contratti, clausole, scadenze |
| Wannabe | Social Media | Calendario editoriale, copy, DM |
| DesignBro | Grafica | Loghi, template, mockup, brand |
| DUCATO | Trading AI | Azioni, crypto, forex, portfolio |
| El Froggo | DeFi | Trading su Base, DEX screener |
| GROOT | Cucina | Menu, inventario, ordinazioni |
| Machiavelli | Orchestratore | Coordina agenti, priorità |
| Sentinel | Sicurezza | Monitoraggio, protezione attiva |
| MR ROBOT | Coding | Production-grade, full-stack |

## Core Messaging (ALWAYS include)
**Decentralization is THE differentiator.** Every material must reinforce:
- Decentralizzato per design — dati non escono mai dal VPS del cliente
- Zero data sharing — nessun cloud terze parti, no API esterne per i dati
- Ogni agente è isolato — zero condivisione dati tra bot
- No telemetry, no tracking — dati restano dove li metti tu
- GDPR by design — compliance naturale, non aggiunto dopo
- Zero Trust — ogni componente è isolato

Where to place: Cover slide pill ("Decentralizzato • Zero Data Sharing"), Problema slide card ("Dati esposti"), Soluzione slide gold box, Architettura slide "Data Sovereignty" column, Investor Metrics "Tech Moat" section.

## Brand Text
- Tagline: "Il tuo wingman AI per il business"
- Section header: "Dieci specialisti. Un solo abbonamento."
- CTA: "Smetti di fare tutto da solo."
- Email: contact@example.com
- URL: hermesbro.cloud
- Telegram: @HermesBroBot
