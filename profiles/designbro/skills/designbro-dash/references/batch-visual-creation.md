# Batch Visual Creation — execute_code Pattern

Proven workflow for generating 25+ social media visuals in one `execute_code` call.

## Structure

```python
from hermes_tools import write_file, terminal
import os

OUT = "<HERMES_ROOT>/shared/marketing/giugno-2026"
os.makedirs(OUT, exist_ok=True)

# ── Helper functions ──

def rgb_hex(hex_color):
    """Convert hex to R,G,B string for rgba() in CSS."""
    h = hex_color.lstrip('#')
    return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"

def css_base(accent, width=1080, height=1080):
    """Common CSS: grid-bg, glow, circuit traces, fonts."""
    return f"""@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{width}px; height:{height}px; background:#0a0a0f; font-family:'Inter',sans-serif; overflow:hidden; position:relative; }}
.grid-bg {{ position:absolute; inset:0; background-image:radial-gradient(circle,rgba(255,255,255,0.03) 1px,transparent 1px); background-size:40px 40px; }}
.glow {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-60%); width:400px; height:400px; background:radial-gradient(circle,rgba({rgb_hex(accent)},0.12) 0%,transparent 70%); }}
.bottom-bar {{ position:absolute; bottom:0; left:0; right:0; height:4px; background:linear-gradient(90deg,transparent,{accent},transparent); opacity:0.4; }}
.logo-area {{ position:absolute; bottom:40px; right:50px; display:flex; align-items:center; gap:10px; }}
.logo-text {{ font-family:'Inter',sans-serif; font-size:14px; color:rgba(255,255,255,0.3); font-weight:500; letter-spacing:2px; text-transform:uppercase; }}
.badge {{ position:absolute; top:40px; left:50px; font-family:'JetBrains Mono',monospace; font-size:11px; color:rgba({rgb_hex(accent)},0.5); letter-spacing:3px; text-transform:uppercase; }}
"""

def logo_html():
    """HermesBots logo SVG + text."""
    return """<div class="logo-area">
<svg class="logo-mark" width="32" height="32" viewBox="0 0 160 160" fill="none">
<path d="M80 20 L60 60 L20 60 L50 85 L40 130 L80 105 L120 130 L110 85 L140 60 L100 60 Z" stroke="#d4a853" stroke-width="2" fill="none" opacity="0.4"/>
</svg>
<span class="logo-text">Hermes Bots</span>
</div>"""

def wrap_html(title, badge_text, accent, body_html, width=1080, height=1080):
    """Full page wrapper with all common elements."""
    return f"""<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8">
<meta name="viewport" content="width={width}">
<style>{css_base(accent, width, height)}</style></head><body>
<div class="grid-bg"></div><div class="glow"></div>
<div class="badge">{badge_text}</div>
<div class="container">{body_html}</div>
<div class="bottom-bar"></div>
{logo_html()}
</body></html>"""

# ── Create all HTML files ──

# Visual 1: Bot Spotlight
body_v1 = """
<div style="font-size:100px;">🐸</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:48px;font-weight:700;color:#ffd60a;">El Froggo</div>
<div style="font-size:20px;color:rgba(255,255,255,0.5);letter-spacing:6px;text-transform:uppercase;">Il bot dietro le quinte</div>
"""
write_file(f"{OUT}/visual-01-el-froggo.html", wrap_html("Spotlight", "HERMES BOTS", "#ffd60a", body_v1))

# ... repeat for each visual ...

# ── Batch convert HTML → JPG ──
result = terminal(f"ls {OUT}/*.html")
html_files = [f.strip() for f in result['output'].strip().split('\n') if f.strip()]

for html_path in html_files:
    jpg_path = html_path.replace('.html', '.jpg')
    # Detect dimensions from filename
    if '1920' in html_path:
        w, h = 1080, 1920
    elif '1350' in html_path:
        w, h = 1080, 1350
    else:
        w, h = 1080, 1080
    terminal(f"wkhtmltoimage --width {w} --height {h} --quality 95 --format jpg {html_path} {jpg_path}")

# ── Send all via Bot API ──
terminal(f"python3 <HERMES_ROOT>/shared/scripts/send-all-photos.py CHAT_ID {OUT}")
```

## Tips

- Keep HTML files as source — user will request changes later
- Use `execute_code` (not sequential tool calls) for 10+ files — much faster
- Helper functions (`css_base`, `wrap_html`, `logo_html`) ensure visual consistency
- JPG quality 95 is the sweet spot for dark backgrounds
- `wkhtmltoimage` renders Google Fonts correctly — no local font files needed
