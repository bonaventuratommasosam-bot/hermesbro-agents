# HermesBro Brand Specification

## Brand Identity
- **Nome:** HermesBro (Hermes bianco + Bro gold)
- **Tagline:** "Il tuo wingman AI per il business"
- **Voice:** Direct, Capable, Loyal, Human — italiano con inserti tech inglesi
- **Tono:** "tu" mai "voi", no filler, no corporate

## Palette
| Name       | Hex       | Usage                          |
|------------|-----------|--------------------------------|
| Ink        | `#0a0a0f` | Sfondo principale, testo       |
| Ink Soft   | `#18181b` | Card, superfici elevate        |
| Gold       | `#d4a853` | Accento, "Bro", CTA primarie   |
| Gold Dark  | `#b8922e` | Gold su sfondo chiaro          |
| Trust Blue | `#2563eb` | Link, azioni, interattività    |
| Surface    | `#fafaf9` | Sfondo chiaro                  |
| Muted      | `#71717a` | Testo secondario, label        |

### Regole colore
- **Gold = sale, non protagonista.** Max 15% della superficie. Mai come background di sezioni.
- **Trust Blue** solo per azioni (link, bottoni), mai per testo decorativo.
- **Dark theme è default.** Light è variante.

## Typography
- **Display/Heading:** Inter (300–900)
- **Mono/Code:** JetBrains Mono (400–600)
- **Regola:** Mai mescolare Inter e JetBrains Mono nello stesso elemento.

## Logo SVG
- Ali stilizzate di Hermes + caduceo
- 3 varianti: gold (dark bg), white (dark bg), dark-gold (light bg)
- Files: `/root/hermesbro-logo-gold.svg`, `-white.svg`, `-light.svg`
- Animazione: draw-in su stroke (dasharray/dashoffset)

## Prodotti
| Bot          | Settore      | Icona | Descrizione                          |
|--------------|--------------|-------|--------------------------------------|
| Ratatouille  | Ristorazione | 🐀    | Food cost, scorte, report vendite    |
| ContAIbile   | Contabilità  | 📊    | Fatture, bilancio, IVA, crypto       |
| LAWrenzo     | Legale       | ⚖️    | NDA, contratti, privacy              |
| Wannabe      | Social Media | 📱    | Scheduling, analytics, contenuti     |
| DesignBro    | Design       | 🎨    | Grafica, brand kit, mockup           |

## Do / Don't
- ✓ Usa "tu" sempre
- ✓ Italiano diretto con termini tech inglesi
- ✓ Messaggi brevi (max 2 righe)
- ✓ Emoji con moderazione (1-2 max)
- ✗ Mai "Gentile cliente" o tono call center
- ✗ Mai gold come background pieno
- ✗ Mai più di 2 font nella stessa composizione
- ✗ Mai "siamo lieti di" / "la ringraziamo"

## File Locations
- Brand system HTML: `/root/hermesbro-brand.html`
- Marketing: `<HERMES_ROOT>/shared/marketing/`
- LinkedIn: `<HERMES_ROOT>/shared/marketing/linkedin/`