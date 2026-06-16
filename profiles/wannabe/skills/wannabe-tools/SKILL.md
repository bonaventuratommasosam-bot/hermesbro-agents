---
name: wannabe-tools
description: "Wannabe Lab — esperimenti, proposte, test skill. Setup: setup"
---

```bash
TOOLS={{HERMES_HOME}}/profiles/wannabe/skills/wannabe-tools/scripts/wannabe_tools.py
python3 $TOOLS propose --title "Dark mode dashboard"
python3 $TOOLS experiment --hypothesis "Nuova skill bus-send"
python3 $TOOLS queue
python3 $TOOLS test --skill frank-tools
python3 $TOOLS promote --id EXP-abc123
```
