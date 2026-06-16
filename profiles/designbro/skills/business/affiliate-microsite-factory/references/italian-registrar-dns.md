# Italian Registrar DNS Configuration — Step-by-Step for [REDACTED — dati personali rimossi]

## Register.it DNS Setup

Give these EXACT steps to [REDACTED — dati personali rimossi] when he needs to point a domain to the VPS (194.146.12.219):

### Steps (copy-paste to [REDACTED — dati personali rimossi]):

1. Vai su https://www.register.it
2. Accedi (Login in alto a destra)
3. Clicca su **"I miei servizi"** o **"Domini"**
4. Clicca sul dominio che vuoi configurare
5. Cerca **"Gestione DNS"** o **"Configurazione DNS"** o **"Zona DNS"**
6. Aggiungi questi record:

**Record A (obbligatorio):**
- Tipo: **A**
- Nome: **@** (oppure lascia vuoto)
- Valore: **194.146.12.219**
- TTL: 3600

**Record CNAME per www (USE CNAME, NOT A):**
- Tipo: **CNAME**
- Nome: **www**
- Valore: **<domain>.it** (es. foodcostitalia.it)
- TTL: 3600

⚠️ **Register.it quirk:** L'A record per "www" viene spesso rifiutato come "valore non valido". Usa SEMPRE CNAME per il www.

7. Salva

**Dopo 5-30 minuti** la propagazione DNS è completa. Poi dimmi "fatto" e configuro SSL.

### ⚠️ Register.it Gotchas (learned 2026-06-01)

1. **Default A record exists**: Register.it crea automaticamente un A record che punta a `195.110.124.133` (la loro pagina parcheggia). Devi **MODIFICARE** quel record, non aggiungerne uno nuovo. Se aggiungi un secondo A record con @, confligge.
2. **www come A record non funziona**: L'interfaccia rifiuta A record con nome "www". Soluzione: usa CNAME www → dominio.it.
3. **TTL field**: Se vedi un campo TTL, metti 3600.
4. **"Modifica zona DNS"**: Il percorso esatto è: Login → I miei domini → [click dominio] → "Modifica zona DNS" (NON "Configurazione DNS").
5. **DNS propagation lenta per .it**: I domini .it possono richiedere fino a 1-2 ore. I .com si propagano in 5-15 minuti. Verifica sempre con `dig`.
6. **Se il click su "Aggiungi" non carica**: Prova browser diverso, modalità incognito, o disabilita ad-blocker.

### If [REDACTED — dati personali rimossi] says "non trovo":

- Register.it ha un'interfaccia diversa per account vecchi/nuovi
- Chiedi uno screenshot
- In alternativa: cerca "DNS" nella barra di ricerca del pannello
- Alcuni piani hanno la gestione DNS sotto "Avanzate" o "Strumenti"

### Troubleshooting:

- **"Impossibile salvare"** → il dominio potrebbe essere in stato "in attesa di attivazione" dopo la registrazione. Aspetta 5-10 minuti.
- **Record A già esistente** → modifica quello esistente, non crearne uno nuovo
- **www già ha un CNAME** → cancella il CNAME e crea un A record

## Google Search Console TXT Verification

When Google asks for domain verification via TXT record:

1. Google shows a TXT value like `google-site-verification=ABC123...`
2. Don't close the Google page
3. Go to Register.it → Modifica zona DNS
4. Click **Aggiungi** → tipo **TXT** → nome **@** → valore: paste the full string → TTL 3600 → Salva
5. Wait 5-15 min → click **Verifica** on Google Search Console
6. After verification → submit sitemap: `https://domain.it/sitemap.xml`

**Pitfall:** Register.it already has an SPF TXT record (`v=spf1 ...`). Don't delete it — the verification TXT is a separate record.

## Aruba.it DNS Setup

Se [REDACTED — dati personali rimossi] usa Aruba:

1. Login su https://admin.aruba.it
2. Menu: **"Domini e Hosting"** → **"Gestione DNS"**
3. Seleziona il dominio
4. Modifica zona DNS
5. Aggiungi record A (come sopra)

## Verification

Dopo che [REDACTED — dati personali rimossi] dice "fatto":

```bash
# Check DNS propagation
dig +short <domain>.it A
dig +short www.<domain>.it A

# Should return: 194.146.12.219
```

Se non risponde ancora → "Aspetta altri 15 minuti, la propagazione DNS può essere lenta."

## SSL Setup (dopo verifica DNS)

```bash
# Install certbot if not present
apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d <domain>.it -d www.<domain>.it --non-interactive --agree-tos -m admin@hermesbro.cloud

# Verify
curl -sI https://<domain>.it | head -5
```

**Pitfall**: certbot fails if DNS isn't pointing yet. Always verify with `dig` first.
