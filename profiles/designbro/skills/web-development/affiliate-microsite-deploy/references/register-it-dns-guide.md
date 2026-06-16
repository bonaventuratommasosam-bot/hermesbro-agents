# Register.it DNS Configuration Guide

## Accessing DNS Zone Editor

1. Login at https://www.register.it
2. "I miei domini" → click domain
3. "Configura i DNS" → "Modifica zona DNS"

## Adding/Editing Records

### Common Pitfalls

- **Don't add a new A record if one already exists** — edit the existing one. Duplicate A records cause issues.
- **www as CNAME, not A** — Register.it rejects `www` as A record name. Use CNAME: `www` → `domain.tld`
- **New domains may have no active DNS zone** — first enable "Usa i DNS di Register.it" under DNS config, then edit zone
- **TTL field**: use 3600 (1 hour) for changes you might need to revert, 900 for faster propagation
- **Save button**: changes are NOT applied until you explicitly save/confirm
- **TXT records for verification**: Add as SEPARATE records. Don't delete existing SPF TXT. Google Search Console TXT goes alongside SPF.
- **Modifica zona DNS** — exact path: Login → I miei domini → [click dominio] → "Modifica zona DNS" (NOT "Configurazione DNS")

### Default Records to Clean Up

New .it domains come with:
- MX record pointing to `mail.register.it` — delete if not using Register.it email
- TXT SPF record — can keep or delete
- SRV `_autodiscover._tcp` — delete if not using their email

### Verification

```bash
# Check if changes propagated (use Register.it NS directly for instant check)
dig +short DOMAIN A @ns1.register.it

# Check global propagation (may take 15-60 min for .it)
dig +short DOMAIN A @8.8.8.8
```

## .it Domain Registration

- Cost: ~€6-10/year
- Category "Privato" is fine for individuals without P.IVA
- WHOIS check: `whois domain.it` → "Status: AVAILABLE" means registerable
- Grace period: expired .it domains may take time to become available

## Expired .it Domain Research

- https://www.seoprof.it/domini-scaduti/ — Italian expired domains with OpenRank metric
- Filter by keyword (ristorante, food, cucina, etc.) or by length
- OpenRank 20+ = has some SEO value
- Always verify with `whois DOMAIN.it` before assuming availability
