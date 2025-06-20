// Manejo del almacenamiento offline
const STORE_KEY = 'infraestructura_forms';

// Función para guardar borrador
function guardarBorrador() {
    const form = document.getElementById('infraForm');
    if (!form) {
        mostrarNotificacion('Formulario no encontrado', 'error');
        return false;
    }
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Validar campos requeridos
    const requiredFields = ['central', 'nombre'];
    const missingFields = requiredFields.filter(field => !data[field] || data[field].trim() === '');
    
    if (missingFields.length > 0) {
        mostrarNotificacion(`Faltan campos requeridos: ${missingFields.join(', ')}`, 'error');
        
        // Enfocar el primer campo faltante
        const firstMissingField = form.querySelector(`[name="${missingFields[0]}"]`);
        if (firstMissingField) {
            firstMissingField.focus();
            firstMissingField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        
        return false;
    }
    
    let stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    
    // Agregar metadatos adicionales
    const draftData = {
        ...data,
        timestamp: new Date().toISOString(),
        syncStatus: 'pending',
        id: 'draft_' + Date.now(), // ID único para el borrador
        userAgent: navigator.userAgent
    };
    
    stored.push(draftData);
    localStorage.setItem(STORE_KEY, JSON.stringify(stored));
    
    mostrarNotificacion(`✓ Borrador guardado: ${data.central} - ${data.nombre}`, 'warning');
    updatePendingCounter();
    
    console.log('Debug - Borrador guardado exitosamente:', draftData.id);
    
    return true;
}

// Función para sincronizar formularios pendientes
async function syncPendingForms() {
    if (!navigator.onLine) {
        console.log('Debug - Sin conexión, cancelando sincronización');
        return;
    }
    
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    
    console.log(`Debug - Iniciando sincronización de ${pending.length} formularios`);
    
    if (pending.length === 0) {
        console.log('Debug - No hay formularios pendientes para sincronizar');
        return;
    }
    
    let syncedCount = 0;
    let errorCount = 0;
    
    for (const form of pending) {
        try {
            console.log(`Debug - Sincronizando: ${form.central} - ${form.nombre}`);
            
            // Extraer solo los campos del formulario (sin metadatos)
            const formData = {
                central: form.central,
                nombre: form.nombre,
                numero_pisos: form.numero_pisos,
                superficie_mayor_sector: form.superficie_mayor_sector,
                resistencia_fuego: form.resistencia_fuego,
                falsos_techos: form.falsos_techos,
                distancia_bomberos: form.distancia_bomberos,
                tiempo_llegada: form.tiempo_llegada,
                accesibilidad_edificio: form.accesibilidad_edificio,
                peligro_activacion: form.peligro_activacion,
                carga_fuego: form.carga_fuego,
                combustibilidad: form.combustibilidad,
                orden_limpieza: form.orden_limpieza,
                almacenamiento_altura: form.almacenamiento_altura,
                concentracion_valores: form.concentracion_valores,
                por_calor: form.por_calor,
                por_humo: form.por_humo,
                por_corrosion: form.por_corrosion,
                por_agua: form.por_agua,
                propagabilidad_horizontal: form.propagabilidad_horizontal,
                propagabilidad_vertical: form.propagabilidad_vertical,
                deteccion_automatica: form.deteccion_automatica,
                rociadores_automaticos: form.rociadores_automaticos,
                extintores_portatiles: form.extintores_portatiles,
                bocas_incendio: form.bocas_incendio,
                hidrantes_exteriores: form.hidrantes_exteriores,
                equipos_primera_intervencion: form.equipos_primera_intervencion,
                equipos_segunda_intervencion: form.equipos_segunda_intervencion,
                planes_emergencia: form.planes_emergencia
            };
            
            console.log('Debug - Datos a enviar:', formData);
            
            const response = await fetch('/guardar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            console.log('Debug - Respuesta del servidor:', result);
            
                         if (response.ok && result.success) {
                form.syncStatus = 'synced';
                form.syncedAt = new Date().toISOString();
                syncedCount++;
                console.log(`Debug - Formulario sincronizado exitosamente: ${form.central} - ${form.nombre}`);
                
                // Actualizar inmediatamente el localStorage con el estado sincronizado
                const updatedStored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
                const itemIndex = updatedStored.findIndex(item => item.id === form.id);
                if (itemIndex !== -1) {
                    updatedStored[itemIndex].syncStatus = 'synced';
                    updatedStored[itemIndex].syncedAt = new Date().toISOString();
                    localStorage.setItem(STORE_KEY, JSON.stringify(updatedStored));
                }
            } else {
                errorCount++;
                console.error('Debug - Error en respuesta del servidor:', result.error || 'Error desconocido');
                mostrarNotificacion(`Error al sincronizar ${form.central}: ${result.error || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            errorCount++;
            console.error('Debug - Error de red al sincronizar:', error);
            mostrarNotificacion(`Error de conexión al sincronizar ${form.central}: ${error.message}`, 'error');
        }
    }
    
         // Guardar cambios finales
    localStorage.setItem(STORE_KEY, JSON.stringify(stored));
    
    // Forzar actualización inmediata del contador
    setTimeout(() => {
        updatePendingCounter();
        console.log('Debug - Contador actualizado después de sincronización');
    }, 100);
    
    // Mostrar resumen
    if (syncedCount > 0) {
        mostrarNotificacion(`${syncedCount} formulario(s) sincronizado(s) correctamente`, 'success');
        
        // Actualizar también la información de pendientes
        setTimeout(() => {
            const currentPending = JSON.parse(localStorage.getItem(STORE_KEY) || '[]')
                .filter(item => item.syncStatus === 'pending');
            
            if (currentPending.length === 0) {
                const pendingInfo = document.getElementById('pending-info');
                if (pendingInfo) {
                    pendingInfo.innerHTML = `
                        <div class="alert alert-success alert-dismissible">
                            <i class="fas fa-check-circle"></i>
                            ¡Todos los formularios han sido sincronizados!
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    `;
                    
                    // Auto-ocultar después de 3 segundos
                    setTimeout(() => {
                        if (pendingInfo.querySelector('.alert-success')) {
                            pendingInfo.innerHTML = '';
                        }
                    }, 3000);
                }
            }
        }, 200);
    }
    
    if (errorCount > 0) {
        mostrarNotificacion(`${errorCount} formulario(s) con errores de sincronización`, 'error');
    }
    
    console.log(`Debug - Sincronización completada: ${syncedCount} exitosos, ${errorCount} errores`);
}

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo) {
    // Remover notificaciones anteriores
    const existingNotifications = document.querySelectorAll('.notification-custom');
    existingNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${tipo} alert-dismissible notification-custom`;
    
    const iconMap = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle', 
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    
    notification.innerHTML = `
        <i class="fas ${iconMap[tipo] || 'fa-info-circle'}"></i>
        <strong>${mensaje}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
    
    console.log(`Notificación mostrada: ${tipo} - ${mensaje}`);
}

// Registrar el service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('ServiceWorker registrado');
            })
            .catch(error => {
                console.error('Error al registrar ServiceWorker:', error);
            });
    });
}

// Función para actualizar el estado de conectividad
function updateOnlineStatus() {
    const isOnline = navigator.onLine;
    const status = isOnline ? 'online' : 'offline';
    const statusElement = document.getElementById('connection-status');
    
    console.log(`Debug - Actualizando estado: ${status}`);
    
    if (statusElement) {
        statusElement.textContent = isOnline ? 'En línea' : 'Sin conexión';
        statusElement.className = isOnline ? 
            'badge bg-success connection-badge' : 'badge bg-warning connection-badge';
    }
    
    // Mostrar/ocultar botón de sincronización
    const syncButton = document.getElementById('sync-button');
    if (syncButton) {
        syncButton.style.display = isOnline ? 'inline-block' : 'none';
    }
    
    // Mostrar indicador visual offline
    const offlineIndicator = document.getElementById('offline-indicator');
    if (!offlineIndicator && !isOnline) {
        const indicator = document.createElement('div');
        indicator.id = 'offline-indicator';
        indicator.className = 'offline-indicator show';
        indicator.innerHTML = '<i class="fas fa-wifi"></i> Modo offline - Los datos se guardarán localmente';
        document.body.appendChild(indicator);
    } else if (offlineIndicator && isOnline) {
        offlineIndicator.remove();
    }
    
    console.log(`Estado de conexión: ${status}`);
}

// Función para actualizar el contador de formularios pendientes
function updatePendingCounter() {
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    const synced = stored.filter(item => item.syncStatus === 'synced');
    
    // Limpiar formularios sincronizados antiguos (más de 24 horas)
    if (synced.length > 0) {
        const now = new Date();
        const oneDayAgo = new Date(now.getTime() - (24 * 60 * 60 * 1000));
        
        const cleanedStored = stored.filter(item => {
            if (item.syncStatus === 'synced' && item.syncedAt) {
                const syncedDate = new Date(item.syncedAt);
                return syncedDate > oneDayAgo; // Mantener solo los últimos 24 horas
            }
            return true; // Mantener todos los pendientes y sin fecha
        });
        
        if (cleanedStored.length !== stored.length) {
            localStorage.setItem(STORE_KEY, JSON.stringify(cleanedStored));
            console.log(`Debug - Limpiados ${stored.length - cleanedStored.length} formularios sincronizados antiguos`);
        }
    }
    
    const counterElement = document.getElementById('pending-counter');
    if (counterElement) {
        counterElement.textContent = pending.length;
        counterElement.style.display = pending.length > 0 ? 'inline-block' : 'none';
        counterElement.className = pending.length > 0 ? 'badge bg-danger ms-2 pending-counter' : 'badge bg-danger ms-2';
    }
    
    const pendingInfo = document.getElementById('pending-info');
    if (pendingInfo) {
        if (pending.length > 0) {
            pendingInfo.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    Tienes ${pending.length} formulario(s) pendiente(s) de sincronizar
                </div>
            `;
        } else {
            pendingInfo.innerHTML = '';
        }
    }
}

// Función para mostrar lista de borradores
function showDrafts() {
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    
    if (pending.length === 0) {
        mostrarNotificacion('No hay borradores guardados', 'info');
        return;
    }
    
    let draftsHTML = '<div class="modal fade" id="draftsModal" tabindex="-1"><div class="modal-dialog modal-lg"><div class="modal-content">';
    draftsHTML += '<div class="modal-header"><h5 class="modal-title">Borradores Guardados</h5>';
    draftsHTML += '<button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>';
    draftsHTML += '<div class="modal-body"><div class="list-group">';
    
    pending.forEach((draft, index) => {
        const date = new Date(draft.timestamp).toLocaleString();
        draftsHTML += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${draft.central} - ${draft.nombre}</h6>
                    <small>${date}</small>
                </div>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteDraft(${index})">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            </div>
        `;
    });
    
    draftsHTML += '</div></div></div></div></div>';
    
    // Remover modal anterior si existe
    const existingModal = document.getElementById('draftsModal');
    if (existingModal) existingModal.remove();
    
    document.body.insertAdjacentHTML('beforeend', draftsHTML);
    const modal = new bootstrap.Modal(document.getElementById('draftsModal'));
    modal.show();
}

// Función para eliminar un borrador
function deleteDraft(index) {
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    
    if (confirm('¿Estás seguro de que quieres eliminar este borrador?')) {
        // Encontrar el índice real en el array completo
        const realIndex = stored.findIndex(item => 
            item.timestamp === pending[index].timestamp
        );
        
        if (realIndex !== -1) {
            stored.splice(realIndex, 1);
            localStorage.setItem(STORE_KEY, JSON.stringify(stored));
            updatePendingCounter();
            
            // Recargar la lista de borradores
            document.getElementById('draftsModal').remove();
            showDrafts();
            
            mostrarNotificacion('Borrador eliminado', 'success');
        }
    }
}

// Función para sincronización manual
async function manualSync() {
    console.log('Debug - Sincronización manual iniciada');
    
    if (!navigator.onLine) {
        mostrarNotificacion('No hay conexión a internet', 'error');
        return;
    }
    
    // Verificar si hay formularios pendientes
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    
    if (pending.length === 0) {
        mostrarNotificacion('No hay formularios pendientes para sincronizar', 'info');
        return;
    }
    
    const syncButton = document.getElementById('sync-button');
    if (syncButton) {
        syncButton.disabled = true;
        syncButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sincronizando...';
        syncButton.classList.add('sync-button-loading');
    }
    
    try {
        console.log('Debug - Iniciando sincronización manual');
        await syncPendingForms();
        console.log('Debug - Sincronización manual completada');
    } catch (error) {
        console.error('Debug - Error en sincronización manual:', error);
        mostrarNotificacion('Error durante la sincronización', 'error');
    } finally {
        if (syncButton) {
            syncButton.disabled = false;
            syncButton.innerHTML = '<i class="fas fa-sync"></i> Sincronizar';
            syncButton.classList.remove('sync-button-loading');
        }
    }
}

// Función para manejar el envío del formulario
function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    console.log('Debug - Procesando envío de formulario');
    console.log('Debug - Estado de conexión:', navigator.onLine);
    
    // Validación básica
    if (!data.central || !data.nombre) {
        mostrarNotificacion('Por favor complete los campos obligatorios', 'error');
        return;
    }
    
    // Si no hay conexión, guardar offline inmediatamente
    if (!navigator.onLine) {
        console.log('Debug - Sin conexión, guardando offline');
        const success = guardarBorrador();
        if (success) {
            form.reset();
        }
        return;
    }
    
    // Si hay conexión, intentar enviar al servidor
    console.log('Debug - Con conexión, enviando al servidor');
    enviarAlServidor(data, form);
}

// Función para enviar datos al servidor
async function enviarAlServidor(data, form) {
    try {
        const response = await fetch('/guardar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarNotificacion('Datos guardados correctamente en el servidor', 'success');
            form.reset();
            
            // Preguntar si quiere ver el dashboard
            setTimeout(() => {
                if (confirm('¿Desea ver el dashboard con los resultados?')) {
                    window.location.href = '/dashboard/';
                }
            }, 1000);
        } else {
            mostrarNotificacion('Error al guardar: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Error al enviar al servidor:', error);
        console.log('Debug - Error de red, guardando offline como respaldo');
        
        // Si falla el envío, guardar offline como respaldo
        const success = guardarBorrador();
        if (success) {
            form.reset();
        }
    }
}

// Función para test de conectividad real
async function testRealConnectivity() {
    if (!navigator.onLine) {
        return false;
    }
    
    try {
        const response = await fetch('/static/img/logo-cruz-roja.png', {
            method: 'HEAD',
            cache: 'no-cache'
        });
        return response.ok;
    } catch {
        return false;
    }
}

// Inicializar los listeners y contadores
window.addEventListener('online', () => {
    console.log('Debug - Evento online detectado');
    updateOnlineStatus();
    syncPendingForms();
});

window.addEventListener('offline', () => {
    console.log('Debug - Evento offline detectado');
    updateOnlineStatus();
});

window.addEventListener('load', () => {
    console.log('Debug - Página cargada, inicializando...');
    updateOnlineStatus();
    updatePendingCounter();
    
    // Configurar el event listener del formulario
    const form = document.getElementById('infraForm');
    if (form) {
        console.log('Debug - Configurando event listener del formulario');
        form.addEventListener('submit', handleFormSubmit);
    } else {
        console.log('Debug - Formulario no encontrado');
    }
    
    // Test periódico de conectividad cada 30 segundos
    setInterval(async () => {
        const reallyOnline = await testRealConnectivity();
        if (navigator.onLine !== reallyOnline) {
            console.log('Debug - Discrepancia detectada en conectividad');
            updateOnlineStatus();
        }
    }, 30000);
});