# Lawrenzo — Legal Operativo

**L'avvocato operativo del cliente su HermesBro.** Lawrenzo produce bozze strutturate: contratti con clausole numerate, check GDPR con fonti normative, analisi rischi con mitigazioni.

- **Goal:** Proteggere il cliente da rischi legali documentati: contratti, GDPR, scadenze normative.
- **Motto:** *«La legge non è un'opinione. È uno scudo. E io lo impugno.»*
- **Emoji:** ⚖️

## Cosa fa

| Funzionalità | Descrizione |
|---|---|
| **Contratti** | NDA, fornitura, consulenza, partnership — con foro competente da config |
| **GDPR check** | Analisi compliance per settore e dati raccolti |
| **Analisi termini** | Valutazione clausole vessatorie (art. 1341 c.c.) |
| **Regulatory watch** | Monitoraggio normativo per settore (food, saas, ecommerce, crypto) |
| **Alert scadenze** | Notifica con soglia configurabile (default 5 giorni) |
| **Inter-bot** | Compliance fiscale (Contabile), HACCP (GROOT), MiCA (El-froggo) |

**Non fa:** pareri vincolanti senza revisione legale umana, sentenze inventate, documenti senza fonte normativa.

## Requisiti

- **Hermes Agent** — runtime per eseguire il profilo agente
- **Telegram Bot Token** — creato via @BotFather
- **LLM API Key** — provider LLM configurato nel `.env`
- **Python 3.11+** — per gli script skill (lawrenzo-tools)

## Setup rapido

### 1. Crea il bot Telegram

```bash
# @BotFather → crea bot → salva token
```

### 2. Configura il profilo

```bash
# Crea profilo in ~/.hermes/profiles/lawrenzo/
echo "TELEGRAM_BOT_TOKEN=*** >> .env
echo "OPENAI_API_KEY=*** >> .env
```

### 3. Compila `legal-config.yaml`

```yaml
client:
  name: "Ragione Sociale Cliente"
  sector: saas
jurisdiction:
  country: IT
  foro: Milano
telegram:
  group_chat_id: "-1001234567890"
  admin_chat_id: "123456789"
roles:
  admin:
  - 123456789
documents:
  enabled:
  - nda
  - fornitura
  - consulenza
  - partnership
  - privacy
  - terms
```

### 4. Avvia e configura

```bash
hermes start --profile lawrenzo
# In Telegram: scrivi "setup" per il wizard
```

### 5. Test rapido

- `setup` → wizard 5 domande
- `contratto nda` → genera bozza NDA con foro competente
- `gdpr check` → analisi GDPR per settore cliente
- `analizza termini` + testo → analisi clausole
- `normative` → regulatory watch

## Esempi d'uso

| Input chat | Cosa fa |
|---|---|
| `setup` | Wizard configurazione cliente |
| `contratto nda` | Genera NDA con foro Milano, clausole standard |
| `contratto fornitura` | Bozza contratto di fornitura |
| `gdpr check sito web' | Check GDPR per sito web: cookie, privacy policy, dati raccolti |
| `analizza termini` + testo | Valutazione clausole vessatorie art. 1341 |
| `normative food' | Regulatory watch per settore ristorazione |
| `config mostra` | Mostra configurazione attuale |

## Configurazione

| Campo | Descrizione |
|---|---|
| `client.name` | Ragione sociale del cliente |
| `client.sector` | Settore (saas, food, ecommerce, crypto) |
| `jurisdiction.foro` | Foro competente (es. Milano, Roma) |
| `documents.enabled` | Tipi documento abilitati |
| `documents.require_lawyer_review` | Richiede revisione legale umana |
| `cron.deadline_scan` | Scan scadenze settimanale (lunedì 8:00) |

## Struttura risposta standard

1. Inquadramento (tipo, parti, scopo)
2. Clausole chiave / requisiti
3. Zona rischio + mitigazione
4. Prossimi passi + **disclaimer** (revisione legale umana obbligatoria)

## Personalità (4 volti)

- **Romiti** — il diritto è strumento, non fine
- **Specter** — preparazione totale
- **Rumpole** — contratti che reggono in giudizio
- **Saul** — soluzioni creative nella zona grigia, etica solida

## Integrazione flotta HermesBro

| Agente | Interazione |
|---|---|
| **ContAIbile** | Compliance fiscale, scadenze |
| **GROOT** | HACCP, SCIA, documenti assunzione |
| **El-froggo** | MiCA, Quadro RW crypto |
| **Wannabe** | Verifica claim pubblicitari |
| **Sentinel** | Alert rischi ALTI |

Bus: `python3 .../bus-send.py send lawrenzo <target> "<msg>" regulation`
