#!/usr/bin/env python3
"""GROOT Brigata — LISTA_SPESA Google Sheets operations (client-config driven)."""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from brigata_config import load, sheet_id, lista_spesa_tab, validate  # noqa: E402

CACHE = Path(__file__).resolve().parents[3] / "cache" / "pending-spesa.jsonl"
GAPI = os.environ.get(
    "HERMES_GAPI",
    f"python3 {os.environ.get('HERMES_HOME', '{{HERMES_HOME}}')}/skills/productivity/google-workspace/scripts/google_api.py",
)


def run_gapi(*args: str) -> dict:
    parts = GAPI.split()
    cmd = parts + list(args)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:500] or r.stdout[:500])
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"raw": r.stdout.strip()}


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _cfg() -> dict:
    return load()


def _sid() -> str:
    sid = sheet_id(_cfg())
    if not sid:
        raise ValueError("google_sheets.spreadsheet_id non configurato in brigata-config.yaml")
    return sid


def _range() -> str:
    tab = lista_spesa_tab(_cfg())
    return f"{tab}!A1:I500"


def get_rows() -> list[list]:
    data = run_gapi("sheets", "get", _sid(), _range())
    rows = data.get("values") or data.get("raw", [])
    if isinstance(rows, str):
        return []
    if rows and isinstance(rows[0], dict):
        return []
    return rows if rows else []


def append_row(row: list) -> None:
    run_gapi(
        "sheets",
        "append",
        _sid(),
        "A:I",
        "--values",
        json.dumps([row], ensure_ascii=False),
    )


def queue_local(row: list) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def cmd_add(args: argparse.Namespace) -> dict:
    row = [
        today(),
        args.item,
        args.qty or "1",
        args.unit or "",
        args.priorita or "normale",
        "da_comprare",
        args.user or "squad",
        args.note or "",
        now_str(),
    ]
    try:
        append_row(row)
        status = "ok"
        exc_msg = ""
    except Exception as exc:
        queue_local(row)
        status = "queued"
        exc_msg = str(exc)

    rows = []
    try:
        raw = get_rows()
        for r in raw[1:]:
            if len(r) < 6:
                continue
            stato = r[5] if len(r) > 5 else ""
            if stato == "da_comprare" and (not r[0] or r[0] == today()):
                rows.append(r)
    except Exception:
        pass

    return {
        "tool": "lista_spesa_add",
        "status": status,
        "item": args.item,
        "open_today": len(rows),
        "error": exc_msg or None,
        "config_ok": validate(_cfg()).get("configured"),
    }


def cmd_list(args: argparse.Namespace) -> dict:
    raw = get_rows()
    items = []
    for r in raw[1:]:
        if len(r) < 2:
            continue
        stato = r[5] if len(r) > 5 else "da_comprare"
        priorita = r[4] if len(r) > 4 else "normale"
        if args.stato and stato != args.stato:
            continue
        if args.priorita and priorita != args.priorita:
            continue
        items.append(
            {
                "data": r[0],
                "item": r[1],
                "qty": r[2] if len(r) > 2 else "",
                "unit": r[3] if len(r) > 3 else "",
                "priorita": priorita,
                "stato": stato,
                "user": r[6] if len(r) > 6 else "",
            }
        )
    limit = args.limit or 15
    return {
        "tool": "lista_spesa_list",
        "count": len(items),
        "items": items[:limit],
    }


def cmd_update(args: argparse.Namespace) -> dict:
    raw = get_rows()
    target = args.item.lower()
    updated = False
    for i, r in enumerate(raw[1:], start=2):
        if len(r) < 2:
            continue
        if r[1].lower() == target and (not args.stato_filter or r[5] == args.stato_filter):
            run_gapi(
                "sheets",
                "update",
                _sid(),
                f"F{i}",
                "--values",
                json.dumps([[args.stato]], ensure_ascii=False),
            )
            run_gapi(
                "sheets",
                "update",
                _sid(),
                f"I{i}",
                "--values",
                json.dumps([[now_str()]], ensure_ascii=False),
            )
            updated = True
            break
    return {
        "tool": "lista_spesa_update",
        "item": args.item,
        "stato": args.stato,
        "updated": updated,
    }


def cmd_ping(_: argparse.Namespace) -> dict:
    v = validate(_cfg())
    if not v.get("configured"):
        return {
            "tool": "sheets_ping",
            "ok": False,
            "error": "Configura google_sheets.spreadsheet_id in brigata-config.yaml",
            "warnings": v.get("warnings", []),
        }
    try:
        rows = get_rows()
        return {"tool": "sheets_ping", "ok": True, "rows": len(rows)}
    except Exception as exc:
        return {"tool": "sheets_ping", "ok": False, "error": str(exc)}


def main() -> None:
    p = argparse.ArgumentParser(description="GROOT Brigata LISTA_SPESA")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--item", required=True)
    a.add_argument("--qty", default="1")
    a.add_argument("--unit", default="")
    a.add_argument("--priorita", default="normale")
    a.add_argument("--user", default="squad")
    a.add_argument("--note", default="")

    l = sub.add_parser("list")
    l.add_argument("--stato", default="da_comprare")
    l.add_argument("--priorita", default="")
    l.add_argument("--limit", type=int, default=15)

    u = sub.add_parser("update")
    u.add_argument("--item", required=True)
    u.add_argument("--stato", required=True)
    u.add_argument("--stato_filter", default="da_comprare")
    u.add_argument("--user", default="chef")

    sub.add_parser("ping")

    args = p.parse_args()
    handlers = {
        "add": cmd_add,
        "list": cmd_list,
        "update": cmd_update,
        "ping": cmd_ping,
    }
    result = handlers[args.cmd](args)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
