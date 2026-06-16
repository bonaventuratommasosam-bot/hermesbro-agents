# Hermes Dashboard

Web UI ufficiale per Hermes Agent — browser-based management dashboard.

## Quick Start

```bash
hermes dashboard
```

Apre `http://127.0.0.1:9119` — tutto locale, nessun dato esce da localhost.

## Prerequisites

```bash
pip install 'hermes-agent[web,pty]'
# oppure
pip install 'hermes-agent[all]'
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | 9119 | Porta web server |
| `--host` | 127.0.0.1 | Bind address |
| `--no-open` | — | Non aprire browser |
| `--insecure` | off | Disabilita OAuth gate (⚠️ espone API keys) |
| `--tui` | off | Abilita Chat tab (embedded hermes --tui) |

```bash
hermes dashboard --port 8080
hermes dashboard --host 0.0.0.0        # ⚠️ With caution
hermes dashboard --no-open
hermes dashboard --tui                  # Enable in-browser chat
```

## Pages

### Status (landing)
- Agent version e data release
- Gateway status — running/stopped, PID, piattaforme connesse
- Sessioni attive — count ultimi 5 minuti
- Sessioni recenti — lista 20 più recenti con modello, token usage, preview
- Auto-refresh ogni 5 secondi

### Chat
- TUI completo embedded nel browser (xterm.js + WebGL)
- Slash commands, model picker, tool-call cards, markdown streaming
- Resume sessioni esistenti da tab Sessions
- `/api/pty` WebSocket authenticated with session token

### Config
- Editor form-based per `config.yaml`
- 150+ campi auto-discover da `DEFAULT_CONFIG`
- Tabs: model, terminal, display, agent, delegation, memory, approvals
- Save, Reset to defaults, Export/Import JSON

### API Keys
- Gestione `.env` file
- Gruppi: LLM Providers, Tool API Keys, Messaging Platforms, Agent Settings
- Ogni key mostra: set/unset, redacted preview, descrizione, link provider

### Sessions
- Browse e ispeziona tutte le sessioni
- Full-text search (FTS5)
- Expand per vedere history completa
- Tool calls con JSON arguments
- Delete sessioni

### Logs
- Agent, gateway, error logs
- Filtro per level (DEBUG/INFO/WARNING/ERROR)
- Filtro per component (gateway/agent/tools/cli/cron)
- Auto-refresh ogni 5 secondi
- Color-coded per severity

### Analytics
- Token usage breakdown (input/output)
- Cache hit percentage
- Cost tracking
- Daily token chart (stacked bar)
- Per-model breakdown
- Time period: 7, 30, o 90 giorni

### Cron
- Create/edit/pause/resume/delete cron jobs
- Trigger now — esecuzione immediata
- Cron expression quick presets
- Delivery target: local, Telegram, Discord, Slack, email

### Skills
- Browse/search skills per categoria
- Toggle enable/disable
- Toolsets con status attivo/configurato

## REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Agent version, gateway status, sessioni attive |
| `/api/sessions` | GET | 20 sessioni recenti |
| `/api/config` | GET | config.yaml come JSON |
| `/api/config` | PUT | Salva configurazione |
| `/api/config/defaults` | GET | Default config values |
| `/api/config/schema` | GET | Config field schema |
| `/api/env` | GET | Variabili ambiente |
| `/api/env` | PUT | Set env var |
| `/api/env` | DELETE | Remove env var |
| `/api/sessions/{id}` | GET | Session metadata |
| `/api/sessions/{id}/messages` | GET | Full message history |
| `/api/sessions/search?q=` | GET | Full-text search |
| `/api/sessions/{id}` | DELETE | Delete session |
| `/api/logs` | GET | Log lines (file, lines, level, component) |
| `/api/analytics/usage?days=30` | GET | Token usage, costi |
| `/api/cron/jobs` | GET | Cron jobs |
| `/api/cron/jobs` | POST | Create cron job |
| `/api/cron/jobs/{id}/pause` | POST | Pause job |
| `/api/cron/jobs/{id}/resume` | POST | Resume job |
| `/api/cron/jobs/{id}/trigger` | POST | Trigger now |
| `/api/cron/jobs/{id}` | DELETE | Delete job |
| `/api/skills` | GET | Skills con status |
| `/api/skills/toggle` | PUT | Enable/disable skill |
| `/api/tools/toolsets` | GET | Toolsets con status |

## OAuth Authentication (gated mode)

| Bind | Auth gate | Use case |
|------|-----------|----------|
| `hermes dashboard` (127.0.0.1) | OFF | Local development |
| `--host 0.0.0.0` | ON | Production / Fly.io |
| `--host 192.168.1.10 --insecure` | OFF | Trusted LAN |

- OAuth via Nous Portal (authorization-code + PKCE)
- Access tokens: 15-minute TTL, no refresh token in v1
- Custom providers: create plugin registering `DashboardAuthProvider`

## Themes (7 built-in)

| Theme | Character |
|-------|-----------|
| Hermes Teal (default) | Dark teal + cream, system fonts |
| Hermes Teal Large | Same, 18px text, roomier spacing |
| Midnight | Deep blue-violet, Inter + JetBrains Mono |
| Ember | Warm crimson + bronze, Spectral serif |
| Mono | Grayscale, IBM Plex, compact |
| Cyberpunk | Neon green on black, Share Tech Mono |
| Rosé | Pink + ivory, Fraunces serif |

## /reload Slash Command

After changing API keys via dashboard, use `/reload` in CLI to pick up changes:
```
/reload → Reloaded .env (3 var(s) updated)
```

## Community Alternative: Hermes Web UI

Full-featured alternative by EKKOLearnAI:
- **GitHub**: https://github.com/EKKOLearnAI/hermes-web-ui
- **Stars**: 6.7k
- **npm**: `npm install -g hermes-web-ui`
- **Port**: 8648
- **Extra features**: Multi-agent chat rooms, WeChat QR login, file browser, web terminal, account management, Docker support
- **Tech**: Vue 3 + Koa 2 + Socket.IO

## Links

- **Docs**: https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
- **Extending**: https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard
- **API Server**: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
