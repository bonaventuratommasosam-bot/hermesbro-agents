# Ducato Finance — Analisi Finanziaria

**L'analista finanziario operativo della flotta HermesBro.** Ducato produce scenari finanziari: best/base/worst case, break-even, runway, allocazione portafoglio.

- **Goal:** Analisi finanziaria e scenari — portafoglio, margini, break-even, runway.
- **Motto:** *«Il prezzo è ciò che paghi. Il valore è ciò che ottieni.»*
- **Emoji:** 📊

## Cosa fa

| Funzionalità | Descrizione |
|---|---|
| **Analisi portafoglio** | Valutazione asset, allocazione, diversificazione |
| **Scenari finanziari** | Proiezioni best/base/worst case |
| **Break-even** | Calcolo punto di pareggio da costi e prezzo |
| **Runway** | Calcolo mesi di autonomia da cassa e burn rate |
| **Ratio analysis** | Indici finanziari su dati forniti |
| **Alert** | Notifica se runway < soglia o crypto > max configurato |

**Non fa:** promesse di rendimento, consulenza finanziaria personalizzata, trading automatico.

## Requisiti

- **Hermes Agent** — runtime per eseguire il profilo agente
- **Telegram Bot Token** — creato via @BotFather
- **LLM API Key** — provider LLM configurato nel `.env`
- **Python 3.11+** — per gli script skill (ducato-tools)

## Setup rapido

### 1. Crea il bot Telegram

```bash
# @BotFather → crea bot → salva token
```

### 2. Configura il profilo

```bash
# Crea profilo in ~/.hermes/profiles/ducato/
echo "TELEGRAM_BOT_TOKEN=*** >> .env
echo "OPENAI_API_KEY=*** >> .env
```

### 3. Compila `finance-config.yaml`

```yaml
client:
  name: "Nome Cliente"
  sector: "ristorazione"
  base_value: 25000
  monthly_burn: 4200
risk:
  max_single_asset_pct: 15
  max_crypto_pct: 30
  min_margin_pct: 15
  runway_alert_months: 3
telegram:
  group_chat_id: "CHAT_ID_GRUPPO"
  admin_chat_id: "ADMIN_CHAT_ID"
roles:
  admin:
  - ADMIN_USER_ID
```

### 4. Avvia

```bash
hermes start --profile ducato
```

### 5. Test rapido

- `setup` → wizard configurazione
- `portafoglio` → analisi portafoglio attuale
- `scenari` → proiezioni scenario
- `break even 50000 15000 120` → break-even con costi fissi 50k, variabili 15k, prezzo 120
- `runway` → calcolo autonomia cassa

## Esempi d'uso

| Input chat | Cosa fa |
|---|---|
| `setup` | Wizard configurazione iniziale |
| `portafoglio` | Analisi asset, allocazione %, diversificazione |
| `scenari crescita 20%` | Proiezioni best/base/worst con +20% ricavi |
| `break even 30000 8000 45` | Punto di pareggio: fissi €30k, var €8k, prezzo €45 |
| `runway` | Mesi di autonomia con cassa e burn correnti |
| `ratios` | Indici finanziari (margine, ROE, liquidità) |
| `aggiungi asset BTC 5000 crypto` | Aggiunge asset al portafoglio |
| `aggiungi asset ETF World 8000 equity` | Aggiunge ETF World al portafoglio |

## Configurazione

| Campo | Descrizione |
|---|---|
| `client.base_value` | Valore base del portafoglio |
| `client.monthly_burn` | Burn rate mensile |
| `risk.max_single_asset_pct` | Max % per singolo asset (15%) |
| `risk.max_crypto_pct` | Max % allocazione crypto (30%) |
| `risk.runway_alert_months` | Soglia alert runway (3 mesi) |
| `cron.monthly_report` | Report mensile (1° del mese 9:00) |

## Regole operative

- Disclaimersempre: scenari simulati, non consulenza finanziaria
- Alert admin solo se runway < soglia o crypto > max configurato
- Ogni analisi include: dati input, metodo, disclaimer

## Integrazione flotta HermesBro

| Agente | Interazione |
|---|---|
| **ContAIbile** | Bilancio, cash flow |
| **GROOT** | Costi evento, break-even ristorante |
| **El-froggo** | P&L crypto, allocazione portafoglio |
| **Wannabe** | KPI per contenuti |

Bus: `python3 .../bus-send.py send ducato <target> "<msg>" info`
