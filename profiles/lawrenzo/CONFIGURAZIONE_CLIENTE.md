# Lawrenzo Legal — Guida configurazione

File: `legal-config.yaml` nel profilo Hermes.

## Campi obbligatori go-live

| Campo | Esempio |
|-------|---------|
| `client.name` | [Ragione Sociale Cliente] |
| `client.sector` | saas |
| `jurisdiction.foro` | Milano |
| `roles.admin` | {{TELEGRAM_CHAT_ID}} |

## Comandi Telegram

```
config mostra
config cliente "[Ragione Sociale]"
config settore saas
config foro Milano
config gruppo {{TELEGRAM_CHAT_ID}}
```

## Checklist

- [ ] Token in `.env`
- [ ] Wizard `setup` completato
- [ ] Test NDA con foro corretto
- [ ] Disclaimer visibile in output
