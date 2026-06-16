#!/usr/bin/env python3
import argparse, json, re
from lab_config import config_path, load, save, set_dotted, validate

def _parse(raw: str):
    if raw.lower() in ("true", "false"): return raw.lower() == "true"
    if re.match(r"^-?\d+$", raw): return int(raw)
    if re.match(r"^-?\d+\.\d+$", raw): return float(raw)
    return raw

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show")
    sub.add_parser("validate")
    sp = sub.add_parser("set"); sp.add_argument("key"); sp.add_argument("value")
    args = p.parse_args()
    if args.cmd == "show":
        cfg = load(); print(json.dumps(cfg, indent=2, ensure_ascii=False)); print(json.dumps(validate(cfg), indent=2))
    elif args.cmd == "validate":
        print(json.dumps(validate(load()), indent=2))
    else:
        cfg = load(); set_dotted(cfg, args.key, _parse(args.value)); save(cfg)
        print(json.dumps({"saved": str(config_path()), "key": args.key}, ensure_ascii=False))

if __name__ == "__main__":
    main()