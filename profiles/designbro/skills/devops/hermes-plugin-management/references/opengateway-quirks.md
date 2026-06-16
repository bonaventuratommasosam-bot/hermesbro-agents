# OpenGateway Integration Reference

## API Structure

OpenGateway routes by provider path: `https://<gateway>/v1/<provider>/<endpoint>`

Each provider path only accepts its own models:
- `/v1/xiaomi-mimo/` → `xiaomi/mimo-*`, `mimo-*`
- Other providers have their own restrictions

## Known Quirks

### Broken gzip response headers
OpenGateway sends `Content-Encoding: gzip` but the body may not be gzip-compressed. The OpenAI Python SDK's httpx client tries to decompress and gets a `DecompressionError`.

**Fix:** Force `Accept-Encoding: identity` via custom httpx client:
```python
import httpx
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    http_client=httpx.Client(headers={"Accept-Encoding": "identity"})
)
```

### curl works but Python SDK fails
curl handles the broken gzip transparently (or sends `Accept-Encoding: identity` by default). The Python OpenAI SDK's httpx client adds `Accept-Encoding: gzip, deflate, br` by default, triggering the bug.

### Model listing
```bash
curl -s "https://<gateway>/v1/<provider>/models" \
  -H "Authorization: Bearer <key>" \
  -H "Accept-Encoding: identity"
```

### Responses API not supported
OpenGateway only supports `/v1/<provider>/chat/completions`. The newer `/v1/responses` endpoint is not available. Patch any code using `client.responses.create()` to use `client.chat.completions.create()` instead.

## Available Models (as of 2026-06-07)

Via `/v1/xiaomi-mimo/`:
- `mimo-v2.5-pro` — reasoning model (content=null, thinking in reasoning field)
- `mimo-v2.5` — non-reasoning, good for structured output
- `mimo-v2-flash` — lighter/faster, may not follow complex prompts

## Environment

- Gateway URL: `<GATEWAY_URL>
- API key env: `OPENGATEWAY_API_KEY` (in bot .env files)
- Used by: all gold bots + gribbito as primary LLM gateway
