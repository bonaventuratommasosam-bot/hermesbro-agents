# Hermes Vault — Credential Storage

## Overview

`hermes-vault` is the installed and configured secrets manager for the VPS stack. Local-first encrypted SQLite database with AES-GCM. Installed at `/root/.local/bin/hermes-vault`.

## Quick Reference

```bash
# Store credential
echo "" | HERMES_VAULT_PASSPHRASE="<pass>" hermes-vault add <service> --secret "<value>" --alias "<name>" --credential-type api_key --tags "tag1,tag2"

# List all
echo "" | HERMES_VAULT_PASSPHRASE="<pass>" hermes-vault list

# Show metadata (no secret exposed)
echo "" | HERMES_VAULT_PASSPHRASE="<pass>" hermes-vault show-metadata <name>

# Import from .env file
echo "" | HERMES_VAULT_PASSPHRASE="<pass>" hermes-vault import --from-env /path/.env --tags "bot-name"

# Scan for exposed secrets
hermes-vault scan --path /path/to/code
```

## Passphrase Management

- Master passphrase stored in `<HERMES_ROOT>/profiles/gribbito/.env` as `HERMES_VAULT_PASSPHRASE`
- Every non-interactive command needs: `echo "" | HERMES_VAULT_PASSPHRASE="<value>" hermes-vault <cmd>`
- Without the pipe, the CLI prompts interactively and hangs

## Pitfalls

- `scan` reports `insecure_permissions` (mode 644) as HIGH severity — these are NOT leaked secrets, just file permission issues
- No `--version` flag — use `hermes-vault --help`
- No `init` command — auto-initializes on first `add` or `import`
