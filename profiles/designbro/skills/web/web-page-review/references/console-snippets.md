# Console Snippets for Web Review

Quick JS snippets to run in browser console during reviews.

## Design Audit

```javascript
(() => {
  const s = getComputedStyle(document.body);
  const colors = new Set();
  document.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.color !== 'rgb(0, 0, 0)') colors.add(cs.color);
    if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'rgb(255, 255, 255)')
      colors.add('bg:' + cs.backgroundColor);
  });
  return {
    bgColor: s.backgroundColor,
    font: s.fontFamily,
    colorCount: colors.size,
    colors: [...colors].slice(0, 15),
    svgs: document.querySelectorAll('svg').length,
    images: document.querySelectorAll('img').length,
    viewport: document.querySelector('meta[name="viewport"]')?.content,
    smoothScroll: getComputedStyle(document.documentElement).scrollBehavior,
    htmlSizeKB: Math.round(document.documentElement.outerHTML.length / 1024)
  };
})()
```

## Content Structure

```javascript
(() => ({
  title: document.title,
  h1: document.querySelector('h1')?.textContent,
  h2s: [...document.querySelectorAll('h2')].map(h => h.textContent),
  sections: document.querySelectorAll('section').length,
  links: document.querySelectorAll('a').length,
  forms: document.querySelectorAll('form').length,
  hasFavicon: !!document.querySelector('link[rel="icon"]'),
  hasOG: !!document.querySelector('meta[property^="og:"]'),
  hasViewport: !!document.querySelector('meta[name="viewport"]'),
  hasDescription: !!document.querySelector('meta[name="description"]')
}))()
```

## Animation Check

```javascript
(() => ({
  animations: document.querySelectorAll('[class*="anim"], [style*="animation"]').length,
  transitions: document.querySelectorAll('[style*="transition"]').length,
  scrollTriggers: document.querySelectorAll('[data-aos], [data-scroll], [class*="fade"]').length,
  totalMotion: document.querySelectorAll('[class*="anim"], [style*="animation"], [style*="transition"], [data-aos]').length
}))()
```

## External Resources Count

```javascript
(() => {
  const scripts = [...document.querySelectorAll('script[src]')].map(s => s.src);
  const styles = [...document.querySelectorAll('link[rel="stylesheet"]')].map(l => l.href);
  const fonts = [...document.querySelectorAll('link[href*="font"]')].map(f => f.href);
  return { scripts: scripts.length, styles: styles.length, fonts: fonts.length, total: scripts.length + styles.length };
})()
```
