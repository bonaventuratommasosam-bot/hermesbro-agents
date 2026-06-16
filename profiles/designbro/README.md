# DesignBro Studio — Brand Identity Designer

**Il designer operativo del brand del tuo cliente su Telegram.** Trasforma brief in identità visiva documentata: logo, palette, typography, formati social — via chat e tool CLI Hermes.

- **Goal:** Ogni output ha HEX/font/dimensioni riproducibili; il cliente approva in chat; il brand kit resta coerente nel tempo.
- **Motto:** *«Dimmi il brief. Ti restituisco pixel, HEX e font — non opinioni.»*
- **Emoji:** 🎨

## Cosa fa

| Funzionalità | Descrizione |
|---|---|
| **Logo concept** | Logo con specifiche SVG/PNG, varianti, area di rispetto |
| **Palette colori** | Palette HEX con contrast ratio e uso per touchpoint |
| **Typography** | Font pairing (heading + body) con dimensioni e line-height |
| **Brand kit** | Linee guida brand complete |
| **Social specs** | Dimensioni esatte per IG (post/story), LinkedIn, X |
| **Menu & volantini** | Design per ristoranti (da brief GROOT) |
| **Review & approvazione** | Preview in chat + OK esplicito prima del finale |

**Non fa:** design senza specifiche tecniche, copy di competitor, usare Papyrus. Mai.

## Requisiti

- **Hermes Agent** — runtime per eseguire il profilo agente
- **Telegram Bot Token** — creato via @BotFather
- **LLM API Key** — provider LLM configurato nel `.env`
- **Python 3.11+** — per gli script skill (designbro-tools)

## Setup rapido

### 1. Crea il bot Telegram

```bash
# @BotFather → crea bot → salva token
```

### 2. Configura il profilo

```bash
# Crea profilo in ~/.hermes/profiles/designbro/
echo "TELEGRAM_BOT_TOKEN=*** >> .env
echo "OPENAI_API_KEY=*** >> .env
```

### 3. Compila `brand-config.yaml`

```yaml
brand:
  name: "Nome Brand"
  industry: "ristorazione"
  tagline: "La miglior cucina..."
  keywords: "tradizione, qualità, artigianale"
visual:
  primary_color: "#1E3A5F"
  mood: "professional"
  style: "modern"
telegram:
  group_chat_id: "-1001234567890"
  admin_chat_id: "123456789"
  require_approval: true
```

### 4. Avvia e configura

```bash
hermes start --profile designbro
# In Telegram: scrivi "setup" per il wizard brand
```

### 5. Test rapido

- `logo concept` → genera concept logo con specifiche
- `palette` → palette colori brand
- `font` / `tipografia` → font pairing
- `brand kit` → linee guida complete
- `dimensioni social` → formati per social network
- `setup` → wizard 5 domande per configurare il brand

## Esempi d'uso

| Input chat | Cosa fa |
|---|---|
| `logo concept raffineria' | Genera 3 concept logo con specifiche SVG/PNG |
| `palette estate 2025` | Palette colore stagionale con HEX |
| `font per menu' | Font pairing heading/body con dimensioni |
| `brand kit` | Documento linee guida brand completo |
| `dimensioni post IG` | Specifiche formato Instagram post/story |
| `menu volantino' | Design menu da brief (ristorante) |
| `approvo logo v2` | Finalizza e archivia design approvato |

## Configurazione

| Campo | Descrizione |
|---|---|
| `brand.name` | Nome del brand/cliente |
| `brand.industry` | Settore (ristorazione, tech, moda, ecc.) |
| `visual.primary_color` | Colore primario HEX |
| `visual.mood` | Tono (professional, creative, playful) |
| `output.formats` | Formati abilitati (logo, palette, typography, social, menu) |
| `telegram.require_approval` | Richiede approvazione esplicita prima del finale |

## Personalità operative

- **Gordon Ramsay del design** — zero tolleranza per brutto, educato ma diretto
- **Elon Musk — first principles** — design come strategia visiva
- **Pierre Devoldère — minimalista** — ogni elemento guadagna il suo spazio

## Integrazione flotta HermesBro

| Agente | Interazione |
|---|---|
| **GROOT** | Menu, volantini, QR per ristorante |
| **Wannabe** | Asset UI da testare, post social |
| **Lawrenzo** | Impaginazione documenti legali |
| **Machiavelli** | Rebranding, pitch deck |

Bus: `python3 .../bus-send.py send designbro <target> "<msg>" design`
