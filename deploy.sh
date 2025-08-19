#!/bin/bash

# Script de despliegue para MESERI en Digital Ocean
# Ejecutar como root o con sudo

set -e

echo "🚀 Iniciando despliegue de MESERI en Digital Ocean..."

# Variables
APP_NAME="meseri"
APP_DIR="/var/www/$APP_NAME"
GITHUB_REPO="https://github.com/hperezc/Proyecto_Meseri.git"
SERVICE_NAME="meseri"
NGINX_SITE="meseri"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
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

# Actualizar sistema
print_status "Actualizando sistema..."
apt update && apt upgrade -y

# Instalar dependencias del sistema
print_status "Instalando dependencias del sistema..."
apt install -y python3 python3-pip python3-venv nginx git supervisor

# Crear directorio de la aplicación
print_status "Creando directorio de la aplicación..."
mkdir -p $APP_DIR
cd $APP_DIR

# Clonar repositorio
print_status "Clonando repositorio desde GitHub..."
if [ -d ".git" ]; then
    print_status "Actualizando repositorio existente..."
    git pull origin main
else
    git clone $GITHUB_REPO .
fi

# Crear entorno virtual
print_status "Configurando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias de Python
print_status "Instalando dependencias de Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar permisos
print_status "Configurando permisos..."
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR

# Configurar Nginx
print_status "Configurando Nginx..."
cp nginx.conf /etc/nginx/sites-available/$NGINX_SITE
ln -sf /etc/nginx/sites-available/$NGINX_SITE /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Verificar configuración de Nginx
nginx -t

# Configurar servicio systemd
print_status "Configurando servicio systemd..."
cp systemd.service /etc/systemd/system/$SERVICE_NAME.service
systemctl daemon-reload
systemctl enable $SERVICE_NAME

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    print_status "Creando archivo .env..."
    cat > .env << EOF
DATABASE_URL=mysql://hperezc97:geoHCP97@mysql-hperezc97.alwaysdata.net/hperezc97_meseribd
SECRET_KEY=d978422048d1ad28cf337105b9dc5bad
FLASK_ENV=production
EOF
fi

# Iniciar servicios
print_status "Iniciando servicios..."
systemctl start $SERVICE_NAME
systemctl restart nginx

# Verificar estado de los servicios
print_status "Verificando estado de los servicios..."
systemctl status $SERVICE_NAME --no-pager
systemctl status nginx --no-pager

# Verificar puertos
print_status "Verificando puertos..."
netstat -tlnp | grep -E ':(80|5001)'

print_status "✅ Despliegue completado exitosamente!"
print_status "🌐 La aplicación estará disponible en: https://aplicativosgrd.crantioquia.org.co/meseri"
print_status "📊 Para ver logs: journalctl -u $SERVICE_NAME -f"
print_status "🔄 Para reiniciar: systemctl restart $SERVICE_NAME"
