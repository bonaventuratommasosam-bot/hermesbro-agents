# GROOT — Brigata Ristorante

**L'assistente tecnologico della squadra di cucina.** GROOT centralizza scorte, lista spesa, food cost e organizzazione per la brigata del ristorante tramite un agente conversazionale Hermes su Telegram, condiviso e proattivo.

- **Goal:** Nessuna mancanza persa in chat private. Una lista ufficiale su Google Sheets. La brigata chiede numeri e idee al bot come al capo partida digitale.
- **Motto:** *«Se manca qualcosa, lo scrivi a me. Io lo metto in lista, calcolo il costo e ti dico come organizzarti meglio.»*
- **Emoji:** 📋

## Cosa fa

| Funzionalità | Descrizione |
|---|---|
| **Lista spesa** | Segnalazione mancanze in linguaggio naturale → parse → write su Google Sheets `LISTA_SPESA` → conferma in chat |
| **Query & stato** | "cosa c'è da comprare?", "urgenti", "ordinato X", "ricevuto X" |
| **Food cost** | Calcolo costo porzione, margine, FC% da ingredienti o ricetta |
| **Prep & organizzazione** | Piano mise en place per N coperti, checklist, collegamento a lista spesa |
| **Proattività (cron)** | Riepilogo mattina, alert pre-servizio, riepilogo post-servizio, trend settimanale |
| **Multi-utente** | Funziona in gruppo Telegram con ruoli: squad, chef/responsabile, admin |

**Non fa:** ordini automatici a fornitori, modifiche menu prezzi in cassa, messaggi a clienti finali.

## Requisiti

- **Hermes Agent** — runtime per eseguire il profilo agente
- **Telegram Bot Token** — creato via @BotFather, aggiunto al gruppo brigata
- **LLM API Key** — provider LLM (OpenAI, OpenRouter, DeepSeek, ecc.) configurato nel `.env`
- **Google Sheets API** — Service Account con ruolo Editor sul foglio del cliente (tab: `LISTA_SPESA`, `MAGAZZINO`, `ORDINI`, `MEMORIA`, `PROMEMORIA`)
- **Python 3.11+** — per gli script skill (groot-tools)

## Setup rapido

### 1. Crea il bot Telegram

```bash
# Vai su @BotFather in Telegram, crea un nuovo bot e salva il token
# Poi aggiungi il bot al gruppo della brigata come amministratore
```

### 2. Configura il profilo Hermes

```bash
# Clona o crea il profilo in ~/.hermes/profiles/groot/
# Inserisci il token Telegram e la LLM API key nel .env:
echo "TELEGRAM_BOT_TOKEN=tuo_token_qui" >> .env
echo "OPENAI_API_KEY=tua_chiave_qui" >> .env    # o altro provider
```

### 3. Compila `brigata-config.yaml`

```yaml
venue:
  name: "Trattoria da Marco"              # Nome del locale
telegram:
  group_chat_id: "-1001234567890"         # ID gruppo brigata
  admin_chat_id: "123456789"             # ID admin
google_sheets:
  spreadsheet_id: "1abc...xyz"           # ID del foglio Google
roles:
  admin: [123456789]                     # Telegram user ID admin
  chef: [987654321]                      # (opzionale) Chef/responsabile
```

### 4. Collega Google Sheets

1. Crea un foglio Google con tab **LISTA_SPESA** (colonne: `Data | Item | Quantita | Unita | Priorita | Stato | Segnalato_da | Note | Aggiornato_il`)
2. Condividilo con il Service Account Hermes
3. Inserisci lo **Spreadsheet ID** in `brigata-config.yaml`

### 5. Avvia il bot

```bash
hermes start --profile groot
```

### 6. Test rapido

Scrivi nel gruppo Telegram:
- `finita la panna` → il bot chiede quantità e aggiunge a LISTA_SPESA
- `lista spesa` → mostra le voci aperte
- `urgenti` → mostra solo le priorità alte
- `costo carbonara` → calcola food cost

## Esempi d'uso

| Input chat | Cosa fa |
|---|---|
| `finita la panna` | Aggiunge "Panna" a LISTA_SPESA, chiede quantità se non specificata |
| `servono 3 kg pomodori pelati` | Aggiunge 3 kg Pomodori Pelati, priorità normale |
| `manca carta forno urgente` | Aggiunge con priorità urgente |
| `cosa c'è in lista?` | Elenca voci aperte |
| `ordinato il burro` | (chef) imposta stato "ordinato" |
| `ricevuto 10 kg farina` | (chef) stato "ricevuto" + aggiorna MAGAZZINO |
| `costo lasagne` | Calcolo costo porzione + FC% |
| `prep per 60 coperti sabato` | Piano step + checklist + ingredienti mancanti |

## Configurazione avanzata

- **Cron proattivi:** morning riepilogo (07:30), pre-servizio alert, post-servizio riepilogo, weekly report
- **Ruoli:** admin (config, report), chef (stati, priorità), squad (segnalazioni, query)
- **Soglie:** target_food_cost_pct (default 32%), merge_same_day per deduplica
- **Disaster recovery:** cache locale `cache/pending-spesa.jsonl` se Google Sheets non risponde, retry 3x con backoff

## File del profilo

| File | Descrizione |
|---|---|
| `SOUL.md` | Identità, personalità, competenze core |
| `GOAL.md` | Missione, obiettivi, flussi, regole |
| `SUBGOALS.md` | Sub-obiettivi con criteri di accettazione |
| `WIZARD.md` | Wizard 5 domande per onboarding cliente |
| `CONFIGURAZIONE_CLIENTE.md` | Guida configurazione per il cliente |
| `brigata-config.yaml` | Configurazione cliente (Sheet, gruppo, ruoli, cron) |
| `skills/groot-tools/` | Skill con script Python (parse, Sheets, food cost) |

## Integrazione flotta HermesBro

GROOT comunica via bus con:
- **ContAIbile** — ricavi giornalieri, food cost alert
- **DesignBro** — menu, volantini, QR code
- **Lawrenzo** — HACCP, SCIA, documenti assunzione
