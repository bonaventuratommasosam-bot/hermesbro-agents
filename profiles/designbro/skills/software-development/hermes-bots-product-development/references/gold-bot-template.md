# Gold Bot — Single-File FastAPI Template

## Structure

```
{bot}-gold/
├── main.py    # Everything in one file
└── .env       # LLM_BASE_URL, LLM_API_KEY, LLM_MODEL, BOT_TOKEN, PORT
```

## Port Assignments (8097-8105)

| Bot | Port |
|-----|------|
| GROOT clone | 8097 |
| Wannabe Gold | 8098 |
| DesignBro Gold | 8099 |
| Ducato Gold | 8100 |
| El Froggo Gold | 8101 |
| MR.ROBOT Gold | 8102 |
| Sentinel Gold | 8103 |
| Machiavelli Gold | 8104 |
| War Room Gold | 8105 |

## main.py Template

```python
"""Bot Name Gold"""
from __future__ import annotations
import json, logging, os, httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

L = os.getenv("LLM_BASE_URL", "<GATEWAY_URL>")
K = os.getenv("LLM_API_KEY", "")
M = os.getenv("LLM_MODEL", "mimo-v2.5-pro")
B = os.getenv("BOT_TOKEN", "")
R = 5
T = 16384

SOUL = 'Sei BOT_NAME, ...'

TOOLS = [
    {"type": "function", "function": {"name": "tool_name", "description": "...", "parameters": {...}}}
]

def X(n, a, u):
    """Tool executor — dispatch by name, return JSON string."""
    try:
        if n == "tool_name":
            return json.dumps({...})
        return f"Unknown:{n}"
    except Exception as e:
        return f"Error:{e}"

async def B2(m, u):
    """Brain loop — LLM → tool_calls → execute → repeat."""
    q = [{"role": "system", "content": SOUL}, {"role": "user", "content": m}]
    for _ in range(R):
        try:
            async with httpx.AsyncClient(timeout=60) as c:
                r = await c.post(f"{L}/chat/completions",
                    json={"model": M, "messages": q, "tools": TOOLS, "tool_choice": "auto", "max_tokens": T},
                    headers={"Authorization": f"Bearer {K}", "Content-Type": "application/json"})
                p = r.json()["choices"][0]["message"]
        except:
            return "Problema tecnico."
        if not p.get("tool_calls"):
            return p.get("content", "")
        q.append(p)
        for t in p["tool_calls"]:
            try:
                a = json.loads(t["function"]["arguments"])
            except:
                a = {}
            q.append({"role": "tool", "tool_call_id": t["id"], "content": X(t["function"]["name"], a, u)})
    return "Troppe op."

@asynccontextmanager
async def lifespan(a):
    logger.info("Bot started")
    yield

a = FastAPI(title="Bot Gold", lifespan=lifespan)

@a.get("/")
async def root():
    return {"service": "Bot Gold", "status": "running"}

@a.get("/health")
async def health():
    return {"status": "ok"}

@a.post("/webhook/{t}")
async def webhook(t, req: Request):
    if t != B:
        return {"error": "Invalid token"}
    try:
        b = await req.json()
    except:
        return {"error": "Invalid JSON"}
    m = b.get("message", {})
    x = (m.get("text") or "").strip()
    c = m.get("chat", {}).get("id")
    u = m.get("from", {}).get("id", 0)
    if not x or not c:
        return {"ok": True}
    if x == "/start":
        return {"method": "sendMessage", "chat_id": c, "text": "Welcome..."}
    r = await B2(x, u)
    return {"method": "sendMessage", "chat_id": c, "text": r}

@a.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return """<html><body style="background:#09090B;color:#FAFAFA;font-family:Inter;padding:2rem">
    <h1 style="color:#d4a853">Bot</h1></body></html>"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(a, host="0.0.0.0", port=int(os.getenv("PORT", "8097")))
```

## Telegram Webhook Format

Return `{"method": "sendMessage", "chat_id": c, "text": r}` directly — no need for Bot API call.

## Dashboard Style

- Background: `#09090B` (near-black)
- Text: `#FAFAFA` (near-white)
- Accent: `#d4a853` (gold)
- Font: Inter
- Minimal, dark, professional
