// Manejo del almacenamiento offline
const STORE_KEY = 'infraestructura_forms';

// Función para guardar borrador
function guardarBorrador() {
    const formData = new FormData(document.getElementById('infraForm'));
    const data = Object.fromEntries(formData.entries());
    
    let stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    stored.push({
        ...data,
        timestamp: new Date().toISOString(),
        syncStatus: 'pending'
    });
    localStorage.setItem(STORE_KEY, JSON.stringify(stored));
    
    mostrarNotificacion('Formulario guardado localmente', 'warning');
    updatePendingCounter();
}

// Función para sincronizar formularios pendientes
async function syncPendingForms() {
    if (!navigator.onLine) return;
    
    const stored = JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
    const pending = stored.filter(item => item.syncStatus === 'pending');
    
    for (const form of pending) {
        try {
            const response = await fetch('/guardar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(form)
            });
            
            if (response.ok) {
                form.syncStatus = 'synced';
                mostrarNotificacion('Formulario sincronizado correctamente', 'success');
            }
        } catch (error) {
            console.error('Error syncing form:', error);
            mostrarNotificacion('Error al sincronizar', 'error');
        }
    }
    
    localStorage.setItem(STORE_KEY, JSON.stringify(stored));
    updatePendingCounter();
}

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${tipo} alert-dismissible fade show`;
    notification.innerHTML = `
        <strong>${mensaje}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').insertBefore(notification, document.querySelector('.form-header'));
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
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

// Inicializar los listeners y contadores
window.addEventListener('online', syncPendingForms);
window.addEventListener('load', () => {
    updateOnlineStatus();
    updatePendingCounter();
});