# 4. Path way RIPE — Ruta inversa (Punto 4)

> Proceso inverso: traceroute **desde cada IP destino hacia mi IP pública** `186.10.176.77`,
> con los 3 protocolos. Al medir en ambos sentidos se obtienen las IPs de las **distintas
> interfaces** de cada nodo. Parámetros iguales al Punto 2 (packets=3, size=48, UDP/TCP port 33435).

## 4.0 Sondas usadas para la vuelta

| Destino | Sonda vuelta | IP | Nota |
|---------|-------------|----|----|
| Valparaíso | **6652** | 138.204.230.242 | AS61506, **sustituta** de la 31416 (Abandoned), mismo AS/ciudad |
| Habana | **12734** | 200.14.48.134 | La original del enunciado |
| Rusia | **870** | 90.151.87.167 | La original (su IP cambió, sigue AS12389 Rostelecom) |

### IDs de medición (vuelta) — verificables

| Destino | ICMP | UDP | TCP |
|---------|------|-----|-----|
| Valparaíso | [225420269](https://atlas.ripe.net/measurements/225420269/) | [225423328](https://atlas.ripe.net/measurements/225423328/) | [225423796](https://atlas.ripe.net/measurements/225423796/) |
| Habana | [225424159](https://atlas.ripe.net/measurements/225424159/) | [225424340](https://atlas.ripe.net/measurements/225424340/) | [225425843](https://atlas.ripe.net/measurements/225425843/) |
| Rusia | [225427525](https://atlas.ripe.net/measurements/225427525/) | [225427859](https://atlas.ripe.net/measurements/225427859/) | [225428926](https://atlas.ripe.net/measurements/225428926/) |

## 4.1 Tabla 2 — IDA vs VUELTA (con AS)

> IDA = sonda 1018349 → destino. VUELTA = sonda destino → 186.10.176.77.
> `(priv)` = IP privada/CGNAT. Los hops 1-2 de la IDA (`172.17.0.1`, `192.168.100.1`) son
> Docker + gateway local de mi lado; los de la VUELTA son la red interna del destino.

### Destino valparaiso (`138.204.228.2`)

**ICMP** — IDA 12 IPs · VUELTA 6 IPs · comunes 1

| HOP | IP IDA (AS) | IP VUELTA (AS) |
|---|---|---|
| 1 | 172.17.0.1 (priv) | 138.204.230.193 (61506) |
| 2 | 192.168.100.1 (priv) | 138.204.228.164 (61506) |
| 3 | 100.83.128.1 (priv) | 10.100.163.1 (priv) |
| 4 | 10.253.197.9 (priv) | 10.100.154.2 (priv) |
| 5 | 10.253.197.10 (priv) | 45.68.17.13 (priv) |
| 6 | 10.253.196.97 (priv) | 192.168.8.194 (priv) |
| 7 | 192.168.8.193 (priv) | * |
| 8 | 45.68.16.129 (priv) | * |
| 9 | 10.100.154.1 (priv) | * |
| 10 | 138.204.228.164 (61506) | * |
| 11 | 138.204.228.162 (61506) | * |
| 12 | 138.204.228.2 (61506) |  |

> **Interfaces espejo:** la VUELTA muestra `45.68.17.13` y `192.168.8.194`, que son las **otras
> interfaces** de los nodos vistos en la IDA como `45.68.16.129` y `192.168.8.193`. Igual
> `10.100.154.2` (vuelta) vs `10.100.154.1` (ida). Esto es exactamente lo que permite ver el
> medir en ambos sentidos.

**UDP** — IDA 11 IPs · VUELTA 6 IPs · comunes 1 — (misma estructura que ICMP en la vuelta)

| HOP | IP IDA (AS) | IP VUELTA (AS) |
|---|---|---|
| 1 | 172.17.0.1 (priv) | 138.204.230.193 (61506) |
| 2 | 192.168.100.1 (priv) | 138.204.228.164 (61506) |
| 3 | 100.83.128.1 (priv) | 10.100.163.1 (priv) |
| 4 | 10.253.197.9 (priv) | 10.100.154.2 (priv) |
| 5 | 10.253.197.10 (priv) | 45.68.17.13 (priv) |
| 6 | 10.253.196.97 (priv) | 192.168.8.194 (priv) |
| 7-11 | (ruta Entel, ver ICMP) | * |
| 12 | 138.204.228.2 no responde (UDP) |  |

**TCP** — IDA 9 IPs · VUELTA 7 IPs · comunes 0

| HOP | IP IDA (AS) | IP VUELTA (AS) |
|---|---|---|
| 1 | 172.17.0.1 (priv) | 138.204.230.193 (61506) |
| 2-6 | (ida Entel) | 138.204.228.164 → 10.100.163.1 → 10.100.154.2 → 45.68.17.13 → 192.168.8.194 |
| 11 | 138.204.228.162 (61506) | 138.204.230.193 (61506) |

### Destino habana (`200.14.48.134`)

**ICMP** — IDA 16 IPs · VUELTA 12 IPs · **comunes 0**

| HOP | IP IDA (AS) | IP VUELTA (AS) |
|---|---|---|
| 1 | 172.17.0.1 (priv) | 200.14.48.132 (27725) |
| 2 | 192.168.100.1 (priv) | 200.14.48.177 (27725) |
| 3 | 100.83.128.1 (priv) | 192.168.118.89 (priv) |
| 4 | 10.253.197.9 (priv) | 172.31.252.185 (priv) |
| 5 | 10.253.197.10 (priv) | 200.0.16.84 (11960) |
| 6 | 10.253.196.97 (priv) | 200.0.16.45 (11960) |
| 7 | 192.168.9.133 (priv) | 200.0.16.20 (11960) |
| 8 | 213.99.17.182 (**12956** ES) | 89.221.37.138 (**6762** TI Sparkle) |
| 9 | 5.53.5.41 (12956) | 89.221.41.155 (6762) |
| 10 | 213.140.35.86 (12956) | 89.221.41.235 (6762) |
| 11 | 193.251.143.67 (**5511** Orange) | 181.78.91.246 (**52468** UFINET PA) |
| 12 | * | 190.211.160.5 (52468) |
| 14-16 | 200.0.16.62/21/29 (11960) | * |
| 19-20 | 200.14.48.178 / .134 (27725) |  |

> **Asimetría de AS total (0 IPs comunes).** IDA Cuba: Entel → **Telxius AS12956 (ES)** →
> **Orange AS5511** → ETECSA. VUELTA Cuba: ETECSA → **Telecom Italia Sparkle AS6762** →
> **UFINET Panamá AS52468** → Level3 → Entel. Caminos de ida y vuelta por **proveedores
> distintos**.

**UDP** — IDA 18 IPs · VUELTA 12 IPs · comunes 0 (misma asimetría; UDP sí completa la ida)

**TCP** — IDA 7 IPs · VUELTA 11 IPs · comunes 0 (la IDA TCP casi no avanza; la VUELTA TCP llega lejos)

### Destino rusia (`37.79.153.66`)

**ICMP** — IDA 17 IPs · VUELTA 7 IPs · **comunes 0**

| HOP | IP IDA (AS) | IP VUELTA (AS) |
|---|---|---|
| 1 | 172.17.0.1 (priv) | 192.168.19.17 (priv) |
| 2 | 192.168.100.1 (priv) | 80.71.208.90 (**12389** Rostelecom) |
| 3 | 100.83.128.1 (priv) | 87.226.151.158 (12389) |
| 4-6 | 10.253.x (Entel) | 192.168.193.167 (priv) / * |
| 7 | 192.168.9.133 (priv) | 193.251.133.3 (**5511** Orange) |
| 8 | 213.99.17.182 (**12956**) | * |
| 9 | 5.53.3.75 (12956) | 200.189.207.14 (**3549** Level3) |
| 10 | 94.142.118.184 (12956) | 8.243.188.94 (**3356** Level3) |
| 11-15 | 195.2.x (**1273** Vodafone) | * |
| 18-19 | 217.107.123.25 / 37.79.153.66 (12389) |  |

> **Asimetría total (0 comunes).** IDA Rusia: Entel → Telxius AS12956 → **Vodafone AS1273** →
> Rostelecom. VUELTA Rusia: Rostelecom → **Orange AS5511** → **Level3 AS3356/3549** → Entel.
> El tránsito internacional de vuelta es completamente distinto (Level3 en vez de Vodafone).

**UDP** — IDA 18 IPs · VUELTA 8 IPs · comunes 0
**TCP** — IDA 12 IPs · VUELTA 9 IPs · comunes 0

*(tablas completas UDP/TCP en `scripts/build_tabla2.py` → se regeneran con
`python3 scripts/build_tabla2.py`)*

## 4.2 Conclusiones — ¿misma ruta? ¿misma cantidad de IPs?

| Destino | IPs comunes ida/vuelta | ¿Misma ruta? | ¿Misma cantidad de IPs? |
|---------|------------------------|--------------|--------------------------|
| Valparaíso | 1 (solo interfaces espejo) | **No** | No (IDA 9-12 vs VUELTA 6-7) |
| Habana | 0 | **No, totalmente asimétrica** | No (IDA 16-18 vs VUELTA 11-12) |
| Rusia | 0 | **No, totalmente asimétrica** | No (IDA 17-18 vs VUELTA 7-9) |

**Hallazgos:**
1. **La ruta NO es la misma de ida y vuelta** en ningún destino → ruteo **asimétrico**, lo
   normal en Internet (cada AS elige su salida según sus políticas BGP/acuerdos de tránsito).
2. **A nivel de AS la asimetría es drástica** en Habana y Rusia: usan proveedores de tránsito
   **distintos** en cada sentido (Cuba: ida Telxius+Orange / vuelta Telecom Italia+UFINET+Level3;
   Rusia: ida Vodafone / vuelta Level3).
3. **No se obtiene la misma cantidad de IPs**: la IDA suele revelar más hops (la VUELTA se
   corta antes por filtrado en el tramo final hacia mi BAF).
4. **Interfaces espejo** (caso Valparaíso): medir en ambos sentidos expuso las dos IPs de un
   mismo router (`45.68.16.129`↔`45.68.17.13`, `192.168.8.193`↔`192.168.8.194`,
   `10.100.154.1`↔`10.100.154.2`), que es el objetivo del path way bidireccional.

> Para el **Punto 5** se tomará, por cada destino, la **ruta más completa** combinando ida +
> vuelta (la ICMP en general), y se construirá el grafo en ndexbio.org.
