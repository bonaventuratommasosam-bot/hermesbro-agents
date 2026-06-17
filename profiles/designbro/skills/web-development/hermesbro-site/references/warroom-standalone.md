# War Room Standalone Service (port 8097)

## Overview

The War Room has TWO implementations. The **standalone service** is the primary one, served at `/warroom`.

| Implementation | Port | Service | Route | Protocol |
|---|---|---|---|---|
| Standalone War Room | 8097 | `warroom.service` | `/warroom`, `/ws/{session_id}` | WebSocket |
| Multitenant backend (legacy) | 8333 | `hermesbro-multitenant.service` | `/api/warroom` | SSE |

## Standalone Service

**Location**: `/home/[REDACTED — dati personali rimossi]/ai-stack/warroom/main.py`
**Config**: `/etc/systemd/system/warroom.service`
**Start**: `systemctl start warroom.service`
**Restart**: `systemctl restart warroom.service`
**Logs**: `journalctl -u warroom.service -f`

### Architecture

- **WebSocket** at `/ws/{session_id}` for real-time bidirectional streaming
- **Moderator agent** (HermesRibbitBot) facilitates the discussion
- **6 workflow templates**: free brainstorming, new project, problem solving, etc.
- **Multi-round discussion**: agents respond to each other, not just sequential monologues
- **OpenGateway** for LLM calls (MiMo V2.5-Pro)

### Agent Profiles

All agents have system prompts that explicitly instruct them to:
- RISPONDI DIRETTAMENTE to what the previous agent said
- Agree/disagree with reasoning
- Not repeat concepts already expressed
- Be concise (max 150 words per turn)

| Agent | Role | Color |
|---|---|---|
| HermesRibbitBot | Moderatore | `#00f0ff` |
| GROOT | Ristorazione | `#f59e0b` |
| ContAIbile | Finanza | `#10B981` |
| LAWrenzo | Legale | `#6366F1` |
| Wannabe | Social Media | `#8B5CF6` |
| DesignBro | Design | `#EC4899` |
| DUCATO | Trading AI | `#d4a853` |
| El Froggo | DeFi | `#22d3ee` |

### Workflow Templates

1. **free** — Brainstorming Libero (round-robin, 2 rounds per agent)
2. **new_project** — Nuovo Progetto (4 phases: explore → risks → opportunities → action plan)
3. **problem** — Risolvi un Problema (diagnosis → solutions → stress-test → decision)
4. Plus 3 more templates in the WORKFLOWS dict

### nginx Configuration

```nginx
# Standalone War Room (port 8097) — HTML page only
location = /warroom {
    proxy_pass http://127.0.0.1:8097/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

# WebSocket for War Room — MUST match /warroom/ws/{session_id}
# The frontend JS connects to: wss://host/warroom/ws/${sessionId}
# which does NOT match `location /ws/` (that only matches paths starting with /ws/)
location /warroom/ws/ {
    rewrite ^/warroom/(.*) /$1 break;
    proxy_pass http://127.0.0.1:8097;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
}

# Generic WebSocket support (for other endpoints like /ws/*)
location /ws/ {
    proxy_pass http://127.0.0.1:8097;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
}
```

**PITFALL — WebSocket path nesting**: The frontend JS connects to `wss://host/warroom/ws/${sessionId}`, NOT `wss://host/ws/${sessionId}`. nginx `location /ws/` only matches paths that START with `/ws/` — it does NOT match `/warroom/ws/`. Without the dedicated `location /warroom/ws/` block with `rewrite`, the WebSocket connection silently fails (status "reconnecting...") and the "AVVIA BRAINSTORMING" button appears to do nothing. **Symptoms**: button click fires `startSession()` which calls `ws.send()`, but ws.readyState may be 0 (CONNECTING) or the connection never establishes. **Diagnosis**: check `browser_console` → `ws.readyState` and `ws.url`. If the URL shows `/warroom/ws/` but readyState is not 1 (OPEN), nginx is not routing the WebSocket. **Fix**: add the `location /warroom/ws/` block with `rewrite ^/warroom/(.*) /$1 break;` BEFORE the generic `location /ws/` block. nginx uses first-match for prefix locations, so order matters.

**PITFALL — File permissions**: `warroom.html` (if served as static) and any new static file created by root defaults to `600` → nginx returns 403. Always `chmod 644` after creating files in `{WEB_ROOT}/`.

**PITFALL — `init()` must call `showSetupPanel()`**: The setup panel (topic input, agent selection, workflow picker, "Avvia Brainstorming" button) starts with `display: none` inline style after a session ends or on page load if a previous session's state was cached. The `init()` function in `warroom.html` must call `showSetupPanel()` at the end to ensure the panel is visible when the page first loads. Without this call, the page renders with the sidebar empty — the user sees the War Room layout but has no way to start a brainstorming. The `showSetupPanel()` function sets `setupPanel.style.display = ''` and hides the active/completed panels. **Symptoms**: page loads, WebSocket is "online", but no topic input or start button visible. The `startBtn` element exists in DOM but has `offsetWidth: 0, offsetHeight: 0` because its parent `setupPanel` is `display: none`. **Diagnosis**: `browser_console` → check `getComputedStyle(document.getElementById('setupPanel')).display` and `document.getElementById('startBtn').offsetWidth`. If display is `none` and width is 0, the panel is hidden. **Fix**: add `showSetupPanel();` as the last line of `async function init()` in `/home/[REDACTED — dati personali rimossi]/ai-stack/warroom/templates/warroom.html`. After editing, restart: `systemctl restart warroom.service`.

**PITFALL**: The `proxy_pass` for `/warroom` has a trailing slash (`http://127.0.0.1:8097/;`) because the standalone service serves its page at `/` not `/warroom`. Without the trailing slash, nginx passes `/warroom` to the backend which returns 404.

### API Endpoints (standalone)

- `GET /` — Main War Room HTML page
- `WS /ws/{session_id}` — WebSocket for real-time discussion
- `GET /api/sessions` — List all sessions
- `GET /api/sessions/{session_id}/result` — Get session result
- `GET /api/agents` — List available agents
- `GET /api/workflows` — List workflow templates

### Key Differences from Legacy Multitenant War Room

| Feature | Standalone (8097) | Legacy (8333) |
|---|---|---|
| Protocol | WebSocket | SSE |
| Moderator | HermesRibbitBot | None |
| Workflows | 6 templates | None |
| Discussion style | Multi-round, interactive | Sequential chain |
| Agent prompts | "Rispondi direttamente" | "Fornisci la tua analisi" |
| Frontend | Full SPA with session history | Inline HTML |

## Legacy Multitenant War Room (still active)

The `/api/warroom` endpoint on port 8333 is still active and used by the landing page demo section. It uses the older sequential chain pattern with `orchestrator.run_hermes()` via CLI. See `references/warroom-interactive.md` for details.

### Improvements Made (2026-06-04)

The prompts in the multitenant backend's `/api/warroom` were updated to encourage more interactive discussion:
- Agents now see "=== RISPOSTE DEI TUOI COLLEGHI (devi rispondere a loro) ==="
- Explicit instructions: cite colleague by name, agree/disagree with reasoning, don't repeat
- Machiavelli synthesis now highlights where specialists agreed/disagreed
