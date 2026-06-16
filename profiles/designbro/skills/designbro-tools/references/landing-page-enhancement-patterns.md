# Landing Page Enhancement Patterns

Reusable CSS/JS snippets for upgrading dark-theme landing pages. Tested on HermesBro landing (Inter + JetBrains Mono + Orbitron, Ink #0a0a0f palette).

## 1. Animated Mesh Gradient Background

Slow-moving radial gradients that give life to flat dark backgrounds. Subtle — 6-10% opacity max.

```css
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 50% at 20% 30%, rgba(37,99,235,0.08) 0%, transparent 70%),
    radial-gradient(ellipse 50% 60% at 80% 70%, rgba(212,168,83,0.06) 0%, transparent 70%),
    radial-gradient(ellipse 40% 40% at 50% 50%, rgba(37,99,235,0.04) 0%, transparent 60%);
  animation: meshShift 12s ease-in-out infinite alternate;
  pointer-events: none;
  z-index: 0;
}

@keyframes meshShift {
  0% {
    background:
      radial-gradient(ellipse 60% 50% at 20% 30%, rgba(37,99,235,0.08) 0%, transparent 70%),
      radial-gradient(ellipse 50% 60% at 80% 70%, rgba(212,168,83,0.06) 0%, transparent 70%),
      radial-gradient(ellipse 40% 40% at 50% 50%, rgba(37,99,235,0.04) 0%, transparent 60%);
  }
  50% {
    background:
      radial-gradient(ellipse 55% 55% at 70% 20%, rgba(37,99,235,0.1) 0%, transparent 70%),
      radial-gradient(ellipse 60% 50% at 30% 80%, rgba(212,168,83,0.08) 0%, transparent 70%),
      radial-gradient(ellipse 45% 45% at 50% 40%, rgba(37,99,235,0.05) 0%, transparent 60%);
  }
  100% {
    background:
      radial-gradient(ellipse 50% 60% at 50% 60%, rgba(37,99,235,0.07) 0%, transparent 70%),
      radial-gradient(ellipse 55% 45% at 20% 40%, rgba(212,168,83,0.07) 0%, transparent 70%),
      radial-gradient(ellipse 40% 50% at 80% 30%, rgba(37,99,235,0.06) 0%, transparent 60%);
  }
}
```

**Pitfall:** `background` in `@keyframes` replaces (not interpolates) the entire value. All 3 keyframes must list all 3 gradients — if you omit one, it snaps.

## 2. SVG Noise Shapes (coolshap.es style)

Decorative shapes with grainy texture using SVG `feTurbulence` filter. Place in hero, pricing, and CTA sections.

```html
<svg width="120" height="120" viewBox="0 0 120 120" fill="none"
  style="position:absolute;top:15%;left:8%;opacity:0.15;animation:floatA 8s ease-in-out infinite;">
  <defs>
    <filter id="noise1">
      <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
  </defs>
  <circle cx="60" cy="60" r="50" fill="url(#g1)" filter="url(#noise1)"/>
  <radialGradient id="g1">
    <stop offset="0%" stop-color="#2563eb"/>
    <stop offset="100%" stop-color="transparent"/>
  </radialGradient>
</svg>
```

Float animations:
```css
@keyframes floatA {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}
@keyframes floatB {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(-3deg); }
}
```

**Rules:**
- Max 4-5 shapes per page. More = noise, not decoration.
- Opacity 0.08-0.15. Never more.
- Each shape needs unique `id` for filter and gradient (no duplicates).
- Hide on mobile: `.deco-shape { display: none; }` in `@media (max-width: 768px)`.
- Disable in reduced motion: `.deco-shape { animation: none !important; }`.

## 3. Staggered Scroll Reveal (IntersectionObserver)

Elements with class `.reveal` start invisible and enter in cascade when scrolled into view.

CSS:
```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

JS — sibling-aware stagger (NOT global index):
```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const siblings = Array.from(entry.target.parentElement.children)
        .filter(c => c.classList.contains('reveal'));
      const idx = siblings.indexOf(entry.target);
      setTimeout(() => entry.target.classList.add('visible'), idx * 120);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

**Pitfall:** Using the global `entries.forEach((entry, i) => ...)` index for stagger delay is WRONG — `i` is the index within the current IntersectionObserver batch, not the element's position among siblings. Elements in different sections get random delays. Always calculate sibling index.

**Pitfall:** `rootMargin: '0px 0px -50px 0px'` triggers slightly before the element is fully in view, giving the animation time to start before the user focuses on it. Without this, animations feel late.

## 4. Hover Micro-interactions

### Product cards
```css
.product-card:hover {
  background: rgba(250,250,249,0.07);
  border-color: rgba(212,168,83,0.2);
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 8px 40px rgba(212,168,83,0.12), 0 0 0 1px rgba(212,168,83,0.15);
}
```

### Pricing cards (subtler)
```css
.pricing-card:hover {
  border-color: rgba(212,168,83,0.2);
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 8px 40px rgba(212,168,83,0.1), 0 0 0 1px rgba(212,168,83,0.12);
}
```

**Rules:**
- Product cards: `scale(1.02)`, pricing cards: `scale(1.01)` — pricing needs to feel stable.
- Gold shadow (`rgba(212,168,83,...)`) on brand with gold accent; use blue shadow for blue-accent brands.
- Featured/pricing-card with `scale(1.02)` base needs adjusted hover: `scale(1.02) translateY(-4px)`.

## 5. Sweep Reveal (Tagline)

Text reveals left-to-right with `clip-path`. More interesting than plain fadeUp.

```css
.sweep-reveal {
  animation: sweepReveal 1.2s ease 0.6s both;
  overflow: hidden;
}

@keyframes sweepReveal {
  0% {
    opacity: 0;
    transform: translateY(20px);
    clip-path: inset(0 100% 0 0);
  }
  60% {
    opacity: 1;
    transform: translateY(0);
    clip-path: inset(0 20% 0 0);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
    clip-path: inset(0 0% 0 0);
  }
}
```

**Pitfall:** `clip-path: inset()` animates independently from `opacity`. The 60% keyframe lifts opacity to 1 early while clip-path still has 20% hidden — this creates a natural "typing" feel. If you set both to 100%, it looks like a simple wipe.

## 6. Cursor Glow

Subtle radial gradient that follows the mouse. Gives depth perception.

```css
.cursor-glow {
  position: fixed;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212,168,83,0.04) 0%, transparent 70%);
  pointer-events: none;
  z-index: 1;
  transform: translate(-50%, -50%);
  transition: left 0.3s ease, top 0.3s ease;
}
```

```js
const cursorGlow = document.createElement('div');
cursorGlow.className = 'cursor-glow';
document.body.appendChild(cursorGlow);
document.addEventListener('mousemove', (e) => {
  cursorGlow.style.left = e.clientX + 'px';
  cursorGlow.style.top = e.clientY + 'px';
});
```

**Rules:**
- Hide on mobile/touch: `display: none` in `@media (max-width: 768px)`.
- Hide in reduced motion: `.cursor-glow { display: none; }`.
- Opacity 0.03-0.05. It's a whisper, not a spotlight.
- Use accent color, not white.

## Accessibility Checklist

Always include in `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-delay: 0ms !important;
    transition-duration: 0.01ms !important;
  }
  .cursor-glow { display: none; }
  .deco-shape { animation: none !important; }
}
```

Force-visible helper for dev/testing (paste in console):
```js
document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
```
