---
name: machiavelli-tools
description: "Machiavelli — fleet, dispatch, workflow plan, debate. Setup: setup"
---

```bash
TOOLS=<PROFILE>/skills/machiavelli-tools/scripts/machiavelli_tools.py
python3 $TOOLS fleet
python3 $TOOLS dispatch --target frank --task "Fix API health"
python3 $TOOLS plan --goal "Lancio feature pagamenti"
python3 $TOOLS debate --topic "Monolite vs microservizi"
python3 $TOOLS queue
```
