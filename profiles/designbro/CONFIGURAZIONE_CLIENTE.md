# DesignBro Studio — Guida configurazione cliente

Ogni cliente configura il proprio bot **senza toccare il codice**. Due modi: file YAML o comandi Telegram (admin).

## 1. File principale: `brand-config.yaml`

Percorso locale: `<PROFILE>/brand-config.yaml`
Clienti paganti: `<CLIENTS_DIR>/<agente>/brand-config.yaml`

### Campi obbligatori per andare live

| Campo | Esempio | Note |
|-------|---------|------|
| `brand.name` | `Caffè Rossi` | Nome in tutti i deliverable |
| `brand.industry` | `food` | Font pairing e mood |
| `telegram.group_chat_id` | `-1001234567890` | Preview design |
| `roles.admin` | `[123456789]` | Approvazioni finali |

### Campi opzionali

- `visual.primary_color` — HEX brand
- `visual.mood` — professional, warm, bold, minimal
- `telegram.require_approval` — default true
- `cron.enabled` — check-in brand kit mensile

## 2. Comandi Telegram (admin)

```
config mostra
config brand "Caffè Rossi"
config settore food
config colore #1E3A5F
config gruppo -1001234567890
config cron on
```

## 3. Script CLI

```bash
python3 .../configure_brand.py show
python3 .../configure_brand.py set brand.name "Caffè Rossi"
python3 .../configure_brand.py validate
python3 .../configure_brand.py apply-cron
```

## 4. Checklist go-live

- [ ] Token Telegram in `.env`
- [ ] `brand-config.yaml` compilato (o wizard `setup`)
- [ ] `configure_brand.py validate` → OK
- [ ] Test: `logo concept` → output con brand name corretto

## 5. Cosa personalizzare liberamente

- Mood e stile visivo
- Gruppo review vs solo DM
- Formati output (logo, palette, social, menu)
- Lingua default

**Non serve** modificare SOUL.md — il bot legge `brand-config.yaml`.
