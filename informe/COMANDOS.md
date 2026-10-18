# Comandos utilizados — Path Discovery (Punto 0 y 1)

Registro reproducible de todos los comandos ejecutados, en orden.

---

## Punto 0 — Entorno

### Identificar IP pública, ISP, AS y prefijo
```bash
curl -s https://ifconfig.me ; echo                 # IP pública -> 186.10.176.77
whois 186.10.176.77 | grep -iE "inetnum|aut-num|owner|country"
# -> AS27651 ENTEL CHILE S.A. · inetnum 186.10.128.0/18 · prefijo BGP 186.10.176.0/24 (bgp.he.net)
```

### Instalar scamper 20260902
```bash
mkdir -p ~/scamper_build && cd ~/scamper_build
curl -O https://www.caida.org/catalog/software/scamper/code/scamper-cvs-20260902.tar.gz
tar xzf scamper-cvs-20260902.tar.gz
cd scamper-cvs-20260902
./configure --disable-scamper-privsep      # necesario para correr con capabilities (sin root)
make -j4
sudo make install
sudo ldconfig
sudo setcap cap_net_raw,cap_net_admin+ep /usr/local/bin/scamper
scamper -v                                  # -> scamper version 20260902
```

### Verificar interfaz de salida
```bash
ip route get 8.8.8.8 | awk '{for(i=1;i<=NF;i++) if($i=="dev") print $(i+1)}'   # -> eth0
```

> **IMPORTANTE (VM VMware):** la red de la VM debe estar en modo **Bridged**, no NAT.
> Con NAT la traza solo muestra el hop 1 y el destino (la NAT descarta los ICMP Time-Exceeded).
> ```bash
> # tras cambiar a Bridged en VM > Settings > Network Adapter:
> sudo dhclient -r eth0 && sudo dhclient eth0
> ```

---

## Punto 1 — Scamper

### Medición individual (un método, un destino) con captura
```bash
IFACE=eth0; ip=138.204.228.2; m=icmp; tag="trace_valparaiso_${m}"

dumpcap -i "$IFACE" -q -f "host $ip or icmp" -w "evidencia/pcap/${tag}.pcap" &
CAP=$!; sleep 2
scamper -O warts -o "evidencia/warts/${tag}.warts" -I "trace -P $m $ip"
sleep 2; kill $CAP
sc_warts2text "evidencia/warts/${tag}.warts" > "evidencia/txt/${tag}.txt"
```

Métodos de traceroute: `udp icmp udp-paris icmp-paris tcp tcp-ack`

### Ejecutar TODO el Punto 1 (33 mediciones) — script
```bash
cd /home/kali/Tarea_Ruteo
bash scripts/run_scamper_p1.sh > evidencia/run_p1.log 2>&1
# en segundo plano, viendo avance:
#   nohup bash scripts/run_scamper_p1.sh > evidencia/run_p1.log 2>&1 &
#   tail -f evidencia/run_p1.log
```

### tracelb (balanceo de carga) — ejemplo
```bash
scamper -O warts -o evidencia/warts/tracelb_valparaiso_icmp-echo.warts \
  -I "tracelb -P icmp-echo 138.204.228.2"
sc_warts2text evidencia/warts/tracelb_valparaiso_icmp-echo.warts
```
Modos de tracelb: `udp-dport icmp-echo udp-sport tcp-sport tcp-ack-sport`

### Re-captura con filtro correcto (incluye Time-Exceeded de retorno)
```bash
cd /home/kali/Tarea_Ruteo
IFACE=eth0; ip=138.204.228.2; label=valparaiso; mkdir -p evidencia/pcap2
for m in udp icmp udp-paris icmp-paris tcp tcp-ack; do
  tag="trace_${label}_${m}"
  dumpcap -i "$IFACE" -q -f "host $ip or icmp" -w "evidencia/pcap2/${tag}.pcap" &
  CAP=$!; sleep 2
  scamper -O warts -o /dev/null -I "trace -P $m $ip"
  sleep 2; kill $CAP 2>/dev/null; wait $CAP 2>/dev/null
done
```

---

## Análisis de tráfico (tshark / Wireshark)

### Patrón de sondas salientes
```bash
# UDP: puerto destino incremental, checksum decreciente
tshark -r evidencia/pcap/trace_valparaiso_udp.pcap -Y "ip.src==192.168.100.74 && udp" \
  -T fields -e ip.ttl -e udp.srcport -e udp.dstport -e udp.checksum

# ICMP: type 8, id fijo, seq incremental
tshark -r evidencia/pcap/trace_valparaiso_icmp.pcap -Y "ip.src==192.168.100.74 && icmp" \
  -T fields -e ip.ttl -e icmp.type -e icmp.ident -e icmp.seq -e icmp.checksum

# UDP-Paris: dport FIJO, checksum incremental (flujo constante)
tshark -r evidencia/pcap/trace_valparaiso_udp-paris.pcap -Y "ip.src==192.168.100.74 && udp" \
  -T fields -e ip.ttl -e udp.srcport -e udp.dstport -e udp.checksum
```

### Detección del RST falsificado (nodo que filtra)
```bash
# TTL del RST "del destino" en TCP-ACK (hop 4):
tshark -r evidencia/pcap2/trace_valparaiso_tcp-ack.pcap -Y "ip.src==138.204.228.2" \
  -T fields -e ip.src -e ip.ttl -e tcp.flags.str          # -> TTL 252 (≈3 saltos)

# TTL de la respuesta genuina del destino (ICMP echo-reply, hop 11):
tshark -r evidencia/pcap2/trace_valparaiso_icmp.pcap -Y "ip.src==138.204.228.2 && icmp.type==0" \
  -T fields -e ip.src -e ip.ttl                           # -> TTL 245 (≈10 saltos)
```

### Mapear AS de cada hop (Team Cymru)
```bash
cat evidencia/txt/trace_*.txt | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort -u > /tmp/ips.txt
{ echo begin; echo verbose; cat /tmp/ips.txt; echo end; } | nc whois.cymru.com 43
```

### Generar la Tabla 1 automáticamente
```bash
python3 scripts/build_tabla1.py
```
