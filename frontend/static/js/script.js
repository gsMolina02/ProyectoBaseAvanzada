// Banco Pichincha - JavaScript

// Validación de formularios
document.addEventListener('DOMContentLoaded', function() {
    // Validar números de cédula
    const cedulaInputs = document.querySelectorAll('input[name="cedula"]');
    cedulaInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            this.value = this.value.replace(/\D/g, '').substring(0, 10);
        });
    });

    // Validar números de teléfono
    const telefonoInputs = document.querySelectorAll('input[name="telefono"]');
    telefonoInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            this.value = this.value.replace(/\D/g, '').substring(0, 10);
        });
    });

    // Auto-cerrar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.style.display = 'none', 300);
        }, 5000);
    });

    // Formatear números de cuenta
    const cuentaInputs = document.querySelectorAll('input[name="cuenta_destino"]');
    cuentaInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            this.value = this.value.replace(/\D/g, '');
        });
    });

    // Confirmar antes de realizar transferencia
    const transferForm = document.getElementById('transferForm');
    if (transferForm) {
        transferForm.addEventListener('submit', function(e) {
            const monto = document.getElementById('monto').value;
            const cuentaDestino = document.getElementById('cuenta_destino').value;
            
            if (!confirm(`¿Está seguro que desea transferir $${parseFloat(monto).toFixed(2)} a la cuenta ${cuentaDestino}?`)) {
                e.preventDefault();
            }
        });
    }
});

// Función para formatear montos
function formatearMonto(monto) {
    return new Intl.NumberFormat('es-EC', {
        style: 'currency',
        currency: 'USD'
    }).format(monto);
}

// Función para copiar número de referencia
function copiarReferencia(referencia) {
    navigator.clipboard.writeText(referencia).then(() => {
        alert('Referencia copiada al portapapeles');
    });
}

// Animaciones suaves al hacer scroll
document.addEventListener('scroll', function() {
    const elements = document.querySelectorAll('.feature-card, .account-card');
    elements.forEach(element => {
        const position = element.getBoundingClientRect();
        if (position.top < window.innerHeight && position.bottom >= 0) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
});

// Inicializar animaciones
window.addEventListener('load', function() {
    const cards = document.querySelectorAll('.feature-card, .account-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease';
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});
