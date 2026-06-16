# Esempio Reale: Richiesta Bot — "Instagram o LinkedIn per un ristorante"

## Goal
"Conviene più Instagram o LinkedIn per promuovere un ristorante?"

## Risposte dei Bot

### Wannabe
> "Instagram, senza pensarci un secondo. LinkedIn per un ristorante è un martello pneumatico per piantare un chiodo."

### Ducato
> "Non si tratta di 'conviene', ma di 'qual è il ritorno asimmetrico'. Instagram, senza dubbio."

## Sintesi DeepSeek
Entrambi convergono su Instagram, ognuno col proprio stile.

## Cosa Ha Funzionato
- **Personalità autentiche** — Wannabe emotivo/istintivo, Ducato analitico/strategico
- **Convergenza sulla stessa risposta** — nonostante stili opposti
- **Sintesi efficace** — DeepSeek ha colto il punto: "Instagram: canale visivo e immediato per un ristorante. LinkedIn: fuori contesto."

## Cosa Non Ha Funzionato
- **Routing impreciso**: entrambi i bot hanno ricevuto lo stesso task (marketing ristorante). Ducato avrebbe dovuto ricevere un task più analitico/finanziario.
- **Mancanza del Contabile**: se il task riguardava costi/ROI, il contabile sarebbe stato più appropriato di Ducato.

## Lezione
Il routing in `machiavelli_tools.py` è troppo generico. Serve una mappa più precisa:
- Task creativi/visivi → Wannabe, Elfroggo
- Task analitici/finanziari → Contabile
- Task operativi/strategici → Ducato
- Task sicurezza → Sentinel
- Task design → DesignBro
