# Free Vision-Capable LLM Providers (May 2026)

## Providers with Free Vision API Access

### 1. OpenRouter (already configured in designbro)
- **Model:** `google/gemini-2.0-flash-001` (free, vision native)
- **Base URL:** `<OPENROUTER_URL>
- **Auth:** `OPENROUTER_API_KEY` from `~/.hermes/.env`
- **Limits:** Free tier, prompts may be logged
- **Setup:** `hermes config set auxiliary.vision.provider openrouter`

### 2. Google AI Studio (Gemini)
- **Models:** `gemini-2.0-flash`, `gemini-2.5-flash` (free, vision native)
- **Base URL:** `https://generativelanguage.googleapis.com/v1beta`
- **Auth:** API key from https://aistudio.google.com/apikey
- **Limits:** Generous free tier, no credit card required

### 3. NVIDIA NIM
- **Model:** `nemotron-3-super` (120B params, vision capable)
- **Auth:** API key from https://build.nvidia.com
- **Limits:** Free tier available

### 4. Mistral (La Plateforme)
- **Models:** `mistral-small` (vision capable)
- **Auth:** API key from https://console.mistral.ai
- **Limits:** Free tier with rate limits

## How Auxiliary Vision Works

The `auxiliary.vision` config in Hermes is INDEPENDENT of the main model config.
When `vision_analyze()` is called, it uses the auxiliary vision provider instead of
the main model. This means:
- Main model can be non-vision (e.g. Xiaomi MiMo v2.5 Pro)
- Vision calls go to the auxiliary provider (e.g. OpenRouter + Gemini Flash)
- No model switching needed — both run simultaneously

## Configuration Commands

```bash
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.base_url "<OPENROUTER_URL>"
hermes config set auxiliary.vision.api_key "sk-or-..."
hermes config set auxiliary.vision.model "google/gemini-2.0-flash-001"
```

Verify with:
```bash
hermes config get auxiliary.vision
```
