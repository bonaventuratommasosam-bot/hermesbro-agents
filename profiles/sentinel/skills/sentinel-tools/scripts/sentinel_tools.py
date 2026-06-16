#!/usr/bin/env python3
"""Sentinel Security Tools."""
import argparse
import json
import socket
import ssl
from datetime import datetime

from audit_config import audit_context


def ssl_check(domain: str, port: int = 443) -> dict:
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert.get("issuer", []))
                return {
                    "tool": "ssl_check",
                    "timestamp": datetime.now().isoformat(),
                    "domain": domain,
                    "issuer": issuer.get("organizationName", "?"),
                    "expires": cert.get("notAfter", ""),
                    "valid": True,
                }
    except Exception as e:
        return {"tool": "ssl_check", "domain": domain, "error": str(e)[:100]}


def security_checklist(target_type: str) -> dict:
    checklists = {
        "web_server": ["HTTPS enforced?", "HSTS header?", "Rate limiting?", "Security headers?"],
        "vps": ["SSH root disabled?", "Firewall active?", "Fail2ban?", "Unnecessary ports closed?"],
        "api": ["Auth on all endpoints?", "HTTPS only?", "No stack traces in responses?"],
    }
    items = checklists.get(target_type, checklists["web_server"])
    return {"tool": "security_checklist", "target_type": target_type, "checklist": items, "total_checks": len(items)}


def backup_audit() -> dict:
    return {
        "tool": "backup_audit",
        "rules": {"rule_3_2_1": "3 copie, 2 formati, 1 offsite"},
        "checklist": ["DB nel backup?", "Restore testato?", "Alert su fallimento?"],
    }


def products(ctx: dict) -> dict:
    return {
        "tool": "products",
        "client": ctx["client"],
        "offerings": [
            {"sku": "Smart Contract Audit", "price_usd": 24.99, "sla_hours": ctx["sc_sla"]},
            {"sku": "VPS Security Audit", "price_usd": 49.99, "sla_hours": ctx["vps_sla"]},
        ],
        "order_hint": "Acquista da hermesbro.cloud/os — report su Telegram",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("tool")
    p.add_argument("--domain", default="")
    p.add_argument("--target_type", default="vps")
    args = p.parse_args()

    ctx = audit_context()
    domain = args.domain or ctx["domain"]
    tools = {
        "ssl_check": lambda: ssl_check(domain),
        "ssl": lambda: ssl_check(domain),
        "security_checklist": lambda: security_checklist(args.target_type),
        "checklist": lambda: security_checklist(args.target_type),
        "backup_audit": backup_audit,
        "backup": backup_audit,
        "products": lambda: products(ctx),
    }
    fn = tools.get(args.tool)
    out = fn() if fn else {"error": f"Unknown: {args.tool}", "available": list(tools)}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
