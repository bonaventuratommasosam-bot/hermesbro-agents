# Wizard configurazione (5 domande)

Trigger: `setup`, `configura`, `/start` se `validate.configured=false`

```bash
python3 <PROFILE>/skills/designbro-tools/scripts/setup_wizard.py status
python3 <PROFILE>/skills/designbro-tools/scripts/setup_wizard.py start
python3 <PROFILE>/skills/designbro-tools/scripts/setup_wizard.py answer "Risposta" --chat-id <CHAT_ID> --user-id <USER_ID>
```

Domande:
1. Nome brand
2. Settore (food, tech, fashion, finance, legal, retail)
3. Colore HEX o mood
4. Gruppo Telegram preview
5. ID admin approvazioni

Post-wizard: `logo concept` | `palette colori` | `brand kit`