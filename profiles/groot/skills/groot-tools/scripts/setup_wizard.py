#!/usr/bin/env python3
"""Wizard Telegram — configurazione GROOT Brigata in 5 domande (no YAML)."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from brigata_config import get_dotted, load, save, set_dotted, validate, profile_root

STATE_FILE = profile_root() / "cache" / "setup-wizard.json"
SCRIPTS = Path(__file__).resolve().parent
CONFIGURE = SCRIPTS / "configure_brigata.py"

STEPS = [
    {
        "id": "venue_name",
        "question": "🏪 Domanda 1/5 — Come si chiama il locale? (es. Trattoria da Marco)",
        "hint": "Nome che vedrà la brigata nei messaggi.",
    },
    {
        "id": "sheet_id",
        "question": "📋 Domanda 2/5 — Incolla l'ID o il link del foglio Google Sheets.\n"
        "Serve la tab LISTA_SPESA. Scrivi *salta* se lo aggiungi dopo.",
        "hint": "Dall'URL: docs.google.com/spreadsheets/d/QUESTO_ID/edit",
    },
    {
        "id": "group_chat",
        "question": "👥 Domanda 3/5 — Gruppo Telegram della brigata.\n"
        "Scrivi *qui* se configuri dal gruppo, oppure incolla il chat ID (es. -100123...).",
        "hint": "Il bot deve essere admin nel gruppo.",
    },
    {
        "id": "admin_id",
        "question": "🔑 Domanda 4/5 — Il tuo ID Telegram (numeri) per alert e config.\n"
        "Scrivi *salta* se non lo sai (puoi usare @userinfobot).",
        "hint": "Sarai admin del bot.",
    },
    {
        "id": "service_time",
        "question": "🕐 Domanda 5/5 — Orario inizio servizio? (es. 20:00)\n"
        "Invia *ok* per accettare il default 20:00.",
        "hint": "Usato per promemoria pre-servizio.",
    },
]


def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"step": 0, "completed": False, "started_at": None, "answers": {}}


def _save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def _extract_sheet_id(text: str) -> str:
    text = text.strip()
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", text)
    if m:
        return m.group(1)
    if re.match(r"^[a-zA-Z0-9-_]{20,}$", text):
        return text
    return ""


def _parse_ids(text: str) -> list[int]:
    return [int(x) for x in re.findall(r"-?\d+", text)]


def _apply_answers(answers: dict, ctx: dict) -> None:
    cfg = load()
    if answers.get("venue_name"):
        set_dotted(cfg, "venue.name", answers["venue_name"])
    if answers.get("sheet_id"):
        set_dotted(cfg, "google_sheets.spreadsheet_id", answers["sheet_id"])
    group = answers.get("group_chat", "")
    if group:
        set_dotted(cfg, "telegram.group_chat_id", group)
    admin = answers.get("admin_id", "")
    if admin:
        aid = int(admin)
        set_dotted(cfg, "telegram.admin_chat_id", str(aid))
        admins = list(get_dotted(cfg, "roles.admin") or [])
        if aid not in admins:
            admins.append(aid)
        set_dotted(cfg, "roles.admin", admins)
    st = answers.get("service_time") or "20:00"
    set_dotted(cfg, "operations.service_time", st)
    if ctx.get("user_id") and not get_dotted(cfg, "telegram.admin_chat_id"):
        uid = int(ctx["user_id"])
        set_dotted(cfg, "telegram.admin_chat_id", str(uid))
        set_dotted(cfg, "roles.admin", [uid])
    save(cfg)


def _run_configure(args: list[str]) -> dict:
    r = subprocess.run(
        ["python3", str(CONFIGURE), *args],
        capture_output=True,
        text=True,
        timeout=30,
    )
    out = (r.stdout or r.stderr or "").strip()
    try:
        return json.loads(out.split("\n")[-1] if "\n" in out else out)
    except Exception:
        return {"raw": out, "code": r.returncode}


def cmd_status(_: argparse.Namespace) -> None:
    cfg = load()
    v = validate(cfg)
    state = _load_state()
    step = state.get("step", 0)
    out = {
        "tool": "setup_wizard_status",
        "configured": v.get("configured"),
        "wizard_complete": state.get("completed"),
        "current_step": step + 1 if step < len(STEPS) else None,
        "total_steps": len(STEPS),
        "question": STEPS[step]["question"] if step < len(STEPS) and not state.get("completed") else None,
        "validate": v,
    }
    if v.get("configured") and not state.get("completed"):
        out["note"] = "Config già valida — scrivi setup finish per chiudere wizard"
    print(json.dumps(out, indent=2, ensure_ascii=False))


def cmd_start(_: argparse.Namespace) -> None:
    state = {
        "step": 0,
        "completed": False,
        "started_at": datetime.now().isoformat(),
        "answers": {},
    }
    _save_state(state)
    print(json.dumps({
        "tool": "setup_wizard_start",
        "step": 1,
        "total": len(STEPS),
        "question": STEPS[0]["question"],
        "hint": STEPS[0]["hint"],
        "instruction": "Rispondi con il nome del locale.",
    }, indent=2, ensure_ascii=False))


def cmd_answer(args: argparse.Namespace) -> None:
    state = _load_state()
    if state.get("completed"):
        print(json.dumps({"tool": "setup_wizard", "status": "already_complete", "message": "Scrivi setup restart per ricominciare."}, ensure_ascii=False))
        return

    step_idx = state.get("step", 0)
    if step_idx >= len(STEPS):
        print(json.dumps({"tool": "setup_wizard", "status": "done", "message": "Scrivi setup finish"}, ensure_ascii=False))
        return

    step = STEPS[step_idx]
    raw = (args.text or "").strip()
    low = raw.lower()
    ctx = {"chat_id": args.chat_id, "user_id": args.user_id}
    answers = state.setdefault("answers", {})
    err = None

    if step["id"] == "venue_name":
        if len(raw) < 2:
            err = "Nome troppo corto — riprova."
        else:
            answers["venue_name"] = raw

    elif step["id"] == "sheet_id":
        if low in ("salta", "skip", "dopo", "-"):
            answers["sheet_id"] = ""
        else:
            sid = _extract_sheet_id(raw)
            if not sid:
                err = "ID foglio non valido. Incolla link Sheets o ID lungo."
            else:
                answers["sheet_id"] = sid

    elif step["id"] == "group_chat":
        if low in ("qui", "questo", "this", "gruppo"):
            cid = args.chat_id or ""
            if cid and str(cid).startswith("-"):
                answers["group_chat"] = str(cid)
            else:
                err = "Scrivi *qui* dal gruppo brigata, oppure incolla il chat ID."
        else:
            ids = _parse_ids(raw)
            if ids and (str(ids[0]).startswith("-") or ids[0] < 0):
                answers["group_chat"] = str(ids[0])
            elif ids:
                err = "Serve il chat ID del gruppo (numero negativo, es. -100...)."
            else:
                err = "Scrivi *qui* nel gruppo o incolla chat ID."

    elif step["id"] == "admin_id":
        if low in ("salta", "skip", "-"):
            if args.user_id:
                answers["admin_id"] = str(args.user_id)
            else:
                answers["admin_id"] = ""
        else:
            ids = _parse_ids(raw)
            if ids:
                answers["admin_id"] = str(ids[0])
            elif args.user_id:
                answers["admin_id"] = str(args.user_id)
            else:
                err = "Invia il tuo ID numerico o scrivi salta."

    elif step["id"] == "service_time":
        if low in ("ok", "default", "20:00", "20"):
            answers["service_time"] = "20:00"
        elif re.match(r"^\d{1,2}:\d{2}$", raw):
            answers["service_time"] = raw
        else:
            err = "Formato HH:MM (es. 20:00) oppure scrivi ok."

    if err:
        print(json.dumps({
            "tool": "setup_wizard_answer",
            "ok": False,
            "error": err,
            "question": step["question"],
            "hint": step["hint"],
        }, indent=2, ensure_ascii=False))
        return

    state["step"] = step_idx + 1
    _save_state(state)

    if state["step"] >= len(STEPS):
        _apply_answers(answers, ctx)
        cfg = load()
        if get_dotted(cfg, "google_sheets.spreadsheet_id") and get_dotted(cfg, "telegram.group_chat_id"):
            set_dotted(cfg, "cron.enabled", True)
            save(cfg)
            _run_configure(["apply-cron"])
        state["completed"] = True
        state["completed_at"] = datetime.now().isoformat()
        _save_state(state)
        v = validate(load())
        print(json.dumps({
            "tool": "setup_wizard_complete",
            "ok": True,
            "summary": {
                "venue": answers.get("venue_name"),
                "sheet": answers.get("sheet_id") or "(da aggiungere: config sheet ID)",
                "group": answers.get("group_chat") or "(manca)",
                "service_time": answers.get("service_time", "20:00"),
            },
            "validate": v,
            "next": "Prova: finita la panna — oppure config sheet ID se hai saltato il foglio.",
        }, indent=2, ensure_ascii=False))
        return

    nxt = STEPS[state["step"]]
    print(json.dumps({
        "tool": "setup_wizard_answer",
        "ok": True,
        "step": state["step"] + 1,
        "total": len(STEPS),
        "question": nxt["question"],
        "hint": nxt["hint"],
    }, indent=2, ensure_ascii=False))


def cmd_finish(_: argparse.Namespace) -> None:
    state = _load_state()
    if state.get("answers"):
        _apply_answers(state["answers"], {})
    v = validate(load())
    if v.get("configured") and get_dotted(load(), "telegram.group_chat_id"):
        cfg = load()
        set_dotted(cfg, "cron.enabled", True)
        save(cfg)
        _run_configure(["apply-cron"])
    state["completed"] = True
    _save_state(state)
    print(json.dumps({"tool": "setup_wizard_finish", "validate": v}, indent=2, ensure_ascii=False))


def cmd_restart(_: argparse.Namespace) -> None:
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    cmd_start(_)


def main() -> None:
    p = argparse.ArgumentParser(description="GROOT Brigata setup wizard")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("start")
    sub.add_parser("finish")
    sub.add_parser("restart")

    a = sub.add_parser("answer")
    a.add_argument("text")
    a.add_argument("--chat-id", default="")
    a.add_argument("--user-id", default="")

    args = p.parse_args()
    handlers = {
        "status": cmd_status,
        "start": cmd_start,
        "finish": cmd_finish,
        "restart": cmd_restart,
        "answer": cmd_answer,
    }
    handlers[args.cmd](args)


if __name__ == "__main__":
    main()
