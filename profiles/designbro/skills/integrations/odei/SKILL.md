---
name: odei
description: "ODEI platform integration — agent builder handoff pairing, MCP server, API patterns"
tags: [odei, agent-builder, handoff, pairing, mcp, integration]
version: 1.0
---

# ODEI Integration

## Quando usare
- Pairing Claude Code (o altri operator) con ODEI Agent Builder
- Bootstrap e lifecycle di agenti ODEI
- Debug handoff errors e state machine

## Handoff API

### Endpoint
```
POST https://app.odei.ai/auth/agent-builder/handoff
Content-Type: application/json
```

**Nessun bearer token richiesto.** Non aggiungere Authorization headers.

### Azioni principali

| Action | Quando | Stato risultante |
|--------|--------|-----------------|
| `mark_setup_running` | Primo callback dopo pairing code | `setup_running` |

**ATTENZIONE**: `mark_setup_running` è l'UNICA action che funziona via REST API. Tutte le altre (`connect`, `request_machine_stage`, `mark_connected`, `report_machine`, `complete_setup`, etc.) restituiscono `invalid_agent_builder_action`. I passi successivi sono gestiti dall'app desktop ODEI locale.

### State Machine
```
issued → setup_running → [ODEI desktop app drives the rest]
```

### Dopo il pairing
Lo stato resta `setup_running`. Il nextAction dice `request_machine_stage` ma non è eseguibile via API. L'app desktop ODEI completa i restanti step (machine, install, runtime, launch) automaticamente.

### Request body (standard)
```json
{
  "action": "<action>",
  "pairingCode": "ODEI-CLAUDE-XXXX-XXXX-XXXX",
  "runId": "ab_xxxxx"
}
```

### Response: successo
```json
{
  "ok": true,
  "handoff": {
    "state": "setup_running",
    "nextAction": "...",
    "status": "..."
  },
  "operator": { ... },
  "agentBuilder": { ... }
}
```

## Errori comuni e fix

### `agent_builder_handoff_superseded`
**Causa**: Il runId usato è stato sostituito da uno più recente.
**Fix**: dalla response leggi `handoff.expectedRunId` e riprova con quello:
```json
{"action":"<azione>","pairingCode":"...","runId":"ab_<expectedRunId>"}
```

### `invalid_agent_builder_action`
**Causa**: L'action non è valida per lo stato corrente del handoff. In pratica, qualsiasi action diversa da `mark_setup_running` restituisce questo errore via REST API.
**Fix**: l'unica action REST è `mark_setup_running`. I passi successivi richiedono l'app desktop ODEI. Se `nextAction` dice `run_supported_handoff_action`, non c'è un'action REST da fare — aspetta l'app.

### `already_connected`
**Info**: Il pairing era già stato accettato. Nessuna azione aggiuntiva necessaria.

## Helper Script (ODEI repo)
```bash
# Dopo aver clonato ODEI:
node scripts/agent-builder-handoff.mjs connect <pairingCode> --endpoint "https://app.odei.ai/auth/agent-builder/handoff"
```
Lo script NON è nel repo kanban workspace — va clonato dal repo principale ODEI.

## ODEI sul VPS

### MCP Server
- Path: `/opt/odei-mcp`
- Package: `@anthropic/odei-mcp` (dist/index.js)

### ODEI App (kanban workspace)
- Path: `<HERMES_ROOT>/kanban/boards/odei/workspaces/t_fbf71eed/odei-app/`
- Scripts utili: `scripts/check-app-subdomain-contract.mjs`, `scripts/build-api-site-slice.mjs`
- NOTA: il handoff script (`agent-builder-handoff.mjs`) NON è in questo workspace

## Pairing Flow (step by step)

1. Vai su `app.odei.ai` → Agent Builder → genera pairing code
2. Ricevi: pairing code + runId + expiry (scade ~12h)
3. Chiama `mark_setup_running` con pairing code + runId
4. Se `agent_builder_handoff_superseded` → chiedi nuovo pairing code all'utente (l'expectedRunId non risolve il problema se il pairing code stesso è stale)
5. Se `already_connected` → pairing già accettato, nessuna azione necessaria
6. Dopo pairing, ODEI mostra stato `setup_running` — l'app desktop completa il resto
7. **Non cercare di fare altri step via API** — non funzionano

## ODEI Rewards

I reward ODEI richiedono il **login via wallet** (MetaMask su Base). Non è possibile fare claim via API.
- Utente deve andare su `app.odei.ai/rewards` → connettere wallet Base con $ODAI
- Il wallet è il provider primario (non email/password)
- [REDACTED — dati personali rimossi] ha ~20M $ODAI su wallet `0xFd2A1cFb95e42DA0197F756adA263bEd9E6951e1`

## Pitfall: Pairing codes scadono
Controlla `handoffExpiresAt` nella response. Se scaduto, genera un nuovo codice da ODEI dashboard.

## DAOrg Governance

### Cos'è
DAOrg è la governance decentralizzata di ODEI. Wallet-linked identity su Base, weighted signaling, motion lifecycle on-chain (in futuro).

### Governance Lobby
- URL: `daorg.odei.ai` (o link "REWARDS Receipts" / "Governance" da app.odei.ai)
- Richiede wallet Base con $ODAI per accedere
- Signal weight = balance $ODAI

### Motion Templates
Quando crei una motion, il Motion Studio offre 4 template:
1. **Ratify Surface** — Conferma una baseline di governance o prodotto
2. **Ship Product Change** — Approva un percorso di build con artifact
3. **Reward Operator Work** — Sposta una contribuzione in una decisione di reward
4. **Governance Policy** — Imposta una regola duratura per DAOrg

### Motion Lifecycle
```
Draft → Discussion → Signal → Decide → Execute
```
- Draft: locale, modificabile, non-blocking
- Discussion: aperta ai holder
- Signal: voting con signal weight (For/Against/Abstain)
- Decide: chiusura window + verdict
- Execute: receipt + proof

### Come creare una motion
1. Vai su Motion Studio → scegli template
2. Compila: Title, Question, Summary, Execution Path
3. Draft si salva localmente (bound al wallet)
4. Quando pronto → "Move to signaling" per aprire il voto
5. Quorum: 3 wallet. Window tipicamente ~7 giorni.

### Per scrivere buone motion
- Study the project first (GitHub, docs, on-chain data, community)
- Summary: COMPATTO. 2-3 frasi max. Non ripetere il title.
- Execution Path: step numerati, ognuno con deliverable verificabile
- Proof: cosa dimostra che il lavoro è stato fatto (contract addresses, URLs, receipts)
- Template "Governance Policy" per regole durature
- Template "Reward Operator Work" per reward specifici

### Stato attuale (giugno 2026)
- ~6 wallet attivi in governance
- $2,447 ETH distribuiti (3 batch, 22 wallet)
- Nessun governance contract on-chain (tutto off-chain)
- $ODAI token: `0x0086cFF0c1E5D17b19F5bCd4c8840a5B4251D959` su Base
- Reward pagati manualmente, non verificabili on-chain

## Project Status (June 2026)

ODEI is **very early stage** — founder singolo (@zer0h1ro, Budapest), v0.02 local app, v0.1 DAOrg preview.

- **GitHub**: 12 repo pubblici, tutti showcase vuoti (1 commit each: "Initial public showcase"), 0 stars, 0 forks
- **Twitter @odei_ai**: 2.8K follower, 0 post pubblicati
- **Community**: Zero — no Discord, no Telegram, no Reddit, no Product Hunt, no media coverage
- **Production gates**: 5/9 pass, 3 staged, 1 blocked
- **Features non ancora rilasciate**: "FOR AGENTS" tab (SOON), "TALK WITH ODEI" (SOON)
- **Public code**: Nessuno. Tutti i repo sono documentazione-only. Il codice reale è privato.

### $ODAI Token

- **Contract**: `0x0086cFF0c1E5D17b19F5bCd4c8840a5B4251D959` su Base
- **Supply**: 100B token, ~95B circolanti
- **Price**: ~$0.000019, mcap ~$1.83M
- **Liquidity**: ~$257K (pool principale ODAI/flETH su Uniswap v4)
- **Volume 24h**: ~$43K
- **Reward distribuiti**: $2,447 in ETH (3 batch, 22 wallet) — meccanismo non verificabile on-chain
- **Governance contracts**: NESSUNO deployato on-chain. Tutto off-chain e centralizzato.
- **Agent Passport NFT**: NESSUNO trovato on-chain. Probabilmente non ancora deployato.

### Implicazioni per motion/strategy

- Il progetto ha un'ottima narrativa ("Personal AI OS") ma execution ancora tutta da dimostrare
- Community quasi inesistente — qualsiasi contributo attivo ha peso enorme
- Reward contracts e governance on-chain sono il gap più evidente
- Essere top holder con ~20M ODAI dà voce significativa nelle motion

## On-Chain Reference
Vedi `references/odei-onchain.md` per dettagli su token, liquidity, contract.
