# Tarea Individual — Path Discovery: RIPE Atlas vs Scamper

Caracterización de la infraestructura de acceso a Internet (Banda Ancha Fija) mediante
*path discovery*, comparando dos herramientas independientes: **scamper** (CAIDA, ejecutado
localmente) y **RIPE Atlas** (medición distribuida vía una sonda por software). Se analizan las
rutas de ida y de vuelta hacia tres destinos internacionales, el tráfico generado por cada método,
el comportamiento de los nodos que filtran y, finalmente, se publican los caminos como grafos
abiertos en NDEx.

> **Nota:** el informe final (LaTeX + PDF) se mantiene en disco pero **no se versiona** en este
> repositorio (ver `.gitignore`). Aquí se conservan únicamente las **evidencias reproducibles**,
> los **scripts** y la **configuración de la sonda**.

---

## Entorno medido

| Parámetro | Valor |
|-----------|-------|
| ISP / origen | **Entel Chile S.A.** |
| Sistema autónomo | **AS27651** |
| IP pública | `186.10.176.77` |
| Prefijo anunciado (BGP) | `186.10.176.0/24` (dentro de `186.10.128.0/18`, LACNIC) |
| Herramienta local | scamper **20260902** (CAIDA) |
| Sonda distribuida | RIPE Atlas **ID 1018349** (Docker, `jamesits/ripe-atlas`) |

### Destinos

| Destino | IP | AS | Operador |
|---------|----|----|----------|
| Valparaíso (CL) | `138.204.228.2` | AS61506 | INSACOM |
| La Habana (CU) | `200.14.48.134` | AS27725 | ETECSA |
| Rusia | `37.79.153.66` | AS12389 | Rostelecom |

---

## Qué se hizo (por punto de la tarea)

- **Punto 0 — Entorno.** Identificación de IP pública, AS y prefijo BGP (`curl`, `whois`,
  bgp.he.net). Instalación de scamper compilado con `--disable-scamper-privsep` para correr con
  *capabilities* en vez de root.
- **Punto 1 — Scamper.** 33 mediciones: los 6 métodos de `trace`
  (`udp, icmp, udp-paris, icmp-paris, tcp, tcp-ack`) contra cada destino, más `tracelb` (MDA) para
  detectar balanceo de carga ECMP. Captura simultánea de tráfico con `dumpcap` y análisis en
  Wireshark/tshark. Hallazgos: ICMP es el método que más infraestructura revela; detección de un
  **RST falsificado** por un firewall *stateful* de Entel (evidenciado por el TTL del RST, 252 vs
  245 de la respuesta genuina); destinos que no responden a UDP/TCP pero sí a ICMP Echo.
- **Punto 2 — RIPE Atlas.** Registro de una sonda por software (Docker), conexión a la plataforma
  y creación de 9 mediciones (ICMP/UDP/TCP × 3 destinos) vía la **API REST** (seleccionando la
  sonda por ID, para sortear la restricción del tag `system-ipv4-works` en una sonda tras NAT).
- **Punto 4 — Ruta inversa.** 9 mediciones de vuelta (sondas en los destinos → mi IP pública),
  comparando ida vs vuelta y evidenciando **ruteo asimétrico** e interfaces espejo.
- **Punto 5 — Public Path.** Publicación de 3 grafos dirigidos (ida + vuelta) en **NDEx**, cada uno
  con los IDs de medición RIPE de origen en su descripción.

---

## Estructura del repositorio

```
.
├── scripts/                 # Todo el código reproducible
│   ├── run_scamper_p1.sh     # Punto 1: 33 mediciones scamper + captura
│   ├── run_ripe_p2.sh        # Punto 2: mediciones RIPE de ida (API REST)
│   ├── run_ripe_p4.sh        # Punto 4: mediciones RIPE de vuelta
│   ├── build_tabla1.py       # Tabla comparativa de métodos scamper
│   ├── build_ripe_tabla.py   # Tabla de hops/AS de las mediciones RIPE
│   ├── build_tabla2.py       # Tabla ida vs vuelta (asimetría)
│   ├── build_graphs.py       # Genera y publica los 3 grafos CX2 en NDEx
│   ├── parse_ripe.py         # Parseo de los JSON de resultados RIPE
│   └── test_bridged.sh       # Verificación de red tras pasar la VM a bridged
│
├── evidencia/               # Evidencia de scamper (Punto 1)
│   ├── warts/   (33)         # Salidas binarias de scamper (.warts)
│   ├── txt/     (33)         # Conversión legible (sc_warts2text)
│   ├── pcap/    (33)         # Capturas por método (sondas salientes)
│   └── pcap2/   (7)          # Re-capturas con filtro "host o icmp" (incluye retorno)
│
├── evidencia_ripe/          # Evidencia de RIPE Atlas (Puntos 2, 4 y 5)
│   ├── json/        (9)      # Resultados crudos de ida
│   ├── json_vuelta/ (9)      # Resultados crudos de vuelta
│   ├── ids/ ids_vuelta/      # IDs de medición generados
│   ├── pcap/ pcap2/          # Capturas del tráfico de la sonda
│   └── graphs/      (3)      # Grafos CX2 publicados en NDEx
│
├── ripe-atlas/              # Configuración de la sonda Docker (sin claves privadas)
│   ├── etc/                  # Config del contenedor (probe_key está en .gitignore)
│   └── MI_CLAVE_PUBLICA.txt  # Clave pública registrada en RIPE
│
├── .gitignore
└── README.md
```

> No versionado (en `.gitignore`): `informe/` e `informe_latex/` (el informe), `ripe-atlas/run/`
> y `ripe-atlas/spool/` (estado *runtime* de la sonda), la clave privada `probe_key`, los `*.log`
> y la carpeta `.claude/`.

---

## Reproducir las mediciones

### Punto 0 — Entorno

```bash
curl -s https://ifconfig.me ; echo                       # IP pública -> 186.10.176.77
whois 186.10.176.77 | grep -iE "aut-num|inetnum|owner|country"

# scamper 20260902
cd ~/scamper_build/scamper-cvs-20260902
./configure --disable-scamper-privsep && make -j4 && sudo make install && sudo ldconfig
sudo setcap cap_net_raw,cap_net_admin+ep /usr/local/bin/scamper
scamper -v
```

> **VM VMware:** usar modo **Bridged** (no NAT). Con NAT se descartan los ICMP Time-Exceeded y la
> traza solo muestra el hop 1 y el destino.

### Punto 1 — Scamper

```bash
cd /home/kali/Tarea_Ruteo
bash scripts/run_scamper_p1.sh > evidencia/run_p1.log 2>&1   # 33 mediciones + captura
python3 scripts/build_tabla1.py                              # tabla comparativa

# Medición individual con captura (método = udp|icmp|udp-paris|icmp-paris|tcp|tcp-ack):
IFACE=eth0; ip=138.204.228.2; m=icmp; tag="trace_valparaiso_${m}"
dumpcap -i "$IFACE" -q -f "host $ip or icmp" -w "evidencia/pcap/${tag}.pcap" & CAP=$!; sleep 2
scamper -O warts -o "evidencia/warts/${tag}.warts" -I "trace -P $m $ip"
sleep 2; kill $CAP
sc_warts2text "evidencia/warts/${tag}.warts" > "evidencia/txt/${tag}.txt"

# tracelb (balanceo de carga, modos: udp-dport|icmp-echo|udp-sport|tcp-sport|tcp-ack-sport):
scamper -O warts -o evidencia/warts/tracelb_valparaiso_icmp-echo.warts \
  -I "tracelb -P icmp-echo 138.204.228.2"
```

### Puntos 2 y 4 — RIPE Atlas

```bash
# La sonda corre en Docker; tras reiniciar la VM queda Exited -> reactivar:
docker start ripe-atlas
docker logs -f ripe-atlas            # verificar conexión (KEEP / established)

bash scripts/run_ripe_p2.sh          # mediciones de ida (API REST, probe por ID)
bash scripts/run_ripe_p4.sh          # mediciones de vuelta
python3 scripts/parse_ripe.py        # parsear JSON de resultados
python3 scripts/build_tabla2.py      # tabla ida vs vuelta
```

### Punto 5 — Grafos en NDEx

```bash
python3 scripts/build_graphs.py                                   # genera los 3 CX2
NDEX_USER="usuario" NDEX_PASS="clave" python3 scripts/build_graphs.py upload   # publica
```

---

## Enlaces

- Mi IP / AS: https://bgp.he.net/ip/186.10.176.77 · https://bgp.he.net/AS27651
- Sonda RIPE Atlas: https://atlas.ripe.net/probes/1018349/
- Grafos NDEx (visor `https://www.ndexbio.org/viewer/networks/<UUID>`):
  - Valparaíso: `0acc00aa-ccbe-11f1-be0a-005056ae3c32`
  - La Habana: `0b0957cd-ccbe-11f1-be0a-005056ae3c32`
  - Rusia: `0b48f7e0-ccbe-11f1-be0a-005056ae3c32`

---

## Notas de reproducibilidad (gotchas)

- **scamper sin root:** compilar con `--disable-scamper-privsep` y dar *capabilities*
  (`setcap cap_net_raw,cap_net_admin+ep`). Si no, falla con "could not mkdir /var/empty".
- **Captura correcta:** el filtro debe ser `host <dst> or icmp`; solo `host <dst>` pierde los
  Time-Exceeded de los routers intermedios.
- **Sonda tras NAT:** la CLI de RIPE añade el tag `system-ipv4-works` que la sonda no tiene; por
  eso las mediciones se crean con la API REST seleccionando el probe por ID.
- **Permisos de la sonda:** nunca hacer `sudo chown -R` sobre todo el proyecto (rompe
  `ripe-atlas/{run,spool}` y la sonda no reconecta).
