# Batch Visual HTML Template — Reference

## Base HTML Structure for Social Post Visuals

Each visual is a self-contained HTML file. No external dependencies except Google Fonts.

### Minimal Template (1080×1080)

```html
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    width:1080px; height:1080px;
    background:#0a0a0f;
    font-family:'Inter',sans-serif;
    overflow:hidden; position:relative;
  }
  .grid-bg {
    position:absolute; inset:0;
    background-image: radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size:40px 40px;
  }
  .glow {
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-60%);
    width:400px; height:400px;
    background:radial-gradient(circle, rgba(ACCENT_RGB,0.12) 0%, transparent 70%);
  }
  .bottom-bar {
    position:absolute; bottom:0; left:0; right:0;
    height:4px;
    background:linear-gradient(90deg, transparent, ACCENT_HEX, transparent);
    opacity:0.4;
  }
  .badge {
    position:absolute; top:40px; left:50px;
    font-family:'JetBrains Mono',monospace;
    font-size:11px; color:rgba(ACCENT_RGB,0.5);
    letter-spacing:3px; text-transform:uppercase;
  }
  .container {
    position:relative; z-index:1;
    width:100%; height:100%;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    padding:60px;
  }
  .logo-area {
    position:absolute; bottom:40px; right:50px;
    display:flex; align-items:center; gap:10px;
  }
  .logo-text {
    font-size:14px; color:rgba(255,255,255,0.3);
    font-weight:500; letter-spacing:2px; text-transform:uppercase;
  }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="glow"></div>
  <div class="badge">HERMES BOTS • CONTEXT</div>
  <div class="container">
    <!-- CONTENT HERE -->
  </div>
  <div class="bottom-bar"></div>
  <div class="logo-area">
    <svg width="32" height="32" viewBox="0 0 160 160" fill="none">
      <path d="M80 20 L60 60 L20 60 L50 85 L40 130 L80 105 L120 130 L110 85 L140 60 L100 60 Z"
            stroke="#d4a853" stroke-width="2" fill="none" opacity="0.4"/>
    </svg>
    <span class="logo-text">Hermes Bots</span>
  </div>
</body>
</html>
```

### Variations

**Thumbnail (video post):** Large number (JetBrains Mono, 120px bold, accent color) + subtitle + play button
**Prima/Dopo:** Split layout with flex, left side dark (#1a1a1a), right side with accent tint
**Sondaggio/Poll:** Stack of option cards with accent border, letter labels (A/B/C/D)
**Case Study:** Big metric numbers (JetBrains Mono, 56px bold) in accent colors
**Infographic (1080×1350):** Vertical stack, numbered items with colored left border
**Founder Story:** Flex row with avatar circle + italic quote (Georgia serif)

### Story Template (1080×1920)

Same base but:
- `width:1080px; height:1920px`
- `padding:80px 60px`
- Larger typography (numbers 140-160px, body 28-36px)
- `link-sticker` at bottom: rounded pill, accent bg, dark text
- `logo-area` centered at bottom (not right-aligned)

### Conversion Command

```bash
wkhtmltoimage --width 1080 --height 1080 --quality 95 --format jpg input.html output.jpg
# For stories:
wkhtmltoimage --width 1080 --height 1920 --quality 95 --format jpg input.html output.jpg
```

### Bot Accent Colors Reference

| Bot | Color | Hex | RGB |
|-----|-------|-----|-----|
| ContAIbile | Ocean Blue | `#3a86ff` | 58,134,255 |
| LAWrenzo | Royal Purple | `#8338ec` | 131,56,236 |
| GROOT | Forest Green | `#06d6a0` | 6,214,160 |
| Wannabe | Vibrant Orange | `#ff9f1c` | 255,159,28 |
| DesignBro | Hot Magenta | `#ff006e` | 255,0,110 |
| El Froggo | Golden Yellow | `#ffd60a` | 255,214,10 |
| HermesBro | Gold | `#d4a853` | 212,168,83 |
| Trust Blue | (links/CTA) | `#2563eb` | 37,99,235 |

### wkhtmltoimage Pitfalls

- Google Fonts may not render if no internet — fallback to system fonts
- Emoji rendering depends on system fonts installed (🐸⚖️📱 work on Linux with Noto)
- `--quality 95` is sweet spot; 100 produces huge files with no visible gain
- Always check file size after conversion; >200KB for 1080×1080 is too heavy
