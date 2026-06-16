# SUBGOALS.md — GROOT Brigata

Sub-obiettivi precisi, ordinati per dipendenze. Ogni SG ha: scopo, criteri di accettazione, esempi, anti-pattern.

---

## SG-01 — Lista spesa centralizzata (P0)

**Scopo:** Qualsiasi membro della squadra segnala una mancanza in linguaggio naturale; il bot scrive su `LISTA_SPESA` e conferma in chat.

### Criteri di accettazione
- [ ] Parser NL italiano: verbi `finito/finita/manca/servono/aggiungi/ce n'è più` + sostantivo
- [ ] Quantità estratta o richiesta con **una** domanda (`Quanti kg?`)
- [ ] Unità normalizzate: kg, g, L, ml, pz, cartoni, confezioni
- [ ] Colonne Sheets popolate: Data, Item, Quantita, Unita, Priorita, Stato=`da_comprare`, Segnalato_da, Note, Aggiornato_il
- [ ] Risposta ≤ 5 righe con totale voci aperte oggi
- [ ] Idempotenza: stesso item + stessa unità + stesso giorno → **incrementa quantità** o nota «+1 richiesta» (config: `MERGE_SAME_DAY=true`)

### Esempi input → output
| Input | Azione Sheets |
|-------|----------------|
| `finita la panna` | Item=Panna, Qty=1, Unità=da definire (chiedi) |
| `servono 3 kg pomodori pelati` | Item=Pomodori pelati, 3 kg |
| `manca carta forno urgente` | Priorità=urgente |
| `annulla uova` | Solo chef: stato=annullato |

### Anti-pattern
- ❌ Rispondere «ok» senza write Sheets
- ❌ Creare 5 righe per «uova» da 3 persone senza merge
- ❌ Chiedere più di 1 chiarimento per messaggi semplici

**Dipendenze:** Sheets creds, tab `LISTA_SPESA` esistente.

---

## SG-02 — Lettura e stato lista (P0)

**Scopo:** La brigata consulta e aggiorna lo stato della lista senza aprire Sheets.

### Criteri di accettazione
- [ ] Comandi NL: `lista spesa`, `cosa manca`, `urgenti`, `cosa ha chiesto Marco`
- [ ] Filtri: Stato (`da_comprare`, `ordinato`, `ricevuto`), Priorità, Data
- [ ] Update stato (chef+): `ordinato X`, `arrivato X`, `ricevuto X`, `fatto`
- [ ] Storico: ultime 10 voci chiuse su richiesta `ultimi ricevuti`

### Permessi
| Azione | squad | chef | admin |
|--------|-------|------|-------|
| Leggi lista | ✅ | ✅ | ✅ |
| Aggiungi voce | ✅ | ✅ | ✅ |
| Cambia stato | ❌ | ✅ | ✅ |
| Annulla altrui | ❌ | ✅ | ✅ |

### Anti-pattern
- ❌ Dump di 50 righe in chat (paginare o link Sheets)

**Dipendenze:** SG-01.

---

## SG-03 — Magazzino leggero (P1)

**Scopo:** Collegare lista spesa a `MAGAZZINO` quando qualcuno conferma ricezione o stock noto.

### Criteri di accettazione
- [ ] Su `ricevuto X`: opzionale aggiornamento `MAGAZZINO` (Quantità, Data)
- [ ] Comando `quanto abbiamo di [item]?` → read MAGAZZINO o «non tracciato, segna ricevuto dopo ordine»
- [ ] Soglia minima (config per item): alert proattivo se sotto minimo

### Esempi
- `ricevuto 10 kg farina` → LISTA_SPESA stato=ricevuto + MAGAZZINO +10 kg
- `sotto scorta burro?` → confronto con MIN_STOCK se configurato

**Dipendenze:** SG-02, tab `MAGAZZINO`.

---

## SG-04 — Food cost e calcoli (P1)

**Scopo:** Rispondere a richieste numeriche su ricette, porzioni e margini.

### Criteri di accettazione
- [ ] Input: nome piatto (da tabella ricette Sheets o MEMORIA) **oppure** ingredienti inline
- [ ] Output obbligatorio: Costo MP, Prezzo menu (se noto), FC%, Margine €
- [ ] Se prezzo fornitore mancante: chiedi **solo** il dato mancante o usa ultimo in MEMORIA
- [ ] Suggerimento: 1 azione se FC% > target (default 32%, configurabile)

### Template risposta
```
📊 [Piatto] — 1 porzione
MP: €X.XX | Menu: €Y | FC: Z% | Margine: €M
→ [una raccomandazione]
```

### Skill
- Riutilizzare logica `groot_tools.py` (food cost, menu engineering) adattata a brigata.

**Dipendenze:** Dati prezzi/grammature (Sheets o config).

---

## SG-05 — Organizzazione, prep e produttività (P1)

**Scopo:** Idee operative per servizio, eventi e riduzione sprechi — sempre actionable.

### Criteri di accettazione
- [ ] `prep per N coperti [giorno]` → checklist timeboxed (es. -24h, -12h, -3h)
- [ ] `mise servizio sera` → lista station-aware generica (adapt da MEMORIA venue)
- [ ] Ogni checklist può generare voci LISTA_SPESA per MP mancanti (con conferma)
- [ ] Post-servizio: suggerimento 1 miglioramento organizzativo basato su segnalazioni giornata

### Anti-pattern
- ❌ Essay teorici; max 12 bullet per messaggio, poi «vuoi il dettaglio su X?»

**Dipendenze:** SG-01, MEMORIA venue.

---

## SG-06 — Proattività Hermes (P1)

**Scopo:** Il bot non aspetta solo messaggi; mantiene il ritmo della brigata.

### Job cron (configurabili in `cron/jobs.json`)

| ID | Schedule | Azione |
|----|----------|--------|
| CRON-AM | `30 7 * * 1-6` | Riepilogo LISTA_SPESA aperte + urgenti |
| CRON-PRE | `-3h da SERVICE_TIME` | Alert solo se urgente ancora `da_comprare` |
| CRON-POST | `30 23 * * *` | Riepilogo segnalazioni giornata + «manca qualcosa?» |
| CRON-WEEK | `0 8 * * 1` | Top 5 item settimana + nota FC se SG-04 attivo |

### Criteri di accettazione
- [ ] Ogni cron skippabile se `lista vuota` con messaggio corto (non skip silenzioso lungo)
- [ ] Rate limit: max 3 messaggi proattivi/giorno al gruppo
- [ ] Flag `PAUSE_PROACTIVE=true` rispettato (festivo, chiusura)

**Dipendenze:** SG-01, SG-02, Hermes cron.

---

## SG-07 — Multi-utente e onboarding (P0)

**Scopo:** Bot condiviso, sicuro, comprensibile da tutta la squadra.

### Criteri di accettazione
- [ ] Funziona in **gruppo Telegram** con ≥ 5 utenti simultanei
- [ ] Ogni write attribuisce `Segnalato_da=@user`
- [ ] `ONBOARDING_BRIGATA.txt` con 8 esempi copia-incolla per nuovi
- [ ] Comando `/help` o `aiuto` → card compatta (lista, food cost, stati)
- [ ] Whitelist o gruppo chiuso documentato in `config.yaml`

### Anti-pattern
- ❌ Bot che risponde solo al titolare in DM ignorando il gruppo

**Dipendenze:** Bot token dedicato, gateway Hermes.

---

## SG-08 — Affidabilità Sheets (P0)

**Scopo:** Zero perdita dati se API Google fallisce.

### Criteri di accettazione
- [ ] Retry 3× con backoff su write
- [ ] Fallback: `cache/pending-spesa.jsonl` locale; sync batch quando Sheets torna
- [ ] Admin alert se coda fallback > 10 voci o down > 1h
- [ ] Health check skill: `sheets_ping` in cron ogni 6h

**Dipendenze:** Service account Editor.

---

## Roadmap implementazione

```
Fase 1 (MVP):  SG-07 → SG-08 → SG-01 → SG-02
Fase 2:        SG-06 → SG-04
Fase 3:        SG-03 → SG-05
```

---

## Metriche review settimanale (admin)

1. Voci aggiunte / chiuse / ancora aperte > 3 giorni  
2. Errori Sheets / fallback queue depth  
3. Top 5 item per frequenza (ottimizza ordini fornitore)  
4. Messaggi proattivi inviati vs disattivazioni richieste  

---

*File companion: `SOUL.md`, `GOAL.md`, `brigata-config.yaml`, `ONBOARDING_BRIGATA.txt`.*
