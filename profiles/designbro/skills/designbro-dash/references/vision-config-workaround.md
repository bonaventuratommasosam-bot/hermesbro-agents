# Vision Configuration for Image Analysis

## Problem
The default Xiaomi mimo model (`XIAOMI_BASE_URL` / `XIAOMI_API_KEY`) does NOT support vision/image input. `vision_analyze` returns 404: "No endpoints found that support image input".

## Solution
Use OpenRouter + a vision-capable model instead:

```bash
# Read keys from main .env (NOT the profile .env)
ORKEY=$(grep OPENROUTER_API_KEY <HERMES_ROOT>/.env | cut -d= -f2-)

hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model google/gemini-2.0-flash-lite-001
hermes config set auxiliary.vision.api_key "$ORKEY"
hermes config set auxiliary.vision.base_url "<OPENROUTER_URL>"
```

## Verified Working Config (May 2026)
- **Provider:** openrouter
- **Model:** google/gemini-2.0-flash-001 ← use this, NOT flash-lite (404)
- **Base URL:** <OPENROUTER_URL>
- **API Key:** OpenRouter key from `<HERMES_ROOT>/.env` (not the profile .env)

## Pitfalls
- The OpenRouter key lives in `<HERMES_ROOT>/.env` (main config), not in `<HERMES_ROOT>/profiles/designbro/.env`. Always grep the main .env.
- Don't forget to set `base_url` — if it's still pointing to the Xiaomi gateway, OpenRouter models will be rejected with "Unsupported model for xiaomi-mimo".
- The Xiaomi mimo model works fine as the main chat model; only vision needs the OpenRouter override.
- **Model choice matters:** `google/gemini-2.0-flash-lite-001` returns 404 ("No endpoints found that support image input"). Use `google/gemini-2.0-flash-001` instead — confirmed working May 2026.
