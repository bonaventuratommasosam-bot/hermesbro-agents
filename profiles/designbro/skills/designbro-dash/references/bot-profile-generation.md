# Bot Profile Image Generation Patterns

## Variation Templates

Each variation creates a different visual style for the same bot. All use:
- 1080×1080px, dark background (#0a0a0f)
- Inter + JetBrains Mono fonts (Google Fonts @import)
- Bot color as accent (rgba for transparency)
- Centered emoji + name + description

### Variation 1: Spotlight Radial
Radial gradient glow behind the emoji circle. Dot grid background using bot color.

### Variation 2: Geometric/Triangles
Diagonal gradient background. Rotated border-only squares (45deg) as decorative elements.

### Variation 3: Minimal
Large emoji (160px) + bot name in bot color. No decoration. Cleanest option — good for website cards.

### Variation 4: Circuit Traces
Horizontal/vertical lines with endpoint dots. Tech aesthetic. Name below emoji circle with sector tag in mono font.

### Variation 5: Badge+Glow
Intense radial glow + concentric circle rings. Most dramatic option — good for hero/spotlight use.

## HTML Structure Pattern

```python
def make_html(bot, variation, width=1080, height=1080):
    r, g, b = hex_to_rgb(bot["color"])
    # ... variation-specific CSS for .glow, .grid-bg, decorative elements ...
    
    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: {width}px; height: {height}px;
    background: #0a0a0f;
    font-family: 'Inter', -apple-system, sans-serif;
    overflow: hidden;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    position: relative;
}}
{overlay_css}
{grid_css}
</style>
</head>
<body>
{decorative_divs}
{content}  <!-- emoji circle + name + desc -->
{bottom_bar}  <!-- HERMESBRO.COM + accent line -->
</body>
</html>'''
```

## Batch Generation in execute_code

```python
from hermes_tools import write_file, terminal
import os

OUT = "<HERMES_ROOT>/shared/marketing/bot-profiles"
os.makedirs(OUT, exist_ok=True)

bots = [
    {"name": "ContAIbile", "emoji": "📊", "color": "#3a86ff", ...},
    # ... all 5 bots ...
]

count = 0
for bot in bots:
    for v in range(1, 6):
        slug = bot["name"].lower().replace(" ", "-")
        html_path = f"{OUT}/bot-profile-{slug}-0{v}.html"
        jpg_path = f"{OUT}/bot-profile-{slug}-0{v}.jpg"
        
        html = make_html(bot, v)
        write_file(html_path, html)
        terminal(f"wkhtmltoimage --width 1080 --height 1080 --quality 95 --format jpg {html_path} {jpg_path}")
        
        if os.path.exists(jpg_path):
            count += 1

print(f"Generated {count}/25 images")
```

## Sending to Telegram

```bash
# Single test
python3 <HERMES_ROOT>/shared/scripts/send-photo.py CHAT_ID /path/to/bot-profile-wannabe-01.jpg "Test"

# Batch all 25
python3 <HERMES_ROOT>/shared/scripts/batch-send.py CHAT_ID <HERMES_ROOT>/shared/marketing/bot-profiles/ "Bot: "
```
