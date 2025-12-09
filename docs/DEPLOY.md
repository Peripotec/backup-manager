# Guía de Despliegue en Linux (Debian/Ubuntu)

Este documento detalla los pasos para instalar el Backup Manager en un servidor de producción.

## Prerrequisitos

- Servidor con Debian 11/12 o Ubuntu 20.04/22.04.
- Acceso root o sudo.
- Conexión a internet.

## 1. Preparación del Sistema

Actualizar el sistema e instalar herramientas básicas:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nodejs npm git iputils-ping traceroute
```

## 2. Instalación del Backend

**1. Crear directorio de la aplicación:**

```bash
sudo mkdir -p /opt/backup-manager
sudo chown $USER:$USER /opt/backup-manager
cd /opt/backup-manager
```

**2. Copiar los archivos del proyecto (o clonar repositorio):**

```bash
git clone https://github.com/Peripotec/backup-manager.git .
```

*Nota: El punto final `.` clona en el directorio actual (`/opt/backup-manager`).*

**3. Crear entorno virtual Python:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**4. Instalar dependencias:**

```bash
pip install -r backend/requirements.txt
```

**5. Configurar variables de entorno:**

Crear archivo `.env` en `backend/` con:

```env
DATABASE_URL=sqlite:////opt/backup-manager/backup_manager.db
SMTP_SERVER=mail.wiltel.com.ar
SMTP_PORT=25
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=admin@wiltel.com.ar
SMTP_RECIPIENTS=noc@wiltel.com.ar
```

## 3. Instalación del Frontend

**1. Ir al directorio frontend:**

```bash
cd frontend
```

**2. Instalar dependencias y construir:**

```bash
npm install
npm run build
```

*Esto generará una carpeta `dist/` con los archivos estáticos.*

## 4. Configuración del Servicio (Systemd)

Para que el backend se ejecute automáticamente al iniciar:

**1. Crear archivo `/etc/systemd/system/backup-manager.service`:**

```ini
[Unit]
Description=Backup Manager Backend
After=network.target

[Service]
User=root
WorkingDirectory=/opt/backup-manager/backend
ExecStart=/opt/backup-manager/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**2. Activar servicio:**

```bash
sudo systemctl enable backup-manager
sudo systemctl start backup-manager
```

## 5. Configuración del Firewall (UFW)

> [!NOTE]
> Según su configuración actual, ya tiene reglas que permiten el tráfico desde sus IPs de gestión (ej. `200.2.127.153`, `10.100.0.0/16`) hacia cualquier puerto.

**1. No es necesario agregar nuevas reglas** si va a acceder desde esas redes confiables.

**2. Solo verifique que el estado sea activo:**

```bash
sudo ufw status verbose
```

*Debería ver sus reglas `ALLOW IN` desde sus IPs.*

## 6. Servir el Frontend (Nginx bajo /manager)

Configuración recomendada para servir el frontend bajo el path `/manager` y la API bajo `/manager/api`.

**1. Actualizar configuración de Nginx:**

Edite el archivo de sitio (ej. `/etc/nginx/sites-available/backup-manager`):

```nginx
server {
    listen 80;
    server_name backup.testwilnet.com.ar;

    # Redirección de /manager a /manager/
    location = /manager {
        return 301 /manager/;
    }

    # Frontend (React/Vite)
    location /manager/ {
        alias /opt/backup-manager/frontend/dist/;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API (FastAPI)
    location /manager/api/ {
        proxy_pass http://127.0.0.1:8000/;
    }
}
```

**2. Verificar configuración:**

```bash
sudo nginx -t
```

**3. Recargar Nginx:**

```bash
sudo systemctl reload nginx
```

## 7. Compilación del Frontend (REQUERIDO)

Cada vez que se realicen cambios, **debe compilar el frontend** para que tome la configuración de rutas correcta.

```bash
cd /opt/backup-manager/frontend
npm install
npm run build
```

*Esto generará los assets en `dist/` con las rutas relativas a `/manager/`.*

## Verificación

1. Acceda a `https://backup.testwilnet.com.ar/manager/` para ver la nueva interfaz.
2. Acceda a `https://backup.testwilnet.com.ar/manager/api/docs` para ver la documentación de la API (Swagger).
