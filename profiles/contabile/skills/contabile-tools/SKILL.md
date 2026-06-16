---
name: contabile-tools
description: "ContAIbile — movimenti, IVA, scadenze. Setup: setup (5 domande)."
---

# Skill: contabile-tools

Leggi `contabile-config.yaml`. Wizard se non configured.

```bash
WIZ=<PROFILE>/skills/contabile-tools/scripts/setup_wizard.py
TOOLS=<PROFILE>/skills/contabile-tools/scripts/contabile_tools.py

python3 $TOOLS register_ricavo --amount 500 --description "Consulenza"
python3 $TOOLS register_spesa --amount 120 --description "Fornitore"
python3 $TOOLS compute_iva
python3 $TOOLS scadenze --days 30
python3 $TOOLS summary
python3 $TOOLS food_cost --revenue 5000 --food_cost 1600
```

Config: `configure_contabile.py show|set|validate|apply-cron`
