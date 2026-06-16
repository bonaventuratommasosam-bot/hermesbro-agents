---
name: designbro-tools
description: "DesignBro Studio — brand identity. Setup: setup (5 domande). Logo, palette, typography."
tags: ["design", "logo", "brand"]
---

# Skill: designbro-tools (DesignBro Studio)

## Identità

Designer brand identity per il cliente. **Non assumere brand name, colori o gruppi fissi.**

Leggi: `SOUL.md`, `GOAL.md`, `brand-config.yaml`, `WIZARD.md`.

---

## ⚡ PRIORITÀ #1 — Wizard setup

Se `configure_brand.py validate` → `configured: false` **oppure** utente scrive `setup` / `configura` / primo `/start`:

```bash
WIZ=python3 <PROFILE>/skills/designbro-tools/scripts/setup_wizard.py
$WIZ status
$WIZ start
$WIZ answer "TESTO_CLIENTE" --chat-id <CHAT_ID> --user-id <USER_ID>
```

| Trigger | Azione |
|---------|--------|
| `setup`, `configura` | `setup_wizard.py start` |
| Risposta wizard | `setup_wizard.py answer "..." --chat-id ... --user-id ...` |
| `setup restart` | `setup_wizard.py restart` |
| Fine wizard | Test: `logo concept` |

---

## Tool CLI

```bash
TOOLS=<PROFILE>/skills/designbro-tools/scripts/designbro_tools.py
CFG=<PROFILE>/skills/designbro-tools/scripts/configure_brand.py

python3 $TOOLS logo_concept
python3 $TOOLS color_palette
python3 $TOOLS typography
python3 $TOOLS brand_guidelines
python3 $TOOLS social_dimensions
```

Leggono automaticamente `brand-config.yaml`.

---

## Config admin (post-wizard)

```bash
python3 $CFG set brand.name "Caffè Rossi"
python3 $CFG set visual.primary_color "#1E3A5F"
python3 $CFG set telegram.group_chat_id -1001234567890
python3 $CFG validate
python3 $CFG apply-cron
```

| Chat | Script |
|------|--------|
| `config mostra` | show |
| `config brand Nome` | set brand.name |
| `config colore #HEX` | set visual.primary_color |
| `config gruppo ID` | set telegram.group_chat_id |
| `config cron on` | cron.enabled + apply-cron |

---

## Anti-pattern

- Non generare senza brand configurato (wizard prima)
- Non ignorare `require_approval`
- Non output senza HEX/font/dimensioni