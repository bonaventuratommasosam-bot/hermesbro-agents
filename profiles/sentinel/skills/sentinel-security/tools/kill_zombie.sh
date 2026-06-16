#!/bin/bash
# Sentinel: Find and kill zombie/orphan processes
set -euo pipefail

DRY_RUN=false
[ "${1:-}" = "--dry-run" ] && DRY_RUN=true

echo "=== ZOMBIE/ORPHAN PROCESS CHECK — $(date '+%Y-%m-%d %H:%M:%S') ==="
[ "$DRY_RUN" = true ] && echo "(DRY RUN — no processes will be killed)"
echo ""

KILLED=0

# 1. Zombie processes (state Z)
echo "--- Zombie Processes (state Z) ---"
ZOMBIES=$(ps aux 2>/dev/null | awk '$8 ~ /Z/ {print $2, $11, $12}' || true)
if [ -n "$ZOMBIES" ]; then
    echo "$ZOMBIES" | while read -r pid cmd args; do
        echo "  ⚠️  PID $pid: $cmd $args"
        if [ "$DRY_RUN" = false ]; then
            kill -9 "$pid" 2>/dev/null && echo "    🔧 Killed PID $pid" || echo "    ❌ Failed to kill PID $pid"
            KILLED=$((KILLED + 1))
        fi
    done
else
    echo "  ✅ No zombie processes found"
fi

# 2. Orphaned hermes processes (no parent systemd)
echo ""
echo "--- Orphaned Hermes Processes ---"
HERMES_PROCS=$(pgrep -af "hermes.*gateway" 2>/dev/null || true)
if [ -n "$HERMES_PROCS" ]; then
    # Get PIDs managed by systemd
    SYSTEMD_PIDS=""
    for svc in $(systemctl list-units --type=service --state=running --no-legend 2>/dev/null | grep hermes | awk '{print $1}'); do
        main_pid=$(systemctl show "$svc" --property=MainPID --value 2>/dev/null || echo "")
        [ -n "$main_pid" ] && [ "$main_pid" != "0" ] && SYSTEMD_PIDS="$SYSTEMD_PIDS $main_pid"
    done

    echo "$HERMES_PROCS" | while read -r pid cmd; do
        if echo "$SYSTEMD_PIDS" | grep -qw "$pid"; then
            echo "  ✅ PID $pid: managed by systemd ($cmd)"
        else
            echo "  ⚠️  PID $pid: ORPHAN ($cmd)"
            if [ "$DRY_RUN" = false ]; then
                kill -15 "$pid" 2>/dev/null && echo "    🔧 Sent SIGTERM to PID $pid" || echo "    ❌ Failed to kill PID $pid"
                KILLED=$((KILLED + 1))
            fi
        fi
    done
else
    echo "  ✅ No orphaned hermes processes"
fi

# 3. Defunct / stale gateway locks
echo ""
echo "--- Stale Gateway Locks ---"
for profile_dir in $HERMES_PROFILES_DIR/*/; do
    profile=$(basename "$profile_dir")
    lockfile="$profile_dir/gateway.lock"
    if [ -f "$lockfile" ]; then
        lock_pid=$(cat "$lockfile" 2>/dev/null || echo "")
        if [ -n "$lock_pid" ] && ! kill -0 "$lock_pid" 2>/dev/null; then
            echo "  ⚠️  $profile: stale lock (PID $lock_pid not running)"
            if [ "$DRY_RUN" = false ]; then
                rm -f "$lockfile"
                echo "    🔧 Removed stale lock"
            fi
        elif [ -n "$lock_pid" ]; then
            echo "  ✅ $profile: lock active (PID $lock_pid)"
        fi
    fi
done

# 4. High-CPU processes (>80% for extended time)
echo ""
echo "--- High CPU Processes (>80%) ---"
HIGH_CPU=$(ps aux 2>/dev/null | awk 'NR>1 && $3>80 {printf "  ⚠️  PID %s (%.0f%% CPU): %s\n", $2, $3, $11}')
if [ -n "$HIGH_CPU" ]; then
    echo "$HIGH_CPU"
else
    echo "  ✅ No high-CPU processes"
fi

echo ""
echo "Zombie/orphan check complete."
