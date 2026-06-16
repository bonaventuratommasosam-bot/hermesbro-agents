---
name: telegram-bot-admin
description: Operazioni amministrative del bot Telegram — recupero chat ID, gestione webhook, troubleshooting gateway log, ispezione configurazione. Usa quando devi interagire con l'API Telegram o diagnosticare problemi di connessione.
category: devops
tags: [telegram, admin, gateway, webhook, chat-id]
---

# Telegram Bot Admin

Operazioni amministrative per il bot Telegram.

## Chat ID Discovery

Quando il webhook è attivo, `getUpdates` restituisce lista vuota. Tre metodi:

### Metodo 0: Invite Link → ID Negativo (quando l'utente dà un link)

L'utente spesso fornisce un invite link o un chat ID che **non funziona** per `send_message` perché positivo invece che negativo.

Regole:
- **I supergruppi hanno SEMPRE chat ID negativo**, di solito con prefisso `-100` (es. `-1001234567890`)
- Se l'utente dà un numero positivo, provare a negarlo
- Il `send_message` fallisce con "Chat not found" se il bot **non è membro del gruppo** — l'utente deve aggiungere il bot manualmente al gruppo

Flusso:
1. Utente dà invite link o numero positivo
2. Mandare il bot nel gruppo: chiedere all'utente di aggiungerlo (Members → Add Member)
3. Dopo che il bot è stato aggiunto, provare `send_message(message="test", target="telegram:-NUMERO")`
4. Se funziona, il chat ID è quello. Aggiornare `.env` e cron job con questo ID.

**PITFALL**: Non usare mai `getUpdates` subito dopo aver aggiunto il bot — il webhook consuma gli update. Usa `send_message` direttamente per testare.

### Metodo 1: Gateway Log (preferito, non invasivo)

1. Chiedere all'utente di scrivere un messaggio nel gruppo
2. Leggere il gateway log alla ricerca del campo `chat=`:
   ```
   tail -5 <gateway_log_path> | grep 'chat='
   ```

**Percorso gateway log:** `~/.hermes/profiles/<profile>/logs/gateway.log`

Esempio output:
```
inbound message: platform=telegram user=User chat=-1001234567890 msg='test'
chat_id = -1001234567890
```

### Metodo 2: Disabilitare webhook (solo se assolutamente necessario)

1. Ottenere il bot token da `~/.hermes/profiles/<profile>/.env` (variabile `TELEGRAM_BOT_TOKEN`)
2. Disabilitare webhook: `https://api.telegram.org/bot<TOKEN>/deleteWebhook`
3. Leggere update: `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Riabilitare webhook (riavviare il gateway)

**Preferire Metodo 1** — non interrompe il servizio.

## Config Inspection

Le configurazioni Telegram possono essere in:
- `~/.hermes/config.yaml` (sezione `telegram:`)
- `~/.hermes/profiles/<profile>/.env` (bot token, allowed users, chat ID)
- `~/.hermes/profiles/<profile>/gateway/` (file YAML/JSON del gateway channel, se presenti)

I target di invio disponibili si ottengono con:
```
send_message(action='list')
```
