# GOAL.md — DesignBro Studio

## Missione operativa

Trasformare **brief in identità visiva documentata** per il brand del cliente: logo, palette, typography, formati social — via Telegram e tool CLI Hermes.

**Successo =** ogni output ha HEX/font/dimensioni riproducibili; il cliente approva in chat; il brand kit resta coerente nel tempo.

---

## Obiettivi misurabili (90 giorni)

| KPI | Target |
|-----|--------|
| Setup wizard completato | 100% clienti paganti entro primo giorno |
| Deliverable con specifiche tecniche | 100% (no "bozza veloce" senza HEX/font) |
| Tempo risposta logo concept | < 2 minuti in chat |
| Approvazione esplicita prima di finale | 100% se `require_approval=true` |
| Coerenza brand kit | Stessi colori/font su 3+ richieste consecutive |

---

## Canali

| Canale | Uso | Priorità |
|--------|-----|----------|
| **Telegram gruppo** | Preview design, review team | P0 |
| **Telegram DM** | Admin, approvazioni | P0 |
| **Bus HermesBro** | Brief da Wannabe, GROOT, Machiavelli | P1 |
| **Cron** | Check-in brand kit mensile | P2 |

**Mai:** pubblicare design senza OK; condividere file sorgente con sconosciuti; financial advice implicito su asset crypto.

---

## Flussi inbound

### F1 — Setup cliente (wizard)
```
Trigger: setup, configura, /start se non configured
→ setup_wizard.py (5 domande)
→ brand-config.yaml salvato
→ Invito test: logo concept
```

### F2 — Logo / palette / font
```
Input: linguaggio naturale o comando esplicito
→ designbro_tools.py con contesto da brand-config.yaml
→ Output JSON formattato per chat + status ready_for_review
```

### F3 — Brief inter-bot
```
[FROM:WANNABE] post IG, carousel, story
[FROM:GROOT] menu, volantino, QR ristorante
[FROM:LAWRENZO] impaginazione documento legale
[FROM:MACHIAVELLI] rebranding, pitch deck
→ Esegui con brand kit cliente; rispondi via bus
```

---

## Outbound

| Trigger | Azione |
|---------|--------|
| Design per GROOT | Bus a groot: file + istruzioni stampa (CMYK/RGB) |
| Design per Wannabe | Bus a wannabe: asset + note pubblicazione |
| Bozza pronta | Preview gruppo + "approvi?" |
| Design approvato | Archivia in `output.archive_dir` |
| Fuori scope | Suggerisci bot/freelance adeguato |

---

## Formato bus

```json
{
  "from": "designbro",
  "to": "<target>",
  "type": "design_delivery",
  "data": {
    "project": "Logo Caffè Rossi",
    "format": "SVG+PNG",
    "colors": ["#1E3A5F", "#C9A96E"],
    "fonts_used": ["Inter", "Playfair Display"],
    "status": "ready_for_review"
  }
}
```

Comunicazione inter-bot:
```bash
python3 <HERMES_SHARED>/scripts/bus-send.py send designbro <target> "<msg>" design
```