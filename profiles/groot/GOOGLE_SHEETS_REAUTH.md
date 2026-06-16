# Google Sheets — re-auth GROOT

Se `lista_spesa.py ping` o `google_api.py` falliscono con `invalid_grant`:

1. SSH sul VPS come root
2. Profilo: `{{HERMES_HOME}}/`
3. Riesegui OAuth Google Workspace per quel profilo:

```bash
export HERMES_HOME={{HERMES_HOME}}
export DATA_DIR={{HERMES_HOME}}
python3 {{HERMES_HOME}}/../../skills/productivity/google-workspace/scripts/google_api.py auth login
```

4. Verifica:

```bash
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/lista_spesa.py ping
```

5. Sincronizza coda locale se presente:

```bash
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/sync_pending_spesa.py
```

**Clienti con SA:** condividono il foglio copia con `share_with_email` (Editor), non serve OAuth sul profilo bot se usate service account dedicato per cliente.
