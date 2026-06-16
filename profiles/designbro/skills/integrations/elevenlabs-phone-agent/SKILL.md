---
name: elevenlabs-phone-agent
description: "Connect ElevenLabs ElevenAgents to Hermes Agent — bot answers phone calls via voice. Architecture, setup, config, and HermesBro integration."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [voice, telephony, elevenlabs, hermesbro, integrations]
    related_skills: [voice-mode, tts, hermesbro-site]
---

# ElevenLabs Phone Agent + Hermes

Connect ElevenLabs ElevenAgents to Hermes Agent so the bot can answer phone calls. Clients call a phone number and talk to their AI assistant naturally.

## When to Use

- Client wants voice interaction with their bot (phone call, not just Telegram)
- HermesBro premium feature: "call your bot"
- Any use case where the user is away from the screen but needs the bot

## Architecture

```
Phone Call → ElevenLabs (telephony + TTS + STT) → POST /v1/chat/completions → Hermes Agent (tools + memory + skills)
```

**ElevenLabs handles:**
- Phone number provisioning (SIP/Twilio)
- Turn-taking (VAD, interruption detection)
- Speech-to-text (Whisper-class)
- Text-to-speech (ElevenLabs voices)
- Call recording, analytics

**Hermes handles:**
- LLM reasoning (any provider)
- Tools (food cost calculator, invoice generator, etc.)
- Memory (conversation history, client context)
- Skills (sector-specific knowledge)

**Protocol:** OpenAI-compatible `POST /v1/chat/completions`
ElevenLabs sends each conversation turn to Hermes as a chat completion request. Hermes responds with the assistant message. ElevenLabs speaks it back.

## Prerequisites

1. **ElevenLabs account** — https://elevenlabs.io (free tier available)
2. **ElevenLabs API key** — Settings → API Keys
3. **ElevenAgents** — enabled in ElevenLabs dashboard
4. **Hermes Agent running** — with gateway accessible from internet
5. **Public URL** — ElevenLabs needs to reach Hermes endpoint (already have: hermesbro.cloud)

## Setup Steps

### Step 1: Get ElevenLabs API Key

1. Go to https://elevenlabs.io → Sign up / Login
2. Settings → API Keys → Create API Key
3. Copy the key

### Step 2: Add to Hermes .env

```bash
# Add to <HERMES_ROOT>/profiles/gribbito/.env (or tenant profile)
ELEVENLABS_API_KEY=your_key_here
```

### Step 3: Install Voice Dependencies

```bash
pip install "hermes-agent[tts-premium]"
# This installs the elevenlabs Python package

# System deps (if not already installed)
sudo apt install -y portaudio19-dev ffmpeg libopus0
```

### Step 4: Configure ElevenLabs Agent

In ElevenLabs dashboard:
1. Go to "Agents" → Create New Agent
2. Set the LLM provider to "Custom API" or "OpenAI-compatible"
3. Set the endpoint URL to: `https://hermesbro.cloud/v1/chat/completions`
   - OR for a specific tenant bot: the Hermes gateway URL for that profile
4. Set the API key (can be a dummy key if Hermes doesn't require auth on that endpoint)
5. Configure the voice, language (Italian), and system prompt
6. Assign a phone number (ElevenLabs provides via SIP/Twilio)

### Step 5: Expose Hermes Chat Completion Endpoint

Hermes Agent exposes `/v1/chat/completions` when running as gateway. Verify:

```bash
# Check if the endpoint is accessible
curl -s https://hermesbro.cloud/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4","messages":[{"role":"user","content":"ciao"}]}' | head -50
```

If the endpoint doesn't exist on the multitenant backend, we need to add a proxy:
- nginx forwards `/v1/chat/completions` to the correct Hermes gateway port
- OR we add a FastAPI route in the multitenant backend that proxies to the tenant's Hermes

### Step 6: Test

1. Call the ElevenLabs phone number
2. Speak: "Ciao, chi sei?"
3. Bot should respond with its persona
4. Test with a tool call: "Calcola il food cost della margherita"

## HermesBro Integration

### Premium Feature: "Call Your Bot"

Add to pricing:
- **Starter €29/mese**: Telegram bot only
- **Pro €79/mese**: Telegram + WhatsApp + Voice (100 min/mese)
- **Enterprise €199/mese**: All channels + unlimited voice

### Implementation per Tenant

Each tenant gets:
1. Their own ElevenLabs agent (or shared with sector-specific prompt)
2. Phone number (ElevenLabs provides, or bring your own via SIP)
3. Voice persona matching their sector (Italian, professional for ContAIbile, friendly for GROOT)

### Tenant Provisioning Update

Add to `hermesbro_multitenant_backend.py`:

```python
def provision_voice_for_tenant(tenant_id: str, sector: str):
    """Provision ElevenLabs voice agent for a tenant."""
    # 1. Create ElevenLabs agent via API
    # 2. Configure endpoint to point to tenant's Hermes gateway
    # 3. Set voice and language based on sector
    # 4. Save phone number to tenant record
    # 5. Update dashboard with voice status
```

ElevenLabs API for agent management:
```bash
# Create agent
curl -X POST "https://api.elevenlabs.io/v1/convai/agents" \
  -H "xi-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ContAIbile - Pizzeria Da Marco",
    "conversation_config": {
      "agent": {
        "language": "it",
        "prompt": "Sei ContAIbile, assistente contabile AI..."
      },
      "llm": {
        "type": "custom_llm",
        "url": "https://hermesbro.cloud/api/tenant/TENANT_ID/v1/chat/completions",
        "model": "gpt-4"
      }
    }
  }'
```

### Nginx Route for Tenant Voice

```nginx
# /api/tenant/{id}/v1/chat/completions → tenant's Hermes gateway
location ~ ^/api/tenant/([a-f0-9-]+)/v1/chat/completions {
    # Look up tenant's Hermes port from DB or profile
    proxy_pass http://127.0.0.1:PORT;
    proxy_set_header Host $host;
    proxy_read_timeout 300s;
    proxy_buffering off;
}
```

## Pitfalls

- **Latency**: Phone calls need < 500ms response time. Hermes + LLM must be fast. Use streaming responses.
- **Italian voices**: ElevenLabs has good Italian voices. Test a few: "Matilde", "Antonio", "Giuseppe".
- **Cost**: ElevenLabs charges per character. Free tier = 10,000 chars/mese. Paid = ~$5/100K chars. Estimate ~500 chars per conversation turn → ~20 turns on free tier.
- **Phone numbers**: ElevenLabs provides US/EU numbers. For Italian numbers, may need SIP or Twilio integration.
- **Auth**: The Hermes gateway may need auth. If so, configure ElevenLabs to send the auth header.
- **Streaming**: For best phone UX, use streaming responses so the bot starts speaking while still generating.

## Verification

1. `ELEVENLABS_API_KEY` set in `.env`
2. ElevenLabs agent created and pointing to Hermes endpoint
3. Phone number assigned and callable
4. Test call: bot responds in Italian
5. Test tool call: bot uses a tool and speaks the result

## References

- Tweet: https://x.com/ElevenLabsDevs/status/2062561944385519801
- ElevenLabs Agents docs: https://elevenlabs.io/docs/agents
- Hermes Voice Mode: hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode
- ElevenLabs API: https://elevenlabs.io/docs/api-reference
