

    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    menuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });

    // Seleccionar todos los enlaces del menú móvil
    const mobileMenuLinks = mobileMenu.querySelectorAll('a');

    // Añadir evento click a cada enlace para ocultar el menú móvil
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    });
   // Seleccionar el enlace "Inicio" por defecto
   // Seleccionar el enlace "Inicio" por defecto
    document.getElementById('tab1').classList.add('bg-blue-950', 'text-white');

    // Obtener todos los enlaces de navegación
    const tabs = document.querySelectorAll('.tab');

    // Agregar el evento click a cada enlace
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Eliminar la clase activa y agregar la clase inactiva a todos los enlaces
            tabs.forEach(item => {
                item.classList.remove('bg-blue-900', 'text-white');
                item.classList.add('text-gray-900');
            });
            
            // Añadir la clase activa y quitar la clase inactiva al enlace clickeado
            tab.classList.add('bg-blue-900', 'text-white');
            tab.classList.remove('text-gray-900');
        });
    });
