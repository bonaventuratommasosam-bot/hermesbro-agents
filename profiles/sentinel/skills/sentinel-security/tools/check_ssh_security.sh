#!/bin/bash
# Sentinel: Audit SSH configuration security
set -euo pipefail

echo "=== SSH SECURITY AUDIT — $(date '+%Y-%m-%d %H:%M:%S') ==="
echo ""

SSHD_CONFIG="/etc/ssh/sshd_config"
ISSUES=0

if [ ! -f "$SSHD_CONFIG" ]; then
    echo "❌ sshd_config not found at $SSHD_CONFIG"
    exit 1
fi

echo "--- sshd_config Analysis ---"

# Helper: get effective sshd setting (handles Include directives)
get_setting() {
    local key="$1"
    local val
    # Check main config
    val=$(grep -iP "^\s*$key\s" "$SSHD_CONFIG" 2>/dev/null | tail -1 | awk '{print $2}')
    # Also check included configs
    if [ -z "$val" ]; then
        for inc in $(grep -iP '^\s*Include\s' "$SSHD_CONFIG" | awk '{print $2}' | sed 's|\*||g'); do
            if [ -d "$inc" ]; then
                val=$(grep -rhiP "^\s*$key\s" "$inc" 2>/dev/null | tail -1 | awk '{print $2}')
                [ -n "$val" ] && break
            fi
        done
    fi
    echo "${val:-not set}"
}

# Root login
root_login=$(get_setting "PermitRootLogin")
if echo "$root_login" | grep -qiE "^no$|^prohibit-password$"; then
    echo "  ✅ PermitRootLogin: $root_login"
else
    echo "  ⚠️  PermitRootLogin: ${root_login:-not set (default: yes)} — should be 'no' or 'prohibit-password'"
    ISSUES=$((ISSUES + 1))
fi

# Password auth
pass_auth=$(get_setting "PasswordAuthentication")
if echo "$pass_auth" | grep -qi "^no$"; then
    echo "  ✅ PasswordAuthentication: no"
else
    echo "  ⚠️  PasswordAuthentication: ${pass_auth:-not set (default: yes)} — recommend 'no' with key auth"
    ISSUES=$((ISSUES + 1))
fi

# Pubkey auth
pubkey_auth=$(get_setting "PubkeyAuthentication")
if echo "$pubkey_auth" | grep -qi "^yes$"; then
    echo "  ✅ PubkeyAuthentication: yes"
elif [ "$pubkey_auth" = "not set" ]; then
    echo "  ✅ PubkeyAuthentication: not set (default: yes)"
else
    echo "  ⚠️  PubkeyAuthentication: $pubkey_auth — should be yes"
    ISSUES=$((ISSUES + 1))
fi

# Max auth tries
max_auth=$(get_setting "MaxAuthTries")
echo "  📊 MaxAuthTries: ${max_auth:-not set (default: 6)}"

# Login grace time
grace=$(get_setting "LoginGraceTime")
echo "  📊 LoginGraceTime: ${grace:-not set (default: 120)}"

# Empty passwords
empty_pass=$(get_setting "PermitEmptyPasswords")
if echo "$empty_pass" | grep -qi "^no$"; then
    echo "  ✅ PermitEmptyPasswords: no"
elif [ "$empty_pass" = "not set" ]; then
    echo "  ✅ PermitEmptyPasswords: not set (default: no)"
else
    echo "  ❌ PermitEmptyPasswords: $empty_pass — should be no"
    ISSUES=$((ISSUES + 1))
fi

# X11 forwarding
x11=$(get_setting "X11Forwarding")
if echo "$x11" | grep -qi "^no$"; then
    echo "  ✅ X11Forwarding: no"
else
    echo "  ⚠️  X11Forwarding: ${x11:-not set (default: no)}"
fi

echo ""
echo "--- SSH Key Audit ---"

# Check for authorized_keys files
for user_dir in /root /home/*; do
    [ -d "$user_dir" ] || continue
    user=$(basename "$user_dir")
    ak_file="$user_dir/.ssh/authorized_keys"

    if [ -f "$ak_file" ]; then
        key_count=$(grep -c '^ssh-\|^ecdsa-\|^sk-' "$ak_file" 2>/dev/null || echo 0)
        echo "  $user: $key_count key(s) in authorized_keys"

        # Check authorized_keys permissions
        ak_perms=$(stat -c '%a' "$ak_file" 2>/dev/null || echo "???")
        if [ "$ak_perms" != "600" ] && [ "$ak_perms" != "644" ]; then
            echo "    ⚠️  authorized_keys permissions: $ak_perms (should be 600)"
            ISSUES=$((ISSUES + 1))
        fi

        # Check .ssh dir permissions
        ssh_perms=$(stat -c '%a' "$user_dir/.ssh" 2>/dev/null || echo "???")
        if [ "$ssh_perms" != "700" ]; then
            echo "    ⚠️  .ssh directory permissions: $ssh_perms (should be 700)"
            ISSUES=$((ISSUES + 1))
        fi
    fi
done

echo ""
echo "--- Active SSH Sessions ---"
who 2>/dev/null || echo "  (who command not available)"

echo ""
echo "--- Recent Failed SSH Attempts ---"
if [ -f /var/log/auth.log ]; then
    failed=$(grep -c "Failed password" /var/log/auth.log 2>/dev/null || echo 0)
    echo "  Failed password attempts (total): $failed"

    echo "  Top 5 attacking IPs:"
    grep "Failed password" /var/log/auth.log 2>/dev/null | \
        grep -oP 'from \K\S+' | sort | uniq -c | sort -rn | head -5 | \
        while read -r count ip; do
            echo "    $ip: $count attempts"
        done
elif [ -f /var/log/secure ]; then
    failed=$(grep -c "Failed password" /var/log/secure 2>/dev/null || echo 0)
    echo "  Failed password attempts: $failed"
fi

echo ""
if [ "$ISSUES" -gt 0 ]; then
    echo "⚠️  $ISSUES SSH security issue(s) found."
else
    echo "✅ SSH configuration looks secure."
fi
