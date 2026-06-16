# Brand Palette Extraction Reference

## Browser Console JS Snippets

### All CSS Custom Properties (`:root` variables)
```javascript
(function() {
  const vars = {};
  for (let s of document.styleSheets) {
    try {
      for (let r of s.cssRules) {
        if (r.selectorText === ':root' || r.selectorText === '*') {
          for (let p of r.style) {
            if (p.startsWith('--')) vars[p] = r.style.getPropertyValue(p);
          }
        }
      }
    } catch(e) {}
  }
  return JSON.stringify(vars, null, 2);
})();
```

### Computed Colors (foreground + background)
```javascript
(function() {
  const allEls = document.querySelectorAll('*');
  const uColors = new Set();
  const uBgs = new Set();
  allEls.forEach(el => {
    const c = getComputedStyle(el);
    if (c.color !== 'rgb(0, 0, 0)') uColors.add(c.color);
    if (c.backgroundColor !== 'rgba(0, 0, 0, 0)') uBgs.add(c.backgroundColor);
  });
  return JSON.stringify({
    topColors: [...uColors].slice(0, 15),
    topBgs: [...uBgs].slice(0, 15)
  }, null, 2);
})();
```

### Typography (key elements)
```javascript
(function() {
  const els = ['h1','h2','h3','h4','body','nav','button','a','code','pre'];
  const r = {};
  els.forEach(sel => {
    const el = document.querySelector(sel);
    if (el) {
      const c = getComputedStyle(el);
      r[sel] = {
        fontFamily: c.fontFamily,
        fontSize: c.fontSize,
        fontWeight: c.fontWeight,
        letterSpacing: c.letterSpacing,
        lineHeight: c.lineHeight,
        color: c.color,
        textTransform: c.textTransform
      };
    }
  });
  return JSON.stringify(r, null, 2);
})();
```

### Bot/Component Accent Colors
```javascript
(function() {
  const cards = document.querySelectorAll('.product-card, [class*="bot"], [class*="card"]');
  const r = [];
  cards.forEach(card => {
    const tag = card.querySelector('.product-tag, [class*="tag"], h3');
    const icon = card.querySelector('.product-icon, [class*="icon"]');
    r.push({
      name: tag?.textContent?.trim(),
      bg: getComputedStyle(card).backgroundColor,
      border: getComputedStyle(card).borderColor
    });
  });
  return JSON.stringify(r, null, 2);
})();
```

### Gradient Backgrounds
```javascript
(function() {
  const grads = [];
  document.querySelectorAll('*').forEach(el => {
    const bg = getComputedStyle(el).backgroundImage;
    if (bg && bg !== 'none' && bg.includes('gradient')) {
      grads.push(bg.substring(0, 300));
    }
  });
  return JSON.stringify([...new Set(grads)].slice(0, 10), null, 2);
})();
```

## RGB to Hex Conversion
```javascript
function rgbToHex(rgb) {
  const m = rgb.match(/\d+/g);
  if (!m || m.length < 3) return rgb;
  return '#' + m.slice(0,3).map(x => (+x).toString(16).padStart(2,'0')).join('');
}
```

## Common CSS Variable Naming Patterns
| Pattern | Example | Usually |
|---------|---------|---------|
| `--color-*` | `--color-primary` | Main brand color |
| `--bg-*` | `--bg-dark` | Background |
| `--text-*` | `--text-muted` | Text color |
| `--accent` | `--accent` | Highlight/CTA |
| `--font-*` | `--font-heading` | Font family |
| `--radius` | `--radius` | Border radius |
| `--spacing-*` | `--spacing-lg` | Whitespace |

## Pitfalls
- CORS blocks cross-origin stylesheets — only same-origin rules are accessible via `sheet.cssRules`
- Some sites use CSS-in-JS (styled-components, emotion) — variables may not be in `:root` rules
- `getComputedStyle` returns computed values, not declared — rgba() may appear where hex was declared
- Always check both light and dark themes if the site supports switching
- Font stacks may include fallbacks — strip `-apple-system, BlinkMacSystemFont, sans-serif` to get the actual custom font
