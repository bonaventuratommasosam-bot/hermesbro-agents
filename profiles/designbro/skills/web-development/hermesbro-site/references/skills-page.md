# skills.html — static skills listing page

## Overview
Client-side rendered page listing all 130+ Hermes fleet skills. Embedded JSON array, category filters, text search, IT/EN toggle.

## Location
`{WEB_ROOT}/skills.html`

## Data structure
```js
const SKILLS = [
  {n:"skill-name", c:"category", d:"Short description."},
  ...
];
```
- `n`: skill name (kebab-case, matches directory name)
- `c`: category slug (e.g. "devops", "creative", "software-development")
- `d`: one-line description

## Category metadata
```js
const CAT_META = {
  "devops": {icon:"", label:"DevOps"},
  "creative": {icon:"", label:"Creatività"},
  // ...
};
```
Icons are empty strings (text-only labels in filter buttons).

## Features
- Deduplication by name (Set-based)
- Category filter buttons with counts
- Text search across name + description + category
- IT/EN language toggle (localStorage persistence)
- Responsive grid (320px min, 1col at 640px)
- Dark theme matching site design system

## Navbar
MINIMAL: Home + Skills + IT/EN toggle only. NO Agenti, NO Prova Gratis (<FOUNDER>'s explicit preference).

## Title
"I superpoteri dei tuoi agenti" / "Your agents' superpowers" — NOT "Le Superpotenze" (<FOUNDER> corrected this).

## Regeneration
When skills change, regenerate the SKILLS array:
```python
import os, re
skills_dir = "<HERMES_ROOT>/profiles/gribbito/skills"
skills = []
for root, dirs, files in os.walk(skills_dir):
    if "SKILL.md" in files:
        cat = os.path.relpath(root, skills_dir).split("/")[0]
        # Extract name + description from frontmatter
        ...
```
Then patch the SKILLS array in skills.html.

## Landing page integration
- Nav link: `<a href="/skills.html">Skill</a>` in index.html navbar (between Agenti and Prezzi)
- CTA section after agenti grid: "130+ skill. Un ecosistema in crescita." with gold button "Esplora tutte le skill →"
