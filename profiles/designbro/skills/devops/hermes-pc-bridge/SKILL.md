---
name: hermes-pc-bridge
description: Comunicazione bidirezionale VPS ↔ Hermes PC (Windows) tramite SSH
tags: [ssh, windows, vps, bridge, communication]
version: 1.0
---

# hermes-pc-bridge
## Comunicazione VPS ↔ Hermes PC (Windows)

### Quando usare
- Quando un bot sul VPS deve eseguire comandi su Hermes PC (Windows)
- Quando un bot deve inviare/ricevere file da Hermes PC
- Quando serve sincronizzare stato tra VPS e Windows

### Architettura
Hermes PC (Windows) è dietro NAT — il VPS non può connettersi direttamente.
Soluzione: **reverse SSH tunnel**. Quando Hermes PC si connette al VPS, apre un tunnel che permette al VPS di raggiungerlo.

### Connessione VPS → Hermes PC (tramite tunnel)
```bash
# Controlla se il tunnel è attivo
<HERMES_ROOT>/scripts/hermes-pc-tunnel.sh --health

# Esegui comando su Hermes PC (tramite tunnel)
<HERMES_ROOT>/scripts/hermes-pc-tunnel.sh --exec "comando"

# Manuale (senza script):
ssh -i /home/hermes-pc/.ssh/id_ed25519 -p 22345 -o StrictHostKeyChecking=no -o ConnectTimeout=5 hermes-pc@127.0.0.1 "comando"
```

### Connessione Hermes PC → VPS (diretta)
```bash
# Da Windows (Hermes PC):
ssh -i ~/.ssh/hermes-pc -p 2222 -o StrictHostKeyChecking=no hermes-pc@194.146.12.219 "comando"

# Copiare file da VPS a Hermes PC:
scp -i /home/hermes-pc/.ssh/id_ed25519 -P 2222 /path/to/file hermes-pc@194.146.12.219:C:/Users/[REDACTED — dati personali rimossi]/file
```

### Aprire il tunnel (da Hermes PC Windows)
```batch
REM Eseguire su Windows per aprire la comunicazione bidirezionale:
ssh -i %USERPROFILE%\.ssh\hermes-pc -p 2222 -o StrictHostKeyChecking=no -R 22345:localhost:22 hermes-pc@194.146.12.219 -N

REM Oppure esegui il batch file:
\\path\to\hermes-pc-connect.bat
```

### Parametri fissi
- **Host VPS**: 194.146.12.219
- **Porta SSH VPS**: 2222
- **Utente**: hermes-pc
- **Chiave VPS**: /home/hermes-pc/.ssh/id_ed25519
- **Porta tunnel (VPS→PC)**: 22345 (localhost)
- **Timeout**: 10 secondi (default), 5 per health check

### Pattern di comunicazione

#### 1. Comando singolo (fire-and-forget)
```bash
ssh -i /home/hermes-pc/.ssh/id_ed25519 -p 2222 -o StrictHostKeyChecking=no -o ConnectTimeout=10 hermes-pc@194.146.12.219 "powershell -Command 'Get-Process'"
```

#### 2. Script complesso (heredoc)
```bash
ssh -i /home/hermes-pc/.ssh/id_ed25519 -p 2222 -o StrictHostKeyChecking=no hermes-pc@194.146.12.219 "powershell -Command @'
# script PowerShell qui
'@"
```

#### 3. Health check (silent)
```bash
ssh -i /home/hermes-pc/.ssh/id_ed25519 -p 2222 -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o BatchMode=yes hermes-pc@194.146.12.219 "echo ok" 2>/dev/null
```

### Bus integration
I bot possono comunicare con Hermes PC anche tramite il bus messaggi:
```bash
# Scrivere messaggio per Hermes PC
python3 <HERMES_ROOT>/shared/scripts/bus-send.py <bot-name> hermes-pc "messaggio"

# Hermes PC può leggere i messaggi dal bus via SSH
ssh ... "cat <HERMES_ROOT>/shared/bus/inbox/hermes-pc/"
```

### Errori comuni
- **Connection timed out**: Hermes PC è spento o non in rete
- **Permission denied**: chiave SSH non configurata o errata
- **Host key verification failed**: aggiungere `-o StrictHostKeyChecking=no`
- **Connection refused**: SSH non attivo su Hermes PC (abilitare OpenSSH Server nelle impostazioni Windows)

### Sicurezza
- La chiave SSH è solo su VPS (nessun bot può accedere al VPS da fuori)
- hermes-pc ha permessi limitati (no sudo, no system files)
- Timeout breve (10s) per evitare processi bloccati
