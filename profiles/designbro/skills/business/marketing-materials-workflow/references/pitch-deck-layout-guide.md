# Pitch Deck Layout Guide — HermesBro

## Slide Dimensions
- **Format**: A4 Landscape = 297mm × 210mm
- **Break**: `page-break-after: always` on every `.slide`
- **Overflow**: `overflow: hidden` on `.slide` to prevent spill into next page

## Common Overflow Problems

### Pricing Cards (Slide 8)
The 3-tier pricing card layout is the #1 overflow offender. Solutions:
- Use `font-size: 12px` for bullet lists (not 14px)
- Reduce card padding to `16px 12px`
- Limit bullets to 5-6 per tier
- If still overflowing: split "Business Model" and "Pricing" into 2 slides
- Use `max-height: 180px` with `overflow: hidden` on card body as safety net

### Bot Grid (Slides 4-5)
6+ bot cards per slide. Solutions:
- Split into Flotta 1/2 (8 + 4 cards)
- Card width: ~130px max for 6-column grid
- Use `font-size: 11px` for bot descriptions
- Remove long descriptions — just name + 4-word tag

### Bullet Lists
Long bullet lists (8+ items) overflow. Solutions:
- Max 6 bullets per section
- Use 2-column layout for dense content
- Cut verbose bullets to 1-line each

## Content Density Rules
1. **One main idea per slide** — don't combine unrelated topics
2. **Max 4 card/grid items per row** — prefer 2-3 columns
3. **Max 6 bullet points per section** — cut or split
4. **Font sizes**: Title 24-28px, Body 13-14px, Labels 10-11px, Small 9-10px
5. **Padding**: 50-60px on slide container, 16-20px on cards
6. **Test**: Open the PDF and visually verify every slide — no content cut off at bottom or right edge

## PDF Generation Command
```bash
wkhtmltopdf --orientation Landscape --page-size A4 --no-stop-slow-scripts \
  --enable-local-file-access --margin-top 0 --margin-bottom 0 \
  --margin-left 0 --margin-right 0 \
  /root/hermesbro-pitch-deck.html /root/hermesbro-pitch-deck.pdf
```

## Post-Generation Verification
```bash
# Check page count (should match expected slide count)
pdfinfo /root/hermesbro-pitch-deck.pdf | grep Pages

# Quick visual check — open in browser or send to [REDACTED — dati personali rimossi]
```

## Slide Template (minimal)
```html
<div class="slide" style="width: 297mm; height: 210mm; page-break-after: always; overflow: hidden; padding: 50px 60px; box-sizing: border-box;">
  <!-- Slide content here -->
</div>
```
