# Shared Knowledge (auto-synced from fleet)
# Last sync: TIMESTAMP_PLACEHOLDER
# DO NOT EDIT — modify <HERMES_SHARED>/knowledge/ instead

## ✅ RIEPILOGO — ARCHITETTURA GENERALE

### 🏗 Architettura

CLIENTE → <platform_url>/register → POST /api/tenants → AUTO-PROVISIONING
                                                        ↓
                                    Crea profili da template (SOUL + GOAL + skills)
                                    Assegna token da bot_pool (quando popolata)
                                    Avvia systemd service
                                    Pronto in <30 secondi

### Flusso

1. Utente si registra sulla piattaforma
2. Provisioning automatico dal template
3. Bot attivo e operativo

### Architettura finale

<HERMES_BASE>/profiles/ ← Profili bot
├── ducato/          ✅ @DucatoBot (placeholder)
├── contabile/       ✅ @ContabilBot (placeholder)
├── lawrenzo/        ✅ @LawrenzoBot (placeholder)
├── [altri profili]  ...

## Bot della flotta
- **GribbitO** — Master Orchestrator
- **Ducato** — Stratega finanziario
- **Contabile** — Bilancio e cash flow
- **GROOT** — Costi evento, break-even
- **El-froggo** — P&L crypto, allocazione
- **Wannabe** — KPI per contenuti
- **DesignBro** — Designer visivo
- **MrRobot/Frank** — Technical architect
- **Sentinel** — Security, compliance
- **Machiavelli** — Orchestratore flotta

## Note operative
- Tutti i bot usano lo stesso token Telegram (un unico bot con personalità diverse) — per personalità veramente autonome servono token separati da BotFather
- Piattaforma con auto-provisioning da template funzionante
- Gruppo Telegram di test per comunicazioni flotta
