# 🚀 Guía de Despliegue MESERI en Digital Ocean

## 📋 Información del Proyecto

- **Aplicación**: MESERI (Método Simplificado de Evaluación de Riesgo de Incendio)
- **Repositorio**: https://github.com/hperezc/Proyecto_Meseri
- **Servidor**: Digital Ocean (45.55.212.201)
- **Dominio**: https://aplicativosgrd.crantioquia.org.co/meseri
- **Base de Datos**: AlwaysData (mysql-hperezc97.alwaysdata.net)

## 🛠️ Requisitos Previos

### En el Servidor Digital Ocean:
- Ubuntu 20.04+ o CentOS 7+
- Acceso root o sudo
- Git instalado
- Python 3.8+
- Nginx
- MySQL (opcional, para futuras migraciones)

### Puertos a Verificar:
- **Puerto 80**: Nginx (HTTP)
- **Puerto 443**: Nginx (HTTPS)
- **Puerto 5001**: Aplicación MESERI
- **Puerto 22**: SSH

## 📦 Archivos de Configuración Creados

1. **`gunicorn.conf.py`**: Configuración del servidor WSGI
2. **`nginx.conf`**: Configuración del proxy reverso
3. **`systemd.service`**: Servicio systemd para la aplicación
4. **`deploy.sh`**: Script de despliegue automatizado
5. **`check_ports.sh`**: Script para verificar puertos ocupados
6. **`update.sh`**: Script para actualizaciones desde GitHub

## 🚀 Pasos de Despliegue

### 1. Conectar al Servidor

```bash
ssh root@45.55.212.201
```

### 2. Verificar Puertos Ocupados

```bash
# Ejecutar el script de verificación
chmod +x check_ports.sh
./check_ports.sh
```

### 3. Ejecutar Despliegue Automatizado

```bash
# Descargar archivos de configuración
cd /tmp
git clone https://github.com/hperezc/Proyecto_Meseri.git temp_meseri
cd temp_meseri

# Ejecutar script de despliegue
chmod +x deploy.sh
sudo ./deploy.sh
```

### 4. Verificar Despliegue

```bash
# Verificar estado de servicios
systemctl status meseri
systemctl status nginx

# Verificar puertos
netstat -tlnp | grep -E ':(80|5001)'

# Verificar logs
journalctl -u meseri -f
```

## 🔧 Configuración Manual (Alternativa)

Si prefieres configurar manualmente:

### 1. Instalar Dependencias

```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv nginx git
```

### 2. Clonar Repositorio

```bash
mkdir -p /var/www/meseri
cd /var/www/meseri
git clone https://github.com/hperezc/Proyecto_Meseri.git .
```

### 3. Configurar Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Nginx

```bash
cp nginx.conf /etc/nginx/sites-available/meseri
ln -sf /etc/nginx/sites-available/meseri /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

### 5. Configurar Servicio Systemd

```bash
cp systemd.service /etc/systemd/system/meseri.service
systemctl daemon-reload
systemctl enable meseri
systemctl start meseri
```

## 🔄 Actualizaciones

### Actualización Automática

```bash
cd /var/www/meseri
chmod +x update.sh
sudo ./update.sh
```

### Actualización Manual

```bash
cd /var/www/meseri
systemctl stop meseri
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
systemctl start meseri
```

## 📊 Monitoreo y Logs

### Ver Logs de la Aplicación

```bash
# Logs en tiempo real
journalctl -u meseri -f

# Últimos 100 logs
journalctl -u meseri -n 100

# Logs de errores
journalctl -u meseri -p err
```

### Ver Logs de Nginx

```bash
# Logs de acceso
tail -f /var/log/nginx/access.log

# Logs de error
tail -f /var/log/nginx/error.log
```

### Verificar Estado de Servicios

```bash
# Estado de MESERI
systemctl status meseri

# Estado de Nginx
systemctl status nginx

# Verificar puertos
netstat -tlnp | grep -E ':(80|5001)'
```

## 🔒 Seguridad

### Firewall (UFW)

```bash
# Instalar UFW
apt install ufw

# Configurar reglas
ufw allow ssh
ufw allow 'Nginx Full'
ufw enable
```

### SSL/HTTPS (Opcional)

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx

# Obtener certificado
certbot --nginx -d aplicativosgrd.crantioquia.org.co
```

## 🗄️ Base de Datos

### Configuración Actual (AlwaysData)

La aplicación está configurada para usar la base de datos en AlwaysData:

```python
DATABASE_URL=mysql://hperezc97:geoHCP97@mysql-hperezc97.alwaysdata.net/hperezc97_meseribd
```

### Migración Futura a Digital Ocean

Para migrar la base de datos a Digital Ocean:

1. Instalar MySQL en el servidor
2. Crear base de datos y usuario
3. Migrar datos desde AlwaysData
4. Actualizar configuración en `.env`

## 🚨 Solución de Problemas

### La Aplicación No Responde

```bash
# Verificar estado del servicio
systemctl status meseri

# Verificar logs
journalctl -u meseri -n 50

# Verificar puerto
netstat -tlnp | grep 5001

# Reiniciar servicio
systemctl restart meseri
```

### Error de Base de Datos

```bash
# Verificar conectividad
mysql -h mysql-hperezc97.alwaysdata.net -u hperezc97 -p

# Verificar variables de entorno
cat /var/www/meseri/.env
```

### Error de Nginx

```bash
# Verificar configuración
nginx -t

# Verificar logs
tail -f /var/log/nginx/error.log

# Reiniciar Nginx
systemctl restart nginx
```

## 📞 Contacto y Soporte

- **Desarrollador**: Héctor Camilo Pérez Contreras
- **Email**: hectorcperez21@gmail.com
- **GitHub**: @hperezc
- **LinkedIn**: Héctor Camilo Pérez Contreras

## 📝 Notas Importantes

1. **Puerto 5001**: La aplicación MESERI usa el puerto 5001 para evitar conflictos con otras aplicaciones
2. **Base de Datos**: Mantiene conexión a AlwaysData hasta futura migración
3. **Backups**: Los scripts crean backups automáticos antes de actualizar
4. **Logs**: Todos los logs se guardan en systemd journal
5. **Permisos**: La aplicación corre como usuario www-data

## 🔄 Control de Versiones

La aplicación está conectada al repositorio de GitHub para facilitar:
- Despliegues automáticos
- Control de versiones
- Rollbacks en caso de problemas
- Actualizaciones incrementales
