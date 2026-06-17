# LinkedIn OAuth — Pitfalls & Lessons Learned

## Scope Restrictions (2026-05-29)

The `w_organization_social` scope (post as company page) is a RESTRICTED API product. LinkedIn requires manual approval — can take days to weeks. Error when requesting it without approval:

```
error=unauthorized_scope_error
error_description=Scope "w_organization_social" is not authorized for your application
```

**Fix**: Remove `w_organization_social` from scope.

## Scope Cascade — What Actually Works (2026-05-29)

LinkedIn apps created with only "Share on LinkedIn" product have a VERY limited scope set:

| Scope | Status | Notes |
|-------|--------|-------|
| `openid` | ❌ unauthorized | Needs "Sign In with LinkedIn using OpenID Connect" product |
| `profile` | ❌ unauthorized | Same — requires OIDC product |
| `email` | ❌ unauthorized | Same |
| `r_liteprofile` | ✅ works | Legacy scope, self-serve |
| `r_emailaddress` | ✅ works | Legacy scope, self-serve |
| `w_member_social` | ✅ works | Share on LinkedIn product |
| `w_organization_social` | ❌ restricted | Needs Marketing Developer Platform approval (days/weeks) |

**Working scope string for first setup**: `r_liteprofile r_emailaddress w_member_social`

## Person URN Problem — CRITICAL BLOCKER

With only `r_liteprofile + w_member_social`, you can get the access token BUT:

1. `/v2/me` returns **403 ACCESS_DENIED** — "Not enough permissions to access: me.GET.NO_VERSION"
2. `/v2/userinfo` returns **403** — same error
3. `/v2/emailAddress` returns **403** — same error
4. LinkedIn access tokens are **opaque strings** (NOT JWTs) — cannot decode to extract member ID
5. Posts API (`/v2/ugcPosts` and `/v2/posts`) **requires** `author` field as `urn:li:person:{id}` or `urn:li:member:{id}`
6. The special value `urn:li:member:~` does NOT work — returns 422 validation error

**This means**: with only the "Share on LinkedIn" product, you can authenticate but CANNOT post because you can't determine the person URN.

**Fix**: [REDACTED — dati personali rimossi] must add the **"Sign In with LinkedIn using OpenID Connect"** product to the app:
1. Go to https://www.linkedin.com/developers/apps → App → Products
2. Request "Sign In with LinkedIn using OpenID Connect" (self-serve, activates immediately)
3. Re-run OAuth with scope `openid profile email w_member_social`
4. The `sub` claim in the userinfo response contains the member ID
5. Construct URN as `urn:li:person:{sub}`

**Alternative (quick hack)**: Ask [REDACTED — dati personali rimossi] for his LinkedIn profile URL (e.g., `linkedin.com/in/sammybwoyy`). The vanity name can sometimes be used to look up the numeric member ID via web scraping, but this is fragile.

To get company page posting later:
1. Go to LinkedIn Developer App → Products tab
2. Request access to "Marketing Developer Platform" or "Share on LinkedIn"
3. Wait for approval
4. Then add `w_organization_social` back to scope

## OAuth Redirect Flow (localhost)

The redirect URI `http://localhost:8089/callback` is required by LinkedIn for local apps. But [REDACTED — dati personali rimossi] runs the browser on his machine, not the VPS.

**What happens:**
1. [REDACTED — dati personali rimossi] opens auth URL → LinkedIn shows consent screen
2. [REDACTED — dati personali rimossi] clicks "Allow" → LinkedIn redirects to `http://localhost:8089/callback?code=XXXXX&state=hermesbots2026`
3. Browser shows "This site can't be reached" (localhost:8089 doesn't exist on [REDACTED — dati personali rimossi]'s machine)
4. [REDACTED — dati personali rimossi] copies `code=` from URL bar and sends it to the bot
5. Bot exchanges code for access token

**Script**: `<HERMES_ROOT>/shared/linkedin/linkedin-oauth.py`
```bash
python3 linkedin-oauth.py auth          # Generate auth URL
python3 linkedin-oauth.py token CODE    # Exchange code for token
python3 linkedin-oauth.py me            # Get profile + save URN
```

## App Creation Requirements

LinkedIn app creation form requires:
- **App name**: Hermes Bots
- **LinkedIn Page**: Must be a Company Page (not personal profile). Create at https://www.linkedin.com/company/setup/new/ FIRST
- **Privacy policy URL**: `https://YOUR_VPS_HOST/hermesbro/privacy-policy.html`
- **App logo**: Square image, at least 100px

After creation:
1. Go to Auth tab
2. Add redirect URL: `http://localhost:8089/callback`
3. Note Client ID and Client Secret

## Token Lifetime

- Access token: 60 days
- Refresh token: 365 days (if `offline_access` scope was requested — not available for basic apps)
- Re-run `python3 linkedin-oauth.py auth` when expired

## Config File Token Write Bug

The `linkedin-oauth.py` script's `exchange_code()` function tries to replace old token strings in `config.env` using `str.replace()`. This **FAILS** because Hermes secret redaction masks existing tokens to `***` in the file content seen by the agent. The replacement finds no match, and the file retains the old (now invalid) token.

**Symptom**: Script prints `ACCESS_TOKEN=<new>` (success) but `config.env` still contains the old token. Next API call uses the old (revoked) token → 401 REVOKED_ACCESS_TOKEN.

**Fix**: After exchanging the code, ALWAYS write the full config file from scratch rather than doing string replacement:

```python
# DON'T — fails with redacted content:
content = content.replace('LINKEDIN_ACCESS_TOKEN=*** f'LINKEDIN_ACCESS_TOKEN="{tok...)
# DO — rewrite the entire file:
with open(env_path, 'w') as f:
    f.write(f'LINKEDIN_CLIENT_ID="{client_id}"\n')
    ...
    f.write(f'LINKEDIN_ACCESS_TOKEN="{tok...)
    f.write(f'LINKEDIN_PERSON_URN="{urn}"\n')
```

**Best approach**: Use the `write_file` tool to write the entire config, using the token value from the script output. Don't rely on the script's internal file-update logic.

## Token Revocation from Re-authorization

If [REDACTED — dati personali rimossi] authorizes the OAuth URL multiple times in sequence (e.g., after scope errors), **each new authorization revokes the previous token**. LinkedIn allows only ONE active token per app per user at a time.

**Symptom**: After successfully exchanging a code, the next API call returns `401 REVOKED_ACCESS_TOKEN`.

**Fix**: Only run the OAuth flow ONCE after all scope issues are resolved. Don't re-authorize "just to be safe." If you need a new token, re-authorize once and use the new code immediately.

**Session lesson (2026-05-29)**: We went through 4 OAuth iterations (scope errors → fix → re-authorize → token revoked → re-authorize again). Each iteration invalidated the previous token. The correct flow is:
1. Add "Sign In with LinkedIn using OpenID Connect" product (self-serve)
2. Single OAuth with scope `openid profile email w_member_social`
3. Exchange code → get token + person URN
4. IMMEDIATELY test posting (don't wait, don't re-authorize)

## [REDACTED — dati personali rimossi]'s LinkedIn Profile

|- **Name**: [Nome Cliente]
|- **Person URN**: `[LinkedIn URN]`
|- **Email**: [email cliente]
|- **LinkedIn Client ID**: [client ID]
- **Config file**: `<HERMES_ROOT>/shared/linkedin/config.env`
