# 3. Path Discovery RIPE — Mediciones (Punto 2)

> Traceroute desde la sonda **1018349** (Entel, 186.10.176.77) hacia las 3 IPs, con los
> 3 protocolos que permite RIPE: **ICMP, UDP, TCP**. Parámetros por defecto de RIPE
> (packets=3, size=48, paris=0, max_hops=255); para UDP/TCP se fijó **puerto 33435**
> (el mismo usado en scamper, Punto 1).

## 3.0 Mediciones realizadas (IDs verificables)

| Destino | ICMP | UDP | TCP |
|---------|------|-----|-----|
| Valparaíso | [225408742](https://atlas.ripe.net/measurements/225408742/) | [225408893](https://atlas.ripe.net/measurements/225408893/) | [225410064](https://atlas.ripe.net/measurements/225410064/) |
| Habana | [225411780](https://atlas.ripe.net/measurements/225411780/) | [225411975](https://atlas.ripe.net/measurements/225411975/) | [225412195](https://atlas.ripe.net/measurements/225412195/) |
| Rusia | [225412517](https://atlas.ripe.net/measurements/225412517/) | [225412819](https://atlas.ripe.net/measurements/225412819/) | [225413533](https://atlas.ripe.net/measurements/225413533/) |

Comando usado (vía API, seleccionando la sonda por ID sin requisito de tag):
```bash
curl -s -X POST "https://atlas.ripe.net/api/v2/measurements/" \
  -H "Authorization: Key $KEY" -H "Content-Type: application/json" \
  --data '{
    "definitions":[{"target":"138.204.228.2","af":4,"type":"traceroute",
      "protocol":"ICMP","packets":3,"size":48,"paris":0,"is_oneoff":true}],
    "probes":[{"type":"probes","value":"1018349","requested":1}]}'
```
> UDP/TCP: agregar `"port":33435`. Script: `scripts/run_ripe_p2.sh`.
> Nota: se usó la API directa porque el cliente `ripe-atlas` añade el tag `system-ipv4-works`
> que la sonda (recién reconectada y tras NAT, tag `system-ipv4-rfc1918`) aún no tenía →
> "No suitable probes".

## 3.1 Tablas: IPs por hop y AS asociado

Leyenda AS: `priv` = IP privada/CGNAT (sin AS público). Números = ASN.

### Destino Valparaíso (`138.204.228.2`)

| HOP | ICMP (AS) | UDP (AS) | TCP (AS) |
|---|---|---|---|
| 1 | 172.17.0.1 (priv) | 172.17.0.1 (priv) | 172.17.0.1 (priv) |
| 2 | 192.168.100.1 (priv) | 192.168.100.1 (priv) | 192.168.100.1 (priv) |
| 3 | 100.83.128.1 (priv) | 100.83.128.1 (priv) | 100.83.128.1 (priv) |
| 4 | 10.253.197.9 (priv) | 10.253.197.9 (priv) | 10.253.197.9 (priv) |
| 5 | 10.253.197.10 (priv) | 10.253.197.10 (priv) | 10.253.197.10 (priv) |
| 6 | 10.253.196.97 (priv) | 10.253.196.97 (priv) | 10.253.196.97 (priv) |
| 7 | 192.168.8.193 (priv) | 192.168.8.193 (priv) | 192.168.8.193 (priv) |
| 8 | 45.68.16.129 (Entel/priv) | 45.68.16.129 (Entel/priv) | * |
| 9 | 10.100.154.1 (priv) | 10.100.154.1 (priv) | * |
| 10 | 138.204.228.164 (**61506**) | 138.204.228.164 (**61506**) | * |
| 11 | 138.204.228.162 (**61506**) | 138.204.228.162 (**61506**) | 138.204.228.162 (**61506**) |
| 12 | **138.204.228.2 (61506)** | * | * |

**Resumen:** ICMP → 12 hops, **llega**. UDP → 11 hops, no llega. TCP → 9 hops, no llega.

### Destino Habana (`200.14.48.134`)

| HOP | ICMP (AS) | UDP (AS) | TCP (AS) |
|---|---|---|---|
| 1–7 | (idénticos: priv) | (priv) | (priv) |
| 8 | 213.99.17.182 (**12956** ES) | 213.99.17.182 (12956) | * |
| 9 | 5.53.5.41 (12956) | 5.53.5.41 (12956) | * |
| 10 | 213.140.35.86 (12956) | 213.140.35.86 (12956) | * |
| 11 | 193.251.143.67 (**5511** Orange) | 193.251.143.67 (5511) | * |
| 12–13 | * | * | * |
| 14 | 200.0.16.62 (**11960** ETECSA-IXP) | 200.0.16.62 (11960) | * |
| 15 | 200.0.16.21 (11960) | 200.0.16.21 (11960) | * |
| 16 | 200.0.16.29 (11960) | 200.0.16.25 (11960) | * |
| 18/19 | * | * | * |
| 19 | 200.14.48.178 (**27725**) | 200.14.48.178 (27725) | * |
| 20 | **200.14.48.134 (27725)** | **200.14.48.134 (27725)** | * |

**Resumen:** ICMP → 16 hops, **llega**. UDP → 18 hops, **llega**. TCP → 7 hops, no llega.

### Destino Rusia (`37.79.153.66`)

| HOP | ICMP (AS) | UDP (AS) | TCP (AS) |
|---|---|---|---|
| 1–7 | (idénticos: priv) | (priv) | (priv) |
| 8 | 213.99.17.182 (**12956** ES) | 213.99.17.182 (12956) | * |
| 9 | 5.53.3.75 (12956) | 5.53.5.41 (12956) | 5.53.5.41 (12956) |
| 10 | 94.142.118.184 (12956) | 94.142.119.188 (12956) | * |
| 11 | 195.2.29.185 (**1273** Vodafone) | 195.2.29.185 (1273) | 195.2.29.185 (1273) |
| 12 | 195.2.3.126 (1273) | 195.2.3.126 (1273) | 195.2.3.126 (1273) |
| 13 | 195.2.20.118 (1273) | 195.2.20.118 (1273) | * |
| 14 | 195.2.3.117 (1273) | 195.2.3.117 (1273) | 195.2.8.230 (1273) |
| 15 | 195.2.8.205 (1273) | 195.2.8.205 (1273) | 195.2.9.242 (1273) |
| 16 | * | 195.27.81.54 (1273) | * |
| 18 | 217.107.123.25 (**12389** Rostelecom) | 217.107.123.25 (12389) | * |
| 19 | **37.79.153.66 (12389)** | * | * |

**Resumen:** ICMP → 17 hops, **llega**. UDP → 18 hops, no llega. TCP → 12 hops, no llega.

> El valor `172.17.0.1` que aparece suelto en algún hop intermedio (p.ej. UDP de Habana/Rusia)
> es un artefacto de la **containerización**: la sonda recibe ocasionalmente un ICMP de su
> propio gateway Docker; no es un nodo real de la ruta.

## 3.2 Comparación de los 3 protocolos — ¿cuál da más información?

| Destino | ICMP llega | UDP llega | TCP llega | Más completo |
|---------|-----------|-----------|-----------|--------------|
| Valparaíso | ✅ (12) | ❌ (11) | ❌ (9) | **ICMP** |
| Habana | ✅ (16) | ✅ (18) | ❌ (7) | UDP/ICMP |
| Rusia | ✅ (17) | ❌ (18*) | ❌ (12) | **ICMP** |

**Conclusión:** **ICMP es el protocolo más indicado** — es el único que **completa la ruta en
los 3 destinos**. UDP revela muchos hops (incluso más que ICMP en Habana/Rusia porque sondea
puertos que generan Time-Exceeded), pero **no alcanza el destino** en Valparaíso y Rusia
(esos destinos no devuelven ICMP Port-Unreachable ante UDP). TCP (SYN a 33435) es el **peor**:
el SYN es filtrado/limitado en el núcleo internacional y deja muchos `*`.

Esto es **coherente con el Punto 1 (scamper)**: ahí también ICMP/ICMP-Paris fueron los más
completos y UDP/TCP fallaron en Valparaíso y Rusia.

## 3.3 Análisis de tráfico (Wireshark) — firmas de RIPE

Capturas en `evidencia_ripe/pcap/`. En el cable, el origen es `192.168.100.74` (la IP privada
de la VM; el contenedor sale con NAT; la IP pública real 186.10.176.77 figura en el JSON).

| Protocolo | L4 | Puerto/ID | Varía por sonda | Paquetes/hop | Tamaño |
|-----------|----|-----------|-----------------|--------------|--------|
| ICMP | Echo (t8) | **ident fijo 36864** | icmp.seq incremental | **3** | ip.len 76 |
| UDP | UDP | sport **fijo 20480**, dport **incremental** (33435+) | dport (+1) | **3** | ip.len 76 |
| TCP | SYN | sport fijo 20480, dport **fijo 33435** | IP-ID / seq | **3** | — |

**Predicción de valores (firmas propias de RIPE Atlas):**
- RIPE envía **3 sondas por TTL** (parámetro `packets=3`), frente a 1 de scamper por defecto.
- **ICMP:** `ident` constante **36864** (0x9000), `seq` incremental global (4,5,6…), TTL repetido 3 veces por hop.
- **UDP:** `srcport` constante **20480** (0x5000), `dstport` incremental desde 33435 (estilo UDP clásico, `paris=0`), payload mayor (size=48 → 76 bytes IP).
- **TCP:** `srcport` 20480, `dstport` 33435 fijo, flag **SYN**.
- Las constantes 20480/36864 son **firmas reconocibles** del software de sonda RIPE.

## 3.4 Nodo que no responde — amenaza para el auditor

- **IPs `138.204.228.2` (Valparaíso) y `37.79.153.66` (Rusia)**: **no responden a UDP ni a
  TCP-SYN** (no se alcanza el destino por esos protocolos), pero **sí responden a ICMP Echo**
  (ambas completan por ICMP).
  - **Regla del nodo/destino:** firewall que descarta UDP a puertos altos (sin Port-Unreachable)
    y filtra/limita TCP SYN a puertos no estándar.
  - **Cómo saltarse la regla:** usar **ICMP Echo**, que sí es respondido → identifica el equipo.
- El tramo TCP se degrada ya en el **núcleo internacional** (AS12956/AS1273): los routers no
  generan Time-Exceeded para SYN o aplican rate-limit, dejando `*`.

## 3.5 Diferencia scamper (Punto 1) vs RIPE (Punto 2)

- **Misma ruta de AS**: Entel (priv/45.68) → Telxius AS12956 (ES) → Orange AS5511 / Vodafone
  AS1273 → ETECSA AS11960/27725 (Cuba) / Rostelecom AS12389 (Rusia). Confirma la
  infraestructura por ambos métodos.
- **Hop extra en RIPE:** la sonda añade `172.17.0.1` (gateway Docker) como hop 1, porque corre
  containerizada; scamper corría directo en el host. El resto de la ruta coincide.
- RIPE usa 3 sondas/hop (más robusto estadísticamente); scamper 1/hop por defecto.
