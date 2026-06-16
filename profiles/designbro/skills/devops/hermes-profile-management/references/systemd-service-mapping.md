# Systemd Service Mapping — Hermes Bots

Last updated: 2026-05-28 (consolidation pass)

## Current State

| Bot | Old Service | Hermes Service | Status |
|---|---|---|---|
| GribbitO (main) | (none) | `hermes-gribbito.service` | ✅ Clean (includes dev+security) |
| Groot | `groot.service` | `hermes-groot.service` | ✅ Old masked |
| LAWrenzo | `lawrenzo.service` + `lawrenzo-web.service` | `hermes-lawrenzo.service` | ✅ Old masked |
| ContAIbile | (none) | `hermes-contabile.service` | ✅ Clean |
| Wannabe | `wannabe.service` | `hermes-wannabe.service` | ✅ Old masked, Hermes active |
| DesignBro | (none) | `hermes-designbro.service` | ✅ Clean |
| EL Froggo | (none) | `hermes-el-froggo.service` | ✅ Clean |
| dev-agent | (none) | (none) | ❌ Consolidated into gribbito 2026-05-28 |
| security-auditor | (none) | (none) | ❌ Consolidated into gribbito 2026-05-28 |
| gribbito-agent | (none) | (none) | ❌ Consolidated into gribbito 2026-05-28 |

## Service File Locations

- `/etc/systemd/system/<name>.service` — custom user services
- `/etc/systemd/system/multi-user.target.wants/` — symlinks for enabled services

## Conflict Detection Command

```bash
systemctl list-units --type=service | grep -iE '(groot|lawrenzo|wannabe|contabile|ratatouille|froggo|designbro)'
```

## Naming Convention

- Hermes profile services: `hermes-<profile-name>.service`
- Old standalone services: `<bot-name>.service`

## Masking Workflow (tested 2026-05-28)

When `stop + disable` doesn't prevent restarts (Restart=always):

```bash
# If service file already exists, remove it first then mask
rm -f /etc/systemd/system/<old>.service
systemctl daemon-reload
systemctl mask <old>.service
```

The `mask` creates a symlink to `/dev/null` — no start is possible.

## Masked Services (permanent, as of 2026-05-28)

- `groot.service` → masked
- `lawrenzo.service` → masked
- `lawrenzo-web.service` → masked
- `wannabe.service` → masked

## Known Issues

- `ratatouille-[REDACTED — dati personali rimossi]` profile may not exist (service shows `not-found`)
- `ratatouille-backup.service` is loaded but failed — not blocking anything
- 7 Hermes profiles active: gribbito, el-froggo, contabile, lawrenzo, groot, wannabe, designbro
