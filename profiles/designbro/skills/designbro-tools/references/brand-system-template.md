# Brand System HTML Template — Reference

## SVG Logo Path Data

The Hermes wings are built from two mirrored cubic Bezier curves + a vertical staff + a circle orb.

### Wing paths (left + right mirror)
```
Left:  M80 22 C65 32, 38 42, 22 68 C16 80, 22 90, 34 86 C50 80, 62 68, 76 56
Right: M80 22 C95 32, 122 42, 138 68 C144 80, 138 90, 126 86 C110 80, 98 68, 84 56
```

### Staff + orb
```
Staff: M80 52 L80 138   (stroke-width 1.5, 25% white opacity)
Orb:   cx=80 cy=44 r=8  (stroke only, no fill)
Dot:   cx=80 cy=44 r=2.5 (filled, 60% opacity)
```

### Feather accents (optional, hide at small sizes)
```
Left:  M48 62 C56 54, 66 48, 78 44   (30% gold opacity)
Right: M112 62 C104 54, 94 48, 82 44
Speed: M28 72 L14 68  /  M132 72 L146 68  (20% opacity)
```

### Size adaptations
- **120px+**: Full detail (wings + staff + orb + dot + feathers + speed lines)
- **80px**: Wings + staff + orb (drop feathers and speed lines)
- **48px**: Wings only, stroke-width bumped to 5px

## HTML Skeleton

```html
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Brand} — Brand System</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --ink: #0a0a0f;
  --ink-soft: #18181b;
  --surface: #fafaf9;
  --muted: #71717a;
  --accent: {trust_blue};
  --gold: {accent_color};
  --gold-dark: {accent_dark};
  --gold-glow: {accent_with_alpha_0.15};
  --radius: 16px;
  --mono: 'JetBrains Mono', monospace;
  --sans: 'Inter', -apple-system, sans-serif;
}
/* ... */
</style>
</head>
<body>
  <nav class="nav">...</nav>
  <div class="hero">...</div>
  <section id="identity">...</section>
  <section id="logo">...</section>
  <section id="palette">...</section>
  <section id="type">...</section>
  <section id="social">...</section>
  <section id="tone">...</section>
  <div class="footer">...</div>
</body>
</html>
```

## Key CSS Patterns

### SVG draw-in animation
```css
.logo-mark svg .wing-path {
  stroke-dasharray: 400;
  stroke-dashoffset: 400;
  animation: drawWing 1.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
@keyframes drawWing { to { stroke-dashoffset: 0; } }
```

### Hero fade-up stagger
```css
.hero .brand-name { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both; }
.hero .tagline    { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.7s both; }
.hero .cta-group  { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 1s both; }
```

### Glassmorphism nav
```css
.nav {
  background: rgba(10,10,15,0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
```

### Social preview aspect ratios
```css
.social-preview-inner { aspect-ratio: 1/1; }        /* IG post */
.social-preview-inner.story { aspect-ratio: 9/16; }  /* IG story */
.social-preview-inner.landscape { aspect-ratio: 1.91/1; } /* LinkedIn */
/* X header: aspect-ratio: 3/1 (inline) */
```

## Reference implementation
`{{HERMES_HOME}}/hermesbro-brand.html` — full working example with all sections, animations, and responsive breakpoints.
