# Bot Token Locations

All bot tokens are stored in `.env` files under `/home/[REDACTED — dati personali rimossi]/ai-stack/<botname>-gold/`.

| Bot | Token File | Profile |
|-----|-----------|---------|
| ContAIbile | `/home/[REDACTED — dati personali rimossi]/ai-stack/contabile-gold/.env` | `contabile` |
| LAWrenzo | `/home/[REDACTED — dati personali rimossi]/ai-stack/lawrenzo-gold/.env` | `lawrenzo` |
| Wannabe | `/home/[REDACTED — dati personali rimossi]/ai-stack/wannabe-gold/.env` | `wannabe` |
| DesignBro | `/home/[REDACTED — dati personali rimossi]/ai-stack/designbro-gold/.env` | `designbro` |
| GROOT | `/home/[REDACTED — dati personali rimossi]/ai-stack/groot-gold/.env` | `groot` |
| DUCATO | `/home/[REDACTED — dati personali rimossi]/ai-stack/ducato-gold/.env` | `ducato` |
| El Froggo | `/home/[REDACTED — dati personali rimossi]/ai-stack/el-froggo-gold/.env` | `el-froggo` |
| MR.ROBOT | `/home/[REDACTED — dati personali rimossi]/ai-stack/mrrobot-gold/.env` | `mr-robot` |
| Sentinel | `/home/[REDACTED — dati personali rimossi]/ai-stack/sentinel-gold/.env` | `sentinel` |
| Machiavelli | `/home/[REDACTED — dati personali rimossi]/ai-stack/machiavelli-gold/.env` | `machiavelli` |

## How to extract a token
```bash
grep BOT_TOKEN /home/[REDACTED — dati personali rimossi]/ai-stack/<botname>-gold/.env
```

## How to "disable" a bot ([REDACTED — dati personali rimossi]'s meaning)
1. Stop the process: `hermes stop <profile-name>` or `systemctl stop hermes-<profile>.service`
2. Token stays in the `.env` file — extract it with grep above
3. Do NOT touch the website/landing page
