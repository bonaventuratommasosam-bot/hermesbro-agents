#!/usr/bin/env python3
"""Wizard El-froggo Lead — 5 domande."""
import argparse, json
from datetime import datetime
from pathlib import Path
from fleet_lead_config import SQUAD, get_dotted, load, save, set_dotted, validate, profile_root

STATE = profile_root() / "cache" / "setup-wizard.json"
STEPS = [
    ("org_name", "🐸 1/5 — Nome organizzazione / team?"),
    ("report_time", "⏰ 2/5 — Orario report giornaliero? *ok* = 08:00"),
    ("founder_id", "👤 3/5 — Chat ID founder (opzionale). *salta* se non lo sai."),
    ("group_chat", "👥 4/5 — Gruppo Telegram. *qui* o chat ID."),
    ("admin_id", "🔑 5/5 — ID Telegram admin. *salta* se non lo sai."),
]

def _state():
    if STATE.exists():
        try: return json.loads(STATE.read_text(encoding="utf-8"))
        except: pass
    return {"step": 0, "completed": False, "answers": {}}

def _save(s):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=2), encoding="utf-8")

def _apply(a, ctx):
    cfg = load()
    if a.get("org_name"): set_dotted(cfg, "org.name", a["org_name"])
    rt = a.get("report_time", "08:00")
    if str(rt).lower() in ("ok", "salta", "skip"): rt = "08:00"
    set_dotted(cfg, "fleet.report_time", rt)
    set_dotted(cfg, "fleet.agents", SQUAD)
    set_dotted(cfg, "fleet.include_trading", False)
    founder = a.get("founder_id", "")
    if founder and founder not in ("salta", "skip"):
        set_dotted(cfg, "org.founder_chat_id", str(int(founder)))
    if a.get("group_chat"): set_dotted(cfg, "telegram.group_chat_id", a["group_chat"])
    admin = a.get("admin_id", "")
    if admin and admin not in ("salta", "skip"):
        set_dotted(cfg, "roles.admin", [int(admin)])
        set_dotted(cfg, "telegram.admin_chat_id", str(int(admin)))
    elif ctx.get("user_id"):
        set_dotted(cfg, "roles.admin", [int(ctx["user_id"])])
    save(cfg)

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("start")
    sub.add_parser("status")
    sub.add_parser("restart")
    sp = sub.add_parser("answer"); sp.add_argument("text"); sp.add_argument("--chat-id", default=""); sp.add_argument("--user-id", default="")
    args = p.parse_args()
    if args.cmd == "start":
        _save({"step": 0, "completed": False, "answers": {}, "started_at": datetime.now().isoformat()})
        print(json.dumps({"action": "ask", "step": 1, "question": STEPS[0][1]}, ensure_ascii=False)); return
    if args.cmd == "status":
        print(json.dumps({"configured": validate(load())["configured"], "wizard": _state()}, ensure_ascii=False)); return
    if args.cmd == "restart":
        STATE.unlink(missing_ok=True); main(); return
    st = _state()
    if st.get("completed"):
        print(json.dumps({"action": "done"}, ensure_ascii=False)); return
    idx = st["step"]
    text = args.text.strip()
    key = STEPS[idx][0]
    if key == "group_chat" and text.lower() in ("qui", "here"): text = args.chat_id
    if key in ("admin_id", "founder_id") and text.lower() in ("salta", "skip"): text = ""
    st["answers"][key] = text
    idx += 1
    st["step"] = idx
    if idx >= len(STEPS):
        _apply(st["answers"], {"user_id": args.user_id})
        st["completed"] = True
        _save(st)
        print(json.dumps({"action": "complete", "summary": f"✅ {get_dotted(load(),'org.name')} — prova *pulse* o *brief*"}, ensure_ascii=False))
        return
    _save(st)
    print(json.dumps({"action": "ask", "step": idx + 1, "question": STEPS[idx][1]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
