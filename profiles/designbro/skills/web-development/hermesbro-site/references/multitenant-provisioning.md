# Multitenant Provisioning Architecture

## Purpose
The multitenant backend IS the HermesBro product. It's not a separate system — it's the SaaS platform that sells AI bots to Italian SMEs.

## Business Model
- B2B SaaS: €29-199/month per tenant
- 6 sectors: Ristorazione, E-Commerce, Libero Professionista, Tech/SaaS, Finance/Crypto, Creativo/Marketing
- Each sector gets pre-configured agents (e.g. ContAIbile + GROOT for ristoranti)
- Trial: 7 giorni, poi pagamento

## Current Architecture

### What EXISTS
```
/hermesbro.cloud/register  →  Backend creates tenant record in SQLite
                          →  Backend creates Hermes profile (tnt-*)
                          →  Profile has: .env, SOUL.md, config.yaml, skills/
```

### What's MISSING (as of 2026-06-04)
1. **Bot token generation** — All 4 tenants share the SAME token (836751...Y5TA). Each tenant needs a UNIQUE token from @BotFather.
2. **Bot process startup** — No Hermes process is actually started for any tenant. Provisioning creates the profile directory but doesn't launch anything.
3. **Demo API auth** — `/api/demo` returns 401 (invalid API key). The .env has a placeholder key.
4. **Billing** — Trial period is tracked in DB but no payment integration exists.
5. **Monitoring** — No health checks on tenant bots, no auto-restart.

## Provisioning Flow (current)
```python
# In hermesbro_multitenant_backend.py
def provision_tenant(tenant):
    # 1. Create Hermes profile via CLI
    create_hermes_profile(profile_name, tenant_id, agents, tenant_name)
    # 2. Update DB with profile_name
    # That's it — no bot token, no process start
```

## Provisioning Flow (needed)
```
1. Generate unique bot token via BotFather API (or manual step)
2. Create Hermes profile with that token in .env
3. Start hermes gateway process for that profile
4. Register webhook for Telegram updates
5. Update DB with bot_token, bot_username
6. Set up monitoring + auto-restart
```

## Key Files
- Backend: `{BACKEND_ROOT}/hermesbro_multitenant_backend.py` (1565 lines)
- DB: `{BACKEND_ROOT}/data/hermesbro.db` (SQLite WAL mode)
- Templates: `{BACKEND_ROOT}/templates/` (register.html, panel.html)
- Tenant profiles: `<HERMES_ROOT>/profiles/tnt-*/`
- .env: `{BACKEND_ROOT}/.env` (OPENAI_API_KEY, XIAOMI_BASE_URL, LLM_MODEL)
- Service: `hermesbro-multitenant.service` (systemd, port 8333)

## Gold Bots (separate system)
The gold bots at `/home/[REDACTED — dati personali rimossi]/ai-stack/*-gold/` are standalone FastAPI scripts, NOT Hermes profiles. They run independently and are NOT connected to the multitenant backend. The multitenant system creates Hermes profiles, not gold bot instances.

## Sectors and Default Agents
| Sector | Default Agents |
|--------|---------------|
| ristorazione | contaibile, groot, wannabe, machiavelli |
| e-commerce | contaibile, wannabe, designbro, machiavelli |
| liberoprofessionista | contaibile, lawrenzo, wannabe, machiavelli |
| tech | mrrobot, sentinel, wannabe, contaibile, machiavelli |
| finance | ducato, elfroggo, sentinel, contaibile, machiavelli |
| creative | designbro, wannabe, lawrenzo, machiavelli |

## API Endpoints
- `POST /api/tenants` — create tenant
- `GET /api/tenants` — list tenants
- `POST /api/tenants/{id}/provision` — provision tenant (create profile)
- `POST /api/tenants/{id}/reset` — reset tenant
- `GET /api/sectors` — list sectors
- `GET /api/stats` — tenant statistics
- `POST /api/waitlist` — waitlist signup
- `POST /api/telegram/webhook` — Telegram bot router
- `POST /api/whatsapp/provision` — WhatsApp bridge setup

## DB Tables
- `tenants` — main tenant records
- `tenant_logs` — provisioning/action logs
- `waitlist` — waitlist signups
- `contacts` — contact form submissions
- `sector_templates` — sector definitions with agents/workflows
