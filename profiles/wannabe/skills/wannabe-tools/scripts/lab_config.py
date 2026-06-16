#!/usr/bin/env python3
"""Load/save Wannabe Lab config."""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

DEFAULTS: dict[str, Any] = {
    "lab": {"name": "", "focus": "skills", "supervisor": "frank", "timezone": "Europe/Rome"},
    "experiments": {"max_active": 5, "require_review": True},
    "telegram": {"group_chat_id": "", "admin_chat_id": ""},
    "roles": {"admin": []},
    "queue": {"items": []},
    "cron": {"weekly_digest": "0 10 * * 5", "enabled": False},
    "language": {"default": "it"},
}


def profile_root() -> Path:
    return Path(__file__).resolve().parents[3]


def config_path(root: Path | None = None) -> Path:
    return (root or profile_root()) / "lab-config.yaml"


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


def lab_context(cfg: dict | None = None) -> dict:
    c = cfg or load()
    return {
        "name": (get_dotted(c, "lab.name") or "Lab").strip(),
        "focus": (get_dotted(c, "lab.focus") or "skills").strip(),
        "supervisor": (get_dotted(c, "lab.supervisor") or "frank").strip(),
        "max_active": int(get_dotted(c, "experiments.max_active") or 5),
        "items": get_dotted(c, "queue.items") or [],
    }


def validate(cfg: dict | None = None) -> dict[str, Any]:
    c = cfg or load()
    errors, warnings = [], []
    if not (get_dotted(c, "lab.name") or "").strip():
        warnings.append("lab.name non impostato")
    if get_dotted(c, "cron.enabled") and not get_dotted(c, "telegram.group_chat_id"):
        errors.append("cron.enabled senza telegram.group_chat_id")
    return {"ok": len(errors) == 0, "errors": errors, "warnings": warnings, "configured": bool((get_dotted(c, "lab.name") or "").strip())}