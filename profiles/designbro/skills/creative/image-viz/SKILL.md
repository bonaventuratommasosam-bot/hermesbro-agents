---
name: image-viz
description: >-
  Visualize and analyze images for design work. Uses vision_analyze to inspect
  photos, screenshots, mockups, brand references, and design assets. Extracts
  color palettes, critiques layouts, reads typography, identifies visual issues,
  and provides actionable design feedback. For DesignBro: the "eye" that sees
  what the client sends.
version: 1.0.0
author: gribbito
license: MIT
tags:
  - vision
  - image-analysis
  - design-critique
  - color-palette
  - layout
  - visual-inspection
metadata:
  hermes:
    tags: [vision, image-analysis, design, creative]
    category: creative
---

# Image Visualization — DesignBro's Eye

When a client sends an image (photo, screenshot, mockup, logo, reference),
this skill teaches you how to analyze it properly using `vision_analyze`.

## When to Use

- Client sends an image in chat (photo, screenshot, mockup, logo)
- Need to inspect a design reference before recreating it
- Need to extract colors, fonts, layout structure from an image
- Need to critique a design before suggesting improvements
- Need to analyze a screenshot of a website or app

## Tool: vision_analyze

```
vision_analyze(image_url="<path_or_url>", question="<specific question>")
```

- `image_url`: local file path, URL, or data: URL
- `question`: be SPECIFIC — don't just say "describe this image"

## How to Analyze Images (Design Workflow)

### 1. First Look — General Scan
```
vision_analyze(image_url="...", question="Describe the overall layout, color scheme, typography, and visual hierarchy of this design. What is the first thing your eye is drawn to?")
```

### 2. Color Palette Extraction
```
vision_analyze(image_url="...", question="Extract the exact hex color codes used in this design. List the primary, secondary, accent, and background colors. Note any gradients.")
```

### 3. Typography Analysis
```
vision_analyze(image_url="...", question="Identify all fonts/typefaces used. Describe the hierarchy (headings, body, captions). Note weights, sizes, and any decorative treatments.")
```

### 4. Layout and Composition
```
vision_analyze(image_url="...", question="Analyze the grid structure, spacing, alignment, and visual flow. Where does the eye go first, second, third? Is there a clear focal point?")
```

### 5. Brand Consistency Check
```
vision_analyze(image_url="...", question="Compare this design against the brand guidelines: [paste brand colors/fonts]. Are there deviations? What does not match?")
```

### 6. Screenshot Analysis (Web/App)
```
vision_analyze(image_url="...", question="Analyze this UI screenshot: identify the layout pattern, navigation structure, CTAs, spacing issues, and any UX problems visible.")
```

### 7. Image Quality Check
```
vision_analyze(image_url="...", question="Check this image for quality issues: pixelation, compression artifacts, misalignment, color banding, or low resolution areas.")
```

## Response Format (Design Critique)

When analyzing an image for a client, structure your response:

- **Cosa vedo:** One-sentence summary
- **Palette:** Primario (hex), Secondario (hex), Accento (hex)
- **Layout:** Grid, spacing, alignment observations
- **Tipografia:** Font hierarchy, readability, pairing
- **Problemi:** Issue 1 with specific fix, Issue 2 with specific fix
- **Suggerimenti:** Actionable improvement 1, Actionable improvement 2

## Pitfalls

- **Vision model required.** `vision_analyze` returns 404 if the current model/provider doesn't support image input. If you get `Error code: 404 - No endpoints found that support image input`, the model has no vision capability. **Fix: configure auxiliary vision with a free provider.** The fastest fix:
  ```bash
  # Use OpenRouter (free tier) with Gemini Flash for vision
  hermes config set auxiliary.vision.provider openrouter
  hermes config set auxiliary.vision.base_url "<OPENROUTER_URL>"
  hermes config set auxiliary.vision.api_key "$OPENROUTER_API_KEY"  # from main .env
  hermes config set auxiliary.vision.model "google/gemini-2.0-flash-001"
  ```
  This works even when the main model has no vision (e.g. Xiaomi MiMo). The auxiliary vision config is independent — main model stays unchanged. Other free vision providers: Google AI Studio (Gemini), NVIDIA NIM, Mistral (La Plateforme). See `references/vision-providers.md` for the full list. Do NOT silently skip analysis — tell the user why you can't see the image and fix the config.
- **Don't ask "what do you want me to do with this image?"** — analyze it immediately and present findings. DesignBro proposes, doesn't ask.
- **Don't be vague** — "nice colors" is useless. Extract hex codes, name the color, explain why it works.
- **Multiple passes** — for complex images, call vision_analyze multiple times with different questions (one for colors, one for layout, etc.)
- **Local files** — when the client sends a file via Telegram, it arrives as a local path. Use the path directly.
- **URLs** — when given a URL, use it directly. Don't download first.
- **Screenshots vs photos** — adjust your question based on context. A screenshot needs UI analysis; a photo needs composition analysis.
- **Always provide actionable feedback** — "the blue doesn't work" is bad. "Sostituisci il #1a73e8 con un #0d47a1 piu scuro per migliorare il contrasto sul bianco" is good.
