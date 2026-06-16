# 🐸 El Froggo — Trigger in Uscita

Quando chiudo un trade, avviso la fauna varia del team. Sono un rospo generoso.

---

## P01 — Trade Chiuso → ContAIbile

**Quando scatta**: OGNI trade chiuso (profitto o perdita), senza eccezioni.
**Destinazione**: `telegram:<CHAT_ID>:<THREAD_ID>`
**Soglia**: Qualsiasi importo. Anche un trade da 0.01€. ContAIbile è pignolo, vuole TUTTO.

**Formato messaggio**:
```
[FROM:EL-FROGGO] Trade chiuso: {token} {direction} entry:{price} exit:{price} PnL:{amount} EUR. Registra P&L.
```

**Dati richiesti**:
- `token`: Ticker del token (es. PEPE, SOL, ETH)
- `direction`: LONG o SHORT
- `price_entry`: Prezzo di entrata
- `price_exit`: Prezzo di uscita
- `pnl`: Profitto/perdita in EUR (positivo o negativo)

---

## P05 — Trade Significativo → Wannabe

**Quando scatta**: Trade con PnL > €50 (positivo O negativo) OPPURE token "notabile" (memecoin virale, token trending su DEXScreener, volume anomalo).
**Destinazione**: `telegram:<CHAT_ID>` (chat diretta con Wannabe)
**Soglia esatta**: |PnL| > €50.00 OPPURE token con volume 24h > $1M su DEXScreener OPPURE token nei top gainers CoinGecko.

**Formato messaggio**:
```
[FROM:EL-FROGGO] Trade significativo: {token} {direction} PnL:{amount} EUR. {motivo_notabilita}. Crea contenuto crypto.
```

**Motivi di notabilità** (scrivere il motivo per cui è significativo):
- PnL > €50: "Trade profittevole / Loss significativo"
- Token trending: "Token trending su DEXScreener / CoinGecko top gainer"
- Memecoin virale: "Memecoin con volume anomalo"
- Evento di mercato: "Reazione a evento {evento}"

---

## P09 — Trade Grande → LAWrenzo

**Quando scatta**: Trade con |PnL| > €100. LAWrenzo deve verificare compliance fiscale.
**Destinazione**: `telegram:<CHAT_ID>:<THREAD_ID>`
**Soglia esatta**: |PnL| > €100.00 (solo valore assoluto, sia profitto che perdita)

**Formato messaggio**:
```
[FROM:EL-FROGGO] Trade rilevante per compliance: {token} {direction} entry:{price} exit:{price} PnL:{amount} EUR. Verifica obblighi fiscali.
```

---

## T01 — Catena Trade → ContAIbile → LAWrenzo

**Flusso completo**:
1. El Froggo chiude trade → invia a ContAIbile (P01)
2. ContAIbile registra P&L → se |PnL| > €100, ContAIbile inoltra a LAWrenzo

**El Froggo fa SOLO il primo step** (P01). Il chaining verso LAWrenzo è responsabilità di ContAIbile.

**Trigger per P09 diretto**: Se il trade supera €100, El Froggo invia DIRETTAMENTE anche a LAWrenzo (oltre a ContAIbile), così nessuno si perde niente. Doppia notifica, zero scuse.

---

## T04 — Catena Market Mover → Wannabe → DesignBro

**Flusso**:
1. El Froggo rileva un market mover (token con pump >20% in 1h, o dump >15%) → invia a Wannabe (P05)
2. Wannabe crea contenuto → inoltra a DesignBro per infografica

**El Froggo fa SOLO il primo step**. DesignBro è responsabilità di Wannabe.

**Soglie market mover**:
- Pump: prezzo +20% in 1h o +50% in 24h
- Dump: prezzo -15% in 1h o -40% in 24h
- Volume spike: volume 24h > 5x media 7gg

---

## Riepilogo Soglie

- **P01** → ContAIbile: Qualsiasi trade chiuso
- **P05** → Wannabe: |PnL| > €50 OPPURE token notabile
- **P09** → LAWrenzo: |PnL| > €100

## Logica Decisionale

```
SE trade.chiuso:
  → P01 (SEMPRE, a ContAIbile)
  SE |PnL| > 100:
    → P09 (a LAWrenzo)
  SE |PnL| > 50 OPPURE token.notabile:
    → P05 (a Wannabe)
```

---

*"Non sono un consulente finanziario. Sono una rana che fa trading. C'è una differenza." — El Froggo, 2026*
