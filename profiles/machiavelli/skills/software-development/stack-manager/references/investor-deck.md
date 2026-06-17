# Investor Pitch Deck — Hermes Bots

Path: `<WORK_DIR>/hermes-bots-deck.html`

Self-contained HTML. Space Mono font. Open directly in browser.

## Design System
- Font: Space Mono (monospace, Google Fonts)
- Dark mode default. Toggle via "Tema" link in top bar.
- Accent: #00ff00 (green fluo) for highlights, badges, active states
- Typography: oversized hero (clamp 48-120px), section labels (11px uppercase tracked)
- Layout: single scrolling page (NOT slide-based navigation)
- No external deps except Google Fonts
- localStorage for theme persistence

## Sections (8, scrolling single-page)
1. **Hero** — full viewport, "Un bot che sa il tuo lavoro meglio di te." + subtitle + scroll hint
2. **01 Problema** — 3-column numbers grid (73%, 4h, €500) with descriptions
3. **02 Soluzione** — horizontal card rows (numbered 01/02/03) with "Online" badges
4. **03 Come funziona** — 2-column grid: esperienza + architettura
5. **04 Mercato** — split layout: big numbers left, "perché adesso" right
6. **05 Pricing** — 3-card grid (€29/€79/€199) with center elevated + unit economics bar
7. **06 Avanzamento** — 2-column traction + 4-column horizontal roadmap
8. **07 Team** — 3 cards (Founder/Hermes/Frank) with role badges
9. **08 Investimento** — €25K CTA box with breakdown + milestones grid
10. **Footer** — contact links (email, Telegram, X)

## Critical Design Rule
When asked to replicate a site's style (e.g. "come il sito di X"):
- Extract ONLY the design system: fonts, colors, spacing, accent treatment
- Create a COMPLETELY ORIGINAL layout and content structure
- Do NOT replicate section order, nav patterns, marquee, or page architecture
- Do NOT copy texts, taglines, or slogans — even translated
- the owner will say "Troppo simile all'originale" if it reads as a copy
- Rule: design system is inspiration, everything else is original

## Usage
Send screenshots via Telegram using MEDIA: path. Can also be served via nginx on VPS.
