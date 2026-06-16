#!/usr/bin/env python3
"""CLI per configurazione cliente GROOT Brigata."""
import argparse
import json
import re
import sys
from pathlib import Path

from brigata_config import (
    config_path,
    get_dotted,
    load,
    save,
    set_dotted,
    validate,
    profile_root,
)

CRON_JOBS = profile_root() / "cron" / "jobs.json"


def _parse_value(raw: str) -> object:
    if raw.lower() in ("true", "false"):
        return raw.lower() == "true"
    if re.match(r"^-?\d+$", raw):
        return int(raw)
    if "," in raw and not raw.startswith('"'):
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if all(re.match(r"^-?\d+$", p) for p in parts):
            return [int(p) for p in parts]
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    return raw


def cmd_show(_: argparse.Namespace) -> None:
    cfg = load()
    print(json.dumps(cfg, indent=2, ensure_ascii=False))
    print("\n--- validate ---")
    print(json.dumps(validate(cfg), indent=2, ensure_ascii=False))


def cmd_set(args: argparse.Namespace) -> None:
    cfg = load()
    set_dotted(cfg, args.key, _parse_value(args.value))
    path = save(cfg)
    print(json.dumps({"saved": str(path), "key": args.key, "value": get_dotted(cfg, args.key)}, ensure_ascii=False))


def cmd_init(_: argparse.Namespace) -> None:
    path = config_path()
    if path.exists():
        print(json.dumps({"status": "exists", "path": str(path)}, ensure_ascii=False))
        return
    save(load())
    print(json.dumps({"status": "created", "path": str(path)}, ensure_ascii=False))


def cmd_validate(_: argparse.Namespace) -> None:
    print(json.dumps(validate(load()), indent=2, ensure_ascii=False))


def cmd_apply_cron(_: argparse.Namespace) -> None:
    cfg = load()
    v = validate(cfg)
    if not get_dotted(cfg, "cron.enabled"):
        print(json.dumps({"status": "skipped", "reason": "cron.enabled=false"}, ensure_ascii=False))
        return
    group = str(get_dotted(cfg, "telegram.group_chat_id") or "").strip()
    admin = str(get_dotted(cfg, "telegram.admin_chat_id") or "").strip()
    if not group:
        print(json.dumps({"status": "error", "reason": "telegram.group_chat_id required"}, ensure_ascii=False))
        sys.exit(1)
    if not CRON_JOBS.exists():
        print(json.dumps({"status": "error", "reason": f"missing {CRON_JOBS}"}, ensure_ascii=False))
        sys.exit(1)

    data = json.loads(CRON_JOBS.read_text(encoding="utf-8"))
    tz = get_dotted(cfg, "venue.timezone") or "Europe/Rome"
    schedules = {
        "groot-brigata-am": get_dotted(cfg, "cron.morning"),
        "groot-brigata-post": get_dotted(cfg, "cron.post_service"),
        "groot-brigata-week": get_dotted(cfg, "cron.weekly"),
        "groot-brigata-sheets-ping": get_dotted(cfg, "cron.sheets_ping"),
    }
    for job in data.get("jobs", []):
        jid = job.get("id", "")
        if jid in schedules and schedules[jid]:
            job.setdefault("schedule", {})["expr"] = schedules[jid]
            job["schedule"]["timezone"] = tz
        if jid == "groot-brigata-sheets-ping":
            deliver = f"telegram:{admin or group}"
        else:
            deliver = f"telegram:{group}"
        job["deliver"] = deliver
        job["state"] = "scheduled"

    CRON_JOBS.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": "ok", "jobs": len(data.get("jobs", [])), "group": group}, ensure_ascii=False))


def main() -> None:
    p = argparse.ArgumentParser(description="GROOT Brigata client configuration")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("show")
    sub.add_parser("init")
    sub.add_parser("validate")
    sub.add_parser("apply-cron")

    s = sub.add_parser("set")
    s.add_argument("key")
    s.add_argument("value")

    args = p.parse_args()
    handlers = {
        "show": cmd_show,
        "init": cmd_init,
        "validate": cmd_validate,
        "apply-cron": cmd_apply_cron,
        "set": cmd_set,
    }
    handlers[args.cmd](args)


if __name__ == "__main__":
    main()
