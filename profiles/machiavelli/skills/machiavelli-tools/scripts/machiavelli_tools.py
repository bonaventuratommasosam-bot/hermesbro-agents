#!/usr/bin/env python3
"""Machiavelli Orchestrator tools."""
import argparse
import json
import uuid
from datetime import datetime

from orchestrator_config import get_dotted, load, org_context, save, set_dotted

FLEET_ROLES = {
    "frank": "Coding & DevOps",
    "groot": "Inventory & Shopping",
    "contabile": "Accounting",
    "ducato": "Finance",
    "lawrenzo": "Legal",
    "designbro": "Brand Design",
    "wannabe": "R&D Lab",
    "sentinel": "Security",
    "el-froggo": "Fleet Lead",
}


def fleet_status(ctx: dict) -> dict:
    roster = []
    for name in ctx["agents"]:
        roster.append({"agent": name, "role": FLEET_ROLES.get(name, "Agent"), "status": "demo"})
    return {"tool": "fleet_status", "timestamp": datetime.now().isoformat(), "org": ctx["name"], "agents": roster, "max_parallel": ctx["max_parallel"]}


def dispatch_task(target: str, task: str, priority: str = "normal") -> dict:
    cfg = load()
    queue = list(get_dotted(cfg, "dispatch.queue") or [])
    item = {
        "id": f"DISP-{uuid.uuid4().hex[:6]}",
        "target": target.lower(),
        "task": task,
        "priority": priority,
        "status": "queued",
        "created": datetime.now().isoformat(),
    }
    queue.append(item)
    set_dotted(cfg, "dispatch.queue", queue)
    save(cfg)
    return {"tool": "dispatch_task", **item, "hint": f"Bus: bus-send.py send machiavelli {target} \"{task}\""}


def workflow_plan(goal: str, ctx: dict) -> dict:
    steps = [
        {"step": 1, "agent": "machiavelli", "action": "scope & debate"},
        {"step": 2, "agent": "frank", "action": "implement core"},
        {"step": 3, "agent": "sentinel", "action": "security review"},
        {"step": 4, "agent": "frank", "action": "deploy"},
        {"step": 5, "agent": "el-froggo", "action": "founder report"},
    ]
    return {"tool": "workflow_plan", "goal": goal, "org": ctx["name"], "steps": steps, "estimated_agents": min(len(ctx["agents"]), ctx["max_parallel"])}


def debate(topic: str, rounds: int = 2) -> dict:
    return {
        "tool": "debate",
        "topic": topic,
        "rounds": rounds,
        "positions": {
            "pro": [f"Pro: {topic} riduce complessità operativa", "Pro: time-to-market più rapido"],
            "con": [f"Con: {topic} aumenta debito tecnico", "Con: serve più coordinamento"],
        },
        "verdict": "Serve decisione admin — rispondi *approva pro* o *approva con*",
    }


def queue_status(ctx: dict) -> dict:
    pending = [q for q in ctx["queue"] if q.get("status") == "queued"]
    return {"tool": "queue_status", "pending": len(pending), "items": pending[-10:]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("tool")
    p.add_argument("--target", default="frank")
    p.add_argument("--task", default="")
    p.add_argument("--goal", default="")
    p.add_argument("--topic", default="")
    p.add_argument("--priority", default="normal")
    args = p.parse_args()

    ctx = org_context()
    tools = {
        "fleet": lambda: fleet_status(ctx),
        "dispatch": lambda: dispatch_task(args.target, args.task or "Task senza titolo", args.priority),
        "plan": lambda: workflow_plan(args.goal or "Obiettivo non specificato", ctx),
        "debate": lambda: debate(args.topic or "Architettura monolite vs microservizi", ctx["debate_rounds"]),
        "queue": lambda: queue_status(ctx),
    }
    fn = tools.get(args.tool)
    out = fn() if fn else {"error": f"Unknown: {args.tool}", "available": list(tools)}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
