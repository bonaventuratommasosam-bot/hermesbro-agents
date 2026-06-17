---
name: marketing-materials-workflow
description: >
  Create complete marketing suite for Hermes Bots: landing page, pitch deck, 
  outreach templates, brand identity, content calendar. Trigger when [REDACTED — dati personali rimossi] 
  asks for marketing materials or client acquisition assets.
version: 1.0.0
author: gribbito
tags: [marketing, outreach, landing-page, pitch-deck, hermes-bots]
triggers:
  - "marketing materials"
  - "landing page"
  - "pitch deck"
  - "outreach"
  - "client acquisition"
  - "brand identity"
  - "marketing del prodotto"
  - "brainstorming marketing"
---

# Marketing Materials Creation Workflow

## Overview

Complete workflow for creating HermesBro marketing assets. All materials go to `<HERMES_ROOT>/shared/marketing/`.

## Prerequisites

- **FIRST**: Read the live site — `curl -sL https://hermesbro.cloud` — this is the SINGLE SOURCE OF TRUTH for tagline, agent count, features, CTAs, and pricing. Do NOT write content from memory.
- Check existing materials first: `ls <HERMES_ROOT>/shared/marketing/`
- Brand identity: dark ink + gold, Inter + JetBrains Mono, minimal
- Target: Italian PMI (ristoratori, commercialisti, avvocati)
- Budget: €50/mese (organico, no ads)
- Style: Fisher + Groucho + JARVIS (direct, minimal, no decorative emoji)
- **DECENTRALIZATION IS CORE MESSAGING** — [REDACTED — dati personali rimossi] explicitly said "dobbiamo spingere sul fatto che sia tutto decentralizzato e che non ce condivisione dei dati ricordatelo sempre". Every pitch deck, landing page, outreach template, and LinkedIn post MUST reinforce: decentralizzato, zero data sharing, dati non escono dal VPS, no cloud terze parti, Zero Trust, GDPR by design. This is NOT optional — it's the #1 differentiator.

## GribbitO Execution Capabilities (VALIDATED 2026-06-05)

**GribbitO CAN execute these marketing actions autonomously — never claim otherwise:**
- ✅ **LinkedIn publishing**: `python3 <HERMES_ROOT>/shared/linkedin/linkedin.py post-file <file>` — works with valid token. Check token first: `python3 linkedin.py me`
- ✅ **LinkedIn text posts**: `post`, `post-file`, `post-image`, `post-file-image` — all functional
- ✅ **Micro-site articles**: Publish to `/var/www/foodcostitalia/` (nginx serves them live). Write HTML, copy to nginx root.
- ✅ **Telegram group research**: Find groups via web search, verify with `urllib.request` to `t.me/<slug>`, curate list
- ✅ **Content creation**: All writing tasks (posts, articles, templates, calendars, outreach docs)
- ✅ **gbrain import**: `gbrain import <HERMES_ROOT>/shared/marketing/ --no-embed && gbrain embed --stale`

**GribbitO must NOT offer or attempt:**
- ❌ **Deploying code** — [REDACTED — dati personali rimossi]: "non devi deployare niente il coding non lo gestisci tu". No `systemctl`, no bot deployment, no service restarts for new code
- ❌ **Writing application code** — demo bots, scripts, backend changes → [REDACTED — dati personali rimossi] does this on Hermes PC
- ❌ **Suggesting deployment as next step** — when producing marketing assets, the deliverable IS the content. Don't wrap up with "vuoi che deployi X?"

**Pitfall**: When [REDACTED — dati personali rimossi] says "fai tutto" for marketing, DO NOT respond with "cosa posso fare e cosa no." Execute everything you CAN (LinkedIn, articles, content, research) and tell [REDACTED — dati personali rimossi] what HE needs to do (join Telegram groups, configure org URN, deploy demo bot). [REDACTED — dati personali rimossi] explicitly corrected this: "acceso a linkedin lo hai visto che pubblichi per me tutti i giorni."

## Autonomous Execution Pattern

When [REDACTED — dati personali rimossi] says **"Fai tutto quello che puoi fare in autonomia"** or similar (do everything you can autonomously):

1. **Create TODO list** with all actionable tasks
2. **Parallelize writing tasks** via `delegate_task` with batch mode (up to 3 subagents). Group logically:
   - Subagent A: Outreach/tracking/templates (structured docs)
   - Subagent B: Content writing (posts, calendars, articles)
   - Subagent C: Research + code (group research, bot scripts)
3. **Do research tasks yourself** (web search, file reading) while subagents write
4. **Import to gbrain** after completion: `gbrain import <HERMES_ROOT>/shared/marketing/ --no-embed && gbrain embed --stale`
5. **Log fact** via `fact-log.py` for fleet-wide awareness
6. **Report**: deliver a concise summary of what was produced, file paths, and next steps [REDACTED — dati personali rimossi] needs to decide on

**Pitfall**: Don't ask [REDACTED — dati personali rimossi] which tasks to prioritize when he says "do everything." Execute ALL of them. The only acceptable question is which to deploy/activate first AFTER everything is built.

**Pitfall**: `gbrain import` (NOT `ingest`) is the correct command. Use `--no-embed` first, then `embed --stale` separately — it's faster than importing with live embedding.

## Workflow Steps

### 1. Brand Identity (if not exists)

Create `<HERMES_ROOT>/shared/marketing/brand/brand-identity.md`:
- Company palette: primary dark (#1a1a2e), accent (#e94560), secondary (#16213e)
- Bot colors: ContAIbile blue, LAWrenzo purple, GROOT green, Wannabe orange, DesignBro pink, El Froggo gold, Machiavelli orange (#F97316), Sentinel red (#EF4444)
- Fonts: Space Grotesk (headings), Inter (body), Lora (quotes/accents)
- Tono di voice: diretto, professionale, leggermente witty, italiano
- 10 template social in `brand/social-templates.md`
- Content calendar 30 giorni in `brand/content-calendar.md`

### 2. Landing Page

Create `<HERMES_ROOT>/shared/marketing/landing/index.html`:
- Dark theme, responsive, Space Mono or Inter
- Sections: hero, bot lineup (10 bots), come funziona, pricing, CTA
- Pricing: A partire da €49/mese (ONLY verified price — do NOT invent tiers)
- 14 giorni gratis, zero carta di credito
- ROI calculator inline
- Form contatto (mailto o Telegram link)

**Pitfall**: [REDACTED — dati personali rimossi] rejects layouts that look too similar to references. Create ORIGINAL design, not copies.

**Pitfall — "fix data, keep graphics"**: When [REDACTED — dati personali rimossi] sends an existing PDF/HTML and says "sistema i dati" or "lascia la grafica come", he wants the SAME visual design with corrected content (bot names, email, pricing, missing bots). Do NOT rebuild the design from scratch. Extract the existing style, fix only the data, regenerate. Rebuilding from scratch when [REDACTED — dati personali rimossi] asked for a fix wastes time and produces a deck he didn't ask for.

### 3. Pitch Deck

Create as HTML with embedded base64 images, then convert to PDF:

**Source**: `/root/hermesbro-pitch-deck.html` (standalone, self-contained)
**PDF**: `/root/hermesbro-pitch-deck.pdf` (generated via wkhtmltopdf)

**Design system — ALWAYS from live site (hermesbro.cloud)**:
Before building ANY pitch deck, run: `curl -sL https://hermesbro.cloud` and extract:
- Colors: `--ink: #0a0a0f`, `--gold: #d4a853`, `--muted: #71717a`
- Fonts: Inter (body 300-900) + JetBrains Mono (labels/tags)
- Logo: SVG line-art mark (gold strokes, NOT PNG) — extract from HTML
- PFP CSS: 48×48, border-radius 12px, border 1px solid rgba(255,255,255,0.1)
- Mesh gradient: radial-gradient with subtle blue + gold tints
See `references/hermesbro-design-system.md` for full extracted CSS.

**Slide structure (11 slides)**:
1. Cover — SVG logo + brand name + tagline + URL
2. Problema — 4 card grid with pain points
3. Soluzione — stat blocks (12 agents, 14 services, 24/7, €50 budget)
4. Flotta 1/2 — 8 bot cards with pixel art pfps (core bots)
5. Flotta 2/2 — 4 specialist bot cards + ecosystem description
6. Architettura — stack tecnico + comunicazione (2-column)
7. Traction — stats + live services list
8. Business model — 3-tier pricing cards (Starter/Pro/Enterprise)
9. Monetizzazione — 80/20 hybrid model with allocation bar
10. Roadmap — timeline with done/active/pending dots
11. CTA — contact info + closing statement
12. **Investor Metrics** (optional, for investor-facing decks) — mix of unit economics AND tech moat, NOT just financials. Include:
    - **Tech Moat**: Decentralizzazione, zero cloud, zero condivisione dati, no API esterne, no telemetria, GDPR by design
    - **Unit Economics**: Costi infrastruttura, margine per cliente, LTV, CAC, breakeven
    - **Market**: TAM/SAM/SOM per PMI italiane
    - **Competitive Advantage**: Why cloud tools can't replicate this (data sovereignty, isolation)
    Pitfall: [REDACTED — dati personali rimossi] explicitly said "gli investitori vogliono vedere unit economics E tech moat, non solo numeri". Both dimensions are required.

**PFP embedding pattern (download from LIVE SITE, not local files)**:
```python
import base64, urllib.request

bots = [
    ("contaibile", "pixel-contaibile.png"),
    ("lawrenzo", "pixel-lawrenzo.png"),
    # ... etc
]
b64 = {}
for name, filename in bots:
    url = f"https://hermesbro.cloud/bot-profiles/{filename}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req).read()
    b64[name] = f"data:image/png;base64,{base64.b64encode(data).decode()}"
```
This ensures pfps match the live site exactly. Local copies may be stale or have different filenames.
**Pitfall**: Always download from `hermesbro.cloud/bot-profiles/` — NOT from local `{WEB_ROOT}/bot-profiles/` or `<HERMES_ROOT>/shared/marketing/bot-profiles/`. [REDACTED — dati personali rimossi] corrected this 3 times.

**PDF conversion**:
```bash
wkhtmltopdf --orientation Landscape --page-size A4 --no-stop-slow-scripts \
  --enable-local-file-access --margin-top 0 --margin-bottom 0 \
  --margin-left 0 --margin-right 0 \
  /root/hermesbro-pitch-deck.html /root/hermesbro-pitch-deck.pdf
```

**Pitfall — Google Fonts**: wkhtmltopdf with unpatched Qt may not load Google Fonts via `@import`. Always include fallback fonts in CSS (`font-family: 'Space Mono', monospace, 'Courier New', Courier;`). If fonts look wrong in PDF, the fallback still renders clean.

**Pitfall — Layout overflow / content spilling**: Each slide MUST fit within 297mm×210mm. Common causes of overflow:
- Pricing cards (3-tier with bullet lists) — reduce padding, use smaller font, or split across 2 slides
- Bot grid (6+ cards in one slide) — use smaller card sizes or split into Flotta 1/2
- Long bullet lists — cut to 5-6 items max per slide
**Test after building**: Open PDF and verify EVERY slide has no content cut off at the bottom or right edge. If any slide overflows, reduce content density or split the slide. [REDACTED — dati personali rimossi] rejected decks where pricing page content was cut off.

**Pitfall — Content density**: Resist the urge to put everything on one slide. [REDACTED — dati personali rimossi] prefers clean, readable slides over packed ones. When in doubt, split into two slides rather than cramming.

**Pitfall — slide dimensions**: Each `.slide` must be `width: 297mm; height: 210mm;` (A4 landscape) with `page-break-after: always`. Without explicit dimensions, wkhtmltopdf collapses slides.

**Pitfall — bot inventory inconsistency**: The site shows 10 customer-facing bots (ContAIbile, LAWrenzo, Wannabe, DesignBro, DUCATO, El Froggo, GROOT, Machiavelli, Sentinel, MR ROBOT). The investor/internal deck may include GribbitO (orchestrator) and Frank/Ratatouille for a total of 12. ALWAYS check the live site HTML for the customer-facing lineup before building materials. When in doubt, `curl -sL https://hermesbro.cloud | grep 'product-card'` to get the actual list.

**Pitfall — ALWAYS verify against live site before writing content**: The website (hermesbro.cloud) is the SINGLE SOURCE OF TRUTH. Before writing ANY LinkedIn posts or marketing copy, fetch the live site and extract: (1) exact tagline, (2) number and names of agents, (3) feature names (War Room, workflows), (4) CTA language (waitlist vs trial), (5) pricing. Session 2026-06-05: wrote 35 posts saying "6 bot" and "wingman" when the site says "10 agenti" and "team AI operativo". [REDACTED — dati personali rimossi] had to correct: "tieni questo come linea guida per i post linkedin" pointing to hermesbro.cloud. ALWAYS `curl -sL https://hermesbro.cloud` and read the actual content before writing. Do NOT rely on memory or previous post templates.

**Pitfall — "fai come sul sito" means COPY the site's design**: When [REDACTED — dati personali rimossi] says this, he wants the EXACT same visual language — same logo SVG, same gold accent, same pfp styling, same font stack, same card CSS. Do NOT interpret it as "use the same general vibe." Copy the actual CSS properties.

### 4. Outreach Templates

Create `<HERMES_ROOT>/shared/marketing/outreach/`:
- `campaign-tracker.csv` — CSV with columns: date, channel, contact_name, company, sector, status, message_sent, notes
- `partnership-commercialisti.md` — 3 variants: LinkedIn connection request (<300 chars), DM after accept, email formale. Pitch: ContAIbile + 15% referral fee + trial 30gg
- `telegram-dm.md` — DM breve per Telegram
- `linkedin-dm.md` — DM medio per LinkedIn
- `email-formale.md` — Email formale
- `follow-up.md` — Follow-up dopo 5 giorni
- `commercialisti.md` — Template specifico per commercialisti
- `coworking.md` — Template per coworking/spazi lavoro

**Template structure**:
1. Breve presentazione (chi sei)
2. Problema specifico del settore
3. Soluzione (il bot cosa fa)
4. CTA: prova gratuita 30 giorni
5. Contatto (Telegram @<USER>)

**Outreach automation script (validated 2026-06-05):**
Script at `<HERMES_ROOT>/shared/linkedin/outreach.py` manages the full outreach lifecycle:
- `outreach.py status` — campaign stats (total targets, contacted today, per-status breakdown)
- `outreach.py batch [N]` — show next N targets with auto-generated messages per sector
- `outreach.py add <csv>` — import targets from CSV (columns: name, company, sector, linkedin_url)
- Templates per sector (ristorante, studio, negozio, ecommerce, generico) — connection request + DM auto-selected
- Daily limit: 20 connection requests (LinkedIn safe limit)
- Target CSV: `<HERMES_ROOT>/shared/marketing/outreach/targets.csv`
- Tracker CSV: `<HERMES_ROOT>/shared/marketing/outreach/campaign-tracker.csv`
- See `references/outreach-automation.md` for full details

**Email drip sequences (created 2026-06-05):**
- Lead nurturing: `<HERMES_ROOT>/shared/marketing/email/drip-sequence.md` — 5 emails (Day 0, 2, 5, 8, 12)
- Commercialisti partnership: `<HERMES_ROOT>/shared/marketing/email/outreach-commercialisti-sequence.md` — 3 emails
- KPI metrics included in each sequence

### 5. Content Calendar

**Deprecated**: The old 30-day generic calendar is replaced by the Monthly Content Calendar workflow (see "Content Calendar — Monthly Workflow" above).

[REDACTED — dati personali rimossi] now writes detailed monthly calendars with specific post types, visual requirements, and asset lists. The canonical calendar lives at `<HERMES_ROOT>/shared/marketing/brand/linkedin-program-completo-<month>-<year>.md`.

Pattern: [REDACTED — dati personali rimossi] provides/approves → save to shared/marketing/brand/ → update WannabeBot cron → auto-publish Lun/Mer/Ven at 10:00.

**July 2026 program**: Full program at `<HERMES_ROOT>/shared/marketing/brand/linkedin-program-completo-luglio-2026.md` — 14 posts, 3/week (Lun=Engagement, Mer=Showcase, Ven=Educational), complete copy + visual briefs for DesignBro.

**July 2026 HIGH-FREQUENCY program**: 3 posts/day (93 total) at `<HERMES_ROOT>/shared/marketing/brand/linkedin-calendario-luglio-2026-3xday.md` (62KB, 2067 lines). Structure:
- 🌅 09:00 — Educational / Thought Leadership
- ☀️ 12:00 — Showcase / Prodotto
- 🌙 18:00 — Engagement / Community
- Weekly themes: Launch (1-7), Problem awareness (8-14), Solution showcase (15-21), Case studies (22-28), Vision/future (29-31)
- All 10 bots represented: ContAIbile, LAWrenzo, GROOT, Wannabe, DesignBro, Ratatouille, El Froggo, DUCATO, Machiavelli, Sentinel
- Ribbit Capital themes integrated (Token Revolution, Trust Flywheel)
- KPI: +500 followers, 50K impressions, 15-25 leads

**Ribbit-style content (June 2026)**: [REDACTED — dati personali rimossi] adopted Ribbit Capital's "Token Letter" style for LinkedIn. Series-based content with bold openings, data-driven claims, and visionary framing. See `references/ribbit-style-content-framework.md` for full framework. The original PDF is saved as text at `<HERMES_ROOT>/shared/marketing/linkedin/ribbit-token-letter.txt` (136K chars).

**Agent-driven content generation pattern**: When the cron needs to generate CREATIVE, VARIED content from source material (not just read a pre-written file), use `no_agent=false` (default). The agent reads the source material + rotation state, generates an original post, publishes via `linkedin.py post-file`, and updates the state. This is more expensive (tokens) but produces unique content each run. Use `no_agent=true` only when the post text is pre-written and just needs publishing.

**Source material integration**: When [REDACTED — dati personali rimossi] provides a PDF or reference document for content inspiration:
1. Extract text: `pdftotext document.pdf <HERMES_ROOT>/shared/marketing/linkedin/source-material.txt`
2. Reference the extracted text in the cron prompt (agent reads first N chars for context)
3. Create a rotation state JSON file for theme tracking
4. Set up agent-driven cron (no_agent=false) that reads source + state, generates, publishes, updates state

### 6. ROI Calculator

Include in landing page or create standalone:
- Input: numero dipendenti, costo medio errore, ore settimanali perso
- Output: risparmio annuo, ROI, break-even
- Formula: (ore_risparmiate × costo_orario × 12) - (prezzo_bot × 12)

### Content Strategy — Pre-Launch vs Launch vs Post-Launch

**[REDACTED — dati personali rimossi] corrected this explicitly (2026-06-01):** "non va bene i post devono solo pubblicizzare il prodotto, e' ancora presto per lanciarlo."

The content strategy depends on product readiness:

### Pre-Launch (product NOT ready)
- **Goal**: Build awareness, curiosity, problem recognition — NOT sell
- **Tone**: Teaser, hype, "we're building something"
- **Rules**:
  - ❌ NO links to website/product
  - ❌ NO pricing or trial offers
  - ❌ NO hard CTAs ("sign up", "try it now")
  - ❌ NO announcing the product as "live" or "available"
  - ✅ Focus on the PROBLEMS (costo nascosto, tempo perso, consulenze ripetitive)
  - ✅ Soft CTAs only ("Presto vi mostreremo", "Segui questa pagina")
  - ✅ Build anticipation without revealing everything
  - ✅ 600-900 chars, 3-4 hashtags, no emoji (actual posts range 600-900, not 500-700)
  - ✅ **Cite credible sources** — reference thought leadership that inspired the vision (e.g. Ribbit Capital Token Letter, industry threads). This builds authority without revealing the product. Use the "lesson N" hook pattern when referencing threads (e.g. "La lezione 12 del thread che ci ha ispirato:"). See `references/prelaunch-content-strategy.md` for full patterns.
- **Duration**: Until [REDACTED — dati personali rimossi] says "siamo pronti" or "lanciamo"

**Pattern — URL shared mid-session**: When [REDACTED — dati personali rimossi] sends a URL (tweet, article, thread) during a content creation session, he wants the content REWRITTEN to incorporate that external reference as inspiration. Don't just append — rework the narrative so the source is the through-line. Example: [REDACTED — dati personali rimossi] sent a tweet about "21 mistakes building AI agents" → rewrote all 5 teaser posts to reference specific lessons from that thread.

### Launch (product ready, first week)
- **Goal**: Drive sign-ups and trials
- **Tone**: Annuncio, CTA forte, link, prezzo
- **Content**: Annuncio, casi studio reali, CTA finale
- **Duration**: 1 week (5-7 days)

### Post-Launch (ongoing)
- **Goal**: Engagement, credibility, leads
- **Tone**: Educational, showcase, engagement mix
- **Content**: Full content calendar with post types (Lun=Engagement, Mer=Showcase, Ven=Educational)
- **Duration**: Indefinite

**Pitfall**: NEVER write launch-style content when [REDACTED — dati personali rimossi] says the product isn't ready. The first instinct should be to ask "are we in pre-launch or launch phase?" if unclear.

**Best practice — Source Citation**: When [REDACTED — dati personali rimossi] wants to reference thought leadership (e.g. Ribbit Capital Token Letter), use this pattern: (1) Open with the discovery — "Qualche mese fa ho letto...", (2) Name the source — "Si chiama Token Letter. L'ha scritta Ribbit Capital.", (3) Quote or paraphrase the key insight, (4) Connect to the problem, (5) Tease the solution — "Da quel giorno stiamo costruendo qualcosa.", (6) Include source hashtag (#TokenLetter). This builds authority without revealing the product. See `references/prelaunch-content-strategy.md` for full examples.

## Content Calendar — Monthly Workflow

[REDACTED — dati personali rimossi] writes (or co-writes) content calendars as the primary LinkedIn strategy. This is a REPEATING monthly task.

### Flow
1. [REDACTED — dati personali rimossi] provides the full calendar (or approves one you draft)
2. Save to `<HERMES_ROOT>/shared/marketing/brand/linkedin-program-completo-<month>-<year>.md` (or `linkedin-calendario-<month>-<year>-3xday.md` for high-frequency)
3. Update WannabeBot's cron job (`linkedin-content-calendar`, ID in References) to read from the new file
4. Cron delivers to `telegram:<ADMIN_CHAT_ID>:32638` on publish

### [REDACTED — dati personali rimossi]'s Post Format (match this structure)
Each post MUST include:
- **Header:** `## POST N — Giorno Data` with **Tipo** (🔵 Engagement / 🟡 Showcase / 🟢 Educational) and **Formato** (Testo / Immagine / Video / Infografica / Sondaggio)
- **Visual:** Description of required visual asset (dimensions, colors, content)
- **COPY:** The actual post text — ready to copy-paste, no meta-commentary
- **Riepilogo table** at the end: #, Data, Tipo, Formato, Bot protagonista
- **Asset list:** separate section listing all visual assets needed (video, images, infografiche, sondaggi, quote cards)
- **Note per WannabeBot:** operational instructions for the cron job
- **NO FABRICATED DATA**: See Anti-Fabrication Rules above. Only verifiable facts.

### Post Mix Pattern (validated June-July 2026)
- **Lun (🔵 Engagement):** Polls, questions, storytelling — drive comments
- **Mer (🟡 Showcase):** Bot spotlight, case studies, founder story — drive credibility
- **Ven (🟢 Educational):** How-to, infographics, video demos — drive saves/shares
- Target: 12-14 posts/month, mix of ~4 engagement, ~4 showcase, ~4 educational
- Max 7 hashtags per post (5-7 range)
- 800-1200 characters per post
- Hook in first 2 lines (before "see more" fold)
- **July 2026 program**: Full 14-post calendar with copy + visual briefs at `<HERMES_ROOT>/shared/marketing/brand/linkedin-program-completo-luglio-2026.md`
- **July 2026 HIGH-FREQUENCY program**: 93 posts (3/day) at `<HERMES_ROOT>/shared/marketing/brand/linkedin-calendario-luglio-2026-3xday.md` — 62KB, 2067 lines, complete copy per ogni post. Cron: `0 9,12,18 * * *`
- **July 2026 HIGH-FREQUENCY program**: 93 posts (3/day) at `<HERMES_ROOT>/shared/marketing/brand/linkedin-calendario-luglio-2026-3xday.md` — 62KB, 2067 lines, complete copy per ogni post. Cron: `0 9,12,18 * * *`

**Pitfall**: Always verify month lengths before publishing. June=30 not 31. Use `datetime` or calendar check.

### Ribbit Capital Style Content (June 2026)
[REDACTED — dati personali rimossi] adopted Ribbit Capital's "Token Letter" style for LinkedIn content. Key principles:
- **Bold, provocative openings** — declarations, NOT questions
- **Data-driven specificity** — concrete numbers, not vague claims
- **Conceptual framing** — "agenti specializzati" not "bot", "team digitale" not "chatbot"
- **Series format** — narrative arcs with teasing between posts
- **Provocative contrasts** — old vs new, traditional vs revolutionary
- **Visionary but grounded** — big vision backed by real examples

Full framework: see `references/ribbit-style-content-framework.md`

**Cron schedule (updated June 2026):** `0 9,12,18 * * *` — 3 posts/day at 09:00+12:00+18:00 (93 posts/month, July 2026 high-frequency program). Previous schedules: `0 10 * * 1,3,5` (3/week), `0 9,15 * * *` (2x/day), `0 9 * * 1,3,5` (3/week 9:00).

**Staggered dual-cron pattern (validated 2026-06-05):** When running TWO posting crons on the same channel, stagger times to avoid double-posting:
- `linkedin-content-calendar` (Wannabe, LLM-driven): 9:00, 12:00, 18:00
- `linkedin-auto-post` (script, queue-based): 10:00, 14:00, 19:00

**Pitfall — Duplicate cron creation:** ALWAYS run `cronjob list` BEFORE creating a new LinkedIn posting cron. [REDACTED — dati personali rimossi] corrected: "esiste gia un job". If a similar job exists, UPDATE it instead of creating a duplicate. If [REDACTED — dati personali rimossi] wants both, stagger the schedules.

**Auto-post script pattern (validated 2026-06-05):** For pre-written post queues, use a lightweight Python script instead of an LLM agent:
- Script: `<HERMES_ROOT>/shared/linkedin/auto-post.py` — reads all `P*.txt` from `posts/` dir, finds next unpublished via `published.json` tracker, publishes via `linkedin.py post`, updates tracker
- Tracker: `<HERMES_ROOT>/shared/marketing/linkedin/published.json` — array of `{file, date, output}`
- Posts dir: `<HERMES_ROOT>/shared/marketing/linkedin/posts/` — `P01-slug.txt` through `P35-slug.txt`
- Cron: `no_agent=True`, `script: python3 <HERMES_ROOT>/shared/linkedin/auto-post.py`
- When queue runs out, script prints "No unpublished posts remaining" (silent delivery)
- **Extend queue**: just add new `P*.txt` files to the dir — script auto-discovers by glob

### LinkedIn Media Support (implemented 2026-05-29)
`linkedin.py` supports text, image, video, and poll posts:
- ✅ Text posts: `post-file <txt>`
- ✅ Image posts: `post-file-image <txt> <img>` (3-step: register upload → PUT binary → create post)
- ✅ Video posts: `post-file-video <txt> <vid>` (4-step: init → chunked PUT → finalize → create post)
- ✅ Poll posts: `post-file-poll <txt> "Q?" "A" "B" ["C" ["D"]]` (2-4 options, configurable duration) — ⚠️ KNOWN FAILURE: returns 422 `\"POLL\" is not an enum symbol`. Fallback: publish as text-only via `post-file`. (Validated 2026-06-05)
- ⚠️ Carousel posts: not yet implemented

**Cron job auto-detects format** from the content calendar's "Formato" field and uses the correct command. If an image/video asset doesn't exist on disk, the cron falls back to text-only with a `[Visual: description]` placeholder.

### Cron Job Profile Routing
**LinkedIn posting belongs to WannabeBot profile**, NOT gribbito. WannabeBot is the Media Manager.
- Profile: `wannabe`
- Deliver: `telegram:<ADMIN_CHAT_ID>:32638`
- Enabled toolsets: `terminal`, `file`

**Pitfall**: Never create LinkedIn posting crons under gribbito. [REDACTED — dati personali rimossi] corrected this explicitly — "i post li deve gestire wannabebot."

## File Structure (23 files, 332KB — created 2026-05-29)

```
<HERMES_ROOT>/shared/marketing/
├── starter-kit.md                    # Pricing tiers + launch offer + pitch script + FAQ
├── brand/
│   ├── brand-identity.md             # Full brand guide (palette, fonts, tone, logo concepts)
│   ├── social-templates.md           # 10 post templates (Bot in Azione, Lo sapevi?, Prima/Dopo)
│   └── content-calendar.md           # 30 giorni LinkedIn (3 post/settimana)
├── landing/
│   └── index.html                    # Production-ready landing page (48KB, dark theme, responsive)
├── pitch-deck/
│   └── index.html                    # 10 slide interattive con navigazione (24KB)
├── audit/
│   ├── audit-questionnaire.md        # 15 domande GDPR per PMI
│   ├── audit-report-template.md      # Report template con score 0-100
│   └── audit-landing-copy.md         # Landing page copy per il free audit
├── outreach/
│   ├── campaign-tracker.csv            # Outreach tracking (date, channel, contact, status, notes)
│   ├── partnership-commercialisti.md   # 3 templates: connection request, DM, email formale
│   ├── commercialisti-outreach.md      # Template per studi contabili (Telegram, LinkedIn, email)
│   ├── coworking-outreach.md           # Template per coworking (workshop proposal)
│   ├── pmi-outreach.md                 # Direct outreach per PMI (4 segmenti)
│   └── referral-program.md             # Programma referral con codici
├── telegram-gruppi.md                  # 70+ gruppi Telegram italiani (PMI, ristoratori, startup, freelance, marketing)
├── demo-bot/
│   ├── demo_bot.py                     # Demo bot Telegram (python-telegram-bot v21+, rate limiting, menu)
│   └── demo-bot-setup.md              # Setup guide (BotFather, systemd, venv)
├── email/
│   ├── drip-sequence.md                # 5-email lead nurturing sequence (Day 0-12)
│   └── outreach-commercialisti-sequence.md  # 3-email commercialisti partnership sequence
├── landing-pages/
│   ├── ContAIbile.md                   # Landing page copy per bot (hero, pain, features, FAQ, CTA)
│   ├── LAWrenzo.md
│   ├── GROOT.md
│   ├── Wannabe.md
│   ├── DesignBro.md
│   └── Ducato.md
├── competitors/
│   └── competitive-analysis.md         # 10 competitor italiani (pricing, features, positioning matrix)
├── micro-siti/
│   ├── food-cost-guida.md              # SEO article: "Come Calcolare il [REDACTED — dati personali rimossi]" (1500 parole)
│   ├── gestionale-pizzeria-guida.md    # SEO article: "Miglior Gestionale Pizzeria 2026" (1500 parole)
│   ├── commercialista-ai-guida.md      # SEO article: "Commercialista AI Guida Completa 2026" (1800 parole)
│   └── gestionale-ristorante-guida.md  # SEO article: "Gestionale Ristorante 2026 - 10 Migliori" (2400 parole)
├── press-release.md                    # Comunicato stampa (StartupItalia, Wired, Sole 24 Ore)
├── referral-program.md                 # "Porta un Amico" — 1 mese gratis per referral
├── google-business-profile.md          # Google Business Profile draft completo
├── linkedin/
│   ├── linkedin-posts.md               # 5 post company page launch (intro, problem, case study, provocation, before/after)
│   ├── editorial-calendar-luglio.md    # Calendario 3/week luglio (lun/mer/ven, 14 post)
│   ├── published.json                  # Tracker post pubblicati (auto-post.py reads this)
│   └── posts/                          # Post queue directory (P01-slug.txt ... P35+slug.txt)
│       ├── P01-intro-azienda.txt
│       ├── P02-problem-solution.txt
│       ├── ...
│       └── P35-cta-prova-gratuita.txt
    ├── banner.html                     # LinkedIn banner 1584x396 (HTML, screenshot to use)
    ├── informativa-cookie.md
    ├── contratto-fornitura.md
    ├── nda.md
    ├── lettera-incarico.md
    ├── regolamento-interno.md
    ├── dpa.md
    ├── clausola-recesso.md
    ├── contratto-consulenza.md
    └── termini-servizio.md
├── linkedin-page.md                  # LinkedIn company page setup (about, specialties, 5 launch posts)
└── linkedin/
    ├── banner.html                   # LinkedIn banner 1584x396 (HTML, screenshot to use)
    ├── banner.png                    # LinkedIn banner 1584x396 (Pillow-generated PNG)
    ├── logo.html                     # LinkedIn logo 300x300 (HTML, screenshot to use)
    ├── post-1.txt                    # Teaser post 1 (Annuncio soft — "Stiamo costruendo qualcosa")
    ├── post-2.txt                    # Teaser post 2 (Problema — costo nascosto ristoranti)
    ├── post-3.txt                    # Teaser post 3 (ROI — consulenze automatizzabili)
    ├── post-4.txt                    # Teaser post 4 (Filosofia — specialisti vs tool generici)
    ├── post-5.txt                    # Teaser post 5 (Soft CTA — "Segui questa pagina")
    ├── post-ribbit-1.txt             # Ribbit-style post 1 (Intro: agenti vs dipendenti)
    ├── post-ribbit-2.txt             # Ribbit-style post 2 (Perché bot generalisti falliscono)
    ├── post-ribbit-3.txt             # Ribbit-style post 3 (Costo nascosto task ripetitivi)
    ├── post-ribbit-4.txt             # Ribbit-style post 4 (Caso studio Torino)
    ├── post-ribbit-5.txt             # Ribbit-style post 5 (Identità digitale agente)
    ├── post-ribbit-6.txt             # Ribbit-style post 6 (Costi team AI vs tradizionale)
    └── post-ribbit-7.txt             # Ribbit-style post 7 (Manifesto: 7 agenti, 1 missione)
├── x-images/                         # X/Twitter character images (DEPRECATED — AI-generated)
│   ├── x-ratatouille.png
│   ├── x-contabile.png
│   ├── x-lawrenzo.png
│   ├── x-wannabe.png
│   ├── x-designbro.png
│   ├── x-el-froggo.png
│   ├── x-groot.png
│   └── x-hermesbro.png
└── x-posts/                          # X/Twitter post images (CURRENT — PIL-composited from existing PFPs)
    ├── x-post-contaibile.png
    ├── x-post-ratatouille.png
    ├── x-post-lawrenzo.png
    ├── x-post-wannabe.png
    ├── x-post-designbro.png
    ├── x-post-el-froggo.png
    ├── x-post-groot.png
    └── x-post-hermesbro.png
```

### 7. LinkedIn Company Page

Create `<HERMES_ROOT>/shared/marketing/linkedin-page.md` with:
- Company name, tagline (one-liner, ~15 words)
- About section (~1850 chars, keyword-rich for SEO)
- 20 specialties (copy-paste for LinkedIn)
- Company info fields (industry, size, type, founded, HQ)
- 5 launch posts (annuncio, problema/soluzione, team intro, caso studio, CTA)
- Banner + logo HTML for screenshotting (see below)

Create visual assets as HTML (no image generation needed):
- `<HERMES_ROOT>/shared/marketing/linkedin/banner.html` — 1584×396px, dark theme with brand palette
**Pitfall**: [REDACTED — dati personali rimossi] may reference `/home/[REDACTED — dati personali rimossi]/hermesbro-landing/index.html` — that file does NOT exist. The canonical file is `{WEB_ROOT}/index.html`.

**Pitfall — No emoji on professional sites**: [REDACTED — dati personali rimossi] explicitly said "le emoji non mi piacciono sono troppo infantili". NEVER use emoji on hermesbro.cloud or any professional marketing material. Replace with SVG icons (Lucide/Heroicons style — thin strokes, gold #d4a853) or use styled text labels. The only exception is the Italian flag in the footer (brand identity).

**Emoji → SVG replacement pattern** (validated 2026-06-03):
When replacing emojis in HTML, use inline SVGs with consistent styling:
```html
<!-- Before -->
<div class="ci">🔒</div>
<!-- After -->
<div class="ci"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#d4a853" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">...</svg></div>
```
SVG specs: 28×28 viewBox, stroke-based (no fill), `#d4a853` gold, `stroke-width="1.5"`, `stroke-linecap="round"`. Use Lucide icon set (lucide.dev) as source. Common icons used on hermesbro.cloud:
- Ristorante/food → utensils
- Costi/compliance → bar-chart
- Prodotto digitale → rocket
- Audit Trail → lock
- GDPR → shield-check
- Disclaimer → info (circle)
- Human Review → eye

**Agent card PFP pattern** (validated 2026-06-03):
The agent cards in the "Dieci agenti" section use `.tp` (top) with `.ic-img` class for PFPs:
```html
<div class="tp">
  <img src="/bot-profiles/pixel-contaibile.png" alt="ContAIbile" class="ic-img">
  <div class="nc"><h3>CONTAIBILE</h3><span class="cat">Contabilità</span></div>
</div>
```
CSS: `.acard .tp .ic-img{width:48px;height:48px;border-radius:12px;flex-shrink:0;object-fit:cover;border:1px solid rgba(212,168,83,0.3);background:rgba(255,255,255,0.03)}`

**Pitfall — Windows files**: [REDACTED — dati personali rimossi] sometimes prepares updated HTML files on his Windows PC (e.g., `C:\Users\pc\hermesbro_new.html`) and asks to SCP them to VPS. This is NOT possible — we can't SSH to his local machine. Ask him to either paste the content in chat or do the SCP himself. If he provides manual change instructions instead, apply them with `patch`.

**Pitfall**: Image generation (FAL) may be unavailable. Always create HTML fallbacks for banner/logo so [REDACTED — dati personali rimossi] can screenshot them. Do NOT block on image_generate.

**Pillow fallback**: When FAL is unavailable, use `pip install Pillow --break-system-packages` and generate PNGs programmatically:
- Logo: 800x800 circle, gold H on dark blue gradient, thin gold ring border
- Banner: 1584x396, dark blue grid background, centered title + subtitle + 5 colored badges (ContAIbile, LAWrenzo, GROOT, Wannabe, DesignBro)
- Use DejaVu or Liberation fonts (available on most Linux systems)
- Save to `<HERMES_ROOT>/shared/marketing/linkedin/logo.png` and `banner.png`

**Banner HTML pattern**: Use CSS gradients, grid background pattern, and bot icons with distinct colors. See existing `banner.html` for reference.

**Logo HTML pattern**: Circular div with radial gradient, large gold letter (H), subtle glow. See existing `logo.html`.

### Adding Bot Images to Landing Page

When new bot profile images become available ([REDACTED — dati personali rimossi] sends them), the landing page at `{WEB_ROOT}/index.html` needs TWO updates per bot:

1. **Hero section** — `<div class="product-card">` uses `<div class="product-avatar">` for the circular bot image. If a bot has no image yet, it shows a colored letter fallback (e.g., `<div class="product-avatar" style="background: var(--green);">G</div>`). Replace with: `<img src="/img/botname.png" alt="BotName" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`

2. **Specs section** — `<div class="spec-icon">` uses a colored circle with emoji. Replace with: `<img src="/bot-profiles/pixel-botname.png" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`

**Image paths**:
- `/img/` = bot profile images (contaibile.png, lawrenzo.png, etc.) — full-color photos/logos
- `/bot-profiles/` = pixel art NFT versions (pixel-*.png) — used in specs section

**Pitfall**: When updating images, verify the file exists on disk before patching HTML. Copy from source to nginx root if needed: `cp <HERMES_ROOT>/shared/marketing/bot-profiles/pixel-*.png {WEB_ROOT}/bot-profiles/`

**Pitfall**: After updating the landing page, always `nginx -t && systemctl reload nginx` and verify with `curl -s https://hermesbro.cloud/ | grep 'img/botname'`.

**Pitfall — Browser cache**: After replacing a bot profile image file on disk, the browser still shows the OLD image (nginx `Cache-Control: max-age=2592000`, 30 days). Fix: add `?v=N` cache-busting parameter to ALL `<img src>` references for that bot. Search ALL occurrences with `grep -n "pixel-botname" {WEB_ROOT}/index.html` — typically TWO per bot (product-avatar in hero + spec-icon in specs). Both must be updated. Without this, [REDACTED — dati personali rimossi] will say "non funziona" / "ce ancora quello vecchio".

See `references/hermesbro-landing-page-structure.md` for full HTML structure reference.

## Privacy Policy Hosting

LinkedIn apps require a Privacy Policy URL. Host at the existing nginx site:
- `{WEB_ROOT}/privacy-policy.html` — GDPR-compliant Italian privacy policy
- URL: `https://hermesbro.cloud/privacy-policy.html`
- Dark theme, branded, covers data collection, legal basis (art. 6 GDPR), retention, rights (art. 15-22), DPO contact

## LinkedIn API Integration

When materials are ready, connect LinkedIn for automated posting:

**Integration location**: `<HERMES_ROOT>/shared/linkedin/`
- `linkedin.py` — Full OAuth + posting script (auth, token, me, post, post-org, post-file)
- `config.env` — Credentials template (CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, PERSON_URN, ORG_URN)
- `SETUP.md` — Step-by-step guide for [REDACTED — dati personali rimossi]

**OAuth flow**:
1. [REDACTED — dati personali rimossi] creates app at https://www.linkedin.com/developers/
2. Redirect URL: `http://localhost:8089/callback`
3. Scopes: `r_liteprofile r_emailaddress w_member_social` (only these work with "Share on LinkedIn" product alone)
4. Run `python3 linkedin.py auth` → browser opens → [REDACTED — dati personali rimossi] authorizes
5. Run `python3 linkedin.py token <code>` → saves access token (60 days)
6. Run `python3 linkedin.py me` → saves person URN

**⚠️ Person URN blocker**: With only "Share on LinkedIn" product, /v2/me returns 403. [REDACTED — dati personali rimossi] must add "Sign In with LinkedIn using OpenID Connect" product (self-serve) to get `openid` scope and the `sub` claim. See `references/linkedin-oauth-pitfalls.md` for full details.

**Posting**:
```bash
python3 linkedin.py post "text"           # Personal profile text post
python3 linkedin.py post-org "text"       # Company page text post
python3 linkedin.py post-file post.txt    # Text from file
python3 linkedin.py post-image "text" img.png    # Image + text
python3 linkedin.py post-file-image post.txt img.png  # Image + text from file
python3 linkedin.py post-video "text" vid.mp4    # Video + text (chunked upload)
python3 linkedin.py post-file-video post.txt vid.mp4  # Video + text from file
python3 linkedin.py post-poll "text" "Q?" "A" "B" ["C" ["D"]]  # Poll (2-4 options)
python3 linkedin.py post-file-poll post.txt "Q?" "A" "B"       # Poll from file
```

**⚠️ Current state (2026-05-29)**: `LINKEDIN_ORG_URN=""` — all posts go to [REDACTED — dati personali rimossi]'s personal profile. To post as company page:
1. [REDACTED — dati personali rimossi] creates LinkedIn Company Page
2. Add `w_organization_social` scope (restricted, needs LinkedIn approval)
3. Re-auth with new scope
4. Run `linkedin.py me` after auth to get ORG_URN
5. Update `config.env` with `LINKEDIN_ORG_URN`

**Pitfall — No analytics API**: `linkedin.py` can only POST content. It cannot read engagement metrics (likes, comments, shares, impressions, views). To get analytics:
- **Manual**: [REDACTED — dati personali rimossi] checks LinkedIn directly and reports back
- **API addition (future)**: Requires `/v2/ugcPosts/{id}/lifecycleState` + `/v2/organizationalEntityShareStatistics` endpoints, plus `r_organization_social` scope (restricted, needs LinkedIn approval)
- **Impersonation (not viable)**: LinkedIn blocks scraping; browser automation gets CAPTCHAed

**Cron automation**: `linkedin-content-calendar` (Mon/Wed/Fri 9:00) generates posts from content calendar AND auto-posts to LinkedIn. The cron prompt embeds the Python posting code directly (reads token + URN from `config.env`, POSTs to `/v2/ugcPosts`). [REDACTED — dati personali rimossi] gets a notification with the published post text. If the token expires (401), the cron reports the error.

**Pitfall**: LinkedIn tokens expire in 60 days. Re-run `auth` when expired.
**Pitfall**: `w_organization_social` scope (posting as company page) is a RESTRICTED LinkedIn API product. It requires manual approval from LinkedIn (can take days/weeks). On first setup, use `w_member_social` ONLY — personal posting works immediately. Scope error: `unauthorized_scope_error: Scope "w_organization_social" is not authorized for your application`.
**Pitfall**: OAuth redirect goes to `http://localhost:8089/callback` which won't load ([REDACTED — dati personali rimossi] isn't on the server). The page will show an error — that's expected. [REDACTED — dati personali rimossi] must copy the `code=` parameter from the URL bar and send it back. Example: if URL is `http://localhost:8089/callback?code=AQT5...&state=hermesbots2026`, send only `AQT5...`.
**Pitfall**: LinkedIn Developer App requires a Company Page URL at creation time. Create the page FIRST (https://www.linkedin.com/company/setup/new/), then create the app.
**Pitfall**: The LinkedIn app creation form asks for a "LinkedIn Page" — this must be a Company Page, not a personal profile. If [REDACTED — dati personali rimossi] hasn't created the company page yet, he needs to do that first.
**Pitfall**: The form asks for "Privacy policy URL" — use `https://YOUR_VPS_HOST/hermesbro/privacy-policy.html`.
**Pitfall**: After creating the app, add redirect URL `http://localhost:8089/callback` in the Auth tab before running `linkedin.py auth`.
**Pitfall**: Image generation (FAL) may be unavailable. Always create HTML fallbacks for banner/logo so [REDACTED — dati personali rimossi] can screenshot them. Do NOT block on image_generate.
**Pitfall**: `pip install Pillow` fails with PEP 688 on newer Debian/Ubuntu. Use `pip install Pillow --break-system-packages`.

**Pitfall**: `urn:li:person:~` and `urn:li:member:~` do NOT work as author values in the Posts API. You must use the actual person URN (e.g., `urn:li:person:XXXXXXXXXX`). Get it from the `sub` claim after OIDC auth.

## LinkedIn Launch Post Scheduling

When [REDACTED — dati personali rimossi] says "programma i post" or "schedule the posts" for a specific set of launch/scheduled posts:

1. **Extract each post** into its own `.txt` file in `<HERMES_ROOT>/shared/marketing/linkedin/` (e.g., `post-ribbit-1.txt`, `post-ribbit-2.txt`)
2. **Create one-shot cron jobs** (`no_agent=True`) — one per post, scheduled daily at 09:00:
   ```
   schedule: "2026-06-02T09:00:00"  # ISO timestamp, one-shot
   script: "cd <HERMES_ROOT>/shared/linkedin && python3 linkedin.py post-file <HERMES_ROOT>/shared/marketing/linkedin/post-ribbit-1.txt"
   deliver: "telegram:<ADMIN_CHAT_ID>"
   ```
3. **Pause conflicting recurring crons** — if `linkedin-content-calendar` runs on the same days/times, pause it for the launch week and tell [REDACTED — dati personali rimossi] you'll re-enable it after
4. **Re-enable recurring crons** after launch week ends

**Pitfall**: Always check for existing LinkedIn cron jobs before scheduling. A recurring content calendar cron at the same time will double-post. Pause it first.

**Pitfall**: `post-file` reads the file at execution time, so the .txt files must exist on disk when the cron fires — don't use temp files that get cleaned up.

**Pattern — Manual publish ahead of schedule**: [REDACTED — dati personali rimossi] sometimes asks to schedule a full campaign, rewrites the content, then says "inizia ora con il primo" (start now with the first). When this happens:
1. Publish the first post immediately via `cd <HERMES_ROOT>/shared/linkedin && python3 linkedin.py post-file /path/to/post-1.txt`
2. Keep remaining posts as scheduled one-shot crons (don't reschedule)
3. Update tracking files: `status.md` (mark as ✅ Pubblicato + URL), `content-calendar.md` (same), `linkedin-posts.md` (append published entry)
4. Report the published URL to [REDACTED — dati personali rimossi]

**Current cron IDs** (verify with `cronjob list` before acting — IDs change on recreation):
- `linkedin-content-calendar`: `bff03691e0e2` (3x/day 09:00+12:00+18:00, Wannabe profile, July 2026 high-frequency program)

### Rotation State Tracking (for recurring content calendars)
When generating varied content on a recurring schedule, use a JSON state file to track what's been posted:
```json
{
  "last_theme_index": -1,
  "last_sub_index": 0,
  "post_count": 0,
  "themes": ["token_factory", "memory_tokens", "identity_kya", ...]
}
```
Location: `<HERMES_ROOT>/shared/marketing/linkedin/rotation-state.json`

The cron agent reads this file at the start of each run, advances to the next theme/sub-angle, generates content, publishes, then updates the file. This prevents repetition across 30+ runs.

Each theme has N sub-angles (e.g. 3: vision/problem/story). When sub_index >= N, advance to next theme and reset. When theme_index >= len(themes), wrap to 0.

**Pitfall**: The rotation state file must be read AND written in the SAME cron run. If the agent reads but forgets to write, the next run will produce a duplicate post.

### Auto-Posting Cron Pattern

When the cron job should post to LinkedIn automatically (not just generate text), use the `post-file` command with `no_agent=True`:

```bash
cd <HERMES_ROOT>/shared/linkedin && python3 linkedin.py post-file /path/to/post.txt
```

Key points:
- Config is at `<HERMES_ROOT>/shared/linkedin/config.env`
- Always check for 401 status (token expired → tell [REDACTED — dati personali rimossi] to re-auth)
- The cron delivers to [REDACTED — dati personali rimossi]'s chat with the published post text + post ID
- **Currently posting to PERSONAL profile only** — `LINKEDIN_ORG_URN` is empty. Company page posting requires creating the LinkedIn Company Page first, then running `linkedin.py me` after adding `w_organization_social` scope
- **Current schedule**: `0 9,13,18 * * *` (3 posts/day at 09:00+13:00+18:00)
- **Current content**: July 2026 high-frequency program at `<HERMES_ROOT>/shared/marketing/brand/linkedin-calendario-luglio-2026-3xday.md`
- **Anti-fabrication**: The cron prompt enforces strict rules against fabricated data. NEVER invent case studies, metrics, pricing tiers, or client testimonials.
- **Anti-fabrication**: Cron prompt includes explicit rules against fabricated data (case studies, metrics, pricing tiers). See Anti-Fabrication Rules section above.

## Deployment

**CRITICAL — NEVER replace the existing site without explicit approval:**
When [REDACTED — dati personali rimossi] asks to work on email/outreach/marketing, do NOT touch the existing landing page at `{WEB_ROOT}/index.html`. The site is live and [REDACTED — dati personali rimossi] has approved it. Creating a new landing page is a SEPARATE task that requires explicit approval. If you need a landing page for a campaign, deploy to a different path (e.g., `{WEB_ROOT}-landing/`) and tell [REDACTED — dati personali rimossi] it's ready for review. NEVER overwrite `index.html` without asking. (Validated 2026-06-03: [REDACTED — dati personali rimossi] said "torna assolutamente al sito che avevamo prima" and "non toccare più il sito".)

Landing page deployment:
1. Source: `{WEB_ROOT}/index.html` (nginx root)
2. Domain: `hermesbro.cloud`
3. Test: `nginx -t && systemctl reload nginx`
4. **Image paths**: `/img/` = bot profile images (contaibile.png, lawrenzo.png, etc.), `/bot-profiles/` = pixel art NFT versions (pixel-*.png). All 10 bots have pixel art PFPs (including Machiavelli and Sentinel as of May 2026).
5. Hero section uses `/img/*.png` for bot cards, specs section uses `/bot-profiles/pixel-*.png`

Pitch deck: `<HERMES_ROOT>/shared/marketing/pitch-deck/index.html` (standalone, no deploy needed)

**Pitfall**: `/bots/` nginx route is DISABLED ([REDACTED — dati personali rimossi] said "non è pronto"). Check before deploying.

## Automation (Cron Jobs)

### Content Calendar — `linkedin-content-calendar`
- **Schedule**: `0 9,12,18 * * *` (3 posts/day at 09:00+12:00+18:00 — 93 posts/month)
- **Deliver**: `telegram:<ADMIN_CHAT_ID>:32638`
- **What**: Reads the program file (`linkedin-calendario-luglio-2026-3xday.md`), identifies today's post by date+slot, publishes via `linkedin.py post-text`
- **Profile**: `wannabe` (Media Manager — NOT gribbito)
- **⚠️ Verify job ID**: run `cronjob list` — IDs change on recreation
- **Current content**: July 2026 high-frequency program — 93 posts (3/day, 09:00+12:00+18:00)
- **Post mix**: 🌅 09:00 Educational / ☀️ 12:00 Showcase / 🌙 18:00 Engagement

**Pitfall**: Content calendar doc says "Lun/Mer/Ven" (Mon/Wed/Fri) but cron uses `1,3,5`. Always verify day mapping.
**Pitfall**: For 3x/day schedules, use `0 9,12,18 * * *` — NOT `0 9,12,18 * * 1-5` (weekdays only). [REDACTED — dati personali rimossi] wants weekend posts too for high-frequency programs.
**Pitfall**: For 3x/day schedules, use `0 9,12,18 * * *` — NOT `0 9,12,18 * * 1-5` (weekdays only). [REDACTED — dati personali rimossi] wants weekend posts too for high-frequency programs.

### GDPR Audit Lead Magnet — `gdpr-audit-check`
- **Schedule**: `0 10 * * *` (daily at 10:00)
- **Deliver**: `telegram:<ADMIN_CHAT_ID>:31761`
- **What**: Checks `<HERMES_ROOT>/shared/marketing/audit/submissions/` for new audit questionnaire submissions, generates personalized GDPR compliance report
- **⚠️ Verify job ID**: run `cronjob list` — IDs change on recreation
- **How submissions arrive**: [REDACTED — dati personali rimossi] forwards audit questionnaire responses → saved as JSON in submissions/ dir

### Outreach Research (on-demand)
When [REDACTED — dati personali rimossi] says "parti" or "start outreach":
1. Search for local businesses (commercialisti, coworking, PMI) via web_search
2. Save results to `<HERMES_ROOT>/shared/marketing/outreach/<segment>-torino.md`
3. Prepare ready-to-send messages (Telegram DM, LinkedIn DM, email) with business details
4. Send all messages to [REDACTED — dati personali rimossi]'s chat with clear "copy and send" instructions

**Telegram Group Research**: When expanding outreach to Telegram groups, use `<HERMES_ROOT>/shared/marketing/telegram-gruppi.md` (70+ groups across 5 categories: PMI, ristoratori, startup, freelance, marketing). Includes best practices (5-phase funnel: Observation → Participation → Authority → Soft Promo → Advocacy) and per-product strategy matrix.

**Verifying Telegram groups exist** (VALIDATED pattern 2026-06-05):
```python
import urllib.request, urllib.error, re
for name, slug in groups:
    url = f"https://t.me/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=10)
    html = resp.read().decode("utf-8", errors="replace")
    has_preview = "tgme_page_description" in html or "tgme_page_title" in html
    # EXISTS if has_preview, 404 if HTTPError
```
Result: 20/20 priority groups verified as existing. Groups with few members (2-3) may be dead — focus on those with 5K+.
[REDACTED — dati personali rimossi] handles joining himself: "per i gruppi telegram tu trovali poi mi aggiungo io."

**Validated Torino targets** (2026-05-29):
- Commercialisti: Studio Thelema (priority #1), Garzena Rizzolio, Caretti, Zamprogna & Brusa, Rizzi
- Coworking: Impact Hub (torino@impacthub.net), Toolbox (info@toolboxcoworking.com), Talent Garden, Copernico
- See `outreach/commercialisti-torino.md` and `outreach/coworking-torino.md`

## Delivering Images to [REDACTED — dati personali rimossi]

**Pitfall**: `send_message` with `MEDIA:` prefix does NOT deliver images as native photos on Telegram. They arrive as text/emoji. Use the direct Bot API script instead:

```bash
python3 <HERMES_ROOT>/shared/scripts/send-photo.py <chat_id> <photo_path> <caption>
```

For logos, banners, screenshots — always use `send-photo.py`. See `telegram-media-sending` skill for details.

## Instagram Integration (2026-05-29)

Instagram is now a second distribution channel alongside LinkedIn. Content adapts from the same brand assets.

### Credentials & Setup
- **Meta Developer App ID**: `964286013154351`
- **Facebook Page**: HermesBro (`61590239981367`)
- **Instagram Account ID**: `836456009537148`
- **Status**: Access token NOT YET generated (user needs to navigate Meta dashboard)
- **Full setup guide**: `<HERMES_ROOT>/shared/instagram/SETUP.md`
- **Skill reference**: `instagram-graph-api` skill — credential collection, API capabilities, publishing script

### Content Files
```
<HERMES_ROOT>/shared/instagram/
├── .env                 # Credentials (chmod 600)
├── publish.py           # Publishing script (photo, carousel, Reel, Story)
├── bio.md               # Bio text + highlight covers plan
├── posts.md             # 10 posts with captions, hashtags, visual direction
└── SETUP.md             # Token generation guide
```

### Instagram vs LinkedIn Content Differences
| Aspect | LinkedIn | Instagram |
|--------|----------|-----------|
| Tone | Più formale, B2B | Più visuale, leggermente più casual |
| Format | Testo lungo ok | Max 2200 char, visual-first |
| Hashtags | 3-5 max | 5-15, mix branded + industry |
| Best format | Text + occasional image | Caroselli, Reels, grafiche |
| Posting | Mon/Wed/Fri 9:00 | Same schedule, adapted content |
| Automation | LinkedIn API (cron) | Graph API (cron, once token available) |

**Pitfall**: Instagram images must be publicly accessible URLs. Local files won't work. Host on the VPS nginx or use a CDN.

### Cross-Post Workflow
When creating a LinkedIn post, also adapt it for Instagram:
1. Shorten to 2200 chars
2. Add 5-15 hashtags
3. Specify visual direction (Instagram is visual-first)
4. Note if it should be a carousel (multi-slide performs better)

**Ribbit-style adaptation**: Instagram posts can use the same provocative openings but need stronger visual hooks. Consider carousel format for series posts (each slide = one post from the series).

## X/Twitter Integration (2026-06)

X/Twitter is configured via `xurl` CLI with app `el-froggo` (@FroggoEl18782).
- **Auth state (2026-06)**: OAuth2 token expired — 401 Unauthorized on `xurl whoami` and `xurl post`
- **Re-auth command**: `xurl auth oauth2 --app el-froggo FroggoEl18782` (user must authorize in browser)
- **Config location**: `~/.xurl` (YAML, auto-refresh OAuth2 tokens)
- **Skill reference**: `xurl` skill — full CLI reference for posting, searching, DMs, media
- **Character images**: 8 composited post images at `<HERMES_ROOT>/shared/marketing/x-posts/x-post-*.png` (1200×675). See "X/Twitter Image Generation" section below for compositing workflow. (Old AI-generated images at `x-images/` are deprecated.)

**Pitfall**: X API tokens expire. If `xurl post` returns 401, tell [REDACTED — dati personali rimossi] to re-auth. Don't retry — same error will repeat.

**Pitfall**: Each Hermes profile needs its own `~/.xurl` copy. If a bot profile can't use xurl, copy: `cp ~/.xurl <HERMES_ROOT>/profiles/<profile>/home/.xurl`

## X/Twitter Image Generation (2026-06)

When [REDACTED — dati personali rimossi] asks for X/Twitter images based on bot PFPs, use this workflow:

### ⚠️ CRITICAL PREFERENCE — USE EXISTING PFPs, DO NOT GENERATE NEW ONES
[REDACTED — dati personali rimossi] explicitly corrected this (2026-06-05): "Voglio che usi esattamente i pfp attuali non che ne crei di nuovi."
**NEVER use image_generate or OpenAI API to create new character images.** Instead, composite the existing pixel art PFPs onto branded canvases using Python/PIL. The PFPs ARE the characters — don't reimagine them.

### Source PFPs
- Pixel art PFPs (8): `<HERMES_ROOT>/shared/marketing/bot-profiles/pixel/pfp-*.png` (256×256)
- Full-color profiles: `<HERMES_ROOT>/shared/marketing/bot-profiles/bot-profile-*.jpg`
- Landing page pixel art (12): `{WEB_ROOT}/bot-profiles/pixel-*.png` (includes Machiavelli, Sentinel, Mr Robot)

### Pitfall — Ratatouille has NO pixel PFP
Only has `bot-profile-ratatouille-01.jpg` (non-pixel). Use the JPG with `Image.LANCZOS` resize (not `Image.NEAREST` which is for pixel art).

### Compositing Pattern (PIL)
Use Python/PIL to composite existing PFPs onto branded 1200×675 canvases:

```python
import os
from PIL import Image, ImageDraw, ImageFont

PFP_DIR = "<HERMES_ROOT>/shared/marketing/bot-profiles/pixel"
OUT_DIR = "<HERMES_ROOT>/shared/marketing/x-posts"
os.makedirs(OUT_DIR, exist_ok=True)
W, H = 1200, 675

# Bot data: (slug, name, tagline, description, accent_color, pfp_path)
bots = [
    ("contaibile", "ContaIbile", "Il tuo commercialista digitale", "Fatture, IVA, F24, crypto tracking", "#00ff00",
     os.path.join(PFP_DIR, "pfp-contaibile.png")),
    ("ratatouille", "Ratatouille", "Il tuo assistente ristoratore", "Food cost, scorte, report vendite", "#ff6b35",
     "<HERMES_ROOT>/shared/marketing/bot-profiles/bot-profile-ratatouille-01.jpg"),  # JPG fallback
    # ... etc
]

for slug, name, tagline, desc, color, pfp_path in bots:
    img = Image.new("RGB", (W, H), "#0a0a0a")
    draw = ImageDraw.Draw(img)
    # Top/bottom accent lines
    draw.rectangle([0, 0, W, 3], fill=color)
    draw.rectangle([0, H-3, W, H], fill=color)
    # Circle behind PFP
    cx, cy = 200, H // 2
    circle_r = 140
    draw.ellipse([cx-circle_r, cy-circle_r, cx+circle_r, cy+circle_r], outline=color, width=2)
    # Load + paste PFP (NEAREST for pixel art, LANCZOS for JPG)
    pfp = Image.open(pfp_path).convert("RGBA")
    pfp_size = circle_r * 2 - 20
    resample = Image.NEAREST if pfp_path.endswith(".png") else Image.LANCZOS
    pfp = pfp.resize((pfp_size, pfp_size), resample)
    img.paste(pfp, (cx - pfp_size//2, cy - pfp_size//2), pfp)
    # Text: name, tagline, description
    # Branding: "HERMES BOTS" top-right, "hermesbro.com" bottom-right
    img.save(os.path.join(OUT_DIR, f"x-post-{slug}.png"), "PNG")
```

### Layout
- 1200×675 PNG (X in-stream recommended size)
- Dark background (#0a0a0a) with accent color top/bottom lines (3px)
- PFP centered in a 280px circle on the left side
- Bot name (56px bold), tagline (24px), description (20px) on the right
- "HERMES BOTS" top-right, "hermesbro.com" bottom-right (subtle gray)
- Each bot gets its own accent color from the brand palette

### Output
- Directory: `<HERMES_ROOT>/shared/marketing/x-posts/`
- Format: `x-post-<botname>.png` (1200×675, ~50-100KB each)
- All 8 bots: contaibile, ratatouille, lawrenzo, wannabe, designbro, el-froggo, groot, hermesbro

### Old generated images (DEPRECATED)
The old AI-generated images at `<HERMES_ROOT>/shared/marketing/x-images/` (1536×1024) are deprecated. Use `x-posts/` instead.

**Pitfall**: `image_generate` tool fails with FAL pip errors even when `image_gen.provider: openai` is set. Irrelevant now — we don't use it for X images anymore.

**Pitfall**: `vision_analyze` may return 404 if the current model doesn't support vision. Use `browser_vision` as fallback to inspect images, or work from character descriptions in the landing page HTML. Note: `browser_vision` also falls back to the same model — if both fail, work from character descriptions in the landing page HTML (`{WEB_ROOT}/index.html`) or bot profile HTMLs (`<HERMES_ROOT>/shared/marketing/bot-profiles/bot-profile-*.html`).

### Video Generation Prompts (Seedance / Runway / Kling)

When [REDACTED — dati personali rimossi] asks for video prompts from bot PFPs (image-to-video), the PFP IS the character reference. Prompts must describe ONLY:
- **Action/motion** — what happens in the scene
- **Camera** — push-in, pull-back, slow motion, angle
- **Environment** — dark background, charts, neon accents
- **Mood** — confident, dramatic, cinematic

Do NOT describe the character's appearance — the model sees it from the image.

**El Froggo prompt examples** (validated 2026-06-05):
```
1. "The character slowly turns to face the camera, eyes glowing bright cyan. Camera pushes in dramatically. Dark background with faint green candlestick charts rising behind."
2. "The character leans back in a chair confidently, arms behind the head. Holographic green charts and candlesticks float up around it."
3. "Close-up on the character's face. One eye lights up like a sniper scope with a cyan crosshair overlay. Camera pulls back as a green laser beam fires forward."
4. "The character walks toward camera in slow motion on a dark wet street. Green candlestick charts rise like skyscrapers in the background. Cinematic neon lighting."
5. "The character blinks, eyes glow cyan, a giant green candle shoots up behind it. The character nods once. Seamless loop, dark background."
```

**Pattern for any bot**: adapt the action/domain (trading→charts, legal→documents, cooking→flames, design→colors splashing) but keep dark backgrounds and the character's brand accent color.

## Telegram Demo Bot

When [REDACTED — dati personali rimossi] asks for a public demo bot to showcase HermesBro products:

**Location**: `<HERMES_ROOT>/shared/marketing/demo-bot/`
- `demo_bot.py` — Working bot (python-telegram-bot v21+), rate-limited (5 msg/day/user), inline keyboard menu for bot selection (ContAIbile/GROOT/LAWrenzo), simulated typing, CTA after demo
- `demo-bot-setup.md` — Full setup guide (BotFather, systemd service, venv)

**Setup steps** (manual — requires [REDACTED — dati personali rimossi] for BotFather):
1. [REDACTED — dati personali rimossi] creates bot via @BotFather → gets BOT_TOKEN
2. `cd <HERMES_ROOT>/shared/marketing/demo-bot && python3 -m venv venv && venv/bin/pip install python-telegram-bot`
3. Set `DEMO_BOT_TOKEN` env var
4. `systemctl enable --now hermes-demo-bot`

**Key design decision**: Demo bot uses CANNED responses (no LLM calls) — shows impressive pre-written conversations that demonstrate each bot's capabilities. Zero cost per interaction.

**Pitfall**: The demo bot is a THIN WRAPPER — it does NOT connect to actual Hermes bot infrastructure. It's a marketing tool, not a functional bot. If [REDACTED — dati personali rimossi] wants real bot functionality in the demo, that's a different project.

## Quality Gates

Before delivering to [REDACTED — dati personali rimossi]:
1. All HTML validates (no broken tags)
2. Mobile responsive (test at 375px width)
3. No lorem ipsum — real copy in Italian
4. No references to non-existent bots
5. **Marketing lineup (customer-facing site = 10 bots)**: ContAIbile, LAWrenzo, Wannabe, DesignBro, DUCATO, El Froggo, GROOT, Machiavelli, Sentinel, MR ROBOT. Investor deck may include GribbitO + Frank/Ratatouille (12 total).
6. Brand name: **HermesBro** (internal/landing) or **Hermes Bots** (LinkedIn company page — [REDACTED — dati personali rimossi] uses both)
7. **Pricing: 3-tier ([REDACTED — dati personali rimossi]-approved as of 2026-06)**:
   - Starter €29/mese (3 agents)
   - Pro €79/mese (7 agents) — most popular
   - Enterprise €199/mese (12 agents, white label, SLA)
   - NOTE: Tenant manager uses different pricing (€49/€119/€299) — those are internal/provisioning prices, NOT public-facing. Always use the landing page prices for marketing materials.
8. Contact email: **contact@example.com** (Proton Mail — NOT info@hermesbro.cloud)
9. Telegram: @HermesBroBot
10. URL: `hermesbro.cloud`
10. **Ribbit-style posts**: Bold openings (not questions), data-driven (specific numbers), conceptual framing ("agenti" not "bot"), series format with teasing between posts

## Anti-Fabrication Rules (MANDATORY for all marketing content)

**NEVER fabricate in LinkedIn posts, outreach, or any public content:**
- ❌ Case study inventati (ristoranti, aziende, professionisti specifici)
- ❌ Metriche inventate (engagement +240%, ROI in 3 settimane, costi tagliati del 60%)
- ❌ Numeri di performance senza fonte verificabile
- ❌ Tier di pricing non esistenti (Pro €149/mese, Enterprise €249/mese)
- ❌ Timeline inventate ("6 mesi fa ha implementato...")
- ❌ Testimonianze o citazioni fittizie

**Numeri VERIFICABILI (OK usare):**
- ✅ €49/mese (prezzo dalla landing page)
- ✅ 10 agenti specializzati
- ✅ 24/7 uptime
- ✅ 14 giorni free trial, zero carta di credito
- ✅ Feature reali di ogni bot

**Quando non hai dati reali:**
- Usa forma ipotetica ("potrebbe", "in genere", "tipicamente")
- Focalizzati su feature e capacità (non numeri)
- Confronta con alternative manuali SENZA inventare risparmi specifici

**Pitfall**: [REDACTED — dati personali rimossi] ha corretto esplicitamente i post LinkedIn perché contenevano dati fabbricati. Questa regola è NON-NEGOTIABLE.

**Pitfall**: When the bot lineup changes (new bots added), ALL existing post files in `<HERMES_ROOT>/shared/marketing/linkedin/` must be audited for stale bot counts. [REDACTED — dati personali rimossi] caught posts saying "5 bot" when there are actually 10. Search all .txt files for old counts: `grep -rn "5 bot\|cinque bot\|6 bot" <HERMES_ROOT>/shared/marketing/linkedin/`

**Pitfall — Stale post file cleanup on rewrite**: When rewriting ALL posts (e.g., to align with updated site copy), OLD files from the previous batch remain in `posts/` and get mixed with new ones. After a full rewrite, DELETE all old files that don't match the new naming convention. Use a script to identify and remove stale files:
```python
from pathlib import Path
posts_dir = Path("<HERMES_ROOT>/shared/marketing/linkedin/posts")
new_files = ["P01-slug.txt", "P02-slug.txt", ...]  # expected new names
new_set = set(new_files)
old_files = [f.name for f in posts_dir.glob("P*.txt") if f.name not in new_set]
for f in old_files:
    (posts_dir / f).unlink()
```
Also reset `published.json` tracker to `{\"published\": []}` since old entries reference deleted files. Session 2026-06-05: had 68 files (33 old + 35 new) after rewrite — auto-post script would have published old content aligned with wrong messaging.

**Pitfall — `gbrain import` slug conflict**: When gbrain import skips files with "Frontmatter slug does not match path-derived slug", the fix is to REMOVE the `slug:` line from the YAML frontmatter. gbrain auto-derives slugs from the file path. Don't try to fix the slug value — just delete the line.

**Pitfall — Never say "what should I do first?" after "fai tutto"**: When [REDACTED — dati personali rimossi] says "fai tutto" or "fai tutto quello che puoi", DO NOT ask what to prioritize. Execute ALL tasks you can. The only acceptable output after "fai tutto" is: (1) a TODO list, (2) parallel execution, (3) a summary of what was produced + what [REDACTED — dati personali rimossi] needs to do manually. [REDACTED — dati personali rimossi] explicitly corrected this: "acceso a linkedin lo hai visto che pubblichi per me tutti i giorni."

## Bot Inventory (12 bots — as of June 2026)

| Bot | Ruolo | Colore |
|-----|-------|--------|
| GribbitO | Orchestratore principale | — |
| Frank / MR ROBOT | Coding & Deploy | — |
| ContAIbile | Contabilità, fatture, bilanci | Blue |
| LAWrenzo | Legale, contratti, compliance | Purple |
| GROOT | Ristorazione, menu, prenotazioni | Green |
| Wannabe | Social media, contenuti, analytics | Orange |
| DesignBro | Grafica, loghi, brand identity | Pink |
| Ratatouille | [REDACTED — dati personali rimossi] & Ricettario | — |
| El Froggo | On-chain analytics, trading | Gold |
| DUCATO | Finanza & Investimenti | — |
| Machiavelli | Strategia & Business | Orange (#F97316) |
| Sentinel | Sicurezza infrastruttura | Red (#EF4444) |

**Pixel art PFPs**: 12 bots have pixel art in `{WEB_ROOT}/bot-profiles/pixel-*.png`.
Source copies at `<HERMES_ROOT>/shared/marketing/bot-profiles/pixel/pfp-*.png` (8 files) + `{WEB_ROOT}/bot-profiles/pixel-*.png` (12 files including Machiavelli, Sentinel, Mr Robot).

**Pitfall — Ratatouille has NO pixel art**: Only has `bot-profile-ratatouille-01.jpg` (non-pixel). Use the JPG for pitch decks that embed base64 images. For landing page pixel art sections, use a fallback or generate one.

**Pitfall — Audit before building**: Before creating ANY marketing material (pitch deck, landing page, outreach), cross-check the bot inventory against `[REDACTED — dati personali rimossi]-stack-manager` and the actual pixel art files on disk (`ls {WEB_ROOT}/bot-profiles/` and `ls <HERMES_ROOT>/shared/marketing/bot-profiles/pixel/`). [REDACTED — dati personali rimossi]'s original pitch deck said "11 Agenti" when there should be 12, and listed Ratatouille nowhere. Always verify the full lineup before starting.

## Wannabe → DesignBro Graphics Coordination

**DesignBro skill**: See `designbro-tools` skill for the full production workflow (brief → HTML → PNG → optimize → notify).

When the `graphics-check` cron job runs (Wannabe profile), it coordinates graphics production for upcoming posts.

### Workflow Pattern
1. Read content calendar from `<HERMES_ROOT>/shared/marketing/content-calendar-<month>-<year>.md`
2. Identify posts needing graphics: format = Immagine, Infografica, Quote Card
3. Check bus inbox for already-sent briefs: `<HERMES_ROOT>/shared/bus/inbox/designbro/`
4. Send new briefs via bus: `python3 <HERMES_ROOT>/shared/scripts/bus-send.py send wannabe designbro "<brief>" design`
5. Track sent briefs in `<HERMES_ROOT>/shared/marketing/graphics-tracker.md`

### Brief Format for DesignBro
```
Brief grafico: <descrizione>, formato <dimensioni>, stile <palette/tono>. Contesto: <post N, data>. Urgenza: <scadenza>.
```

**Example:**
```
Brief grafico: Card El Froggo per post LinkedIn. Sfondo scuro #1a1a2e, icona rana 🐸 con occhi stile tech, accento giallo oro #ffd60a. Testo: 'El Froggo — Il bot dietro le quinte'. Stile: dark tech, minimale, professionale. Formato LinkedIn 1080x1080. Contesto: post showcase per bot integrazioni software Hermes Bots. Urgenza: pubblicazione Mer 3 Giugno 2026.
```

### Calendar Asset Types
| Format | Asset Needed | Priority |
|--------|-------------|----------|
| Immagine | Graphic card | High |
| Infografica | Data visualization | High |
| Quote Card | Avatar + quote | Medium |
| Video | Screen recording | Manual |
| Testo | None | — |
| Sondaggio | None (LinkedIn native) | — |

### Tracking Sent Briefs
Create `<HERMES_ROOT>/shared/marketing/graphics-tracker.md` to avoid duplicate requests:
```markdown
# Graphics Tracker — <Month> <Year>

| Post | Data | Graphic | Status | Sent Date |
|------|------|---------|--------|-----------|
| #2 | Mer 3 Giugno | Card El Froggo | Sent | 2026-05-29 |
| #6 | Ven 12 Giugno | Infografica PRIMA/DOPO | Pending | — |
```

**Pitfall**: Always check `graphics-tracker.md` AND bus inbox before sending. Duplicate briefs waste DesignBro's time.

**Pitfall**: `graphics-tracker.md` is NOT auto-created. The cron job must create it on first run from the template or from the content calendar's ASSET NECESSARI section. If the file doesn't exist, assume all briefs are pending and create the tracker.

**Template**: Use `templates/graphics-tracker-giugno-2026.md` as a starting point. Copy to `<HERMES_ROOT>/shared/marketing/graphics-tracker.md` and update for the current month. The template includes a "Next Actions" section with recommended send dates.

**Reference**: See `references/wannabe-designbro-graphics-coordination.md` for the full workflow, brief structure, timing guidelines, and lessons learned.

## Cross-Sell Asset Integration Workflow

When adding a new cross-sell asset (e.g. foodcostitalia.it, a micro-site, a new product page) to LinkedIn content, update ALL FOUR artifacts:

1. **Post .txt files** (`<HERMES_ROOT>/shared/marketing/linkedin/post-*.txt`) — add asset link/reference where contextually relevant
2. **Content calendar** (`<HERMES_ROOT>/shared/marketing/brand/content-calendar.md`) — add `foodcostitalia.it: Sì/No` column per post
3. **Master copy** (`<HERMES_ROOT>/shared/marketing/linkedin/linkedin-posts.md`) — mirror all changes from .txt files
4. **Cron job prompts** (both `linkedin-content-calendar` and `Content Suggestions`) — add cross-sell section to prompt

**Current cross-sell assets:**
- `foodcostitalia.it` — micro-sito affiliato per ristoratori (guide [REDACTED — dati personali rimossi], gestionali, stampanti termiche). Link in 6/14 posts (43%). Added June 2026.

**Pitfall:** When updating URLs in post files, ALL four artifacts must use the same URL. The old VPS URL (`YOUR_VPS_HOST/hermesbro/`) was still in some files while others had `hermesbro.cloud`. Grep all artifacts after updating.

**Pitfall:** Cron job prompts are the source of truth for the automated flow. If a cross-sell section is missing from the cron prompt, the automated posts won't include it — even if the calendar says they should.

## LinkedIn Personal Profile (CV → Full Profile)

When [REDACTED — dati personali rimossi] asks to build or update his **personal LinkedIn profile**, use this workflow. This is distinct from content/post creation — it's about the profile itself (headline, about, experience, skills, languages).

### Trigger
- "profilo LinkedIn", "LinkedIn profile", "completare il profilo", "dati profilo"

### Input
- CV/resume (PDF or text) — extract with pymupdf: `python3 -c "import pymupdf; doc=pymupdf.open('CV.pdf'); [print(p.get_text()) for p in doc]"`
- Business context (from shared knowledge + current venture)

### Output — deliver ALL sections at once
1. **Headline** (max 220 chars) — role + venture + key differentiator. Bridge past career with current.
2. **About / Informazioni** (600-900 chars) — narrative arc: past experience → insight → current venture → what makes it different → CTA. No emoji, 3-4 hashtags.
3. **Experience entries** — one per significant role. Each has: title, company, dates, location, 3-5 bullet points. Current venture gets the most detail. Past roles get concise bullets focusing on transferable skills.
4. **Education** — if in CV. Skip section if no formal education (don't ask, just omit).
5. **Skills** — 8-12 relevant skills mixing: technical (AI, Python, Blockchain) + domain (Entrepreneurship, Product Development) + soft (Project Coordination, Logistics) + languages.
6. **Languages** — proficiency levels from CV.
7. **Projects** (optional) — current venture + URL.

### Style Rules
- Professional tone, zero emoji, zero decorative formatting
- Italian for Italian audience (unless CV is in another language and [REDACTED — dati personali rimossi] says otherwise)
- About section: narrative > bullet list — tell a story, don't list achievements
- Experience bullets: action verb + concrete result/context, no filler
- Headline: current role first, then differentiator, then hook

### Pitfall — Past career integration
When the CV shows a career pivot (e.g., humanitarian work → AI startup), DON'T ignore the past. Weave it into the narrative as strength: "queste competenze trasferibili mi hanno portato a..." The About section should bridge old and new careers naturally.

### Pitfall — "Ne voglio una sola"
[REDACTED — dati personali rimossi] explicitly said "Ne voglio una sola" when offered 3 headline variants. Preference: **deliver ONE well-chosen option, not multiple variants**. Pick the best approach, deliver it. If [REDACTED — dati personali rimossi] wants alternatives, he'll ask. This applies to ALL profile sections — don't offer Option A/B/C.

### Pitfall — CV language mismatch
[REDACTED — dati personali rimossi]'s CV was entirely in French (humanitarian work in Switzerland/France). The LinkedIn profile must be in Italian (his audience). Translate and adapt — don't paste French bullets directly.

## Outbound Email Campaign

Cold email campaign targeting 200 Italian businesses (40/sector) across 5 sectors: ristoranti, studi legali, e-commerce, startup, PMI. Templates at `/root/hermes-landing/outbound/templates/`.

### Sending Infrastructure
- **Provider**: SendGrid (free tier: 100 emails/day)
- **Sender email**: contact@example.com
- **Alternative**: Mailgun (100/day free) if SendGrid account issues
- **⚠️ SendGrid signup**: Cloudflare CAPTCHA blocks automated signup — [REDACTED — dati personali rimossi] must register manually. Provide credentials + steps.
- **Himalaya CLI**: Installed (`himalaya v1.2.0`) but NOT configured — needs `~/.config/himalaya/config.toml` with SMTP credentials
- **VPS limitation**: Direct SMTP from VPS is blocked by Gmail (no SPF/DKIM). Must use transactional email service.

### Contact Form API
Backend endpoint at `/api/contact` (FastAPI):
- `POST /api/contact` with JSON body: `{name, email, company, message}`
- Saves to `contacts` table in SQLite DB
- Returns `{status: "ok", message: "Messaggio ricevuto, ti contatteremo presto"}`
- Table schema: `id, name, email, company, message, created_at`

### Template Files (actual filenames)
| Sector | File | Product |
|--------|------|---------|
| Ristoranti | `ristoranti.md` | ContAIbile |
| Studi legali | `studi-legali.md` (NOT `studlegali.md`) | LAWrenzo |
| E-commerce | `e-commerce.md` | Team bot 24/7 |
| Startup | `startup.md` | Team scalabile |
| PMI generica | `pmi-generica.md` | Automazione |

Full guide: `references/outbound-email-campaign.md`

## Affiliate SEO Content (Micro-Siti)

When creating SEO articles for affiliate micro-siti (foodcostitalia.it, etc.):

**Location**: `<HERMES_ROOT>/shared/marketing/micro-siti/`

**Article template**:
1. YAML front matter (title, meta description, target keywords, author)
2. H1 with primary keyword
3. 1500+ words, H2/H3 hierarchy
4. Practical value (formulas, comparison tables, step-by-step)
5. Natural keyword placement (3-5 occurrences of primary, 2-3 secondary)
6. CTA to HermesBro product at the end (not aggressive — "Prova GROOT gratis")
7. Link to hermesbro.cloud

**Target keywords** (validated): "[REDACTED — dati personali rimossi] calcolatore online", "miglior gestionale per pizzeria", "software prenotazioni ristorante"

**Pitfall**: Articles must provide genuine value FIRST, then soft-sell. [REDACTED — dati personali rimossi] rejected articles that read like ads. The reader should learn something useful even if they never click the CTA.

**gbrain import**: After creating marketing materials, always import to gbrain for fleet-wide searchability:
```bash
export PATH="$HOME/.bun/bin:$PATH"
gbrain import <HERMES_ROOT>/shared/marketing/ --no-embed
gbrain embed --stale
```

## References

- Brand palette: see `references/brand-palette.md`
- Pre-launch content strategy (teaser campaigns): see `references/prelaunch-content-strategy.md`
- Ribbit Capital content framework: see `references/ribbit-style-content-framework.md`
- Graphics coordination workflow: see `references/wannabe-designbro-graphics-coordination.md`
- Graphics tracker template: see `templates/graphics-tracker-giugno-2026.md`
- Pricing: see [REDACTED — dati personali rimossi]-stack-manager skill
- Bot inventory: see [REDACTED — dati personali rimossi]-stack-manager skill
- Telegram groups research (70+ groups + best practices): `<HERMES_ROOT>/shared/marketing/telegram-gruppi.md`
- Demo bot code + setup guide: `<HERMES_ROOT>/shared/marketing/demo-bot/`
- SEO articles for affiliate micro-siti: `<HERMES_ROOT>/shared/marketing/micro-siti/` (food-cost-guida.md, gestionale-pizzeria-guida.md, commercialista-ai-guida.md, gestionale-ristorante-guida.md)
- Outreach tracker + partnership templates: `<HERMES_ROOT>/shared/marketing/outreach/`
- Outreach automation script: `<HERMES_ROOT>/shared/linkedin/outreach.py`
- Auto-post script: `<HERMES_ROOT>/shared/linkedin/auto-post.py`
- Post queue: `<HERMES_ROOT>/shared/marketing/linkedin/posts/` (P01-P35+ .txt files)
- Published tracker: `<HERMES_ROOT>/shared/marketing/linkedin/published.json`
- Email drip sequences: `<HERMES_ROOT>/shared/marketing/email/`
- Landing page copy per bot: `<HERMES_ROOT>/shared/marketing/landing-pages/` (6 bots)
- Competitive analysis: `<HERMES_ROOT>/shared/marketing/competitors/competitive-analysis.md`
- Press release: `<HERMES_ROOT>/shared/marketing/press-release.md`
- Referral program: `<HERMES_ROOT>/shared/marketing/referral-program.md`
- Google Business Profile: `<HERMES_ROOT>/shared/marketing/google-business-profile.md`
- LinkedIn auto-posting infrastructure (dedup-tracked): see `linkedin-content-automation` skill
- Marketing strategy: `<HERMES_ROOT>/plans/hermes-bots-marketing.md`
- Torino outreach targets: see `references/torino-outreach-targets.md`
- LinkedIn API integration: see `references/linkedin-api-integration.md`
- LinkedIn company page setup: see `references/linkedin-company-page-setup.md`
- LinkedIn company page structure (June 2026): see `references/linkedin-company-page-structure.md`
- LinkedIn OAuth pitfalls & scope restrictions: see `references/linkedin-oauth-pitfalls.md`
- Telegram photo/document sending workaround: see `references/telegram-photo-sending.md` (includes curl pattern for PDFs)
- HermesBro website structure: see `references/hermesbro-website-structure.md`
- Landing page HTML structure + image management: see `references/hermesbro-landing-page-structure.md`
- HermesBro design system (colors, logo, pfp CSS, bot roster): see `references/hermesbro-design-system.md`
- Privy + Ribbit Capital design system research: see `references/privy-ribbit-design-system.md`
- Pitch deck layout guide (overflow prevention, density rules): see `references/pitch-deck-layout-guide.md`
- Outreach automation script (batch, templates per sector): see `references/outreach-automation.md`
- LinkedIn auto-post queue (P01-P35+ pattern, published.json tracker): see `references/linkedin-auto-post-queue.md`
