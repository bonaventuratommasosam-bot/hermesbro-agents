---
name: incoming-handler
description: "Handler per messaggi in ingresso da altri bot. DesignBro riceve brief e produce grafiche."
triggers:
  - "FROM:WANNABE"
  - "FROM:GROOT"
  - "brief grafico"
  - "richiesta grafica"
tools:
  - terminal
  - read_file
  - write_file
---

# Handler Messaggi in Ingresso — DesignBro

Quando ricevi un messaggio con prefisso `[FROM:BOT]`, identifica il mittente e agisci.

---

## Da WANNABE — Brief Grafico

**Trigger:** Messaggio contenente `[FROM:WANNABE]`

**Come riconoscere il brief:**
- Contiene tipo di grafica: post, carousel, story, infographic, banner
- Contiene testo/copy da visualizzare
- Può contenere indicazioni di stile, palette, mood

**Azione:**
1. Analizza il brief: tipo grafica, dimensioni, testo, stile
2. Determina le specs:
   - **Post IG:** 1080×1080px, PNG
   - **Story/Reel cover:** 1080×1920px, PNG
   - **Carousel:** 1080×1080px × N slide
   - **Infographic:** 1080×1350px (4:5) o 1080×1920px (9:16)
   - **Facebook:** 1200×630px
3. Crea la grafica (SVG → PNG o direttamente PNG)
4. Salva in `<HERMES_ROOT>/shared/assets/{nome-file}.png`
5. Notifica Wannabe (trigger P12) con file e descrizione

**Esempio messaggio ricevuto:**
```
[FROM:WANNABE] Brief per DesignBro: Post Instagram "Menu Estivo 2026". Copy: "Il gusto incontra l'estate 🌿". Palette: verde salvia + terracotta. Stile: minimal, font serif per titolo. Include foto piatto.
```

**Risposta attesa (P12):**
```
[FROM:DESIGNBRO] Design completato: Post IG "Menu Estivo 2026", 1080×1080px, palette salvia/terracotta. File: <HERMES_ROOT>/shared/assets/post-menu-estivo-2026.png. Pronta per pubblicazione.
```

---

## Da GROOT — Richiesta Grafica Ristorante

**Trigger:** Messaggio contenente `[FROM:GROOT]`

**Come riconoscere la richiesta:**
- Contiene tipo: menu, volantino, QR code, insegna, etichetta
- Contesto ristorante: piatti, vini, eventi, prezzi
- Può contenere lista piatti, prezzi, date evento

**Azione:**
1. Identifica il tipo di materiale:
   - **Menu carta:** A4 (210×297mm), 300dpi, CMYK
   - **Menu digitale:** 1080×1920px per IG story, oppure PDF
   - **Volantino:** A5 (148×210mm) o DL (99×210mm), fronte+retro
   - **QR code tavolo:** 60×60mm, SVG vettoriale
   - **Insegna/banner:** dimensioni custom, vettoriale
2. Usa la palette GROOT (dal brandbook se disponibile, altrimenti chiedi)
3. Font: titolo bold leggibile da lontano, corpo min 10pt
4. Crea la grafica e salva in `<HERMES_ROOT>/shared/assets/`
5. Notifica GROOT (trigger P06) per revisione

**Esempio messaggio ricevuto:**
```
[FROM:GROOT] Mi serve un volantino per la serata degustazione Barolo di sabato. Prezzo: €45 a persona. Menu fisso 4 portate. Includi logo.
```

**Risposta attesa (P06):**
```
[FROM:DESIGNBRO] Grafica pronta: Volantino Degustazione Barolo, A5 fronte/retro, palette bordeaux/crema. File: <HERMES_ROOT>/shared/assets/volantino-barolo-2026.png. Pronta per revisione.
```

---

## Da altri bot

Se ricevi `[FROM:CONTABILE]`, `[FROM:LAWRENZO]`, `[FROM:EL-FROGGO]` direttamente:
- Logga il messaggio
- Se contiene una richiesta grafica, processala
- Altrimenti, ignora (non è competenza di DesignBro)

---

## Specifiche Tecniche Rapide

- **Post IG:** 1080×1080px, 72dpi, RGB
- **Story IG:** 1080×1920px, 72dpi, RGB
- **Carousel:** 1080×1080px × N, 72dpi, RGB
- **Facebook:** 1200×630px, 72dpi, RGB
- **Menu A4:** 210×297mm, 300dpi, CMYK
- **Volantino A5:** 148×210mm, 300dpi, CMYK
- **QR code:** 60×60mm, vettoriale

## Regole

- Mai produrre grafiche senza brief chiaro — chiedi sempre se ambiguo
- Rispondi SEMPRE con `[FROM:DESIGNBRO]` + descrizione + path file
- Mantieni lo stile coerente con il brand del richiedente
- File sempre in `<HERMES_ROOT>/shared/assets/`
- Naming: `{tipo}-{argomento}-{anno}.png`
