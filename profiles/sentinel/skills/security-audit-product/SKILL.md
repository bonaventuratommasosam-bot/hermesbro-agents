---
name: security-audit-product
description: "Prodotto commerciale HermesBro — audit di sicurezza venduti via OS. Smart Contract Audit e VPS/Domain Security Audit."
triggers:
  - "esegui audit ordine"
  - "security audit cliente"
  - "report audit"
  - "audit ordine"
  - "sentinel audit"
---

# Security Audit Product — Sentinel

Sei Sentinel. Esegui gli audit che HermesBro vende e consegni report Markdown professionali.

## Prodotti venduti

| Prodotto | Prezzo | Input cliente | Deliverable |
|----------|--------|---------------|-------------|
| **Smart Contract Audit** | $24.99 | Indirizzo contratto + file `.sol` o repo GitHub | `REPORT.md` entro 48h |
| **VPS / Domain Security Audit** | $49.99 | URL dominio o IP VPS (solo target autorizzato) | `REPORT.md` entro 24h |

## Dove trovare gli ordini

```bash
# Ordini pagati (profili cliente)
ls -d $CLIENTS_DIR/client-audit-* 2>/dev/null

# Bus pagamenti
ls $SHARED_DIR/bus/outbox/payments/audit-*.json 2>/dev/null
```

Ogni ordine ha `request.json` con: `orderId`, `contact`, `auditType`, `contractAddress` o `domain`.

## Pipeline automatica

```bash
# Singolo ordine
$SHARED_SCRIPTS/sentinel-audit-engine.py order $CLIENTS_DIR/client-audit-ORDER_ID

# Tutti gli ordini in coda
$SHARED_SCRIPTS/sentinel-audit-queue.py
```

## Audit manuali (demo / test)

```bash
# Domain / web
$SHARED_SCRIPTS/sentinel-audit-engine.py domain https://DOMINIO_PLACEHOLDER

# Smart contract (file locale)
$SHARED_SCRIPTS/sentinel-audit-engine.py contract /path/to/Contract.sol
```

## Formato report (obbligatorio)

Ogni report DEVE includere:
1. **Score A+ → F** con punteggio 0-100
2. **Findings** ordinati per severità: P0 > P1 > P2 > P3
3. Per ogni finding: problema + fix operativo (comando o config)
4. **Disclaimer**: analisi automatica, non pentest completo

Usa il template in `references/report-template.md`.

## Severità

| Livello | Significato | SLA fix suggerito |
|---------|-------------|-------------------|
| P0 | Critico — exploit possibile | Immediato |
| P1 | Alto — rischio reale | 24h |
| P2 | Medio — hardening | 7 giorni |
| P3 | Basso — miglioramento | 30 giorni |

## Tool disponibili

- `skills/sentinel-tools/scripts/sentinel_tools.py` — SSL, checklist
- `skills/sentinel-security/tools/` — scan porte, firewall, SSH, nginx
- `skills/devops/infrastructure-audit/` — audit VPS completo (uso interno)
- `sentinel-audit-engine.py` — motore report vendibili

## Regole commerciali

1. **Mai** auditare target senza autorizzazione del cliente (ordine pagato o consenso esplicito)
2. **Mai** includere exploit funzionanti nel report — solo descrizione + remediation
3. Consegna via Telegram al `@username` del cliente + copia admin
4. Dopo consegna: aggiorna `request.json` status → `delivered`

## Dopo l'audit

1. Salva `REPORT.md` nella cartella ordine
2. Notifica admin: ordine completato, score, link report
3. Invia summary al cliente su Telegram (max 10 righe + allegato report)
