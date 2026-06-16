# Design Inspiration Sources

Curated sites for landing pages, UI patterns, motion design, and visual assets.

## Curated Galleries

| Site | Focus | URL |
|------|-------|-----|
| siteInspire | 2,068+ curated websites by style/category | siteinspire.com (mirror: siteinspire.net) |
| 60fps.design | 1,956 UI/UX animation shots from 458 apps | 60fps.design |
| logggos.club | Logo design inspiration | logggos.club |
| uncut.wtf | Typography & font exploration | uncut.wtf |

## Assets & Tools

| Site | What it offers | URL |
|------|---------------|-----|
| coolshap.es | 100+ abstract shapes with grainy gradient textures (SVG/JSX/PNG), MIT license, Figma file available | coolshap.es |
| thiings.co | 3D animated objects/icons | thiings.co |
| endlesstools.io | 3D text, AI textures, visual effects, web embeds (PRO $24.99/mo) | endlesstools.io |
| shadergpt.14islands.com | Shader/gradient generation | shadergpt.14islands.com |

## Key Design Patterns (from 60fps.design)

### Micro-interactions for landing pages
- **Staggered entrance animations** — elements cascade in with slight delays
- **Spring-based easing** — physics-based curves, not linear/ease-in-out
- **Hover micro-animations** — scale(1.02), shadow shift, reveal secondary elements
- **Animated gradients** — slowly shifting background for sense of life
- **Scroll-triggered reveals** — IntersectionObserver fade+slide from bottom
- **Typing/sweep effects** — hero text appears character by character or sweeps in
- **Skeleton shimmer** — pulse loading states instead of spinners
- **Cursor-responsive parallax** — tilt/depth on mouse move

### Premium visual elements (from coolshap.es)
- Grainy gradient shapes as hero decorations
- Noise texture overlays for depth
- Abstract geometric forms in brand accent color

## Research Workflow

When user shares design inspiration links (X posts, bookmarks, etc.):

1. **Extract content** — use `browser_navigate` + `browser_vision` (NOT `web_extract` — see pitfall below)
2. **Explore top 3-4 sites** — parallel via `delegate_task` with `browser` toolset
3. **Audit current project** — screenshot existing page/asset with `browser_vision`
4. **Match patterns to project** — which improvements have highest impact for lowest effort?
5. **Propose concrete changes** — specific CSS/JS snippets, not vague "make it better". For implementation patterns (mesh gradients, noise shapes, stagger reveal, hover effects, sweep animations), see `references/landing-page-enhancement-patterns.md`.

## Pitfalls

### X/Twitter content extraction
`web_extract` does NOT work for X/Twitter URLs (returns DuckDuckGo search-only error). Use:
```
browser_navigate(url) → browser_vision(question="read the post text and describe content")
```
Works for posts, threads, and profiles. Screenshots capture the content even when the DOM doesn't load properly.

### siteInspire bot detection
siteinspire.com (now on Vercel) blocks automated browsers with a security checkpoint. Use the mirror site `siteinspire.net` — same curated database, no bot detection.

### endlesstools.io pricing
The 3D/AI tools are paid ($24.99/mo PRO). Free tier is 3-day trial only. Factor cost into recommendations — prefer free alternatives (coolshap.es SVGs, CSS gradients) for budget-conscious clients.
