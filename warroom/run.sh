#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load .env if present
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

cd "$SCRIPT_DIR"

# Ensure virtualenv
if [ ! -f ".venv/bin/python3" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    .venv/bin/pip install -q fastapi uvicorn httpx
fi

exec .venv/bin/python3 -m uvicorn main:app \
    --host "${HOST:-127.0.0.1}" \
    --port "${PORT:-8097}" \
    --reload
