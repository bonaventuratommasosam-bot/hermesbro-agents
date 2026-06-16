# DesignBro — Example Reference (Companion Bot)

Companion bot to Wannabe Bot. Wannabe generates text content, DesignBro generates visuals.

## Personality: Fortunato Depero + Bruno Munari + Milton Glaser

- **Depero** (futurist): Bold, geometric, experimental, breaks rules. Campari, Casa d'Arte Futurista. "Basta con le linee morbide, viva la geometria!"
- **Munari** (experimentalist): Design that communicates, multidisciplinary, simplicity. "Design è arte che funziona."
- **Glaser** (iconic): Memorable design, visual communication. "Il design è la risposta a un problema di comunicazione."

## Tools (11)

1. `generate_image` — AI image gen (Flux/DALL-E) with style, aspect ratio, platform, brand colors
2. `create_social_template` — template social media con layout e brand kit
3. `create_web_image` — hero, banner, OG image, favicon, background, icon
4. `update_brand_kit` — colori, font, logo, stile
5. `get_brand_kit` — mostra brand kit corrente
6. `generate_palette` — palette colori da ispirazione/settore/mood
7. `resize_for_platform` — specifiche ridimensionamento per piattaforma
8. `create_infographic` — infografica con dati (stats, comparison, timeline, process, tips)
9. `create_mockup` — mockup (website, social feed, print, menu)
10. `design_advice` — consigli layout, typography, color, spacing, hierarchy
11. `list_designs` — design salvati filtrati per tipo/piattaforma

## Database (5 tables)

- `brand_kits` — colori, font, logo per tenant
- `designs` — design generati con metadata
- `palettes` — palette colori salvate
- `templates` — template riutilizzabili
- `brand_assets` — font, icone, texture, pattern

## Integration with Wannabe

- Same tenant_id across both bots
- API endpoints: `POST /api/generate-image`, `GET /api/brand-kit/{tenant_id}`, `POST /api/create-social-image`
- Wannabe calls DesignBro when posts need visuals
- Brand kit in DesignBro = single source of truth for visual identity

## Port: 8094

## [REDACTED — dati personali rimossi]'s Design Preferences

- Fortunato Depero was [REDACTED — dati personali rimossi]'s specific choice (replacing Massimo Vignelli)
- [REDACTED — dati personali rimossi] values Italian cultural references in bot personalities
- Dark theme dashboard (consistent with all bots)
