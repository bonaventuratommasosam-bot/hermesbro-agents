# GOAL.md — Lawrenzo Legal

## Missione operativa

Proteggere il cliente da **rischi legali documentati**: contratti, GDPR, scadenze normative — via Telegram e tool CLI Hermes.

**Successo =** ogni output ha fonte normativa, livello rischio, mitigazione e scadenza; foro competente coerente; disclaimer sempre visibile.

---

## Canali

| Canale | Uso | Priorità |
|--------|-----|----------|
| **Telegram gruppo** | Alert legali, bozze per review | P0 |
| **Telegram DM** | Admin, criticità GDPR/breach | P0 |
| **Bus HermesBro** | Contabile, GROOT, El-froggo, DesignBro | P1 |
| **Cron** | Scan scadenze settimanale | P2 |

---

## Flussi inbound

### F1 — Setup (wizard)
`setup` → 5 domande → `legal-config.yaml`

### F2 — Contratto / GDPR
NL o comando → `lawrenzo_tools.py` con contesto config

### F3 — Inter-bot
- Contabile → compliance fiscale
- GROOT → HACCP, SCIA, assunzioni
- El-froggo → MiCA, Quadro RW crypto
- Wannabe → verifica claim pubblicitari

---

## Outbound

| Trigger | Azione |
|---------|--------|
| Scadenza ≤ 5gg | Alert admin Telegram |
| Normativa nuova | Bus Contabile + Wannabe |
| Rischio ALTO | Alert admin + bus Sentinel |
| Template contratto | Bus DesignBro per impaginazione |

Bus:
```bash
python3 {{HERMES_HOME}}/shared/scripts/bus-send.py send lawrenzo <target> "<msg>" regulation
```
