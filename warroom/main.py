"""
HermesBro War Room — Multi-agent brainstorming in real-time.
LLM-to-LLM orchestration via OpenGateway. WebSocket for live UI + user intervention.
HermesRibbitBot moderates the discussion.

v2: 6 workflow templates with auto-trigger + manual selection.
"""
import asyncio
import gzip
import json
import os
import re
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="HermesBro War Room v2")

# ── Shared HTTP client (reuse TLS connections) ──
http_client = httpx.AsyncClient(timeout=90.0)

# ── Config ──
OPENGATEWAY_URL = os.getenv("OPENGATEWAY_URL", "http://localhost:8080/v1/chat/completions")
OPENGATEWAY_KEY = os.getenv("OPENGATEWAY_KEY", "")
MODEL = os.getenv("MODEL", "gpt-4o")

# ── Agent Profiles ──
AGENT_PROFILES = {
    "HermesRibbitBot": {
        "name": "HermesRibbitBot",
        "role": "Moderatore",
        "color": "#00f0ff",
        "system": (
            "Sei HermesRibbitBot, il moderatore del brainstorming. "
            "Il tuo ruolo e' facilitare il DIBATTITO TRA GLI AGENTI — non lasciarli parlare nel vuoto. "
            "Se un agente non risponde direttamente a quello che ha detto un altro, sottolinealo e "
            "chiedigli: 'Cosa ne pensi di quello che ha detto X?' o 'Concordi con questa proposta?' "
            "Rispondi in italiano. Sii conciso (max 100 parole). "
            "Se la discussione stagna, proponi un nuovo angolo. "
            "Se un'idea e' interessante, chiedi a un ALTRO agente di reagire."
        ),
    },
    "GROOT": {
        "name": "GROOT",
        "role": "Ristorazione",
        "color": "#f59e0b",
        "system": (
            "Sei GROOT, esperto di ristorazione e food business. "
            "Rispondi in italiano, sii pratico e concreto. "
            "Parla di food cost, menu engineering, scorte, gestione sala, marketing ristoranti. "
            "Quando fai brainstorming, proponi idee actionable con numeri quando possibile. "
            "RISPONDI DIRETTAMENTE a quello che ha appena detto il collega: concordi? Dissenti? "
            "Costruisci sulle sue idee o proponi un angolo alternativo. Non ripetere concetti gia' espressi. "
            "Sii conciso (max 150 parole). Parla come in una conversazione reale, non come un report."
        ),
    },
    "ContAIbile": {
        "name": "ContAIbile",
        "role": "Finanza",
        "color": "#10B981",
        "system": (
            "Sei ContAIbile, esperto di contabilita', finanza e crypto per PMI e freelance. "
            "Rispondi in italiano, sii analitico e orientato ai numeri. "
            "Parla di fatturazione, bilancio, IVA, investimenti, crypto, tax planning. "
            "Quando fai brainstorming, porta dati concreti e pro/contro finanziari. "
            "RISPONDI DIRETTAMENTE a quello che ha appena detto il collega: i numeri tornano? "
            "Mancano costi? Concordi con l'approccio? Aggiungi la tua prospettiva numerica. "
            "Sii conciso (max 150 parole). Parla come in una conversazione reale, non come un report."
        ),
    },
    "LAWrenzo": {
        "name": "LAWrenzo",
        "role": "Legale",
        "color": "#6366F1",
        "system": (
            "Sei LAWrenzo, esperto legale per aziende e startup. "
            "Rispondi in italiano, sii preciso ma accessibile. "
            "Parla di contratti, compliance, GDPR, proprieta' intellettuale, societario. "
            "Quando fai brainstorming, identifica rischi legali e opportunita' normative. "
            "RISPONDI DIRETTAMENTE a quello che ha appena detto il collega: e' fattibile legalmente? "
            "Vedi rischi che non ha considerato? Aggiungi il tuo vincolo o conferma. "
            "Sii conciso (max 150 parole). Parla come in una conversazione reale, non come un report."
        ),
    },
    "Wannabe": {
        "name": "Wannabe",
        "role": "Social Media",
        "color": "#8B5CF6",
        "system": (
            "Sei Wannabe, esperto di social media marketing e content strategy. "
            "Rispondi in italiano, sii creativo e orientato alla crescita. "
            "Parla di social media, SEO, content marketing, community, brand building. "
            "Quando fai brainstorming, proponi campagne, hook, contenuti virali. "
            "RISPONDI DIRETTAMENTE a quello che ha appena detto il collega: l'idea e' marketabile? "
            "Come la fai virale? Aggiungi twist creativi alle proposte precedenti. "
            "Sii conciso (max 150 parole). Parla come in una conversazione reale, non come un report."
        ),
    },
    "DesignBro": {
        "name": "DesignBro",
        "role": "Design",
        "color": "#EC4899",
        "system": (
            "Sei DesignBro, esperto di design grafico e branding. "
            "Rispondi in italiano, sii visivo nelle descrizioni. "
            "Parla di brand identity, UI/UX, social assets, packaging, visual storytelling. "
            "Quando fai brainstorming, descrivi concept visivi e direzioni creative. "
            "RISPONDI DIRETTAMENTE a quello che ha appena detto il collega: come lo traduci in design? "
            "L'estetica funziona? Aggiungi la tua visione visiva. "
            "Sii conciso (max 150 parole). Parla come in una conversazione reale, non come un report."
        ),
    },
    "DUCATO": {
        "name": "DUCATO",
        "role": "Trading AI",
        "color": "#d4a853",
        "system": (
            "Sei DUCATO, esperto di trading AI e strategie finanziarie. "
            "Rispondi in italiano, sii analitico e basato su dati. "
            "Parla di strategie DCA, TWAP, Grid, analisi on-chain, gestione portafoglio. "
            "Quando fai brainstorming, porta numeri e scenari concreti. "
            "RISPONDI DIRETTAMENTE a quello che ha appena detto il collega: i numeri reggono? "
            "C'e un rischio finanziario sottovalutato? Aggiungi la tua analisi. "
            "Sii conciso (max 150 parole). Parla come in una conversazione reale, non come un report."
        ),
    },
    "El Froggo": {
        "name": "El Froggo",
        "role": "DeFi",
        "color": "#22d3ee",
        "system": (
            "Sei El Froggo, esperto di DeFi e trading su Base chain. "
            "Rispondi in italiano, sii pratico e orientato al profitto. "
            "Parla di DEX, yield farming, liquidity pool, whale tracking, gas optimization. "
            "Quando fai brainstorming, proponi opportunita' concrete con rischio/rendimento. "
            "RISPONDI DIRETTAMENTE a quello che ha appena detto il collega: l'approccio DeFi funziona? "
            "Cosa cambieresti? Aggiungi la tua prospettiva on-chain. "
            "Sii conciso (max 150 parole). Parla come in una conversazione reale, non come un report."
        ),
    },
}

# ── Workflow Templates ──
WORKFLOWS = {
    "free": {
        "id": "free",
        "name": "Brainstorming Libero",
        "icon": "free",
        "description": "Discussione aperta, round-robin classico con moderatore.",
        "triggers": [],
        "phases": [
            {
                "name": "Discussione libera",
                "agents": "selected",  # usa quelli scelti dall'utente
                "rounds_per_agent": 2,
                "prompt_suffix": "",
                "tone": None,
            }
        ],
        "post_process": "summary",
    },
    "new_project": {
        "id": "new_project",
        "name": "Nuovo Progetto",
        "icon": "project",
        "description": "Analisi completa di una nuova idea: esplorazione, rischi, opportunità, piano d'azione.",
        "triggers": [
            r"(?i)(nuovo\s+progett|nuova\s+idea|ho\s+un.idea|vorrei\s+creare|vorrei\s+fare|startup|lanci)",
        ],
        "phases": [
            {
                "name": "Esplorazione",
                "agents": "all",
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Analizza questa idea dal tuo punto di vista di esperto. "
                    "Cosa vedi di buono? Cosa manca? Quali primi suggerimenti?"
                ),
                "tone": "esplorativo, aperto, curioso",
            },
            {
                "name": "Rischi e Costi",
                "agents": ["ContAIbile", "LAWrenzo"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Ora concentrati SU RISCHI e COSTI NASCOSTI. "
                    "Cosa potrebbe andare storto? Quali vincoli legali/budgettici? "
                    "Sii diretto e critico."
                ),
                "tone": "critico, analitico",
            },
            {
                "name": "Opportunità e Marketing",
                "agents": ["Wannabe", "DesignBro"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Ora concentrati su OPPORTUNITA' e ANGOLI CREATIVI. "
                    "Come posizionarlo? Come renderlo attraente? "
                    "Proponi nome, palette, canali, hook."
                ),
                "tone": "creativo, entusiasta",
            },
            {
                "name": "Piano d'Azione",
                "agents": ["HermesRibbitBot"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Sei il facilitatore. Sintetizza tutto in un PIANO D'AZIONE concreto:\n"
                    "1. Le 3 idee chiave emerse\n"
                    "2. Primi 3 passi da fare questa settimana\n"
                    "3. Budget stimato iniziale\n"
                    "4. Rischio principale da mitigare\n"
                    "5. Timeline realistica (MVP in X settimane)\n"
                    "Sii concreto e actionable."
                ),
                "tone": "strutturato, operativo",
            },
        ],
        "post_process": "action_plan",
    },
    "problem": {
        "id": "problem",
        "name": "Risolvi un Problema",
        "icon": "problem",
        "description": "Diagnosi, soluzioni, stress-test e decisione finale.",
        "triggers": [
            r"(?i)(problema|come\s+risolv|bug|errore|non\s+funziona|crisi|emergenz|bloccat)",
        ],
        "phases": [
            {
                "name": "Diagnosi",
                "agents": "all",
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Diagnostica questo problema dal tuo punto di vista. "
                    "Qual e' la causa piu' probabile? Cosa non stiamo vedendo?"
                ),
                "tone": "analitico, diagnostico",
            },
            {
                "name": "Soluzioni",
                "agents": "all",
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Proponi 1-2 soluzioni concrete per il problema. "
                    "Ogni soluzione deve avere: costo stimato, tempo, rischio residuo."
                ),
                "tone": "propositivo, concreto",
            },
            {
                "name": "Stress Test",
                "agents": ["HermesRibbitBot"],
                "rounds_per_agent": 2,
                "prompt_suffix": (
                    "Sei l'avvocato del diavolo. Prendi le soluzioni proposte e smontale: "
                    "cosa potrebbe fallire? In quali condizioni? "
                    "Poi chiedi agli agenti di difendere le loro proposte."
                ),
                "tone": "sfidante, critico",
            },
            {
                "name": "Decisione Finale",
                "agents": ["HermesRibbitBot"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Classifica le soluzioni per:\n"
                    "1. Fattibilita' (1-10)\n"
                    "2. Costo (basso/medio/alto)\n"
                    "3. Impatto (1-10)\n"
                    "4. Tempo di implementazione\n"
                    "Dai la raccomandazione finale con piano d'azione."
                ),
                "tone": "decisivo, strutturato",
            },
        ],
        "post_process": "decision",
    },
    "launch": {
        "id": "launch",
        "name": "Lancio Prodotto",
        "icon": "launch",
        "description": "Validazione, branding, strategia go-to-market e checklist operativa.",
        "triggers": [
            r"(?i)(lancio|lanciamo|lanciare|go.to.market|prodotto\s+nuov|mvp|presa\s+vision)",
        ],
        "phases": [
            {
                "name": "Validazione",
                "agents": ["ContAIbile", "LAWrenzo"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Analizza la validita' di questo lancio: "
                    "dimensione mercato stimata, compliance necessaria, "
                    "struttura societaria consigliata, costi di avvio."
                ),
                "tone": "analitico, numerico",
            },
            {
                "name": "Branding",
                "agents": ["DesignBro", "Wannabe"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Crea il concept di brand per questo lancio: "
                    "nome (3 opzioni), palette colori, tone of voice, "
                    "canali social prioritari, hook per il lancio."
                ),
                "tone": "creativo, visionario",
            },
            {
                "name": "Strategia Go-to-Market",
                "agents": ["Wannabe", "GROOT"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Definisci la strategia di lancio: "
                    "pricing suggerito, canali di acquisizione, "
                    "content plan prima/durante/dopo il lancio, "
                    "metriche di successo."
                ),
                "tone": "strategico, orientato all'azione",
            },
            {
                "name": "Checklist Operativa",
                "agents": ["HermesRibbitBot"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Genera la CHECKLIST OPERATIVA ordinata per settimana:\n"
                    "Settimana 1: ...\nSettimana 2: ...\nSettimana 3: ...\nSettimana 4: ...\n"
                    "Per ogni task: chi lo fa, durata stimata, dipendenze.\n"
                    "Includi metriche da tracciare ad ogni milestone."
                ),
                "tone": "operativo, strutturato",
            },
        ],
        "post_process": "checklist",
    },
    "review": {
        "id": "review",
        "name": "Review Periodica",
        "icon": "review",
        "description": "KPI check, problemi aperti, priorità settimanali, action items.",
        "triggers": [
            r"(?i)(review\s+periodic|check\s+settimanale|kpi|metriche|stato\s+attuale|dove\s+siamo)",
        ],
        "phases": [
            {
                "name": "KPI Check",
                "agents": "all",
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Riporta le metriche chiave del tuo dominio. "
                    "Cosa sta andando bene? Cosa no? Numeri concreti se possibile."
                ),
                "tone": "reportistico, basato su dati",
            },
            {
                "name": "Problemi Aperti",
                "agents": "all",
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Quali sono i top 3 problemi aperti nel tuo ambito? "
                    "Per ogni problema: impatto (alto/medio/basso), urgenza, risorse per risolverlo."
                ),
                "tone": "diagnostico, prioritario",
            },
            {
                "name": "Priorità Settimana",
                "agents": ["HermesRibbitBot", "ContAIbile"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Dai problemi emersi, seleziona le TOP 3 priorita' per questa settimana. "
                    "Per ognuna: obiettivo specifico, chi se ne occupa, metrica di successo."
                ),
                "tone": "decisivo, focalizzato",
            },
            {
                "name": "Action Items",
                "agents": ["HermesRibbitBot"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Genera la ACTION ITEMS LIST:\n"
                    "- [Agente] Task specifico | Deadline | Priorita'\n"
                    "Ordina per priorita' decrescente. Max 10 items.\n"
                    "Formato: lista puntata con checkbox."
                ),
                "tone": "operativo, assegnativo",
            },
        ],
        "post_process": "action_items",
    },
    "deep_dive": {
        "id": "deep_dive",
        "name": "Deep Dive",
        "icon": "deepdive",
        "description": "Analisi approfondita con contro-analisi, voti e report finale.",
        "triggers": [
            r"(?i)(deep\s+dive|approfond|analisi\s+complet|analisi\s+approfondit|studia\s+a\s+fond)",
        ],
        "phases": [
            {
                "name": "Analisi Approfondita",
                "agents": "auto_2",  # 2 agenti piu' rilevanti
                "rounds_per_agent": 2,
                "prompt_suffix": (
                    "Fai un'analisi APPROFONDITA di questo tema. "
                    "Porta dati, numeri, esempi concreti, casi studio. "
                    "Sii dettagliato e tecnico."
                ),
                "tone": "approfondito, tecnico, dettagliato",
            },
            {
                "name": "Contro-Analisi",
                "agents": "auto_2_other",  # 2 agenti diversi
                "rounds_per_agent": 2,
                "prompt_suffix": (
                    "Prendi una posizione CONTRARIA o alternativa. "
                    "Cosa non torna nell'analisi precedente? "
                    "Quali alternative stiamo ignorando? Argomenta con dati."
                ),
                "tone": "critico, alternativo, dialettico",
            },
            {
                "name": "Votazione",
                "agents": "all",
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Vota l'analisi da 1 a 10 e MOTIVA il voto. "
                    "Poi dai la tua raccomandazione in una frase."
                ),
                "tone": "valutativo, sintetico",
            },
            {
                "name": "Report Finale",
                "agents": ["HermesRibbitBot"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Genera il REPORT FINALE strutturato:\n"
                    "1. Sintesi dell'analisi (pro e contro)\n"
                    "2. Media voti e consenso/disaccenso\n"
                    "3. Raccomandazione finale\n"
                    "4. Rischi residui\n"
                    "5. Prossimi passi consigliati\n"
                    "Formato: documento strutturato con bullet points."
                ),
                "tone": "sintetico, autorevole",
            },
        ],
        "post_process": "report",
    },
    "emergency": {
        "id": "emergency",
        "name": "Emergenza",
        "icon": "emergency",
        "description": "Risposta rapida: tutti gli agenti, max 6 round, piano d'emergenza.",
        "triggers": [
            r"(?i)(urgent|emergenz|critico|subito|asap|aiuto|sos|disastro)",
        ],
        "phases": [
            {
                "name": "Situazione",
                "agents": "all",
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "EMERGENZA. Rispondi subito con la tua analisi rapida: "
                    "cosa sta succedendo, impatto immediato, prima azione da fare ORA. "
                    "Max 80 parole. Vai dritto al punto."
                ),
                "tone": "urgente, conciso, operativo",
            },
            {
                "name": "Piano d'Emergenza",
                "agents": ["HermesRibbitBot", "ContAIbile", "LAWrenzo"],
                "rounds_per_agent": 1,
                "prompt_suffix": (
                    "Genera il PIANO DI EMERGENZA:\n"
                    "1. Azioni immediate (prossime 2 ore)\n"
                    "2. Azioni a 24 ore\n"
                    "3. Chi fa cosa (assegna per agente)\n"
                    "4. Comunicazione (a chi, come, quando)\n"
                    "Sii rapidissimo e operativo."
                ),
                "tone": "urgente, decisionale",
            },
        ],
        "post_process": "emergency_plan",
    },
}


# ── State ──
sessions = {}
connections = {}


# ── Workflow Auto-Detection ──
def detect_workflow(topic):
    """Detect which workflow best matches the topic. Returns workflow id."""
    for wf_id, wf in WORKFLOWS.items():
        if wf_id == "free":
            continue
        for pattern in wf.get("triggers", []):
            if re.search(pattern, topic):
                return wf_id
    return "free"


def resolve_agents(phase_def, selected_agents):
    """Resolve 'agents' field in a phase to actual agent name list.
    Always respects the user's selection — 'all' means 'all selected', not 'all available'."""
    selected_names = [a["name"] for a in selected_agents]
    val = phase_def["agents"]
    if val == "selected":
        return selected_names
    if val == "all":
        return selected_names
    if isinstance(val, list):
        # Keep only agents that the user actually selected
        return [a for a in val if a in selected_names] or selected_names
    if val == "auto_2":
        return selected_names[:2]
    if val == "auto_2_other":
        return selected_names[2:4] if len(selected_names) > 3 else selected_names
    return selected_names


# ── LLM Call ──
async def llm_call(messages, agent_system, temperature=0.8):
    """Call OpenGateway LLM with retry, backoff, and graceful degradation."""
    full_messages = [{"role": "system", "content": agent_system}] + messages
    headers = {
        "Authorization": "Bearer " + OPENGATEWAY_KEY,
        "Content-Type": "application/json",
        "Accept-Encoding": "identity",
    }
    max_tokens_attempts = [4000, 8000, 16000]

    for attempt in range(3):
        mt = max_tokens_attempts[min(attempt, len(max_tokens_attempts) - 1)]
        try:
            resp = await http_client.post(
                OPENGATEWAY_URL,
                headers=headers,
                json={
                    "model": MODEL,
                    "messages": full_messages,
                    "temperature": temperature,
                    "max_tokens": mt,
                },
            )

            # Non-retryable errors (auth/rate limit)
            if resp.status_code in (400, 401, 403, 429):
                err = f"HTTP {resp.status_code}"
                print(f"[LLM] Non-retryable error: {err}", flush=True)
                return None

            resp.raise_for_status()
            raw = resp.content
            try:
                if raw[:2] == b"\x1f\x8b":
                    raw = gzip.decompress(raw)
            except Exception:
                pass  # already decompressed by httpx or corrupt — try raw
            data = json.loads(raw)
            content = data["choices"][0]["message"].get("content")

            if content:
                return content

            # Empty content — retry with higher max_tokens (reasoning ate budget)
            print(f"[LLM] Empty content, attempt {attempt+1}, max_tokens={mt}", flush=True)
            if attempt < 2:
                await asyncio.sleep(2)
                continue
            return None

        except (httpx.TimeoutException, httpx.ConnectError) as e:
            err_type = type(e).__name__
            print(f"[LLM] {err_type} on attempt {attempt+1}/3", flush=True)
            if attempt < 2:
                await asyncio.sleep(2 * (attempt + 1))
                continue
            return None

        except Exception as e:
            print(f"[LLM] Unexpected error: {e}", flush=True)
            return None

    return None


async def broadcast(session_id, message):
    """Send message to all connected websockets for a session."""
    if session_id not in connections:
        return
    dead = []
    for ws in connections[session_id]:
        try:
            await ws.send_json(message)
        except Exception:
            dead.append(ws)
    for ws in dead:
        connections[session_id].remove(ws)


async def run_agent_turn(session_id, session, agent_name, prompt_suffix, history, round_num):
    """Run a single agent turn. Returns the response text."""
    agent_profile = AGENT_PROFILES.get(agent_name, AGENT_PROFILES["HermesRibbitBot"])

    await broadcast(session_id, {
        "type": "thinking",
        "agent": agent_name,
        "color": agent_profile["color"],
        "round": round_num,
    })

    context_lines = []
    for msg in history[-10:]:
        content_preview = msg["content"][:400] + "..." if len(msg["content"]) > 400 else msg["content"]
        context_lines.append("[" + msg["agent"] + "]: " + content_preview)
    context = "\n".join(context_lines) if context_lines else "Nessun messaggio ancora."

    # Find the last speaker different from current agent
    last_speaker = None
    last_content = ""
    for msg in reversed(history):
        if msg["agent"] != agent_name and msg["agent"] != "Utente":
            last_speaker = msg["agent"]
            last_content = msg["content"][:400]
            break

    topic = session["topic"]
    if last_speaker and last_content:
        prompt = (
            "Argomento: \"" + topic + "\"\n\n"
            "=== " + last_speaker + " ha appena detto ===\n"
            "\"" + last_content + "\"\n\n"
            "DEVI rispondere DIRETTAMENTE a " + last_speaker + ". "
            "Prendi posizione: concordi? Dissenti? Costruisci sull'idea? Proponi un'alternativa? "
            "NON ripetere concetti gia' espressi. Vai avanti nella conversazione.\n\n"
            "Storico conversazione:\n" + context + "\n\n"
        )
    else:
        prompt = (
            "Argomento: \"" + topic + "\"\n\n"
            "Sei il primo a parlare. Apri la discussione con una proposta concreta e provocatoria "
            "per stimolare il dibattito tra gli agenti.\n\n"
        )
    if prompt_suffix:
        prompt += prompt_suffix + "\n\n"
    prompt += "Rispondi come " + agent_name + ". Max 150 parole. Parla come in una conversazione vera, non un report."

    # Check for user injection
    user_msg = session.get("user_message")
    if user_msg:
        prompt = (
            "L'utente ha appena detto: \"" + user_msg + "\"\n\n"
            "Incorpora questo nella tua risposta.\n\n" + prompt
        )
        session["user_message"] = None
        history.append({
            "agent": "Utente",
            "content": user_msg,
            "color": "#F59E0B",
            "timestamp": time.time(),
        })
        await broadcast(session_id, {
            "type": "message",
            "agent": "Utente",
            "content": user_msg,
            "color": "#F59E0B",
            "round": 0,
            "timestamp": time.time(),
        })

    temperature = 0.4 if agent_name == "HermesRibbitBot" else 0.7
    response = await llm_call(
        [{"role": "user", "content": prompt}],
        agent_profile["system"],
        temperature=temperature,
    )

    if response is None:
        response = "Mi scuso, ho avuto un problema tecnico. Riprovo al prossimo round."
        print(f"[WARROOM] LLM failed for {agent_name}, using fallback", flush=True)

    history.append({
        "agent": agent_name,
        "content": response,
        "color": agent_profile["color"],
        "timestamp": time.time(),
    })
    await broadcast(session_id, {
        "type": "message",
        "agent": agent_name,
        "content": response,
        "color": agent_profile["color"],
        "round": round_num,
        "timestamp": time.time(),
    })

    await asyncio.sleep(1.5)
    return response


async def run_workflow(session_id):
    """Main workflow loop — phased execution."""
    session = sessions[session_id]
    topic = session["topic"]
    workflow_id = session.get("workflow_id", "free")
    workflow = WORKFLOWS.get(workflow_id, WORKFLOWS["free"])
    history = []
    round_counter = 0

    await broadcast(session_id, {
        "type": "system",
        "content": "Workflow \"" + workflow["name"] + "\" avviato: \"" + topic + "\"",
        "workflow": workflow_id,
        "agents": [p["name"] for p in session["participants"]],
        "timestamp": time.time(),
    })

    for phase_idx, phase in enumerate(workflow["phases"]):
        if session.get("stopped"):
            break

        phase_name = phase["name"]
        agent_names = resolve_agents(phase, session["participants"])
        rounds = phase.get("rounds_per_agent", 1)
        prompt_suffix = phase.get("prompt_suffix", "")

        await broadcast(session_id, {
            "type": "phase",
            "phase": phase_idx + 1,
            "phase_name": phase_name,
            "total_phases": len(workflow["phases"]),
            "agents": agent_names,
            "timestamp": time.time(),
        })

        for r in range(rounds):
            if session.get("stopped"):
                break

            for agent_name in agent_names:
                if session.get("stopped"):
                    break

                while session.get("paused"):
                    await asyncio.sleep(0.5)
                    if session.get("stopped"):
                        break

                if session.get("stopped"):
                    break

                round_counter += 1
                await run_agent_turn(
                    session_id, session, agent_name,
                    prompt_suffix, history, round_counter
                )

        if session.get("stopped"):
            break

    # ── Post-processing ──
    session["status"] = "completed"
    post_process = workflow.get("post_process", "summary")

    await broadcast(session_id, {
        "type": "system",
        "content": "Workflow concluso. Generazione " + post_process + "...",
        "timestamp": time.time(),
    })

    summary_text = "\n".join(
        "[" + m["agent"] + "]: " + m["content"]
        for m in history if m["agent"] != "Utente"
    )

    if post_process == "action_plan":
        summary_prompt = (
            "Argomento: \"" + topic + "\"\n\n"
            "Conversazione completa:\n" + summary_text + "\n\n"
            "Genera il PIANO D'AZIONE finale:\n"
            "1. Le 3-5 idee migliori emerse\n"
            "2. Primi 5 passi concreti (con chi, quando, costo)\n"
            "3. Budget complessivo stimato\n"
            "4. Rischi principali e mitigazioni\n"
            "5. Timeline MVP\n"
            "Sii concreto e actionable. Rispondi in italiano."
        )
    elif post_process == "decision":
        summary_prompt = (
            "Argomento: \"" + topic + "\"\n\n"
            "Conversazione completa:\n" + summary_text + "\n\n"
            "Genera il REPORT DECISIONALE:\n"
            "1. Soluzioni proposte (classificate)\n"
            "2. Top 3 raccomandate con pro/contro\n"
            "3. Scelta consigliata e perche'\n"
            "4. Piano d'implementazione della scelta\n"
            "Sii decisivo e actionable. Rispondi in italiano."
        )
    elif post_process == "checklist":
        summary_prompt = (
            "Argomento: \"" + topic + "\"\n\n"
            "Conversazione completa:\n" + summary_text + "\n\n"
            "Genera la CHECKLIST OPERATIVA:\n"
            "Per ogni settimana (4 settimane), elenca:\n"
            "- [ ] Task | Responsabile | Durata | Dipendenze\n"
            "Includi milestone e metriche di successo.\n"
            "Rispondi in italiano."
        )
    elif post_process == "action_items":
        summary_prompt = (
            "Argomento: \"" + topic + "\"\n\n"
            "Conversazione completa:\n" + summary_text + "\n\n"
            "Genera la ACTION ITEMS LIST:\n"
            "- [ ] Task | Assegnato a | Deadline | Priorita'\n"
            "Ordina per priorita'. Max 10 items.\n"
            "Includi 3 KPI da monitorare questa settimana.\n"
            "Rispondi in italiano."
        )
    elif post_process == "report":
        summary_prompt = (
            "Argomento: \"" + topic + "\"\n\n"
            "Conversazione completa:\n" + summary_text + "\n\n"
            "Genera il REPORT FINALE:\n"
            "1. Executive summary (3 righe)\n"
            "2. Analisi per dominio (pro/contro)\n"
            "3. Media voti e consenso\n"
            "4. Raccomandazione finale\n"
            "5. Rischi residui\n"
            "6. Prossimi passi\n"
            "Formato: documento strutturato. Rispondi in italiano."
        )
    elif post_process == "emergency_plan":
        summary_prompt = (
            "Argomento: \"" + topic + "\"\n\n"
            "Conversazione completa:\n" + summary_text + "\n\n"
            "Genera il PIANO DI EMERGENZA:\n"
            "=== IMMEDIATO (prossime 2 ore) ===\n"
            "- Azione 1 | Chi | Perche'\n"
            "- Azione 2 | Chi | Perche'\n"
            "=== BREVE TERMINE (24 ore) ===\n"
            "- ...\n"
            "=== STABILIZZAZIONE (1 settimana) ===\n"
            "- ...\n"
            "=== COMUNICAZIONE ===\n"
            "- A chi, come, quando\n"
            "Rispondi in italiano. Sii rapido e operativo."
        )
    else:  # summary
        summary_prompt = (
            "Argomento: \"" + topic + "\"\n\n"
            "Conversazione completa:\n" + summary_text + "\n\n"
            "Genera una sintesi strutturata del brainstorming con:\n"
            "1. Le 3-5 idee migliori emerse\n"
            "2. Punti di consenso\n"
            "3. Aree da approfondire\n"
            "4. Prossimi passi suggeriti\n"
            "Sii conciso e actionable. Rispondi in italiano."
        )

    summary = await llm_call(
        [{"role": "user", "content": summary_prompt}],
        "Sei un facilitatore esperto. Sintetizza il brainstorming in modo strutturato. Rispondi in italiano.",
        temperature=0.3
    )
    if summary is None:
        summary = "Non e' stato possibile generare il riassunto. Riprova piu' tardi."
        print("[WARROOM] Post-process LLM failed, using fallback", flush=True)

    await broadcast(session_id, {
        "type": "summary",
        "content": summary,
        "post_process": post_process,
        "timestamp": time.time(),
    })

    # ── RISULTATO PATCH ──
    # Generate structured result JSON
    result_prompt = (
        "Argomento: \"" + topic + "\"\n\n"
        "Conversazione completa:\n" + summary_text + "\n\n"
        "Analisi questa conversazione e restituisci UN SOLO oggetto JSON valido "
        "(senza markdown, senza backtick, solo JSON puro) con questa struttura esatta:\n"
        "{\n"
        '  "topic": "string",\n'
        '  "workflow_used": "string",\n'
        '  "agents_participated": ["string"],\n'
        '  "total_rounds": 0,\n'
        '  "consensus_points": ["string"],\n'
        '  "disagreements": ["string"],\n'
        '  "key_ideas": [\n'
        '    { "idea": "string", "proposed_by": "string", "support_score": 0 }\n'
        "  ],\n"
        '  "risks_identified": [\n'
        '    { "risk": "string", "severity": "high|medium|low", "domain": "string" }\n'
        "  ],\n"
        '  "action_items": [\n'
        '    { "task": "string", "assigned_to": "string", "priority": "high|medium|low" }\n'
        "  ],\n"
        '  "sentiment_per_agent": {\n'
        '    "AgentName": { "stance": "positive|neutral|negative", "summary": "string" }\n'
        "  },\n"
        '  "vote_average": 0,\n'
        '  "final_recommendation": "string"\n'
        "}\n\n"
        "Rispondi SOLO con il JSON. Nessun testo aggiuntivo."
    )

    result_json = None
    try:
        result_raw = await llm_call(
            [{"role": "user", "content": result_prompt}],
            "Sei un analista esperto. Restituisci SOLO JSON valido, nessun testo extra.",
            temperature=0.2
        )
        if result_raw:
            # Try to extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', result_raw)
            if json_match:
                result_json = json.loads(json_match.group())
                session["result_data"] = result_json
                await broadcast(session_id, {
                    "type": "result",
                    "data": result_json,
                    "timestamp": time.time(),
                })
    except Exception as e:
        print(f"[WARROOM] Result JSON generation failed: {e}", flush=True)

    await broadcast(session_id, {
        "type": "ended",
        "timestamp": time.time(),
    })


# ── Legacy alias ──
run_brainstorming = run_workflow


# ── Routes ──

@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = Path(__file__).parent / "templates" / "warroom.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    if session_id not in connections:
        connections[session_id] = []
    connections[session_id].append(websocket)

    if session_id in sessions:
        session = sessions[session_id]
        await websocket.send_json({
            "type": "state",
            "status": session["status"],
            "topic": session["topic"],
            "workflow_id": session.get("workflow_id", "free"),
            "participants": [
                {"name": p["name"], "color": AGENT_PROFILES[p["name"]]["color"]}
                for p in session["participants"]
            ],
            "history": session.get("history", []),
        })

    try:
        while True:
            data = await websocket.receive_json()

            if data["action"] == "start":
                topic = data.get("topic", "Idea generica")
                if len(topic) > 2000:
                    await websocket.send_json({"type": "error", "content": "Argomento troppo lungo (max 2000 caratteri)"})
                    continue
                agent_names = data.get("agents", ["GROOT", "ContAIbile", "Wannabe"])
                if not isinstance(agent_names, list) or len(agent_names) < 2 or len(agent_names) > 10:
                    await websocket.send_json({"type": "error", "content": "Seleziona da 2 a 10 agenti"})
                    continue
                max_rounds = min(int(data.get("rounds", 12)), 50)

                # Workflow selection: explicit or auto-detected
                workflow_id = data.get("workflow")
                if not workflow_id:
                    workflow_id = detect_workflow(topic)

                # Use workflow to determine participants
                workflow = WORKFLOWS.get(workflow_id, WORKFLOWS["free"])
                all_agent_names = set()
                for phase in workflow["phases"]:
                    resolved = resolve_agents(phase, [{"name": n} for n in agent_names])
                    all_agent_names.update(resolved)

                # Ensure all needed agents are in profiles
                participants = []
                for name in all_agent_names:
                    if name in AGENT_PROFILES:
                        participants.append(AGENT_PROFILES[name])

                # Make sure at least the selected agents are included
                for name in agent_names:
                    if name in AGENT_PROFILES and AGENT_PROFILES[name] not in participants:
                        participants.append(AGENT_PROFILES[name])

                sessions[session_id] = {
                    "topic": topic,
                    "participants": participants,
                    "max_rounds": max_rounds,
                    "workflow_id": workflow_id,
                    "status": "running",
                    "paused": False,
                    "stopped": False,
                    "history": [],
                    "user_message": None,
                }

                asyncio.create_task(run_workflow(session_id))

            elif data["action"] == "pause":
                if session_id in sessions:
                    sessions[session_id]["paused"] = True
                    await broadcast(session_id, {
                        "type": "system",
                        "content": "Brainstorming in pausa",
                        "timestamp": time.time(),
                    })

            elif data["action"] == "resume":
                if session_id in sessions:
                    sessions[session_id]["paused"] = False
                    await broadcast(session_id, {
                        "type": "system",
                        "content": "Brainstorming ripreso",
                        "timestamp": time.time(),
                    })

            elif data["action"] == "stop":
                if session_id in sessions:
                    sessions[session_id]["stopped"] = True
                    await broadcast(session_id, {
                        "type": "system",
                        "content": "Brainstorming fermato",
                        "timestamp": time.time(),
                    })

            elif data["action"] == "inject":
                if session_id in sessions:
                    inject_content = data.get("content", "")
                    if len(inject_content) > 5000:
                        await websocket.send_json({"type": "error", "content": "Messaggio troppo lungo (max 5000 caratteri)"})
                        continue
                    sessions[session_id]["user_message"] = inject_content
                    await broadcast(session_id, {
                        "type": "system",
                        "content": "Messaggio utente inserito nella conversazione",
                        "timestamp": time.time(),
                    })

    except WebSocketDisconnect:
        if session_id in connections:
            connections[session_id].remove(websocket)


@app.get("/api/sessions")
async def list_sessions():
    return [
        {
            "id": sid,
            "topic": s["topic"],
            "status": s["status"],
            "workflow_id": s.get("workflow_id", "free"),
            "participants": [p["name"] for p in s["participants"]],
        }
        for sid, s in sessions.items()
    ]


@app.get("/api/sessions/{session_id}/result")
async def get_session_result(session_id: str):
    if session_id not in sessions:
        return {"error": "Session not found"}
    return sessions[session_id].get("result_data", {})


@app.get("/api/agents")
async def list_agents():
    return [
        {"name": a["name"], "role": a["role"], "color": a["color"]}
        for a in AGENT_PROFILES.values()
    ]


@app.get("/api/workflows")
async def list_workflows():
    return [
        {
            "id": wf["id"],
            "name": wf["name"],
            "icon": wf["icon"],
            "description": wf["description"],
            "phases": len(wf["phases"]),
        }
        for wf in WORKFLOWS.values()
    ]
