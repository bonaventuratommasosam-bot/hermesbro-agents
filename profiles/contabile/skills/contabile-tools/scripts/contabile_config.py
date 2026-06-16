#!/usr/bin/env python3
"""Load/save ContAIbile config (contabile-config.yaml)."""
from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

DEFAULTS: dict[str, Any] = {
    "company": {
        "name": "",
        "piva": "",
        "regime": "forfettario",
        "iva_regime": "trimestrale",
        "sector": "",
        "timezone": "Europe/Rome",
    },
    "fiscal": {
        "default_iva": 22,
        "food_cost_alert_pct": 35,
        "anomaly_threshold_eur": 500,
    },
    "telegram": {
        "group_chat_id": "",
        "admin_chat_id": "",
        "alert_days_before": 7,
    },
    "roles": {"admin": []},
    "ledger": {"path": "cache/ledger.jsonl"},
    "cron": {"deadline_check": "0 8 * * 1-5", "weekly_report": "0 9 * * 1", "enabled": False},
    "language": {"default": "it"},
}


def profile_root() -> Path:
    """Return the profile root directory.

    Priority:
    1. HERMES_PROFILE_ROOT env var (set by deployment)
    2. Fallback: 3 levels up from this file (standalone dev)
    """
    env = os.environ.get("HERMES_PROFILE_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[3]


def config_path(root: Path | None = None) -> Path:
    return (root or profile_root()) / "contabile-config.yaml"


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
        raise RuntimeError("PyYAML required")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return _deep_merge(DEFAULTS, data)


def save(cfg: dict[str, Any], root: Path | None = None) -> Path:
    if yaml is None:
        raise RuntimeError("PyYAML required")
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


def company_context(cfg: dict | None = None) -> dict[str, str | int | float]:
    c = cfg or load()
    return {
        "company": (get_dotted(c, "company.name") or "Azienda").strip(),
        "piva": (get_dotted(c, "company.piva") or "").strip(),
        "regime": (get_dotted(c, "company.regime") or "forfettario").strip(),
        "iva_regime": (get_dotted(c, "company.iva_regime") or "trimestrale").strip(),
        "sector": (get_dotted(c, "company.sector") or "servizi").strip(),
        "default_iva": int(get_dotted(c, "fiscal.default_iva") or 22),
        "food_cost_alert_pct": float(get_dotted(c, "fiscal.food_cost_alert_pct") or 35),
    }


def ledger_path(cfg: dict | None = None) -> Path:
    c = cfg or load()
    rel = get_dotted(c, "ledger.path") or "cache/ledger.jsonl"
    return profile_root() / rel


def validate(cfg: dict | None = None) -> dict[str, Any]:
    c = cfg or load()
    errors, warnings = [], []
    if not (get_dotted(c, "company.name") or "").strip():
        warnings.append("company.name non impostato — usa setup wizard")
    if get_dotted(c, "cron.enabled") and not get_dotted(c, "telegram.group_chat_id"):
        errors.append("cron.enabled=true ma manca telegram.group_chat_id")
    if not get_dotted(c, "roles.admin"):
        warnings.append("roles.admin vuoto — nessun admin per alert scadenze")
    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "configured": bool((get_dotted(c, "company.name") or "").strip()),
    }
