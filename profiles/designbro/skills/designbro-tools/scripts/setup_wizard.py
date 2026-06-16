#!/usr/bin/env python3
"""Wizard Telegram — configurazione DesignBro Studio in 5 domande (no YAML)."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from brand_config import get_dotted, load, save, set_dotted, validate, profile_root

STATE_FILE = profile_root() / "cache" / "setup-wizard.json"
SCRIPTS = Path(__file__).resolve().parent
CONFIGURE = SCRIPTS / "configure_brand.py"

STEPS = [
    {
        "id": "brand_name",
        "question": "🎨 Domanda 1/5 — Come si chiama il brand o l'attività? (es. Caffè Rossi)",
        "hint": "Nome usato in logo, palette e brief.",
    },
    {
        "id": "industry",
        "question": "🏷️ Domanda 2/5 — Settore? (food, tech, fashion, finance, legal, retail)\n"
        "Oppure descrivi in una parola.",
        "hint": "Serve per font pairing e mood visivo.",
    },
    {
        "id": "primary_color",
        "question": "🎯 Domanda 3/5 — Colore principale in HEX (es. #1E3A5F) o mood (professional, warm, bold, minimal).\n"
        "Invia *ok* per default professional.",
        "hint": "Se non hai un colore, scegli il mood.",
    },
    {
        "id": "group_chat",
        "question": "👥 Domanda 4/5 — Gruppo Telegram per preview design.\n"
        "Scrivi *qui* se configuri dal gruppo, oppure incolla il chat ID.",
        "hint": "Il bot deve essere nel gruppo.",
    },
    {
        "id": "admin_id",
        "question": "🔑 Domanda 5/5 — Il tuo ID Telegram per approvazioni finali.\n"
        "Scrivi *salta* se non lo sai (usa @userinfobot).",
        "hint": "Sarai admin del bot.",
    },
]

INDUSTRIES = {"food", "tech", "fashion", "finance", "legal", "retail"}
MOODS = {"professional", "warm", "bold", "minimal"}


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


def _parse_hex_or_mood(text: str) -> tuple[str, str]:
    text = text.strip().lower()
    if text in ("ok", "skip", "salta", ""):
        return "", "professional"
    if re.match(r"^#[0-9a-fA-F]{3,8}$", text):
        return text, ""
    if text in MOODS:
        return "", text
    return "", "professional"


def _apply_answers(answers: dict, ctx: dict) -> None:
    cfg = load()
    if answers.get("brand_name"):
        set_dotted(cfg, "brand.name", answers["brand_name"])
    industry = (answers.get("industry") or "tech").strip().lower()
    if industry not in INDUSTRIES:
        industry = "retail"
    set_dotted(cfg, "brand.industry", industry)
    color, mood = _parse_hex_or_mood(answers.get("primary_color", ""))
    if color:
        set_dotted(cfg, "visual.primary_color", color)
    if mood:
        set_dotted(cfg, "visual.mood", mood)
    group = answers.get("group_chat", "")
    if group:
        set_dotted(cfg, "telegram.group_chat_id", group)
    admin = answers.get("admin_id", "")
    if admin and admin not in ("salta", "skip"):
        aid = int(admin)
        set_dotted(cfg, "telegram.admin_chat_id", str(aid))
        admins = list(get_dotted(cfg, "roles.admin") or [])
        if aid not in admins:
            admins.append(aid)
        set_dotted(cfg, "roles.admin", admins)
        reviewers = list(get_dotted(cfg, "roles.reviewers") or [])
        if aid not in reviewers:
            reviewers.append(aid)
        set_dotted(cfg, "roles.reviewers", reviewers)
    if ctx.get("user_id") and not get_dotted(cfg, "telegram.admin_chat_id"):
        uid = int(ctx["user_id"])
        set_dotted(cfg, "telegram.admin_chat_id", str(uid))
        set_dotted(cfg, "roles.admin", [uid])
        set_dotted(cfg, "roles.reviewers", [uid])
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
    v = validate(load())
    state = _load_state()
    print(
        json.dumps(
            {
                "configured": v["configured"],
                "validate": v,
                "wizard": {
                    "step": state.get("step", 0),
                    "completed": state.get("completed", False),
                    "total_steps": len(STEPS),
                },
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def cmd_start(_: argparse.Namespace) -> None:
    state = {
        "step": 0,
        "completed": False,
        "started_at": datetime.now().isoformat(),
        "answers": {},
    }
    _save_state(state)
    step = STEPS[0]
    print(
        json.dumps(
            {
                "action": "ask",
                "step": 1,
                "total": len(STEPS),
                "question": step["question"],
                "hint": step["hint"],
            },
            ensure_ascii=False,
        )
    )


def cmd_restart(_: argparse.Namespace) -> None:
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    cmd_start(_)


def _normalize_answer(step_id: str, text: str, ctx: dict) -> str:
    text = text.strip()
    if step_id == "group_chat" and text.lower() in ("qui", "here", "questo gruppo"):
        return str(ctx.get("chat_id") or "")
    if step_id == "admin_id" and text.lower() in ("salta", "skip"):
        return ""
    if step_id == "primary_color" and text.lower() in ("ok", "skip", "salta"):
        return "ok"
    return text


def cmd_answer(args: argparse.Namespace) -> None:
    state = _load_state()
    if state.get("completed"):
        print(json.dumps({"action": "done", "message": "Setup già completato. Usa config mostra o setup restart."}, ensure_ascii=False))
        return
    step_idx = int(state.get("step", 0))
    if step_idx >= len(STEPS):
        print(json.dumps({"action": "done"}, ensure_ascii=False))
        return

    step = STEPS[step_idx]
    answer = _normalize_answer(step["id"], args.text, {"chat_id": args.chat_id, "user_id": args.user_id})
    state.setdefault("answers", {})[step["id"]] = answer
    step_idx += 1
    state["step"] = step_idx

    if step_idx >= len(STEPS):
        _apply_answers(state["answers"], {"chat_id": args.chat_id, "user_id": args.user_id})
        state["completed"] = True
        _save_state(state)
        cfg = load()
        summary = (
            f"✅ Setup completato per *{get_dotted(cfg, 'brand.name')}*\n"
            f"• Settore: {get_dotted(cfg, 'brand.industry')}\n"
            f"• Mood/colore: {get_dotted(cfg, 'visual.primary_color') or get_dotted(cfg, 'visual.mood')}\n"
            f"• Gruppo: {get_dotted(cfg, 'telegram.group_chat_id') or '—'}\n\n"
            "Prova: *logo concept* oppure *palette colori*"
        )
        print(json.dumps({"action": "complete", "summary": summary, "validate": validate(cfg)}, ensure_ascii=False))
        return

    _save_state(state)
    next_step = STEPS[step_idx]
    print(
        json.dumps(
            {
                "action": "ask",
                "step": step_idx + 1,
                "total": len(STEPS),
                "question": next_step["question"],
                "hint": next_step["hint"],
            },
            ensure_ascii=False,
        )
    )


def main() -> None:
    p = argparse.ArgumentParser(description="DesignBro Studio setup wizard")
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