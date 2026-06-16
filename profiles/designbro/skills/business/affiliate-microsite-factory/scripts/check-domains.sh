#!/bin/bash
# Check .it domain availability in bulk
# Usage: bash check-domains.sh domain1.it domain2.it domain3.it
# Or:    bash check-domains.sh (reads from domains.txt, one per line)

if [ $# -gt 0 ]; then
    domains=("$@")
else
    if [ -f "domains.txt" ]; then
        mapfile -t domains < domains.txt
    else
        echo "Usage: bash check-domains.sh domain1.it domain2.it ..."
        echo "Or create domains.txt with one domain per line"
        exit 1
    fi
fi

echo "=== Domain Availability Check ==="
echo ""

available=()
taken=()

for d in "${domains[@]}"; do
    status=$(whois "$d" 2>/dev/null | grep -i "Status:" | head -1 | awk '{print $2}')
    if [ "$status" = "AVAILABLE" ]; then
        echo "✅ $d — AVAILABLE"
        available+=("$d")
    elif [ "$status" = "ok" ] || [ -n "$status" ]; then
        echo "❌ $d — REGISTERED ($status)"
        taken+=("$d")
    else
        echo "⚠️  $d — UNKNOWN (check manually)"
    fi
done

echo ""
echo "=== Summary ==="
echo "Available: ${#available[@]}"
echo "Registered: ${#taken[@]}"
echo ""
if [ ${#available[@]} -gt 0 ]; then
    echo "Available domains:"
    for d in "${available[@]}"; do
        echo "  → $d"
    done
fi
