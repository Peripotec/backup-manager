# Backup Manager

Sistema automatizado para la gestión de backups de equipos de red (Huawei, Cisco, Mikrotik, etc.).

> **Filosofía del Proyecto**: Este sistema está diseñado para ser **robusto**, **escalable** y, sobre todo, **fácil de entender**. Cada componente está documentado y la interfaz de usuario guía al operador en cada paso.

## 📚 Documentación

Toda la documentación detallada se encuentra en la carpeta `docs/`:

- [📘 Manual de Usuario](docs/USER_MANUAL.md): Guía paso a paso para operadores (cómo agregar equipos, ver backups, etc.).
- [🛠️ Guía de Despliegue](docs/DEPLOY.md): Instrucciones para instalar el sistema en un servidor Linux (Debian/Ubuntu).
- [🏗️ Arquitectura](docs/ARCHITECTURE.md): Explicación técnica de cómo funciona el sistema por dentro.
- [🔧 Troubleshooting](docs/TROUBLESHOOTING.md): Solución a problemas comunes.

## 🚀 Inicio Rápido (Desarrollo)

### Backend (Python)
1. Instalar dependencias: `pip install -r backend/requirements.txt`
2. Iniciar servidor: `uvicorn app.main:app --reload`
3. Ver documentación API: `http://localhost:8000/docs`

### Frontend (React)
*Nota: Requiere Node.js instalado.*
1. Instalar dependencias: `cd frontend && npm install`
2. Iniciar servidor: `npm run dev`
3. Acceder a la web: `http://localhost:5173`

## 🌟 Características Clave

- **Multi-Vendor**: Soporte nativo para Huawei, con arquitectura extensible para otras marcas.
- **Diagnóstico Automático**: Si un backup falla, el sistema ejecuta ping y traceroute automáticamente.
- **Notificaciones**: Alertas por email con reportes detallados.
- **Rotación Inteligente**: Política de retención de 30 días + históricos mensuales.
- **UI Autodescriptiva**: Interfaz diseñada para explicar cada acción al usuario.
