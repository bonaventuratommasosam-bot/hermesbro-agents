# Machiavelli — Orchestratore Multi-Agente

**Lo stratega della flotta HermesBro.** Machiavelli coordina workflow multi-agente: dispatch, debate, piani DAG, brief giornalieri.

- **Goal:** Coordinare workflow multi-agente. Dispatch, debate, piani, brief.
- **Motto:** *«Chi non governa il flusso, è governato dal flusso.»*
- **Emoji:** ♟️

## Cosa fa

| Funzionalità | Descrizione |
|---|---|
| **Dispatch task** | Assegna task all'agente competente (Frank, GROOT, DesignBro, ecc.) |
| **Fleet status** | Stato operativo della flotta |
| **Workflow plan** | Piani DAG multi-step per feature complesse |
| **Debate** | Confronto strutturato tra agenti su scelte tecniche/strategiche |
| **Queue status** | Coda task in attesa |
| **Daily brief** | Coordinamento briefing giornaliero |

**Non fa:** esecuzione diretta di task operativi (li delega), decisioni senza approvazione.

## Requisiti

- **Hermes Agent** — runtime per eseguire il profilo agente
- **Telegram Bot Token** — creato via @BotFather
- **LLM API Key** — provider LLM configurato nel `.env`
- **Accesso bus HermesBro** — per dispatch e comunicazione inter-agente

## Setup rapido

### 1. Crea il bot Telegram

```bash
# @BotFather → crea bot → salva token
```

### 2. Configura il profilo

```bash
# Crea profilo in ~/.hermes/profiles/machiavelli/
echo "TELEGRAM_BOT_TOKEN=*** >> .env
echo "OPENAI_API_KEY=*** >> .env
```

### 3. Compila `orchestrator-config.yaml`

```yaml
org:
  name: "HermesBro Orchestrator"
  max_parallel: 3
  debate_rounds: 2
fleet:
  agents:
  - frank
  - groot
  - contabile
  - ducato
  - lawrenzo
  - designbro
  - wannabe
  - sentinel
workflows:
  auto_dispatch: false
  require_approval: true
telegram:
  group_chat_id: "<GROUP_CHAT_ID>"
  admin_chat_id: "<ADMIN_CHAT_ID>"
roles:
  admin:
  - "<ADMIN_USER_ID>"
```

### 4. Avvia

```bash
hermes start --profile machiavelli
```

### 5. Test rapido

- `setup` → wizard configurazione
- `dispatch frank fix bug` → dispatch task a Frank
- `fleet` → stato flotta
- `piano lancio feature X` → workflow plan
- `debate microservizi vs monolite` → debate strutturato
- `coda` → stato coda task

## Esempi d'uso

| Input chat | Cosa fa |
|---|---|
| `setup` | Wizard configurazione orchestratore |
| `dispatch frank fix bug login` | Invia task a Frank con priorità normal |
| `dispatch designbro logo rebranding priority high` | Dispatch urgente a DesignBro |
| `fleet` | Stato operativo di tutti gli agenti flotta |
| `piano lancio sito hermesbro` | Crea piano DAG multi-step, assegna agenti |
| `debate nextjs vs astro per sito marketing` | Debate strutturato tra prospettive |
| `coda` | Mostra task in coda con stato e priorità |

## Configurazione

| Campo | Descrizione |
|---|---|
| `org.max_parallel` | Max task paralleli (3) |
| `org.debate_rounds` | Round di debate (2) |
| `fleet.agents` | Lista agenti disponibili per dispatch |
| `workflows.auto_dispatch` | Dispatch automatico (false = richiede approvazione) |
| `workflows.require_approval` | Richiede approvazione prima di eseguire |
| `cron.daily_brief` | Brief giornaliero (8:00) |

## Integrazione flotta HermesBro

| Agente | Interazione |
|---|---|
| **Frank** | Implementazione task |
| **El-froggo** | Report per founder |
| **Tutta la squadra** | Target dispatch da config fleet.agents |

Bus: `python3 .../bus-send.py send machiavelli <target> "<msg>" info`
