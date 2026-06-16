# Hermes PC Bridge — Manda lavoro a Hermes PC

Quando l'utente chiede di mandare un progetto, un task di coding, o qualsiasi lavoro a "Hermes PC" o "il PC", usa questo bridge.

## Come funziona

Il PC dietro NAT ha un worker che polla il VPS ogni 30 secondi. Tu crei un task sul VPS, il worker lo prende, esegue Hermes localmente sul PC, e scrive il risultato.

## Creare un task

```bash
pc-task-create "titolo" "body con istruzioni dettagliate" "nome-utente-telegram"
```

- **titolo**: breve, descrittivo (es. "Crea landing page per HermesBro")
- **body**: istruzioni COMPLETE e dettagliate — il PC non ha contesto della chat, solo quello che scrivi qui
- **nome-utente**: chi ha fatto la richiesta (per tracciamento)

Esempio:
```bash
pc-task-create "Crea API FastAPI per gestione task" "Crea un'app FastAPI con: 1) Endpoint POST /tasks per creare task 2) Endpoint GET /tasks per listarli 3) SQLite come DB 4) Mettila in <WORK_DIR>/task-app/ con requirements.txt" "<USER_NAME>"
```

## Controllare il risultato

```bash
pc-task-check <task_id>
```

Codici di uscita:
- 0 = completato (stampa il risultato)
- 1 = task non trovato
- 2 = ancora in esecuzione
- 3 = in coda (pending)

## Best practices

1. **Sii dettagliato nel body** — il PC non vede la chat, solo il body del task
2. **Specifica il percorso** dove creare file (es. "<WORK_DIR>/progetto/")
3. **Includi tutto**: dipendenze, struttura file, requisiti tecnici
4. **Dopo aver creato il task**, comunica all'utente il task ID e che il PC lo sta processando
5. **Polla il risultato** ogni 30-60 secondi finché non è pronto
6. **Inoltra il risultato** all'utente su Telegram

## Limiti

- Il worker PC deve essere attivo (chiedi all'admin se non risponde)
- Esecuzione singola (un task alla volta)
- Timeout: ~5 minuti per task
- Solo coding/scripting, non può accedere a servizi Telegram del VPS
