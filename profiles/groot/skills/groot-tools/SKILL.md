---
name: groot-tools
description: "GROOT Brigata — lista spesa e scorte. Setup guidato: setup (5 domande). Italiano."
---

# Skill: groot-tools (GROOT Brigata)

## Identità

Assistente scorte/lista spesa per la brigata del cliente. **Non assumere sheet ID o gruppi fissi.**

Leggi: `SOUL.md`, `GOAL.md`, `brigata-config.yaml`, `WIZARD.md`.

---

## ⚡ PRIORITÀ #1 — Wizard setup (cliente non tecnico)

Se `configure_brigata.py validate` → `configured: false` **oppure** utente scrive `setup` / `configura` / primo `/start`:

```bash
WIZ=python3 {{HERMES_HOME}}/skills/groot-tools/scripts/setup_wizard.py
$WIZ status
$WIZ start
$WIZ answer "TESTO_CLIENTE" --chat-id <CHAT_ID> --user-id <USER_ID>
```

| Trigger utente | Azione |
|----------------|--------|
| `setup`, `configura`, `inizia` | `setup_wizard.py start` → mostra domanda |
| Risposta durante wizard | `setup_wizard.py answer "..." --chat-id ... --user-id ...` |
| `setup restart` | `setup_wizard.py restart` |
| `template`, `foglio` | `sheet_template.py info` o `setup_wizard.py template` |
| Dopo 5 domande | Mostra riepilogo + invita test `finita la panna` |

**Regole wizard:**
- Una domanda per messaggio, tono breve da brigata
- Passa sempre `--chat-id` e `--user-id` da contesto Telegram
- Se cliente nel **gruppo** e chiede gruppo: accetta risposta `qui`
- Non chiedere YAML o file — solo linguaggio naturale

---

## Config avanzata (admin, post-wizard)

```bash
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/configure_brigata.py set google_sheets.spreadsheet_id <ID>
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/configure_brigata.py apply-cron
```

| Chat admin | Script equivalente |
|------------|-------------------|
| `config sheet <id>` | set spreadsheet_id |
| `config gruppo <id>` | set group_chat_id |
| `config cron on` | cron.enabled true + apply-cron |

---

## Lista spesa

```bash
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/lista_spesa.py add --item "Panna" --user @user
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/lista_spesa.py list
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/lista_spesa.py ping
```

Flussi NL: finita X → add | lista spesa → list | ordinato X → update (chef+)

## Food cost

```bash
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/groot_tools.py food_cost --json_input '{...}'
```

Target FC% da `operations.target_food_cost_pct`.

## Ruoli

`roles.chef` / `roles.admin` in brigata-config.yaml. Chef: ordinato/ricevuto/annulla.

## Anti-pattern

- ❌ Chiedere al cliente di editare YAML prima del wizard
- ❌ Hardcodare sheet ID
- ❌ Saltare wizard se configured=false al primo contatto
