# 0. Caracterización del entorno (BAF) e instalación de herramientas

> Path Discovery — Comparación de tráfico entre RIPE Atlas y Scamper
> Fecha de ejecución: 2026-10-17

## 0.1 Identificación de mi conexión (BAF / ISP)

Objetivo de la tarea: caracterizar la infraestructura de Internet de mi Banda Ancha Fija,
indicando **ISP** y **prefijo** de mi IP pública, según la info del AS (ver https://bgp.he.net).

### Comando — obtener IP pública
```bash
curl -s https://ifconfig.me ; echo
```
**Resultado:**
```
186.10.176.77
```

### Comando — obtener ISP / AS / prefijo (whois LACNIC)
```bash
whois 186.10.176.77 | grep -iE "netname|owner|aut-num|origin|inetnum|country|route"
```
**Resultado:**
```
inetnum:     186.10.128.0/18
aut-num:     AS27651
owner:       ENTEL CHILE S.A.
country:     CL
inetnum-up:  186.10.128.0/17
```

### Verificación cruzada en bgp.he.net
Consulta: `https://bgp.he.net/ip/186.10.176.77`

Resultado del sitio:
- rDNS / hostname: **z276.entelchile.net**
- Origin AS: **AS27651**
- Announcement (prefijo BGP): **186.10.176.0/24**
- Description: ENTEL CHILE S.A.
- "Address has 0 hosts associated with it."

Observación: el prefijo **anunciado por BGP** (`186.10.176.0/24`) es más **específico** que
el bloque asignado en LACNIC (`186.10.128.0/18`). Entel desagrega el /18 en /24 para la
publicación BGP (práctica común para ingeniería de tráfico / granularidad de ruteo).

| Dato | Valor |
|------|-------|
| IP pública | `186.10.176.77` |
| rDNS | z276.entelchile.net |
| ISP | ENTEL CHILE S.A. |
| ASN | **AS27651** |
| Prefijo asignado (LACNIC inetnum) | `186.10.128.0/18` |
| **Prefijo anunciado (BGP he.net)** | **`186.10.176.0/24`** |
| País | CL (Chile) |

## 0.2 IPs destino (sondas RIPE Atlas)

| Representa | IP destino | ID sonda RIPE |
|------------|-----------|---------------|
| Valparaíso (mayor velocidad mundial) | `138.204.228.2` | 31416 |
| Habana (peor velocidad mundial) | `200.14.48.134` | 12734 |
| Rusia (mayor censura reciente) | `37.79.153.66` | 870 |

## 0.3 Instalación de scamper 20260902 (última versión)

### Dependencias de compilación
```bash
sudo apt update
sudo apt install -y build-essential   # gcc, make (ya venían en Kali)
```

### Descargar, compilar e instalar
```bash
# Directorio de trabajo
mkdir -p ~/scamper_build && cd ~/scamper_build

# Descargar la última versión desde CAIDA
curl -O https://www.caida.org/catalog/software/scamper/code/scamper-cvs-20260902.tar.gz

# Extraer y compilar
tar xzf scamper-cvs-20260902.tar.gz
cd scamper-cvs-20260902
# IMPORTANTE: --disable-scamper-privsep para poder correr con capabilities (sin root).
# La separación de privilegios (privsep) necesita root real para chroot/setuid a /var/empty;
# al usar capabilities (CAP_NET_RAW) en vez de root, privsep falla con:
#   "scamper_privsep_init: could not mkdir /var/empty: Permission denied"
./configure --disable-scamper-privsep
make -j4
sudo make install
sudo ldconfig
```

### Permitir ejecución sin root (raw sockets vía capabilities)
En lugar de ejecutar `sudo scamper` cada vez, le damos capacidades de red al binario:
```bash
sudo setcap cap_net_raw,cap_net_admin+ep /usr/local/bin/scamper
```

### Verificación
```bash
scamper -v
getcap /usr/local/bin/scamper
```
**Resultado esperado:**
```
scamper version 20260902
/usr/local/bin/scamper cap_net_raw,cap_net_admin=ep
```

## 0.4 Herramientas de captura

```bash
# Ya instaladas en Kali. dumpcap trae cap_net_raw, así que tshark captura sin sudo:
getcap /usr/bin/dumpcap
# -> /usr/bin/dumpcap cap_net_admin,cap_net_raw=eip
tshark -v | head -1
```

Interfaz de salida a Internet (para capturar en la interfaz correcta):
```bash
ip route get 8.8.8.8 | awk '{print "iface:",$5; exit}'
```
