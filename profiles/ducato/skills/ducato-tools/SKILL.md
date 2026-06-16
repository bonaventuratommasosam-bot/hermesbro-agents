---
name: ducato-tools
description: "Ducato Finance — portafoglio, scenari, break-even. Setup: setup"
---

```bash
TOOLS=<PROFILE>/skills/ducato-tools/scripts/ducato_tools.py
python3 $TOOLS portfolio
python3 $TOOLS scenarios --growth 5 --months 12
python3 $TOOLS break_even --fixed 5000 --price 25 --variable 8
python3 $TOOLS runway --cash 15000
python3 $TOOLS add_asset --name BTC --value 2000 --class crypto
```
