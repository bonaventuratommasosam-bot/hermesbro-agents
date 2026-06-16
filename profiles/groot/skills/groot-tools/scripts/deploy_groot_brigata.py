#!/usr/bin/env python3
"""Deploy GROOT Brigata — replace old groot profile content (run as root on VPS)."""
import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

LOCAL = Path("/tmp/groot-brigata")
PROFILE = Path("{{HERMES_HOME}}")
SKILL = PROFILE / "skills/groot-tools"
SCRIPTS = SKILL / "scripts"
WEB = Path("/var/www/hermesbro/os/agents")
SRC = Path("{{HERMES_HOME}}/../../hermesbro-os-app/src/agents")
SYSTEMD = Path("/etc/systemd/system/hermes-squad-groot.service")


def run(cmd: str) -> str:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd}\n{r.stderr[:600]}")
    return (r.stdout or "").strip()


def backup(path: Path) -> None:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(path, path.with_suffix(path.suffix + f".bak_{ts}"))


def copy(name: str, dst: Path) -> None:
    src = LOCAL / name
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())
    print(f"  ok {name} -> {dst}")


def patch_config() -> None:
    cfg = PROFILE / "brigata-config.yaml"
    backup(cfg)
    text = cfg.read_text(encoding="utf-8")

    brigata_block = """
brigata:
  sheet_id: "{{GOOGLE_SHEETS_ID}}"
  merge_same_day: true
  target_food_cost_pct: 32
  pause_proactive: false
  service_time: "20:00"
  roles:
    admin: []
    chef: []
    squad: []
"""
    if "brigata:" not in text:
        text = text.rstrip() + "\n" + brigata_block

    cfg.write_text(text, encoding="utf-8")
    print("  ok brigata-config.yaml patched (brigata block)")


def patch_systemd() -> None:
    if not SYSTEMD.exists():
        return
    backup(SYSTEMD)
    text = SYSTEMD.read_text(encoding="utf-8")
    text = text.replace(
        "Hermes Squad - groot (demo — activate on command)",
        "Hermes Squad - GROOT Brigata (scorte/lista spesa — activate on command)",
    )
    SYSTEMD.write_text(text, encoding="utf-8")
    run("systemctl daemon-reload")
    print("  ok systemd description updated")


def main() -> None:
    print("=== GROOT Brigata deploy ===")

    # Core identity
    for name, dst in [
        ("SOUL.md", PROFILE / "SOUL.md"),
        ("GOAL.md", PROFILE / "GOAL.md"),
        ("SUBGOALS.md", PROFILE / "SUBGOALS.md"),
        ("ONBOARDING_BRIGATA.txt", PROFILE / "ONBOARDING_BRIGATA.txt"),
    ]:
        backup(dst)
        copy(name, dst)

    # Skill
    backup(SKILL / "SKILL.md")
    copy("groot-tools-SKILL.md", SKILL / "SKILL.md")

    copy("lista_spesa.py", SCRIPTS / "lista_spesa.py")
    run(f"chmod 755 {SCRIPTS / 'lista_spesa.py'}")

    # Cron
    cron_dst = PROFILE / "cron/jobs.json"
    backup(cron_dst)
    copy("cron-jobs.json", cron_dst)

    # Config + systemd
    patch_config()
    patch_systemd()

    # UI
    for name in ("groot.html", "index.html"):
        copy(name, SRC / name)
        if WEB.parent.exists():
            copy(name, WEB / name)

    # Verify files
    soul = (PROFILE / "SOUL.md").read_text(encoding="utf-8")
    if "GROOT Brigata" not in soul:
        raise RuntimeError("SOUL.md missing GROOT Brigata identity")
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if "LISTA_SPESA" not in skill:
        raise RuntimeError("SKILL.md missing LISTA_SPESA")

    status = run("systemctl is-active hermes-squad-groot.service || true")
    print("GROOT_SERVICE", status, "(not starting — demo policy)")

    print("DONE — GROOT Brigata profile ready. Activate with: activate-demo-bot.sh groot")


if __name__ == "__main__":
    main()
