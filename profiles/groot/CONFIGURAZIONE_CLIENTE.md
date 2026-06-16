# GROOT Brigata — Guida configurazione cliente

Ogni cliente configura il proprio bot **senza toccare il codice**. Due modi: file YAML o comandi Telegram (admin).

## 1. File principale: `brigata-config.yaml`

Percorso sul profilo: `{{HERMES_HOME}}/brigata-config.yaml`

### Campi obbligatori per andare live

| Campo | Esempio | Note |
|-------|---------|------|
| `venue.name` | `Trattoria da Marco` | Nome locale (messaggi proattivi) |
| `telegram.group_chat_id` | `{{TELEGRAM_CHAT_ID}}` | Gruppo brigata |
| `google_sheets.spreadsheet_id` | `1abc...xyz` | Foglio con tab LISTA_SPESA |
| `roles.admin` | `[{{TELEGRAM_USER_ID}}]` | Telegram user ID dell'admin |

### Campi opzionali (default sensati)

- `operations.target_food_cost_pct` — default 32%
- `operations.service_time` — default 20:00
- `operations.merge_same_day` — deduplica voci stesso giorno
- `google_sheets.tabs.*` — rinomina tab se il tuo foglio usa nomi diversi
- `roles.chef` — chi può segnare ordinato/ricevuto
- `cron.enabled` — attiva job mattina/post-servizio dopo setup

## 2. Setup Google Sheets

1. Crea o duplica un foglio con tab **LISTA_SPESA**
2. Colonne consigliate: `Data | Item | Quantita | Unita | Priorita | Stato | Segnalato_da | Note | Aggiornato_il`
3. Condividi il foglio con il service account Hermes (email fornita in onboarding)
4. Incolla lo **Spreadsheet ID** dall'URL in `google_sheets.spreadsheet_id`

## 3. Comandi Telegram (admin)

Dopo il primo avvio, l'admin può configurare via chat:

```
config mostra
config venue "Nome Ristorante"
config sheet 1abc...xyz
config gruppo {{TELEGRAM_CHAT_ID}}
config foodcost 30
config servizio 21:00
config chef 123456789,987654321
config cron on
```

Il bot esegue `configure_brigata.py` e conferma.

## 4. Script CLI (SSH o supporto)

```bash
python3 .../configure_brigata.py show
python3 .../configure_brigata.py set telegram.group_chat_id {{TELEGRAM_CHAT_ID}}
python3 .../configure_brigata.py set google_sheets.spreadsheet_id 1abc...
python3 .../configure_brigata.py validate
python3 .../configure_brigata.py apply-cron
```

## 5. Checklist go-live

- [ ] Bot Telegram creato (@BotFather) e token in `.env`
- [ ] Bot aggiunto al gruppo brigata (admin)
- [ ] `brigata-config.yaml` compilato
- [ ] `configure_brigata.py validate` → OK
- [ ] `cron.enabled: true` + `apply-cron`
- [ ] Test: `finita la panna` → riga su LISTA_SPESA

## 6. Cosa puoi personalizzare liberamente

- Nomi tab Sheets
- Soglia food cost
- Orari cron e fuso orario
- Ruoli chef/admin/squad
- Lingua default
- Pausa messaggi proattivi (festivi/chiusure)

**Non serve** modificare SOUL.md o SKILL.md — il bot legge `brigata-config.yaml` a ogni sessione.
