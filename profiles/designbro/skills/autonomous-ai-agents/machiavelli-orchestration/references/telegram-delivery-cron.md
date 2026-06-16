# Telegram Delivery per Machiavelli Cron Jobs

## Il Problema

I cron job Machiavelli mandano messaggi Telegram ma falliscono con:
```
Chat not found
```

## Cause Comuni

### 1. Bot non membro del gruppo
Il bot GribbitO (o il bot Hermes del profilo) **deve essere aggiunto manualmente** al gruppo. L'invite link da solo non basta — Hermes non ha accesso alla lista degli aggiornamenti di un gruppo dove non è stato invitato.

**Soluzione:** Apri il gruppo Telegram → Members → Add Member → cerca il bot (es. `@GribbitO_bot`).

### 2. ID positivo vs negativo
Un supergruppo Telegram ha sempre ID negativo (es. `-1001234567890`).
ID positivi bassi (es. `<CHAT_ID>`) non sono supergruppi validi.

**Soluzione:** Dopo aver aggiunto il bot, manda un messaggio nel gruppo. Poi:
```bash
python3 -c "
import urllib.request, json
t = open('<HERMES_ROOT>/.env').read().split()
t = [x for x in t if 'TELEGRAM_BOT_TOKEN' in x][0].split('=',1)[1]
r = urllib.request.urlopen(f'https://api.telegram.org/bot{t}/getUpdates').read()
d = json.loads(r)
for u in d.get('result',[]):
    msg = u.get('message') or u.get('channel_post') or {}
    c = msg.get('chat',{})
    print(f'Chat ID: {c.get(\"id\")} | {c.get(\"title\",\"?\")} ({c.get(\"type\",\"?\")})')
    if 'message_thread_id' in msg:
        print(f'  Thread ID: {msg[\"message_thread_id\"]}')
"
```

### 3. Thread ID mancante
Se il gruppo usa topic, ogni topic ha un `message_thread_id` diverso.
Il formato per il deliver è: `telegram:<chat_id>:<thread_id>`

### 4. Updates vuoti
Se `getUpdates` ritorna `result: []`:
- Il bot non ha mai ricevuto messaggi (non è membro — vedi punto 1)
- Oppure il bot è stato aggiunto ma nessuno ha scritto. Manda "test" nel gruppo.

## Comando Rapido di Test

```bash
python3 -c "
import urllib.request, json
t = open('<HERMES_ROOT>/.env').read().split()
t = [x for x in t if 'TELEGRAM_BOT_TOKEN' in x][0].split('=',1)[1]
chat_id = -1001234567890  # SOSTITUISCI
r = urllib.request.urlopen(urllib.request.Request(
    f'https://api.telegram.org/bot{t}/sendMessage',
    data=json.dumps({'chat_id': chat_id, 'text': 'Test da GribbitO'}).encode(),
    headers={'Content-Type': 'application/json'}
)).read()
print(json.loads(r))
"
```

## Esempio Funzionante

Questa sessione: chat_id non ancora trovato. Il bot GribbitO è stato aggiunto al gruppo ma nessuno ha mandato messaggi → `getUpdates` vuoto. <FOUNDER> deve scrivere "test" nel gruppo o mandare un messaggio per popolare gli aggiornamenti.
