document.getElementById('infraForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    if (!navigator.onLine) {
        guardarBorrador();
        return;
    }
    
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
            alert('Datos guardados correctamente');
            e.target.reset();
        } else {
            alert('Error al guardar: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        guardarBorrador();
    }
});