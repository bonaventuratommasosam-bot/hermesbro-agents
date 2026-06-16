# Sentinel — Security Auditor

**Il security auditor di HermesBro.** Sentinel vende audit gestiti su smart contract (Solidity) e VPS/domain tramite report Markdown con SLA.

- **Goal:** Security audit vendibili — smart contract (via Slither) + VPS/domain (SSL, headers, score).
- **Motto:** *«Zero trust. Always verify.»*
- **Emoji:** 🛡️

## Prodotti

| SKU | Prezzo | SLA | Output |
|---|---|---|---|
| **Smart Contract Audit** | $24.99 | 48h | Report Markdown + findings (score, pattern statici, raccomandazioni fix) |
| **VPS/Domain Security Audit** | $49.99 | 24h | Score A–F + remediation (SSL, security headers, esposizione HTTP) |

**Target:** team DeFi, startup, PMI, founder con VPS o sito web.

## Cosa fa

| Funzionalità | Descrizione |
|---|---|
| **SSL Check** | Analisi certificato SSL/TLS per dominio |
| **Security Checklist** | Checklist VPS completa (headers, porte, esposizione) |
| **Backup Audit** | Verifica stato backup e procedure |
| **Smart Contract Analysis** | Slither + pattern statici su sorgente Solidity |
| **Report generation** | Report Markdown strutturato con score, findings, remediation |
| **Coda ordini** | Gestione ordini in coda con processing ogni 15 min |

**Non fa:** penetration test invasivo, audit senza autorizzazione esplicita del cliente.

## Requisiti

- **Hermes Agent** — runtime per eseguire il profilo agente
- **Telegram Bot Token** — creato via @BotFather
- **LLM API Key** — provider LLM configurato nel `.env`
- **Slither** — per analisi smart contract (`pip install slither-analyzer`)
- **Python 3.11+** — per tool CLI (ssl_check, security_checklist, backup_audit)

## Setup rapido

### 1. Crea il bot Telegram

```bash
# @BotFather → crea bot → salva token
```

### 2. Configura il profilo

```bash
# Crea profilo in ~/.hermes/profiles/sentinel/
echo "TELEGRAM_BOT_TOKEN=*** >> .env
echo "OPENAI_API_KEY=*** >> .env
```

### 3. Compila `audit-config.yaml`

```yaml
client:
  name: "Nome Cliente"
  default_domain: "esempio.com"
audit:
  smart_contract_sla_hours: 48
  vps_audit_sla_hours: 24
  min_score_alert: 60
telegram:
  group_chat_id: "CHAT_ID_GRUPPO"
  admin_chat_id: "CHAT_ID_ADMIN"
roles:
  admin:
  - "ADMIN_CHAT_ID"
```

### 4. Avvia

```bash
hermes start --profile sentinel
```

### 5. Test rapido

- `setup` → wizard configurazione
- `ssl esempio.com` → check SSL/TLS
- `checklist vps` → security checklist VPS
- `backup` → audit procedure backup

## Esempi d'uso

| Input chat | Cosa fa |
|---|---|
| `setup` | Wizard configurazione iniziale |
| `ssl esempio.com` | Analisi certificato SSL, scadenza, chain |
| `checklist vps` | Checklist sicurezza VPS completa |
| `backup` | Audit configurazione backup |
| `nuovo audit sc 0x...` | Crea nuovo smart contract audit in coda |

## Flusso operativo audit

```
Cliente paga (Stripe/Base)
    → deployAudit() crea client-audit-{id}/
    → ONBOARDING.txt + request.json
    → Cliente invia .sol o URL su Telegram
    → sentinel-audit-queue.py processa
    → REPORT.md generato
    → Consegna Telegram + email
```

## Configurazione

| Campo | Descrizione |
|---|---|
| `audit.smart_contract_sla_hours` | SLA audit smart contract (48h) |
| `audit.vps_audit_sla_hours` | SLA audit VPS (24h) |
| `audit.min_score_alert` | Score minimo per alert (60) |
| `cron.queue_process` | Processa coda ogni 15 min |

## Metriche da tracciare

- Ordini in coda vs completati
- Score medio per tipo audit
- Tempo medio consegna (target < SLA)
- Clienti ricorrenti

## Integrazione flotta HermesBro

| Agente | Interazione |
|---|---|
| **Machiavelli** | Dispatch audit in workflow multi-agente |
| **Lawrenzo** | Alert rischi ALTI legati a security |

Engine: `$SHARED_SCRIPTS/sentinel-audit-engine.py`
