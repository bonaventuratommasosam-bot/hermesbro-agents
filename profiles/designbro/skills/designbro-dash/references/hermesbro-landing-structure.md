# HermesBro Landing Page Structure

## Live Site Sections (Contabo)

The live site at `https://YOUR_VPS_HOST/hermesbro/` uses these section IDs:

- `#bot` — Product cards (7 bots: Ratatouille, ContAIbile, LAWrenzo, Wannabe, DesignBro, DUCATO, El Froggo)
- `#prezzi` — Pricing grid (3 cards: Starter €50, Pro €120, Enterprise Custom)
- `#faq` — Accordion FAQ
- Hero section (no ID)
- "Come funziona" — 3 steps
- Social proof — stats grid
- Final CTA
- Footer

## Local File

`/root/hermesbro-landing.html` — may be outdated vs live. Always check live site structure before modifying.

## Product Card Structure (live site)

```html
<div class="product-card reveal">
  <div class="product-icon" style="color: #HEX; background: #HEX15;">LETTER</div>
  <h3>BotName</h3>
  <span class="product-tag">Sector</span>
  <p>Description text.</p>
</div>
```

### To replace letter icons with images:

Replace `<div class="product-icon" style="color: #HEX; background: #HEX15;">LETTER</div>` with:
```html
<div class="product-icon"><img src="bot-profiles/bot-profile-name-01.jpg" alt="BotName"></div>
```

Update CSS to support images:
```css
.product-icon {
  width: 72px; height: 72px; border-radius: 16px;
  overflow: hidden; flex-shrink: 0;
}
.product-icon img {
  width: 100%; height: 100%; object-fit: cover; border-radius: 16px;
}
```

## Pricing Section Structure (live site)

3-card grid with features lists:
- **Starter** €50/mese: 1 bot, 1000 msg, Telegram, weekly reports
- **Pro** €120/mese: 3 bots, unlimited, Telegram+WhatsApp, daily reports (featured/highlighted)
- **Enterprise** Custom: unlimited bots, on-premise, SLA, account manager

## Deployment

No SSH access to Contabo. Workflow:
1. Modify `/root/hermesbro-landing.html` locally
2. Send HTML + assets to user via Telegram
3. User uploads to server manually

## Pitfall: Multiple Editors

The landing page is edited by multiple sessions. Always re-read the file before patching — `patch` fails if the file was modified externally since last read.
