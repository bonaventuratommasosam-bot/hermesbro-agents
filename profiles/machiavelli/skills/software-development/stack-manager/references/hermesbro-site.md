# HermesBro Cloud — Site Reference

**Domain:** hermesbro.cloud
**Nginx root:** `<NGINX_ROOT_DIR>/`
**Config:** `/etc/nginx/sites-enabled/hermesbro.cloud`

## File Structure

```
<NGINX_ROOT_DIR>/
├── index.html          # Main landing (owned by www-data)
├── brand.html          # Brand identity page
├── privacy-policy.html # GDPR privacy policy
├── bot-profiles/       # Bot profile HTML generators
└── img/                # Bot PFP images
    ├── contaibile.png
    ├── lawrenzo.png
    ├── wannabe.png
    ├── designbro.png
    ├── ducato.png
    ├── el-froggo.png
    ├── groot.png
    ├── hermesbro.png
    └── ratatouille.jpg  # Not used in current HTML
```

## Bot PFP Source Locations

**Pixel art (primary):** `<SHARED_DIR>/marketing/bot-profiles/pixel/`
- `pfp-contaibile.png`, `pfp-lawrenzo.png`, `pfp-wannabe.png`, `pfp-designbro.png`
- `pfp-ducato.png`, `pfp-el-froggo.png`, `pfp-groot.png`, `pfp-hermesbro.png`

**Bot profile JPGs:** `<SHARED_DIR>/marketing/bot-profiles/`

**Deploy command:**
```bash
mkdir -p <NGINX_ROOT_DIR>/img
cp <SHARED_DIR>/marketing/bot-profiles/pixel/pfp-*.png <NGINX_ROOT_DIR>/img/
# Rename: pfp-contaibile.png → contaibile.png, etc.
cd <NGINX_ROOT_DIR>/img && for f in pfp-*.png; do mv "$f" "${f#pfp-}"; done
```

## CSS Patterns for Bot Icons

### Product cards (`.product-icon`)
```css
.product-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
  flex-shrink: 0;
  position: relative;
  border: 1px solid rgba(255,255,255,0.1);
  overflow: hidden;
}
```

### Spec cards (`.spec-icon`)
```css
.spec-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid rgba(255,255,255,0.1);
  overflow: hidden;
}
```

### HTML pattern for image icons
```html
<!-- Product card -->
<div class="product-icon" style="overflow:hidden;">
  <img src="img/contaibile.png" alt="ContAIbile" style="width:100%;height:100%;object-fit:cover;border-radius:12px;">
</div>

<!-- Spec card -->
<div class="spec-icon" style="overflow:hidden;">
  <img src="img/contaibile.png" alt="ContAIbile" style="width:100%;height:100%;object-fit:cover;border-radius:12px;">
</div>
```

## Current Bot Lineup on Site

**Product cards (6):** ContAIbile, LAWrenzo, Wannabe, DesignBro, DUCATO, GROOT
**Spec cards (7):** ContAIbile, LAWrenzo, DesignBro, Wannabe, DUCATO, El Froggo, GROOT

## Editing Pitfalls

1. **File ownership**: `index.html` is `www-data:www-data`. `patch` tool edits get silently reverted. Use `sed -i` via terminal.
2. **CSS `currentColor`**: Old CSS used `border: 1px solid currentColor` which doesn't work with images. Must use `rgba(255,255,255,0.1)`.
3. **Cache**: After changes, user may need Ctrl+Shift+R (hard refresh) to see updates.
4. **Verify images**: `curl -sI https://hermesbro.cloud/img/<name>.png` should return `200 OK` with correct `Content-Type`.

## i18n Pattern (data-it / data-en)

The landing page uses `data-it` and `data-en` attributes for bilingual content. A JS lang toggle swaps `textContent` based on selected language. Always add both attributes when editing UI text.

## War Room (`/warroom/`)

Separate FastAPI app proxied through nginx. NOT part of the static site — lives at `<USER_HOME>/ai-stack/warroom/`. Uses the same `/img/*.png` bot PFPs.
