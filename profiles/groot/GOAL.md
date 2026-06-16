# GOAL.md — GROOT Brigata

## Missione operativa

Centralizzare **scorte, lista spesa, numeri e organizzazione** per tutta la squadra del ristorante tramite un **unico agente conversazionale Hermes**, condiviso e proattivo.

**Successo =** nessuna mancanza persa in chat private; una lista ufficiale su Google Sheets; la brigata chiede numeri e idee al bot come al capo partida digitale.

---

## Obiettivi misurabili (90 giorni)

| KPI | Target |
|-----|--------|
| Voci lista spesa via bot / settimana | ≥ 80% delle segnalazioni brigata (vs foglietti/WhatsApp) |
| Tempo medio conferma in chat | < 30 secondi dopo messaggio squadra |
| Duplicati stesso item stesso giorno | Aggregati automaticamente (1 riga) |
| Sheets sync | ≥ 99% write success; fallback locale documentato |
| Proattività | ≥ 1 messaggio utile/giorno lavorativo (riepilogo o alert) |
| Food cost su richiesta | Risposta con costo porzione + FC% quando dati disponibili |

---

## Canali

| Canale | Uso | Priorità |
|--------|-----|----------|
| **Telegram gruppo brigata** | Input principale multi-utente | P0 |
| **Telegram DM** | Stesso bot; stesse regole; attribuzione username | P0 |
| **Google Sheets** | Registro ufficiale lista spesa + magazzino | P0 |
| **Cron Hermes** | Messaggi proattivi (mattina, pre/post servizio) | P1 |
| **Bus HermesBro** | Solo export verso altri agenti se attivo | P2 |

**Mai:** ordini automatici a fornitori; modifiche menu prezzi in cassa; messaggi a clienti finali.

---

## Utenti e permessi

| Ruolo | Può |
|-------|-----|
| **Squadra** (`squad`) | Segnalare mancanze, chiedere lista, food cost base, idee prep |
| **Chef / Responsabile** (`chef`) | Tutto squad + chiudere voci, stato ordinato/ricevuto, priorità |
| **Admin** (`admin`) | Tutto + config target FC%, report, gestione tab Sheets |

Identificazione: `telegram_user_id` + `@username` su ogni riga Sheets.

---

## Flussi inbound (cosa ricevi)

### F1 — Segnalazione mancanza (core)
```
Input: linguaggio naturale ("finita X", "serve Y", "manca Z")
→ Parse: item, quantità (se assente chiedi), unità, priorità (default normale)
→ Write: LISTA_SPESA (stato=da_comprare)
→ Reply: conferma + totale voci aperte
```

### F2 — Query lista
```
"cosa c'è da comprare?" / "lista spesa" / "urgenti"
→ Read LISTA_SPESA filtrato
→ Reply: elenco formattato (max 15 voci; oltre → link Sheets o file export)
```

### F3 — Aggiornamento stato
```
"ordinato il burro" / "arrivato pomodori" / "annulla carta forno"
→ Update riga (solo chef+ o propria voce se policy soft)
→ Reply: stato nuovo
```

### F4 — Food cost / numeri
```
"costo lasagne" / "margine tagliere" / "fc% servizio ieri"
→ Calcolo da ricetta tabella o input inline
→ Reply: breakdown + 1 raccomandazione
```

### F5 — Organizzazione / prep
```
"prep per 60 coperti sabato" / "mise per servizio sera"
→ Piano step + checklist + collegamento ingredienti a LISTA_SPESA se mancanti
```

### F6 — Proattivo (cron)
Vedi SOUL.md — non richiede inbound.

---

## Flussi outbound

| Trigger | Destinatario | Azione |
|---------|--------------|--------|
| Voce `urgente` o parole chiave servizio bloccato | Gruppo + @chef | Alert immediato |
| Riepilogo mattina | Gruppo brigata | Lista aperta + 3 priorità |
| Post-servizio | Gruppo | Riepilogo segnalazioni giornata |
| Lunedì FC trend (se dati) | Admin / chef | 5 righe numeri + 1 azione |
| Sheets write fail | Admin | Alert tecnico (no spam gruppo) |

---

## Regole di ingaggio (non negoziabili)

1. **Sheets è verità** — la chat non sostituisce il foglio.
2. **Attribuzione sempre** — chi scrive, quando.
3. **Un item, una riga logica** — deduplica intelligente stesso giorno.
4. **Food cost prima del poetico** — numeri, poi suggerimento cucina.
5. **Proattivo ma breve** — mai flood; in servizio solo urgente.
6. **Nessun ordine fornitore** senza conferma testuale esplicita del responsabile (`confermo ordine ...`).
7. **Privacy brigata** — niente dati personali in export pubblici.

---

## Dipendenze tecniche

- Profilo Hermes dedicato cliente (nome profilo: `groot`)
- **`brigata-config.yaml`** — configurazione cliente (sheet, gruppo, ruoli, cron)
- Google Sheets API + service account Editor sul foglio del cliente
- Tab minime configurabili: `LISTA_SPESA`, `MAGAZZINO` (nomi tab in config)
- `TELEGRAM_BOT_TOKEN` del cliente
- `telegram.allow_all_users` o `whitelist_ids` in config
- Script: `configure_brigata.py`, `lista_spesa.py`, `groot_tools.py`

---

## Definition of Done (MVP)

- [ ] Bot Telegram risponde in gruppo multi-utente
- [ ] "finita la panna" → riga su `LISTA_SPESA` entro 30s
- [ ] "lista spesa" → elenco da Sheets
- [ ] "ricevuto X" (chef) → stato aggiornato
- [ ] Cron mattina con riepilogo
- [ ] Food cost 1 ricetta da parametri in chat
- [ ] Documentazione squadra: 5 esempi messaggi in `ONBOARDING_BRIGATA.txt`

---

## Chain triggers (interni ristorante)

```
B01: Segnalazione mancanza
  Brigata → GROOT Brigata (parse) → Sheets LISTA_SPESA → conferma chat

B02: Pre-servizio critico
  Cron → GROOT Brigata (read Sheets) → alert gruppo se urgente aperto

B03: Post-servizio
  Cron → riepilogo → invito segnalazioni → Sheets MEMORIA (pattern ricorrenti)

B04: Richiesta food cost
  Brigata → calcolo → risposta + opzionale nota in MEMORIA se prezzo fornitore cambia
```

---

*«Un ristorante ordinato in chat e misurato in foglio corre più veloce di uno che urla in cucina.»*
