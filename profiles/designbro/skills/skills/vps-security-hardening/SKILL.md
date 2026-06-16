---
name: vps-security-hardening
description: Implementa e gestisce le pratiche di sicurezza per il hardening del VPS.
emoji: 🔒
tags: [security, vps, ssh, user-management, credentials, hardening]
visibility: public
---

# VPS Security Hardening Skill

Questa skill guida l'agente e l'utente attraverso i processi di hardening di sicurezza per un VPS, in particolare focalizzandosi sulle raccomandazioni critiche da security audit.

## Workflow

### Read-Only Security Audit (no modifications)

When [REDACTED — dati personali rimossi] says "controlla la sicurezza" or "fai un audit", run the checklist in `references/vps-audit-checklist.md` WITHOUT making changes. Present a scored report with ✅/❌/⚠️ per category. Offer to fix issues but don't act without approval.

**Key checks:** SSH config, firewall, fail2ban, open ports, nginx headers, SSL certs, system updates, .env permissions, running services.

**Pitfall:** [REDACTED — dati personali rimossi] said "senza toccare nulla" during a security audit. Always run read-only first, then ask before fixing. He may want Frank (manual ops) to handle fixes, not the bot.

1.  **Rimozione Credenziali Hardcoded (CRITICO - ORA):**
    *   **Diagnosi:** Rileva file contenenti password, token API o chiavi private in chiaro.
    *   **Azione:** Rimuove o commenta le credenziali, avvisando l'utente di caricarle in modo sicuro (es. variabili d'ambiente).
    *   **Riferimento:** `references/hardcoded-credentials-remediation.md` (da creare se servono esempi specifici oltre a quelli già incontrati)

2.  **Gestione Utenti (OGGI):**
    *   **Diagnosi:** Verifica l'esistenza di un utente non-root con `sudo` privileges.
    *   **Azione:** Se non esiste, crea un nuovo utente non-root e lo aggiunge al gruppo `sudo`.
    *   **Pitfall:** Utente già esistente (`adduser` fallisce) - verificare l'appartenenza al gruppo `sudo`.

3.  **Autenticazione SSH Basata su Chiavi (OGGI):**
    *   **Diagnosi:** Verifica la presenza di chiavi SSH per l'utente non-root e se l'autenticazione con password è abilitata.
    *   **Generazione Chiavi:** Genera una coppia di chiavi SSH RSA 4096-bit per l'utente non-root sul VPS.
    *   **Trasferimento Chiave Privata:** Istruisce l'utente su come trasferire in modo sicuro la chiave privata al suo PC locale (tramite `scp`). **ATTENZIONE:** MAI esporre la chiave privata in chat.
        *   **Riferimento:** `references/ssh-key-transfer.md`
    *   **Disabilitare Login Password:** Modifica la configurazione SSH (`/etc/ssh/sshd_config`) per disabilitare l'autenticazione tramite password e/o il login root diretto, forzando l'uso delle chiavi.
    *   **Test:** Richiede all'utente di testare la connessione con la chiave prima di riavviare il servizio SSH.

4.  **Altre Raccomandazioni (SETTIMANA/MESE):**
    *   **Fail2ban:** Abilitare `fail2ban` per proteggere SSH da attacchi brute-force.
    *   **2FA:** Abilitare 2FA sul pannello di controllo del provider VPS (es. Contabo).
    *   **Secrets Manager:** Usare `hermes-vault` (installato a `/root/.local/bin/hermes-vault`) per criptare credenziali. Comando non-interattivo: `echo "" | HERMES_VAULT_PASSPHRASE="<pass>" hermes-vault add <service> --secret <value> --alias <name> --credential-type api_key --tags <tags>`. La passphrase master va salvata nel `.env` del profilo che usa il vault (es. gribbito). Per recuperare: `hermes-vault show-metadata <service>`. Riferimento: `hermes-vault --help`.


## Pitfalls e Workaround

*   **Verificare PRIMA di confermare**: Quando qualcuno (Hermes PC, un subagent) riporta "tutto completato", verificare SEMPRE con tool calls dirette. Controllare mount, permessi, servizi attivi, cron. Non fidarsi delle tabelle riportate. Pattern: `dmsetup ls`, `mount | grep`, `find ... -name`, `systemctl list-units`, `crontab -l`. In questa sessione: LUKS2 e tier confermati, ma audit ogni 10 min NON esisteva nonostante fosse riportato come fatto.
*   **Credenziali esposte in chat:** MAI chiedere o mostrare chiavi private, token o password direttamente in chat. Se un file le contiene, la patch deve essere fatta in-place e nascosta dall'output, fornendo solo un riassunto dell'azione.
*   **Cross-profile writes:** Quando l'utente chiede esplicitamente di installare/configurare qualcosa per un altro profilo (es. Sentinel), usare `cross_profile=True` nei write_file/patch. Senza esplicita richiesta, non scrivere su altri profili.
*   **Problemi con `gh` CLI:** Se `gh` non è riconosciuto dopo l'installazione, può essere un problema di `PATH`. Verificare `which gh` e aggiungere al `.bashrc` o `.profile`. (Riferimento: `github-auth` skill).
*   **Blocco SSH:** Disattivare l'autenticazione password o il login root SOLO dopo aver verificare che il login con chiave funziona correttamente con l'utente non-root.
*   **SSH service name Ubuntu 24.04**: Il servizio SSH si chiama `ssh.service` (NOT `sshd.service`) su Ubuntu Noble. `systemctl restart sshd` fallisce silenziosamente. Sempre usare `systemctl restart ssh`. Verificare con `systemctl list-units | grep ssh`.
*   **SSH systemd socket activation**: Su Debian 12/Ubuntu 24.04, SSH usa `ssh.socket` (systemd socket activation). Cambiare `Port` in `/etc/ssh/sshd_config` NON basta — il socket gestisce il binding. Dopo ogni modifica a Port/ListenAddress: `systemctl daemon-reload && systemctl restart ssh.socket` (NON `restart ssh`). Verificare con `systemctl cat ssh.socket` per vedere le porte effettive. Se `ss -tlnp | grep :PORT` non mostra la nuova porta, il socket non ha ricaricato.
*   **ISP blocca porta 22**: Se SSH su porta 22 ha timeout ma altre porte (443, 80) rispondono, il problema è l'ISP/firewall di rete (non il VPS). Soluzione: porta SSH alternativa (es. 2222). Pattern: (1) `ufw allow 2222/tcp`, (2) aggiungi `Port 2222` in sshd_config DOPO `Port 22`, (3) `systemctl daemon-reload && systemctl restart ssh.socket`, (4) verifica con `ss -tlnp | grep :2222`. Test: `ssh -p 2222 user@host "echo ok"` da remoto.
*   **X11Forwarding**: Disabilitare (`X11Forwarding no`) se non serve. Rischio: attacco X11 forwarding permette keylogging e screenshot sulla sessione remota. Dopo la modifica, restart del servizio SSH (`systemctl restart ssh`).
*   **Permessi .env**: Tutti i file `.env` con credenziali devono avere permessi `600` (`chmod 600`). Verificare con `ls -la`. File in chiaro con permessi 644 sono un rischio CRITICAL.
*   **apt autoremove**: Dopo un upgrade, eseguire `apt autoremove -y` per rimuovere kernel e pacchetti vecchi. Libera spazio e riduce superficie di attacco.
*   **Telegram token reuse**: Two Hermes bot profiles sharing the SAME `TELEGRAM_BOT_TOKEN` in their `.env` will cause one to fail silently with "Telegram bot token already in use". The first service to start grabs the token; the second exits. Always verify unique tokens across all profiles: `grep -rh TELEGRAM_BOT_TOKEN <HERMES_BOT>/.hermes/profiles/*/.env <HERMES_ROOT>/profiles/*/.env 2>/dev/null | sort | uniq -d`. If duplicates appear, the affected bot needs its own token from BotFather. Tested 2026-06-08: frank and mr-robot shared token `841076...6lAo`.
*   **GribbitO runs as root**: The master orchestrator (GribbitO) runs as root by deliberate decision (<FOUNDER>, 2026-06-08). It needs full access to coordinate all bot profiles. Do NOT flag root as a security risk or suggest migrating it. Business bots (frank, sentinel, etc.) run as hermes-bot:hermesbro — that isolation is correct.
*   **Audit read-only**: Per security review senza modificare nulla, usare solo comandi di lettura (`ufw status`, `ss -tlnp`, `grep`, `ls -la`, `openssl s_client`). MAI `systemctl restart` o `chmod` durante un audit.
*   **Health check HTTP 000 con Svc=OK**: Se un health check riporta `HTTP=000` ma il servizio e' attivo, la causa e' quasi sempre il metodo di check (curl verso URL pubblico da localhost → hairpin NAT fallito), NON il servizio. Fix: usare `http://127.0.0.1/health` invece di `https://domain.tld/health`. Aggiungere retry (3 tentativi, 3s delay) prima di allertare. Dettagli completi: `references/nginx-health-check-debugging.md`.
*   **gocryptfs non disponibile**: Su VPS Contabo/Debian base, gocryptfs potrebbe non essere nei repo. Alternativa testata: LUKS2 su file container. Creare file vuoto con `dd`, formattare con `cryptsetup luksFormat`, aprire con `cryptsetup luksOpen`, formattare ext4, montare. Gestire auto-mount con systemd. Vedi `references/isolation-architecture.md` per il setup completo.
*   **Nginx "conflicting server name"**: Warning al boot se due blocchi `server {}` dichiarano lo stesso `server_name` sulla stessa porta. Non critico (uno viene ignorato) ma va pulito. Diagnosi: `grep -rn "server_name" /etc/nginx/sites-enabled/`. Controllare anche che i file in `sites-enabled/` siano symlink a `sites-available/` (non file diretti).
*   **Fix "FAILED" quando nessun fix e' stato tentato**: Se uno script di health check dice "Auto-fix FAILED" ma il servizio e' UP (solo HTTP fallisce), il messaggio e' fuorviante. Un buon check distingue: (a) servizio down → restart → se ancora down, "restart failed", (b) servizio UP ma HTTP fallito → "HTTP check failing, possible network issue" (no fix applicable).

## External Repo Security Audit

Before installing any third-party code (GitHub repos, skill libraries, plugins):

1. **Clone in `/tmp/`** — never in production paths
2. **Scan with SkillSpector** (if available):
   ```bash
   ./scan-skill.sh /path/to/skill --no-llm
   ```
3. **Manual scan** (if SkillSpector not installed):
   - `find . -name "*.py" | wc -l` — count scripts
   - `grep -rl "(socket\.connect|os\.system|eval\(|exec\(|__import__|base64\.b64decode)" --include="*.py"` — dangerous patterns
   - `grep -rl "(reverse_shell|bind_shell|nc -|bash -i|/dev/tcp)" --include="*.py"` — shell patterns
   - `find . -name "*.sh" -o -name "*.exe" -o -name "*.bin"` — unexpected binaries
4. **Check secrets exposure:**
   - `grep -rl "(api_key|secret_key|password|token).*=.*['\"][A-Za-z0-9]" --include="*.py" --include="*.md" --include="*.json"`
   - Verify matches are placeholders/env lookups, not real credentials
5. **Inspect CI/CD workflows** (`.github/workflows/*.yml`) — check for exfiltration, crypto miners, or supply chain attacks
6. **Check plugin manifests** (`.claude-plugin/`, `plugin.json`) — metadata only, no executable payloads
7. **Sample-read 3-5 random scripts** — verify they do what the README claims
8. **Only then copy** the curated subset to production paths

**SkillSpector Installation** (for Sentinel / security agents):
```bash
cd /home/[REDACTED — dati personali rimossi]/ai-stack/agents/sentinel/
git clone https://github.com/nvidia/skillspector.git
```
Wrapper: `./scan-skill.sh` — runs `python skillspector/tools/scan_skill.py` with proper venv.

**Pitfall**: `grep` for `eval(` and `exec(` in Python files will match legitimate uses (e.g., `json.loads`, `argparse`). Read the matched files to confirm, don't blacklist blindly.

## Remote Agent Access (SSH + Limited Sudo)

When granting a remote machine (Hermes PC, another server) SSH access to the VPS for bot management: create a dedicated user, user provides public key, limited sudoers file. Full pattern in `references/remote-agent-ssh-access.md`.

Key rules:
- User generates keypair on THEIR machine (never generate on VPS and transfer private key)
- Limited sudoers: only systemctl (hermes-*, warroom*, compliance-ai, demo-ristorante) + nginx + chown/chmod on /home/[REDACTED — dati personali rimossi]/*
- Always validate sudoers with `sudo visudo -cf`
- `write_file` tool refuses `/etc/sudoers.d/` — use `terminal` with `sudo tee`

### Pattern: `hermes-bot` user (tested 2026-06-03)

When [REDACTED — dati personali rimossi] or a remote operator needs SSH access to manage bot profiles without full root:

```bash
# 1. Create user
useradd -m -s /bin/bash hermes-bot

# 2. Limited sudo — only safe commands
echo 'hermes-bot ALL=(ALL) NOPASSWD: /bin/cp, /bin/mv, /bin/chown, /bin/chmod, /bin/systemctl, /usr/bin/python3' | tee /etc/sudoers.d/hermes-bot
chmod 440 /etc/sudoers.d/hermes-bot

# 3. SSH key — user provides their public key
mkdir -p <HERMES_BOT>/.ssh
echo '<USER_PUBLIC_KEY>' | tee <HERMES_BOT>/.ssh/authorized_keys
chown -R hermes-bot:hermes-bot <HERMES_BOT>/.ssh
chmod 700 <HERMES_BOT>/.ssh
chmod 600 <HERMES_BOT>/.ssh/authorized_keys

# 4. Grant access to bot profiles
for profile in contabile designbro lawrenzo wannabe sentinel machiavelli groot; do
  chown -R hermes-bot:hermes-bot <HERMES_ROOT>/profiles/$profile
done
chown -R hermes-bot:hermes-bot <HERMES_ROOT>/shared
```

**Pitfall**: Do NOT give `NOPASSWD: ALL` — limits blast radius. The commands above cover: file copy/move, ownership changes, systemctl restart/enable/disable, and Python script execution. That's enough for bot management.

**Pitfall**: `hermes-bot` cannot edit `/etc/` config files, restart nginx, or modify the backend. If those are needed, add specific commands to the sudoers file (e.g., `/usr/bin/vim`, `/usr/sbin/nginx`). Prefer narrow additions over broad `ALL`.

## Architettura di Isolamento (2026-06-08)

Vedi `references/isolation-architecture.md` per dettagli completi.

**Tier knowledge** (filesystem ACL):
- `personal/` → root:root 750 (solo GribbitO)
- `business/` → hermes-bot:hermesbro 750 (bot business)
- `shared/` → hermes-bot:hermesbro 750 (tutti)

**DB cifrati**: LUKS2 512MB su `/mnt/hermesbro-encrypted`, 10 state.db per bot business. Auto-mount al boot.

**GribbitO = root** (decisione confermata). NON flaggare come rischio.

## LUKS2 Encrypted Volume for Bot State

When multiple bots need encrypted-at-rest session DBs without filesystem-level encryption (gocryptfs/ecryptfs unavailable):

```bash
# 1. Create container
dd if=/dev/zero of=/root/hermesbro-crypt.img bs=1M count=512
cryptsetup luksFormat /root/hermesbro-crypt.img
cryptsetup luksOpen /root/hermesbro-crypt.img hermesbro-crypt
mkfs.ext4 /dev/mapper/hermesbro-crypt
mount /dev/mapper/hermesbro-crypt /mnt/hermesbro-encrypted

# 2. Create per-bot directories
for profile in sentinel machiavelli lawrenzo contabile mr-robot ducato wannabe frank groot designbro; do
  mkdir -p /mnt/hermesbro-encrypted/$profile
done
chown -R hermes-bot:hermesbro /mnt/hermesbro-encrypted/

# 3. Symlink state.db from each profile to encrypted volume
for profile in <list>; do
  rm -f <HERMES_BOT>/.hermes/profiles/$profile/state.db
  ln -sf /mnt/hermesbro-encrypted/$profile/state.db <HERMES_BOT>/.hermes/profiles/$profile/state.db
done

# 4. Auto-mount at boot — add to /etc/crypttab and /etc/fstab
echo "hermesbro-crypt /root/hermesbro-crypt.img none luks" >> /etc/crypttab
echo "/dev/mapper/hermesbro-crypt /mnt/hermesbro-encrypted ext4 defaults 0 2" >> /etc/fstab
```

**Pitfall:** LUKS passphrase at boot requires manual entry OR a keyfile. For unattended boot, store keyfile at `/etc/hermesbro/gcrypt.key` (mode 600, root-only) and reference it in crypttab: `hermesbro-crypt /root/hermesbro-crypt.img /etc/hermesbro/gcrypt.key luks`.

**Pitfall:** After creating symlinks, verify the service user (hermes-bot) can actually write to the encrypted mount. Run `sudo -u hermes-bot touch /mnt/hermesbro-encrypted/<profile>/test`.

**Reference:** `references/luks2-bot-encryption.md` — full setup walkthrough with troubleshooting.

## Tier Integrity Audit

Automated monitoring of knowledge tier permissions and system health. Script runs as cron, logs JSON to `/var/log/hermesbro-audit.jsonl`.

Checks:
1. **Tier permissions** — personal/ (root:root 750), business/ and shared/ (hermes-bot:hermesbro 750)
2. **Unauthorized files** — no root-owned files in business tier, no non-root files in personal tier
3. **LUKS mount** — `/mnt/hermesbro-encrypted` must be mounted; auto-remount if down
4. **Service health** — all hermes-*.service units must be active
5. **.env permissions** — all .env files must be mode 600
6. **Critical file checksums** — SHA256 baseline for facts.md, decisions.md, preferences.md; warn on unexpected changes

**Pitfall:** The audit should exclude services intentionally stopped (e.g., `hermes-bus-watcher` if removed). Maintain an exclusion list in the script.

**Reference:** `references/tier-integrity-audit.md` — script template and cron setup.

## Riferimenti

*   [Hermes Vault — Credential Storage]: `references/hermes-vault-setup.md`
*   [Nginx Security Headers patterns + CSP + SRI]: `references/nginx-security-headers.md`
*   [Istruzioni per trasferimento chiave privata SSH]: `references/ssh-key-transfer.md`
*   [VPS Security Audit — Quick Checklist (read-only)]: `references/vps-audit-checklist.md`
*   [VPS Security Audit Checklist (comandi + scoring)]: `references/vps-audit-checklist.md`
*   [Security Tools Installation (lynis, rkhunter, clamav, aide, nmap)]: `references/security-tools-installation.md`
*   [Remote Agent SSH Access (dedicated user + limited sudoers)]: `references/remote-agent-ssh-access.md`
*   [Nginx Health Check Debugging (false positives, hairpin NAT, config pitfalls)]: `references/nginx-health-check-debugging.md`
*   [LUKS2 Bot Encryption Setup]: `references/luks2-bot-encryption.md`
*   [Tier Integrity Audit]: `references/tier-integrity-audit.md`
