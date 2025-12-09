# Manual de Usuario

Bienvenido al Backup Manager. Este sistema le ayudará a mantener seguros los respaldos de sus equipos de red.

## 1. Conceptos Básicos

- **Dispositivo (Device)**: Un equipo de red (Router, Switch, OLT) que se va a respaldar.
- **Backup**: Una copia de la configuración del dispositivo en un momento dado.
- **Vendor**: El fabricante del equipo (ej. Huawei, Cisco).

## 2. Gestión de Dispositivos

### Agregar un Nuevo Equipo
1. Vaya a la sección **Inventario** en el menú lateral.
2. Haga clic en el botón **"Nuevo Dispositivo"**.
3. Complete el formulario:
   - **Nombre**: Un identificador único (ej. `Core-Rafaela`).
   - **IP**: La dirección IP de gestión.
   - **Vendor**: Seleccione la marca (esto define cómo nos conectamos).
   - **Protocolo**: Se recomienda **SSH** por seguridad, use **Telnet** solo si es necesario.
   - **Credenciales**: Usuario y contraseña del equipo.
4. Haga clic en **Guardar**.

> [!TIP]
> Pase el mouse sobre los iconos de interrogación (?) en el formulario para ver consejos sobre cada campo.

### Editar o Borrar
En la tabla de inventario, use los botones de **Lápiz** (Editar) o **Basura** (Borrar) a la derecha de cada fila.

## 3. Realizar Backups

### Backup Manual
1. En el **Inventario**, busque el equipo deseado.
2. Haga clic en el botón **"Ejecutar Backup"** (icono de Play ▶️).
3. Espere unos segundos. Verá una notificación con el resultado.

### Backups Automáticos
El sistema realiza backups automáticamente todos los días a las 03:00 AM (por defecto). Puede cambiar esto en la sección **Configuración**.

## 4. Ver Historial y Logs

1. Vaya a la sección **Historial**.
2. Verá una lista de todos los backups realizados.
3. Haga clic en el icono de **Ojo** 👁️ para ver detalles:
   - Si fue **Exitoso**: Verá el contenido del archivo de configuración.
   - Si **Falló**: Verá el error y el diagnóstico automático (Ping/Traceroute) para ayudarle a entender qué pasó.

## 5. Solución de Problemas Comunes

- **Error de Autenticación**: Verifique que la contraseña en el Inventario sea la correcta. Intente conectarse manualmente al equipo.
- **Timeout**: El equipo tardó mucho en responder. Verifique si hay congestión en la red.
