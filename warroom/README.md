# War Room — Multi-Agent Brainstorming

**Template avviabile di brainstorming multi-agente.** 8 agenti specializzati discutono il tuo progetto, problema o idea in tempo reale via WebSocket.

## Workflow

1. Scegli 2-8 agenti e un argomento
2. La War Room avvia un brainstorming strutturato in fasi
3. Ogni agente risponde agli altri creando un dibattito reale
4. Alla fine genera un report strutturato con azioni concrete

## 7 Workflow Inclusi

| Workflow | Descrizione |
|----------|-------------|
| **Libero** | Discussione aperta round-robin con moderatore |
| **Nuovo Progetto** | Esplorazione → Rischi e Costi → Marketing → Piano d'Azione |
| **Risolvi un Problema** | Diagnosi → Soluzioni → Stress Test → Decisione |
| **Lancio Prodotto** | Validazione → Branding → Go-to-Market → Checklist |
| **Review** | KPI → Problemi → Priorità → Action Items |
| **Deep Dive** | Analisi → Contro-Analisi → Votazione → Report |
| **Emergenza** | Situazione → Piano d'Emergenza (risposta rapida) |

## Agenti

| Agente | Ruolo |
|--------|-------|
| **HermesRibbitBot** | Moderatore |
| **GROOT** | Ristorazione e Food Business |
| **ContAIbile** | Finanza e Contabilità |
| **LAWrenzo** | Legale |
| **Wannabe** | Social Media Marketing |
| **DesignBro** | Design e Branding |
| **DUCATO** | Trading AI |
| **El Froggo** | DeFi e Base Chain |

## Setup Rapido

```bash
# 1. Clona
git clone https://github.com/bonaventuratommasosam-bot/hermesbro-agents.git
cd hermesbro-agents/warroom

# 2. Crea ambiente
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn httpx

# 3. Configura il tuo LLM
cp .env.example .env
# Modifica OPENGATEWAY_URL e OPENGATEWAY_KEY

# 4. Avvia
./run.sh
```

Apri `http://localhost:8097` nel browser.

## Configurazione

Copia `.env.example` in `.env` e imposta:

- `OPENGATEWAY_URL` — endpoint LLM compatibile OpenAI API
- `OPENGATEWAY_KEY` — API key
- `MODEL` — modello (default: `mimo-v2.5-pro`)

## API

| Endpoint | Descrizione |
|----------|-------------|
| `GET /` | Interfaccia web |
| `WS /ws/{session_id}` | WebSocket in tempo reale |
| `GET /api/agents` | Lista agenti disponibili |
| `GET /api/workflows` | Lista workflow |
| `GET /api/sessions` | Sessioni attive |
| `GET /api/sessions/{id}/result` | Risultato sessione JSON |

## Licenza

MIT — vedi [LICENSE](../LICENSE).
