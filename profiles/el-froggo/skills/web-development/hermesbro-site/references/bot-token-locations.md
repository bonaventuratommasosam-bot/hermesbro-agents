# Bot Token Locations

All bot tokens are stored in `.env` files under `<AI_STACK_PATH>/<botname>-gold/`.

| Bot | Token File | Profile |
|-----|-----------|---------|
| ContAIbile | `<AI_STACK_PATH>/contabile-gold/.env` | `contabile` |
| LAWrenzo | `<AI_STACK_PATH>/lawrenzo-gold/.env` | `lawrenzo` |
| Wannabe | `<AI_STACK_PATH>/wannabe-gold/.env` | `wannabe` |
| DesignBro | `<AI_STACK_PATH>/designbro-gold/.env` | `designbro` |
| GROOT | `<AI_STACK_PATH>/groot-gold/.env` | `groot` |
| DUCATO | `<AI_STACK_PATH>/ducato-gold/.env` | `ducato` |
| El Froggo | `<AI_STACK_PATH>/el-froggo-gold/.env` | `el-froggo` |
| MR.ROBOT | `<AI_STACK_PATH>/mrrobot-gold/.env` | `mr-robot` |
| Sentinel | `<AI_STACK_PATH>/sentinel-gold/.env` | `sentinel` |
| Machiavelli | `<AI_STACK_PATH>/machiavelli-gold/.env` | `machiavelli` |

## How to extract a token
```bash
grep BOT_TOKEN <AI_STACK_PATH>/<botname>-gold/.env
```

## How to "disable" a bot
1. Stop the process: `hermes stop <profile-name>` or `systemctl stop hermes-<profile>.service`
2. Token stays in the `.env` file — extract it with grep above
3. Do NOT touch the website/landing page
