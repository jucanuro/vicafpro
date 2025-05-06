(() => {
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        const mobileMenuLinks = mobileMenu.querySelectorAll('a');
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    }

    const tabInicio = document.getElementById('tab1');
    if (tabInicio) {
        tabInicio.classList.add('bg-blue-950', 'text-white');
    }

    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(item => {
                item.classList.remove('bg-blue-900', 'text-white');
                item.classList.add('text-gray-900');
            });

            tab.classList.add('bg-blue-900', 'text-white');
            tab.classList.remove('text-gray-900');
        });
    });
})();
