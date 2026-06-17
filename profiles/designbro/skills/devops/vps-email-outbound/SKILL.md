---
name: vps-email-outbound
description: "Set up Postfix + OpenDKIM on a VPS for outbound cold email campaigns. Covers SMTP config, DKIM signing, SPF DNS records, deliverability, and sending scripts with rate limiting."
version: 1.0.0
author: gribbito
license: MIT
metadata:
  hermes:
    tags: [email, postfix, opendkim, outbound, cold-email, smtp]
    related_skills: [vps-security-hardening, marketing-materials-workflow]
---

# VPS Email Outbound Infrastructure

## When to use this skill

- Setting up outbound cold email from a VPS
- Configuring Postfix as a sending MTA
- Adding DKIM signing for deliverability
- Troubleshooting email bounces (SPF/DKIM/SMTPUTF8)
- Building rate-limited email sending scripts

## Architecture

```
Script (Python) → sendmail → Postfix → OpenDKIM (sign) → Recipient MX
                                                              ↓
                                          SPF check ← DNS TXT record
                                          DKIM check ← DKIM header
```

## Step-by-step setup

### 1. Configure Postfix

```bash
# Set domain identity
postconf -e "myhostname = mail.DOMAIN"
postconf -e "myorigin = DOMAIN"
postconf -e "mydestination = DOMAIN, mail.DOMAIN, localhost"
postconf -e "inet_interfaces = all"
postconf -e "smtp_tls_security_level = may"
postconf -e "smtpd_tls_security_level = may"

# Set mailname
echo "DOMAIN" > /etc/mailname

# Restart
systemctl restart postfix
```

### 2. Install and configure OpenDKIM

```bash
apt-get install -y opendkim opendkim-tools

# Generate DKIM keys
mkdir -p /etc/opendkim/keys/DOMAIN
opendkim-genkey -b 2048 -d DOMAIN -D /etc/opendkim/keys/DOMAIN -s mail -v
chown -R opendkim:opendkim /etc/opendkim
chmod 600 /etc/opendkim/keys/DOMAIN/mail.private
```

Create `/etc/opendkim.conf`:
```
AutoRestart            Yes
AutoRestartRate        10/1h
Syslog                 yes
SyslogSuccess          Yes
LogWhy                 Yes
Canonicalization       relaxed/simple
ExternalIgnoreList     refile:/etc/opendkim/TrustedHosts
InternalHosts          refile:/etc/opendkim/TrustedHosts
KeyTable               refile:/etc/opendkim/KeyTable
SigningTable           refile:/etc/opendkim/SigningTable
Mode                   sv
PidFile                /run/opendkim/opendkim.pid
SignatureAlgorithm     rsa-sha256
UserID                 opendkim:opendkim
Socket                 inet:8891@localhost
```

Create key/signing/trusted files:
```bash
# /etc/opendkim/KeyTable
mail._domainkey.DOMAIN DOMAIN:mail:/etc/opendkim/keys/DOMAIN/mail.private

# /etc/opendkim/SigningTable
*@DOMAIN mail._domainkey.DOMAIN

# /etc/opendkim/TrustedHosts
127.0.0.1
localhost
DOMAIN
```

Connect to Postfix:
```bash
postconf -e "milter_default_action = accept"
postconf -e "milter_protocol = 6"
postconf -e "smtpd_milters = inet:localhost:8891"
postconf -e "non_smtpd_milters = inet:localhost:8891"

systemctl restart opendkim && systemctl restart postfix
```

### 3. DNS Records (required for deliverability)

**SPF** (TXT on domain):
```
v=spf1 ip4:SERVER_IP ip6:SERVER_IPv6 ~all
```

**DKIM** (TXT on `mail._domainkey.DOMAIN`):
Content from `/etc/opendkim/keys/DOMAIN/mail.txt`

**DMARC** (TXT on `_dmarc.DOMAIN`):
```
v=DMARC1; p=quarantine; rua=mailto:postmaster@DOMAIN
```

### 4. Test

```bash
# Send test email
echo "Test body" | mail -s "Test Subject" -r "sender@DOMAIN" recipient@example.com

# Check logs
tail -f /var/log/mail.log | grep -E "status=|DKIM"

# Expected: DKIM-Signature field added, status=sent
```

## Pitfalls

### FROM address must match authenticated domain
The `-r sender@DOMAIN` address MUST use the domain that has SPF+DKIM configured. Sending from a Gmail/external address through your VPS Postfix will ALWAYS be rejected — Gmail checks that the sender domain matches the sending infrastructure.

**Wrong:** `echo "test" | mail -s "test" -r "user@gmail.com" dest@example.com` → `550-5.7.26 SPF did not pass`
**Right:** `echo "test" | mail -s "test" -r "user@hermesbro.cloud" dest@example.com` → `status=sent`

Verified 2026-06-06: Postfix + OpenDKIM on YOUR_VPS_ID sends to Gmail successfully when FROM uses `@hermesbro.cloud`.

### Gmail blocks without SPF+DKIM
Gmail rejects unauthenticated email with `550-5.7.26`. MUST have both SPF TXT record AND DKIM signing. SPF alone is not enough.

### SMTPUTF8 bounce
If email body or recipient contains non-ASCII characters (accents, etc.) and the receiving MX doesn't support SMTPUTF8, the email bounces. **Fix:** Always lowercase email addresses, avoid non-ASCII in headers.

### ProtonMail/Resend/SendGrid signup CAPTCHAs
All major email services block automated account creation with Cloudflare Turnstile or reCAPTCHA. User must create accounts manually. Don't waste time trying to automate — direct the user to do it.

### VPS IP reputation
Contabo/cheap VPS IPs can have mixed reputation. However, with proper SPF+DKIM+DMARC setup, deliverability to Gmail and major providers works well (verified on YOUR_VPS_ID with Aruba IP). Monitor bounces. If deliverability drops below 90%, consider a relay service (SendGrid/Mailgun SMTP relay).

### Rate limiting for cold email
Send max 20-50 emails per day from a new IP. Warm up over 2-4 weeks. Space emails 30+ seconds apart. Too fast = spam flag.

## Sending Script Pattern

```python
# Key features:
# - Rate limiting (DELAY_SECONDS between emails)
# - Deduplication (sent.json tracks who was contacted)
# - Batch size control (BATCH_SIZE per run)
# - Template per sector
# - Lowercase all emails
# - sendmail via subprocess
```

See `scripts/send_campaign.py` for the basic implementation.
See `references/outreach-engine.md` for the production outreach engine with sequences, tracking, and cron automation.

### Gmail API / OAuth2 for sending

Gmail API **does NOT accept API keys** for sending or reading email. It requires OAuth2 with user consent. Error: `"API keys are not supported by this API. Expected OAuth2 access token"`.

Google also rejects raw IP addresses as OAuth redirect URIs — the redirect must use a domain with a valid TLD (`.com`, `.org`, etc.). For VPS-based OAuth flows, set up an nginx proxy callback:
1. Add `location /oauth/callback { proxy_pass http://127.0.0.1:9876/callback; }` to your site's nginx config
2. Run a temporary Python HTTP server on port 9876 to capture the code
3. Use `https://yourdomain.com/oauth/callback` as the redirect URI in Google Cloud Console

For simple email sending from a VPS, Postfix + DKIM is simpler and cheaper than OAuth2. Reserve Gmail OAuth for reading user mailboxes.

See `references/gmail-oauth2-callback.md` for the full VPS-based OAuth2 flow with nginx proxy callback.

## Verification

```bash
# Check Postfix running
systemctl is-active postfix

# Check OpenDKIM running
systemctl is-active opendkim

# Check DKIM signing in logs
grep "DKIM-Signature field added" /var/log/mail.log | tail -3

# Check email delivery
grep "status=sent" /var/log/mail.log | tail -5
```

## Related skills

- `vps-security-hardening`: SSH and firewall config
- `marketing-materials-workflow`: Email templates and campaign copy
- `himalaya`: IMAP/SMTP client for reading email (not sending campaigns)
