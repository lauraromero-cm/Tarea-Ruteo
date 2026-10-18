# Guía de capturas en Wireshark — Punto 1

## Dónde están las capturas

| Carpeta | Contenido | Uso recomendado |
|---------|-----------|-----------------|
| `evidencia/pcap2/` | 6 trazas de Valparaíso con filtro `host <ip> or icmp` | **Mejor evidencia**: incluye los ICMP Time-Exceeded de retorno |
| `evidencia/pcap/` | Las 33 mediciones (filtro `host <ip>`) | Sondas salientes + respuesta del destino |

Abrir una captura:
```bash
wireshark /home/kali/Tarea_Ruteo/evidencia/pcap2/trace_valparaiso_icmp.pcap &
```

---

## 1) Filtro de CAPTURA (al grabar) — sintaxis BPF

Es el que pusimos en `dumpcap -f "..."`. Para capturar una traza y ver también el retorno:

```
host 138.204.228.2 or icmp
```

En Wireshark gráfico: *Capture → Options → Capture filter* y escribe esa línea antes de iniciar.

Otros filtros de captura útiles:
| Objetivo | Filtro de captura (BPF) |
|----------|-------------------------|
| Solo tráfico con el destino | `host 138.204.228.2` |
| Destino + ICMP de routers | `host 138.204.228.2 or icmp` |
| Solo UDP del rango traceroute | `udp portrange 33434-33534` |
| Solo el puerto TCP de sonda | `tcp port 33435` |

---

## 2) Filtros de VISUALIZACIÓN (display filter) por método

Escríbelos en la **barra de filtro** de Wireshark (arriba) tras abrir el `.pcap`.

### UDP (clásico)
```
udp && ip.src == 192.168.100.74
```
Qué observar: `udp.dstport` **sube +1** por paquete (33435, 33436…); `ip.ttl` sube 1,2,3…;
`udp.checksum` **baja −1**. Para ver el retorno: `icmp.type == 11` (Time-Exceeded).

### ICMP
```
icmp && ip.src == 192.168.100.74
```
Qué observar: `icmp.type == 8` (Echo Request), `icmp.ident` fijo, `icmp.seq` incremental.
Respuestas: `icmp.type == 11` (routers) y `icmp.type == 0` (echo-reply del destino).

### UDP-Paris
```
udp && ip.src == 192.168.100.74
```
Qué observar (clave): `udp.dstport` **FIJO** (33435) y `udp.checksum` **incremental** →
el flujo no cambia (misma ruta bajo balanceo de carga).

### ICMP-Paris
```
icmp && ip.src == 192.168.100.74
```
Qué observar (clave): `icmp.checksum` **constante** (0xbeec) aunque `icmp.seq` cambie.

### TCP (SYN)
```
tcp && ip.src == 192.168.100.74
```
Qué observar: `tcp.flags.syn == 1` (flags 0x002), `tcp.dstport` fijo, `tcp.srcport` fijo.

### TCP-ACK (detección del RST falso)
```
tcp
```
Qué observar: sondas con `tcp.flags.ack == 1` (0x010). La respuesta del "destino" en el hop 4
es un **RST**: filtra con
```
tcp.flags.reset == 1
```
y mira la columna **TTL** del paquete (`ip.ttl == 252`). Compáralo con el echo-reply genuino
(`icmp.type == 0` en la captura ICMP, `ip.ttl == 245`). TTL distintos = RST falsificado.

---

## 3) Filtros para evidenciar los hallazgos (capturas de pantalla sugeridas)

| Hallazgo | Archivo | Display filter |
|----------|---------|----------------|
| Puerto UDP incremental | `pcap2/trace_valparaiso_udp.pcap` | `udp && ip.src==192.168.100.74` |
| UDP-Paris flujo fijo | `pcap2/trace_valparaiso_udp-paris.pcap` | `udp && ip.src==192.168.100.74` |
| ICMP-Paris checksum fijo | `pcap2/trace_valparaiso_icmp-paris.pcap` | `icmp && ip.src==192.168.100.74` |
| Time-Exceeded de routers | `pcap2/trace_valparaiso_icmp.pcap` | `icmp.type==11` |
| **RST falso (firewall)** | `pcap2/trace_valparaiso_tcp-ack.pcap` | `tcp.flags.reset==1` |

> Para la columna TTL en Wireshark: clic derecho en un campo `Time to live` dentro de la
> sección IP → *Apply as Column*. Así el TTL aparece como columna y se ve el 252 vs 245.
