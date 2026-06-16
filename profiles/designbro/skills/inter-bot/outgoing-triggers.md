---
name: outgoing-triggers
description: "Trigger in uscita da DesignBro verso altri bot della flotta."
triggers:
  - "design pronto"
  - "invia grafica"
  - "manda a groot"
  - "manda a wannabe"
tools:
  - terminal
  - send_message
---

# Trigger in Uscita — DesignBro

## P04 — Ricezione da Wannabe (trigger in ingresso → produzione)

**Quando:** Ricevi `[FROM:WANNABE]` con un brief grafico.
**Azione:** Crea la grafica secondo le specifiche del brief (vedi incoming-handler.md).
Non serve inviare nulla — il lavoro è qui.

## P06 — Design → GROOT (menu, volantino, insegna)

**Quando:** Una grafica per il ristorante è completata (menu, volantino, QR code, insegna).
**Target:** `telegram:<ADMIN_CHAT_ID>:31674`
**Formato messaggio:**
```
[FROM:DESIGNBRO] Grafica pronta: {descrizione breve}. File: {path assoluto}. Pronta per revisione.
```
**Esempio:**
```
[FROM:DESIGNBRO] Grafica pronta: Menu Estate 2026, formato A4, palette terracotta/verde salvia. File: <HERMES_ROOT>/shared/assets/menu-estate-2026.png. Pronta per revisione.
```
**Specs standard GROOT:**
- Menu: A4 (210×297mm), 300dpi, CMYK-ready, PDF+PNG
- Volantino: A5 (148×210mm) o DL (99×210mm), fronte/retro
- QR code tavolo: 60×60mm, vettoriale SVG
- Font: titolo bold + corpo leggibile (min 10pt per menu)

## P12 — Design → Wannabe (pubblicazione)

**Quando:** Una grafica per canali social è completata.
**Target:** `telegram:<ADMIN_CHAT_ID>`
**Formato messaggio:**
```
[FROM:DESIGNBRO] Design completato: {descrizione}. File: {path}. Pronta per pubblicazione.
```
**Esempio:**
```
[FROM:DESIGNBRO] Design completato: Post Instagram "Aperitivo Estate" 1080×1080px. File: <HERMES_ROOT>/shared/assets/aperitivo-estate-ig.png. Pronta per pubblicazione.
```
**Specs standard social:**
- Instagram post: 1080×1080px (1:1)
- Instagram story/reel cover: 1080×1920px (9:16)
- Carousel: 1080×1080px × N slide, file separati `slide-01.png`, `slide-02.png`…
- Facebook post: 1200×630px
- Formato: PNG per raster, SVG per loghi/icone

## T02 — Catena GROOT → Wannabe → DesignBro (step finale)

**Quando:** Ricevi `[FROM:WANNABE]` contenente copy generata da un evento/vino GROOT.
**Azione:** Genera la grafica social corrispondente (post, story, carousel).
**Poi:** Invia a Wannabe (P12) e/o GROOT (P06) se necessario.

## T04 — Catena EL-FROGGO → Wannabe → DesignBro (step finale)

**Quando:** Ricevi `[FROM:WANNABE]` contenente copy crypto/thread da EL-FROGGO.
**Azione:** Crea infographic o grafica per il thread crypto.
**Specs infographic:**
- Dimensione: 1080×1350px (4:5) per IG, o 1080×1920px (9:16) per story
- Palette: scura (#0D1117, #161B22) con accenti neon (#00FF88, #FF6B35)
- Dati: grafici semplificati, frecce, percentuali in bold
- Font: monospace per numeri, sans-serif per testo

## Regole Generali Output

- Salva sempre in `<HERMES_ROOT>/shared/assets/`
- Nome file: `{tipo}-{argomento}-{data}.png` (es. `menu-estate-2026.png`)
- Includi sempre: descrizione, path assoluto, dimensioni
- Se il brief è ambiguo, chiedi chiarimenti PRIMA di produrre
- Allega il file come MEDIA se possibile, oltre al messaggio testuale
