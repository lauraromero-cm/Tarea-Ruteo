#!/usr/bin/env bash
# Ejecutar DESPUES de cambiar a Bridged + renovar DHCP.
echo "=== IP eth0 ==="; ip -4 addr show eth0 | grep inet
echo "=== gateway ==="; ip route | grep default
echo "=== IP publica / ISP ==="; curl -s https://ifconfig.me; echo
echo "=== prueba traceroute ICMP (deben verse hops intermedios) ==="
scamper -O text -I "trace -P icmp 138.204.228.2" 2>&1 | head -20
