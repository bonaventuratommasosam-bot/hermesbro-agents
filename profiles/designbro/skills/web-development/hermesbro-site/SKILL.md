---
name: hermesbro-site
description: "Maintain hermesbro.cloud — the HermesBro landing page + multitenant backend. Covers site structure, design system, backend templates, SVG icons, and deployment."
version: 3.0
tags: [hermesbro, website, landing-page, html, backend, svg-icons, dark-theme, marketing]
related_skills: [marketing-materials-workflow, web-page-review, affiliate-microsite-deploy]
---

# hermesbro-site — HermesBro Website

## When to use
- Editing, fixing, or updating https://hermesbro.cloud
- Working on the multitenant backend ({BACKEND_ROOT}/)
- Replacing assets (PFPs, images, icons)
- Fixing broken buttons/links
- Adding/modifying sections or pages
- i18n updates (IT/EN)

## CRITICAL PREFERENCE: NO EMOJIS
[REDACTED — dati personali rimossi] explicitly said: "Le emoji non mi piacciono sono troppo infantili."
**ALL icons must be SVG Lucide-style inline SVGs.** Never use emoji characters for icons.
Use the SVG icon pattern documented below. This applies to ALL pages — landing, register, panel, etc.

## Navbar conventions — subpages vs landing

**Landing page (index.html)**: full nav — Casi d'uso, War Room, Agenti, Skill, Prezzi, Waitlist, IT/EN toggle, CTA button.

**Subpages (skills.html, agent pages, etc.)**: MINIMAL nav — only Home + current page + IT/EN toggle. NO "Agenti", NO "Prova Gratis", NO other links. <FOUNDER> explicitly removed them: "i link AGENTI e PROVA GRATIS VANNO tolti".

Pattern for subpage nav:
```html
<nav>
  <a href="/" class="nav-brand">HERMES<span class="bro">BRO</span></a>
  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/pagename.html" class="active">PageName</a>
    <div class="lang-toggle">
      <button class="lang-btn active" data-lang="it" onclick="setLang('it')">IT</button>
      <button class="lang-btn" data-lang="en" onclick="setLang('en')">EN</button>
    </div>
  </div>
</nav>
```

## IT/EN language toggle pattern

All public pages must have IT/EN toggle. Use `data-it` / `data-en` attributes on text elements:

```html
<h1 data-it="I superpoteri dei tuoi agenti" data-en="Your agents' superpowers">I superpoteri dei tuoi agenti</h1>
<p data-it="Descrizione IT" data-en="EN description">Descrizione IT</p>
<input data-it="Cerca..." data-en="Search..." placeholder="Cerca...">
```

JS (add before `</script>`):
```js
let currentLang = localStorage.getItem('lang') || 'it';
function setLang(lang) {
  currentLang = lang;
  localStorage.setItem('lang', lang);
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
  document.querySelectorAll('[data-it][data-en]').forEach(el => {
    el.textContent = el.getAttribute('data-' + lang);
    if (el.hasAttribute('placeholder')) el.placeholder = el.getAttribute('data-' + lang);
  });
}
setLang(currentLang);
```

CSS for toggle:
```css
.lang-toggle{display:flex;gap:4px;margin-left:16px}
.lang-btn{padding:4px 10px;border-radius:6px;border:1px solid var(--border);background:transparent;color:var(--muted);font-size:12px;font-weight:600;cursor:pointer;transition:all 0.2s;font-family:var(--sans)}
.lang-btn.active{background:var(--gold);color:var(--ink);border-color:var(--gold)}
```

**Pitfall**: for complex HTML content (like capability lists with SVGs), `data-en` on the `<ul>` is fragile — prefer static Italian content or use JS that rebuilds innerHTML.

## Site structure

### Static site — `{WEB_ROOT}/`
```
├── index.html          ← main landing page (single-file, all CSS/JS inline)
├── register.html       ← waitlist page (3-step: sector → agents → email signup)
├── panel.html          ← client dashboard (agent table, stats, actions)
├── bot-profiles/       ← pixel art PFPs for each agent
│   ├── pixel-contaibile.png
│   ├── pixel-designbro.png
│   ├── pixel-ducato.png
│   ├── pixel-el-froggo.png
│   ├── pixel-groot.png
│   ├── pixel-hermesbro.png
│   ├── pixel-lawrenzo.png
│   ├── pixel-machiavelli.png
│   ├── pixel-mr-robot.png
│   ├── pixel-sentinel.png
│   └── pixel-wannabe.png
├── img/                ← general images (agent PNGs, OG image)
├── brand.html          ← brand guidelines page
├── landing.html        ← older/alternate landing
├── investitori/        ← investor materials
├── privacy-policy.html
├── agents/             ← individual agent profile pages (static HTML)
│   ├── contaibile.html
│   ├── lawrenzo.html
│   ├── wannabe.html
│   ├── designbro.html
│   ├── ducato.html
│   ├── el-froggo.html
│   ├── groot.html
│   ├── machiavelli.html
│   ├── sentinel.html
│   └── mr-robot.html
├── skills.html         ← skills listing page (embedded JSON, search, filters, IT/EN)
├── robots.txt
├── sitemap.xml
└── index.html.bak      ← backup before last edit
```

### Multitenant backend — `{BACKEND_ROOT}/`
```
├── hermesbro_multitenant_backend.py  ← FastAPI app (uvicorn, port 8333)
├── templates/
│   ├── register.html   ← Jinja2 template with {{SECTORS}}, {{AGENTS}}
│   └── panel.html      ← Jinja2 template
└── venv/               ← Python virtual environment
```

**NOTE**: `/warroom` is served by the **standalone War Room service** on port 8097 (NOT the multitenant backend). The standalone service at `/home/[REDACTED — dati personali rimossi]/ai-stack/warroom/main.py` uses WebSocket for real-time streaming, has a moderator agent (HermesRibbitBot), workflow templates, and proper multi-round agent discussion. See `references/warroom-standalone.md` for the full architecture.

The multitenant backend (port 8333) still has an older inline HTML warroom page + `/api/warroom` SSE endpoint (used by the landing page demo section), but the primary `/warroom` route now points to the standalone service.

**Services**:
- `warroom.service` (systemd, port 8097) — standalone War Room with WebSocket
- `hermesbro-multitenant.service` (systemd, port 8333) — backend + older warroom API
**Restart**: `systemctl restart hermesbro-multitenant.service` (preferred — systemd manages auto-restart)
**Manual start** (only if service is stopped): `cd {BACKEND_ROOT} && ./venv/bin/python hermesbro_multitenant_backend.py`
**PITFALL**: Do NOT start uvicorn manually while the systemd service is running — both fight for port 8333 → `[Errno 98] address already in use`. Always check `systemctl status hermesbro-multitenant.service` first. If you killed the port with `fuser -k 8333/tcp`, the service auto-restarts — wait rather than starting manually.

### nginx config
- `/etc/nginx/sites-enabled/hermesbro.cloud` — main site config
- `/etc/nginx/sites-enabled/stack` — alternative/legacy config
- Static files served directly from `{WEB_ROOT}/`
- `/api/*` and dynamic routes proxied to `127.0.0.1:8333` (uvicorn/FastAPI)
- `/warroom` proxied to `127.0.0.1:8097` (standalone War Room service, NOT the multitenant backend)
- `/warroom/ws/` proxied to `127.0.0.1:8097` with rewrite + WebSocket upgrade (for War Room frontend WS connections)
- `/ws/` proxied to `127.0.0.1:8097` with WebSocket upgrade support (`proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "upgrade"; proxy_read_timeout 86400;`)
- Dynamic pages: `/register`, `/panel` — `location = /path` (exact match, NO trailing slash)
- SSE endpoint: `/api/warroom` — requires `proxy_buffering off`, `proxy_read_timeout 600s` (see Pitfalls)
- `/agents/` — **static files** served directly from `{WEB_ROOT}/agents/` (`try_files $uri $uri/ =404`). NOT proxied to backend.
- `/dashboard/` — `location /dashboard/` (prefix match, proxied to backend)
- Static cache zone: `static_cache` (100MB inactive=10m)
- Cache bypass: `X-No-Cache: 1` header
- **CRITICAL**: `location = /warroom` (exact) does NOT match `/warroom/` — trailing slash falls through to `try_files $uri $uri/ /index.html` which serves the main landing page. Always link without trailing slash.

## Design system

### Colors
```css
--ink: #0a0a0f;          /* background */
--ink-light: #12121a;    /* cards, panels */
--ink-lighter: #1a1a2e;  /* hover states, secondary bg */
--gold: #d4a853;         /* primary accent */
--gold-dim: #c9a84c26;   /* subtle gold backgrounds */
--blue: #2563eb;         /* secondary accent */
--white: #f1f1f1;        /* primary text */
--white-dim: #8888a0;    /* secondary text */
```

### Typography
- **Headings**: `'Orbitron', sans-serif`
- **Body**: `'Inter', sans-serif`
- **Mono**: `'JetBrains Mono', monospace`
- **Base size**: 14px
- **Font smoothing**: antialiased

### Spacing & Layout
- **Border radius**: 14px (cards), 10px (buttons), 8px (inputs)
- **Card padding**: 24px
- **Section gap**: 80px
- **Max width**: 1280px (content), 480px (form containers)
- **Glass morphism**: `backdrop-filter: blur(12px) saturate(1.4)`

### Animations
- **Fade-up**: `translateY(20px)` → `translateY(0)`, 600ms, ease-out
- **Stagger**: 100ms per element via `animation-delay`
- **Gold glow hover**: `box-shadow: 0 0 15px rgba(212,168,83,0.4)`
- **Card hover**: `translateY(-3px)` + gold border glow
- **Step connectors**: pulse animation on active step dots

## SVG Icon Pattern (Lucide-style)

**Always use this pattern instead of emojis.** 24x24 viewBox, stroke-based, no fill.

### Sector icons (used in register.html cards and panel.html backend):
```html
<!-- Food & Beverage -->
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>

<!-- Fashion & Luxury -->
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.38 3.46 16 2 12 5.5 8 2l-4.38 1.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/></svg>

<!-- Professional Services -->
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>

<!-- E-Commerce & Retail -->
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>

<!-- Automotive & Mobility -->
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>

<!-- Real Estate & Construction -->
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
```

### Action icons (used in panel.html buttons):
```html
<!-- Provision (rocket) -->
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>

<!-- Reset (refresh-cw) -->
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>

<!-- Delete (trash-2) -->
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>

<!-- Search (search) -->
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
```

### How to add a new SVG icon
1. Go to https://lucide.dev/icons/
2. Find the icon, click it
3. Copy the SVG markup
4. Adjust `width`/`height` to match context (14px for buttons, 20px for cards, 24px for headers)
5. Set `stroke="currentColor"` so it inherits text color

### Demo section (landing page)
The demo section (`#demoScenarios` + `#demoSelect`) on the landing page uses **real agent responses** via `/api/demo` (single-agent SSE endpoint). No more `demoResponses` JS object — removed entirely. The button says "Analizza" (not "Simula risposta"). The response area shows real output from the selected Hermes agent profile. Agent takes ~30-60s to respond. The `/api/demo` endpoint streams a single SSE `response` event with the agent's text. Frontend uses `fetch()` + ReadableStream (not EventSource, since EventSource doesn't support POST). Scenario shortcut buttons (`data-scenario`) auto-select the agent and prefill the textarea.

### API endpoints summary
- `POST /api/warroom` — SSE, multi-agent chain discussion (2-4 agents + Machiavelli synthesis)
- `POST /api/demo` — SSE, single-agent demo for landing page (1 agent, no synthesis)
- `POST /api/orchestrate` — JSON, full orchestration (non-streaming)
- `POST /api/waitlist` — JSON, waitlist signup (`{email, sector, agents, name?}`) → saves to DB
- `POST /api/contact` — JSON, contact form submission (`{name, email, company?, phone?, message}`) → saves to `contacts` table, returns `{status: "ok", message: "Messaggio ricevuto, ti contatteremo presto"}`

### SSE API pattern (used by /api/warroom and /api/demo)
```python
from starlette.responses import StreamingResponse

@app.post("/api/warroom")
async def api_warroom(request: Request):
    body = await request.json()
    # ... validate input ...

    async def event_stream():
        # Stream events as JSON
        yield "data: " + json.dumps({"type": "status", "message": "..."}) + "\n\n"
        # Run blocking work in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: run_hermes(profile, prompt))
        yield "data: " + json.dumps({"type": "response", "text": result["response"]}) + "\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
    )
```

**IMPORTANT**: Always use string concatenation (`"data: " + json.dumps(...) + "\n\n"`) NOT f-strings for SSE yields — nested f-strings with dicts cause SyntaxError. See Pitfalls.

## Backend template system

The backend (`hermesbro_multitenant_backend.py`) renders pages with Jinja2 templates for register and panel. **War Room (`/warroom`) is inline HTML** — a Python triple-quoted string inside the `warroom_page()` FastAPI route. **War Room API (`/api/warroom`) is a StreamingResponse** — SSE endpoint that runs agents via `orchestrator.run_hermes()` and streams results as JSON events. Key pattern:

### Sector injection
```python
# In hermesbro_multitenant_backend.py — sectors defined as list of dicts
SECTORS = [
    {"id": "food", "name": "Food & Beverage", "icon": "coffee"},
    {"id": "fashion", "name": "Fashion & Luxury", "icon": "gem"},
    ...
]

# Template receives: {{SECTORS}} and {{AGENTS}}
```

### register.html template pattern
```html
<!-- Sector options rendered dynamically -->
{% for sector in SECTORS %}
<label class="sector-option" data-sector="{{ sector.id }}">
  <input type="checkbox" name="sectors" value="{{ sector.id }}">
  <span class="sector-icon">{{ sector.icon_svg|safe }}</span>
  <span>{{ sector.name }}</span>
</label>
{% endfor %}
```

### Agent checkboxes with toggle
```html
{% for agent in AGENTS %}
<label class="agent-option {{ 'premium-agent' if agent.is_premium }}">
  <input type="checkbox" name="agents" value="{{ agent.id }}">
  <span class="agent-name">{{ agent.name }}</span>
  {% if agent.is_premium %}
  <span class="premium-tag">PRO</span>
  {% endif %}
</label>
{% endfor %}
```

## Agent card structure (in #agenti section of index.html)

Each agent card uses this pattern:
```html
<div class="acard reveal" data-cat="business">
  <div class="tp">
    <img src="/bot-profiles/pixel-NAME.png" alt="NAME" class="ic-img">
    <div class="nc"><h3>NAME</h3><span class="cat">Category</span></div>
  </div>
  <div class="uses">...</div>
  <div class="rr">
    <span class="sb rd|co|pr">Status</span>
    <a href="#agenti" class="dl">Vedi agente →</a>
  </div>
</div>
```

Status badges: `.rd` = green (Active), `.co` = yellow (Coming Soon), `.pr` = purple (Pro).

## Common patching patterns

### Replacing PFP images
1. Place new image in `{WEB_ROOT}/bot-profiles/`
2. Patch the `<img src="...">` in the agent card's `.tp` div
3. CSS for PFP: `.acard .tp .ic-img` — 48×48px, border-radius 12px, gold border

### Fixing buttons/links
- Disabled buttons have `style="pointer-events:none;opacity:0.6"` — remove both to enable
- `href="#"` placeholders → replace with real target (mailto, section anchor, external URL)
- "COMING SOON" pricing buttons → `mailto:hermesbro10@gmail.com?subject=PLAN_NAME%20-%20Interesse`
- [REDACTED — dati personali rimossi] wants them clickable (mailto) even if product isn't ready — NOT disabled with pointer-events:none
- **Duplicate href**: `<a href="mailto:..." href="/register">` — second `href` is silently ignored. Pick one and remove the other.
- **Deprecating features / "not ready to ship"**: When [REDACTED — dati personali rimossi] says "non siamo pronti" or "toglilo", REMOVE the button entirely — do NOT just disable it with `pointer-events:none;opacity:0.6`. Redirect the route (302 → `/`), remove ALL links to it from every page (nav, hero, footer, inline), and verify with `grep`. [REDACTED — dati personali rimossi] prefers no button over a dead/disabled button.
- **Internal links**: Always use NO trailing slash (`/warroom` not `/warroom/`) due to nginx exact match config
- **Register page**: `/register` is LIVE — serves a 3-step waitlist form (sector → agents → email). Backend renders via Jinja2 template at `{BACKEND_ROOT}/templates/register.html`. Step 3 collects email + optional business name. POSTs to `/api/waitlist` which saves to `waitlist` table in SQLite. No token/payment step.
- **Contact CTAs**: Hero CTA "Richiedi una demo" → `mailto:info@hermesbro.it?subject=Richiesta%20Demo%20HermesBots`. Nav "Inizia Ora" → `mailto:info@hermesbro.it?subject=Richiesta%20Info%20HermesBots`. Pricing buttons (Starter/Pro/Enterprise) → `mailto:info@hermesbro.it?subject=Interesse%20Piano%20NAME`. Email in contact section is clickable `<a href="mailto:...">`. Added "Scrivici a info@hermesbro.it" button above the contact form. Contact email: `info@hermesbro.it`.
- **Hero CTAs**: Primary = "Guarda la War Room" (`#warroom`), Secondary = "Unisciti alla waitlist" (`/register`). No "Attiva Ora" until ready to ship bots.
- **Waitlist API**: `POST /api/waitlist` — JSON body: `{email, sector, agents, name?}`. Saves to `waitlist` table. Returns `{status: "ok"}`.
- **Waitlist DB table**: `waitlist` (id, email, name, sector, agents, created_at). Created in `init_db()`. Index on email.
- **Contacts DB table**: `contacts` (id, name, email, company, phone, message, created_at). Created in `init_db()`. Used by `/api/contact` endpoint (contact form on landing page). Index on email.
- **DB path**: SQLite at `{BACKEND_ROOT}/data/hermesbro.db` (NOT `{BACKEND_ROOT}/hermesbro.db`). DATA_DIR = BASE_DIR / "data".
- **New landing page (not deployed)**: A dark-theme landing page exists at `{WEB_ROOT}-landing/index.html` — responsive, Lucide SVG icons, form contatto. NOT deployed per [REDACTED — dati personali rimossi]'s explicit request ("non toccare più il sito"). Keep as reference for future redesign.

### Adding a new agent
1. Add PFP to `{WEB_ROOT}/bot-profiles/pixel-NAME.png`
2. Add card HTML in `#agentGrid` with correct `data-cat` for filter
3. Add demo response in `demoResponses` JS object if applicable
4. Add agent to backend's `AGENTS` list in hermesbro_multitenant_backend.py
5. Create agent profile page at `{WEB_ROOT}/agents/{slug}.html`
6. Update "Vedi agente" link in index.html card to point to `/agents/{slug}.html`

### Agent profile pages

Individual profile pages for each agent at `{WEB_ROOT}/agents/{slug}.html`. Generated via batch Python script from agent data (SOUL.md personality, capabilities, tools). See `references/agent-profile-generator.md` for the full template and generator script.

**Structure per page:**
- Nav: HERMESBRO brand + "Tutti gli agenti" back link → `/#agenti`
- Hero: PFP pixel art (120px), status badge, name (Orbitron), tagline (mono), description
- Stats: 3 cards (tools count, personalities, capabilities)
- Personalities: 3-column grid of cards (name, role, description) — sourced from SOUL.md
- Capabilities: 2-column grid with checkmark SVG icons
- Tech stack: badge pills
- CTA: Waitlist (gold) + Contact (outline) buttons
- Footer + IT/EN lang toggle (bottom-right floating)

**Design rules:**
- Same design system as landing page (dark theme, gold accent, Orbitron/Inter/JetBrains Mono)
- CSS is inline `<style>` (single-file, no build step)
- Each agent has a unique `--cat-color` accent (e.g., ContAIbile green, LAWrenzo indigo)
- Status badges: `.rd` (active/Attivo), `.co` (coming/Prossimamente), `.pr` (pro/Pro)
- SVG icons only, NO emoji ([REDACTED — dati personali rimossi]'s rule)
- Mobile responsive: persona-grid → 1col, stats → stacked at 768px

**i18n pattern:**
- `data-it` / `data-en` attributes on text elements
- JS `setLang(l)` swaps all `[data-{l}]` textContent
- Lang toggle: bottom-right fixed position, IT/EN buttons
- Pitfall: for complex HTML content (like capability lists with SVGs), `data-en` on the `<ul>` is fragile — prefer static Italian content or use JS that rebuilds innerHTML

**nginx config:**
- `/agents/` serves static files: `location /agents/ { try_files $uri $uri/ =404; }`
- NOT proxied to FastAPI backend (was proxy before 2026-06-03, changed to static)
- Files MUST have `.html` extension — extensionless URLs return 404
- `chmod 644` required for all new files (nginx runs as www-data)

**Pitfalls:**
- Extensionless URLs: links MUST be `/agents/name.html` not `/agents/name`. nginx `try_files` doesn't auto-append `.html` unless configured with `$uri.html` fallback.
- `data-en` placeholder: batch generator may leave `data-en="placeholder"` on elements — always verify and remove/fix after generation.
- `chmod 644`: new files created by root default to 600 → nginx 403. Always `chmod 644 {WEB_ROOT}/agents/*.html` after creating pages.
- Backup index.html before updating "Vedi agente" links: `cp index.html index.html.bak`

### Disabling a bot vs removing from site — CRITICAL DISTINCTION
When [REDACTED — dati personali rimossi] says "disattivare" or "spegnere" a bot, he means **stop the running bot process and free the token** — NOT remove it from the website. These are separate operations:

**"Disable the bot" (process/token)** = what [REDACTED — dati personali rimossi] usually means:
1. Stop the bot's Hermes gateway process: `hermes stop <profile-name>`
2. Extract the Telegram bot token for reuse: check `/home/[REDACTED — dati personali rimossi]/ai-stack/<botname>-gold/.env` for `BOT_TOKEN=***`. Leave the landing page, agent cards, and all website references completely untouched. The bot profile at `~/.hermes/profiles/<name>/` stays — it's just not running.

**"Remove from site"** = only when [REDACTED — dati personali rimossi] explicitly says "togli dal sito" or "rimuovi dalla landing":
1. Comment out agent card with HTML comments
2. Remove from workflow text, pricing, tag lists
3. Update backend default agents
4. Verify with `grep`

**PITFALL**: Once removed MR.ROBOT from the landing page when [REDACTED — dati personali rimossi] said "disattivare temporaneamente" — he was furious: *"no non dalla landing scemo devi solo disattivarlo, ho bisogno del suo token per un altro bot rimettilo sul sito"*. Always clarify: process/token vs website presence.

### Temporarily hiding an agent from the LANDING PAGE only (rare)
Only do this when [REDACTED — dati personali rimossi] explicitly says "togli dal sito" or "nascondi dalla landing". Use HTML comments to hide the agent card. Do NOT delete — makes re-enabling a one-line change.
```html
<!-- AGENTNAME — TEMPORANEAMENTE DISATTIVATO
<div class="acard reveal" data-cat="tech">
  ... card content ...
</div>
-->
```
Also:
- Remove mentions from workflow text/data-it/data-en attributes in the demo section
- Remove from `<span class="a">` tags in the workflow agent list
- Remove from pricing feature lists (replace with generic text)
- In backend `hermesbro_multitenant_backend.py`: swap the agent ID in `SECTORS` default agents list with another agent (e.g., replace `mrrobot` with `groot`)
- Verify: `grep -n 'AGENTNAME' {WEB_ROOT}/index.html` — only matches should be inside `<!-- -->` comments
- Agent does NOT need to be removed from the War Room JS `agents` array (it's in the backend, separate from landing page)
- Agent does NOT need to be removed from `orchestrator.py` AGENTS dict (unused agents are harmless)
- **ALWAYS revert** if [REDACTED — dati personali rimossi] says "rimettilo" — undo all changes, don't just re-enable the card

### Replacing emojis with SVG icons
1. Identify all emoji characters in the HTML
2. Replace with appropriate Lucide SVG (see icon pattern above)
3. Wrap in `<span class="icon-wrap">` if sizing context differs
4. Verify no emoji remains: search for Unicode ranges `\u{1F300}-\u{1FAD6}`

### Register page — waitlist flow
- 3 steps: Sector selection → Agent selection → Email signup
- Step 1: Glass-morphism cards with SVG icon + radio (sector_grid)
- Step 2: Checkbox list with Machiavelli auto-toggle (agent_grid)
- Step 3: Email (required) + business name (optional) → "Iscriviti alla waitlist"
- POSTs JSON to `/api/waitlist` → saves to `waitlist` DB table
- Success: "Sei in lista!" with sector/agents summary
- Template at `{BACKEND_ROOT}/templates/register.html` (Jinja2 with `{{SECTORS}}` injection)

### Panel page — client dashboard
- 4 stat cards at top with SVG icons (total agents, active, sectors, pending)
- Search input with SVG search icon
- Agent table with status badges (active/pending/expired)
- Action buttons: Provision (rocket), Reset (refresh), Delete (trash)
- Modal confirmations instead of `alert()` calls
- Toast notifications for feedback

## Terminal-style component pattern

Used for War Room and Demo sections — gives a "live session" feel:

```html
<div class="wr-demo"> <!-- or dbox for demo -->
  <div class="wr-header"> <!-- terminal title bar -->
    <div class="dot"></div><div class="dot"></div><div class="dot"></div>
    <span>hermesbro — warroom session</span>
  </div>
  <div class="wr-body"> <!-- content area -->
    ...
  </div>
</div>
```

CSS for terminal header:
```css
.wr-header{display:flex;align-items:center;gap:8px;padding:16px 24px;background:rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.06)}
.wr-header .dot{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,0.15)}
.wr-header .dot:nth-child(1){background:#ef4444}
.wr-header .dot:nth-child(2){background:#f59e0b}
.wr-header .dot:nth-child(3){background:#10B981}
.wr-header span{font-size:12px;color:var(--muted);margin-left:8px;font-family:var(--mono)}
```

Container: `background:rgba(10,10,15,0.8); border-radius:20px; overflow:hidden; backdrop-filter:blur(10px); box-shadow:0 25px 80px rgba(0,0,0,0.4); padding:0`

## Agent response card pattern (with pixel avatars)

Used in War Room — each agent response has its pixel art avatar:

```html
<div class="ri">
  <img src="/bot-profiles/pixel-contaibile.png" alt="ContAIbile" class="ri-avatar">
  <div class="ri-content">
    <div class="ri-name"><span class="d" style="background:#10B981"></span>ContAIbile</div>
    <div class="ri-text">Response text here...</div>
  </div>
</div>
```

CSS: `.ri-avatar{width:36px;height:36px;border-radius:10px;flex-shrink:0;object-fit:cover;border:1px solid rgba(255,255,255,0.06)}`

## Status bar with pulse animation

Shows active agents working — adds dynamism to static demos:

```html
<div class="wr-status">
  <div class="pulse"></div>
  <span>6 agenti stanno lavorando…</span>
</div>
```

```css
.wr-status{display:flex;align-items:center;gap:8px;padding:10px 16px;background:rgba(34,211,238,0.04);border:1px solid rgba(34,211,238,0.1);border-radius:10px;font-size:12px;color:#22d3ee;font-family:var(--mono)}
.wr-status .pulse{width:6px;height:6px;border-radius:50%;background:#22d3ee;animation:wrPulse 1.5s ease infinite}
@keyframes wrPulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.4;transform:scale(0.8)}}
```

## Orchestrator dashboard pattern (hero section)

The hero visual is a dashboard mockup showing the Request → Agents → Output flow:

```html
<div class="dash">
  <div class="d-topbar">  <!-- terminal-style header -->
    <div class="dot"></div><div class="dot"></div><div class="dot"></div>
    <div class="d-title">HERMESBRO | ORCHESTRATOR</div>
    <div class="d-status">Operativo</div>
  </div>
  <div class="d-body">
    <div class="flow">  <!-- horizontal flow: request → agents → output -->
      <div class="ui">  <!-- request section -->
        <div class="l">Richiesta</div>
        <div class="t">"Devo lanciare un nuovo piatto"</div>
      </div>
      <div class="arrow"><svg>→</svg></div>
      <div class="ag">  <!-- agents section -->
        <div class="l">Agenti attivi</div>
        <div class="ag-row">
          <div class="c ok"><img src="/bot-profiles/pixel-NAME.png"><span class="d" style="background:#COLOR"></span>AgentName</div>
        </div>
      </div>
      <div class="arrow2"><svg>→</svg></div>
      <div class="out">  <!-- output section -->
        <div class="l">Output</div>
        <div class="items"><span>Deliverable 1</span></div>
      </div>
    </div>
  </div>
</div>
```

CSS: `.dash` is padding:0 with overflow:hidden. `.d-topbar` has 3 colored dots (red/amber/green) + title (mono, gold) + status (green with pulse). `.flow` is flex with `gap:0` — sections touch each other (no gaps). Arrows are 40px wide with gold/green SVG chevrons. Agent cards have pixel avatars via `<img>` (22x22px, border-radius 6px). Responsive: flow goes vertical at 900px, arrows rotate 90deg.

## Scenario shortcut pattern (demo section)

Quick-fill buttons that auto-select the right agent and prefill the textarea. Great UX for showing what each agent can do:

```html
<div class="dsc" id="demoScenarios">
  <button data-scenario="fatture">Analisi fatture</button>
  <button data-scenario="contratto">Revisione contratto</button>
</div>
```

JS:
```js
// Scenario shortcuts auto-select agent and prefill textarea
// The button click triggers the same flow as manual input + agent selection
const demoScenarios = {
  fatture: { text: 'Analizza le mie ultime fatture...', agent: 'contaibile' },
  contratto: { text: 'Rivedi questo contratto...', agent: 'lawrenzo' },
  social: { text: 'Crea un piano social...', agent: 'wannabe' },
  menu: { text: 'Ottimizza il mio menu...', agent: 'groot' },
};
document.querySelectorAll('#demoScenarios button').forEach(btn => {
  btn.addEventListener('click', function() {
    const s = demoScenarios[this.dataset.scenario];
    document.getElementById('demoInput').value = s.text;
    document.querySelectorAll('#demoSelect button').forEach(b => b.classList.remove('sel'));
    document.querySelector(`#demoSelect button[data-agent="${s.agent}"]`)?.classList.add('sel');
  });
});
```

## Pitfalls

- **Bulk email replacement across site**: When changing the contact email across all HTML files, use: `find {WEB_ROOT} -name '*.html' -not -name '*.bak' -exec sed -i 's|old@email|new@email|g' {} +`. Verify with `grep -r 'old@email' {WEB_ROOT}/`. Don't forget the backend file at `{BACKEND_ROOT}/hermesbro_multitenant_backend.py` if it also references the email. Update the skill's Contact CTAs section after any email change. (Pattern validated 2026-06-03: changed from contact@example.com to hermesbro10@gmail.com across 13+ files.)
- **CRITICAL — CSS class name must match HTML**: Multiple mismatches found and fixed (2026-06-03): `.wr-demo` vs `warroom-demo`, `.ag-filter` vs `agents-filter`, `.dash .top` vs `.d-topbar`. Result: zero styles applied to affected sections. **Systematic verification**: extract all CSS class selectors from `<style>` block, extract all HTML `class="..."` attributes, diff them. Or use this one-liner:
  ```python
  import re; css=set(re.findall(r'\.([a-zA-Z][a-zA-Z0-9_-]*)', style_block)); html=set(c for m in re.findall(r'class="([^"]*)"', html) for c in m.split()); print(css - html)  # orphan CSS classes
  ```
  Common pattern: CSS uses short names (`.wr-demo`, `.ag-filter`) but HTML uses longer descriptive names (`warroom-demo`, `agents-filter`). When editing any section's CSS, always verify the selector matches the actual HTML class. **After any redesign**: re-verify all selectors — class names often change during HTML restructuring.
- **Always backup before editing**: `cp index.html index.html.bak` (or timestamped)
- **No table syntax in Telegram** — when reporting changes to [REDACTED — dati personali rimossi], use bullet lists
- **[REDACTED — dati personali rimossi]'s preference**: show concrete changes, not explanations. "Fatto ✅" + bullet list of what changed.
- **[REDACTED — dati personali rimossi] wants to review BEFORE deploy**: When creating new pages or major changes, show screenshots/mockups for approval BEFORE pushing live. For static files: write to a temp location or deploy silently, take screenshots, show to [REDACTED — dati personali rimossi], get approval, THEN update index.html links / make visible. "Prima creale, fammele vedere prima del deploy" (2026-06-03). Exception: minor patches/fixes don't need preview.
- **"Vedi agente →" links**: Point to individual agent profile pages at `/agents/{name}.html` (e.g., `/agents/contaibile.html`). MUST include `.html` extension — nginx does not handle extensionless URLs by default. See "Agent profile pages" section below.
- **Image sizes**: pixel-machiavelli.png and pixel-sentinel.png are ~1000px (larger than others at 256px). CSS handles this with `object-fit:cover` and fixed dimensions.
- **Duplicate `href` attributes**: HTML allows only one `href` per element. If you see `<a href="mailto:..." href="/register">`, the SECOND `href` is silently ignored by browsers (they use the first). Always verify there's only one `href` attribute. Common pattern: mailto + page link on same CTA button — pick one.
- **`curl -sI` vs FastAPI**: `curl -sI` sends a HEAD request. FastAPI/uvicorn returns 405 for HEAD on many routes. Always use `curl -s -o /dev/null -w "%{http_code}" URL` or `curl -s URL | head` for verification, NOT `curl -sI`.
- **CRITICAL — systemd `EnvironmentFile` position**: When adding `EnvironmentFile=` to a systemd service file, it MUST be inside the `[Service]` section, NOT at the end of the file. Using `echo 'EnvironmentFile=...' | sudo tee -a service_file` appends AFTER the `[Install]` section, which puts the directive in `[Install]` → systemd ignores it with `"Unknown key name 'EnvironmentFile' in section 'Install', ignoring"`. **Fix**: insert BEFORE `[Install]` line: `sudo sed -i '/^\[Install\]/i EnvironmentFile=/path/to/.env' /etc/systemd/system/service.service`. Always verify with `cat` after editing and check `systemctl status` for warnings.
- **Backend port**: The FastAPI backend runs on port 8333 (uvicorn), NOT 5000 (old Flask). nginx proxies dynamic routes there.
- **SSE endpoints through nginx**: Any Server-Sent Events endpoint (like `/api/warroom`) MUST have a dedicated nginx location block with `proxy_buffering off; proxy_cache off; chunked_transfer_encoding off; proxy_read_timeout 600s;`. Without these, nginx buffers the SSE stream and the client never receives events until the connection closes. Always place the SSE location BEFORE the generic `/api/` prefix match in nginx config (nginx uses first-match for prefix locations).
- **NEVER use emoji characters for icons** — [REDACTED — dati personali rimossi] hates them. Always use inline SVG.
- **Backend must be running** for register.html, panel.html, and the `/api/warroom` SSE endpoint to work. The standalone War Room at `/warroom` requires `warroom.service` (port 8097) instead.
- **New DB tables after init**: If you add a `CREATE TABLE` to `init_db()` but the DB already exists, the table WON'T be created — `init_db()` only runs on first startup. You must create it manually: `python3 -c "import sqlite3; conn = sqlite3.connect('{BACKEND_ROOT}/data/hermesbro.db'); conn.executescript('CREATE TABLE IF NOT EXISTS ...'); conn.commit(); conn.close()"`. Always verify the table exists after adding one.
- **`execute_code` + `read_file` key name**: When using `read_file()` inside `execute_code` scripts, the returned dict uses key `content_returned`, NOT `content`. Using `result["content"]` raises `KeyError`. For large file rewrites (like replacing inline HTML in the backend), prefer `terminal("python3 << 'PYEOF' ...")` over `write_file` — gives full control over encoding and avoids silent issues with triple-quoted strings containing backslashes.
- **After editing templates or backend**: `systemctl restart hermesbro-multitenant.service` (preferred). Manual fallback: `fuser -k 8333/tcp 2>/dev/null; sleep 1` then `cd {BACKEND_ROOT} && python3 -m uvicorn hermesbro_multitenant_backend:app --host 127.0.0.1 --port 8333`. The `sleep 1` is critical. **PITFALL**: `hermesbro-multitenant.service` is a systemd service that auto-restarts. If you start uvicorn manually while the service is running, both fight for port 8333. Always use `systemctl restart` or kill the service first with `systemctl stop hermesbro-multitenant.service`.
- **PITFALL — Nested WebSocket paths in nginx**: `location /ws/` only matches paths starting with `/ws/`. If a frontend connects to a NESTED WebSocket path like `/warroom/ws/{id}`, it will NOT match `location /ws/` — the connection silently fails. You need a dedicated `location /warroom/ws/` block with `rewrite ^/warroom/(.*) /$1 break;` BEFORE the generic `/ws/` block. See `references/warroom-standalone.md` for the full nginx config with both blocks. Symptom: WebSocket status stuck on "reconnecting...", button click does nothing, no JS errors.

**PITFALL — War Room setup panel hidden on page load**: The `init()` function in `warroom.html` must call `showSetupPanel()` at the end. Without it, the setup panel (topic input, agent selection, start button) stays `display: none` — the user sees the War Room page but cannot start a brainstorming. The `startBtn` exists in DOM but has zero dimensions. Symptom: "il tasto per far partire il brainstorming non funziona" — actually the entire panel is invisible. Fix: add `showSetupPanel();` to `init()`, restart `warroom.service`. See `references/warroom-standalone.md` for full details.
- **PITFALL — SyntaxError in backend causes cascading 502 on ALL dynamic routes**: Any Python syntax error in `hermesbro_multitenant_backend.py` crashes the entire uvicorn process (it can't even import the module). The symptom is **502 on every dynamic route** (`/register`, `/panel`, `/api/*`) while static pages (`/`, `/agents/`) continue working fine. Diagnosis pattern (validated 2026-06-05, line 289: bare identifiers `[sudo, chown, -R, ...]` instead of `["sudo", "chown", "-R", ...]` in subprocess.run):
  1. `curl -s -o /dev/null -w "%{http_code}" https://hermesbro.cloud/register` → 502
  2. `systemctl status hermesbro-multitenant.service` → `activating (auto-restart)` + `exit-code`
  3. `journalctl -u hermesbro-multitenant.service --no-pager -n 30` → find the `SyntaxError` / `ImportError` / actual Python traceback
  4. Fix the code, `systemctl restart`, verify 200
  The key insight: uvicorn loads the module ONCE at startup. A single syntax/import error in ANY part of the file kills the entire server — not just the broken route. Always check `systemctl status` first when seeing 502 on dynamic routes.
- **After editing static files** (in `{WEB_ROOT}/`): changes are live immediately (nginx serves directly), BUT you must `chmod 644` any new file — root's default umask creates 600, and nginx runs as www-data which can't read those. Always verify: `curl -s -o /dev/null -w "%{http_code}" URL` after creating any static file.
- **Google Search Console verification** uses HTML file upload method (not meta tag, not DNS). Upload the `googleXXXX.html` file to `{WEB_ROOT}/`, `chmod 644`, verify it's served, then click "Verifica" in GSC. This was used for both foodcostitalia and hermesbro.cloud.
- **CRITICAL — `\\n` in Python triple-quoted strings becomes a real newline**: When embedding JavaScript inside a Python `\"\"\"...\"\"\"` string (e.g., the warroom inline HTML), writing `\\n` in the Python source produces an ACTUAL newline character in the HTML output — not the literal two characters `\\n`. This breaks JS strings like `text:'line1\\nline2'` — the browser receives an unescaped real newline inside a single-quoted JS string, causing `Uncaught SyntaxError: Invalid or unexpected token`. **Fix**: use `\\\\n` in the Python source to produce literal `\\n` in the HTML output. Example: `\"text:'line1\\\\nline2'\"` in Python → `text:'line1\\nline2'` in HTML. This applies to ALL JS escape sequences (`\\n`, `\\t`, `\\\"`, etc.) — always double the backslash in Python triple-quoted strings. **Detection**: if the browser shows blank/empty page content but the HTML source is non-empty, check for broken JS — often caused by this issue. Verify with `browser_console()` for SyntaxError. **Hex verification**: when `repr()` output is ambiguous (4+ backslashes), read the file as raw bytes and check hex values: `0x5c` = backslash, `0x5c 0x5c` = two backslashes (→ `\\` in Python → `\` in output). Example: `python3 -c \"f=open(path,'rb'); c=f.read(); i=c.find(b\\\"split('\\\"); print([hex(b) for b in c[i:i+20]])\"`. **SSE parsing in browser**: The JS `buffer.split('\\n')` in the browser must split on actual newline characters (`\n` = 0x0a), NOT on literal backslash-n. If the Python source has `\\\\n` (2 backslashes), the HTML gets `\\n` (1 backslash + n), and JS `'\n'` = actual newline. If the Python source has `\\\\\\\\n` (4 backslashes), the HTML gets `\\\\n` (2 backslashes + n), and JS `'\\n'` = literal backslash-n — SSE parsing BREAKS silently (events never match). Always verify with hex check.
- **CRITICAL — JS apostrophes in Python triple-quoted strings**: When embedding JavaScript inside a Python `"""..."""` string (e.g., the warroom inline HTML), Italian text with apostrophes (`dell'affitto`, `l'analisi`, `dell'agenzia`) WILL BREAK. Python interprets `\'` inside `"""..."""` as just `'`, so the browser receives an unescaped `'` inside a JS single-quoted string like `t:'dell'affitto'`, which terminates the string early. **Fix**: avoid apostrophes in JS string literals entirely — rephrase Italian text (`dell affitto`, `analisi`, `agenzia`), or use backtick template literals instead of single quotes for JS strings. Never try to double-escape (`\\\\'`) — it's fragile and produces `\\'` in HTML which also breaks JS.
- **CRITICAL — Nested f-strings with escaped quotes in Python triple-quoted strings**: When writing Python code that generates JSON/YAML inside a `"""..."""` string (e.g., SSE event yields in the warroom API), nested f-strings with `\\\"` cause `SyntaxError: unexpected character after line continuation character`. **Fix**: build the dict/data first as a variable, then use string concatenation: `yield "data: " + json.dumps({"key": var}) + "\n\n"` instead of `yield f"data: {json.dumps({'key': var})}\n\n"`. This avoids all escaping issues.
- **Missing `import sys`**: When adding new API endpoints that use `sys.path.insert()` (e.g., to import `orchestrator`), verify `import sys` is at the top of the file. The backend imports `json, os, sqlite3, uuid, subprocess, re` but NOT `sys` by default. Add it before writing code that references `sys`.
- **Missing FastAPI imports**: The backend imports `FastAPI, HTTPException, Request, Query, Form` from fastapi. If you need `Body` (for JSON request bodies without Pydantic models), add it to the import: `from fastapi import ..., Body`. For `BaseModel` + `EmailStr`, they're imported from pydantic. Always check existing imports before adding a new endpoint.
- **Orchestrator AGENTS dict**: The `orchestrator.py` `AGENTS` dict must include ALL agents used by the War Room. If adding a new agent to the frontend selection grid, also add it to `AGENTS` in `orchestrator.py` with `"profile"` matching the Hermes profile name. Machiavelli must be present for synthesis to work.
- **nginx config**: `/api/*` routes and dynamic pages go through proxy; static assets bypass it
- **Stagger animations**: use `animation-delay: calc(var(--i, 0) * 100ms)` on child elements, set `--i` via nth-child or JS. For War Room cards: use explicit nth-child delays (0.3s, 0.5s, 0.7s...) with `opacity:0;transform:translateY(12px)` as initial state and `animation:wrCardIn .5s ease forwards` to animate in.
- **Responsive War Room**: at 900px, `.wr-demo .resp` goes to `grid-template-columns:1fr` and reduce card padding to 12px.

### Multitenant provisioning
See `references/multitenant-provisioning.md` for the full provisioning architecture, gaps, sector-agent mapping, and API endpoints.

**PITFALL — Business context first**: When working on the multitenant backend, ALWAYS study the business plan at `/root/hermes-bots-business-plan.md` and the monetization plan at `<HERMES_ROOT>/plans/monetizzazione-hermesbro.md` BEFORE proposing technical changes. [REDACTED — dati personali rimossi] corrected this twice: the multitenant backend IS the HermesBro product (SaaS for Italian SMEs at €29-199/month), not a standalone tech project. Any feature proposal must connect to the business model. "no ma questo mica to con tutto quello che abbiamo?" = you're analyzing in isolation, connect to the existing architecture and plan.

### Bot token management
See `references/bot-token-locations.md` for all bot token file paths. When [REDACTED — dati personali rimossi] asks for a token or wants to "disable" (= free the token), consult that file.

### War Room implementation details
- **Standalone service (primary)**: See `references/warroom-standalone.md` — WebSocket, moderator, workflow templates, port 8097
- **Legacy multitenant API**: See `references/warroom-interactive.md` — SSE chain discussion, port 8333

### Agent profile pages generator
See `references/agent-profile-generator.md` for the template, data structure, and batch generation script for individual agent profile pages at `/agents/{slug}.html`.

### Static site
- Files served directly by nginx from `{WEB_ROOT}/`
- No build/deploy pipeline — edit files in place, changes are live immediately
- After editing: verify with `curl -sI https://hermesbro.cloud/` and browser check
- For data listing pages (skills, catalogs): see `references/static-data-pages.md` — embedded JSON + client-side search/filter pattern
- For skills.html specifically: see `references/skills-page.md` — data structure, regeneration, navbar conventions

### Backend
- FastAPI app at `{BACKEND_ROOT}/hermesbro_multitenant_backend.py`
- Runs on port 8333 (uvicorn), bound to 127.0.0.1
- nginx proxies `/register`, `/panel`, `/warroom`, `/api/*` to it
- DB: `{BACKEND_ROOT}/data/hermesbro.db` (SQLite)
- Templates: `{BACKEND_ROOT}/templates/`
- Restart: kill+rerun (see Pitfalls)

### Verification checklist
- [ ] `curl -s -o /dev/null -w "%{http_code}" https://hermesbro.cloud/` → 200
- [ ] `curl -s -o /dev/null -w "%{http_code}" https://hermesbro.cloud/register` → 200 (waitlist page)
- [ ] `curl -s -o /dev/null -w "%{http_code}" https://hermesbro.cloud/panel` → 200
- [ ] `curl -s -o /dev/null -w "%{http_code}" https://hermesbro.cloud/warroom` → 200 (standalone service on port 8097)
- [ ] `curl -s -o /dev/null -w "%{http_code}" https://hermesbro.cloud/warroom.html` → 200 (check permissions: `chmod 644`)
- [ ] `systemctl is-active warroom.service` → active (standalone War Room)
- [ ] `curl -s -X POST https://hermesbro.cloud/api/warroom -H "Content-Type: application/json" -d '{"query":"test","agents":["contaibile"]}' -w "%{http_code}"` → 400 (needs 2+ agents)
- [ ] `curl -s -X POST https://hermesbro.cloud/api/demo -H "Content-Type: application/json" -d '{"query":"test","agent":"contaibile"}' -w "%{http_code}"` → 200 (SSE stream)
- [ ] `curl -s -X POST https://hermesbro.cloud/api/waitlist -H "Content-Type: application/json" -d '{"email":"test@test.com","sector":"tech","agents":"auto"}' -w "%{http_code}"` → 200
- [ ] No emoji characters in any HTML file
- [ ] All SVG icons use `stroke="currentColor"`
- [ ] Animations work (check stagger delays)
- [ ] Mobile responsive (test at 375px width)
- [ ] No duplicate `href` attributes on any `<a>` element
- [ ] All internal links use NO trailing slash (nginx exact match)
