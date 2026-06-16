#!/usr/bin/env python3
"""Load/save GROOT Brigata client config (brigata-config.yaml)."""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

DEFAULTS: dict[str, Any] = {
    "venue": {"name": "", "concept": "", "timezone": "Europe/Rome"},
    "telegram": {
        "group_chat_id": "",
        "admin_chat_id": "",
        "allow_all_users": True,
        "whitelist_ids": [],
    },
    "google_sheets": {
        "spreadsheet_id": "",
        "tabs": {
            "lista_spesa": "LISTA_SPESA",
            "magazzino": "MAGAZZINO",
            "ordini": "ORDINI",
            "memoria": "MEMORIA",
            "promemoria": "PROMEMORIA",
        },
    },
    "operations": {
        "merge_same_day": True,
        "target_food_cost_pct": 32,
        "service_time": "20:00",
        "pause_proactive": False,
    },
    "roles": {"admin": [], "chef": [], "squad": []},
    "cron": {
        "morning": "30 7 * * 1-6",
        "post_service": "30 23 * * *",
        "weekly": "0 8 * * 1",
        "sheets_ping": "0 */6 * * *",
        "enabled": False,
    },
    "language": {"default": "it"},
}


def profile_root() -> Path:
    # scripts/ -> groot-tools/ -> skills/ -> profile/
    return Path(__file__).resolve().parents[3]


def config_path(root: Path | None = None) -> Path:
    return (root or profile_root()) / "brigata-config.yaml"


def _deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load(root: Path | None = None) -> dict[str, Any]:
    path = config_path(root)
    if not path.exists():
        return copy.deepcopy(DEFAULTS)
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return _deep_merge(DEFAULTS, data)


def save(cfg: dict[str, Any], root: Path | None = None) -> Path:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    path = config_path(root)
    path.write_text(
        yaml.dump(cfg, default_flow_style=False, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return path


def get_dotted(cfg: dict, key: str) -> Any:
    cur: Any = cfg
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def set_dotted(cfg: dict, key: str, value: Any) -> dict:
    parts = key.split(".")
    cur = cfg
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
    cur[parts[-1]] = value
    return cfg


def sheet_id(cfg: dict | None = None) -> str:
    c = cfg or load()
    return (get_dotted(c, "google_sheets.spreadsheet_id") or "").strip()


def lista_spesa_tab(cfg: dict | None = None) -> str:
    c = cfg or load()
    return get_dotted(c, "google_sheets.tabs.lista_spesa") or "LISTA_SPESA"


def validate(cfg: dict | None = None) -> dict[str, Any]:
    c = cfg or load()
    errors = []
    warnings = []
    if not get_dotted(c, "google_sheets.spreadsheet_id"):
        warnings.append("google_sheets.spreadsheet_id non impostato — lista spesa in coda locale")
    if not get_dotted(c, "telegram.group_chat_id"):
        warnings.append("telegram.group_chat_id non impostato — cron disabilitati")
    if get_dotted(c, "cron.enabled") and not get_dotted(c, "telegram.group_chat_id"):
        errors.append("cron.enabled=true ma manca telegram.group_chat_id")
    admins = get_dotted(c, "roles.admin") or []
    if not admins:
        warnings.append("roles.admin vuoto — nessun admin per alert tecnici")
    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "configured": bool(get_dotted(c, "google_sheets.spreadsheet_id")),
    }
