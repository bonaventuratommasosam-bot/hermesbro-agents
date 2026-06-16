---
name: sentinel-tools
description: "Sentinel Audit — SSL, checklist, prodotti audit. Setup: setup"
---

```bash
TOOLS=<PROFILE>/skills/sentinel-tools/scripts/sentinel_tools.py
python3 $TOOLS ssl --domain DOMINIO_PLACEHOLDER
python3 $TOOLS checklist --target_type vps
python3 $TOOLS backup
python3 $TOOLS products
```
