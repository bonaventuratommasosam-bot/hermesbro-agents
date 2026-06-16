---
name: machiavelli-orchestration
description: "Deploy and operate the Machiavelli multi-bot strategic loop on Hermes. Pipeline: Dispatch → Task Executor → Collect → Judge → Escalation, plus Debate and Scout loops."
version: 1.0.0
author: GribbitO
platforms: [linux]
metadata:
  hermes:
    tags: [machiavelli, multi-agent, orchestration, bots, cron, strategic-loop]
---

# Machiavelli Orchestration

Deploy e gestione della pipeline multi-bot Machiavelli. Ogni bot ha una personalità unica (SOUL.md) e un task specifico. L'orchestratore dispatcha, raccoglie, giudica e scala.

## Architettura

```
┌─ Goal in ingresso ──────────────────────────────────────┐
│                                                          │
│  strategic-dispatch.py (cron ogni 5min)                   │
│    ↓ scompone goal in task → scrive in /bus/task/*.json   │
│    ↓ assegna bot target (es. "wannabe" o "ducato")        │
│                                                          │
│  task-executor.py (cron ogni 20s)                         │
│    ↓ legge SOUL.md del bot target                         │
│    ↓ chiama DeepSeek API → scrive risposta in outbox      │
│                                                          │
│  strategic-collect.py (cron ogni 2min)                    │
│    ↓ raccoglie risposte dalla outbox                      │
│    ↓ chiama il judge (DeepSeek) → valuta                  │
│    ↓ COMPLETATO | RIPROVA | ESCALATION                    │
│    │        │          │                                  │
│    │        │          └─→ task a GribbitO                │
│    │        └─→ ri-dispatcha con feedback                 │
│    └─→ logga, notifica                                    │
└──────────────────────────────────────────────────────────┘
```

## Componenti

### 1. Strategic Loop (Dispatch → Execute → Collect → Judge)
File su: `<HERMES_BOT>/strategic-dispatch.py`, `task-executor.py`, `strategic-collect.py`
Cron: ogni 5min, 20s, 2min rispettivamente.

### 2. Debate Loop
Stesso goal a N bot indipendentemente → sintesi via DeepSeek → cross-check contraddizioni.
File: `<HERMES_BOT>/debate-loop.py`
Cron: ogni 5min.

### 3. Scout Loop
Controllo salute sistema: bus attivo, bot raggiungibili, disco, cron funzionanti.
File: `<HERMES_BOT>/scout-loop.py`
Cron: ogni 6h.

### 4. Bus Watcher (daemon)
Ascolta eventi sul bus dei bot, reagisce a comandi.
File: `<HERMES_BOT>/bus-watcher.py`
Run: daemon (300s tick).

## Cron Job Setup

I cron job Machiavelli girano sotto il profilo `machiavelli` in Hermes. Ogni job va creato con `deliver` impostato al chat ID Telegram di <FOUNDER>.

### Creare un cron job per Machiavelli:

```bash
# Schema generico: 
# cronjob(action='create',
#   schedule='...',
#   prompt='Run <HERMES_BOT>/<script>.py',
#   skills=['machiavelli-orchestration'],
#   deliver='telegram:<chat_id>:<thread_id>')
```

## Bot Routing

I task vengono assegnati ai bot in base al tipo:

- **Task finanziari** → contabile (non ducato — è un pitfall comune)
- **Task strategici/visione** → wannabe
- **Task operativi** → ducato
- **Task guardia/sicurezza** → sentinel
- **Task creativi** → elfroggo
- **Task design** → designbro

### PITFALL: routing generico
`machiavelli_tools.py` assegna bot generici (es. "ducato" per task finanziari invece di "contabile"). **Patch manuale necessaria** nel dispatch dopo il deploy.

## Telegram Delivery & Identità dei Bot

### Regola fondamentale: ogni bot parla con la propria voce

La flotta Machiavelli ha **un solo token Telegram** — tutti i bot condividono lo stesso. Questo significa che:
- I bot **non possono** mandare messaggi autonomamente nel gruppo
- L'orchestratore (GribbitO) è l'unico che può scrivere via Hermes `send_message()`
- Se l'utente chiede "voglio che i bot parlino da soli", serve un token Telegram **per ogni bot**

### Per l'autonomia reale dei bot

Ogni bot Machiavelli deve avere un bot Telegram suo, con nome e username unici. Procedura:

1. Creare i bot su BotFather (un token per bot)
2. Configurare `TELEGRAM_TOKEN=<token_unico>` nel `.env` di ogni bot in `<HERMES_BOT>/bots/<nome>/.env`
3. Aggiungere ogni bot al gruppo Telegram come membro
4. I bot possono ora parlare indipendentemente usando l'API Telegram diretta

### Configurazione gruppo attuale

- **Gruppo HermesBro**: `<GROUP_CHAT_ID>` (supergruppo, chat ID negativo)
- **DM <FOUNDER>**: `<ADMIN_CHAT_ID>`
- **GribbitO**: già membro, invia messaggi via `send_message()` di Hermes
- **Bot Machiavelli**: tutti condividono lo stesso token — **non parlano autonomamente**

### PITFALL: Il ventriloquo involontario

L'orchestratore che firma messaggi come "Ducato: ..." ma li manda col proprio token **è un fake**. I bot veri devono avere token propri. L'utente lo nota e lo corregge.

### PITFALL: "Chat not found"
Se il cron job fallisce con "Chat not found":
- Il bot non è membro del gruppo. Aggiungilo manualmente.
- Poi mandagli un messaggio e fai `getUpdates` per catturare l'ID esatto.
- O usa direttamente `send_message()` di Hermes per testare — salta il webhook.

### PITFALL: ID positivo non è un supergruppo
ID come `<CHAT_ID>` (positivo, ≤ 9 cifre) non è un supergruppo. Un supergruppo ha sempre ID negativo (es. `-1001827376543` o `<GROUP_CHAT_ID>`).

## SOUL.md dei bot

Ogni bot ha una personalità definita in `<HERMES_BOT>/bots/<nome>/SOUL.md`.
Il task-executor legge questo file per costruire il system prompt.

Esempio di SOUL.md:
```
# SOUL di [Nome Bot]
Personalità: [descrizione]
Competenze: [lista]
Regole: [comportamento]
```

## Dati su disco

Tutto risiede su:
- `<HERMES_BOT>/` — script principali
- `<HERMES_BOT>/bots/<nome>/` — bot individuali (SOUL.md, main.py)
- `<HERMES_BOT>/bus/` — bus messaggi
- `<HERMES_BOT>/bus/task/` — task inbox
- `<HERMES_BOT>/bus/outbox/` — risposte bot
- Cron job in Hermes: profilo `machiavelli`

## Esempi di Risposte Reali

Vedi `references/esempio-richiesta-bot.md` per un test concreto di Wannabe e Ducato su un task marketing. Le personalità emergono autenticamente; la convergenza sulla stessa risposta conferma che il sistema funziona, ma il routing dei bot è ancora generico.

## Stato Deploy

Vedi `references/deploy-stato-2026-06-08.md` per lo snapshot completo dei 19 cron job attivi con tutti i loop verificati.

## Telegram Delivery Troubleshooting

Vedi `references/telegram-delivery-cron.md` per diagnosticare "Chat not found" nei cron job. Il problema più comune: il bot non è membro del gruppo.

### PITFALL: ID positivo non è un supergruppo
`<CHAT_ID>` (positivo, ≤ 9 cifre) non è un supergruppo. Un supergruppo ha sempre ID negativo (es. `-1001827376543`). Se il primo tentativo fallisce con "Chat not found", il bot probabilmente non è stato aggiunto o l'ID è sbagliato.

### PITFALL: getUpdates vuoto dopo aver aggiunto il bot
Dopo aver aggiunto il bot al gruppo, qualcuno deve scrivere un messaggio prima che l'API di Telegram mostri l'update. Anche solo "test" basta.

## Verifica salute

```bash
# Tutti i bot alive?
hermes cron list --profile machiavelli

# Log degli script
journalctl -u hermes-machiavelli.service

# Scout ultimo report
ls -lt <HERMES_BOT>/scout-reports/
```

## To-Do noti

- **Debate event-driven**: ora è blocking (come orchestrator vecchio). Rifattorizzare come lo strategic loop (dispatch→execute→collect→judge).
- **Thread ID Telegram**: i cron job non trovano il canale finché <FOUNDER> non fornisce i chat_id/thread_id corretti.
