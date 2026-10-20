#!/usr/bin/env python3
# Genera la tabla del Punto 2 (hop x protocolo, con AS) por cada destino.
import json, os, re

JBASE = "/home/kali/Tarea_Ruteo/evidencia_ripe/json"
DEST = {"valparaiso": "138.204.228.2", "habana": "200.14.48.134", "rusia": "37.79.153.66"}
PROTOS = ["icmp", "udp", "tcp"]

# cargar ASN de cymru
asn = {}
for line in open("/tmp/ripe_asn.txt"):
    parts = [p.strip() for p in line.split("|")]
    if len(parts) >= 7 and re.match(r"\d+|NA", parts[0]):
        a, ip = parts[0], parts[1]
        if ip == "IP":
            continue
        asn[ip] = a

def astag(ip):
    if ip == "*":
        return ""
    if re.match(r"^(10\.|192\.168\.|172\.1[6-9]\.|172\.2[0-9]\.|172\.3[01]\.|100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.)", ip):
        return "priv"
    a = asn.get(ip, "?")
    return a if a != "NA" else "priv"

def hops_of(path):
    data = json.load(open(path)); r = data[0]
    out = {}
    for h in r.get("result", []):
        ips = [x.get("from") for x in h.get("result", []) if x.get("from")]
        out[h.get("hop")] = ips[0] if ips else "*"
    return out

for label, ip in DEST.items():
    data = {p: hops_of(os.path.join(JBASE, f"ripe_{label}_{p}.json")) for p in PROTOS}
    realhops = [h for p in PROTOS for h in data[p] if h != 255]
    maxhop = max(realhops) if realhops else 0
    print(f"\n### Destino {label}  (`{ip}`)\n")
    print("| HOP | ICMP (AS) | UDP (AS) | TCP (AS) |")
    print("|---|---|---|---|")
    for h in range(1, maxhop + 1):
        row = [str(h)]
        for p in PROTOS:
            v = data[p].get(h, "")
            if v and v != "*":
                row.append(f"{v} ({astag(v)})")
            else:
                row.append(v)
        print("| " + " | ".join(row) + " |")
    # resumen
    print("\n**Resumen:**")
    print("| Protocolo | Hops con respuesta | ¿Llega? |")
    print("|---|---|---|")
    for p in PROTOS:
        resp = sum(1 for k, v in data[p].items() if v != "*" and k != 255)
        reaches = any(v == ip for v in data[p].values())
        print(f"| {p.upper()} | {resp} | {'Sí' if reaches else 'No'} |")
