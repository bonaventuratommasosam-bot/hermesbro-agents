# War Room + Demo — Real Agent Architecture

## Overview

Both the War Room (`/warroom`) and Demo section (landing `#demo`) use **real Hermes agent calls** via SSE, not simulated responses.

- `/api/warroom` — multi-agent chain: selected agents discuss sequentially, Machiavelli synthesizes
- `/api/demo` — single-agent: one agent answers the user's query directly

## War Room Architecture

### Agent Chain Flow
1. User selects 2-4 agents + optional topic on `/warroom`
2. Frontend POSTs to `/api/warroom` with `{query, agents: ["contaibile", "lawrenzo", ...]}`
3. Backend runs agents sequentially via `orchestrator.run_hermes(profile, prompt)`
4. Each agent receives ALL previous responses as context (cumulative chain)
5. After all agents respond, Machiavelli runs a final synthesis
6. Each result is streamed as an SSE event: `data: {"type": "response", "agent": "...", "text": "...", "index": N}\n\n`
7. Status events: `{"type": "status", "message": "ContAIbile sta analizzando...", "index": N}`
8. End event: `{"type": "end"}`

### Key Files
- `{BACKEND_ROOT}/orchestrator.py` — `run_hermes(profile, prompt)` + `AGENTS` dict
- `{BACKEND_ROOT}/hermesbro_multitenant_backend.py` — `/api/warroom` endpoint + inline HTML for `/warroom` page

### Orchestrator Pattern
```python
# orchestrator.py
AGENTS = {
    "contaibile": {"name": "ContAIbile", "profile": "contaibile", ...},
    "lawrenzo": {"name": "LAWrenzo", "profile": "lawrenzo", ...},
    "wannabe": {"name": "Wannabe", "profile": "wannabe", ...},
    "groot": {"name": "GROOT", "profile": "groot", ...},
    "machiavelli": {"name": "Machiavelli", "profile": "machiavelli", ...},
}

def run_hermes(profile: str, prompt: str) -> dict:
    # Uses `hermes --profile NAME -p "prompt"` CLI
    # Returns {"response": "...", "latency": N.NN}
```

### SSE Endpoint (Python)
```python
import json, sys
sys.path.insert(0, "{BACKEND_ROOT}")
from orchestrator import run_hermes, AGENTS

@app.post("/api/warroom")
async def api_warroom(request: Request):
    body = await request.json()
    query = body.get("query", "").strip()
    agents = body.get("agents", [])
    if len(agents) < 2:
        return JSONResponse({"error": "Need at least 2 agents"}, status_code=400)

    async def event_stream():
        responses = []
        for i, agent_key in enumerate(agents):
            agent = AGENTS[agent_key]
            yield "data: " + json.dumps({"type": "status", "message": f"{agent['name']} sta analizzando...", "index": i}) + "\n\n"
            
            # Build cumulative prompt with all previous responses
            context = "\n\n".join([f"[{r['agent']}]: {r['text']}" for r in responses])
            prompt = f"Domanda: {query}\n\nRisposte precedenti:\n{context}\n\nRispondi come {agent['name']}."
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: run_hermes(agent["profile"], prompt))
            
            resp = {"type": "response", "agent": agent["name"], "text": result["response"], "index": i}
            responses.append(resp)
            yield "data: " + json.dumps(resp) + "\n\n"
        
        # Machiavelli synthesis
        yield "data: " + json.dumps({"type": "status", "message": "Machiavelli sta sintetizzando..."}) + "\n\n"
        synthesis_prompt = f"Domanda: {query}\n\n" + "\n\n".join([f"[{r['agent']}]: {r['text']}" for r in responses])
        synthesis = await loop.run_in_executor(None, lambda: run_hermes("machiavelli", synthesis_prompt))
        yield "data: " + json.dumps({"type": "response", "agent": "Machiavelli", "text": synthesis["response"], "index": len(agents), "synthesis": True}) + "\n\n"
        
        yield "data: " + json.dumps({"type": "end"}) + "\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"})
```

### Frontend (fetch + ReadableStream)
```javascript
// EventSource doesn't support POST — use fetch with ReadableStream
const response = await fetch('/api/warroom', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query: userInput, agents: selectedAgents})
});

const reader = response.body.getReader();
const decoder = new TextDecoder();
let buffer = '';

while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, {stream: true});
    
    const lines = buffer.split('\n');
    buffer = lines.pop(); // Keep incomplete line in buffer
    
    for (const line of lines) {
        if (line.startsWith('data: ')) {
            const event = JSON.parse(line.slice(6));
            if (event.type === 'status') { /* show loading */ }
            if (event.type === 'response') { /* append agent response */ }
            if (event.type === 'end') { /* done */ }
        }
    }
}
```

## Demo Section Architecture

### Single-Agent Flow
1. User selects an agent (or uses scenario shortcut) on landing page
2. Frontend POSTs to `/api/demo` with `{query, agent: "contaibile"}`
3. Backend runs ONE agent via `orchestrator.run_hermes(profile, prompt)`
4. Streams back a single `response` event, then `end`

### /api/demo Endpoint
```python
@app.post("/api/demo")
async def api_demo(request: Request):
    body = await request.json()
    query = body.get("query", "").strip()
    agent_key = body.get("agent", "contaibile")
    agent = AGENTS.get(agent_key)
    if not agent:
        return JSONResponse({"error": f"Unknown agent: {agent_key}"}, status_code=400)

    async def event_stream():
        yield "data: " + json.dumps({"type": "status", "message": f"{agent['name']} sta analizzando..."}) + "\n\n"
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: run_hermes(agent["profile"], query))
        yield "data: " + json.dumps({"type": "response", "text": result["response"]}) + "\n\n"
        yield "data: " + json.dumps({"type": "end"}) + "\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"})
```

## nginx Configuration

Both SSE endpoints need dedicated nginx location blocks placed BEFORE the generic `/api/` prefix match:

```nginx
location = /api/warroom {
    proxy_pass http://127.0.0.1:8333;
    proxy_buffering off;
    proxy_cache off;
    chunked_transfer_encoding off;
    proxy_read_timeout 600s;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location = /api/demo {
    proxy_pass http://127.0.0.1:8333;
    proxy_buffering off;
    proxy_cache off;
    chunked_transfer_encoding off;
    proxy_read_timeout 600s;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Pitfalls (specific to War Room + Demo)

1. **f-strings in SSE yields**: Never use `yield f"data: {json.dumps({'key': val})}\n\n"` — causes SyntaxError with nested quotes. Use string concatenation: `yield "data: " + json.dumps({"key": val}) + "\n\n"`

2. **import sys**: Backend needs `import sys` for `sys.path.insert()` to import orchestrator. Add it to the imports at the top of the backend file.

3. **AGENTS dict completeness**: All agents available in the frontend selection grid MUST exist in `orchestrator.AGENTS`. Missing agents cause KeyError at runtime.

4. **Agent latency**: Each agent takes 30-60s. War Room with 3 agents + synthesis = 2-4 minutes total. Frontend must handle long waits gracefully (show progress, disable buttons).

5. **nginx buffering**: Without `proxy_buffering off`, nginx buffers the entire SSE stream and the client receives nothing until connection closes. The `X-Accel-Buffering: no` header in the response helps but the nginx config directive is the reliable fix.

6. **EventSource vs fetch**: `EventSource` only supports GET. Since `/api/warroom` and `/api/demo` are POST endpoints, frontend MUST use `fetch()` + `ReadableStream` pattern.
