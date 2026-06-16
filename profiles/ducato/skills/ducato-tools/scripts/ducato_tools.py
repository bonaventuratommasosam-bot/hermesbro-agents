#!/usr/bin/env python3
"""Ducato Finance tools."""
import argparse
import json
from datetime import datetime

from finance_config import finance_context, get_dotted, load, save, set_dotted


def portfolio_analyze(assets: list[dict], max_single: float = 15, max_crypto: float = 30) -> dict:
    total = sum(float(a.get("value", 0)) for a in assets)
    results, alerts = [], []
    for a in assets:
        val = float(a.get("value", 0))
        pct = round(val / total * 100, 1) if total > 0 else 0
        results.append({"name": a.get("name", "?"), "class": a.get("class", ""), "value": val, "allocation_pct": pct})
        if pct > max_single:
            alerts.append(f"{a.get('name')}: {pct}% > max {max_single}%")
    crypto_pct = sum(r["allocation_pct"] for r in results if "crypto" in (r.get("class") or "").lower())
    if crypto_pct > max_crypto:
        alerts.append(f"Crypto totale {crypto_pct}% > max {max_crypto}%")
    return {
        "tool": "portfolio_analyze",
        "timestamp": datetime.now().isoformat(),
        "total_value": round(total, 2),
        "assets": results,
        "diversification_score": min(100, len(assets) * 15),
        "alerts": alerts,
        "advice": ["Max 5-10% singolo asset", "3+ classi diverse", "Ribilanciare trimestralmente"],
    }


def ratio_analysis(data: dict) -> dict:
    rev = float(data.get("revenue", 0))
    profit = float(data.get("profit", 0))
    equity = float(data.get("equity", 0))
    debt = float(data.get("debt", 0))
    assets = float(data.get("assets", 0))
    return {
        "tool": "ratio_analysis",
        "timestamp": datetime.now().isoformat(),
        "ratios": {
            "profit_margin": f"{round(profit / rev * 100, 1)}%" if rev > 0 else "N/A",
            "roe": f"{round(profit / equity * 100, 1)}%" if equity > 0 else "N/A",
            "debt_ratio": f"{round(debt / assets * 100, 1)}%" if assets > 0 else "N/A",
        },
        "benchmarks": {"profit_margin": ">10%", "roe": ">15%", "debt_ratio": "<50%"},
    }


def scenario_projection(base: float, monthly_growth: float, months: int) -> dict:
    scenarios = {"best": monthly_growth * 1.5, "base": monthly_growth, "worst": monthly_growth * 0.3}
    proj = {}
    for name, rate in scenarios.items():
        val = base
        for _ in range(months):
            val = round(val * (1 + rate / 100), 2)
        proj[name] = {"rate_pct": rate, "final_value": val, "total_return_pct": round((val / base - 1) * 100, 1)}
    return {"tool": "scenario_projection", "timestamp": datetime.now().isoformat(), "initial": base, "months": months, "scenarios": proj}


def break_even(fixed_costs: float, price: float, variable_cost: float) -> dict:
    if price <= variable_cost:
        return {"tool": "break_even", "error": "prezzo deve essere > costo variabile"}
    units = round(fixed_costs / (price - variable_cost), 1)
    return {"tool": "break_even", "fixed_costs": fixed_costs, "price": price, "variable_cost": variable_cost, "break_even_units": units, "margin_per_unit": round(price - variable_cost, 2)}


def cash_runway(cash: float, monthly_burn: float, alert_months: int = 3) -> dict:
    if monthly_burn <= 0:
        return {"tool": "cash_runway", "cash": cash, "runway_months": None, "status": "no_burn_data"}
    months = round(cash / monthly_burn, 1)
    status = "ok" if months >= alert_months else "alert"
    return {"tool": "cash_runway", "cash": cash, "monthly_burn": monthly_burn, "runway_months": months, "status": status}


def add_asset(name: str, value: float, asset_class: str = "") -> dict:
    cfg = load()
    assets = list(get_dotted(cfg, "portfolio.assets") or [])
    assets.append({"name": name, "value": value, "class": asset_class})
    set_dotted(cfg, "portfolio.assets", assets)
    save(cfg)
    ctx = finance_context(cfg)
    return portfolio_analyze(assets, get_dotted(cfg, "risk.max_single_asset_pct") or 15, ctx["max_crypto_pct"])


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("tool")
    p.add_argument("--json_input", default="")
    p.add_argument("--name", default="")
    p.add_argument("--value", type=float, default=0)
    p.add_argument("--class", dest="asset_class", default="")
    p.add_argument("--revenue", type=float, default=0)
    p.add_argument("--profit", type=float, default=0)
    p.add_argument("--fixed", type=float, default=0)
    p.add_argument("--price", type=float, default=0)
    p.add_argument("--variable", type=float, default=0)
    p.add_argument("--cash", type=float, default=0)
    p.add_argument("--growth", type=float, default=5)
    p.add_argument("--months", type=int, default=12)
    args = p.parse_args()

    ctx = finance_context()
    ji = json.loads(args.json_input) if args.json_input else {}

    tools = {
        "portfolio": lambda: portfolio_analyze(ctx["assets"] or ji.get("assets", []), 15, ctx["max_crypto_pct"]),
        "ratios": lambda: ratio_analysis({**ji, "revenue": args.revenue or ji.get("revenue", 0), "profit": args.profit or ji.get("profit", 0)}),
        "scenarios": lambda: scenario_projection(ctx["base_value"], args.growth, args.months),
        "break_even": lambda: break_even(args.fixed, args.price, args.variable),
        "runway": lambda: cash_runway(args.cash or ctx["base_value"], ctx["monthly_burn"] or args.fixed, ctx["runway_alert_months"]),
        "add_asset": lambda: add_asset(args.name, args.value, args.asset_class),
    }
    fn = tools.get(args.tool)
    out = fn() if fn else {"error": f"Unknown: {args.tool}", "available": list(tools)}
    out["disclaimer"] = "Analisi informativa — non consulenza finanziaria autorizzata."
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
