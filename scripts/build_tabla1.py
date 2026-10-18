#!/usr/bin/env python3
# Construye la Tabla 1 (hop x metodo) por cada destino a partir de los .txt de scamper.
import os, re, sys

TXT = "/home/kali/Tarea_Ruteo/evidencia/txt"
DEST = {"valparaiso": "138.204.228.2", "habana": "200.14.48.134", "rusia": "37.79.153.66"}
METHODS = ["udp", "icmp", "udp-paris", "icmp-paris", "tcp", "tcp-ack"]

def parse(path):
    """devuelve dict hop->ip ('*' si no respondio). Marca [closed] si aparece."""
    hops = {}
    if not os.path.exists(path):
        return hops
    for line in open(path):
        m = re.match(r"\s*(\d+)\s+(.*)", line)
        if not m:
            continue
        hop = int(m.group(1)); rest = m.group(2).strip()
        if rest.startswith("*"):
            hops[hop] = "*"
        else:
            ip = rest.split()[0]
            if "[closed]" in rest:
                ip += " [c]"
            hops[hop] = ip
    return hops

for label, ip in DEST.items():
    data = {m: parse(os.path.join(TXT, f"trace_{label}_{m}.txt")) for m in METHODS}
    maxhop = max((max(d) for d in data.values() if d), default=0)
    print(f"\n### Destino: {label}  (`{ip}`)\n")
    hdr = "| HOP | " + " | ".join(METHODS) + " |"
    sep = "|---" * (len(METHODS) + 1) + "|"
    print(hdr); print(sep)
    for h in range(1, maxhop + 1):
        row = [str(h)]
        for m in METHODS:
            row.append(data[m].get(h, ""))
        print("| " + " | ".join(row) + " |")
    # resumen: hops respondidos y si completa
    print("\n**Resumen por método:**\n")
    print("| Método | Hops con respuesta | ¿Llega al destino? | Último hop visible |")
    print("|---|---|---|---|")
    for m in METHODS:
        d = data[m]
        resp = sum(1 for v in d.values() if v != "*")
        reaches = any(v.startswith(ip) for v in d.values())
        last = ""
        for h in sorted(d):
            if d[h] != "*":
                last = f"{h}:{d[h]}"
        print(f"| {m} | {resp} | {'Sí' if reaches else 'No'} | {last} |")
