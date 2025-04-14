document.getElementById("closeModalHome").addEventListener("click", function() {
    document.getElementById("myModalHome").style.display = "none";
});

// Función para cambiar de imagen automáticamente
let currentIndex = 0;
const carouselItems = document.querySelectorAll(".carousel-item");
const totalItems = carouselItems.length;

function changeImage() {
    // Eliminar clase 'active' de la imagen actual y ocultarla
    carouselItems[currentIndex].classList.remove("active");
    carouselItems[currentIndex].classList.add("hidden");

    // Actualizar el índice
    currentIndex = (currentIndex + 1) % totalItems;

    // Mostrar la siguiente imagen y agregar clase 'active'
    carouselItems[currentIndex].classList.remove("hidden");
    carouselItems[currentIndex].classList.add("active");
}

// Cambiar imagen cada 5 segundos (5000 ms)
setInterval(changeImage, 5000);