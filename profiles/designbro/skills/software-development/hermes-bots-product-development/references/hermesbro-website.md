# HermesBro Website — Structure & Assets

## Location
- **Site root**: `{WEB_ROOT}/` (Nginx root, NOT `/var/www/html/`)
- **Domain**: hermesbro.cloud
- **Main file**: `{WEB_ROOT}/index.html` (single-page, ~1600 lines)
- **Images**: `{WEB_ROOT}/img/` (copied from marketing assets)

## Bot Profile Images (PFPs)

### Source locations
- **Pixel PFPs** (preferred, consistent style): `<HERMES_ROOT>/shared/marketing/bot-profiles/pixel/`
  - `pfp-contaibile.png`, `pfp-designbro.png`, `pfp-ducato.png`, `pfp-el-froggo.png`, `pfp-groot.png`, `pfp-lawrenzo.png`, `pfp-wannabe.png`, `pfp-hermesbro.png`
- **Bot-profile JPGs** (photo-realistic): `<HERMES_ROOT>/shared/marketing/bot-profiles/`
  - `bot-profile-ratatouille-01.jpg` (no pixel version exists for Ratatouille)
  - Also: `bot-profile-ducato-01.jpg`, `bot-profile-el-froggo-01.jpg`, etc.
- **Pixel variants** (parent dir): `<HERMES_ROOT>/shared/marketing/bot-profiles/pixel-*.png`

### Deployed to site
Images copied to `{WEB_ROOT}/img/` with consistent naming:
- `ratatouille.jpg` (source: bot-profile JPG — no pixel version)
- `contaibile.png`, `lawrenzo.png`, `wannabe.png`, `designbro.png`, `ducato.png`, `el-froggo.png`, `groot.png` (source: pixel PFPs)

## HTML Icon Pattern

Bot icons appear in two sections: **product cards** (`.product-icon`) and **spec cards** (`.spec-icon`).

### Current pattern (images) — as of 2026-05-29:

**Product cards** (hero "I tuoi agenti" section) — direct `<img>`, no wrapper div:
```html
<img src="/img/contaibile.png" alt="ContAIbile" class="product-icon" style="width:80px;height:80px;border-radius:16px;">
```

**Spec cards** ("Ogni bot. Ogni dettaglio." section) — pixel art PFPs:
```html
<img src="/bot-profiles/pixel-contaibile.png" alt="ContAIbile NFT" class="spec-icon" style="width:48px;height:48px;border-radius:10px;border:1px solid #10B981;">
```

### Image paths on server:
- `/img/*.png` — bot profile images (contaibile.png, lawrenzo.png, etc.)
- `/bot-profiles/pixel-*.png` — pixel art NFT-style images

### CSS note:
The `.product-icon` class exists in the stylesheet but the inline styles on the `<img>` tags override it. If restyling, update the inline styles or add `!important` to the CSS.

## Pitfalls
- **Filename encoding**: `pfp-ducatо.png` in the pixel/ dir has a Cyrillic 'о' (U+043E) not Latin 'o'. Use `cp` carefully or rename.
- **No Ratatouille pixel PFP**: Use `bot-profile-ratatouille-01.jpg` instead.
- **Single HTML file**: All CSS is inline `<style>`, all JS is inline `<script>`. No build step.
- **IT/EN toggle**: Content uses `data-it` / `data-en` attributes for bilingual support.
- **Don't break the scroll animations**: Cards use `.reveal` class + IntersectionObserver for fade-in.

## Updating images
1. Copy new images to `{WEB_ROOT}/img/` (profile PNGs) or `{WEB_ROOT}/bot-profiles/` (pixel art)
2. For product cards: replace `<div class="product-icon" style="...">LETTER</div>` with `<img src="/img/botname.png" alt="BotName" class="product-icon" style="width:80px;height:80px;border-radius:16px;">`
3. For spec cards: update `src="/bot-profiles/pixel-botname.png"` path
4. Verify with `browser_console` — check `naturalWidth > 0` on all `<img>` elements
5. **Always use absolute paths** (`/img/...` not `img/...`) — the site is served at domain root
