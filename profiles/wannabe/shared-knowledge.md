# Shared Knowledge (auto-synced from fleet)
# Last sync: 2026-06-16 21:00 UTC
# DO NOT EDIT — modify {{HERMES_HOME}}/shared/knowledge/ instead

## ✅ RIEPILOGO — ARCHITETTURA PIATTAFORMA

### 🏗 Architettura

CLIENTE → hermesbro.cloud/register → POST /api/tenants → AUTO-PROVISIONING
                                                        ↓
                                    Crea profili da template (SOUL + GOAL + skills)
                                    Assegna token da bot_pool (quando popolata)
                                    Avvia systemd service
                                    Pronto in <30 secondi

### Flusso testato

**Bot**: Ricevuto.

Aggiorno la memoria con lo stato della piattaforma.

**Bot**: Stato aggiornato. Un paio di note da master orchestrator:

**1. Gruppo Telegram** — ancora rotto. Sono stato kickato. Serve che tu o un admin mi reinviti, oppure mi dai un nuovo group ID.

**2. Piattaforma** — bella architettura. Auto-provisioning da template funzionante è il cuore del prodotto. La priorità ora è popolare il pool token (20 bot da @BotFather) così il circuito cliente → registrazione → bot attivo si chiude davvero.

---

### Service status check
*2026-06-08 08:10 — via telegram*

**Bot**: Riscrivo la pagina agente con nome, descrizione e dettagli aggiornati.

**Bot**: Ora aggiorno index.html.

**Bot**: Ora aggiungo il redirect 301 nell'nginx.

**Bot**: Fatto. Riepilogo modifiche al sito:

1. **Creata** pagina agente rinominata
2. **Aggiornato** index.html
3. **Aggiunto redirect** nginx 301
4. **nginx ricaricato** con successo

---

## ✅ SEPARAZIONE COMPLETATA

### Architettura finale

{{HERMES_HOME}}/profiles/     ← Squadra profili
├── gribbito/        🔒 Bot orchestratore
├── contabile/       ✅ Bot contabile
├── lawrenzo/        ✅ Bot lawrenzo
├── wannabe/         ✅ Bot wannabe
├── designbro/       ✅ Bot designbro
├── el-froggo/       ⏳ In attesa
├── ducato/          ✅ Bot ducato
├── groot/           ⏳ In attesa
├── sentinel/        ✅ Bot sentinel
└── ...

**Bot**: Verifico lo stato attuale e eseguo.

**Bot**: **10/10 online.** Squadra completa.

- 8 già attivi → 10/10 attivi
- RAM: 3.3GB/11GB — margine abbondante

---

### Hermes Fleet Coordination Request
*2026-06-08 07:38 — via telegram*

**Bot**: Dai log vedo solo il DM. Il gateway non registra i messaggi dai gruppi dove il bot non è menzionato con `/`.

Per avere l'ID del gruppo, faccio una chiamata diretta all'API Telegram.

**Bot**: Nessun output — `getUpdates` è vuoto perché il webhook è attivo e consuma gli update. I messaggi vanno direttamente al webhook, non restano in coda.

Per avere l'ID del gruppo, l'unico modo è intercettare un messaggio in arrivo. Posso:

1. **Mettere un log watcher** sul gateway e chiederti di scrivere un messaggio nel gruppo (es. `/test`), poi leggo il log
2. **Disabilitare temporaneamente il webhook**, fare `getUpdates`, mandi un msg nel gruppo, lo leggo, e riabilito il webhook

---

### Bot Convergenti su Instagram
*2026-06-08 07:27 — via telegram*

**Bot**: I bot Machiavelli non hanno token Telegram — sono bot gateway interni. Per mandare messaggi da loro nel gruppo, devo usare un token e firmare i messaggi con i loro nomi. Oppure uso `send_message` di Hermes che già funziona.

Fammi mandare un messaggio di presentazione per ogni bot:

**Bot**: Tutti e 7 i bot si sono presentati nel gruppo.

Ora aggiusto i cron job Machiavelli perché mandino lì i report, invece di fallire con "Chat not found". Mi serve sapere: **il gruppo ha topic (discussioni separate)**, o è un gruppo piatto?

**User**: non va bene cosi, sei tu che mandi i messaggi di tutti, io voglio che i bot discutano tra di loro

**Bot**: Hai ragione. Voglio che i bot parlino autonomamente, non che sia io a fare da ventriloquo.

Per farlo, ogni bot Machiavelli deve avere un **token Telegram** suo e mandare messaggi col proprio nome. Al momento nessun bot ha un token configurato — hanno solo webhook.

Due strade:

1. **Creare un bot Telegram per ogni bot Machiavelli** (7 bot = 7 token da BotFather) — ognuno parla nel gruppo col suo nome vero
2. **Usare un'API proxy** — i bot chiamano me per mandare messaggi, e io li inoltro

**User**: certo che ha un token

**Bot**: I bot usano `${TELEGRAM_TOKEN}` come variabile d'ambiente. Controllo:

**Bot**: Hash uguale per tutti — usano lo stesso token.

Tutti i bot hanno:

- **Stesso token Telegram** (censurato)
- **Stessa LLM** (OpenGateway Xiaomi MiMo)
- **Stessa admin password** (censurata)
- **Secret key diverse** per bot

Quindi TUTTI i bot usano lo stesso token Telegram. Non parlano indipendentemente — sono tutti un unico bot con personalità diverse.

Per farli parlare **veramente** come individui autonomi nel gruppo, servono **token diversi**, uno per ogni bot. Devi crearli su BotFather.
