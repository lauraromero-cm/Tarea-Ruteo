# Links importantes — Tarea Path Discovery

> Documento vivo: se completa con los IDs de medición RIPE a medida que se generan.

## Infraestructura / entorno
- Mi IP pública en bgp.he.net: https://bgp.he.net/ip/186.10.176.77
- Mi AS (Entel): https://bgp.he.net/AS27651
- Sonda RIPE Atlas (ID 1018349): https://atlas.ripe.net/probes/1018349/

## Destinos
- Valparaíso 138.204.228.2 (AS61506 INSACOM): https://bgp.he.net/ip/138.204.228.2
- Habana 200.14.48.134 (AS27725 ETECSA): https://bgp.he.net/ip/200.14.48.134
- Rusia 37.79.153.66 (AS12389 Rostelecom): https://bgp.he.net/ip/37.79.153.66

## Mediciones RIPE — Punto 2 (ida: sonda 1018349 -> destino)

| Destino | Protocolo | ID | Link |
|---------|-----------|----|----|
| Valparaíso | ICMP | 225408742 | https://atlas.ripe.net/measurements/225408742/ |
| Valparaíso | UDP | 225408893 | https://atlas.ripe.net/measurements/225408893/ |
| Valparaíso | TCP | 225410064 | https://atlas.ripe.net/measurements/225410064/ |
| Habana | ICMP | 225411780 | https://atlas.ripe.net/measurements/225411780/ |
| Habana | UDP | 225411975 | https://atlas.ripe.net/measurements/225411975/ |
| Habana | TCP | 225412195 | https://atlas.ripe.net/measurements/225412195/ |
| Rusia | ICMP | 225412517 | https://atlas.ripe.net/measurements/225412517/ |
| Rusia | UDP | 225412819 | https://atlas.ripe.net/measurements/225412819/ |
| Rusia | TCP | 225413533 | https://atlas.ripe.net/measurements/225413533/ |

### Re-capturas con tráfico de retorno (Valparaíso, para análisis Wireshark)
- ICMP: https://atlas.ripe.net/measurements/225419454/
- UDP: https://atlas.ripe.net/measurements/225419811/
- TCP: https://atlas.ripe.net/measurements/225420022/

## Mediciones RIPE — Punto 4 (vuelta: sonda destino -> mi IP 186.10.176.77)
Sondas: Valparaíso=6652 (AS61506, sustituta de 31416 Abandoned), Habana=12734, Rusia=870.

| Destino | ICMP | UDP | TCP |
|---------|------|-----|-----|
| Valparaíso | https://atlas.ripe.net/measurements/225420269/ | https://atlas.ripe.net/measurements/225423328/ | https://atlas.ripe.net/measurements/225423796/ |
| Habana | https://atlas.ripe.net/measurements/225424159/ | https://atlas.ripe.net/measurements/225424340/ | https://atlas.ripe.net/measurements/225425843/ |
| Rusia | https://atlas.ripe.net/measurements/225427525/ | https://atlas.ripe.net/measurements/225427859/ | https://atlas.ripe.net/measurements/225428926/ |

## Grafos ndexbio — Punto 5 (3 UUID)

| Destino | UUID | Link |
|---------|------|------|
| Valparaíso | 0acc00aa-ccbe-11f1-be0a-005056ae3c32 | https://www.ndexbio.org/viewer/networks/0acc00aa-ccbe-11f1-be0a-005056ae3c32 |
| Habana | 0b0957cd-ccbe-11f1-be0a-005056ae3c32 | https://www.ndexbio.org/viewer/networks/0b0957cd-ccbe-11f1-be0a-005056ae3c32 |
| Rusia | 0b48f7e0-ccbe-11f1-be0a-005056ae3c32 | https://www.ndexbio.org/viewer/networks/0b48f7e0-ccbe-11f1-be0a-005056ae3c32 |

IDs RIPE usados por grafo (ida / vuelta):
- Valparaíso: 225408742 / 225423796
- Habana: 225411975 / 225424159
- Rusia: 225412819 / 225428926
