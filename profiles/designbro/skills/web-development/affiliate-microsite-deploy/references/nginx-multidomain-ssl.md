# Nginx Multi-Domain SSL Pattern

When serving multiple domains (e.g., .it primary + .com redirect) with separate SSL certs.

## Problem

Certbot's `--nginx` flag modifies the config to use ONE cert for all server_name entries.
If you run certbot separately for each domain, it creates conflicting configs.

## Solution

After running certbot for each domain, manually write separate server blocks:

```nginx
# HTTP → HTTPS redirect (all domains)
server {
    listen 80;
    server_name domain.it www.domain.it domain.com www.domain.com;
    return 301 https://$host$request_uri;
}

# Primary domain (.it) — serves content
server {
    listen 443 ssl;
    server_name domain.it www.domain.it;
    ssl_certificate /etc/letsencrypt/live/domain.it/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/domain.it/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    root /var/www/SITE;
    # ... rest of config
}

# Redirect domain (.com) → primary (.it)
server {
    listen 443 ssl;
    server_name domain.com www.domain.com;
    ssl_certificate /etc/letsencrypt/live/domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/domain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    return 301 https://domain.it$request_uri;
}
```

## Verification

```bash
nginx -t && systemctl reload nginx
curl -sk -o /dev/null -w "%{http_code}" https://domain.it/    # should be 200
curl -sk -o /dev/null -w "%{http_code}" https://domain.com/   # should be 301
```

## SSL Certificate Renewal

Certbot auto-renews. Check with: `certbot certificates`
