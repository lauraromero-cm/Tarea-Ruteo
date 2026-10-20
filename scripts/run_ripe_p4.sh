#!/usr/bin/env bash
# =====================================================================
# Punto 4 - Path way RIPE (VUELTA): sondas destino -> mi IP (186.10.176.77)
# Sondas: Valparaiso=6652 (AS61506, sustituta de 31416 Abandoned),
#         Habana=12734, Rusia=870.  Protocolos: ICMP, UDP, TCP (puerto 33435).
# =====================================================================
set -u
KEY="82f6f109-1c13-4ce7-ac06-0d535153fa2c"
MYIP="186.10.176.77"
BASE="/home/kali/Tarea_Ruteo/evidencia_ripe"
mkdir -p "$BASE"/{json_vuelta,ids_vuelta}

declare -A PROBE=( [valparaiso]="6652" [habana]="12734" [rusia]="870" )

crear() {  # $1=probe_id $2=proto $3=label
  local pid="$1" proto="$2" label="$3" extra=""
  [ "$proto" != "ICMP" ] && extra='"port": 33435,'
  curl -s --max-time 25 -X POST "https://atlas.ripe.net/api/v2/measurements/" \
    -H "Authorization: Key $KEY" -H "Content-Type: application/json" \
    --data "{\"definitions\":[{\"target\":\"$MYIP\",\"af\":4,\"type\":\"traceroute\",\"protocol\":\"$proto\",\"description\":\"P4 vuelta $proto $label\",\"packets\":3,\"size\":48,\"paris\":0,$extra\"is_oneoff\":true}],\"probes\":[{\"type\":\"probes\",\"value\":\"$pid\",\"requested\":1}]}" 2>/dev/null | python3 -I -c "import sys,json;print(json.load(sys.stdin)['measurements'][0])" 2>/dev/null
}

bajar() {  # $1=id  espera resultados
  local id="$1"
  for i in $(seq 1 30); do
    local n=$(curl -s --max-time 15 "https://atlas.ripe.net/api/v2/measurements/$id/results/" 2>/dev/null | python3 -I -c "import sys,json;print(len(json.load(sys.stdin)))" 2>/dev/null)
    [ "${n:-0}" -ge 1 ] 2>/dev/null && return 0
    sleep 8
  done
  return 1
}

for label in valparaiso habana rusia; do
  pid="${PROBE[$label]}"
  for proto in ICMP UDP TCP; do
    lp=$(echo "$proto"|tr A-Z a-z); tag="vuelta_${label}_${lp}"
    echo "==== $tag (probe $pid -> $MYIP) ===="
    MID=$(crear "$pid" "$proto" "$label")
    echo "$MID" > "$BASE/ids_vuelta/${tag}.id"
    echo "  id: $MID"
    if bajar "$MID"; then
      curl -s --max-time 20 "https://atlas.ripe.net/api/v2/measurements/$MID/results/" > "$BASE/json_vuelta/${tag}.json" 2>/dev/null
      echo "  resultados OK"
    else
      echo "  SIN resultados (timeout)"
    fi
  done
done
echo "LISTO. IDs en $BASE/ids_vuelta/, resultados en $BASE/json_vuelta/"
