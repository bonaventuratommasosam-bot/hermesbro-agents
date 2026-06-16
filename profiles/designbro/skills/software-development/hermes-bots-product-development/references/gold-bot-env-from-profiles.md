# Gold Bot Deploy — .env from Hermes Profiles

When deploying gold bots, create .env files by extracting BOT_TOKEN from existing Hermes profile `.env` files.

## Problem

Terminal masks secret values (BOT_TOKEN, API keys) in stdout. You can't just `grep` and see the full value.

## Solution

Use a shell script that reads tokens internally and writes .env files without printing secrets to stdout.

```bash
#!/bin/bash
BASE="/home/[REDACTED — dati personali rimossi]/ai-stack"
PROFILES="<HERMES_ROOT>/profiles"
LLM_KEY="<from existing .env>"
LLM_URL="<GATEWAY_URL>"
LLM_MODEL="mimo-v2.5-pro"

create_env() {
  local dir="$1"
  local profile="$2"
  local port="$3"
  local token=""
  
  if [ -n "$profile" ] && [ -f "$PROFILES/$profile/.env" ]; then
    token=$(grep TELEGRAM_BOT_TOKEN "$PROFILES/$profile/.env" | cut -d= -f2-)
  fi
  
  if [ -z "$token" ] || [ "$token" = "PLACEHOLDER" ]; then
    token="PLACEHOLDER"
  fi
  
  cat > "$BASE/$dir/.env" << EOF
# $dir — Environment Variables
PORT=$port
LLM_BASE_URL=$LLM_URL
LLM_API_KEY=$LLM_KEY
LLM_MODEL=$LLM_MODEL
BOT_TOKEN=$token
EOF
  echo "Created: $BASE/$dir/.env (token: ${token:0:10}...)"
}

# Usage:
create_env "botname-gold" "profile-name" "8097"
```

## Profile → Bot Token Mapping

Check existing profiles: `ls <HERMES_ROOT>/profiles/`
Read token: `grep TELEGRAM_BOT_TOKEN <HERMES_ROOT>/profiles/{name}/.env`

## After Creating .env

```bash
sudo chown -R [REDACTED — dati personali rimossi]:[REDACTED — dati personali rimossi] /home/[REDACTED — dati personali rimossi]/ai-stack/*-gold
sudo chmod -R u+w /home/[REDACTED — dati personali rimossi]/ai-stack/*-gold
```

## Verify

```bash
# Check .env exists and has no PLACEHOLDER
for d in /home/[REDACTED — dati personali rimossi]/ai-stack/*-gold; do
  name=$(basename $d)
  token=$(grep BOT_TOKEN $d/.env | cut -d= -f2-)
  if [ "$token" = "PLACEHOLDER" ]; then
    echo "PLACEHOLDER: $name"
  else
    echo "OK: $name"
  fi
done
```
