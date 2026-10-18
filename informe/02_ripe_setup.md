# 2. Path Discovery RIPE — Instalación de la sonda (setup)

> Sonda RIPE Atlas por software, en Docker, sobre la misma VM Kali (Entel AS27651).

## 2.1 Instalación de la sonda con Docker

Imagen usada: `jamesits/ripe-atlas` (empaquetado estándar de la sonda por software).

```bash
# 1) Directorios persistentes (para no perder la clave al reiniciar)
mkdir -p /home/kali/Tarea_Ruteo/ripe-atlas/{etc,run,spool}

# 2) Descargar imagen
docker pull docker.io/jamesits/ripe-atlas:latest

# 3) Levantar el contenedor
docker run -d --restart always --name ripe-atlas \
  --memory=64m \
  --cap-drop ALL \
  --cap-add NET_RAW --cap-add KILL --cap-add SETUID --cap-add SETGID \
  --cap-add CHOWN --cap-add FOWNER --cap-add DAC_OVERRIDE \
  -v /home/kali/Tarea_Ruteo/ripe-atlas/etc:/etc/ripe-atlas \
  -v /home/kali/Tarea_Ruteo/ripe-atlas/run:/run/ripe-atlas \
  -v /home/kali/Tarea_Ruteo/ripe-atlas/spool:/var/spool/ripe-atlas \
  docker.io/jamesits/ripe-atlas:latest

# 4) Verificar
docker ps --filter name=ripe-atlas
docker logs ripe-atlas | tail -20
```

## 2.2 Clave pública generada

La sonda genera su par de claves en `ripe-atlas/etc/`. La **clave pública** a registrar:

```bash
cat /home/kali/Tarea_Ruteo/ripe-atlas/etc/probe_key.pub
```

> Guardada en `ripe-atlas/MI_CLAVE_PUBLICA.txt`.

**Nota sobre el log:** antes de registrar la clave, el log muestra
`REGINIT exit with error` / `ssh-permission-denied`. Es **normal**: el servidor de registro
de RIPE aún no conoce la clave. También aparece `Network is unreachable` para IPv6 porque la
VM no tiene IPv6 (usará IPv4). Ambos desaparecen tras registrar y conectar.

## 2.3 Registro de la sonda (requiere cuenta RIPE)

1. Crear/entrar con cuenta **RIPE NCC Access**: https://access.ripe.net/
2. Ir al formulario: **https://atlas.ripe.net/apply/swprobe/**
3. Pegar la **clave pública** (`probe_key.pub`).
4. Datos de la conexión:
   - **ASN:** AS27651 (ENTEL CHILE S.A.)
   - **IP pública:** 186.10.176.77
5. Enviar. El registro es **manual/diferido**: la sonda no aparece al instante.
6. Cuando el estado pase a **Connected**, anotar el **Probe ID** (aparece en el dashboard).

### Probe ID de mi sonda
- **Probe ID: `1018349`**
- Status: **Connected** (confirmado vía `https://atlas.ripe.net/api/v2/probes/1018349/`)
- address_v4: `186.10.176.77` · asn_v4: `27651` (Entel) · país: CL
- Dashboard: https://atlas.ripe.net/probes/1018349/

Verificación por consola:
```bash
docker logs ripe-atlas 2>&1 | grep -iE "KEEP connection|controller"   # conexión al controlador
curl -s "https://atlas.ripe.net/api/v2/probes/1018349/" | python3 -c "import sys,json;print(json.load(sys.stdin)['status']['name'])"
# -> Connected
```

## 2.4bis Estado de créditos (BLOQUEADOR)

Primera medición de prueba (ICMP a 138.204.228.2 desde la sonda 1018349) devolvió:
```
"You do not have enough credit to schedule this measurement.
 The cost of this measurement is: 60.0cr, while your current balance is 0cr."
```
Una sonda recién conectada parte con **0 créditos**. Para medir se necesita:
- **Opción A:** esperar la acumulación por hospedaje (~900 cr/h, acreditado periódicamente → horas).
- **Opción B (recomendada):** solicitar transferencia de créditos del curso/profesor
  (el PDF muestra una cuenta con ~666M créditos → *My Credits → Transfer credits*).

Necesidad estimada total: ~18 mediciones (9 ida + 9 vuelta) × 60cr ≈ **1.080 cr**.

## 2.4 Créditos y API key

- **Créditos:** se acumulan por hospedar la sonda (o los asigna el curso). Verlos en
  *atlas.ripe.net > My Credits*.
- **API key:** *atlas.ripe.net > My API Keys > (+) Generate*. Crear una key con permiso para
  **crear mediciones** (`Measurement creation`). Guardarla para usar `ripe-atlas` CLI.

### Instalar el cliente de consola (Magellan / ripe-atlas CLI)
```bash
pipx install ripe.atlas.tools    # o: pip install --user ripe.atlas.tools
ripe-atlas configure --set authorisation.create=TU_API_KEY
```

---

> **Siguiente:** cuando la sonda esté Connected y con API key, se harán las mediciones
> traceroute (UDP/ICMP/TCP) desde esta sonda hacia las 3 IPs → documento `03_ripe_mediciones.md`.
