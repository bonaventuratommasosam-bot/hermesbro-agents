---
name: designbro-dash
description: "Web dashboard + HTML-to-image export pipeline per DesignBro"
tags: [design, html, export, social]
related_skills: [designbro-tools]
---

# DesignBro Dashboard & Export

Web dashboard per DesignBro + pipeline per esportare grafiche HTML→PNG/JPG.

## Avviare la dashboard

```bash
cd /home/[REDACTED — dati personali rimossi]/ai-stack/designbro && python3 -m uvicorn web.app:app --host 0.0.0.0 --port 8094 &
```

## Pagine

- `/` — Dashboard principale (design recenti, brand kit attivo)
- `/generator` — Genera immagini con interfaccia
- `/brand-kit` — Gestione colori, font, logo
- `/gallery` — Tutti i design generati
- `/templates` — Template riutilizzabili
- `/palettes` — Palette salvate

## HTML-to-Image Pipeline

Per esportare grafiche da HTML a PNG/JPG (banner, social post, mockup):

```bash
# Cattura a dimensioni esatte (es. LinkedIn banner 1584×396)
wkhtmltoimage --width 1584 --height 396 --quality 95 --format png input.html output.png

# Converti PNG → JPG (Pillow — sempre disponibile, ImageMagick no)
python3 -c "
from PIL import Image
img = Image.open('input.png')
img.convert('RGB').save('output.jpg', 'JPEG', quality=95)
"
```

**Pitfall:** `convert` (ImageMagick) potrebbe non essere installato. Usa sempre Pillow per conversioni.

**Workflow tipico:**
1. Crea HTML con layout esatto (width/height fissi, font importati da Google Fonts)
2. `wkhtmltoimage` per catturare a dimensioni precise
3. `Pillow` per convertire in JPG (molto più piccolo del PNG)
4. Invia con `MEDIA:/path/to/file`

## Dimensioni Social

- LinkedIn banner: 1584×396
- LinkedIn post: 1200×627
- Instagram post: 1080×1080
- Instagram story: 1080×1920
- X header: 1500×500
- X post: 1200×675
- YouTube thumbnail: 1280×720
- Facebook post: 1200×630

## Brand Files Location

- Brand system HTML: `/root/hermesbro-brand.html`
- Marketing assets: `<HERMES_ROOT>/shared/marketing/`
- LinkedIn assets: `<HERMES_ROOT>/shared/marketing/linkedin/`
- Logo SVGs: `/root/hermesbro-logo-gold.svg`, `-white.svg`, `-light.svg`
- Content calendars: `<HERMES_ROOT>/shared/marketing/brand/content-calendar*.md`
- Social templates: `<HERMES_ROOT>/shared/marketing/brand/social-templates.md`
- Brand identity guide: `<HERMES_ROOT>/shared/marketing/brand/brand-identity.md`
- Monthly content plans: `<HERMES_ROOT>/shared/marketing/brand/content-plan-<month>-<year>-completo.md`
- Monthly visual assets: `<HERMES_ROOT>/shared/marketing/<month>-<year>/`

## Content Plan → Visual Assets Pipeline

When WannabeBot delivers a content plan (e.g. `content-plan-<month>-completo.md`), the workflow is:

1. **Parse the brief** — extract the "PARTE 2: BRIEF VISIVI" section. Each visual has: format, background, elements, style.
2. **Create HTML file** — one self-contained HTML per visual, saved to `<HERMES_ROOT>/shared/marketing/<month>-<year>/visual-NN-<slug>.html`
3. **Render with wkhtmltoimage** — `wkhtmltoimage --width <W> --height <H> --quality 95 --format jpg input.html output.jpg`
4. **Verify files exist** — `ls -la *.jpg` to confirm all expected files were created. Don't trust "success" messages without checking.
5. **Send via Bot API** — `python3 <HERMES_ROOT>/shared/scripts/batch-send.py CHAT_ID /path/to/directory/ "Caption prefix"`
6. **Iterate** — user will request changes. Edit HTML, re-render, re-send.

### HTML Template Pattern for Social Visuals

See `templates/social-post-visual.html` for a ready-to-copy starting point. Key structure:

Standard structure for dark-theme HermesBots social posts:

```html
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080, initial-scale=1.0">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1080px; height: 1080px;  /* match target dimensions */
    background: #0a0a0f;
    font-family: 'Inter', sans-serif;
    overflow: hidden;
    position: relative;
  }
  /* Dot grid background */
  .grid-bg {
    position: absolute; inset: 0;
    background-image: radial-gradient(circle, rgba(<accent>,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
  }
  /* Ambient glow */
  .glow {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -60%);
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(<accent>,0.12) 0%, transparent 70%);
  }
  /* Bottom accent bar */
  .bottom-bar {
    position: absolute; bottom: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, transparent, <accent>, transparent);
    opacity: 0.4;
  }
  /* Logo area */
  .logo-area {
    position: absolute; bottom: 40px; right: 50px;
    display: flex; align-items: center; gap: 10px;
  }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="glow"></div>
  <!-- Content centered -->
  <div class="bottom-bar"></div>
  <div class="logo-area"><!-- HermesBots logo --></div>
</body>
</html>
```

### Bot Accent Colors

| Bot | Color | Hex | Emoji |
|-----|-------|-----|-------|
| Ratatouille | Red | `#ef4444` | 🍝 |
| ContAIbile | Ocean Blue | `#3a86ff` | 📊 |
| LAWrenzo | Royal Purple | `#8338ec` | ⚖️ |
| Wannabe | Vibrant Orange | `#ff9f1c` | 📱 |
| DesignBro | Hot Magenta | `#ff006e` | 🎨 |
| DUCATO | Gold | `#d4a853` | 📈 |
| El Froggo | Cyan | `#22d3ee` | 🐸 |

**Pitfall:** The bot lineup has changed over time. GROOT was an earlier name for the restaurant bot; it's now **Ratatouille**. Always use the brand brief's current bot list, not hardcoded names.

### HermesBro Brand Palette (current)

| Role | Color | Hex |
|------|-------|-----|
| Ink (background) | Deep Black | `#0a0a0f` |
| Gold (accent) | Warm Gold | `#d4a853` |
| Trust Blue | Electric Blue | `#2563eb` |
| Surface (light bg) | Off-White | `#fafaf9` |
| Muted (secondary text) | Gray | `#71717a` |

**Pitfall:** Older brand files reference `#1a1a2e` (Deep Navy). Always use `#0a0a0f` (Ink) for new work. When a WannabeBot brief specifies the old palette, silently substitute the current one.

### Rendering Notes

- `wkhtmltoimage` renders Google Fonts (`@import url(...)`) correctly — no need for local font files.
- JPG quality 95 is the sweet spot — 100 is huge, 90 has visible artifacts on dark backgrounds.
- For vertical formats (1080×1920, 1080×1350), add `--height <H>` explicitly — wkhtmltoimage defaults to viewport height.
- PNG is 3-5× larger than JPG. Use JPG for social posts, PNG only when transparency is needed.

## WannabeBot Collaboration Workflow

Telegram bots cannot message other bots. The content pipeline is:

1. **DesignBro** creates content calendar/brief → saves to shared marketing dir
2. **User** copies brief text and sends to WannabeBot manually
3. **WannabeBot** produces full content plan (posts + visual briefs + video briefs + stories) → saves to shared dir
4. **User** tells DesignBro the file path
5. **DesignBro** reads the plan, generates visuals from the brief section

Shared marketing dir: `<HERMES_ROOT>/shared/marketing/brand/` (calendars, templates, brand docs)
Monthly assets dir: `<HERMES_ROOT>/shared/marketing/<month>-<year>/` (generated visuals, HTML sources)

## Telegram Photo Delivery

**MEDIA: tag behavior:**
- ✅ Works in **assistant response text** — the gateway auto-processes it into a native Telegram photo. Limit: one image per turn this way.
- ❌ Does NOT work inside `send_message` tool — arrives as plain text, not a photo.

For single images, just include `MEDIA:/path/to/file.jpg` in your response text. For multiple images (2+), use the Bot API scripts below.

**Always use the direct Bot API script for batch/multi-image delivery:**

```bash
# Single photo (requires profile name as first arg)
python3 <HERMES_ROOT>/shared/scripts/send-photo.py designbro CHAT_ID /path/to/image.jpg "Caption text"

# Batch (loads token ONCE — much faster for 10+ photos)
python3 <HERMES_ROOT>/shared/scripts/batch-send.py CHAT_ID /path/to/directory/ "Caption prefix"
# Also available as skill script: designbro-dash/scripts/batch-send.py
```

Both scripts read `TELEGRAM_BOT_TOKEN` from the profile's `.env`.
`send-photo.py` requires the Hermes profile name as first arg (e.g. `designbro`, `default`).

**Pitfalls:**

- **Inline Python with token gets mangled.** The secret redaction filter scrambles any code containing `TELEGRAM_BOT_TOKEN` patterns. Always write photo-sending scripts to files, never run inline via `terminal`.
- **Verify files exist before batch sending.** Previous sessions may have generated images in memory or temp dirs that don't persist. Always `ls` or `search_files` to confirm JPGs exist in the directory before running batch send. A script that reports "✅ Sent" for non-existent files is worse than one that errors.
- **send-photo.py is slow in loops.** It reloads `.env` on every invocation. For batch operations (5+ photos), use `batch-send.py` which loads the token once. Measured: ~5 photos/180s with send-photo.py loop vs ~25 photos/30s with batch-send.py.

See `references/telegram-photo-delivery.md` for implementation details and pitfalls.
See `references/hermesbro-landing-structure.md` for the landing page HTML structure and deployment workflow.

## Batch Visual Creation with execute_code

When generating 10+ visuals, use `execute_code` to create all HTML files in one call, then batch-convert:

```python
from hermes_tools import write_file, terminal

# 1. Create all HTML files (use helper functions for consistent structure)
write_file(f"{OUT}/visual-NN-slug.html", wrap_html(...))

# 2. Convert all HTML → JPG in a loop
for html_path in html_files:
    width, height = 1080, 1080  # or detect from filename
    terminal(f"wkhtmltoimage --width {width} --height {height} --quality 95 --format jpg {html_in} {jpg_out}")
```

**Key helpers for consistent visuals:**
- `css_base(accent, width, height)` — common CSS with grid-bg, glow, circuit traces
- `wrap_html(title, badge, accent, body_html, width, height)` — full page wrapper
- `rgb_hex(hex_color)` — convert hex to R,G,B for rgba() in CSS

**Batch send after creation:**
```bash
python3 <HERMES_ROOT>/shared/scripts/batch-send.py CHAT_ID /path/to/directory/ "Caption prefix"
```

**Pitfall — `read_file` in `execute_code`:** The `read_file` helper in execute_code returns output with line-number prefixes (`1|line content\n2|...`), NOT a dict with a `"content"` key. To get raw file content for string manipulation, use `terminal("cat /path/to/file")["output"]` instead.

## Bot Profile Image Generation

When generating bot profile images (for website, social, branding), use a **multi-variation pattern** — generate N style variations per bot so the user can pick:

**Standard set:** 7 bots × 5 variations = 35 images
**Variations:** spotlight radial, geometric/triangles, minimal, circuit traces, badge+glow

**Workflow:**
1. Define bot list with name, emoji, hex color, description, sector tag
2. Use `execute_code` to generate all HTML files in one call (helper function per variation)
3. Render all with `wkhtmltoimage --width 1080 --height 1080 --quality 95 --format jpg`
4. Save to `<HERMES_ROOT>/shared/marketing/bot-profiles/`
5. Send via `batch-send.py` — verify files exist first

**Bot color mapping:**\n| Bot | Hex | Emoji |\n|-----|-----|-------|\n| Ratatouille | `#ef4444` | 🍝 |\n| ContAIbile | `#3a86ff` | 📊 |\n| LAWrenzo | `#8338ec` | ⚖️ |\n| Wannabe | `#ff9f1c` | 📱 |\n| DesignBro | `#ff006e` | 🎨 |\n| DUCATO | `#d4a853` | 📈 |\n| El Froggo | `#22d3ee` | 🐸 |

**Naming convention:** `bot-profile-{name-lowercase}-0{N}.jpg` (e.g. `bot-profile-wannabe-03.jpg`)

## Landing Page Updates

The HermesBro landing page lives at:
- **Local:** `/root/hermesbro-landing.html`
- **Live:** `https://YOUR_VPS_HOST/hermesbro/` (Contabo server, no SSH access from Hermes)

**Deployment workflow:**
1. Modify `/root/hermesbro-landing.html` locally
2. Tell user to upload to Contabo server (they have access, we don't)
3. If images are needed on the site, they must also be uploaded to the server

**Pitfall:** The local file may be outdated vs the live site. Before modifying, check the live site structure with `browser_navigate` + `browser_console` to see current HTML. The live site has sections with IDs: `#bot`, `#prezzi`, `#faq`. The local file may use different structure.

**Product cards with images:** Replace emoji `.product-icon` divs with `<img>` tags. Increase icon size from 48px to 72px. Add `overflow: hidden; flex-shrink: 0;` and `object-fit: cover; border-radius: 16px;` on the img.

## Bot Profile Image Generation

When generating bot profile images (for the website, social, brand kit):

1. **Use actual bot names from the brand brief** — the `name` field becomes the filename slug. Don't substitute names (e.g. don't use "GROOT" for "Ratatouille").
2. **5 variations per bot** (spotlight, geometric, minimal, circuit, badge) — gives options for different contexts.
3. **Output:** `<HERMES_ROOT>/shared/marketing/bot-profiles/bot-profile-{name}-0{1-5}.jpg`
4. **Accent color per bot:** ContAIbile `#3a86ff`, LAWrenzo `#8338ec`, Ratatouille `#ef4444`, Wannabe `#ff9f1c`, DesignBro `#ff006e`, DUCATO `#d4a853`, El Froggo `#22d3ee`
5. **After generation:** verify files exist with `search_files` before referencing in HTML.

## Pixel Art PFP Extraction (from screenshot)

When the user sends a screenshot containing multiple bot PFPs (e.g. pixel art avatars stacked vertically), extract each into a separate file:

```python
from PIL import Image
import os

img = Image.open('/path/to/screenshot.jpg')
w, h = img.size
n = 8  # number of PFPs expected
part_h = h // n

bots = ['ducatо', 'hermesbro', 'el-froggo', 'groot', 'wannabe', 'designbro', 'contaibile', 'lawrenzo']
out = '<HERMES_ROOT>/shared/marketing/bot-profiles/pixel'
os.makedirs(out, exist_ok=True)

for i in range(n):
    crop = img.crop((0, i*part_h, w, (i+1)*part_h))
    # Make square
    cw, ch = crop.size
    if cw < ch:
        new = Image.new('RGB', (ch, ch), (10, 10, 15))
        new.paste(crop, ((ch-cw)//2, 0))
        crop = new
    elif cw > ch:
        left = (cw - ch) // 2
        crop = crop.crop((left, 0, left+ch, ch))
    crop = crop.resize((256, 256), Image.NEAREST)  # NEAREST preserves hard pixels
    crop.save(f'{out}/pfp-{bots[i]}.png', 'PNG')
```

Then copy to `bot-profiles/` with correct bot names and update HTML `<img src="...">` references.

**Pitfall:** The vision model may not identify bot names correctly from pixel art. Map bots by position in the screenshot (top→bottom) and cross-reference with the known bot list from the brand brief. "GROOT" in the screenshot = "Ratatouille" on the website (same bot, renamed).

**Pitfall:** `Image.NEAREST` is critical for pixel art — never use `Image.BILINEAR` or `Image.BICUBIC` which blur the hard pixel edges.

## Website Deployment (HermesBro Landing)

The landing page lives on Contabo (`YOUR_VPS_HOST/hermesbro/`). Local copy: `/root/hermesbro-landing.html`. No SSH access — modify locally, send HTML + assets to user for upload.

Directory structure on server:
```
/hermesbro/
├── index.html
├── bot-profiles/
│   ├── bot-profile-ratatouille-01.jpg
│   ├── bot-profile-contaibile-01.jpg
│   ├── bot-profile-lawrenzo-01.jpg
│   ├── bot-profile-wannabe-01.jpg
│   ├── bot-profile-designbro-01.jpg
│   ├── pixel-ratatouille.png      ← pixel art PFPs
│   ├── pixel-contaibile.png
│   ├── pixel-lawrenzo.png
│   ├── pixel-wannabe.png
│   ├── pixel-designbro.png
│   ├── pixel-ducatо.png
│   ├── pixel-el-froggo.png
│   └── pixel-hermesbro.png
```

**Pitfall:** The landing page is edited by multiple sessions (DesignBro, other bots). Always re-read before patching — `patch` will fail if the file was modified externally since last read.

See `references/vision-config-workaround.md` for configuring image analysis (Xiaomi mimo doesn't support vision — use OpenRouter + Gemini).

## Cross-Platform Limitations

**Telegram:** Bot non può inviare messaggi ad altri bot. Per consegnare asset ad un altro bot, passa i file all'utente umano che li inoltra manualmente.
