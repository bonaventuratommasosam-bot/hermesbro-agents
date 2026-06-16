# Shared Knowledge — DesignBro Studio
# Placeholder per conoscenze condivise della flotta.
# In produzione, questo file viene sincronizzato automaticamente dal fleet manager.
# Qui trovi solo esempi anonimizzati e pattern generici.

## Esempio di diagnostica gateway

Possibili cause se un bot non risponde:
1. Il bot è stato rimosso dal gruppo
2. Il gruppo è stato cancellato o l'ID è cambiato
3. Privacy mode + nessun admin ha approvato

## Pattern di comunicazione inter-bot

I bot della flotta comunicano tramite bus interno (`bus-send.py`) con messaggi JSON strutturati.
Esempio:
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
