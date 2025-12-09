# Guía de Solución de Problemas (Troubleshooting)

Esta guía ayuda a resolver los problemas más comunes que pueden surgir durante la operación del Backup Manager.

## 1. Problemas de Conexión con Equipos

### Síntoma: "Connection Timeout" o "Authentication Failed" en el log.

**Posibles Causas:**
- El equipo está apagado o inalcanzable.
- Credenciales incorrectas.
- Firewall bloqueando SSH/Telnet.

**Pasos de Diagnóstico:**

**1. Verificar Diagnóstico Automático:**
El sistema debería haber ejecutado un Ping. Revise el detalle del backup fallido en la Web.

**2. Prueba Manual:**
Desde el servidor, intente conectar manualmente:

```bash
ping <ip-equipo>
telnet <ip-equipo>
# o
ssh user@<ip-equipo>
```

**3. Revisar Credenciales:**
Asegúrese de que el usuario/password en el Inventario sean correctos.

## 2. Problemas del Sistema

### Síntoma: La Web no carga.

**Pasos:**

**1. Verificar si el servicio backend está corriendo:**

```bash
sudo systemctl status backup-manager
```

**2. Verificar Nginx:**

```bash
sudo systemctl status nginx
```

**3. Revisar logs del backend:**

```bash
journalctl -u backup-manager -f
```

### Síntoma: "Error 500" al intentar guardar un equipo.

**Causa Probable:**
- Error de base de datos o permisos.

**Solución:**
- Verifique que el archivo de base de datos (`backup_manager.db`) tenga permisos de escritura para el usuario que ejecuta el servicio.
- Revise los logs del backend para ver el error específico de Python.

## 3. Problemas de Espacio en Disco

### Síntoma: Los backups fallan con error de escritura.

**Solución:**

**1. Verificar espacio libre:**

```bash
df -h
```

**2. Si el disco está lleno:**
Puede ser necesario ajustar la política de retención o borrar backups antiguos manualmente en `/opt/backup-manager/backups/`.
