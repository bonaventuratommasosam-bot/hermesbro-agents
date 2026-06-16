#!/bin/bash
# Sentinel: Scan project dependencies for known vulnerabilities
set -euo pipefail

SCAN_DIR="${1:-/path/to/project}"
echo "=== DEPENDENCY SCAN — $(date '+%Y-%m-%d %H:%M:%S') ==="
echo "Scanning: $SCAN_DIR"
echo ""

TOTAL_VULNS=0

# Python projects
echo "--- Python (pip) ---"
find "$SCAN_DIR" -name "requirements.txt" -o -name "Pipfile" -o -name "pyproject.toml" 2>/dev/null | while read -r f; do
    dir=$(dirname "$f")
    echo "  📁 $dir"

    if command -v pip-audit &>/dev/null; then
        result=$(cd "$dir" && pip-audit 2>/dev/null || true)
        if [ -n "$result" ]; then
            echo "$result" | head -20
        else
            echo "  ✅ No known vulnerabilities"
        fi
    elif command -v safety &>/dev/null; then
        (cd "$dir" && safety check 2>/dev/null || echo "  ⚠️  safety check failed")
    else
        # Manual check: look for outdated/pinned versions
        if [ -f "$dir/requirements.txt" ]; then
            pinned=$(grep -cP '==' "$dir/requirements.txt" 2>/dev/null || echo 0)
            total=$(wc -l < "$dir/requirements.txt" 2>/dev/null || echo 0)
            echo "  📊 $pinned/$total packages pinned (no audit tool available)"
        fi
    fi
done

echo ""
echo "--- Node.js (npm) ---"
find "$SCAN_DIR" -name "package.json" -not -path "*/node_modules/*" 2>/dev/null | while read -r f; do
    dir=$(dirname "$f")
    echo "  📁 $dir"

    if [ -f "$dir/package-lock.json" ] || [ -f "$dir/yarn.lock" ]; then
        if command -v npm &>/dev/null; then
            result=$(cd "$dir" && npm audit --json 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    v = d.get('metadata', {}).get('vulnerabilities', {})
    total = sum(v.values()) if isinstance(v, dict) else 0
    if total > 0:
        print(f'  ⚠️  {total} vulnerabilities: {v}')
    else:
        print('  ✅ No known vulnerabilities')
except:
    print('  ⚠️  Could not parse audit results')
" 2>/dev/null || echo "  ⚠️  npm audit failed")
            echo "$result"
        fi
    else
        echo "  ⚠️  No lockfile — cannot audit"
    fi
done

echo ""
echo "--- Outdated System Packages ---"
if command -v apt &>/dev/null; then
    upgradable=$(apt list --upgradable 2>/dev/null | grep -c upgradable || echo 0)
    echo "  Packages with updates available: $upgradable"
    if [ "$upgradable" -gt 20 ]; then
        echo "  ⚠️  Many packages outdated — consider running apt upgrade"
    fi
fi

echo ""
echo "--- Docker Images ---"
if command -v docker &>/dev/null; then
    images=$(docker images --format '{{.Repository}}:{{.Tag}}' 2>/dev/null | wc -l)
    echo "  Docker images: $images"
    # Check for images with known CVEs if trivy is available
    if command -v trivy &>/dev/null; then
        echo "  Running trivy scan..."
        docker images --format '{{.Repository}}:{{.Tag}}' 2>/dev/null | head -5 | while read -r img; do
            trivy image --severity HIGH,CRITICAL "$img" 2>/dev/null | tail -5
        done
    fi
fi
