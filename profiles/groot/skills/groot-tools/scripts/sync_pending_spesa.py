#!/usr/bin/env python3
"""Sync cache/pending-spesa.jsonl → LISTA_SPESA when Sheets is back."""
import json
import subprocess
import sys
from pathlib import Path

PROFILE = Path(__file__).resolve().parents[3]
CACHE = PROFILE / "cache" / "pending-spesa.jsonl"
LISTA = PROFILE / "skills/groot-tools/scripts/lista_spesa.py"


def main() -> None:
    if not CACHE.exists():
        print(json.dumps({"synced": 0, "reason": "no queue"}))
        return
    lines = [ln for ln in CACHE.read_text(encoding="utf-8").splitlines() if ln.strip()]
    ok, fail = 0, 0
    remaining = []
    env = {**dict(__import__("os").environ), "HERMES_HOME": str(PROFILE), "DATA_DIR": str(PROFILE)}
    for ln in lines:
        row = json.loads(ln)
        item = row[1] if len(row) > 1 else "?"
        r = subprocess.run(
            ["python3", str(LISTA), "add", "--item", str(item), "--user", "sync_pending"],
            capture_output=True,
            text=True,
            env=env,
            timeout=60,
        )
        if r.returncode == 0 and '"status": "ok"' in (r.stdout or ""):
            ok += 1
        else:
            fail += 1
            remaining.append(ln)
    CACHE.write_text("\n".join(remaining) + ("\n" if remaining else ""), encoding="utf-8")
    print(json.dumps({"synced": ok, "failed": fail, "remaining": len(remaining)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
