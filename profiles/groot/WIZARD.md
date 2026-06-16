# Wizard configurazione (5 domande)

Trigger: `setup`, `configura`, `/start` se `validate.configured=false`

```bash
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/setup_wizard.py status
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/setup_wizard.py start
python3 {{HERMES_HOME}}/skills/groot-tools/scripts/setup_wizard.py answer "Risposta cliente" --chat-id {{TELEGRAM_CHAT_ID}} --user-id {{TELEGRAM_USER_ID}}
```

Flusso agente:
1. `status` → se non configurato, `start` e mostra domanda 1
2. Ogni messaggio cliente durante wizard → `answer` con chat-id e user-id Telegram
3. A fine wizard → riepilogo + test `finita la panna`
4. `setup restart` per ricominciare

Comandi rapidi post-wizard: `config sheet ID`, `config gruppo ID`, `lista spesa`
