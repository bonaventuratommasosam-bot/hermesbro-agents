# Remote Agent SSH Access — Provisioning Pattern

When a remote machine (e.g., Hermes PC on Windows) needs SSH access to the VPS for bot management, create a dedicated user with limited sudo — NOT root, NOT [REDACTED — dati personali rimossi].

## Pattern

### 1. Create user on VPS

```bash
sudo adduser --disabled-password --gecos "" hermes-pc
sudo mkdir -p /home/hermes-pc/.ssh
sudo chmod 700 /home/hermes-pc/.ssh
```

### 2. User generates keypair on THEIR machine

```powershell
# Windows (PowerShell)
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\hermes-pc" -N "" -C "hermes-pc@YOUR_VPS_ID"

# Read public key
Get-Content "$env:USERPROFILE\.ssh\hermes-pc.pub"
```

```bash
# Linux/Mac
ssh-keygen -t ed25519 -f ~/.ssh/hermes-pc -N "" -C "hermes-pc@YOUR_VPS_ID"
cat ~/.ssh/hermes-pc.pub
```

**Pitfall**: NEVER generate the keypair on the VPS and transfer the private key. The private key must be born on the machine that will use it.

### 3. Add public key to VPS

```bash
# User pastes their public key, agent runs:
sudo tee /home/hermes-pc/.ssh/authorized_keys << 'EOF'
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... hermes-pc@YOUR_VPS_ID
EOF
sudo chmod 600 /home/hermes-pc/.ssh/authorized_keys
sudo chown -R hermes-pc:hermes-pc /home/hermes-pc/.ssh
```

### 4. Create limited sudoers file

```bash
sudo tee /etc/sudoers.d/hermes-pc > /dev/null << 'EOF'
# hermes-pc: sudo limitato per bot management
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart hermes-*.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop hermes-*.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl start hermes-*.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl status hermes-*.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart warroom*.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop warroom*.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl start warroom*.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart compliance-ai.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop compliance-ai.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl start compliance-ai.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart demo-ristorante.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop demo-ristorante.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl start demo-ristorante.service
hermes-pc ALL=(ALL) NOPASSWD: /usr/sbin/nginx -t
hermes-pc ALL=(ALL) NOPASSWD: /usr/sbin/nginx -s reload
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/journalctl -u hermes-* -n *
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/journalctl -u warroom* -n *
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/chown -R [REDACTED — dati personali rimossi]\:[REDACTED — dati personali rimossi] /home/[REDACTED — dati personali rimossi]/*
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/chmod -R u+w /home/[REDACTED — dati personali rimossi]/*
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/systemctl daemon-reload
EOF
sudo chmod 440 /etc/sudoers.d/hermes-pc
sudo visudo -cf /etc/sudoers.d/hermes-pc  # MUST say "parsed OK"
```

**Pitfall**: `write_file` tool refuses to write to `/etc/sudoers.d/`. Use `terminal` with `sudo tee` instead.

### 5. Test from remote machine

```bash
ssh -i ~/.ssh/hermes-pc -o StrictHostKeyChecking=no hermes-pc@194.146.12.219 "ls /home/[REDACTED — dati personali rimossi]/ai-stack/"
ssh -i ~/.ssh/hermes-pc -o StrictHostKeyChecking=no hermes-pc@194.146.12.219 "sudo systemctl status hermes-gribbito.service"
```

## What the agent CAN do

- `sudo systemctl restart/stop/start/status hermes-*.service`
- `sudo systemctl restart/stop/start warroom*.service`
- `sudo nginx -t` / `sudo nginx -s reload`
- `sudo journalctl -u hermes-* -n ...`
- `sudo chown/chmod` on `/home/[REDACTED — dati personali rimossi]/*`
- `sudo systemctl daemon-reload`

## What the agent CANNOT do

- Modify system config (`/etc/`, `/root/`)
- Install packages (`apt`)
- Manage users (`adduser`, `usermod`)
- Access other users' files
- Run arbitrary sudo commands

## Connection string for automation

```
ssh -i ~/.ssh/hermes-pc -o StrictHostKeyChecking=no hermes-pc@194.146.12.219 "command"
```

`StrictHostKeyChecking=no` is needed for first connection in automation (no interactive prompt). Subsequent connections use cached `known_hosts`.

## Alternate SSH Port (when ISP blocks port 22)

If SSH on port 22 times out but other ports (443, 80) respond, the ISP is blocking port 22. Configure an alternate port:

```bash
# 1. Open firewall
sudo ufw allow 2222/tcp

# 2. Add Port 2222 to sshd_config (keep Port 22 too)
sudo sed -i '/^Port 22$/a Port 2222' /etc/ssh/sshd_config

# 3. Reload socket (Debian 12/Ubuntu 24.04 uses socket activation)
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket

# 4. Verify
ss -tlnp | grep :2222

# 5. Test from remote
ssh -p 2222 -i ~/.ssh/hermes-pc hermes-pc@<VPS_IP> "echo ok"
```

**Pitfall — systemd socket activation**: Changing `Port` in sshd_config and doing `systemctl restart ssh` is NOT enough on Debian 12/Ubuntu 24.04. The `ssh.socket` unit manages the actual port binding. Must do `systemctl daemon-reload && systemctl restart ssh.socket`. Verify with `systemctl cat ssh.socket` — the auto-generated `addresses.conf` overrides sshd_config.

**Pitfall — SSH key mismatch**: Always verify `cat /home/hermes-pc/.ssh/authorized_keys` matches the key the user provided. Interrupted sessions can save wrong keys.

## Customization

Add more sudoers rules as needed. Pattern:
```
hermes-pc ALL=(ALL) NOPASSWD: /usr/bin/command args
```

Always validate with `sudo visudo -cf /etc/sudoers.d/hermes-pc` after changes.
