# HermesBro Website Structure

## Image Paths

- `/img/` — Bot profile images (contaibile.png, lawrenzo.png, groot.png, wannabe.png, designbro.png)
- `/bot-profiles/` — Pixel art NFT versions (pixel-contaibile.png, pixel-lawrenzo.png, etc.)

## Hero Section

Uses `/img/*.png` for bot cards with `bg-white/5 backdrop-blur-sm` styling.

## Specs Section

Uses `/bot-profiles/pixel-*.png` for smaller tech-looking images.

## Important Notes

- All images MUST be 1:1 aspect ratio (square)
- Pixel art images MUST use transparent backgrounds (RGBA)
- Non-square or white-background images look broken
- If proper images aren't available, use simple colored placeholders with the bot's first letter

## Contact Info (canonical)

- Email: **contact@example.com** (Proton Mail)
- Telegram: @HermesBroBot
- URL: hermesbro.cloud
- **Pitfall**: The original pitch deck PDF had `info@hermesbro.cloud` — this is WRONG. Always use contact@example.com. Grep all marketing materials for the old email before delivery.
