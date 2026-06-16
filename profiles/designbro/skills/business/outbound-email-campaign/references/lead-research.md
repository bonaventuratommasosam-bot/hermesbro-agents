# Lead Research Methodology

## Objective
Collect 200+ qualified leads (40 per sector) for outbound email campaign.

## Target sectors (example: HermesBots)
1. Ristoranti e attività di ristorazione
2. Studi legali e avvocati
3. E-commerce
4. Startup e tech
5. PMI generica (manifattura, servizi, consulenza)

## Method 1: Google Maps Scraping

**Tools:** Outscraper, PhantomBuster, Google Maps API, Apify

**Procedure:**
1. Search Google Maps by category + target city:
   - "ristorante" + Milano, Roma, Torino, Napoli, Bologna
   - "studio legale" + Milano, Roma, Torino, Napoli, Bologna
   - "e-commerce" (via Google reviews or categories)
2. Export: business name, address, phone, email, website, review count
3. Filter: at least 10+ reviews (active business), website present (has digital budget)
4. Target: 8 contacts per city × 5 cities = 40 per sector

**Quality criteria:**
- Has website (has digital budget)
- Recent reviews (active business)
- NOT large chains (unreachable decision-makers)

## Method 2: LinkedIn

**Tools:** LinkedIn Sales Navigator, Apollo.io, Hunter.io

**Procedure:**
1. Sales Navigator filters:
   - Title: "Proprietario", "CEO", "Fondatore", "Partner", "Direttore"
   - Industry: target sectors
   - Company size: 1-50 employees
   - Location: Italy
2. Collect: name, company, role, LinkedIn URL
3. Use Apollo.io or Hunter.io to find business email
4. Verify emails with NeverBounce or ZeroBounce

## Method 3: PagineGialle

**Tools:** Manual scraping, Octoparse, ParseHub

**Procedure:**
1. Go to paginegialle.it
2. Search by category in target cities
3. Extract: name, address, phone, email, website
4. Filter same as Google Maps

**Advantage:** PagineGialle often has direct email, which Google Maps doesn't always provide.

## Recommended workflow

1. **Week 1:** Google Maps for all 5 sectors (160 contacts)
2. **Week 2:** LinkedIn to supplement (40 premium contacts with direct decision-maker)
3. **Email verification:** All addresses verified before sending
4. **Cleanup:** Remove duplicates, closed businesses, contacts without email

## Tool recommendations

| Tool | Use | Cost |
|------|-----|------|
| Outscraper | Google Maps scraping | ~$10 per 1000 results |
| Apollo.io | Email finding + outreach | Free plan available |
| Hunter.io | Email verification | 25 searches/month free |
| NeverBounce | Email verification | ~$0.005/email |
| Google Sheets | Lead organization | Free |

## CSV format

```
nome,cognome,azienda,settore,email,telefono,sito_web,citta,fonte,stato
```

## Notes
- GDPR: include opt-out in every email
- Don't email contacts who already have a declared AI bot
- Prioritize those without visible chatbot on their website (greater need)
