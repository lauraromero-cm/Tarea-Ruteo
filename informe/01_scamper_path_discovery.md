# 1. Path Discovery con Scamper

> Mediciones desde ISP **Entel (AS27651)**, IP pública `186.10.176.77`, interfaz `eth0`
> (VM en modo **bridged**; la IP privada local es `192.168.100.74`).
> scamper versión **20260902** (compilado con `--disable-scamper-privsep`).
> Fecha: 2026-10-17.

## Destinos y su AS

| Etiqueta | IP | ID RIPE | AS destino | Prefijo | País |
|----------|----|---------|-----------|---------|------|
| valparaiso | `138.204.228.2` | 31416 | **AS61506** INSACOM SpA | `138.204.228.0/24` | CL |
| habana | `200.14.48.134` | 12734 | **AS27725** ETECSA | `200.14.48.0/21` | CU |
| rusia | `37.79.153.66` | 870 | **AS12389** Rostelecom | `37.79.144.0/20` | RU |

---

## 1.A Traceroute — 6 métodos (Tabla 1)

Comando genérico (ejemplo ICMP a Valparaíso) con captura de tráfico:

```bash
IFACE=eth0; ip=138.204.228.2; m=icmp; tag="trace_valparaiso_${m}"
dumpcap -i "$IFACE" -q -f "host $ip or icmp" -w "evidencia/pcap/${tag}.pcap" &
CAP=$!; sleep 2
scamper -O warts -o "evidencia/warts/${tag}.warts" -I "trace -P $m $ip"
sleep 2; kill $CAP
sc_warts2text "evidencia/warts/${tag}.warts"
```

> Nota: el filtro de captura correcto es **`host $ip or icmp`**. Usar solo `host $ip`
> deja fuera los **ICMP Time-Exceeded** de los routers intermedios (su IP de origen es la
> del router, no la del destino), que son justamente las respuestas del traceroute.

Automatización de las 33 mediciones: `scripts/run_scamper_p1.sh`.

### Tabla 1 — Destino Valparaíso `138.204.228.2`

| HOP | udp | icmp | udp-paris | icmp-paris | tcp | tcp-ack |
|---|---|---|---|---|---|---|
| 1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 |
| 2 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 |
| 3 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 |
| 4 | 10.253.197.10 | 10.253.197.10 | 10.253.197.10 | 10.253.197.10 | 10.253.197.10 | **138.204.228.2 [RST]** |
| 5 | 10.253.196.97 | 10.253.196.97 | 10.253.196.97 | 10.253.196.97 | 10.253.196.97 | — |
| 6 | 192.168.8.193 | 192.168.8.193 | 192.168.8.193 | 192.168.8.193 | 192.168.8.193 | — |
| 7 | 45.68.16.129 | 45.68.16.129 | 10.100.154.1 | 45.68.16.129 | 45.68.16.129 | — |
| 8 | 10.100.154.1 | 10.100.154.1 | 138.204.228.164 | 10.100.154.1 | 10.100.154.1 | — |
| 9 | 138.204.228.164 | 138.204.228.164 | 138.204.228.162 | 138.204.228.164 | * | — |
| 10 | 138.204.228.162 | 138.204.228.162 | * | 138.204.228.162 | * | — |
| 11 | * | **138.204.228.2** | * | **138.204.228.2** | * | — |
| 12–15 | * | | * | | * | |

**¿Llega al destino?** udp: No · icmp: **Sí** · udp-paris: No · icmp-paris: **Sí** · tcp: No · tcp-ack: Sí (falso, ver 1.C)

### Tabla 1 — Destino Habana `200.14.48.134`

| HOP | udp | icmp | udp-paris | icmp-paris | tcp | tcp-ack |
|---|---|---|---|---|---|---|
| 1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 |
| 2 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 |
| 3 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 |
| 4 | 10.253.197.10 | 10.253.197.10 | 10.253.197.10 | 10.253.197.10 | 10.253.197.10 | **200.14.48.134 [RST]** |
| 5 | 10.253.196.97 | 10.253.196.97 | 10.253.196.97 | 10.253.196.97 | 10.253.196.97 | — |
| 6 | 192.168.9.133 | 192.168.9.133 | 192.168.9.133 | 192.168.9.133 | 192.168.9.133 | — |
| 7 | * | 213.99.17.182 | 5.53.3.71 | * | * | — |
| 8 | 5.53.5.41 | 5.53.5.41 | 213.140.35.110 | 5.53.5.41 | 5.53.5.41 | — |
| 9 | 213.140.35.110 | 213.140.35.86 | 193.251.143.67 | 213.140.35.86 | * | — |
| 10 | 193.251.143.67 | 193.251.143.67 | * | 193.251.143.67 | * | — |
| 11 | * | * | * | * | * | — |
| 12 | * | * | 200.0.16.62 | * | * | — |
| 13 | 200.0.16.62 | 200.0.16.62 | 200.0.16.21 | 200.0.16.62 | 200.0.16.62 | — |
| 14 | 200.0.16.21 | 200.0.16.21 | 200.0.16.29 | 200.0.16.21 | 200.0.16.21 | — |
| 15 | 200.0.16.25 | 200.0.16.29 | 200.0.16.29 | 200.0.16.29 | 200.0.16.29 | — |
| 16–17 | * | * | * | * | * | — |
| 18 | 200.14.48.178 | 200.14.48.178 | 200.14.48.178 | 200.14.48.178 | * | — |
| 19 | 200.14.48.178 | **200.14.48.134** | **200.14.48.134** | **200.14.48.134** | **200.14.48.134** | — |
| 20 | **200.14.48.134** | | | | | — |

**¿Llega al destino?** udp: **Sí** · icmp: **Sí** · udp-paris: **Sí** · icmp-paris: **Sí** · tcp: **Sí** · tcp-ack: Sí (falso)

### Tabla 1 — Destino Rusia `37.79.153.66`

| HOP | udp | icmp | udp-paris | icmp-paris | tcp | tcp-ack |
|---|---|---|---|---|---|---|
| 1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 | 192.168.100.1 |
| 2 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 | 100.83.128.1 |
| 3 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 | 10.253.197.9 |
| 4 | 10.253.197.10 | 10.253.197.10 | 10.253.197.10 | 10.253.197.10 | 10.253.197.10 | **37.79.153.66 [RST]** |
| 5 | 10.253.196.97 | 10.253.196.97 | 10.253.196.97 | 10.253.196.97 | 10.253.196.97 | — |
| 6 | 192.168.9.133 | 192.168.9.133 | 192.168.9.133 | 192.168.9.133 | 192.168.9.133 | — |
| 7 | 213.99.17.182 | 213.99.17.182 | 5.53.5.41 | 213.99.17.182 | 213.99.17.182 | — |
| 8 | 5.53.5.41 | 5.53.3.75 | * | 5.53.3.75 | 5.53.3.75 | — |
| 9 | 94.142.119.188 | * | 94.142.119.188 | 94.142.118.184 | * | — |
| 10 | 195.2.29.185 | 195.2.29.185 | 195.2.29.185 | 195.2.29.185 | * | — |
| 11 | 195.2.20.197 | 195.2.20.197 | 195.2.20.197 | 195.2.20.197 | 195.2.20.197 | — |
| 12 | 195.2.24.246 | 195.2.24.246 | 195.2.24.246 | 195.2.24.246 | 195.2.24.246 | — |
| 13 | 195.2.31.14 | 195.2.31.14 | 195.2.31.14 | 195.2.31.14 | * | — |
| 14 | 195.2.9.242 | 195.2.9.242 | 195.2.9.242 | 195.2.9.242 | 195.2.9.242 | — |
| 15 | 195.27.81.54 | * | 195.27.81.54 | 195.27.81.54 | * | — |
| 16 | * | * | * | * | * | — |
| 17 | 217.107.123.25 | 217.107.123.25 | 217.107.123.25 | 217.107.123.25 | * | — |
| 18 | * | **37.79.153.66** | * | **37.79.153.66** | * | — |
| 19–22 | * | | * | | * | — |

**¿Llega al destino?** udp: No · icmp: **Sí** · udp-paris: No · icmp-paris: **Sí** · tcp: No · tcp-ack: Sí (falso)

---

## 1.B Comparación de los 6 métodos y método recomendado

Resumen de hops con respuesta y si la ruta se completa:

| Destino | udp | icmp | udp-paris | icmp-paris | tcp | tcp-ack |
|---------|-----|------|-----------|-----------|-----|---------|
| Valparaíso | 10, no llega | **11, llega** | 9, no llega | **11, llega** | 8, no llega | 4 (RST falso) |
| Habana | 15, llega | **15, llega** | 15, llega | 14, llega | 11, llega | 4 (RST falso) |
| Rusia | 16, no llega | 15, llega | 15, no llega | **17, llega** | 11, no llega | 4 (RST falso) |

**Conclusiones:**
- **ICMP e ICMP-Paris son los mejores métodos**: son los únicos que **completan la ruta en los 3 destinos** y producen la menor cantidad de `*`. Para Rusia, **icmp-paris** es el más completo (17 hops).
- **UDP** solo completa en Habana. En Valparaíso y Rusia los destinos **no generan ICMP Port-Unreachable** ante UDP a puertos altos, por lo que el traceroute UDP nunca "ve" el destino (se queda en `*` tras el último router).
- **UDP-Paris** mantiene el flujo constante (mejor ante ECMP) pero igualmente no completa en Valparaíso/Rusia por la misma razón (destino no responde a UDP). En Valparaíso incluso reveló un salto distinto (omitió `45.68.16.129`), evidenciando balanceo de carga.
- **TCP (SYN)** es el que **más `*` deja** en el núcleo internacional: muchos routers no responden a SYN a puerto 33435 o lo limitan por rate-limit, y el SYN que no llega al destino no completa.
- **TCP-ACK** es engañoso: "completa" en 4 hops en los 3 destinos, pero es un **RST falsificado** (ver 1.C), no la ruta real.

**Recomendación global: ICMP-Paris** — combina máxima completitud con robustez frente a balanceadores de carga ECMP.

---

## 1.C Análisis de tráfico por método (payload + capa de transporte)

Valores extraídos con `tshark` de las capturas (sondas **salientes** desde `192.168.100.74`).
El patrón es predecible y permite caracterizar/firmar cada método:

### Patrón de las sondas salientes

| Método | L4 | Puerto origen | Puerto destino | Campo que varía por sonda | Flujo (5-tupla) | ip.len |
|--------|----|---------------|----------------|---------------------------|-----------------|--------|
| **udp** | UDP | **fijo** 47886 | **incrementa** 33435,33436,… | dport (+1) y checksum (−1) | **cambia** cada hop | 44 |
| **icmp** | ICMP t8 | — | — | icmp.seq 0,1,2,…; checksum cambia | id fijo 48361 | 44 |
| **udp-paris** | UDP | fijo 48391 | **fijo** 33435 | **UDP checksum** 0x0001,0x0002,… | **constante** | 44 |
| **icmp-paris** | ICMP t8 | — | — | icmp.seq 0,1,…; **checksum FIJO** 0xbeec | **constante** | 44 |
| **tcp** | TCP SYN | fijo 48897 | fijo 33435 | IP-ID (seq=0, flags=SYN 0x002) | constante | 44 |
| **tcp-ack** | TCP ACK | fijo 49419 | fijo 33435 | IP-ID (seq=0, flags=ACK 0x010) | constante | 44 |

**Predicción de valores (lo clave):**
- **udp clásico:** el `dstport` arranca en 33435 y **sube +1 por cada sonda**; el checksum UDP **baja exactamente −1** por paquete (0x2e52, 0x2e51, 0x2e50…) porque el único byte que cambia es el puerto. El TTL IP va 1,2,3,…n. → Firma inconfundible.
- **udp-paris:** mantiene `sport`/`dport` **fijos** (flujo constante → todas las sondas siguen la **misma ruta** bajo ECMP) y en su lugar varía el **checksum UDP** (0x0001, 0x0002…) manipulando el payload. Es la diferencia esencial con el UDP clásico.
- **icmp:** Echo Request (type 8), `id` fijo, `seq` 0,1,2… (una por TTL); el checksum ICMP cambia con el seq.
- **icmp-paris:** `id` fijo y **checksum ICMP constante (0xbeec)** aunque el `seq` cambie — se ajusta el payload para fijar el checksum, que es el campo que muchos balanceadores usan como identificador de flujo ICMP → ruta estable.
- **tcp / tcp-ack:** puertos fijos, un único flujo; SYN (`0x002`) o ACK (`0x010`). Se distinguen las sondas por el campo IP-ID.

### Tráfico de retorno observado (ICMP)
En las capturas (`evidencia/pcap2/`) se observan, para cada sonda saliente, su **ICMP Time-Exceeded (type 11, code 0)** desde el router correspondiente, con el **paquete original embebido** en el payload ICMP. El destino que completa devuelve **ICMP Echo-Reply (type 0)** (métodos ICMP), **ICMP Port-Unreachable (type 3 code 3)** (UDP) o **TCP RST** (TCP), según el método.

```bash
# Ver los Time-Exceeded de los routers intermedios:
tshark -r evidencia/pcap2/trace_valparaiso_icmp.pcap -Y "icmp.type==11" \
  -T fields -e ip.src -e icmp.type -e icmp.code
```

---

## 1.D Nodo que filtra — amenaza para el auditor

Se detectan **dos reglas** de filtrado:

### (1) Firewall stateful que inyecta RST falsos (TCP-ACK)
En los **3 destinos**, el método `tcp-ack` reporta que se "llega" al destino en el **hop 4**
con un `[closed]` (RST). Es **falso**: un middlebox intercepta el ACK fuera de estado y
responde con un **RST falsificado** usando la IP del destino como origen. La prueba está en
el **TTL** del paquete de retorno:

| | TCP-ACK "destino" (hop 4) | Echo-Reply genuino del destino (hop 11) |
|---|---|---|
| ip.src | 138.204.228.2 | 138.204.228.2 |
| **ip.ttl de llegada** | **252** (≈3 saltos) | **245** (≈10 saltos) |

Como el RST llega con TTL 252 (origen a ~3 saltos) y la respuesta real del destino llega con
TTL 245 (origen a ~10 saltos), **no provienen del mismo equipo**. El RST lo genera un firewall
stateful de Entel ubicado a ~4 saltos (zona `10.253.197.x`).

- **Regla del nodo:** descartar/responder con RST los segmentos TCP ACK que no pertenecen a
  una conexión establecida (anti-escaneo *ACK scan*).
- **Amenaza para el auditor:** un atacante que use *ACK scan* para mapear la red obtiene una
  topología **falsa** (destino aparente a 4 saltos) y un estado `[closed]` inventado.
- **Cómo saltarse la regla:** no fiarse del `tcp-ack`; usar **ICMP-Paris** (o SYN real) para
  la topología, y **validar el TTL** de las respuestas para detectar RST falsificados.

### (2) Destinos que no responden a UDP (Valparaíso y Rusia)
`138.204.228.2` y `37.79.153.66` **no responden** a las sondas **UDP** (no generan ICMP
Port-Unreachable), por lo que el traceroute UDP/UDP-Paris **nunca completa**. En cambio **sí
responden a ICMP Echo** (ambos completan con icmp / icmp-paris).

- **Regla del nodo:** firewall del destino que **descarta UDP** a puertos altos sin devolver
  error (política *drop* silenciosa).
- **Cómo saltarse la regla:** cambiar de método a **ICMP (Echo)**, que sí es respondido →
  permite identificar el equipo final.

> IP que no responde a un tipo de solicitud y sí a otro (ejemplo pedido por la tarea):
> **`138.204.228.2`** → **no responde a UDP**, **sí responde a ICMP Echo**.

---

## 1.E tracelb (traceroute con balanceo de carga) — 5 modos

Comando (ejemplo icmp-echo a Valparaíso):
```bash
scamper -O warts -o evidencia/warts/tracelb_valparaiso_icmp-echo.warts \
  -I "tracelb -P icmp-echo 138.204.228.2"
sc_warts2text evidencia/warts/tracelb_valparaiso_icmp-echo.warts
```

### Nodos/enlaces e IPs únicas descubiertas

| Destino / modo | udp-dport | icmp-echo | udp-sport | tcp-sport | tcp-ack-sport |
|----------------|-----------|-----------|-----------|-----------|---------------|
| Valparaíso (nodos) | 9 | **11** | 8 | 8 | 4 |
| Habana (nodos) | 7 | **14** | 6 | 6 | 4 |
| Rusia (nodos) | 7 | **14** | 11 | 6 | 4 |

### ¿tracelb descubre más IPs que los traceroute previos?

| Destino | Traceroute (unión 6 métodos) | tracelb (unión 5 modos) | Unión total |
|---------|------------------------------|--------------------------|-------------|
| Valparaíso | 10 IPs | 10 IPs | 10 |
| Habana | 17 IPs | 17 IPs | 17 |
| Rusia | 18 IPs | 18 IPs | **19** |

**Conclusión:** en volumen total de IPs, tracelb es **comparable** a la unión de los 6 métodos
de traceroute (en Rusia aporta 1 IP adicional). Su ventaja real es que **en una sola medición
revela las ramas paralelas (ECMP)**: descubre **varias IPs en un mismo hop** (p.ej. en Habana
`200.0.16.21/25/29/62` coexistiendo en el mismo nivel), algo que el traceroute lineal muestra
como un único camino. El modo **icmp-echo** es el que más nodos revela de forma consistente;
**tcp-ack-sport** se queda en 4 nodos por el mismo RST falso de 1.D.

### Caracterización del tráfico tracelb

tracelb envía **múltiples sondas por TTL** (≈6), cada una con un **identificador de flujo
distinto**, para detectar cuándo flujos diferentes toman next-hops diferentes (balanceo):

| Modo | Campo que se varía entre las ~6 sondas de cada hop | Campo fijo |
|------|----------------------------------------------------|-----------|
| udp-dport | `dstport` 33435→33440 | sport fijo (64927) |
| udp-sport | `srcport` 34420→34425 | dport fijo (33435) |
| icmp-echo | `icmp.checksum` 0x0001→0x0006 | id fijo (34286) |
| tcp-sport | `srcport` variable | dport fijo |
| tcp-ack-sport | `srcport` variable, flag ACK | dport fijo |

Diferencia clave con traceroute: traceroute manda **1 flujo por hop**; tracelb manda **N flujos
por hop** y correlaciona respuestas para reconstruir el grafo de rutas paralelas.
