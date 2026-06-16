## Bot Accent Colors Reference (updated)

| Bot | Color | Hex | RGB |
|-----|-------|-----|-----|
| ContAIbile | Ocean Blue | `#3a86ff` | 58,134,255 |
| LAWrenzo | Royal Purple | `#8338ec` | 131,56,236 |
| GROOT | Forest Green | `#06d6a0` | 6,214,160 |
| Wannabe | Vibrant Orange | `#ff9f1c` | 255,159,28 |
| DesignBro | Hot Magenta | `#ff006e` | 255,0,110 |
| El Froggo | Cyan | `#22d3ee` | 34,211,238 |
| DUCATO | Gold | `#d4a853` | 212,168,83 |
| Sentinel | Red | `#EF4444` | 239,68,68 |
| Machiavelli | Indigo | `#6366f1` | 99,102,241 |
| HermesBro | Gold | `#d4a853` | 212,168,83 |
| Trust Blue | (links/CTA) | `#2563eb` | 37,99,235 |

## Landing Page Structure (hermesbro-landing.html)

The landing page uses `spec-card` (not `product-card`) for bot cards. Structure:
```html
<div class="spec-card reveal" style="border-top: 2px solid BOT_COLOR;">
  <div class="spec-header">
    <img src="/bot-profiles/pixel-BOTNAME.png" alt="BOTNAME" class="spec-icon">
    <div>
      <h3>BOTNAME</h3>
      <span class="spec-badge">Sector</span>
    </div>
  </div>
  <div class="spec-stats">
    <div><div class="spec-stat-val">N</div><div class="spec-stat-label">Tools</div></div>
    ...
  </div>
  <ul class="spec-tools">
    <li data-it="Italiano" data-en="English">Italiano</li>
    ...
  </ul>
</div>
```

The page is bilingual (IT/EN) using `data-it` and `data-en` attributes.
