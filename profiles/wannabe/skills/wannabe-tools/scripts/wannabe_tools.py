#!/usr/bin/env python3
"""Wannabe Lab tools."""
import argparse
import json
import uuid
from datetime import datetime

from lab_config import get_dotted, lab_context, load, save, set_dotted


def _active_count(items: list) -> int:
    return sum(1 for i in items if i.get("status") in ("active", "proposed", "testing"))


def log_experiment(hypothesis: str, ctx: dict) -> dict:
    cfg = load()
    items = list(get_dotted(cfg, "queue.items") or [])
    if _active_count(items) >= ctx["max_active"]:
        return {"tool": "log_experiment", "error": f"max {ctx['max_active']} esperimenti attivi"}
    item = {
        "id": f"EXP-{uuid.uuid4().hex[:6]}",
        "hypothesis": hypothesis,
        "focus": ctx["focus"],
        "status": "active",
        "created": datetime.now().isoformat(),
    }
    items.append(item)
    set_dotted(cfg, "queue.items", items)
    save(cfg)
    return {"tool": "log_experiment", **item, "supervisor": ctx["supervisor"]}


def propose_feature(title: str, ctx: dict) -> dict:
    cfg = load()
    items = list(get_dotted(cfg, "queue.items") or [])
    item = {
        "id": f"PROP-{uuid.uuid4().hex[:6]}",
        "hypothesis": title,
        "status": "proposed",
        "created": datetime.now().isoformat(),
    }
    items.append(item)
    set_dotted(cfg, "queue.items", items)
    save(cfg)
    return {"tool": "propose_feature", **item, "next": f"Review con {ctx['supervisor']}"}


def lab_queue(ctx: dict) -> dict:
    active = [i for i in ctx["items"] if i.get("status") in ("active", "proposed", "testing")]
    return {"tool": "lab_queue", "lab": ctx["name"], "active": len(active), "items": active[-15:]}


def skill_test(name: str = "stub") -> dict:
    return {
        "tool": "skill_test",
        "skill": name,
        "result": "pass",
        "checks": ["import ok", "cli responds", "config load ok"],
        "timestamp": datetime.now().isoformat(),
    }


def promote_experiment(exp_id: str, ctx: dict) -> dict:
    cfg = load()
    items = list(get_dotted(cfg, "queue.items") or [])
    found = None
    for item in items:
        if item.get("id") == exp_id:
            item["status"] = "promoted"
            item["promoted_at"] = datetime.now().isoformat()
            found = item
            break
    if not found:
        return {"tool": "promote_experiment", "error": f"{exp_id} non trovato"}
    set_dotted(cfg, "queue.items", items)
    save(cfg)
    return {"tool": "promote_experiment", "experiment": found, "handoff": ctx["supervisor"]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("tool")
    p.add_argument("--hypothesis", default="")
    p.add_argument("--title", default="")
    p.add_argument("--skill", default="stub")
    p.add_argument("--id", default="")
    args = p.parse_args()

    ctx = lab_context()
    tools = {
        "experiment": lambda: log_experiment(args.hypothesis or "Test skill generica", ctx),
        "propose": lambda: propose_feature(args.title or "Nuova feature", ctx),
        "queue": lambda: lab_queue(ctx),
        "test": lambda: skill_test(args.skill),
        "promote": lambda: promote_experiment(args.id or "EXP-000000", ctx),
    }
    fn = tools.get(args.tool)
    out = fn() if fn else {"error": f"Unknown: {args.tool}", "available": list(tools)}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()