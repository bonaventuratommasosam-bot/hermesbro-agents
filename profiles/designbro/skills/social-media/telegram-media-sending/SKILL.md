---
name: telegram-media-sending
description: "Send photos, videos, and files on Telegram via Bot API. Covers the gap where send_message MEDIA: tags deliver as text instead of native media."
version: 1.0.0
author: gribbito
metadata:
  hermes:
    tags: [telegram, media, photos, bot-api, upload]
---

# Telegram Media Sending

## Problem

The `MEDIA:/path/to/file` tag has **context-dependent behavior**:
- ✅ Works in **assistant response text** — the gateway auto-processes it into a native Telegram photo. Limit: one image per turn this way.
- ❌ Does NOT work inside `send_message` tool — arrives as plain text, not a photo.

For single images, just include `MEDIA:/path/to/file.jpg` in your response text. For multiple images (2+), use the Bot API scripts below.

## Solution: Direct Bot API

Use the Telegram Bot API `sendPhoto` endpoint directly with multipart form data.

### Script Location

`<HERMES_ROOT>/shared/scripts/send-photo.py`

### Usage

```bash
python3 <HERMES_ROOT>/shared/scripts/send-photo.py <profile> <chat_id> <photo_path> [caption] [thread_id]
```

Examples:
```bash
# Basic photo
python3 <HERMES_ROOT>/shared/scripts/send-photo.py gribbito <ADMIN_CHAT_ID> /path/to/logo.jpg "Logo Hermes Bots"

# Photo to group topic/thread
python3 <HERMES_ROOT>/shared/scripts/send-photo.py el-froggo <GROUP_CHAT_ID> /tmp/chart.png "ETH chart" 32638
```

### How It Works

1. Reads bot token from `~/.hermes/profiles/<profile>/.env` (`TELEGRAM_BOT_TOKEN`)
2. Constructs multipart/form-data body with `chat_id`, `caption`, `photo`, and optional `message_thread_id`
3. POSTs to `https://api.telegram.org/bot<token>/sendPhoto`
4. Returns `ok=True` on success with `msg_id` and `photo_sizes`

### Key Details

- **Supported formats:** JPG, PNG, WEBP, GIF
- **Max file size:** 10MB (Telegram limit for photos)
- **For documents/files:** Use `sendDocument` instead of `sendPhoto` (modify the script endpoint)
- **For videos:** Use `sendVideo` endpoint
- **Group chats:** Use negative chat_id (e.g., `-1001234567890`)
- **Topics/threads:** Add `message_thread_id` parameter to the form body

## Pitfalls

1. **Secret redaction mangles inline code:** When writing the script via `write_file`, the `.env` token gets redacted to `***` in the code. Always write the script to a file first, then execute it — never try to inline the token reading in terminal commands.

2. **str/bytes concatenation bug:** When building the multipart body, you MUST encode text parts to bytes BEFORE concatenating with binary photo data. Mixing `str + bytes` raises `TypeError`. Build text parts as a list, join with `\\r\\n`, `.encode()`, then concatenate with photo bytes. See the fixed script in `scripts/send-photo.py`.

3. **File size:** Photos must be ≤10MB (Telegram limit). For larger files, compress with Pillow or use `sendDocument`.

4. **Caption length:** Max 1024 characters for photo captions.

5. **Rate limits:** Telegram limits to ~30 messages/second per bot. For bulk sends, add delays.

6. **Token reading pattern:** Use `parts = line.split('=', 1)` + `if parts[0] == 'KEY'` instead of `startswith('KEY=')` — the latter breaks when the redaction engine mangles the prefix in code.

7. **Group chats:** Use negative chat_id (e.g., `-1001234567890`). For topics/threads, add `message_thread_id` field to the multipart body.

8. **Debug output:** Always print `msg_id` and `photo_sizes` from the response to verify delivery. `ok=True` alone doesn't confirm the image rendered as a photo.

## When to Use

- Sending generated images (logos, banners, diagrams) to Telegram
- Sending screenshots from browser automation
- Sending any image that must appear as a native photo (not a file attachment)

## When NOT to Use

- Text-only messages → use `send_message`
- Documents/PDFs → use `sendDocument` endpoint (see below)
- When `MEDIA:` tag works (some gateway versions may support it)

## Sending Documents (PDFs, files)

For non-image files, change the endpoint from `sendPhoto` to `sendDocument`:

```python
conn.request('POST', '/bot' + token + '/sendDocument', body=body,
             headers={'Content-Type': 'multipart/form-data; boundary=' + boundary})
```

And change the form field name from `photo` to `document`:

```python
'Content-Disposition: form-data; name="document"; filename="report.pdf"\r\n'
'Content-Type: application/pdf\r\n\r\n'
```

## Sending Videos

Endpoint: `sendVideo`, field name: `video`, Content-Type: `video/mp4`.
Max: 50MB (local upload) or 200MB (via URL).

## Sending Audio/Voice

Endpoint: `sendAudio` (music) or `sendVoice` (voice message).
Field name: `audio` or `voice`, Content-Type: `audio/ogg` or `audio/mpeg`.
