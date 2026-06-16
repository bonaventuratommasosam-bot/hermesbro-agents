#!/usr/bin/env python3
"""Wizard ContAIbile — 5 domande."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from contabile_config import get_dotted, load, save, set_dotted, validate, profile_root

STATE_FILE = profile_root() / "cache" / "setup-wizard.json"
STEPS = [
    {"id": "company_name", "question": "📊 Domanda 1/5 — Ragione sociale o nome attività?", "hint": "Usato in report e movimenti."},
    {"id": "regime", "question": "🏛️ Domanda 2/5 — Regime fiscale? (forfettario, semplificato, ordinario)", "hint": "Default forfettario se incerto."},
    {"id": "sector", "question": "🏷️ Domanda 3/5 — Settore? (ristorante, saas, retail, crypto, servizi)", "hint": "Ristorante abilita alert food cost."},
    {"id": "group_chat", "question": "👥 Domanda 4/5 — Gruppo Telegram per alert fiscali. *qui* o chat ID.", "hint": "Bot nel gruppo."},
    {"id": "admin_id", "question": "🔑 Domanda 5/5 — Tuo ID Telegram. *salta* se non lo sai.", "hint": "Alert scadenze urgenti."},
]
REGIMES = {"forfettario", "semplificato", "ordinario"}
SECTORS = {"ristorante", "saas", "retail", "crypto", "servizi"}


def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"step": 0, "completed": False, "answers": {}}


def _save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def _apply(answers: dict, ctx: dict) -> None:
    cfg = load()
    if answers.get("company_name"):
        set_dotted(cfg, "company.name", answers["company_name"])
    regime = (answers.get("regime") or "forfettario").strip().lower()
    set_dotted(cfg, "company.regime", regime if regime in REGIMES else "forfettario")
    sector = (answers.get("sector") or "servizi").strip().lower()
    set_dotted(cfg, "company.sector", sector if sector in SECTORS else "servizi")
    if answers.get("group_chat"):
        set_dotted(cfg, "telegram.group_chat_id", answers["group_chat"])
    admin = answers.get("admin_id", "")
    if admin and admin not in ("salta", "skip"):
        aid = int(admin)
        set_dotted(cfg, "telegram.admin_chat_id", str(aid))
        set_dotted(cfg, "roles.admin", [aid])
    elif ctx.get("user_id"):
        uid = int(ctx["user_id"])
        set_dotted(cfg, "telegram.admin_chat_id", str(uid))
        set_dotted(cfg, "roles.admin", [uid])
    save(cfg)


def cmd_start(_: argparse.Namespace) -> None:
    _save_state({"step": 0, "completed": False, "started_at": datetime.now().isoformat(), "answers": {}})
    s = STEPS[0]
    print(json.dumps({"action": "ask", "step": 1, "total": 5, "question": s["question"], "hint": s["hint"]}, ensure_ascii=False))


def cmd_status(_: argparse.Namespace) -> None:
    st = _load_state()
    print(json.dumps({"configured": validate(load())["configured"], "wizard": st}, ensure_ascii=False))


def cmd_restart(_: argparse.Namespace) -> None:
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    cmd_start(_)


def cmd_answer(args: argparse.Namespace) -> None:
    state = _load_state()
    if state.get("completed"):
        print(json.dumps({"action": "done"}, ensure_ascii=False))
        return
    idx = int(state.get("step", 0))
    text = args.text.strip()
    if STEPS[idx]["id"] == "group_chat" and text.lower() in ("qui", "here"):
        text = str(args.chat_id or "")
    if STEPS[idx]["id"] == "admin_id" and text.lower() in ("salta", "skip"):
        text = ""
    state.setdefault("answers", {})[STEPS[idx]["id"]] = text
    idx += 1
    state["step"] = idx
    if idx >= len(STEPS):
        _apply(state["answers"], {"user_id": args.user_id})
        state["completed"] = True
        _save_state(state)
        cfg = load()
        print(json.dumps({
            "action": "complete",
            "summary": f"✅ {get_dotted(cfg, 'company.name')} — regime {get_dotted(cfg, 'company.regime')}. Prova: *riepilogo* o *scadenze*",
            "validate": validate(cfg),
        }, ensure_ascii=False))
        return
    _save_state(state)
    s = STEPS[idx]
    print(json.dumps({"action": "ask", "step": idx + 1, "total": 5, "question": s["question"], "hint": s["hint"]}, ensure_ascii=False))


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("start").set_defaults(func=cmd_start)
    sub.add_parser("restart").set_defaults(func=cmd_restart)
    sp = sub.add_parser("answer")
    sp.add_argument("text")
    sp.add_argument("--chat-id", default="")
    sp.add_argument("--user-id", default="")
    sp.set_defaults(func=cmd_answer)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
