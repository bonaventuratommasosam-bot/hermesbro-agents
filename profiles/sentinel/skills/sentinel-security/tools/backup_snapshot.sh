#!/bin/bash
# Sentinel: Create backup snapshot of critical configs
set -euo pipefail

BACKUP_DIR="${1:-$HOME/backups}"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="$BACKUP_DIR/sentinel-backup-$TIMESTAMP.tar.gz"

echo "=== BACKUP SNAPSHOT — $(date '+%Y-%m-%d %H:%M:%S') ==="
echo ""

mkdir -p "$BACKUP_DIR"

# Collect files to back up
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "--- Collecting critical configs ---"

# nginx configs
if [ -d /etc/nginx ]; then
    mkdir -p "$TEMP_DIR/nginx"
    cp -r /etc/nginx/sites-enabled "$TEMP_DIR/nginx/" 2>/dev/null || true
    cp /etc/nginx/nginx.conf "$TEMP_DIR/nginx/" 2>/dev/null || true
    echo "  ✅ nginx configs"
fi

# SSH config
mkdir -p "$TEMP_DIR/ssh"
cp /etc/ssh/sshd_config "$TEMP_DIR/ssh/" 2>/dev/null || true
echo "  ✅ sshd_config"

# systemd service files
mkdir -p "$TEMP_DIR/systemd"
for svc in /etc/systemd/system/hermes-*.service; do
    [ -f "$svc" ] && cp "$svc" "$TEMP_DIR/systemd/" 2>/dev/null
done
echo "  ✅ Hermes service files"

# Hermes profile configs (NOT state.db — too large)
mkdir -p "$TEMP_DIR/profiles"
for profile_dir in $HERMES_PROFILES_DIR/*/; do
    profile=$(basename "$profile_dir")
    mkdir -p "$TEMP_DIR/profiles/$profile"
    cp "$profile_dir/config.yaml" "$TEMP_DIR/profiles/$profile/" 2>/dev/null || true
    cp "$profile_dir/.env" "$TEMP_DIR/profiles/$profile/" 2>/dev/null || true
    cp "$profile_dir/SOUL.md" "$TEMP_DIR/profiles/$profile/" 2>/dev/null || true
    cp "$profile_dir/channel_directory.json" "$TEMP_DIR/profiles/$profile/" 2>/dev/null || true
done
echo "  ✅ Hermes profile configs"

# iptables rules
mkdir -p "$TEMP_DIR/firewall"
iptables-save > "$TEMP_DIR/firewall/iptables-rules.v4" 2>/dev/null || true
echo "  ✅ iptables rules"

# Start scripts
mkdir -p "$TEMP_DIR/scripts"
cp $HOME/hermes-*-start.sh "$TEMP_DIR/scripts/" 2>/dev/null || true
echo "  ✅ Start scripts"

# crontab
crontab -l > "$TEMP_DIR/crontab-root.txt" 2>/dev/null || true
echo "  ✅ Crontab"

# Package list
dpkg --get-selections > "$TEMP_DIR/packages.txt" 2>/dev/null || true
echo "  ✅ Package list"

# Blocked IPs
cp /etc/sentinel-blocked-ips.txt "$TEMP_DIR/" 2>/dev/null || true

# Create tarball
echo ""
echo "--- Creating backup ---"
tar czf "$BACKUP_FILE" -C "$TEMP_DIR" .
SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "  ✅ Backup created: $BACKUP_FILE ($SIZE)"

# Cleanup old backups (keep last 7)
echo ""
echo "--- Cleanup (keeping last 7 backups) ---"
ls -t "$BACKUP_DIR"/sentinel-backup-*.tar.gz 2>/dev/null | tail -n +8 | while read -r old; do
    rm -f "$old"
    echo "  🗑️  Removed: $(basename "$old")"
done

echo ""
echo "Backup complete: $BACKUP_FILE"
