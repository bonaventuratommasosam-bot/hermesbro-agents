#!/usr/bin/env python3
"""ContAIbile tools — movimenti, IVA stimata, scadenze, food cost."""
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

from contabile_config import company_context, get_dotted, ledger_path, load

DEADLINES_IT = [
    {"id": "iva_trim", "name": "Liquidazione IVA trimestrale", "month_day": "16", "months": [5, 8, 11, 3]},
    {"id": "f24_inps", "name": "F24 contributi/INPS", "month_day": "16", "months": list(range(1, 13))},
    {"id": "dich_730", "name": "Dichiarazione 730 (se applicabile)", "month_day": "30", "months": [9]},
]


def _append_ledger(entry: dict) -> Path:
    path = ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    entry["timestamp"] = datetime.now().isoformat()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path


def _read_ledger() -> list[dict]:
    path = ledger_path()
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def register_movement(kind: str, amount: float, description: str, category: str = "", iva_pct: float | None = None) -> dict:
    ctx = company_context()
    iva = iva_pct if iva_pct is not None else ctx["default_iva"]
    net = round(amount / (1 + iva / 100), 2) if kind == "spesa" and iva else amount
    entry = {
        "tool": "register_movement",
        "kind": kind,
        "amount": round(amount, 2),
        "net": net,
        "iva_pct": iva,
        "description": description,
        "category": category or ("ricavi" if kind == "ricavo" else "costi"),
        "company": ctx["company"],
    }
    path = _append_ledger(entry)
    return {**entry, "ledger": str(path), "status": "registered"}


def list_movements(limit: int = 20) -> dict:
    rows = _read_ledger()[-limit:]
    return {"tool": "list_movements", "count": len(rows), "movements": rows}


def compute_iva_estimate(period_days: int = 90) -> dict:
    ctx = company_context()
    cutoff = datetime.now() - timedelta(days=period_days)
    iva_debito = iva_credito = 0.0
    ricavi = costi = 0.0
    for row in _read_ledger():
        try:
            ts = datetime.fromisoformat(row.get("timestamp", ""))
        except ValueError:
            continue
        if ts < cutoff:
            continue
        amt = float(row.get("amount", 0))
        iva_pct = float(row.get("iva_pct", ctx["default_iva"]))
        if row.get("kind") == "ricavo":
            ricavi += amt
            iva_debito += amt - (amt / (1 + iva_pct / 100))
        elif row.get("kind") == "spesa":
            costi += amt
            iva_credito += amt - (amt / (1 + iva_pct / 100))
    da_versare = round(max(0, iva_debito - iva_credito), 2)
    return {
        "tool": "compute_iva",
        "company": ctx["company"],
        "regime": ctx["regime"],
        "iva_regime": ctx["iva_regime"],
        "period_days": period_days,
        "ricavi": round(ricavi, 2),
        "costi": round(costi, 2),
        "iva_debito": round(iva_debito, 2),
        "iva_credito": round(iva_credito, 2),
        "iva_da_versare_stimata": da_versare,
        "note": "Stima da ledger locale — non sostituisce liquidazione ufficiale",
    }


def upcoming_deadlines(days_ahead: int = 30) -> dict:
    today = datetime.now().date()
    end = today + timedelta(days=days_ahead)
    upcoming = []
    year = today.year
    for dl in DEADLINES_IT:
        for m in dl["months"]:
            try:
                d = datetime(year, m, int(dl["month_day"])).date()
            except ValueError:
                continue
            if d < today and m < today.month:
                d = datetime(year + 1, m, int(dl["month_day"])).date()
            if today <= d <= end:
                upcoming.append({"id": dl["id"], "name": dl["name"], "date": d.isoformat(), "days_left": (d - today).days})
    upcoming.sort(key=lambda x: x["date"])
    alert_days = int(get_dotted(load(), "telegram.alert_days_before") or 7)
    urgent = [u for u in upcoming if u["days_left"] <= alert_days]
    return {"tool": "upcoming_deadlines", "days_ahead": days_ahead, "deadlines": upcoming, "urgent": urgent}


def food_cost_check(revenue: float, food_cost: float) -> dict:
    ctx = company_context()
    if revenue <= 0:
        return {"tool": "food_cost_check", "error": "ricavi devono essere > 0"}
    pct = round(food_cost / revenue * 100, 1)
    threshold = float(ctx["food_cost_alert_pct"])
    status = "ok" if pct <= threshold else "alert"
    return {
        "tool": "food_cost_check",
        "company": ctx["company"],
        "revenue": revenue,
        "food_cost": food_cost,
        "food_cost_pct": pct,
        "threshold_pct": threshold,
        "status": status,
        "message": "OK" if status == "ok" else f"Food cost {pct}% > soglia {threshold}%",
    }


def summary() -> dict:
    rows = _read_ledger()
    ricavi = sum(float(r.get("amount", 0)) for r in rows if r.get("kind") == "ricavo")
    spese = sum(float(r.get("amount", 0)) for r in rows if r.get("kind") == "spesa")
    ctx = company_context()
    return {
        "tool": "summary",
        "company": ctx["company"],
        "regime": ctx["regime"],
        "movements": len(rows),
        "ricavi_totali": round(ricavi, 2),
        "spese_totali": round(spese, 2),
        "margine": round(ricavi - spese, 2),
    }


def main() -> None:
    p = argparse.ArgumentParser(description="ContAIbile Tools")
    p.add_argument("tool", help="register_ricavo,register_spesa,list_movements,compute_iva,scadenze,food_cost,summary")
    p.add_argument("--amount", type=float, default=0)
    p.add_argument("--description", default="")
    p.add_argument("--category", default="")
    p.add_argument("--revenue", type=float, default=0)
    p.add_argument("--food_cost", type=float, default=0)
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--limit", type=int, default=20)
    args = p.parse_args()

    tools = {
        "register_ricavo": lambda: register_movement("ricavo", args.amount, args.description, args.category),
        "register_spesa": lambda: register_movement("spesa", args.amount, args.description, args.category),
        "list_movements": lambda: list_movements(args.limit),
        "compute_iva": compute_iva_estimate,
        "scadenze": lambda: upcoming_deadlines(args.days),
        "food_cost": lambda: food_cost_check(args.revenue, args.food_cost),
        "summary": summary,
    }
    fn = tools.get(args.tool)
    print(json.dumps(fn() if fn else {"error": f"Unknown: {args.tool}"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
