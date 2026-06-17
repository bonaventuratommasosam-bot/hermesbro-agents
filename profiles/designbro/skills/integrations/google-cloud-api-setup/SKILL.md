---
name: google-cloud-api-setup
description: "Set up Google Cloud APIs (Gemini/Vertex AI, etc.) for bot integration. Covers API key auth, service accounts, common blockers, and Python SDK setup."
version: 1.0
tags: [gcp, google-cloud, gemini, vertex-ai, api, python, ai]
related_skills: [hermesbro-site, [REDACTED — dati personali rimossi]-stack-manager]
---

# Google Cloud API Setup

## When to use
- Enabling GCP APIs for bot integrations (Gemini, Vertex AI, Cloud Run, etc.)
- Setting up API keys or service account credentials on the VPS
- Troubleshooting GCP API permission errors
- Configuring Python SDKs for Google Cloud services

## Project context
- **GCP Project**: ratatouille-app (ID: `ratatouille-app-497213`, number: `528018243613`)
- **Credits**: 257€, valid until August 24, 2026
|- **Key owner**: [Nome Cliente] (French GCP console locale)
- **gcloud CLI**: installed at `/usr/bin/gcloud` (SDK 570.0.0)

## Gemini API setup (Google AI Studio key)

### Quick setup
```bash
pip3 install --break-system-packages google-genai
```

```python
from google import genai
client = genai.Client(api_key='YOUR_API_KEY')
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Hello'
)
print(response.text)
```

### Direct curl test
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=YOUR_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Ciao"}]}]}'
```

## Common errors and fixes

### 403 `API_KEY_SERVICE_BLOCKED`
**Cause**: The key is an **AI Studio key** (`AQ.` prefix), NOT a GCP API key. AI Studio keys cannot consume GCP project credits — they're tied to AI Studio's free tier, not the GCP billing account.

**How to tell the difference**:
- `AQ.Ab...` → AI Studio key (wrong for GCP credits)
- `AIzaSy...` → GCP Console key (correct for GCP credits)

**Fix**:
1. Go to: `https://console.cloud.google.com/apis/credentials?project=PROJECT_ID`
2. Click **"+ CREA CREDENZIALI" → "Chiave API"**
3. The new key starts with `AIza...` — use THIS one
4. Also ensure Generative Language API is enabled in the project

**Note**: API key restrictions in the GCP Console are a SEPARATE issue. The `API_KEY_SERVICE_BLOCKED` error with an `AQ.` key specifically means the key type is wrong for GCP project billing.

### 403 `PERMISSION_DENIED` (no service_blocked detail)
**Cause**: The Generative Language API is not enabled in the project.

**Fix**:
1. Go to: `https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com?project=PROJECT_ID`
2. Click "Abilita" / "Enable"
3. Wait 1-2 minutes for propagation

### 404 on Vertex AI endpoints
**Cause**: Vertex AI API not enabled, or using wrong endpoint (AI Studio vs Vertex).

**AI Studio key** → uses `generativelanguage.googleapis.com`
**Vertex AI** → uses `REGION-aiplatform.googleapis.com`

## API key vs Service Account

| Method | Use case | Setup |
|--------|----------|-------|
| API Key | Quick Gemini API access | Console → Credenziali → Create API Key |
| Service Account | Vertex AI, Cloud Run, full GCP access | Console → IAM → Service Accounts → Create → Download JSON |

### Service account setup (for Vertex AI / full access)
1. IAM & Admin → Service Accounts → "Crea account servizio"
2. Name: `hermes-bots`
3. Role: `Vertex AI User`
4. Create key → JSON → Download
5. Upload to VPS, set env var: `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`

## Gemini OpenAI-Compatible Endpoint (drop-in replacement)

Gemini has a native OpenAI-compatible endpoint — NO SDK needed, works with any OpenAI client:

```
Base URL: https://generativelanguage.googleapis.com/v1beta/openai
Auth: Bearer <GEMINI_API_KEY>  (same key, different endpoint)
Model: gemini-2.5-flash, gemini-3-flash-preview, etc.
```

**curl test**:
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" \
  -H "Authorization: Bearer $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-2.5-flash","messages":[{"role":"user","content":"Ciao"}],"max_tokens":50}'
```

**Python (httpx)**:
```python
r = await client.post(
    "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
    json={"model": "gemini-2.5-flash", "messages": q, "tools": TOOLS, "max_tokens": T},
    headers={"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
)
```

**Use case**: Fallback LLM for any OpenAI-compatible bot. Swap only the base_url + api_key, keep all other code identical. Supports tool calling, streaming, function calling — same schema as OpenAI.

**Tested**: 2026-06-03 on VPS. Works with both `AQ.` AI Studio keys and GCP keys.

## Gemini key rotation workflow

When Gemini returns errors or the gateway falls back to another model:

1. **Check the key in .env** — it may be truncated or stale:
   ```bash
   grep GEMINI_API_KEY <HERMES_ROOT>/profiles/<profile>/.env
   ```
   A valid AI Studio key is ~53 chars starting with `AQ.Ab`.

2. **Replace with sed** (never hand-edit .env):
   ```bash
   sed -i 's|^GEMINI_API_KEY=.*|GEMINI_API_KEY=<new_key>|' <HERMES_ROOT>/profiles/<profile>/.env
   ```

3. **Test with curl before restarting**:
   ```bash
   GEMINI_KEY=$(grep '^GEMINI_API_KEY=' <HERMES_ROOT>/profiles/<profile>/.env | cut -d= -f2)
   curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_KEY}" \
     -H 'Content-Type: application/json' \
     -d '{"contents":[{"parts":[{"text":"hi"}]}]}'
   ```
   Expect a JSON response with `candidates[0].content.parts[0].text`.

4. **Restart gateway** — MUST be done from a shell OUTSIDE the running gateway:
   ```bash
   hermes gateway restart
   ```
   ⚠️ Running `hermes gateway restart` from inside the gateway gives:
   "Refusing to restart the gateway from inside the gateway process."
   [REDACTED — dati personali rimossi] must run this from a separate SSH session, or via the PC bridge.

## Pitfalls

- **AI Studio keys (`AQ.`) vs GCP keys (`AIzaSy.`)**: They are DIFFERENT systems. `AQ.` keys work with AI Studio's free tier only. To consume GCP project credits (257€ on ratatouille-app), you MUST create a key from GCP Console → Credenziali → "Chiave API" (starts with `AIzaSy.`). This is the #1 gotcha when setting up Gemini.
- **API key propagation**: After enabling an API, wait 1-2 min before testing. First call may fail with 403.
- **`curl -sI` on GCP endpoints**: Returns 405 for HEAD. Use `curl -s -o /dev/null -w "%{http_code}" URL` for status checks.
- **Generative Language API must be enabled**: Even with a correct GCP API key, `generativelanguage.googleapis.com` must be explicitly enabled in the project. Link: `https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com?project=PROJECT_ID`
- **Project locale**: [REDACTED — dati personali rimossi]'s GCP console may be in French. "Abilita" = "Enable", "Credenziali" = "Credentials".
- **gcloud CLI auth mismatch**: The VPS gcloud may be authenticated as a different service account (e.g. neon-nexus project). `gcloud services list --project=ratatouille-app` may fail with permission denied. Use the GCP Console web UI for API management instead.
- **Python SDK**: Use `google-genai` package (new unified SDK), NOT the older `google-generativeai`. Already installed at `<PYTHON_LIB>/google/genai/`.
- **Free tier vs credits**: Gemini API via AI Studio has a generous free tier. GCP credits are consumed via Vertex AI usage. For [REDACTED — dati personali rimossi]'s bots, AI Studio keys are fine for dev/testing; GCP keys are needed when he wants to burn credits.
- **`AQ.` keys CAN work**: Despite the pitfall above, AI Studio keys (`AQ.` prefix) DO work with `generativelanguage.googleapis.com` once the API is enabled in the project. The `API_KEY_SERVICE_BLOCKED` error means the API isn't enabled OR the key has project-level restrictions — not necessarily that the key type is wrong. If the key was created from within the GCP project's AI Studio page, it IS linked to that project and can consume credits.
- **OAuth Client ID is NOT an API key**: `528018243613-...apps.googleusercontent.com` format is an OAuth Client ID, not an API key. Cannot be used for direct API calls. The user may confuse these when copying from the console.

## Gemini OpenAI-compatible endpoint (critical for integration)

Gemini has a **native OpenAI-compatible endpoint** — no SDK needed, just swap the base URL:

```
Base URL: https://generativelanguage.googleapis.com/v1beta/openai
Auth: Bearer <API_KEY> (same AI Studio key that starts with AQ.)
```

**Test with curl**:
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-2.5-flash","messages":[{"role":"user","content":"Ciao"}],"max_tokens":50}'
```

**Why this matters**: Any code that uses OpenAI-compatible API calls (httpx to `/chat/completions`) can switch to Gemini by just changing `base_url` + `api_key`. No SDK migration needed. This is how the gold bots integrate Gemini as fallback.

**For Hermes Agent config.yaml**:
```yaml
model:
  default: gemini-2.5-flash
  provider: custom
  base_url: https://generativelanguage.googleapis.com/v1beta/openai
  api_key: $GEMINI_API_KEY
  api_mode: openai
```

## Model availability (tested with AI Studio key, June 2026)

| Model | Status | Notes |
|-------|--------|-------|
| `gemini-2.5-flash` | ✅ Works | Primary workhorse, fast + cheap |
| `gemini-3-flash-preview` | ✅ Works | New generation, higher token count per response |
| `gemini-2.5-flash-lite` | ✅ Works | Ultra-light for simple tasks |
| `gemini-2.5-flash-image` | ✅ Available | Image generation |
| `gemini-2.5-flash-preview-tts` | ✅ Available | Text-to-speech |
| `gemini-3-pro-preview` | ✅ Available | New generation Pro |
| `gemini-2.5-pro` | ⚠️ Needs billing | Returns "API key expired" without active billing |
| `gemini-2.0-flash` | ✅ Works | Previous generation |

**To list models programmatically**:
```python
from google import genai
client = genai.Client(api_key='YOUR_KEY')
for m in client.models.list():
    if 'gemini' in m.name.lower():
        print(m.name)
```

## Key creation confusion matrix

| Format | What it is | Use for API calls? |
|--------|-----------|-------------------|
| `AIzaSy...` | GCP API Key | ✅ Yes |
| `AQ.Ab...` | AI Studio Key | ✅ Yes (if API enabled) |
| `52801...apps.googleusercontent.com` | OAuth Client ID | ❌ No — needs OAuth flow |
| Service account JSON | Service account credentials | ✅ Yes (via ADC) |

## User workflow preference ([REDACTED — dati personali rimossi])
- [REDACTED — dati personali rimossi]'s GCP console is in **French** — expect French UI labels
- When setting up APIs, prefer step-by-step console links over CLI commands (gcloud auth on VPS may be a different account)
- Give exact URLs with `?project=PROJECT_ID` for direct navigation
