#!/bin/bash

TARGET="${TARGET:-localhost}"
# x = x if x else 'localhost'

echo "Starting network probe loop"
echo "Target: $TARGET"
echo "Press Ctrl+C to stop ......... "
echo ""

while true; do
    echo "========================================"
    echo "  Timestamp : $(date -u)"
    echo "  Target    : $TARGET"
    echo "========================================"

    echo ""
    echo "--- PING ---"
    ping -c 3 -W 2 "$TARGET" 2>&1 || \
        echo "[INFO] Ping did not get response — ClusterIP services may not respond to ICMP. This is expected."

    echo ""
    echo "--- CURL ---"
    curl -s --connect-timeout 5 --max-time 10 "http://$TARGET" 2>&1 || \
        echo "[WARN] curl failed — is the service running and the TARGET correct?"

    echo ""
    sleep 5
done
