---
name: web-search
description: Cercare informazioni su internet in tempo reale. Utile per notizie crypto, prezzi, documentazione, news generali.
emoji: 🌐
tags: [web, search, internet, crypto, news]
visibility: public
---
# Web Search Skill

## Purpose
Cercare informazioni su internet in tempo reale. Utile per notizie crypto, prezzi, documentazione, news generali.

## When to activate
- [REDACTED — dati personali rimossi] chiede "cerca", "trova", "googla", "cercami"
- [REDACTED — dati personali rimossi] vuole notizie su crypto, token, progetti
- [REDACTED — dati personali rimossi] chiede informazioni aggiornate che non sono nella memoria
- [REDACTED — dati personali rimossi] dice "cosa sta succedendo con...", "dimmi di più su..."
- [REDACTED — dati personali rimossi] chiede prezzi, quotazioni, documentazione tecnica

## How to invoke

```bash
python3 /home/[REDACTED — dati personali rimossi]/ai-stack/scripts/web_search.py "QUERY DI RICERCA"
```

### Opzioni
| Flag | Cosa fa |
|------|---------|
| `--num N` | Numero di risultati (default: 5, max: 10) |
| `--json` | Output in formato JSON (per parsing programmatico) |

### Esempi
```bash
# Ricerca base
python3 /home/[REDACTED — dati personali rimossi]/ai-stack/scripts/web_search.py "Bitcoin price today"

# 10 risultati
python3 /home/[REDACTED — dati personali rimossi]/ai-stack/scripts/web_search.py "Base chain new tokens" --num 10

# Output JSON per processare
python3 /home/[REDACTED — dati personali rimossi]/ai-stack/scripts/web_search.py "Ethereum news" --json
```

## Workflow

1. [REDACTED — dati personali rimossi] fa una domanda che richiede info aggiornate
2. Formula una query di ricerca efficace (inglese funziona meglio)
3. Esegui `web_search.py` con la query
4. Leggi i risultati e riassumili in italiano per [REDACTED — dati personali rimossi]
5. Se servono più dettagli, fai una seconda ricerca più mirata

## Come formulare buone query

- Per prezzi crypto: `"TOKEN price today"` o `"TOKEN price USD"`
- Per notizie: `"TOKEN news"` o `"crypto news today"`
- Per documentazione: `"library_name documentation"` o `"how to use library_name"`
- Per sicurezza/token scam: `"TOKEN contract address scam"` o `"TOKEN rugpull"`

## Installazione dipendenze

Se `duckduckgo_search` non è installato:
```bash
pip install duckduckgo_search
```

## Safety
- Non cercare mai contenuti illegali o dannosi
- Non fidarti ciecamente dei risultati — verifica sempre le informazioni importanti
- Non cliccare link sospetti nei risultati
- Se [REDACTED — dati personali rimossi] chiede info su un token, cerca anche "scam" o "rugpull" per sicurezza