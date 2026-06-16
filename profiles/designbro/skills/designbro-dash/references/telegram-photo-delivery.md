# Telegram Photo Delivery — Workaround

## Problem

The `send_message` tool with `MEDIA:` prefix does NOT reliably deliver images as native Telegram photos:
- `MEDIA:/path/to/image.jpg` alone → "No deliverable text or media remained after processing MEDIA tags"
- Text + `MEDIA:` → message sent but arrived as text/emoji, NOT as a photo

**HOWEVER:** `MEDIA:/path` DOES work when used in the assistant's direct response text (not inside `send_message`). The gateway auto-processes it into a native photo. This is useful for single images but cannot send multiple images in one turn.

This was confirmed in testing on 2026-05-28 (banner sent via response text) and 2026-05-29 (send_message failed, Bot API worked).

## Solution

Use the direct Telegram Bot API `sendPhoto` endpoint via Python scripts.

### Single Photo

```bash
python3 <HERMES_ROOT>/shared/scripts/send-photo.py PROFILE CHAT_ID /path/to/image.jpg "Caption text"
```

NOTE: `send-photo.py` requires a Hermes profile name as first arg (e.g. `designbro`, `default`). It reads the token from `~/.hermes/profiles/{PROFILE}/.env`.

### Batch (recommended for 5+ photos — loads token once)

```bash
python3 <HERMES_ROOT>/shared/scripts/batch-send.py CHAT_ID /path/to/directory/ "Caption prefix"
```

### Legacy batch (slower — reloads .env per photo)

```bash
python3 <HERMES_ROOT>/shared/scripts/send-all-photos.py CHAT_ID /path/to/directory/
```

### How they work:
1. Read `TELEGRAM_BOT_TOKEN` from current profile's `.env`
2. Build multipart/form-data POST body with chat_id, caption, and photo binary
3. POST to `https://api.telegram.org/bot{token}/sendPhoto`
4. Return `ok=True` with message_id and photo_sizes count

## Pitfalls

1. **Secret redaction**: Inline Python containing `TELEGRAM_BOT_TOKEN` gets mangled by the redaction filter. ALWAYS write scripts to files, never run inline via `terminal`.

2. **VERIFY FILES EXIST before sending.** Previous sessions may have generated images in memory or temp dirs that don't persist across sessions. Always `ls` or `search_files` to confirm JPGs exist before running batch send. A script that reports "✅ Sent" for non-existent files is worse than one that errors. This burned us on 2026-05-29 — bot-profile images from a prior session were never saved to disk.

3. **send-photo.py is slow in loops.** It reloads `.env` on every invocation (~7s/photo). For batch operations (5+ photos), use `batch-send.py` which loads the token once (~1.2s/photo). Measured: 25 photos in 180s vs 30s.

4. **Body construction**: Mixing `str` and `bytes` in the multipart body causes `TypeError`. Build text parts as string, encode to bytes, then concatenate with binary photo data and footer bytes.

5. **Timeout**: Single photos take 2-5 seconds. Batch of 25 takes ~30 seconds with batch-send.py. Set `timeout=300` for batch operations.

6. **File size**: Telegram accepts photos up to 10MB. For larger files, use `sendDocument` instead.

7. **Rate limiting**: Add 0.4s delay between photos in batch sends to avoid hitting Telegram rate limits.

8. **Background process buffering**: Running batch-send via `terminal(background=True)` may buffer stdout. Use `python3 -u` flag or run in foreground with generous timeout for visibility.

9. **Verify bot image filenames match brand.** When generating bot profile images, the `name` field in the generation script becomes the filename slug. If you use "GROOT" instead of "Ratatouille", the file is `bot-profile-groot-01.jpg` but the HTML expects `bot-profile-ratatouille-01.jpg`. Always cross-check the bot names from the brand brief against the generated filenames before referencing them in HTML.

10. **Externally modified files.** If `patch` fails with "modified since you last read it", re-read the file before editing. The HermesBro landing page is edited by multiple sessions — always `read_file` or `terminal("cat ...")` before `patch`.

## Script Locations

- `<HERMES_ROOT>/shared/scripts/send-photo.py` — single photo sender
- `<HERMES_ROOT>/shared/scripts/batch-send.py` — batch sender (loads token once, recommended)
- `<HERMES_ROOT>/shared/scripts/send-all-photos.py` — legacy batch sender
- `designbro-dash/scripts/batch-send.py` — copy bundled with skill
