# 5. Public Path — Grafos en NDEx (Punto 5)

> Por cada destino se tomó la **ruta más completa** del Punto 4 (ida + vuelta) y se generó un
> grafo dirigido, publicado en https://www.ndexbio.org/. La descripción de cada grafo incluye
> los **2 IDs de medición RIPE** (traceroute de ida y de vuelta) usados en su construcción.

## 5.1 Grafos publicados (3 UUID)

| Destino | UUID | Visor | ida (ID) | vuelta (ID) |
|---------|------|-------|----------|-------------|
| **Valparaíso** `138.204.228.2` | `0acc00aa-ccbe-11f1-be0a-005056ae3c32` | [ver](https://www.ndexbio.org/viewer/networks/0acc00aa-ccbe-11f1-be0a-005056ae3c32) | ICMP **225408742** | TCP **225423796** |
| **Habana** `200.14.48.134` | `0b0957cd-ccbe-11f1-be0a-005056ae3c32` | [ver](https://www.ndexbio.org/viewer/networks/0b0957cd-ccbe-11f1-be0a-005056ae3c32) | UDP **225411975** | ICMP **225424159** |
| **Rusia** `37.79.153.66` | `0b48f7e0-ccbe-11f1-be0a-005056ae3c32` | [ver](https://www.ndexbio.org/viewer/networks/0b48f7e0-ccbe-11f1-be0a-005056ae3c32) | UDP **225412819** | TCP **225428926** |

- Valparaíso: 17 nodos, 17 aristas
- Habana: 28 nodos, 27 aristas
- Rusia: 25 nodos, 25 aristas

## 5.2 Construcción del grafo

Cada grafo combina en una sola vista las dos mediciones (ida + vuelta) de ese destino:
- **Nodos** = IPs de los hops (atributos: `name` = IP, `AS` = ASN o "privada/CGNAT").
- **Aristas dirigidas** = saltos consecutivos, con atributo `direction` = `ida` o `vuelta`.
- **Atributos de red:** `description` (con los 2 IDs), `ida_measurement_id`, `vuelta_measurement_id`.

Al unir ambos sentidos, los nodos con **misma IP** se fusionan y se visualizan las **interfaces
espejo** (p.ej. en Valparaíso `45.68.16.129` de la ida junto a `45.68.17.13` de la vuelta) y la
**asimetría de ruteo** (en Habana/Rusia los caminos de ida y vuelta no comparten nodos).

### Comandos
```bash
# generar los 3 grafos CX2
python3 scripts/build_graphs.py
# publicarlos en NDEx (requiere credenciales)
NDEX_USER="usuario" NDEX_PASS="clave" python3 scripts/build_graphs.py upload
```
Archivos CX2 locales: `evidencia_ripe/graphs/{valparaiso,habana,rusia}.cx2`.

> Nota: los grafos están en modo **PUBLIC**. Si se requiere, se pueden abrir en el editor web de
> NDEx para ajustar el layout visual antes de entregar.
