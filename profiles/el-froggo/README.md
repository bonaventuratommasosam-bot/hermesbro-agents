# El-froggo — Fleet Lead

**Il leader della flotta HermesBro.** El-froggo coordina la comunicazione founder ↔ squadra: pulse servizi, brief giornalieri, escalation.

- **Goal:** Coordinamento founder ↔ squadra. Report, pulse servizi, escalation.
- **Motto:** *«La flotta dorme, io no.»*
- **Emoji:** 🐸

## Cosa fa

| Funzionalità | Descrizione |
|---|---|
| **Fleet Pulse** | Stato operativo di tutti gli agenti della flotta |
| **Daily Brief** | Report giornaliero per il founder |
| **Escalation** | Gestione criticità e dispatch verso l'agente competente |
| **Market Overview** | Intel crypto (informativo, non trading) |

**Non fa:** trading produzione (H2BB/GribbitO sono fuori scope), decisioni operative senza consultazione founder.

## Requisiti

- **Hermes Agent** — runtime per eseguire il profilo agente
- **Telegram Bot Token** — creato via @BotFather
- **LLM API Key** — provider LLM configurato nel `.env`
- **Accesso bus HermesBro** — per comunicazione inter-agente

## Setup rapido

### 1. Crea il bot Telegram

```bash
# @BotFather → crea bot → salva token
```

### 2. Configura il profilo

```bash
# Crea profilo in ~/.hermes/profiles/el-froggo/
echo "TELEGRAM_BOT_TOKEN=*** >> .env
echo "OPENAI_API_KEY=*** >> .env
```

### 3. Compila `fleet-lead-config.yaml`

```yaml
org:
  name: "La Tua Org"
  founder_chat_id: "YOUR_CHAT_ID"
fleet:
  report_time: 08:00
  agents: []
telegram:
  group_chat_id: "YOUR_GROUP_CHAT_ID"
  admin_chat_id: "YOUR_ADMIN_CHAT_ID"
roles:
  admin:
  - 0  # sostituisci con il tuo Telegram user ID
```

### 4. Avvia

```bash
hermes start --profile el-froggo
```

### 5. Test rapido

- `setup` → wizard configurazione
- `pulse` → stato flotta
- `brief` → daily brief per founder
- `escala server down` → escalation criticità

## Esempi d'uso

| Input chat | Cosa fa |
|---|---|
| `setup` | Wizard configurazione |
| `pulse` | Mostra lo stato operativo di tutti gli agenti |
| `brief` | Genera daily briefing per il founder |
| `escala mancato pagamento fornitore` | Escalation al founder con dettagli |
| `mercato` | Overview mercato crypto (informativo) |

## Configurazione

| Campo | Descrizione |
|---|---|
| `org.founder_chat_id` | Telegram chat ID del founder |
| `fleet.report_time` | Ora del daily brief |
| `fleet.agents` | Lista agenti nella flotta |
| `reports.daily_enabled` | Abilita report giornalieri automatici |
| `cron.daily_brief` | Schedule cron per daily brief |

## Integrazione flotta HermesBro

| Agente | Interazione |
|---|---|
| **Machiavelli** | Dispatch operativo |
| **Frank** | Implementazione task |
| **Tutta la squadra** | Status in pulse |

Bus: `python3 .../bus-send.py send el-froggo <target> "<msg>" info`
