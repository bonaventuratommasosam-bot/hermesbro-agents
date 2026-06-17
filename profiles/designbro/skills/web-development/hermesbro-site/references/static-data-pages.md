# Static data pages — pattern for adding listing/catalog pages

## When to use
Adding a static page that lists data from the system (skills, agents, integrations, etc.) with client-side search and filtering. No backend needed — pure HTML+JS.

## Pattern: embedded JSON + client-side filtering

### 1. Generate data
```python
import os, json

skills_dir = "<HERMES_ROOT>/profiles/gribbito/skills"
skills = []
for root, dirs, files in os.walk(skills_dir):
    if "SKILL.md" in files:
        # Extract metadata from SKILL.md frontmatter
        skills.append({"name": ..., "category": ..., "description": ...})

with open('/tmp/data.json', 'w') as f:
    json.dump(skills, f)
```

### 2. Create HTML page
- Single file, all CSS/JS inline (no build step)
- Embed data as a JS const array: `const ITEMS = [...]`
- Client-side search: filter on name + description + category
- Category filter buttons with counts
- Responsive grid layout

### 3. Deploy
```bash
cp page.html {WEB_ROOT}/page.html
chmod 644 {WEB_ROOT}/page.html
curl -s -o /dev/null -w "%{http_code}" https://hermesbro.cloud/page.html  # expect 200
```

### 4. Add nav link
Edit index.html nav-links to include: `<a href="/page.html">PageName</a>`

## Design rules
- Use site design system (dark theme, --gold, --ink, Orbitron/Inter/JetBrains Mono)
- No emojis — SVG Lucide icons only
- Mobile responsive (grid → 1col at 640px)
- `chmod 644` mandatory — nginx runs as www-data

## Example: skills.html (130 skills, 30 categories)
- Skills embedded as `{n:"name", c:"category", d:"description"}`
- Deduplication by name (Set)
- Category metadata: icon + Italian label
- Search filters on all fields simultaneously
- Filter buttons show count per category

## Pitfall: data freshness
Static pages are snapshots. When underlying data changes, the page must be regenerated. Options:
- Manual: regenerate and redeploy when needed
- Cron: script that regenerates weekly
- Dynamic: if data changes frequently, use backend endpoint instead
