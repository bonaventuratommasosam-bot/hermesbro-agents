# Pre-Launch Content Strategy — LinkedIn Teaser Campaigns

## Context

When HermesBro (or any product) is not ready for public launch, LinkedIn content must build awareness without announcing availability. [REDACTED — dati personali rimossi] corrected this on 2026-06-01: the posts were too much "launch" content when the product wasn't ready.

## Rules

1. **NO product links** — hermesbro.cloud, pricing pages, sign-up forms
2. **NO pricing** — not even "€49/mese" or "14 giorni gratis"
3. **NO hard CTAs** — no "prova ora", "registrati", "contattaci"
4. **NO availability announcements** — no "è online", "è disponibile", "lanciamo"
5. **Focus on PROBLEMS** — tempo perso, costi nascosti, consulenze ripetitive
6. **Soft CTAs only** — "Presto vi mostreremo", "Segui questa pagina", "Sta per succedere qualcosa"
7. **Build curiosity** — reveal enough to interest, not enough to satisfy
8. **600-900 chars** — short, punchy, mobile-friendly (actual posts range 600-900)
9. **3-4 hashtags** — mix generic (#AI #PMI) + specific (#Automazione #Efficienza)
10. **No emoji** — serious, professional tone
11. **Cite credible sources** — reference thought leadership that inspired the vision. [REDACTED — dati personali rimossi] explicitly asked to mention external sources as inspiration (2026-06-01). Include source hashtag when referencing it.

## Post Structure (5-post teaser campaign with source citation)

| # | Day | Theme | Hook Pattern |
|---|-----|-------|--------------|
| 1 | Mon | Source Discovery | "Qualche mese fa ho letto una lettera di 41 pagine..." |
| 2 | Tue | Source Quote | Citazione diretta dalla fonte — commercialista, avvocato, social manager |
| 3 | Wed | Problem + ROI | "Quanto paghi ogni anno per consulenze..." + source reference |
| 4 | Thu | Philosophy | "L'AI non sostituisce le persone. Le libera." + source reference |
| 5 | Fri | Soft CTA | "Dietro ogni PMI che funziona..." + source vision |

## Source Citation Patterns

### Pattern 1: Letter/Report (e.g. Ribbit Capital Token Letter)

1. **Open with the discovery** — "Qualche mese fa ho letto una lettera di 41 pagine..."
2. **Name the source** — "Si chiama Token Letter. L'ha scritta Ribbit Capital."
3. **Quote or paraphrase the key insight** — "La tesi è semplice:..."
4. **Connect to the problem** — "Non parliamo di crypto. Parliamo di..."
5. **Tease the solution** — "Da quel giorno stiamo costruendo qualcosa."
6. **Include source hashtag** — #TokenLetter

### Pattern 2: Thread/Article (e.g. @gkisokay "21 mistakes")

1. **Open with the thread** — "Qualche giorno fa ho letto un thread che mi ha fatto sentire meno solo."
2. **Cite the lesson number** — "La lezione 12 del thread che ci ha ispirato:"
3. **Paraphrase the insight** — "Non usare modelli costosi per tutto."
4. **Connect to your approach** — "Noi facciamo esattamente così."
5. **Tease the solution** — "Stiamo costruendo qualcosa per chi gestisce un'attività."
6. **No hashtag for the thread** — just #AI #PMI etc.

**Why "lesson N" works**: It creates a series feel (readers want to see the other lessons), positions you as someone who learns from others (humble, credible), and lets you reference the source without quoting it verbatim (avoids copyright issues).

### Pattern 3: Mixed (Token Letter + Thread in same campaign)

When using multiple sources in a 5-post campaign:
- Posts 1-4: Reference the thread (lesson 1, 12, 17, 21)
- Post 5: Reference the letter (Token Letter)
- Each post stands alone but the campaign has a narrative arc

## Example — Post 1 (Thread Discovery)

```
Qualche giorno fa ho letto un thread che mi ha fatto sentire meno solo.

"21 painful mistakes I made building AI agents so you don't have to."

La prima lezione: non costruire un agente gigante.
Costruisci un team di specialisti.

È esattamente quello che stiamo facendo.
Non un chatbot che fa di tutto male.
Agenti che fanno ognuno una cosa — e la fanno bene.

Il contabile. Il legale. Il marketing. La segreteria.
Ognuno con il suo compito. Ognuno con la sua memoria.

Stiamo costruendo qualcosa per chi gestisce un'attività e non ha tempo.

Presto ve lo mostriamo.

#AI #PMI #Automazione #AIAgents
```

## Example — Post 2 (Lesson N Pattern)

```
La lezione 12 del thread che ci ha ispirato:

"Non usare modelli costosi per tutto."

Scansioni, riassunti, brainstorming → modelli locali, economici.
Pianificazione, debugging, ragionamento complesso → modelli frontier.

Noi facciamo esattamente così.
Il nostro team AI non costa come un dipendente.
Ma lavora 24/7, non si distrae, non sbaglia le cose ripetitive.

Un commercialista per le fatture base: €200-400/mese
Un consulente GDPR: €500-1500/anno
Un social media manager: €300-800/mese

Totale: €15.000-25.000 all'anno.

E se potessi avere tutto questo per una frazione del costo?

Non parliamo di risparmiare sulle persone.
Parliamo di dare alle persone il tempo di fare ciò che conta davvero.

#PMI #Risparmio #AI #CostOptimization
```

## Example — Post 5 (Token Letter)

```
La "Token Letter" di Ribbit Capital dice una cosa che ci ha cambiato il modo di pensare:

"Il tuo commercialista che registra una fattura? Tokenizza un flusso di cassa.
Il tuo avvocato che legge un contratto? Tokenizza un rischio.
Il tuo social media manager che pubblica un post? Tokenizza l'attenzione."

Ogni processo aziendale è un token di valore.
Prima lo facevano persone, in ore, con costi variabili.
Oggi possono farlo agenti specializzati, in secondi, con costi fissi.

Non parliamo di crypto o blockchain.
Parliamo di come il tuo business può diventare una "Token Factory".

Dietro ogni PMI che funziona c'è un proprietario che fa 10 cose diverse ogni giorno.
E nel frattempo? Il business non cresce. Sopravvive.

Stiamo costruendo qualcosa per chi vuole smettere di sopravvivere e iniziare a crescere.

Presto ve lo mostriamo.

#TokenLetter #PMI #AI #Crescita
```

## Reading External Content for Reference

When [REDACTED — dati personali rimossi] shares a tweet/thread URL to use as inspiration:

1. **FxTwitter API** (no auth needed): `curl -sL "https://api.fxtwitter.com/status/{tweet_id}"` — returns full article/thread JSON
2. **xurl CLI** (if auth configured): `xurl read {tweet_id}` — returns tweet JSON
3. **Extract key lessons** — don't quote the entire source, pick 1-2 insights per post
4. **Attribute properly** — name the author/source, but don't reproduce entire passages

**Pitfall**: FxTwitter returns article content as Draft.js blocks. Parse with:
```bash
curl -sL "https://api.fxtwitter.com/status/{tweet_id}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
article = data['tweet'].get('article', {})
for b in article.get('content', {}).get('blocks', []):
    if b['text'].strip():
        print(b['text'])
"
```

**Pitfall**: FxTwitter returns tweet metadata even for articles. Check `tweet.article.title` to distinguish articles from regular tweets. Articles have a `content.blocks` structure; regular tweets have just `text`.

## Validated Source Examples

### Source: Ribbit Capital "Token Letter" (June 2025)
- 41-page letter about tokenization of business processes
- Key thesis: every business process becomes a "token of value" when automated
- Used in Post 5 of the June 2026 teaser campaign
- Hashtag: #TokenLetter

### Source: @gkisokay "21 painful mistakes building AI agents" (May 2026)
- Thread/article: 172 likes, 467 bookmarks, 33k views
- 21 lessons from 3 months of building Hermes/OpenClaw agents
- Key lessons used in campaign:
  - Lesson 1: "Don't build one giant agent → build a crew of specialists"
  - Lesson 12: "Don't use frontier models for everything → save costs"
  - Lesson 17: "Don't think the model is the product → the system matters"
  - Lesson 21: "Don't be afraid to share what you're building → build in public"
- Used in Posts 1-4 of the June 2026 teaser campaign
- No hashtag for the thread (just generic #AI #PMI)

**Why this worked**: The thread validated HermesBro's architecture (multi-agent specialization) without [REDACTED — dati personali rimossi] needing to explain it directly. Citing it as inspiration built credibility while keeping the product under wraps.

## Scheduling Pattern

Same as launch posts — one-shot crons + pause recurring calendar:

1. Save posts to `<HERMES_ROOT>/shared/marketing/linkedin/post-*.txt`
2. Create one-shot crons (no_agent=True) at 09:00 daily
3. Pause `linkedin-content-calendar` for the campaign period
4. Create a one-shot cron to resume recurring calendar after campaign ends
5. **Include source hashtag** (#TokenLetter) in all posts that reference the source

## Transition to Launch

When [REDACTED — dati personali rimossi] says "siamo pronti" or "lanciamo":
1. Rewrite post files with launch content (link, pricing, CTA forte)
2. Update content calendar
3. Resume recurring calendar at full frequency (3x/day)
4. Remove source citation pattern (no longer needed — product is live)
