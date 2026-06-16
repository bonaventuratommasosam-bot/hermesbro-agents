# LinkedIn API Integration Reference

## Overview

LinkedIn API v2 integration for Hermes Bots. Enables automated posting to personal profile and company page.

## Files

- Script: `<HERMES_ROOT>/shared/linkedin/linkedin.py` (posting: auth, post, post-org, post-file, me)
- OAuth script: `<HERMES_ROOT>/shared/linkedin/linkedin-oauth.py` (auth URL generation, code exchange, profile fetch)
- Config: `<HERMES_ROOT>/shared/linkedin/config.env`
- Setup guide: `<HERMES_ROOT>/shared/linkedin/SETUP.md`
- Banner HTML: `<HERMES_ROOT>/shared/marketing/linkedin/banner.html` (1584×396)
- Logo HTML: `<HERMES_ROOT>/shared/marketing/linkedin/logo.html` (300×300)
- Banner PNG: `<HERMES_ROOT>/shared/marketing/linkedin/banner.png` (1584×396, Pillow-generated)
- Logo PNG: `<HERMES_ROOT>/shared/marketing/linkedin/logo.png` (800x800, Pillow-generated)
- Page setup doc: `<HERMES_ROOT>/shared/marketing/linkedin-page.md`

## OAuth 2.0 Flow

### Endpoints
- Authorization: `https://www.linkedin.com/oauth/v2/authorization`
- Token: `https://www.linkedin.com/oauth/v2/accessToken`
- Userinfo: `https://api.linkedin.com/v2/userinfo`
- Posts: `https://api.linkedin.com/v2/ugcPosts`

### Scopes (2026-05-29 verified)
- `openid` — OpenID Connect (**requires "Sign In with LinkedIn using OpenID Connect" product — self-serve, instant**)
- `profile` — Basic profile (requires same OIDC product)
- `email` — User email (requires same OIDC product)
- `w_member_social` — Post to personal profile (**WORKS IMMEDIATELY** with "Share on LinkedIn" product)
- `w_organization_social` — Post as company page (**RESTRICTED** — requires Marketing Developer Platform approval, days/weeks)

**Critical**: `openid` scope returns `unauthorized_scope_error` unless "Sign In with LinkedIn using OpenID Connect" product is added first. Self-serve, activates instantly — but must be explicitly requested on Products tab.

**Critical**: `w_organization_social` is restricted. Always start with `openid profile email w_member_social` only.

### Author URN — What Works and What Doesn't

| Value | Result | Notes |
|-------|--------|-------|
| `urn:li:person:{id}` | ✅ Works | Use member ID from `sub` claim in /v2/userinfo |
| `urn:li:member:{id}` | ✅ Works | Also accepted (same ID) |
| `urn:li:person:~` | ❌ 400/422 | Tilde does NOT auto-resolve to current user |
| `urn:li:member:~` | ❌ 400/422 | Same — does not work |
| No `author` field | ❌ 400 | Field is required |

### Redirect URI
`http://localhost:8089/callback` (local server catches the code)

### Token Lifetime
- Access token: 60 days
- No refresh token available (re-auth required)

## Posting API

### Personal Profile Post
```
POST https://api.linkedin.com/v2/ugcPosts
Authorization: Bearer <token>
X-Restli-Protocol-Version: 2.0.0

{
  "author": "urn:li:person:<ID>",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {"text": "post text"},
      "shareMediaCategory": "NONE"
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
```

### Company Page Post
Same as above but `author` = `urn:li:organization:<ORG_ID>`

## Setup Steps (for [REDACTED — dati personali rimossi])

1. Go to https://www.linkedin.com/developers/
2. Create App → Name: "Hermes Bots" → Link to company page
3. Auth tab → Add redirect URL: `http://localhost:8089/callback`
4. Products tab → Request "Share on LinkedIn" + "Marketing Developer Platform"
5. Copy Client ID + Client Secret
6. Edit `<HERMES_ROOT>/shared/linkedin/config.env`
7. Run `python3 linkedin.py auth` → authorize in browser
8. Run `python3 linkedin.py token <code>` from callback
9. Test: `python3 linkedin.py post "Test post"`

## Cron Integration

The `linkedin-content-calendar` cron job generates posts and sends to [REDACTED — dati personali rimossi]. Once API is configured, update the cron to auto-post:

```
# In cron prompt, add:
# After generating the post text, save to /tmp/linkedin-post.txt
# Then run: python3 <HERMES_ROOT>/shared/linkedin/linkedin.py post-file /tmp/linkedin-post.txt
```

## Pitfalls

- **Token expiry**: 60 days. Re-run `auth` when expired.
- **Rate limits**: LinkedIn has aggressive rate limits. Don't post more than 1-2x/day.
- **Company page requires org admin**: [REDACTED — dati personali rimossi] must be admin of the LinkedIn company page.
- **Products need approval**: "Share on LinkedIn" may take 1-2 days for approval.
- **No image upload in basic API**: Media uploads require additional API calls (not implemented).
- **Secret redaction**: The Hermes session redacts secrets. Use file-based config, not inline strings.
