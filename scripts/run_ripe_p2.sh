#!/usr/bin/env bash
# =====================================================================
# Punto 2 - Path Discovery RIPE (ida): sonda 1018349 -> 3 IPs
# Protocolos: ICMP, UDP, TCP  (UDP/TCP con puerto 33435, como en scamper)
# Para cada uno: crea medicion via API, captura en eth0, baja resultados.
# =====================================================================
set -u
KEY="82f6f109-1c13-4ce7-ac06-0d535153fa2c"
PROBE="1018349"
IFACE="eth0"
BASE="/home/kali/Tarea_Ruteo/evidencia_ripe"
mkdir -p "$BASE"/{txt,pcap,json,ids}

declare -A DST=( [valparaiso]="138.204.228.2" [habana]="200.14.48.134" [rusia]="37.79.153.66" )

crear_medicion() {  # $1=target $2=proto(ICMP/UDP/TCP)
  local target="$1" proto="$2" extra=""
  [ "$proto" != "ICMP" ] && extra='"port": 33435,'
  local body
  body=$(cat <<JSON
{ "definitions": [{
    "target": "$target", "af": 4, "type": "traceroute",
    "protocol": "$proto", "description": "P2 $proto $target",
    "packets": 3, "size": 48, "first_hop": 1, "max_hops": 255,
    "paris": 0, "timeout": 4000, $extra "is_oneoff": true }],
  "probes": [{ "type": "probes", "value": "$PROBE", "requested": 1 }] }
JSON
)
  curl -s --max-time 25 -X POST "https://atlas.ripe.net/api/v2/measurements/" \
    -H "Authorization: Key $KEY" -H "Content-Type: application/json" \
    --data "$body" 2>/dev/null | python3 -I -c "import sys,json;print(json.load(sys.stdin)['measurements'][0])"
}

bajar_resultados() {  # $1=measurement_id  -> espera hasta tener resultados (max ~4min)
  local id="$1"
  for i in $(seq 1 30); do
    local n
    n=$(curl -s --max-time 15 "https://atlas.ripe.net/api/v2/measurements/$id/results/" 2>/dev/null | python3 -I -c "import sys,json;print(len(json.load(sys.stdin)))" 2>/dev/null)
    [ "${n:-0}" -ge 1 ] 2>/dev/null && return 0
    sleep 8
  done
  return 1
}

for label in valparaiso habana rusia; do
  ip="${DST[$label]}"
  for proto in ICMP UDP TCP; do
    lp=$(echo "$proto" | tr 'A-Z' 'a-z')
    tag="ripe_${label}_${lp}"
    echo "==== $tag ($ip) ===="
    # captura
    dumpcap -i "$IFACE" -q -f "host $ip" -w "$BASE/pcap/${tag}.pcap" >/dev/null 2>&1 &
    CAP=$!; sleep 2
    # crear
    MID=$(crear_medicion "$ip" "$proto")
    echo "$MID" > "$BASE/ids/${tag}.id"
    echo "  measurement id: $MID"
    # esperar resultados
    if bajar_resultados "$MID"; then
      curl -s --max-time 20 "https://atlas.ripe.net/api/v2/measurements/$MID/results/" > "$BASE/json/${tag}.json" 2>/dev/null
      echo "  resultados OK"
    else
      echo "  SIN resultados (timeout)"
    fi
    sleep 2; kill $CAP 2>/dev/null; wait $CAP 2>/dev/null
    pk=$(tshark -r "$BASE/pcap/${tag}.pcap" 2>/dev/null | wc -l)
    echo "  pcap: $pk paquetes"
  done
done
echo "LISTO. IDs en $BASE/ids/, resultados en $BASE/json/, capturas en $BASE/pcap/"
