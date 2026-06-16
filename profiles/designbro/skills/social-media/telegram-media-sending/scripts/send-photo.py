#!/usr/bin/env python3
"""Send photo via Telegram Bot API. Native photo delivery (not text)."""
import json, http.client, ssl, sys, os

def get_token(profile):
    env_path = f'<HERMES_ROOT>/profiles/{profile}/.env'
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            parts = line.split('=', 1)
            if len(parts) == 2 and parts[0] == 'TELEGRAM_BOT_TOKEN':
                return parts[1]
    raise ValueError(f"No TELEGRAM_BOT_TOKEN in {env_path}")

def send_photo(token, chat_id, photo_path, caption="", thread_id=None):
    with open(photo_path, 'rb') as f:
        photo_data = f.read()

    print(f"Sending photo ({len(photo_data)} bytes) to chat {chat_id}")

    boundary = '----HermesPhoto'
    parts = []
    
    # chat_id
    parts.append('--' + boundary)
    parts.append('Content-Disposition: form-data; name="chat_id"')
    parts.append('')
    parts.append(str(chat_id))
    
    # caption
    if caption:
        parts.append('--' + boundary)
        parts.append('Content-Disposition: form-data; name="caption"')
        parts.append('')
        parts.append(caption)
    
    # thread_id for topics
    if thread_id:
        parts.append('--' + boundary)
        parts.append('Content-Disposition: form-data; name="message_thread_id"')
        parts.append('')
        parts.append(str(thread_id))
    
    text_body = '\r\n'.join(parts) + '\r\n'
    
    photo_header = '--' + boundary + '\r\n'
    photo_header += 'Content-Disposition: form-data; name="photo"; filename="photo.jpg"\r\n'
    photo_header += 'Content-Type: image/jpeg\r\n\r\n'
    
    footer = '\r\n--' + boundary + '--\r\n'
    
    body = text_body.encode() + photo_header.encode() + photo_data + footer.encode()
    
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection('api.telegram.org', context=ctx)
    conn.request('POST', '/bot' + token + '/sendPhoto', body=body,
                 headers={'Content-Type': 'multipart/form-data; boundary=' + boundary})
    resp = conn.getresponse()
    raw = resp.read().decode()
    result = json.loads(raw)
    print(f"Status: {resp.status}")
    print(f"ok={result.get('ok')}")
    if not result.get('ok'):
        print(f"error={result.get('description')}")
    else:
        msg = result['result']
        print(f"msg_id={msg.get('message_id')}")
        print(f"photo_sizes={len(msg.get('photo', []))}")
    conn.close()
    return result

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: send-photo.py <profile> <chat_id> <photo_path> [caption] [thread_id]")
        print("Example: send-photo.py gribbito <ADMIN_CHAT_ID> /tmp/photo.jpg 'My caption'")
        sys.exit(1)
    
    profile = sys.argv[1]
    chat_id = sys.argv[2]
    photo_path = sys.argv[3]
    caption = sys.argv[4] if len(sys.argv) > 4 else ""
    thread_id = sys.argv[5] if len(sys.argv) > 5 else None
    
    token = get_token(profile)
    send_photo(token, chat_id, photo_path, caption, thread_id)
