---
name: lawrenzo-tools
description: "Lawrenzo Legal — contratti, GDPR, compliance. Setup: setup (5 domande)."
tags: ["legal", "contracts", "gdpr"]
---

# Skill: lawrenzo-tools (Lawrenzo Legal)

Leggi: `SOUL.md`, `GOAL.md`, `legal-config.yaml`, `WIZARD.md`.

## Wizard setup

```bash
WIZ=python3 <PROFILE>/skills/lawrenzo-tools/scripts/setup_wizard.py
$WIZ status | start | answer "..." --chat-id ID --user-id ID
```

Trigger: `setup`, `configura`, `/start` se non configured.

## Tool CLI

```bash
TOOLS=<PROFILE>/skills/lawrenzo-tools/scripts/lawrenzo_tools.py
CFG=<PROFILE>/skills/lawrenzo-tools/scripts/configure_legal.py

python3 $TOOLS generate_contract --contract_type nda
python3 $TOOLS gdpr_check --data_collected "email,nome"
python3 $TOOLS analyze_terms --terms_text "..."
python3 $TOOLS regulatory_watch
```

Usano `legal-config.yaml` (cliente, foro, settore).

## Config admin

| Chat | Script |
|------|--------|
| `config mostra` | configure_legal.py show |
| `config cliente Nome` | set client.name |
| `config foro Milano` | set jurisdiction.foro |
| `config gruppo ID` | set telegram.group_chat_id |
| `config cron on` | cron.enabled + apply-cron |

## Anti-pattern

- Mai output senza disclaimer
- Mai foro diverso da config senza conferma admin
- Mai parere vincolante — sempre "bozza per revisione legale"
