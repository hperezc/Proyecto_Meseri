#!/bin/bash

# Script para verificar puertos ocupados en Digital Ocean
# Útil para identificar qué aplicaciones están corriendo

echo "🔍 Verificando puertos ocupados en el servidor..."
echo "================================================"

# Verificar puertos comunes
echo "📊 Puertos más comunes:"
netstat -tlnp | grep -E ':(80|443|22|21|25|110|143|993|995|3306|5432|27017|6379|8080|3000|5000|5001|8000|9000)'

echo ""
echo "🌐 Servicios web (puertos 80, 443, 8080, 3000, 5000, 5001, 8000, 9000):"
netstat -tlnp | grep -E ':(80|443|8080|3000|5000|5001|8000|9000)'

echo ""
echo "🗄️ Bases de datos (puertos 3306, 5432, 27017, 6379):"
netstat -tlnp | grep -E ':(3306|5432|27017|6379)'

echo ""
echo "🔧 Servicios SSH y FTP (puertos 22, 21):"
netstat -tlnp | grep -E ':(22|21)'

echo ""
echo "📧 Servicios de correo (puertos 25, 110, 143, 993, 995):"
netstat -tlnp | grep -E ':(25|110|143|993|995)'

echo ""
echo "📋 Todos los puertos TCP en uso:"
netstat -tlnp

echo ""
echo "🔍 Procesos que podrían estar usando puertos:"
echo "Nginx:"
ps aux | grep nginx | grep -v grep

echo ""
echo "Apache:"
ps aux | grep apache | grep -v grep

echo ""
echo "Python/Flask:"
ps aux | grep python | grep -v grep

echo ""
echo "Node.js:"
ps aux | grep node | grep -v grep

echo ""
echo "✅ Verificación completada"
