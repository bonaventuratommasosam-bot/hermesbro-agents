# Agent Profile Page Generator

Batch-generates individual agent profile pages for `hermesbro.cloud/agents/`.

## How to use

Run the generator script at `/tmp/gen_agent_pages.py` (or copy to a permanent location). It reads agent data from a Python dict and writes HTML files to `{WEB_ROOT}/agents/`.

## Agent data structure

Each agent entry requires:

```python
{
    "slug": "contaibile",           # URL slug → agents/{slug}.html
    "name": "ContAIbile",           # Display name
    "tagline": "Il Commercialista AI",  # Short tagline
    "category": "Contabilita",      # Category label
    "cat_color": "#10B981",         # Accent color (hex)
    "status": "active",             # active | coming | pro
    "status_label_it": "Attivo",
    "status_label_en": "Active",
    "pfp": "/bot-profiles/pixel-contaibile.png",  # PFP path
    "description_it": "...",        # Full description (IT)
    "description_en": "...",        # Full description (EN)
    "personalities": [              # 3 personality archetypes
        {
            "name": "Luca Pacioli",
            "role_it": "La Precisione",
            "role_en": "Precision",
            "desc_it": "...",
            "desc_en": "..."
        },
        # ... 2 more
    ],
    "capabilities_it": ["Fatturazione...", ...],  # 6-8 capabilities
    "capabilities_en": ["Invoicing...", ...],
    "tools": 33,                    # Tool count (stat card)
    "tech": ["Python", "SQLite", "Telegram Bot API"],  # Tech badges
}
```

## Personality sourcing

Personality data comes from each bot's SOUL.md at `<HERMES_ROOT>/profiles/{name}/SOUL.md`. Look for the `## PERSONALITÀ` or `## Chi Sono` section with the 3 archetypes.

## Adding a new agent page

1. Add agent data dict to the `AGENTS` list in the generator
2. Run: `python3 /tmp/gen_agent_pages.py`
3. Fix permissions: `chmod 644 {WEB_ROOT}/agents/*.html`
4. Update index.html "Vedi agente" link: `href="/agents/{slug}.html"`
5. Verify: `curl -s -o /dev/null -w "%{http_code}" https://hermesbro.cloud/agents/{slug}.html`

## Regenerating all pages

```bash
python3 /tmp/gen_agent_pages.py
chmod 644 {WEB_ROOT}/agents/*.html
# Verify all return 200
for f in {WEB_ROOT}/agents/*.html; do
  name=$(basename "$f" .html)
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://hermesbro.cloud/agents/${name}.html")
  echo "$name: $code"
done
```

## Current agent slugs (as of 2026-06-03)

| Slug | Name | Status | Color |
|------|------|--------|-------|
| contaibile | ContAIbile | active | #10B981 |
| lawrenzo | LAWrenzo | coming | #6366f1 |
| wannabe | Wannabe | coming | #ec4899 |
| designbro | DesignBro | coming | #8b5cf6 |
| ducato | DUCATO | coming | #f59e0b |
| el-froggo | El Froggo | coming | #22c55e |
| groot | GROOT | coming | #ef4444 |
| machiavelli | Machiavelli | coming | #d4a853 |
| sentinel | Sentinel | coming | #06b6d4 |
| mr-robot | MR.ROBOT | pro | #e11d48 |
