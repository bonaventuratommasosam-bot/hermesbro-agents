# Privy + Ribbit Capital Design System Reference

Research conducted 2026-06-01 for HermesBro pitch deck redesign.

## Privy (privy.io) — Polished Crypto Infrastructure

**Color Palette:**
- Primary background: White `#FFFFFF`
- Dark sections: Deep navy-black `#010110`, charcoal `#111117`, `#22222A`
- Accent: Electric blue `#0000EE` (signature — all CTAs, interactive elements)
- Neutral grays: `#F7F7F7` (warm off-white), `#D9D9D9` (mid-gray)
- Text: Near-black `#111118` (body), white `#FFF` on dark, `rgba(255,255,255,0.7)` secondary

**Typography:**
- Headings: ABC Favorit Regular — geometric sans-serif, 78px, weight 400, tight tracking (-4.68px)
- Body/UI: Inter Medium — 14px, weight 500
- Feature lists: Inter, 20px, weight 400

**Layout:**
- 80px vertical padding between sections
- Alternating light/dark sections for visual rhythm
- Pill-shaped CTAs (border-radius: 100px, padded 16px)
- Two-tier CTA: Primary dark pill + secondary outline pill
- Stats inline as sentences ("Powering 120M+ accounts for 2,000+ teams")
- Built on Framer

**Vibe:** Polished, premium SaaS, Stripe-like DNA. Developer-focused. Clean typography scale + color contrast.

---

## Ribbit Capital (ribbitcap.com) — Counter-Cultural VC

**Color Palette:**
- Primary: Light warm gray `#F2F2F2` (NOT pure white — matte, editorial feel)
- Accent: Neon green `#00FF00` (extremely bold — active nav, highlights)
- Text: Dark charcoal `#222222`
- Only 3 colors total. Strikingly minimal.
- Dark mode available (toggle)

**Typography:**
- Single font: Space Mono (monospace) — EVERYWHERE
- Hero: Individual characters at 112px, weight 700, separate block-level spans
- Body: Space Mono, 18px, weight 400, line-height 27px
- Nav/buttons: Space Mono, 12px, weight 400, UPPERCASE
- All text lowercase or uppercase — no mixed case

**Layout:**
- Extremely minimal — few elements, lots of breathing room
- Single scrolling page with massive typography
- Hero marquee: "THE FUTURE BELONGS TO THE REBELS" — each letter separate element
- No images except one (frog coin logo)
- No stats/numbers — narrative-driven
- "MEET OUR REBELS" — lowercase link with underline arrow, no button styling

**Vibe:** Anti-corporate, punk, editorial. Indie magazine / art project. Monospace + neon green + minimal = Web3 rebel energy.

---

## HermesBro Hybrid — Iteration History

### v1 (Privy/Ribbit — 2026-06-01 first deck)
[REDACTED — dati personali rimossi] wanted "più minimalista e in tono con Privy e Ribbit Capital":
- Background: `#F2F2F2` warm gray (Ribbit)
- Dark sections: `#111117` charcoal (Privy)
- Accent: `#00FF00` neon green (Ribbit — frog/crypto identity)
- Headings: Space Mono bold (Ribbit)
- Body: Inter (Privy)

### v2 (Original style preserved — 2026-06-01 fix pass)
[REDACTED — dati personali rimossi] sent original PDF and said "lascia la grafica come" (keep graphics as-is):
- Background: `#0f0f1a` dark navy (original)
- Accent: `#00d4aa` teal-green (original)
- Headings: Inter bold (original)
- Body: Inter (original)

**Key lesson**: When [REDACTED — dati personali rimossi] sends an existing document and says "keep the graphics", extract the ACTUAL colors from that document (use `pdftotext` + visual inspection). The source document is the authority, NOT this reference file. The Privy/Ribbit palette was for a NEW design — not a template for all future decks.

---

## Common Patterns (both palettes)

- Generous whitespace (80px+ sections)
- Clean card layouts with subtle borders, no heavy shadows
- Stats as big monospace numbers with accent color
- Pill badges for labels/CTAs
- Dark backgrounds for hero/cover, lighter for content sections
- Bot cards: circular image + name + role, grid layout (4 per row)
- Base64-embed all images for PDF portability (wkhtmltopdf)
