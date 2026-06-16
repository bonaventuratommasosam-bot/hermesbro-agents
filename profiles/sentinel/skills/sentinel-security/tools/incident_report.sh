#!/bin/bash
# Sentinel: Generate structured incident report from recent logs
set -euo pipefail

HOURS="${1:-24}"
REPORT_DIR="$HOME/incident-reports"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
REPORT_FILE="$REPORT_DIR/incident-$TIMESTAMP.md"

mkdir -p "$REPORT_DIR"

echo "=== INCIDENT REPORT — $(date '+%Y-%m-%d %H:%M:%S') ==="
echo "Period: last $HOURS hours"
echo ""

# Start building report
cat > "$REPORT_FILE" << EOF
# Sentinel Incident Report
**Generated:** $(date '+%Y-%m-%d %H:%M:%S')
**Period:** Last $HOURS hours
**Host:** $(hostname)
**IP:** $(hostname -I 2>/dev/null | awk '{print $1}')

---

EOF

FINDINGS=0

# 1. Failed SSH attempts
echo "## Failed SSH Attempts" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
ssh_failed=0
for logfile in /var/log/auth.log /var/log/secure; do
    [ -f "$logfile" ] || continue
    count=$(journalctl --since "$HOURS hours ago" -u sshd 2>/dev/null | grep -ci "failed\|invalid" || echo 0)
    ssh_failed=$((ssh_failed + count))
done

if [ "$ssh_failed" -gt 0 ]; then
    echo "- **Total failed attempts:** $ssh_failed" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "- **Top attacking IPs:**" >> "$REPORT_FILE"
    journalctl --since "$HOURS hours ago" 2>/dev/null | grep -i "failed password" | \
        grep -oP 'from \K\S+' | sort | uniq -c | sort -rn | head -10 | \
        while read -r cnt ip; do
            echo "  - \`$ip\`: $cnt attempts" >> "$REPORT_FILE"
        done
    echo "  ⚠️  $ssh_failed failed SSH attempts"
    FINDINGS=$((FINDINGS + 1))
else
    echo "- No failed SSH attempts detected." >> "$REPORT_FILE"
    echo "  ✅ No failed SSH attempts"
fi

echo "" >> "$REPORT_FILE"

# 2. Service failures
echo "## Service Failures" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
svc_failures=$(journalctl --since "$HOURS hours ago" -p err --no-pager 2>/dev/null | grep -c "systemd" || echo 0)
if [ "$svc_failures" -gt 0 ]; then
    echo "- **Error entries from systemd:** $svc_failures" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "- **Recent service errors:**" >> "$REPORT_FILE"
    journalctl --since "$HOURS hours ago" -p err --no-pager 2>/dev/null | grep "systemd" | tail -10 | \
        while IFS= read -r line; do
            echo "  \`\`\`" >> "$REPORT_FILE"
            echo "  $line" >> "$REPORT_FILE"
            echo "  \`\`\`" >> "$REPORT_FILE"
        done
    echo "  ⚠️  $svc_failures systemd error entries"
    FINDINGS=$((FINDINGS + 1))
else
    echo "- No service failures detected." >> "$REPORT_FILE"
    echo "  ✅ No service failures"
fi

echo "" >> "$REPORT_FILE"

# 3. Disk pressure
echo "## Disk Usage" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
disk_pct=$(df / 2>/dev/null | awk 'NR==2 {gsub(/%/,""); print $5}')
echo "- Root partition: ${disk_pct}% used" >> "$REPORT_FILE"
if [ "${disk_pct:-0}" -gt 80 ]; then
    echo "- **WARNING: Disk usage above 80%**" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "- Largest directories:" >> "$REPORT_FILE"
    du -sh /var/log /root /home /tmp 2>/dev/null | sort -rh | head -5 | \
        while read -r size dir; do
            echo "  - \`$dir\`: $size" >> "$REPORT_FILE"
        done
    echo "  ⚠️  Disk at ${disk_pct}%"
    FINDINGS=$((FINDINGS + 1))
else
    echo "  ✅ Disk OK at ${disk_pct}%"
fi

echo "" >> "$REPORT_FILE"

# 4. Suspicious processes
echo "## Suspicious Activity" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# High CPU processes
high_cpu=$(ps aux 2>/dev/null | awk 'NR>1 && $3>50 {printf "- PID %s (%.0f%% CPU): %s\n", $2, $3, $11}')
if [ -n "$high_cpu" ]; then
    echo "### High CPU Processes" >> "$REPORT_FILE"
    echo "$high_cpu" >> "$REPORT_FILE"
    echo "  ⚠️  High CPU processes detected"
    FINDINGS=$((FINDINGS + 1))
fi

# Outbound connections to unusual ports
echo "" >> "$REPORT_FILE"
echo "### Outbound Connections" >> "$REPORT_FILE"
unusual_outbound=$(ss -tn state established 2>/dev/null | awk 'NR>1 {print $5}' | grep -vP ':(80|443|22|53)$' | head -10)
if [ -n "$unusual_outbound" ]; then
    echo "- Unusual outbound connections:" >> "$REPORT_FILE"
    echo "$unusual_outbound" | while IFS= read -r conn; do
        echo "  - \`$conn\`" >> "$REPORT_FILE"
    done
    echo "  ⚠️  Unusual outbound connections"
    FINDINGS=$((FINDINGS + 1))
else
    echo "- No unusual outbound connections." >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"

# 5. Blocked IPs (from sentinel log)
echo "## Blocked IPs" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
if [ -f /var/log/sentinel-blocks.log ]; then
    recent_blocks=$(tail -20 /var/log/sentinel-blocks.log 2>/dev/null)
    if [ -n "$recent_blocks" ]; then
        echo '```' >> "$REPORT_FILE"
        echo "$recent_blocks" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
    else
        echo "- No IPs blocked in this period." >> "$REPORT_FILE"
    fi
else
    echo "- No block log found." >> "$REPORT_FILE"
fi

# Summary
echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## Summary" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "- **Findings:** $FINDINGS" >> "$REPORT_FILE"
if [ "$FINDINGS" -eq 0 ]; then
    echo "- **Status:** ✅ No issues detected" >> "$REPORT_FILE"
elif [ "$FINDINGS" -le 2 ]; then
    echo "- **Status:** ⚠️ Minor issues — review recommended" >> "$REPORT_FILE"
else
    echo "- **Status:** ❌ Multiple issues — immediate review required" >> "$REPORT_FILE"
fi

echo ""
echo "Report saved: $REPORT_FILE"
echo "Findings: $FINDINGS"
