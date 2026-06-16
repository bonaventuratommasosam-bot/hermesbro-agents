# Gmail OAuth2 via VPS — Nginx Callback Pattern

## When to use
When you need OAuth2 access to a user's Gmail (read or send) and the app runs on a VPS with a domain.

## Problem
Google rejects raw IP addresses as OAuth redirect URIs:
> "l'URI doit se terminer par une extension de domaine public de premier niveau, telle que .com ou .org"

Google also deprecated `urn:ietf:wg:oauth:2.0:oob` (the "copy-paste code" flow) for most app types.

## Solution: Nginx proxy callback

### 1. Add nginx location block
```nginx
# In the existing HTTPS server block for your domain
location /oauth/callback {
    proxy_pass http://127.0.0.1:9876/callback;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```
Then `nginx -t && systemctl reload nginx`.

### 2. Run temporary Python callback server
```python
#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        code = qs.get("code", [None])[0]
        if code:
            with open("/tmp/oauth-code.txt", "w") as f:
                f.write(code)
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>OK! Puoi chiudere questa pagina.</h1>")
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code found")

HTTPServer(("0.0.0.0", 9876), Handler).handle_request()
```

### 3. Add redirect URI in Google Cloud Console
- Go to https://console.cloud.google.com/apis/credentials
- Open your OAuth 2.0 Client ID
- Add `https://yourdomain.com/oauth/callback` to "Authorized redirect URIs"
- Save

### 4. Generate auth URL and exchange code
```python
from urllib.parse import urlencode

params = {
    'client_id': 'YOUR_CLIENT_ID',
    'redirect_uri': 'https://yourdomain.com/oauth/callback',
    'scope': 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send',
    'response_type': 'code',
    'access_type': 'offline',  # gets refresh_token
    'prompt': 'consent'        # forces refresh_token on repeat
}
auth_url = 'https://accounts.google.com/o/oauth2/auth?' + urlencode(params)
# User opens this, grants access, server captures code automatically

# Exchange code for tokens:
import requests
r = requests.post('https://oauth2.googleapis.com/token', data={
    'code': auth_code,
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'redirect_uri': 'https://yourdomain.com/oauth/callback',
    'grant_type': 'authorization_code'
})
tokens = r.json()
# tokens['refresh_token'] — save this, it's long-lived
# tokens['access_token'] — expires in 1 hour
```

### 5. Refresh access token (for ongoing use)
```python
r = requests.post('https://oauth2.googleapis.com/token', data={
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'refresh_token': REFRESH_TOKEN,
    'grant_type': 'refresh_token'
})
access_token = r.json()['access_token']
```

## Pitfalls
- **Two different client IDs in same project** can have different secrets. Always match the correct secret to the correct client ID.
- **API keys don't work for Gmail** — always returns 401 "API keys are not supported by this API".
- **Code is single-use** — if you exchange it once (even with the wrong secret), you need a fresh code.
- **`prompt=consent`** is needed to get a refresh_token on repeated authorizations. Without it, Google only returns the refresh_token on the first consent.
- **refresh_token expires in 7 days** for apps in "Testing" mode. Publish the app to make refresh tokens long-lived.

## Minimal Gmail API test
```python
r = requests.get(
    'https://gmail.googleapis.com/gmail/v1/users/me/profile',
    headers={'Authorization': f'Bearer {access_token}'}
)
print(r.json())  # Should show emailAddress, messagesTotal, etc.
```
