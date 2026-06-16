# Isolation Architecture — HermesBro VPS

## Tier Structure (applicato 2026-06-08)

```
<HERMES_ROOT>/shared/knowledge/
├── personal/   → root:root 750       (solo GribbitO/root)
├── business/   → hermes-bot:hermesbro 750  (bot business)
└── shared/     → hermes-bot:hermesbro 750  (tutti)
```

- **personal/**: conversations.md, decisions.md, preferences.md, feedback.md, test-from-gribbito.md
- **business/**: facts.md, gold-examples.md, market-context.md, ownership.md, shared-facts.md, checkpoint, digests, orchestrations.jsonl
- **shared/**: isolation-plan.md, FRANK-README.md

## LUKS2 Container

- **Device**: `/dev/mapper/hermesbro-crypt`
- **Mount**: `/mnt/hermesbro-encrypted`
- **Size**: 512MB ext4
- **Contents**: 10 state.db files (uno per bot business)
- **Auto-mount**: gestito da systemd al boot
- **Keyfile**: `/etc/hermesbro/gribbito.key` (root-only 600)

Bot con DB cifrato: contabile, ducato, el-froggo, frank, groot, designbro, machiavelli, sentinel, lawrenzo, wannabe, mr-robot.

## Bot Services (13 attivi)

Tutti i servizi business girano come `hermes-bot:hermesbro` (tranne GribbitO che resta root):

```
hermes-contabile.service
hermes-dashboard.service
hermes-designbro.service
hermes-ducato.service
hermes-el-froggo.service
hermes-frank.service
hermes-groot.service
hermes-hermesribbit.service      ← GribbitO (root)
hermes-lawrenzo.service
hermes-league.service
hermes-machiavelli.service
hermes-sentinel.service
hermes-wannabe.service
hermesbro-multitenant.service
```

## What's Missing

- **Audit ogni 10 min con log JSON**: NON implementato. Solo cron sentinel nginx ogni 6h.
- **Bus isolation**: rimossa (non serviva)
- **Cifratura dati live**: solo state.db in LUKS. Gli altri DB (sessioni, memory) restano in chiaro.

## Design Decisions

- GribbitO = root by design (orchestrator, accesso totale confermato da <FOUNDER>)
- Separazione logica (tier + permessi), NON fisica (stesso VPS)
- Pronta per split su 2 VPS quando 3+ clienti paganti
