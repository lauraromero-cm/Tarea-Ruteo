# Informe — Path Discovery (RIPE Atlas vs Scamper)

**Autor:** leocacru@gmail.com · **ISP:** Entel Chile (AS27651) · **IP pública:** 186.10.176.77
(prefijo BGP `186.10.176.0/24`)

## Índice

| # | Documento | Estado |
|---|-----------|--------|
| 0 | [00_setup_entorno.md](00_setup_entorno.md) — ISP/AS/prefijo, instalación scamper, bridged | ✅ Completo |
| 1 | [01_scamper_path_discovery.md](01_scamper_path_discovery.md) — 6 métodos + tracelb, Tabla 1, análisis tráfico, nodo que filtra | ✅ Completo |
| — | [COMANDOS.md](COMANDOS.md) — todos los comandos reproducibles (Punto 0 y 1) | ✅ Completo |
| — | [GUIA_WIRESHARK.md](GUIA_WIRESHARK.md) — dónde están los pcap y filtros por método | ✅ Completo |
| 2 | Path Discovery RIPE (UDP/ICMP/TCP + AS por hop) | ⏸️ Stand-by (requiere sonda + API RIPE) |
| 4 | Path way RIPE (ida y vuelta, Tabla 2) | ⏸️ Stand-by |
| 5 | Public Path (grafos en ndexbio.org, 3 UUID) | ⏸️ Stand-by |

## Estructura de evidencia

```
evidencia/
├── warts/   # salidas binarias scamper (.warts) — 33 mediciones
├── txt/     # conversión legible (sc_warts2text) — 33
├── pcap/    # capturas por método (sondas salientes)
└── pcap2/   # re-capturas de Valparaíso con filtro correcto (incluye retorno ICMP)
scripts/
├── run_scamper_p1.sh    # driver completo Punto 1
├── build_tabla1.py      # genera Tabla 1 desde los .txt
└── test_bridged.sh      # verificación post-cambio a bridged
```

## Hallazgos clave del Punto 1
1. **ICMP-Paris** es el método más completo (llega a los 3 destinos, menos `*`).
2. **Firewall stateful de Entel (~hop 4)** inyecta **RST falsos** ante TCP-ACK (detectado por TTL 252 vs 245).
3. **138.204.228.2 y 37.79.153.66 no responden a UDP** pero sí a **ICMP Echo**.
4. **tracelb icmp-echo** revela mejor las ramas ECMP (múltiples IPs por hop).
