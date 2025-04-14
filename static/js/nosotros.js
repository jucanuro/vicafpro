const modalButtons = document.querySelectorAll('[data-modal]');
        
// Añadir evento de click a los botones para abrir los modales
modalButtons.forEach(button => {
    button.addEventListener('click', function () {
        const modalId = this.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
        }
    });
});

// Obtener todos los botones que cierran modales
const closeModalButtons = document.querySelectorAll('[data-modal-close]');

// Añadir evento de click a los botones para cerrar los modales
closeModalButtons.forEach(button => {
    button.addEventListener('click', function () {
        const modalId = this.getAttribute('data-modal-close');
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
        }
    });
});

// Cerrar el modal al hacer clic fuera del contenido
window.addEventListener('click', function (e) {
    if (e.target.classList.contains('bg-black')) {
        e.target.classList.add('hidden');
    }
});