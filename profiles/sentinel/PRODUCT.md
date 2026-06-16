# Sentinel — Prodotto Security Audit

## Posizionamento

Sentinel è l'agente **Security Auditor** di HermesBro. Vende audit gestiti (non self-service istantaneo): il cliente paga, invia il target, riceve report Markdown entro SLA.

## Offerta commerciale

### 1. Smart Contract Audit — $24.99
- **Per:** team DeFi, NFT, token launch su Base/Ethereum
- **Cosa riceve:** report Markdown con score, findings Slither + pattern statici, raccomandazioni fix
- **SLA:** 48h dalla ricezione sorgente Solidity
- **Canale vendita:** hermesbro.cloud/os → Sentinel page → Stripe

### 2. VPS / Domain Security Audit — $49.99
- **Per:** startup, PMI, founder con VPS o sito web
- **Cosa riceve:** SSL, security headers, esposizione HTTP, score complessivo
- **SLA:** 24h dalla ricezione URL autorizzato
- **Nota:** non include penetration test invasivo — assessment esterno + checklist

## Flusso operativo

```
Cliente paga (Stripe/Base)
    → deployAudit() crea client-audit-{id}/
    → ONBOARDING.txt + request.json
    → Cliente invia .sol o URL su Telegram
    → sentinel-audit-queue.py processa
    → REPORT.md generato
    → Consegna Telegram + email
```

## Attivazione Sentinel (demo → live)

```bash
$SHARED_SCRIPTS/activate-demo-bot.sh sentinel <TOKEN>
```

Poi esegui audit con la skill `security-audit-product`.

## Metriche da tracciare

- Ordini in coda vs completati
- Score medio per tipo audit
- Tempo medio consegna (target < SLA)
- Repeat customers
