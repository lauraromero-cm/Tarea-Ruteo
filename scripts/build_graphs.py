#!/usr/bin/env python3
# Punto 5: construye un grafo CX2 por destino (ida+vuelta) y opcionalmente lo sube a NDEx.
# Subida: definir env NDEX_USER y NDEX_PASS y pasar argumento "upload".
import json, os, re, sys
from ndex2.cx2 import CX2Network
from ndex2.client import Ndex2

ER = "/home/kali/Tarea_Ruteo/evidencia_ripe"
OUT = os.path.join(ER, "graphs"); os.makedirs(OUT, exist_ok=True)

# Por destino: (ida_tag, ida_id, vuelta_tag, vuelta_id, proto_ida, proto_vuelta)
GRAPHS = {
  "valparaiso": ("ripe_valparaiso_icmp", 225408742, "vuelta_valparaiso_tcp", 225423796, "ICMP", "TCP",
                 "138.204.228.2"),
  "habana":     ("ripe_habana_udp",     225411975, "vuelta_habana_icmp",     225424159, "UDP",  "ICMP",
                 "200.14.48.134"),
  "rusia":      ("ripe_rusia_udp",      225412819, "vuelta_rusia_tcp",       225428926, "UDP",  "TCP",
                 "37.79.153.66"),
}

# ASN lookup (de los dos archivos cymru)
asn = {}
for fn in ("/tmp/ripe_asn.txt", "/tmp/vuelta_asn.txt"):
    if os.path.exists(fn):
        for line in open(fn):
            p = [x.strip() for x in line.split("|")]
            if len(p) >= 7 and p[1] not in ("IP",):
                asn[p[1]] = p[0]

def asof(ip):
    if re.match(r"^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.)", ip):
        return "privada/CGNAT"
    a = asn.get(ip, "?")
    return "privada" if a in ("NA", "?") else f"AS{a}"

def path_of(tag, folder):
    f = os.path.join(ER, folder, f"{tag}.json")
    d = json.load(open(f))
    if not d: return []
    seq = []
    for h in d[0].get("result", []):
        if h.get("hop") == 255: continue
        ips = [x.get("from") for x in h.get("result", []) if x.get("from")]
        if ips: seq.append(ips[0])
    return seq

def build(label):
    ida_tag, ida_id, vue_tag, vue_id, pi, pv, dst = GRAPHS[label]
    ida = path_of(ida_tag, "json")
    vue = path_of(vue_tag, "json_vuelta")
    net = CX2Network()
    net.set_name(f"Path {label} (ida+vuelta) - {dst}")
    desc = (f"Grafo de ruta ida+vuelta hacia {dst} ({label}). "
            f"IDA: traceroute {pi} sonda 1018349 -> {dst}, medicion RIPE {ida_id}. "
            f"VUELTA: traceroute {pv} sonda destino -> 186.10.176.77, medicion RIPE {vue_id}. "
            f"ISP origen: Entel AS27651.")
    net.add_network_attribute("description", desc)
    net.add_network_attribute("ida_measurement_id", str(ida_id))
    net.add_network_attribute("vuelta_measurement_id", str(vue_id))

    nid = {}
    def node(ip):
        if ip not in nid:
            nid[ip] = net.add_node(attributes={"name": ip, "AS": asof(ip)})
        return nid[ip]

    def add_path(seq, direction):
        prev = None
        for ip in seq:
            n = node(ip)
            if prev is not None and prev != n:
                net.add_edge(source=prev, target=n, attributes={"direction": direction})
            prev = n

    add_path(ida, "ida")
    add_path(vue, "vuelta")

    cx = net.to_cx2()
    outf = os.path.join(OUT, f"{label}.cx2")
    json.dump(cx, open(outf, "w"))
    print(f"{label}: {len(nid)} nodos, archivo {outf}")
    return net, ida_id, vue_id

nets = {l: build(l) for l in GRAPHS}

if len(sys.argv) > 1 and sys.argv[1] == "upload":
    u, p = os.environ.get("NDEX_USER"), os.environ.get("NDEX_PASS")
    if not u or not p:
        print("ERROR: define NDEX_USER y NDEX_PASS"); sys.exit(1)
    client = Ndex2(username=u, password=p)
    print("\n=== Subiendo a NDEx ===")
    for label, (net, ida_id, vue_id) in nets.items():
        url = client.save_new_cx2_network(net.to_cx2(), visibility="PUBLIC")
        uuid = url.rstrip("/").split("/")[-1]
        print(f"{label}: UUID={uuid}  (ida={ida_id}, vuelta={vue_id})")
        print(f"   https://www.ndexbio.org/viewer/networks/{uuid}")
