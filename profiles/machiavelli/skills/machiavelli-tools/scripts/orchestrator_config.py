#!/usr/bin/env python3
"""Load/save Machiavelli Orchestrator config."""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

DEFAULTS: dict[str, Any] = {
    "org": {"name": "", "max_parallel": 3, "debate_rounds": 2, "timezone": "Europe/Rome"},
    "fleet": {"agents": [], "default_priority": "normal"},
    "workflows": {"auto_dispatch": False, "require_approval": True},
    "telegram": {"group_chat_id": "", "admin_chat_id": ""},
    "roles": {"admin": []},
    "dispatch": {"queue": []},
    "cron": {"daily_brief": "0 8 * * *", "enabled": False},
    "language": {"default": "it"},
}

SQUAD_DEFAULT = ["frank", "groot", "contabile", "ducato", "lawrenzo", "designbro", "wannabe", "sentinel"]


def profile_root() -> Path:
    return Path(__file__).resolve().parents[3]


def config_path(root: Path | None = None) -> Path:
    return (root or profile_root()) / "orchestrator-config.yaml"


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


def org_context(cfg: dict | None = None) -> dict:
    c = cfg or load()
    agents = get_dotted(c, "fleet.agents") or SQUAD_DEFAULT
    return {
        "name": (get_dotted(c, "org.name") or "Organizzazione").strip(),
        "agents": agents,
        "max_parallel": int(get_dotted(c, "org.max_parallel") or 3),
        "debate_rounds": int(get_dotted(c, "org.debate_rounds") or 2),
        "queue": get_dotted(c, "dispatch.queue") or [],
    }


def validate(cfg: dict | None = None) -> dict[str, Any]:
    c = cfg or load()
    errors, warnings = [], []
    if not (get_dotted(c, "org.name") or "").strip():
        warnings.append("org.name non impostato")
    if get_dotted(c, "cron.enabled") and not get_dotted(c, "telegram.group_chat_id"):
        errors.append("cron.enabled senza telegram.group_chat_id")
    return {"ok": len(errors) == 0, "errors": errors, "warnings": warnings, "configured": bool((get_dotted(c, "org.name") or "").strip())}
