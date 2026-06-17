# HermesBro Landing Page Structure

**File**: `{WEB_ROOT}/index.html`
**Domain**: `hermesbro.cloud`
**Nginx root**: `{WEB_ROOT}/`

**Pitfall**: [REDACTED — dati personali rimossi] may reference `/home/[REDACTED — dati personali rimossi]/hermesbro-landing/index.html` — that file does NOT exist. The canonical file is `{WEB_ROOT}/index.html`.

## Image Paths

- `/img/` = bot profile images (contaibile.png, lawrenzo.png, groot.png, wannabe.png, designbro.png, ducato.png, machiavelli.png, sentinel.png, ratatouille.png, el-froggo.png)
- `/bot-profiles/` = pixel art NFT versions (pixel-contaibile.png, pixel-lawrenzo.png, etc.)

## HTML Structure

### Hero Section — Counters

The hero section has animated counters in `<div class="counters">`:
```html
<div class="counters">
  <div class="counter-item">
    <div class="counter-value">10</div>
    <div class="counter-label">Agenti Specializzati</div>
  </div>
  <div class="counter-item">
    <div class="counter-value">180+</div>
    <div class="counter-label">Tools Totali</div>
  </div>
</div>
```

**Current values (as of June 2026)**: 10 Agenti Specializzati, 180+ Tools Totali. When the bot lineup changes, update both the counter values AND the spec cards below.

### Hero Section — Product Cards

Each bot has a `<div class="product-card">` containing:
```html
<div class="product-card">
  <div class="product-avatar" style="background: var(--blue);">
    <img src="/img/contaibile.png" alt="ContAIbile" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">
  </div>
  <div class="product-name">ContAIbile</div>
  <div class="product-tagline">Contabilità, fatture, bilanci</div>
</div>
```

**Fallback (no image)**: Replace `<img>` with a colored letter:
```html
<div class="product-avatar" style="background: var(--green);">G</div>
```

### Specs Section — Spec Cards

Each spec card has TWO parts: **spec-stats** (3 metrics) and **spec-tools** (feature list).

```html
<div class="spec-card">
  <div class="spec-icon">
    <img src="/bot-profiles/pixel-contaibile.png" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">
  </div>
  <div class="spec-title">ContAIbile</div>
  <div class="spec-subtitle">Il tuo commercialista digitale</div>
  
  <div class="spec-stats">
    <div class="spec-stat">
      <div class="spec-number">99.2%</div>
      <div class="spec-label">Precisione</div>
    </div>
    <div class="spec-stat">
      <div class="spec-number">&lt;30s</div>
      <div class="spec-label">Fattura</div>
    </div>
    <div class="spec-stat">
      <div class="spec-number">€2.4k</div>
      <div class="spec-label">Risparmio/anno</div>
    </div>
  </div>
  
  <div class="spec-tools">
    <div class="spec-tool" data-it="Fatturazione elettronica" data-en="Electronic invoicing">Fatturazione elettronica</div>
    <div class="spec-tool" data-it="Note spese automatiche" data-en="Auto expense reports">Note spese automatiche</div>
    <!-- ... more items ... -->
  </div>
</div>
```

**Key details**:
- `spec-stats`: Always 3 stat blocks, each with `.spec-stat-val` + `.spec-stat-label`
- `spec-tools`: Feature list items (`<li>`) with `data-it` and `data-en` attributes for i18n

- Feature counts per bot (as of June 2026):
  - ContAIbile: 10 features, stats: 99.2% Precisione, <30s Fattura, €2.4k Risparmio
  - LAWrenzo: 10 features, stats: 36 Template, 100% GDPR, <60s Review
  - DesignBro: 10 features, stats: 15+ Formati, CMYK+RGB, <2min Gen
  - Wannabe: 10 features, stats: 5 Piattaforme, AI Copy, Analytics
  - DUCATO: 10 features, stats: 4 Strategie, Backtest, Live Alerts
  - El Froggo: 10 features, stats: 15+ Chain, Real-time, DEX+CEX
  - GROOT: 10 features, stats: Menu AI, Fornitori, €18k Risparmio
  - Machiavelli: 10 features, stats: 10 Agents, ∞ Workflows, 24/7 Uptime
  - Sentinel: 12 features, stats: 12 Tools, 100 Score, 24/7 Uptime
  - MR ROBOT: 20 features, stats: 20 Tools, All Languages, NVD CVE DB
- When [REDACTED — dati personali rimossi] asks to normalize feature counts across cards, copy the pattern from the most complete card and adapt values
- **Bilingual pattern**: All `<li>` items in `spec-tools` use `data-it` / `data-en` for language switching. The visible text defaults to Italian.

## CSS Variables (brand palette)

```css
--primary: #1a1a2e;
--secondary: #16213e;
--accent: #e94560;
--gold: #ffd60a;
--blue: #4361ee;
--purple: #7209b7;
--green: #06d6a0;
--orange: #f77f00;
--pink: #e63946;
```

## Replacing Bot Profile Pictures (from Telegram images)

When [REDACTED — dati personali rimossi] sends an image via Telegram saying "cambia il pfp di [bot]":

1. Image arrives in `<HERMES_ROOT>/profiles/gribbito/image_cache/` as JPG
2. Convert to PNG 256x256 using Pillow:
```python
from PIL import Image
img = Image.open('<HERMES_ROOT>/profiles/gribbito/image_cache/<filename>.jpg')
img = img.resize((256, 256), Image.LANCZOS)
img.save('{WEB_ROOT}/bot-profiles/pixel-<botname>.png', 'PNG')
```
3. Verify: `file {WEB_ROOT}/bot-profiles/pixel-<botname>.png` (should say 256x256 PNG)
4. **CRITICAL — Cache-bust the image references**: The browser will STILL show the old image because nginx sets `Cache-Control: max-age=2592000` (30 days). You MUST add `?v=N` to ALL `<img src>` references for that bot:
   - Search ALL occurrences: `grep -n "pixel-<botname>" {WEB_ROOT}/index.html`
   - There are typically TWO references per bot: `<img class="product-avatar">` in hero + `<img class="spec-icon">` in specs
   - Change `pixel-<botname>.png` → `pixel-<botname>.png?v=2` in BOTH places
   - Without this, [REDACTED — dati personali rimossi] will say "no ce ancora quello vecchio" — the file IS updated on disk but the browser cache prevents it from showing
5. No nginx reload needed (static file, served directly)

**Pitfall**: Pillow requires `pip install Pillow --break-system-packages` on newer Debian/Ubuntu (PEP 668).
**Pitfall**: Always backup the old file before overwriting: `cp pixel-<botname>.png pixel-<botname>-old.png`
**Pitfall**: Vision analysis may be unavailable (model doesn't support image input). Don't block on it — just convert and deploy.
**Pitfall — Browser cache is the #1 reason [REDACTED — dati personali rimossi] thinks the image didn't change**: Always add `?v=N` after replacing any image. Increment N each time you replace the same image. [REDACTED — dati personali rimossi] will see the old image and tell you "non funziona" — it's not a server problem, it's cache.

## Editing Counters (bilingual)

Counters use `data-it` / `data-en` attributes. To change a number word:

```html
<p class="reveal" data-it="HermesBro ti dà dieci assistenti AI specializzati..."
   data-en="HermesBro gives you ten specialized AI assistants...">
```

Also update the `<h2>` section heading:
```html
<h2><span data-it="Dieci specialisti." data-en="Ten specialists.">Dieci specialisti.</span></h2>
```

**Pitfall**: Italian number words change (sette→dieci, nove→dieci). Always update BOTH data-it AND data-en attributes, plus the visible text.

## Expanding Spec Card Features

When [REDACTED — dati personali rimossi] provides a feature list for a bot:

1. Count current features: `grep -c '<li' {WEB_ROOT}/index.html` per section
2. Replace the `<ul class="spec-tools">` block entirely with the new features
3. Use bilingual pattern: `<li data-it="Italian text" data-en="English text">Italian text</li>`
4. Update `spec-stats` numbers if the tool count changed (e.g., "7" → "10" for Agents)
5. Verify with Python script counting features per spec card block

**Pattern for spec-tools replacement**:
```html
<ul class="spec-tools">
  <li data-it="Feature name — description" data-en="Feature name — description">Feature name — description</li>
</ul>
```

**Pitfall**: When [REDACTED — dati personali rimossi] provides feature lists, the count may not match what's in the file. Always count first with the Python script, then replace. [REDACTED — dati personali rimossi] expects consistent counts (or at least the counts he specified).

## Deployment Checklist

After any edit:
```bash
nginx -t && systemctl reload nginx
curl -s https://hermesbro.cloud/ | grep 'img/botname'  # verify image loads
```

## Bot Image Sources

- Full-color profiles: `<HERMES_ROOT>/shared/marketing/bot-profiles/` (source of truth)
- Pixel art: `<HERMES_ROOT>/shared/marketing/bot-profiles/pixel-*.png`
- Nginx serving: `{WEB_ROOT}/img/` and `{WEB_ROOT}/bot-profiles/`

**Sync command** (when new images added to source):
```bash
cp <HERMES_ROOT>/shared/marketing/bot-profiles/*.png {WEB_ROOT}/img/
cp <HERMES_ROOT>/shared/marketing/bot-profiles/pixel-*.png {WEB_ROOT}/bot-profiles/
```

## Updating Bot Counters

When the bot lineup changes (new bots added or removed):
1. Update `.counter-value` in the hero section (e.g., "10" → "12")
2. Update `.counter-label` if needed (e.g., "Agenti Specializzati")
3. Update the Tools counter if tool count changed
4. Add/remove `.product-card` entries in the hero grid
5. Add/remove `.spec-card` entries in the specs section
6. Sync images to nginx: `cp <HERMES_ROOT>/shared/marketing/bot-profiles/*.png {WEB_ROOT}/img/`

**Pitfall**: [REDACTED — dati personali rimossi] may ask to update counters from Windows files he prepared. Since we can't SCP from his machine, he needs to either paste the content or upload it himself. Always verify the current file state before applying changes — the file on VPS may already have been partially updated.
