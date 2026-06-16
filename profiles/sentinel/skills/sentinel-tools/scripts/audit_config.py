#!/usr/bin/env python3
"""Load/save Sentinel Audit config."""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

DEFAULTS: dict[str, Any] = {
    "client": {"name": "", "default_domain": "DOMINIO_PLACEHOLDER", "timezone": "Europe/Rome"},
    "audit": {"smart_contract_sla_hours": 48, "vps_audit_sla_hours": 24, "min_score_alert": 60},
    "telegram": {"group_chat_id": "", "admin_chat_id": ""},
    "roles": {"admin": []},
    "queue": {"pending": []},
    "cron": {"queue_process": "*/15 * * * *", "enabled": False},
    "language": {"default": "it"},
}


def profile_root() -> Path:
    return Path(__file__).resolve().parents[3]


def config_path(root: Path | None = None) -> Path:
    return (root or profile_root()) / "audit-config.yaml"


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
    return _deep_merge(DEFAULTS, yaml.safe_load(path.read_text(encoding="utf-8")) or {})


def save(cfg: dict[str, Any], root: Path | None = None) -> Path:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    path = config_path(root)
    path.write_text(yaml.dump(cfg, default_flow_style=False, allow_unicode=True, sort_keys=False), encoding="utf-8")
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


def audit_context(cfg: dict | None = None) -> dict:
    c = cfg or load()
    return {
        "client": (get_dotted(c, "client.name") or "Cliente").strip(),
        "domain": (get_dotted(c, "client.default_domain") or "DOMINIO_PLACEHOLDER").strip(),
        "sc_sla": int(get_dotted(c, "audit.smart_contract_sla_hours") or 48),
        "vps_sla": int(get_dotted(c, "audit.vps_audit_sla_hours") or 24),
    }


def validate(cfg: dict | None = None) -> dict[str, Any]:
    c = cfg or load()
    errors, warnings = [], []
    if not (get_dotted(c, "client.name") or "").strip():
        warnings.append("client.name non impostato")
    if get_dotted(c, "cron.enabled") and not get_dotted(c, "telegram.group_chat_id"):
        errors.append("cron.enabled senza telegram.group_chat_id")
    return {"ok": len(errors) == 0, "errors": errors, "warnings": warnings, "configured": bool((get_dotted(c, "client.name") or "").strip())}
