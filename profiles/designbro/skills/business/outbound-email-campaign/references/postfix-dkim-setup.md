# Postfix + OpenDKIM Setup for VPS Email Sending

Tested on YOUR_VPS_ID (Contabo, Ubuntu 24.04). Domain: hermesbro.cloud.

## 1. Configure Postfix

```bash
postconf -e "myhostname = mail.hermesbro.cloud"
postconf -e "myorigin = hermesbro.cloud"
postconf -e "mydestination = hermesbro.cloud, mail.hermesbro.cloud, localhost.localdomain, localhost"
postconf -e "inet_interfaces = all"
postconf -e "smtp_tls_security_level = may"
echo "hermesbro.cloud" > /etc/mailname
systemctl restart postfix
```

## 2. Install & Configure OpenDKIM

```bash
apt-get install -y opendkim opendkim-tools

# Generate 2048-bit DKIM key
mkdir -p /etc/opendkim/keys/hermesbro.cloud
opendkim-genkey -b 2048 -d hermesbro.cloud -D /etc/opendkim/keys/hermesbro.cloud -s mail -v
chown -R opendkim:opendkim /etc/opendkim
chmod 600 /etc/opendkim/keys/hermesbro.cloud/mail.private
```

### /etc/opendkim.conf
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

### /etc/opendkim/KeyTable
```
mail._domainkey.hermesbro.cloud hermesbro.cloud:mail:/etc/opendkim/keys/hermesbro.cloud/mail.private
```

### /etc/opendkim/SigningTable
```
*@hermesbro.cloud mail._domainkey.hermesbro.cloud
```

### /etc/opendkim/TrustedHosts
```
127.0.0.1
localhost
hermesbro.cloud
```

## 3. Wire Postfix to OpenDKIM

```bash
postconf -e "milter_default_action = accept"
postconf -e "milter_protocol = 6"
postconf -e "smtpd_milters = inet:localhost:8891"
postconf -e "non_smtpd_milters = inet:localhost:8891"
systemctl restart opendkim && systemctl restart postfix
```

## 4. DNS Records (on registrar — Register.it for hermesbro.cloud)

### SPF (TXT on @)
```
v=spf1 ip4:194.146.12.219 ip6:2a02:c207:2330:5875::1 ~all
```

### DKIM (TXT on mail._domainkey)
Get from: `cat /etc/opendkim/keys/hermesbro.cloud/mail.txt`

### DMARC (TXT on _dmarc)
```
v=DMARC1; p=none; rua=mailto:dmarc@hermesbro.cloud
```

## 5. Test

```bash
echo "Test body" | mail -s "Test Subject" -r "[REDACTED — dati personali rimossi]@hermesbro.cloud" recipient@example.com
sleep 5
tail -10 /var/log/mail.log | grep -E "DKIM|status="
# Expected: "DKIM-Signature field added" + "status=sent"
```

## VPS-specific notes

- Contabo VPS defaults to IPv6 for SMTP. If delivery fails, force IPv4: `postconf -e "inet_protocols = ipv4"`
- Port 25 is open on this VPS (verified)
- Reverse DNS (PTR) should match `mail.hermesbro.cloud` — set via Contabo panel
- Without SPF, Gmail rejects with `550-5.7.26`. Other providers (ProtonMail, Outlook, custom domains) may accept.
