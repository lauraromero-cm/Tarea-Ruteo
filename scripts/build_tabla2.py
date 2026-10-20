#!/usr/bin/env python3
# Tabla 2 (con AS): IDA (sonda 1018349 -> destino) vs VUELTA (sonda destino -> 186.10.176.77)
import json, os, re

IDA = "/home/kali/Tarea_Ruteo/evidencia_ripe/json"
VUE = "/home/kali/Tarea_Ruteo/evidencia_ripe/json_vuelta"
DEST = {"valparaiso": "138.204.228.2", "habana": "200.14.48.134", "rusia": "37.79.153.66"}
PROTOS = ["icmp", "udp", "tcp"]

# cargar ASN (ida + vuelta)
asn = {}
for fn in ("/tmp/ripe_asn.txt", "/tmp/vuelta_asn.txt"):
    if not os.path.exists(fn): continue
    for line in open(fn):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 7 and parts[1] != "IP":
            asn[parts[1]] = parts[0]

def tag(ip):
    if ip in ("*", ""): return ip
    if re.match(r"^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.)", ip):
        return f"{ip} (priv)"
    a = asn.get(ip, "?")
    return f"{ip} ({'priv' if a in ('NA','?') else a})"

def hops(path):
    if not os.path.exists(path): return []
    d = json.load(open(path))
    if not d: return []
    out = []
    for h in d[0].get("result", []):
        if h.get("hop") == 255: continue
        ips = [x.get("from") for x in h.get("result", []) if x.get("from")]
        out.append(ips[0] if ips else "*")
    return out

for label, ip in DEST.items():
    print(f"\n### Destino {label} (`{ip}`)\n")
    for p in PROTOS:
        ida = hops(os.path.join(IDA, f"ripe_{label}_{p}.json"))
        vue = hops(os.path.join(VUE, f"vuelta_{label}_{p}.json"))
        ni = sum(1 for x in ida if x != "*"); nv = sum(1 for x in vue if x != "*")
        si = set(x for x in ida if x != "*"); sv = set(x for x in vue if x != "*")
        print(f"**{p.upper()}** — IDA {ni} IPs · VUELTA {nv} IPs · comunes {len(si&sv)}\n")
        print("| HOP | IP IDA (AS) | IP VUELTA (AS) |")
        print("|---|---|---|")
        for i in range(max(len(ida), len(vue))):
            a = tag(ida[i]) if i < len(ida) else ""
            b = tag(vue[i]) if i < len(vue) else ""
            print(f"| {i+1} | {a} | {b} |")
        print()
