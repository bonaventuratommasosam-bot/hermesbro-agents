# LUKS2 Bot Encryption — Setup Reference

## Context
HermesBro VPS runs 10+ bot profiles. Session databases (state.db) contain conversation history, memory, and user data. Needed encryption at-rest. gocryptfs/ecryptfs not available on the VPS. LUKS2 with a file container was the solution.

## Architecture
- Container: `/root/hermesbro-crypt.img` (512MB LUKS2)
- Mapper: `/dev/mapper/hermesbro-crypt`
- Mount: `/mnt/hermesbro-encrypted` (ext4)
- Per-bot dirs: `/mnt/hermesbro-encrypted/<profile>/state.db`
- Symlinks: each profile's `state.db` → encrypted mount
- Auto-mount: crypttab + fstab with keyfile

## Keyfile for Unattended Boot
```bash
# Generate keyfile
dd if=/dev/urandom of=/etc/hermesbro/gcrypt.key bs=4096 count=1
chmod 600 /etc/hermesbro/gcrypt.key
chown root:root /etc/hermesbro/gcrypt.key

# Add key to LUKS container
cryptsetup luksAddKey /root/hermesbro-crypt.img /etc/hermesbro/gcrypt.key

# crypttab entry
hermesbro-crypt /root/hermesbro-crypt.img /etc/hermesbro/gcrypt.key luks
```

## Verification Commands
```bash
# Is it mounted?
mount | grep hermesbro-crypt
dmsetup ls | grep hermesbro

# Can hermes-bot write?
sudo -u hermes-bot touch /mnt/hermesbro-encrypted/test && echo "OK"

# Symlinks intact?
for profile in sentinel machiavelli lawrenzo contabile mr-robot ducato wannabe frank groot designbro; do
  ls -la <HERMES_BOT>/.hermes/profiles/$profile/state.db
done
```

## Pitfalls
- **keyfile permissions**: MUST be 600 root-only. If hermes-bot can read it, the encryption is theater.
- **symlink vs copy**: symlinks are correct — the state.db lives ONLY on the encrypted volume. If the mount fails, the bot fails (which is the desired behavior — fail closed, not open).
- **container size**: 512MB holds ~10 state.db files. Monitor with `df -h /mnt/hermesbro-encrypted`. Resize with `cryptsetup resize` + `resize2fs` if needed.
- **backup**: the LUKS container file itself should be backed up (encrypted backup). If the container is lost, all session data is lost.
- **audit script**: the tier-integrity-audit checks that `/mnt/hermesbro-encrypted` is mounted. If not mounted, triggers auto-remount attempt + CRITICAL alert on Telegram.
