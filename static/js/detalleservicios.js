document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.menu-item');
    const imagesContainer = document.getElementById('images');
    const modal = document.getElementById('modal');
    const closeModalButton = document.getElementById('closeModal');
    const mobileMenu = document.getElementById('mobile-menu');
    const modalTitle = document.getElementById('modalTitle');
    const modalContent = document.getElementById('modalContent');

    if (!imagesContainer) {
        console.error("❌ No se encontró el elemento con id 'images'. Asegúrate de que esté presente en el HTML.");
        return;
    }

    const images = [
        [
            "/static/img/detalleservicios/controlcalidad/CC-1.jpeg",
            "/static/img/detalleservicios/controlcalidad/CC-4.jpeg",
            "/static/img/detalleservicios/controlcalidad/CC-5.jpg",
            "/static/img/detalleservicios/controlcalidad/CC-6.jpg",
            "/static/img/detalleservicios/controlcalidad/CC-7.jpg",
            "/static/img/detalleservicios/controlcalidad/CC-8.jpg",
            "/static/img/detalleservicios/controlcalidad/CC-9.jpg",
            "/static/img/detalleservicios/controlcalidad/CC-10.jpg",
            "/static/img/detalleservicios/controlcalidad/CC-11.jpg",
            "/static/img/detalleservicios/controlcalidad/CC-12.jpeg",
            "/static/img/detalleservicios/controlcalidad/CC-13.jpeg",
            "/static/img/detalleservicios/controlcalidad/CC-14.jpeg",
            "/static/img/detalleservicios/controlcalidad/CC-15.jpeg",
            "/static/img/detalleservicios/controlcalidad/CC-16.jpeg",
            "/static/img/detalleservicios/controlcalidad/CC-2.jpeg",
            "/static/img/detalleservicios/controlcalidad/CC-3.jpeg"
        ],
        [
            "/static/img/detailservices/ems/EMS-2.jpg",
            "/static/img/detailservices/ems/EMS-1.jpg",
            "/static/img/detailservices/ems/EMS-3.jpg",
            "/static/img/detailservices/ems/EMS-4.jpg",
            "/static/img/detailservices/ems/EMS-5.jpg",
            "/static/img/detailservices/ems/EMS-6.jpg",
            "/static/img/detailservices/ems/EMS-7.jpg",
            "/static/img/detailservices/ems/EMS-8.jpg",
            "/static/img/detailservices/ems/EMS-9.jpg",
            "/static/img/detailservices/ems/EMS-10.jpg",
            "/static/img/detailservices/ems/EMS-11.jpg"
        ],
        [
            "/static/img/detailservices/canteras/CC-1.jpg",
            "/static/img/detailservices/canteras/CC-2.jpg",
            "/static/img/detailservices/canteras/CC-3.jpg",
            "/static/img/detailservices/canteras/CC-4.jpg",
            "/static/img/detailservices/canteras/CC-5.jpg",
            "/static/img/detailservices/canteras/CC-6.jpg"
        ],
        [
            "/static/img/detailservices/estructuras/ES-1.jpeg",
            "/static/img/detailservices/estructuras/ES-2.jpg",
            "/static/img/detailservices/estructuras/ES-3.jpeg",
            "/static/img/detailservices/estructuras/ES-4.jpg"
        ],
        [
            "/static/img/detailservices/mezclas/DM-1.jpg",
            "/static/img/detailservices/mezclas/DM-2.jpg",
            "/static/img/detailservices/mezclas/DM-3.jpg",
            "/static/img/detailservices/mezclas/DM-4.jpg",
            "/static/img/detailservices/mezclas/DM-5.jpg"
        ],
        [
            "/static/img/detailservices/laboratorio/LB-1.jpg",
            "/static/img/detailservices/laboratorio/LB-3.jpg",
            "/static/img/detailservices/laboratorio/LB-4.jpg",
            "/static/img/detailservices/laboratorio/LB-5.jpg",
            "/static/img/detailservices/laboratorio/LB-6.jpg",
            "/static/img/detailservices/laboratorio/LB-7.jpg",
            "/static/img/detailservices/laboratorio/LB-8.jpg",
            "/static/img/detailservices/laboratorio/LB-9.jpg",
            "/static/img/detailservices/laboratorio/LB-10.jpg",
            "/static/img/detailservices/laboratorio/LB-11.jpg",
            "/static/img/detailservices/laboratorio/LB-12.jpg",
            "/static/img/detailservices/laboratorio/LB-14.jpeg",
            "/static/img/detailservices/laboratorio/LB-15.jpeg",
            "/static/img/detailservices/laboratorio/LB-16.jpeg",
            "/static/img/detailservices/laboratorio/LB-17.jpeg",
            "/static/img/detailservices/laboratorio/LB-18.jpeg",
            "/static/img/detailservices/laboratorio/LB-19.jpeg"
        ],
        [
            "/static/img/detailservices/quimicos/QM-1.jpg",
            "/static/img/detailservices/quimicos/QM-2.jpg",
            "/static/img/detailservices/quimicos/QM-3.jpg",
            "/static/img/detailservices/quimicos/QM-4.jpg",
            "/static/img/detailservices/quimicos/QM-5.jpg",
            "/static/img/detailservices/quimicos/QM-6.jpg",
            "/static/img/detailservices/quimicos/QM-7.jpg",
            "/static/img/detailservices/quimicos/QM-8.jpg",
            "/static/img/detailservices/quimicos/QM-9.jpg",
            "/static/img/detailservices/quimicos/QM-10.jpg",
            "/static/img/detailservices/quimicos/QM-11.jpg",
            "/static/img/detailservices/quimicos/QM-12.jpg",
            "/static/img/detailservices/quimicos/QM-13.jpg"
        ],
        [
            "/static/img/detailservices/equipos/EQ-1.jpg",
            "/static/img/detailservices/equipos/EQ-2.jpg",
            "/static/img/detailservices/equipos/EQ-3.jpg",
            "/static/img/detailservices/equipos/EQ-4.jpg",
            "/static/img/detailservices/equipos/EQ-5.jpg"
        ]
    ];

    let currentIndex = 0;
    let currentImages = images[0];

    function updateCarousel(index) {
        currentImages = images[index];
        currentIndex = 0;
        imagesContainer.innerHTML = currentImages.map((src, i) => {
            return `<img src="${src}" alt="Imagen ${i + 1}" class="carousel-image w-full h-full object-cover ${i === 0 ? '' : 'hidden'}">`;
        }).join('');
        highlightMenuItem(index);
    }

    function changeImage(direction) {
        currentIndex += direction;
        if (currentIndex < 0) currentIndex = currentImages.length - 1;
        if (currentIndex >= currentImages.length) currentIndex = 0;

        const imgs = document.querySelectorAll('.carousel-image');
        imgs.forEach((img, i) => {
            img.classList.toggle('hidden', i !== currentIndex);
        });
    }

    function highlightMenuItem(index) {
        menuItems.forEach((item, i) => {
            item.classList.toggle('bg-blue-300', i === index);
            item.classList.toggle('text-white', i === index);
        });
    }

    function openModal() {
        modal.classList.remove('hidden');
    }

    function closeModal() {
        modal.classList.add('hidden');
    }

    // Listeners para menú principal
    menuItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            updateCarousel(index);
            openModal();
        });
    });

    // Listener para el menú móvil
    if (mobileMenu) {
        mobileMenu.addEventListener('change', function () {
            const selectedIndex = parseInt(this.value);
            if (!isNaN(selectedIndex)) {
                updateCarousel(selectedIndex);
                openModal();
            }
        });
    }

    // Botones de navegación
    const prev = document.getElementById('prev');
    const next = document.getElementById('next');
    if (prev) prev.addEventListener('click', () => changeImage(-1));
    if (next) next.addEventListener('click', () => changeImage(1));

    // Cerrar modal
    if (closeModalButton) {
        closeModalButton.addEventListener('click', closeModal);
    }

    // Inicializar carrusel
    updateCarousel(0);

    // Tooltips
    const tooltips = document.querySelectorAll('.tooltip');
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function () {
            tooltips.forEach(t => t.classList.add('hidden'));
            const modalId = this.getAttribute('data-modal');
            const tooltip = document.getElementById(modalId);
            if (tooltip) tooltip.classList.remove('hidden');
        });
    });

    document.querySelectorAll('.close-tooltip').forEach(button => {
        button.addEventListener('click', function () {
            this.closest('.tooltip').classList.add('hidden');
        });
    });
});
