# Ribbit Capital "Token Letter" Style — Content Framework

## Source Inspiration
Ribbit Capital's "Token Letter" (June 2025) — 41-page investor letter framing tokens as the fundamental unit of the future economy. Style adopted for HermesBro LinkedIn content (June 2026).

## Key Style Elements

### 1. Bold, Provocative Openings
Start with a statement that challenges conventional thinking. NOT a question — a declaration.

❌ "Hai mai pensato di automatizzare il tuo business?"
✅ "L'ultimo dipendente che hai assunto ha fatto colloqui, ha firmato un contratto, ha fatto un periodo di prova."

❌ "Come migliorare la tua presenza sui social?"
✅ "Perché un bot che fa tutto non funziona mai."

### 2. Data-Driven Specificity
Use concrete numbers, not vague claims.

❌ "Risparmia tempo e denaro"
✅ "15+ ore a settimana recuperate. ROI raggiunto in 3 settimane."

❌ "Costa meno di un consulente"
✅ "Team tradizionale: €900-1.700/mese. Team AI: €50-120/mese."

### 3. Conceptual Framing
Frame HermesBro not as "bots" but as a new category:
- "Agenti specializzati" (not "bot")
- "Team digitale" (not "chatbot")
- "Dipendenti digitali" (not "AI tools")
- "Identità digitale" (not "NFT")

### 4. Series Format
Structure content as multi-part series (7-post series works well):
1. Introduction — the big idea
2. Problem — why current solutions fail
3. Mechanism — how it works
4. Proof — case study with numbers
5. Differentiation — what makes us unique
6. Economics — cost comparison
7. Manifesto — visionary closing

### 5. Narrative Arc
Each post builds on the previous:
- Post 1: "Here's a new category" → Post 2: "Why old approaches fail"
- Post 3: "The hidden cost" → Post 4: "Real results"
- Post 5: "Our unique approach" → Post 6: "The economics"
- Post 7: "The vision"

### 6. Provocative Contrasts
Use before/after, old/new, traditional/revolutionary contrasts:

"Prima, avere un team del genere costava €10.000-20.000 all'anno. Oggi costa €50-120 al mese."

"Non perché il lavoro vale meno. Ma perché la tecnologia ha abbattuto il costo dell'intelligenza specializzata."

### 7. Visionary but Grounded
End with big vision, but ground it in reality:

"Il bot del futuro non è un lusso. È un diritto."
"E il futuro è già qui."

## Post Structure Template

```
[PROVOCATIVE OPENING STATEMENT]

[CONTEXT/PROBLEM]

[DATA/NUMBERS]

[SOLUTION/INSIGHT]

[CONTRAST: OLD vs NEW]

[CALL TO ACTION]

[SERIES TEASER: "Prossimo post: ..."]

→ hermesbro.cloud
→ @<USER> su Telegram

#[HASHTAGS]
```

## Hashtag Strategy
- Max 5 hashtags per post
- Mix: 2 branded (#HermesBro #AIAgents) + 2-3 industry (#Automazione #PMI #Innovazione)
- Italian hashtags for Italian audience

## Character Count
- Target: 800-1200 characters
- Hook in first 2 lines (before "see more" fold on LinkedIn)
- Break text with line spacing for readability

## What NOT to Do
- ❌ Questions as openings (use declarations)
- ❌ Vague claims ("risparmia tempo")
- ❌ Generic AI buzzwords ("rivoluzione", "futuro")
- ❌ Lists without context
- ❌ CTA without prior value delivery
- ❌ Emoji overload (use sparingly, max 3-4 per post)

## Example Series Created (June 2026)
7-post series in `<HERMES_ROOT>/shared/marketing/linkedin/post-ribbit-*.txt`:
1. post-ribbit-1.txt — "L'ultimo dipendente che hai assunto..."
2. post-ribbit-2.txt — "Perché un bot che fa tutto non funziona mai"
3. post-ribbit-3.txt — "Il costo nascosto dei task ripetitivi"
4. post-ribbit-4.txt — "Come un ristorante ha recuperato 15 ore"
5. post-ribbit-5.txt — "L'identità digitale dell'agente"
6. post-ribbit-6.txt — "Quanto costa un team AI?"
7. post-ribbit-7.txt — "Il manifesto — 7 agenti, una missione"

## Cron Configuration
- Schedule: `0 9,12,18 * * *` (3 posts/day at 09:00, 12:00, 18:00)
- Profile: `wannabe` (Media Manager)
- Deliver: `telegram:<ADMIN_CHAT_ID>:32638`
- Mode: Agent-driven (no_agent=false) — reads source material, generates original post, publishes via `linkedin.py post-file`, updates rotation state
- Source material: `<HERMES_ROOT>/shared/marketing/linkedin/ribbit-token-letter.txt` (136K chars, extracted from Ribbit Capital PDF)
- Rotation state: `<HERMES_ROOT>/shared/marketing/linkedin/rotation-state.json`
- Cron job ID: `bff03691e0e2` (verify with `cronjob list`)

## 10 Thematic Pillars (from Token Letter)
The recurring calendar rotates through these 10 themes, each with 3 sub-angles (30 unique variations before repeating):

0. **Token Factory** — Every business becomes a token factory. HermesBro is a token factory for PMI.
1. **Memory Tokens** — Memory shared with agents is your most valuable digital asset. HermesBro bots learn from your business.
2. **Identity / KYA** — Know Your Agent: knowing WHO is working for you. Each HermesBro bot has clear identity, role, responsibilities.
3. **Tokenizers** — Simple apps will be AI's killer apps. ContAIbile tokenizes invoices. LAWrenzo tokenizes contracts.
4. **Vertical Token Platforms** — Vertical systems will replace SaaS and BPO. HermesBro is the AI operating system for Italian PMI.
5. **Agent Economy** — Everyone will have dozens of agents. HermesBro gives you your AI team today.
6. **Data Flywheels** — Moats are built on token and trust flywheels. HermesBro bots improve daily from your usage.
7. **Stablecoins Prototype** — Programmable money was just the prototype. HermesBro automates payments, invoices, financial flows.
8. **Financial Advisors** — Everyone will have an AI financial advisor. ContAIbile is already your AI accountant.
9. **Expert Tokens** — Human expertise encoded in reusable tokens. LAWrenzo encodes legal knowledge. ContAIbile encodes fiscal knowledge.

Sub-angles per theme: (a) General vision — Ribbit thesis applied, (b) Concrete problem — cost of NOT having these agents, (c) Story/example — real scenario of an entrepreneur using HermesBro
