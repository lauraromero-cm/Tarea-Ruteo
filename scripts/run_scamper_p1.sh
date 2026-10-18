#!/usr/bin/env bash
# =====================================================================
# Punto 1 - Path Discovery con scamper 20260902
# Ejecuta los 6 metodos de traceroute + tracelb (5 modos) a las 3 IPs,
# guardando .warts, texto y captura .pcap por cada metodo.
# Uso:  bash run_scamper_p1.sh

# 1) captura en segundo plano solo del tráfico con ese destino
# dumpcap -i eth0 -q -f "host 200.14.48.134" -w evidencia/pcap/trace_habana_icmp.pcap &
# CAP=$!; sleep 1

# 2) scamper guardando en formato warts
# scamper -O warts -o evidencia/warts/trace_habana_icmp.warts -I "trace -P icmp 200.14.48.134"

# 3) detener captura y convertir a texto
# kill $CAP
# sc_warts2text evidencia/warts/trace_habana_icmp.warts > evidencia/txt/trace_habana_icmp.txt

# =====================================================================
set -u

IFACE="eth0"                      # interfaz de salida a Internet
BASE="/home/kali/Tarea_Ruteo/evidencia"
WARTS="$BASE/warts"; TXT="$BASE/txt"; PCAP="$BASE/pcap"
mkdir -p "$WARTS" "$TXT" "$PCAP"

# IPs destino: etiqueta=IP
declare -A DST=(
  [valparaiso]="138.204.228.2"
  [habana]="200.14.48.134"
  [rusia]="37.79.153.66"
)

# Metodos de traceroute (trace -P <metodo>)
TRACE_METHODS=(udp icmp udp-paris icmp-paris tcp tcp-ack)
# Modos de tracelb (tracelb -P <modo>)
TRACELB_METHODS=(udp-dport icmp-echo udp-sport tcp-sport tcp-ack-sport)

cap_start() {  # cap_start <pcapfile> <dst_ip>
  dumpcap -i "$IFACE" -q -f "host $2" -w "$1" >/dev/null 2>&1 &
  echo $!            # devuelve PID
  sleep 1            # dar tiempo a que dumpcap abra la interfaz
}
cap_stop() { kill "$1" 2>/dev/null; sleep 1; }

echo "######## TRACEROUTE (6 metodos) ########"
for label in "${!DST[@]}"; do
  ip="${DST[$label]}"
  echo "==== Destino $label ($ip) ===="
  for m in "${TRACE_METHODS[@]}"; do
    tag="trace_${label}_${m}"
    pcap="$PCAP/${tag}.pcap"
    warts="$WARTS/${tag}.warts"
    pid=$(cap_start "$pcap" "$ip")
    scamper -O warts -o "$warts" -I "trace -P $m $ip"
    cap_stop "$pid"
    sc_warts2text "$warts" > "$TXT/${tag}.txt" 2>/dev/null
    echo "  [$m] -> $warts (+pcap/txt)"
  done
done

echo "######## TRACELB (5 modos) ########"
for label in "${!DST[@]}"; do
  ip="${DST[$label]}"
  echo "==== Destino $label ($ip) ===="
  for m in "${TRACELB_METHODS[@]}"; do
    tag="tracelb_${label}_${m}"
    pcap="$PCAP/${tag}.pcap"
    warts="$WARTS/${tag}.warts"
    pid=$(cap_start "$pcap" "$ip")
    scamper -O warts -o "$warts" -I "tracelb -P $m $ip"
    cap_stop "$pid"
    sc_warts2text "$warts" > "$TXT/${tag}.txt" 2>/dev/null
    echo "  [$m] -> $warts (+pcap/txt)"
  done
done

echo "LISTO. Evidencia en $BASE"
