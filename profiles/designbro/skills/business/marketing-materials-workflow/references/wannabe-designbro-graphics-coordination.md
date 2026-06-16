# Wannabe → DesignBro Graphics Coordination

## Overview

This document describes the workflow for Wannabe (Media Manager) to coordinate graphics production with DesignBro via the inter-bot message bus.

## Trigger

The `graphics-check` cron job runs periodically under the Wannabe profile. Its job is to:
1. Read the current month's content calendar
2. Identify posts needing graphics
3. Send briefs to DesignBro for any graphics not yet requested
4. Track what's been sent to avoid duplicates

## Content Calendar Parsing

The calendar lives at `<HERMES_ROOT>/shared/marketing/content-calendar-<month>-<year>.md`.

### Identifying Posts Needing Graphics

Look for posts with these **Formato** values:
- `Immagine` — Static graphic card
- `Infografica` — Data visualization, before/after, lists
- `Quote Card` — Avatar + quote overlay

Posts with these formats do NOT need graphics from DesignBro:
- `Testo` — Text-only post
- `Sondaggio` — LinkedIn native poll
- `Video` — Requires screen recording (manual task, not DesignBro)

### Asset Section

The calendar has an `## ASSET NECESSARI` section at the bottom listing all required assets:

```markdown
## ASSET NECESSARI

### Immagini/Infografiche (4)
- Post 2: Card El Froggo (bg #1a1a2e, icona 🐸, accent #ffd60a)
- Post 6: Split PRIMA/DOPO Wannabe (rosso → verde)
- Post 8: Case study before/after (#3a86ff + #ff006e)
- Post 12: Lista 5 attività automatizzabili (sfondo scuro)
```

Each entry includes:
- Post number and date
- Description of the visual
- Color palette / style notes

## Sending Briefs via Bus

### Command Pattern

```bash
python3 <HERMES_ROOT>/shared/scripts/bus-send.py send wannabe designbro "<brief_text>" design
```

### Brief Structure

A good brief includes:

1. **What**: Description of the graphic
2. **Format**: Dimensions (e.g., 1080×1080 LinkedIn)
3. **Style**: Visual style (dark tech, minimale, professionale)
4. **Colors**: Specific hex codes from brand palette
5. **Text**: Any text to include on the graphic
6. **Context**: Which post, what date
7. **Urgency**: When it's needed

### Example Brief

```
Brief grafico: Card El Froggo per post LinkedIn. Sfondo scuro #1a1a2e, icona rana 🐸 con occhi stile tech, accento giallo oro #ffd60a. Testo: 'El Froggo — Il bot dietro le quinte'. Stile: dark tech, minimale, professionale. Formato LinkedIn 1080x1080. Contesto: post showcase per bot integrazioni software Hermes Bots. Urgenza: pubblicazione Mer 3 Giugno 2026.
```

### Brief Timing

Send briefs **7-14 days** before the post publication date:
- 14 days: Complex infographics, case studies
- 10 days: Standard cards, quote cards
- 7 days: Simple graphics, lists

**Pitfall**: Don't send all briefs at once on the first cron run. Stagger them by urgency — send the most urgent first, let DesignBro batch the rest.

## Tracking Sent Briefs

### Graphics Tracker File

Create `<HERMES_ROOT>/shared/marketing/graphics-tracker.md` on first run if missing:

```markdown
# Graphics Tracker — <Month> <Year>

| Post | Data | Graphic | Status | Sent Date |
|------|------|---------|--------|-----------|
| #2 | Mer 3 Giugno | Card El Froggo | Sent | 2026-05-29 |
| #6 | Ven 12 Giugno | Infografica PRIMA/DOPO | Pending | — |
| #8 | Mer 17 Giugno | Case study before/after | Pending | — |
| #11 | Mer 24 Giugno | Quote card founder | Pending | — |
| #12 | Ven 26 Giugno | Lista 5 attività | Pending | — |
```

### Checking for Duplicates

Before sending a brief:
1. Check if `graphics-tracker.md` exists — if not, create it from the template
2. Read `graphics-tracker.md` — check if post already has "Sent" status
3. Check bus inbox: `ls <HERMES_ROOT>/shared/bus/inbox/designbro/` — look for messages with matching content
4. Only send if neither shows the brief was already sent

**Pitfall**: The `graphics-tracker.md` file is NOT auto-created. The cron job must create it on first run if missing. Use the template from `templates/graphics-tracker-giugno-2026.md` as a starting point, or generate from the content calendar's ASSET NECESSARI section.

**Pitfall**: The bus inbox may contain old processed messages. Check the `timestamp` field to distinguish recent from stale. If a message is >7 days old and `read: true`, DesignBro likely already processed it.

**Duplicate detection priority**: Bus inbox (ground truth) > graphics-tracker.md (may be stale) > calendar parsing (only identifies need, not status).

### Updating the Tracker

After sending a brief, update the tracker:
```bash
# Read current tracker
cat <HERMES_ROOT>/shared/marketing/graphics-tracker.md

# Update status (use patch tool or sed)
# Change "Pending" to "Sent" and add date
```

## Cron Job Configuration

### Job Name: `graphics-check`

**Schedule**: Runs weekly (e.g., every Monday at 08:00)
**Profile**: `wannabe`
**Deliver**: `telegram:<ADMIN_CHAT_ID>:31761`

**Prompt** (updated 2026-05-30):
```
You are Wannabe, the Media Manager. Check for content that needs graphics:

1. Read the content calendar: <HERMES_ROOT>/shared/marketing/content-calendar-<month>-<year>.md
2. Check if graphics-tracker.md exists — if not, create it from the template or generate from calendar's ASSET NECESSARI
3. Check graphics-tracker.md for already-sent briefs (status = "Sent")
4. Check bus inbox for any matching briefs: ls <HERMES_ROOT>/shared/bus/inbox/designbro/
5. For any post needing graphics that hasn't been sent:
   python3 <HERMES_ROOT>/shared/scripts/bus-send.py send wannabe designbro "<brief>" design
6. Update graphics-tracker.md with sent status and date
7. Report what was sent (or "no new graphics needed")

Only send if there are actual pending items. Italian language.
```

## Brand Palette Reference

| Bot | Primary | Hex |
|-----|---------|-----|
| ContAIbile | Blue | #3a86ff |
| LAWrenzo | Purple | #8338ec |
| GROOT | Green | #06d6a0 |
| Wannabe | Orange | #ff9f1c |
| DesignBro | Pink | #ff006e |
| El Froggo | Gold | #ffd60a |

**Background**: Dark #1a1a2e or #16213e
**Text**: White #ffffff or light gray #e0e0e0

## DesignBro's Response

When DesignBro completes a graphic, it sends back via bus:

```bash
python3 <HERMES_ROOT>/shared/scripts/bus-send.py send designbro wannabe "Design completato: <descrizione>, file: <path>. Pronta per pubblicazione." design
```

Wannabe should:
1. Check bus inbox for completed designs
2. Update graphics-tracker.md status to "Completed"
3. Notify [REDACTED — dati personali rimossi] that the graphic is ready for review/publishing

## Lessons Learned (2026-05-30)

### What Worked
- Bus inbox check correctly identified the already-sent brief for Post #2
- Brief format with 7 elements (what, format, style, colors, text, context, urgency) is comprehensive
- Staggering briefs by urgency prevents overwhelming DesignBro

### What Needs Improvement
- `graphics-tracker.md` doesn't exist by default — cron must create it
- No automated way to verify DesignBro received the brief (bus is fire-and-forget)
- Template should be updated as briefs are sent (not just a static starting point)

### Recommended Cron Improvements
1. Auto-create `graphics-tracker.md` if missing
2. Update tracker after each brief sent
3. Check for DesignBro responses (completed designs)
4. Report summary: "X briefs sent, Y pending, Z completed"
