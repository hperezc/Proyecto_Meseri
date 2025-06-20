// Funcionalidad offline completa para MESERI
const STORE_KEY = 'infraestructura_forms';
let isOnline = navigator.onLine;

// Función para actualizar el estado de conexión
function updateOnlineStatus() {
    isOnline = navigator.onLine;
    const statusBar = document.getElementById('status-bar');
    const statusText = document.getElementById('status-text');
    const pendingCounter = document.getElementById('pending-counter');
    
    if (statusBar && statusText) {
        if (isOnline) {
            statusBar.className = 'status-bar status-online';
            statusText.textContent = '🟢 Conectado - Los datos se guardan automáticamente';
            // Intentar sincronizar automáticamente cuando se recupere la conexión
            setTimeout(syncPendingForms, 1000);
        } else {
            statusBar.className = 'status-bar status-offline';
            statusText.textContent = '🔴 Sin conexión - Los datos se guardan localmente';
        }
    }
    
    updatePendingCounter();
}

// Función para actualizar el contador de formularios pendientes
function updatePendingCounter() {
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    const pendingCounter = document.getElementById('pending-counter');
    
    if (pendingCounter) {
        if (pending.length > 0) {
            pendingCounter.textContent = pending.length;
            pendingCounter.style.display = 'inline-block';
        } else {
            pendingCounter.style.display = 'none';
        }
    }
    
    // Forzar actualización del DOM
    setTimeout(() => {
        const counter = document.getElementById('pending-counter');
        if (counter && pending.length > 0) {
            counter.textContent = pending.length;
            counter.style.display = 'inline-block';
        } else if (counter) {
            counter.style.display = 'none';
        }
    }, 100);
}

// Función para validar campos requeridos
function validarCamposRequeridos(formData) {
    const camposRequeridos = [
        'central', 'nombre', 'numero_pisos', 'superficie_mayor_sector',
        'resistencia_fuego', 'falsos_techos', 'distancia_bomberos',
        'tiempo_llegada', 'accesibilidad_edificio'
    ];
    
    const camposFaltantes = [];
    
    for (const campo of camposRequeridos) {
        if (!formData[campo] || formData[campo].trim() === '') {
            camposFaltantes.push(campo);
        }
    }
    
    return {
        valido: camposFaltantes.length === 0,
        camposFaltantes: camposFaltantes
    };
}

// Función para guardar borrador
function guardarBorrador() {
    try {
        const form = document.getElementById('infraForm');
        if (!form) {
            mostrarNotificacion('No se encontró el formulario', 'error');
            return;
        }
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Validar campos requeridos
        const validacion = validarCamposRequeridos(data);
        if (!validacion.valido) {
            mostrarNotificacion(`Campos requeridos faltantes: ${validacion.camposFaltantes.join(', ')}`, 'warning');
            return;
        }
        
        let stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
        
        const nuevoFormulario = {
            ...data,
            id: Date.now().toString(),
            timestamp: new Date().toISOString(),
            syncStatus: 'pending',
            userAgent: navigator.userAgent
        };
        
        stored.push(nuevoFormulario);
        localStorage.setItem(STORE_KEY, JSON.stringify(stored));
        
        mostrarNotificacion('✅ Formulario guardado localmente', 'success');
        updatePendingCounter();
        
        // Limpiar formulario después de guardar
        form.reset();
        
    } catch (error) {
        console.error('Error guardando borrador:', error);
        mostrarNotificacion('❌ Error al guardar el borrador', 'error');
    }
}

// Función para sincronizar formularios pendientes
async function syncPendingForms() {
    if (!navigator.onLine) {
        mostrarNotificacion('🔴 Sin conexión a internet', 'warning');
        return;
    }
    
    const syncButton = document.getElementById('sync-button');
    if (syncButton) {
        syncButton.innerHTML = '<span class="loading-spinner"></span>Sincronizando...';
        syncButton.disabled = true;
    }
    
    try {
        const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
        const pending = stored.filter(item => item.syncStatus === 'pending');
        
        if (pending.length === 0) {
            mostrarNotificacion('✅ No hay formularios pendientes de sincronización', 'info');
            return;
        }
        
        mostrarNotificacion(`🔄 Sincronizando ${pending.length} formulario(s)...`, 'info');
        
        let sincronizados = 0;
        let errores = 0;
        
        for (const form of pending) {
            try {
                // Extraer solo los campos del formulario, sin metadatos
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
                
                const response = await fetch('/guardar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                if (response.ok) {
                    form.syncStatus = 'synced';
                    sincronizados++;
                } else {
                    const errorData = await response.json();
                    console.error('Error del servidor:', errorData);
                    errores++;
                }
                
            } catch (error) {
                console.error('Error sincronizando formulario:', error);
                errores++;
            }
        }
        
        // Limpiar formularios sincronizados del localStorage
        const updatedStored = stored.filter(item => item.syncStatus !== 'synced');
        localStorage.setItem(STORE_KEY, JSON.stringify(updatedStored));
        
        // Mostrar resultado
        if (sincronizados > 0) {
            mostrarNotificacion(`✅ ${sincronizados} formulario(s) sincronizado(s) correctamente`, 'success');
        }
        if (errores > 0) {
            mostrarNotificacion(`❌ ${errores} formulario(s) con errores`, 'error');
        }
        
        updatePendingCounter();
        
    } catch (error) {
        console.error('Error en sincronización:', error);
        mostrarNotificacion('❌ Error durante la sincronización', 'error');
    } finally {
        if (syncButton) {
            syncButton.innerHTML = '🔄 Sincronizar Pendientes';
            syncButton.disabled = false;
        }
    }
}

// Función para mostrar borradores guardados
function mostrarBorradores() {
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    
    if (pending.length === 0) {
        mostrarNotificacion('📝 No hay borradores guardados', 'info');
        return;
    }
    
    let html = '<div class="mt-3"><h5>Borradores Guardados:</h5>';
    
    pending.forEach((draft, index) => {
        const fecha = new Date(draft.timestamp).toLocaleString();
        html += `
            <div class="draft-item">
                <h6>${draft.nombre} - ${draft.central}</h6>
                <small>Guardado: ${fecha}</small>
                <div class="draft-actions">
                    <button class="btn btn-sm btn-primary" onclick="cargarBorrador(${index})">📝 Cargar</button>
                    <button class="btn btn-sm btn-danger" onclick="eliminarBorrador(${index})">🗑️ Eliminar</button>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    const container = document.createElement('div');
    container.innerHTML = html;
    document.body.appendChild(container);
    
    setTimeout(() => {
        container.remove();
    }, 10000);
}

// Función para cargar un borrador
function cargarBorrador(index) {
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    
    if (pending[index]) {
        const draft = pending[index];
        const form = document.getElementById('infraForm');
        
        // Cargar datos en el formulario
        Object.keys(draft).forEach(key => {
            if (key !== 'timestamp' && key !== 'syncStatus' && key !== 'id' && key !== 'userAgent') {
                const field = form.querySelector(`[name="${key}"]`);
                if (field) {
                    field.value = draft[key];
                }
            }
        });
        
        mostrarNotificacion('📝 Borrador cargado en el formulario', 'success');
    }
}

// Función para eliminar un borrador
function eliminarBorrador(index) {
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    
    if (pending[index]) {
        const allStored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
        const draftToRemove = pending[index];
        const updatedStored = allStored.filter(item => item.id !== draftToRemove.id);
        
        localStorage.setItem(STORE_KEY, JSON.stringify(updatedStored));
        mostrarNotificacion('🗑️ Borrador eliminado', 'info');
        updatePendingCounter();
    }
}

// Función para mostrar notificaciones mejoradas
function mostrarNotificacion(mensaje, tipo) {
    // Remover notificaciones existentes
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${tipo}`;
    notification.textContent = mensaje;
    
    document.body.appendChild(notification);
    
    // Mostrar con animación
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Ocultar después de 4 segundos
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 4000);
}

// Función para manejar el envío del formulario
async function manejarEnvioFormulario(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Validar campos requeridos
    const validacion = validarCamposRequeridos(data);
    if (!validacion.valido) {
        mostrarNotificacion(`❌ Campos requeridos faltantes: ${validacion.camposFaltantes.join(', ')}`, 'error');
        return;
    }
    
    if (navigator.onLine) {
        // Envío online
        try {
            const response = await fetch('/guardar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                mostrarNotificacion('✅ Formulario enviado correctamente', 'success');
                form.reset();
            } else {
                mostrarNotificacion(`❌ Error: ${result.error}`, 'error');
            }
        } catch (error) {
            console.error('Error enviando formulario:', error);
            mostrarNotificacion('❌ Error de conexión. Guardando localmente...', 'warning');
            guardarBorrador();
        }
    } else {
        // Guardado offline
        guardarBorrador();
    }
}

// Registrar el service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('✅ ServiceWorker registrado correctamente');
            })
            .catch(error => {
                console.error('❌ Error al registrar ServiceWorker:', error);
            });
    });
}

// Event listeners
window.addEventListener('online', () => {
    updateOnlineStatus();
    mostrarNotificacion('🟢 Conexión restaurada', 'success');
});

window.addEventListener('offline', () => {
    updateOnlineStatus();
    mostrarNotificacion('🔴 Sin conexión - Modo offline activado', 'warning');
});

window.addEventListener('load', () => {
    updateOnlineStatus();
    updatePendingCounter();
    
    // Configurar el formulario para manejo offline
    const form = document.getElementById('infraForm');
    if (form) {
        form.addEventListener('submit', manejarEnvioFormulario);
    }
});

// Funciones globales para los botones
window.guardarBorrador = guardarBorrador;
window.syncPendingForms = syncPendingForms;
window.mostrarBorradores = mostrarBorradores;
window.cargarBorrador = cargarBorrador;
window.eliminarBorrador = eliminarBorrador;