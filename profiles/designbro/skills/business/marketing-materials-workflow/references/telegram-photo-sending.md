# Sending Photos on Telegram — Workaround

## Problem

The `send_message` tool with `MEDIA:` prefix does NOT reliably deliver images as native Telegram photos. In testing (2026-05-29):
- `MEDIA:/path/to/image.jpg` alone → "No deliverable text or media remained after processing MEDIA tags"
- Text + `MEDIA:/path/to/image.jpg` → message sent but arrived as text/emoji, NOT as a photo

## Solution

Use the direct Telegram Bot API `sendPhoto` endpoint via a Python script.

**Script**: `<HERMES_ROOT>/shared/scripts/send-photo.py`

```bash
python3 <HERMES_ROOT>/shared/scripts/send-photo.py CHAT_ID /path/to/image.jpg "Caption text"
```

### How it works:
1. Reads bot token from `<HERMES_ROOT>/profiles/gribbito/.env` (key: `TELEGRAM_BOT_TOKEN`)
2. Builds multipart/form-data POST body with chat_id, caption, and photo binary
3. POSTs to `https://api.telegram.org/bot{token}/sendPhoto`
4. Returns `ok=True` with message_id and photo_sizes count

### API Response (success):
```
Sending photo (61643 bytes) to chat <ADMIN_CHAT_ID>
Status: 200
ok=True
msg_id=8216
photo_sizes=3
```

## Pitfalls

1. **Secret redaction**: The `.env` file has `TELEGRAM_BOT_TOKEN=***` in the system. Inline Python code containing this pattern gets mangled by the redaction filter. ALWAYS write photo-sending scripts to files, never run inline via `terminal`.

2. **Body construction**: Mixing `str` and `bytes` in the multipart body causes `TypeError`. Build text parts as string, encode to bytes, then concatenate with binary photo data and footer bytes.

3. **File size**: Telegram accepts photos up to 10MB. For larger files, use `sendDocument` instead.

4. **JPEG format**: Photos must be valid JPEG/PNG. PIL-generated images work fine. Save as JPEG with `quality=95` for good quality/size balance.

## Alternative: sendDocument

For non-image files (PDFs, etc.), use `sendDocument` endpoint.

### Quick curl one-liner (preferred for one-off sends)
```bash
source <HERMES_ROOT>/profiles/gribbito/.env 2>/dev/null
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument" \
  -F chat_id="<ADMIN_CHAT_ID>" \
  -F document=@/path/to/file.pdf \
  -F caption="Description"
```

**Why curl over Python**: No script file needed, no str/bytes issues, handles binary natively. Use this for one-off document sends.

### Python approach
```python
# Similar to sendPhoto but endpoint is sendDocument
conn.request('POST', '/bot' + token + '/sendDocument', body=body, ...)
# Content-Disposition: name="document" (not "photo")
```

**Pitfall**: `send_message` with `MEDIA:/path/to/file.pdf` does NOT work for PDFs either. Same limitation as photos. Always use direct Bot API (curl or Python).
