#!/usr/bin/env python3
"""El-froggo tools — fleet lead + crypto intel (informativo)."""
import argparse
import json
import subprocess
import uuid
from datetime import datetime

from fleet_lead_config import get_dotted, lead_context, load, save, set_dotted


def market_overview() -> dict:
    return {
        "tool": "market_overview",
        "timestamp": datetime.now().isoformat(),
        "sectors": {"DeFi": {"trend": "neutral"}, "L2": {"trend": "bullish"}},
        "disclaimer": "Intel informativo — non consulenza. Trading prod: H2BB/GribbitO separati.",
    }


def fleet_pulse(ctx: dict) -> dict:
    roster = []
    for name in ctx["agents"]:
        try:
            r = subprocess.run(
                ["systemctl", "is-active", f"hermes-squad-{name}.service"],
                capture_output=True, text=True, timeout=5,
            )
            svc = (r.stdout or "").strip() if r.returncode == 0 else "inactive"
        except Exception:
            svc = "unknown"
        roster.append({"agent": name, "service": svc, "status": "online" if svc == "active" else "demo"})
    online = sum(1 for x in roster if x["service"] == "active")
    return {"tool": "fleet_pulse", "timestamp": datetime.now().isoformat(), "org": ctx["org"], "online": online, "total": len(roster), "agents": roster}


def daily_brief(ctx: dict) -> dict:
    pulse = fleet_pulse(ctx)
    brief = {
        "tool": "daily_brief",
        "timestamp": datetime.now().isoformat(),
        "org": ctx["org"],
        "report_time": ctx["report_time"],
        "fleet_online": pulse["online"],
        "fleet_total": pulse["total"],
        "highlights": ["Squad demo attiva", "Attiva bot con activate-*-*.sh <TOKEN>", "Founder: usa *pulse* e *escala*"],
    }
    cfg = load()
    set_dotted(cfg, "reports.last_brief", datetime.now().isoformat())
    save(cfg)
    return brief


def escalate(message: str, severity: str = "normal") -> dict:
    cfg = load()
    item = {"id": f"ESC-{uuid.uuid4().hex[:6]}", "message": message, "severity": severity, "created": datetime.now().isoformat()}
    return {"tool": "escalate", **item, "routed_to": get_dotted(cfg, "org.founder_chat_id") or "admin", "disclaimer": "Demo: log locale — produzione usa bus Hermes"}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("tool")
    p.add_argument("--message", default="")
    p.add_argument("--severity", default="normal")
    args = p.parse_args()

    ctx = lead_context()
    tools = {
        "pulse": lambda: fleet_pulse(ctx),
        "brief": lambda: daily_brief(ctx),
        "escalate": lambda: escalate(args.message or "Escalation senza testo", args.severity),
        "market_overview": market_overview,
        "mercato": market_overview,
    }
    fn = tools.get(args.tool)
    out = fn() if fn else {"error": f"Unknown: {args.tool}", "available": list(tools)}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
