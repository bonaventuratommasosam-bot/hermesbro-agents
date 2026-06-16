# Stato Deploy Machiavelli — 8 Giugno 2026

## Cron Job Attivi (19 totali)

| Componente | File | Cron | Stato |
|---|---|---|---|
| Bus Watcher | <HERMES_BOT>/bus-watcher.py | Daemon (300s) | ✅ |
| Task Executor | <HERMES_BOT>/task-executor.py | Ogni 20s | ✅ |
| Strategic Dispatch | <HERMES_BOT>/strategic-dispatch.py | Ogni 5min | ✅ |
| Strategic Collect | <HERMES_BOT>/strategic-collect.py | Ogni 2min | ✅ |
| Scout Loop | <HERMES_BOT>/scout-loop.py | Ogni 6h | ✅ |
| Debate Loop | <HERMES_BOT>/debate-loop.py | Ogni 5min | ✅ |
| Orchestrator | skills/machiavelli-tools/scripts/orchestrator.py | — | ✅ Patched |
| Machiavelli Gateway | hermes-machiavelli.service | — | ✅ Running |

## Loop Verificati

### 1. Strategico
Dispatch → Task Executor (1676 token) → Collect → Judge ("FALLITO") → Escalation

### 2. Contestazione (Debate)
2 bot rispondono indipendentemente con personalità autentica → sintesi DeepSeek

### 3. Scout
Check bus, bot, disk, cron → report ogni 6 ore

## Flusso Completo

1. Arriva un goal → strategic-dispatch.py lo scompone e scrive task nelle inbox dei bot
2. Ogni 20 secondi → task-executor.py legge SOUL.md del bot target, chiama DeepSeek, scrive risposta in outbox
3. Ogni 2 minuti → strategic-collect.py raccoglie risposte, chiama il judge (DeepSeek), completa o ri-dispatcha o scala a GribbitO
4. Ogni 6 ore → scout-loop.py controlla salute sistema, logga anomalie
5. Debate → manda stesso goal a N bot, cross-checka contraddizioni, sintetizza

## To-Do Residui

1. Thread ID Telegram — i cron job hanno "Chat not found", servono i thread ID corretti
2. Debate event-driven — ora è blocking, da rifattorizzare come strategic loop
3. Decompose qualità — machiavelli_tools.py assegna bot generici (es. "ducato" per task finanziari invece di "contabile")
