# HermesBro Multitenant Architecture

Backend: `{BACKEND_ROOT}/hermesbro_multitenant_backend.py` (1634 lines)
Service: `hermesbro-multitenant.service` on port 8333
DB: SQLite WAL mode at `{BACKEND_ROOT}/data/hermesbro.db`

## Endpoints

- `POST /api/tenants` — create tenant
- `GET /api/tenants` — list (filter: status, sector)
- `POST /api/tenants/{id}/provision` — full provisioning
- `POST /api/tenants/{id}/reset` — reset tenant
- `DELETE /api/tenants/{id}` — delete tenant
- `POST /api/waitlist` — join waitlist
- `POST /api/demo` — demo chat (SSE streaming)
- `POST /api/warroom` — multi-agent orchestration (SSE)
- `POST /api/telegram/webhook` — Telegram router
- `POST /api/whatsapp/provision|start|stop` — WhatsApp bridge
- `GET /api/health` — healthcheck
- `GET /api/stats` — tenant stats
- `GET /api/sectors` — sector templates
- `GET /panel` — admin panel (HTML)
- `GET /register` — waitlist registration (HTML)
- `GET /dashboard/{tenant_id}` — client dashboard (HTML)
- `GET /agents/{agent_name}` — agent profile pages (HTML)
- `GET /warroom` — war room page (HTML)
- `POST /api/orchestrate` — orchestration endpoint

## Provisioning Flow (lines 209-301)

1. Assign bot token from `bot_pool` table (or fallback to `FALLBACK_BOT_TOKEN` env)
2. Create Hermes profile via CLI: `hermes profile create {name} --clone --clone-from default --no-alias`
3. Write `tenant.json` with metadata (tenant_id, agents, bot_username)
4. Write `.env` with TELEGRAM_TOKEN + TENANT_ID + TENANT_NAME
5. Create systemd service `hermes-tnt-{profile_name}.service` (ExecStart: `hermes --profile {name} gateway run`)
6. Enable and start the service
7. Update tenant record with bot_username

## Sector Templates (DB table: sector_templates)

| Sector | Agents |
|--------|--------|
| ristorazione | groot,contaibile,machiavelli |
| e-commerce | wannabe,designbro,contaibile,machiavelli |
| liberoprofessionista | lawrenzo,contaibile,machiavelli |
| tech | mrrobot,sentinel,machiavelli |
| finance | ducato,elfroggo,contaibile,machiavelli |
| creative | wannabe,designbro,machiavelli |

## Bot Pool (DB table: bot_pool)

Pre-created Telegram bot tokens stored in DB. Provisioning assigns one per tenant.
Status: available → assigned. Fallback: `FALLBACK_BOT_TOKEN` env var.

## Templates

- `register.html` — 3-step wizard (sector → agents → email)
- `panel.html` — admin panel with stats, filters, tenant table, provision/reset/delete actions

## Nginx Config

Routes:
- `/api/demo` → 8333 (SSE, 300s timeout)
- `/api/warroom` → 8333 (SSE, 600s timeout)
- `/api/` → 8333
- `/register` → 8333
- `/panel` → 8333
- `/warroom` → 8097 (websocket)
- `/ws/` → 8097 (websocket upgrade)
- `/agents/` → static files
- `/dashboard/` → 8333

## Current State (as of 2026-06-04)

- Backend running, 4 tenants in DB (3 active, 1 trial)
- 4 Hermes profiles created (tnt-*)
- Bot pool has tokens but all tenants share same fallback token
- No Hermes gateway processes actually running for tenants
- Demo API returns 401 (invalid API key)
- Service file fix: EnvironmentFile must be in [Service] section, not [Install]

## Relationship to Business Plan

The multitenant system IS the core product of HermesBro. Flow:
1. Client arrives from hermesbro.cloud → registers (/register)
2. Backend creates dedicated Hermes profile (tnt-*)
3. Backend assigns bot token from pool
4. Backend starts bot with sector-specific agents
5. Client chats with bot on Telegram
6. After 7-day trial → pays or deactivates

See: `<HERMES_ROOT>/plans/monetizzazione-hermesbro.md` for the full business plan.
