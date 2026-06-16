# Google Search Console + Amazon Associates — Step-by-Step for [REDACTED — dati personali rimossi]

## Google Search Console TXT Verification

### What Google Shows You
Google will show a page with:
1. A dropdown to select verification method (choose **TXT record**)
2. A long string like `google-site-verification=Gq5wL5_USe6r-G9N_wHOzpPchO9VoltH_yAgWDk_Xx8`
3. Instructions in French/English/Italian (ignore them — follow these steps)

### Steps on Register.it
1. Open a new tab (keep Google page open!)
2. Go to https://www.register.it
3. Login (top right)
4. Click **"I miei servizi"** or **"Domini"**
5. Click your domain (e.g., foodcostitalia.it)
6. Click **"Modifica zona DNS"** (NOT "Configurazione DNS")
7. Find and click **"Aggiungi"** or **"Add record"** button
8. Fill in:
   - **Tipo:** TXT (from dropdown)
   - **Nome:** @ (or leave empty)
   - **Valore:** paste the full `google-site-verification=...` string
   - **TTL:** 3600
9. Click **"Salva"** or **"Conferma"**
10. Wait 5-15 minutes (TXT records propagate faster than A records)
11. Go back to Google page → click **"Verifica"** or **"Validate"**

### If Verification Fails
- Wait 30 more minutes (DNS propagation can be slow for .it)
- Check record was saved: `dig TXT domain.it @ns1.register.it`
- Make sure you didn't accidentally delete the existing SPF TXT record
- Try again — sometimes Google needs multiple attempts

### After Verification
1. Google Search Console dashboard → **Sitemap** (left menu)
2. Enter: `sitemap.xml` → click **Invia**
3. Wait 24-48 hours for Google to crawl
4. Check **Copertura** for indexing status

## Amazon Associates Registration

### Step 1: Register
1. Go to https://programma-affiliazione.amazon.it
2. Click **"Iscriviti gratuitamente"**
3. Login with Amazon account (or create one)
4. Fill in:
   - Sito web: `https://foodcostitalia.it` (or your domain)
   - Categoria: "Cucina e casa" or "Ristorazione"
   - Traffico: "SEO / contenuti editoriali"
5. Amazon reviews the site — needs real content (not placeholder)

### Step 2: Get Your ID
- After approval, Amazon assigns an **Associate ID** like `hermebro-21`
- Format: `name-21` (always ends with `-21`)
- Find it: Dashboard → "Link affiliati" or "Account settings"

### Step 3: Create Affiliate Links
- Search for a product on Amazon
- Click "Genera link affiliato" or use the SiteStripe toolbar
- URL format: `https://www.amazon.it/dp/ASIN?tag=hermebro-21`
- For search: `https://www.amazon.it/s?k=gestionale+pizzeria&tag=hermebro-21`

### Step 4: Update Site
Replace all `{{AFF_LINK_*}}` placeholders in your articles with real affiliate links.
All links MUST have: `rel="nofollow noopener sponsored"`

### If Rejected
Amazon rejects sites with:
- No real content (just placeholder text)
- No traffic (brand new domain)
- Offensive/illegal content

Fix: add 5+ real articles, wait 2 weeks for SEO, reapply.

## Timeline
1. Domain live + content ready → Register Amazon Associates
2. Amazon approves (1-7 days) → replace affiliate links
3. Google indexes (1-4 weeks) → traffic starts
4. First commission: usually 1-3 months after going live
