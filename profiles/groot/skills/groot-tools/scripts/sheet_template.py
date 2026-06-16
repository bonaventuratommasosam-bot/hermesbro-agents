#!/usr/bin/env python3
"""Info foglio template GROOT Brigata — link copia 1 click."""
import argparse
import json

from brigata_config import template_info


def main() -> None:
    p = argparse.ArgumentParser(description="GROOT Brigata sheet template")
    p.add_argument("cmd", nargs="?", default="info", choices=["info"])
    args = p.parse_args()
    info = template_info()
    info["tool"] = "sheet_template_info"
    info["message_it"] = (
        "📋 **Foglio template GROOT Brigata**\n\n"
        f"1️⃣ Crea la tua copia:\n{info['copy_url']}\n\n"
        "2️⃣ Apri il foglio copiato → Condividi → Editor"
        + (f" → {info['share_with_email']}\n" if info["share_with_email"] else " → email HermesBro (in onboarding)\n")
        + "3️⃣ Copia il nuovo ID dall'URL e incollalo qui.\n\n"
        "Tab incluse: LISTA_SPESA, MAGAZZINO, ORDINI, MEMORIA, PROMEMORIA"
    )
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
