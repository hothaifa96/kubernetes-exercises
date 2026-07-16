#!/bin/bash

# This script demonstrates a simple bash job in Kubernetes
# It performs system checks and outputs results

echo "=========================================="
echo "Kubernetes Job - Bash Script Execution"
echo "=========================================="
echo ""

echo "1. System Information:"
uname -a
echo ""

echo "2. Current Date and Time:"
date
echo ""

echo "3. Available Memory:"
free -h || echo "free command not available"
echo ""

echo "4. Disk Space:"
df -h || echo "df command not available"
echo ""

echo "5. CPU Information:"
nproc || echo "nproc command not available"
echo ""

echo "6. Network Test:"
curl -I https://www.google.com || echo "curl command not available"
echo ""

echo "=========================================="
echo "Job completed successfully!"
echo "=========================================="
