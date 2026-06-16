# Wannabe Lab — R&D Incubator

**L'incubatore R&D della flotta HermesBro.** Wannabe Lab testa skill, logga esperimenti, propone feature e promuove in produzione solo dopo review del Supervisor.

- **Goal:** R&D controllato — coda esperimenti, test skill, proposte feature con review Supervisor.
- **Motto:** *«Fallire veloce, imparare in fretta, promuovere con evidenza.»*
- **Emoji:** 🧪

## Cosa fa

| Funzionalità | Descrizione |
|---|---|
| **Gestione esperimenti** | Log esperimenti con ipotesi, focus, stato (proposed → active → reviewing → promoted/rejected) |
| **Proposte feature** | Raccolta idee e proposte dalla flotta e dal founder |
| **Skill testing** | Esecuzione test su skill in sviluppo |
| **Coda lab** | Queue prioritaria, max 5 esperimenti attivi |
| **Promozione** | Sposta esperimenti in produzione dopo approvazione Supervisor |

**Non fa:** deploy in produzione senza review, test su ambienti live.

## Requisiti

- **Hermes Agent** — runtime per eseguire il profilo agente
- **Telegram Bot Token** — creato via @BotFather
- **LLM API Key** — provider LLM configurato nel `.env`

## Setup rapido

### 1. Crea il bot Telegram

```bash
# @BotFather → crea bot → salva token
```

### 2. Configura il profilo

```bash
# Crea profilo in ~/.hermes/profiles/wannabe/
echo "TELEGRAM_BOT_TOKEN=*** >> .env
echo "OPENAI_API_KEY=*** >> .env
```

### 3. Compila `lab-config.yaml`

```yaml
lab:
  name: "R&D Lab"
  focus: skills
  supervisor: supervisor
telegram:
  group_chat_id: "-1001234567890"
  admin_chat_id: "123456789"
experiments:
  max_active: 5
  require_review: true
```

### 4. Avvia

```bash
hermes start --profile wannabe
```

### 5. Test rapido

- `setup` → wizard configurazione
- `esperimento skill X` → log nuovo esperimento
- `coda lab` → mostra coda esperimenti
- `promuovi EXP-1` → propone per promozione a Supervisor

## Esempi d'uso

| Input chat | Cosa fa |
|---|---|
| `esperimento skill bus-send v2` | Crea EXP con ipotesi "skill bus-send v2" |
| `proponi dark mode` | Crea proposta feature "dark mode" |
| `coda lab` | Mostra tutti gli esperimenti e il loro stato |
| `test stub menu-engine` | Lancia test su skill stub |
| `promuovi EXP-351c41` | Invia richiesta promozione a Supervisor |
| `setup` | Wizard configurazione iniziale |

## Configurazione

| Campo | Descrizione |
|---|---|
| `lab.focus` | Area di focus del lab (skills, tools, processi) |
| `lab.supervisor` | Nome agente Supervisor (default: "supervisor") |
| `experiments.max_active` | Massimo esperimenti attivi contemporanei (5) |
| `experiments.require_review` | Richiede review prima della promozione |
| `cron.weekly_digest` | Digest settimanale esperimenti (venerdì 10:00) |

## Integrazione flotta HermesBro

| Agente | Interazione |
|---|---|
| **Supervisor** | Promozione esperimenti in produzione |
| **DesignBro** | Asset UI da testare |
| **Machiavelli** | Schedulazione esperimenti paralleli |

Bus: `python3 .../bus-send.py send wannabe <target> "<msg>" info`
