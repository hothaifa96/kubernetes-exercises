#!/usr/bin/env python3
"""
Health Check Backend Script
This script performs health checks on various services
"""

import requests
import socket
from datetime import datetime
import json

def check_http_service(url, name):
    """Check if an HTTP service is accessible"""
    try:
        response = requests.get(url, timeout=5)
        return {
            "service": name,
            "url": url,
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "http_code": response.status_code,
            "response_time": response.elapsed.total_seconds()
        }
    except Exception as e:
        return {
            "service": name,
            "url": url,
            "status": "error",
            "error": str(e)
        }

def check_dns_resolution(hostname):
    """Check DNS resolution"""
    try:
        ip = socket.gethostbyname(hostname)
        return {
            "hostname": hostname,
            "status": "resolved",
            "ip_address": ip
        }
    except Exception as e:
        return {
            "hostname": hostname,
            "status": "failed",
            "error": str(e)
        }

def main():
    print("=" * 60)
    print("Health Check CronJob - Backend")
    print("=" * 60)
    print()
    
    print(f"Starting health checks at {datetime.now().isoformat()}")
    print()
    
    # Perform health checks
    checks = []
    
    # HTTP Service Checks
    print("1. HTTP Service Checks:")
    checks.append(check_http_service("https://www.google.com", "Google"))
    checks.append(check_http_service("https://httpbin.org/status/200", "HTTPBin"))
    
    for check in checks[-2:]:
        print(f"   {check['service']}: {check.get('status', 'unknown')}")
    
    print()
    
    # DNS Checks
    print("2. DNS Resolution Checks:")
    dns_checks = [
        check_dns_resolution("kubernetes.default.svc"),
        check_dns_resolution("google.com")
    ]
    
    for dns_check in dns_checks:
        print(f"   {dns_check['hostname']}: {dns_check['status']}")
    
    print()
    
    # Summary
    print("3. Health Check Summary:")
    all_checks = checks + dns_checks
    healthy = sum(1 for c in all_checks if c.get('status') in ['healthy', 'resolved'])
    total = len(all_checks)
    
    print(f"   Total checks: {total}")
    print(f"   Healthy: {healthy}")
    print(f"   Unhealthy: {total - healthy}")
    
    print()
    print("=" * 60)
    print("Health check completed!")
    print("=" * 60)
    
    # Return exit code based on health
    return 0 if healthy == total else 1

if __name__ == "__main__":
    exit(main())
