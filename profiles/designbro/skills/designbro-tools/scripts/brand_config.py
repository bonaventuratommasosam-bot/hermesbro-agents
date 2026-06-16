#!/usr/bin/env python3
"""Load/save DesignBro Studio client config (brand-config.yaml)."""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

DEFAULTS: dict[str, Any] = {
    "brand": {
        "name": "",
        "industry": "",
        "tagline": "",
        "keywords": "",
        "timezone": "Europe/Rome",
    },
    "visual": {
        "primary_color": "",
        "mood": "professional",
        "style": "modern",
    },
    "telegram": {
        "group_chat_id": "",
        "admin_chat_id": "",
        "allow_all_users": True,
        "require_approval": True,
    },
    "roles": {"admin": [], "reviewers": []},
    "output": {
        "formats": ["logo", "palette", "typography", "social", "menu"],
        "archive_dir": "cache/designs",
    },
    "cron": {"brand_checkin": "0 9 1 * *", "enabled": False},
    "language": {"default": "it"},
}


def profile_root() -> Path:
    return Path(__file__).resolve().parents[3]


def config_path(root: Path | None = None) -> Path:
    return (root or profile_root()) / "brand-config.yaml"


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


def brand_context(cfg: dict | None = None) -> dict[str, str]:
    c = cfg or load()
    return {
        "brand": (get_dotted(c, "brand.name") or "Brand").strip(),
        "industry": (get_dotted(c, "brand.industry") or "tech").strip(),
        "keywords": (get_dotted(c, "brand.keywords") or "").strip(),
        "style": (get_dotted(c, "visual.style") or "modern").strip(),
        "mood": (get_dotted(c, "visual.mood") or "professional").strip(),
        "primary_color": (get_dotted(c, "visual.primary_color") or "#1a1a2e").strip(),
    }


def validate(cfg: dict | None = None) -> dict[str, Any]:
    c = cfg or load()
    errors = []
    warnings = []
    if not (get_dotted(c, "brand.name") or "").strip():
        warnings.append("brand.name non impostato — usa setup wizard")
    if not (get_dotted(c, "telegram.group_chat_id") or "").strip():
        warnings.append("telegram.group_chat_id non impostato — preview solo in DM")
    if get_dotted(c, "cron.enabled") and not get_dotted(c, "telegram.group_chat_id"):
        errors.append("cron.enabled=true ma manca telegram.group_chat_id")
    admins = get_dotted(c, "roles.admin") or []
    if not admins:
        warnings.append("roles.admin vuoto — nessun admin per approvazioni")
    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "configured": bool((get_dotted(c, "brand.name") or "").strip()),
    }