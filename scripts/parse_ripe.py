#!/usr/bin/env python3
# Parsea los JSON de RIPE (Punto 2) y arma rutas hop->IP, sin ASN (el ASN se agrega aparte).
import json, os, re

BASE = "/home/kali/Tarea_Ruteo/evidencia_ripe/json"
DEST = {"valparaiso": "138.204.228.2", "habana": "200.14.48.134", "rusia": "37.79.153.66"}
PROTOS = ["icmp", "udp", "tcp"]

def hops_of(path):
    """devuelve lista [(hop, ip_o_*)] tomando la IP mas comun del hop."""
    data = json.load(open(path))
    r = data[0]
    out = []
    for h in r.get("result", []):
        hop = h.get("hop")
        ips = [x.get("from") for x in h.get("result", []) if x.get("from")]
        ip = ips[0] if ips else "*"
        out.append((hop, ip))
    return out, r.get("from"), r.get("prb_id")

allips = set()
routes = {}
for label, ip in DEST.items():
    for p in PROTOS:
        f = os.path.join(BASE, f"ripe_{label}_{p}.json")
        if not os.path.exists(f):
            continue
        hops, src, prb = hops_of(f)
        routes[(label, p)] = (hops, src, prb)
        for _, hip in hops:
            if hip != "*":
                allips.add(hip)

# volcar IPs para cymru
open("/tmp/ripe_ips.txt", "w").write("\n".join(sorted(allips)) + "\n")
print("IPs unicas:", len(allips))
for (label, p), (hops, src, prb) in routes.items():
    print(f"\n### {label} / {p}  (probe {prb}, src {src})")
    for hop, hip in hops:
        print(f"  {hop}: {hip}")
