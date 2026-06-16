# Shared Knowledge — ContAIbile (ripulito per pubblicazione)

## Possibili cause (gruppo Telegram non raggiungibile)

1. Il bot è stato rimosso dal gruppo
2. Il gruppo è stato cancellato o l'ID è cambiato
3. Privacy mode + nessun admin ha approvato

## Architettura

CLIENTE → hermesbro.cloud/register → POST /api/tenants → AUTO-PROVISIONING
                                                        ↓
                                    Crea profili da template (SOUL + GOAL + skills)
                                    Assegna token da bot_pool (quando popolata)
                                    Avvia systemd service
                                    Pronto in <30 secondi

## Template profili

I profili dei bot risiedono in `{{HERMES_HOME}}/profiles/<nome>/`:

- gribbito/        🔒 Orchestratore principale
- contabile/       📊 ContAIbile — contabilità PMI
- lawrenzo/        📜 Normative fiscali
- wannabe/         🎯 [descrizione]
- designbro/       🎨 Design e UI
- el-froggo/       🐸 Vision, creatività, crypto
- ducato/          💰 Strategia finanziaria
- groot/           🌱 Ricavi e food cost
- sentinel/        🛡️ Security e monitoraggio
- machiavelli/     🎭 Orchestratore flotta

## Flotta

- 10 bot attivi su singola istanza
- RAM: ~3.3GB su 11GB
- Bus Hermes per comunicazione inter-bot
- Gateway Telegram con webhook
