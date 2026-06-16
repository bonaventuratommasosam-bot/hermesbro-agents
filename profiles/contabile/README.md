# ContAIbile — Contabilità Operativa

**Il contabile operativo per PMI e ristoranti su Telegram.** ContAIbile centralizza movimenti, IVA stimata, scadenze fiscali e food cost con un ledger locale, alert e report configurabili.

- **Goal:** Ricavi, spese, IVA stimata, scadenze fiscali. Ogni numero ha fonte e data.
- **Motto:** *«I conti non mentono. Le persone sì. E io sto dalla parte dei conti.»*
- **Emoji:** 📊

## Cosa fa

| Funzionalità | Descrizione |
|---|---|
| **Movimenti** | Registra ricavi/spese in linguaggio naturale → ledger locale (`cache/ledger.jsonl`) |
| **IVA stimata** | Calcolo IVA da movimenti registrati (non liquidazione ufficiale) |
| **Scadenze** | Alert IVA, F24 con soglia configurabile (default 7 giorni prima) |
| **Food cost** | Check per settore ristorazione, integrazione via bus GROOT |
| **Riepilogo** | Margine, totali, trend base |
| **Cron** | Check scadenze giornaliero, report settimanale |

**Non fa:** sostituzione commercialista, dichiarazioni ufficiali, bilanci certificati.

## Requisiti

- **Hermes Agent** — runtime per eseguire il profilo agente
- **Telegram Bot Token** — creato via @BotFather
- **LLM API Key** — provider LLM configurato nel `.env`
- **Python 3.11+** — per gli script skill (contabile-tools)

## Setup rapido

### 1. Crea il bot Telegram

```bash
# @BotFather → crea bot → salva token
```

### 2. Configura il profilo

```bash
# Crea profilo in ~/.hermes/profiles/contabile/
echo "TELEGRAM_BOT_TOKEN=*** >> .env
echo "OPENAI_API_KEY=*** >> .env
```

### 3. Compila `contabile-config.yaml`

```yaml
company:
  name: "Azienda SRL"
  piva: "01234567890"
  regime: forfettario
  iva_regime: trimestrale
  sector: "ristorazione"
telegram:
  group_chat_id: "-1001234567890"
  admin_chat_id: "123456789"
roles:
  admin: [123456789]
```

### 4. Avvia e configura

```bash
hermes start --profile contabile
# In Telegram: scrivi "setup" per il wizard di configurazione
```

### 5. Test rapido

- `ricavo 500 consulenza` → registra ricavo
- `spesa 120 fornitore` → registra spesa
- `iva` / `liquidazione iva` → calcola IVA stimata
- `scadenze` → mostra prossime scadenze
- `riepilogo` → bilancio del periodo

## Esempi d'uso

| Input chat | Cosa fa |
|---|---|
| `ricavo 3500 catering weekend` | Registra ricavo di €3500, categoria catering |
| `spesa 890 fornitore carne` | Registra spesa €890 |
| `iva` | Calcola IVA stimata da movimenti del trimestre |
| `scadenze` | Elenco prossimi adempimenti (IVA, F24) |
| `food cost 32% su 5000` | Verifica food cost su ricavi ristorazione |
| `riepilogo giugno` | Report mensile entrate/uscite/margine |
| `setup` | Avvia wizard di configurazione |

## Configurazione

| Campo chiave | Descrizione |
|---|---|
| `fiscal.default_iva` | Aliquota IVA default (22%) |
| `fiscal.food_cost_alert_pct` | Soglia alert food cost (35%) |
| `fiscal.anomaly_threshold_eur` | Soglia anomalia movimenti (€500) |
| `cron.deadline_check` | Check scadenze giornaliero (lun-ven 8:00) |
| `cron.weekly_report` | Report settimanale (lun 9:00) |

## Regole operative

- Mai inventare numeri — chiedi se manca importo/data
- Alert admin solo per scadenze ≤ soglia o anomalie > threshold config
- Disclaimer: stime AI, non sostituiscono commercialista

## Integrazione flotta HermesBro

| Agente | Dati scambiati |
|---|---|
| **GROOT** | Ricavi giornalieri, food cost alert |
| **Lawrenzo** | Scadenze fiscali, documenti compliance |
| **El-froggo** | P&L crypto |
| **Ducato** | Report trimestrale bilanci |

Bus: `python3 .../bus-send.py send contabile <target> "<msg>" info`
