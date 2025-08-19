#!/bin/bash

# Script para actualizar la aplicación MESERI desde GitHub
# Ejecutar cuando se hagan cambios en el repositorio

set -e

echo "🔄 Iniciando actualización de MESERI..."

# Variables
APP_NAME="meseri"
APP_DIR="/var/www/$APP_NAME"
SERVICE_NAME="meseri"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si se ejecuta como root
if [ "$EUID" -ne 0 ]; then
    print_error "Este script debe ejecutarse como root o con sudo"
    exit 1
fi

# Navegar al directorio de la aplicación
cd $APP_DIR

# Crear backup antes de actualizar
print_status "Creando backup de la aplicación..."
BACKUP_DIR="/var/backups/meseri/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR
cp -r * $BACKUP_DIR/ 2>/dev/null || true

# Detener el servicio
print_status "Deteniendo servicio MESERI..."
systemctl stop $SERVICE_NAME

# Actualizar desde GitHub
print_status "Actualizando código desde GitHub..."
git fetch origin
git reset --hard origin/main

# Activar entorno virtual
source venv/bin/activate

# Actualizar dependencias
print_status "Actualizando dependencias de Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Aplicar migraciones de base de datos si existen
if [ -f "init_db.py" ]; then
    print_status "Aplicando migraciones de base de datos..."
    python init_db.py
fi

# Configurar permisos
print_status "Configurando permisos..."
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR

# Reiniciar servicios
print_status "Reiniciando servicios..."
systemctl start $SERVICE_NAME
systemctl reload nginx

# Verificar estado
print_status "Verificando estado de los servicios..."
systemctl status $SERVICE_NAME --no-pager

# Verificar que la aplicación responde
print_status "Verificando que la aplicación responde..."
sleep 5
if curl -s http://localhost:5001 > /dev/null; then
    print_status "✅ Aplicación respondiendo correctamente"
else
    print_warning "⚠️ La aplicación no responde, revisar logs"
    journalctl -u $SERVICE_NAME --no-pager -n 20
fi

print_status "✅ Actualización completada exitosamente!"
print_status "🌐 La aplicación estará disponible en: https://aplicativosgrd.crantioquia.org.co/meseri"
print_status "📊 Para ver logs: journalctl -u $SERVICE_NAME -f"
