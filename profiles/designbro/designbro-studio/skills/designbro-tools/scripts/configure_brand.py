#!/usr/bin/env python3
"""CLI per configurazione cliente DesignBro Studio."""
import argparse
import json
import re
import sys
from pathlib import Path

from brand_config import (
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
    if not get_dotted(cfg, "cron.enabled"):
        print(json.dumps({"status": "skipped", "reason": "cron.enabled=false"}, ensure_ascii=False))
        return
    group = str(get_dotted(cfg, "telegram.group_chat_id") or "").strip()
    if not group:
        print(json.dumps({"status": "error", "reason": "telegram.group_chat_id required"}, ensure_ascii=False))
        sys.exit(1)
    if not CRON_JOBS.exists():
        print(json.dumps({"status": "error", "reason": f"missing {CRON_JOBS}"}, ensure_ascii=False))
        sys.exit(1)

    data = json.loads(CRON_JOBS.read_text(encoding="utf-8"))
    schedule = get_dotted(cfg, "cron.brand_checkin") or "0 9 1 * *"
    brand = get_dotted(cfg, "brand.name") or "Brand"
    for job in data.get("jobs", []):
        if job.get("id") == "brand_checkin":
            job["schedule"] = schedule
            job["message"] = (
                f"🎨 Check-in brand kit — {brand}. "
                "Palette, font e logo ancora allineati? Scrivi *brand kit* per rivedere."
            )
            job["target"] = f"telegram:{group}"
    CRON_JOBS.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": "applied", "cron": str(CRON_JOBS), "schedule": schedule}, ensure_ascii=False))


def main() -> None:
    p = argparse.ArgumentParser(description="DesignBro Studio — configure brand")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show").set_defaults(func=cmd_show)
    sub.add_parser("init").set_defaults(func=cmd_init)
    sub.add_parser("validate").set_defaults(func=cmd_validate)
    sub.add_parser("apply-cron").set_defaults(func=cmd_apply_cron)
    sp = sub.add_parser("set")
    sp.add_argument("key")
    sp.add_argument("value")
    sp.set_defaults(func=cmd_set)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()