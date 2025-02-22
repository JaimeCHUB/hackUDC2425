window.onload = function() {
    const logoContainer = document.getElementById('logo-container');
    const mainContent = document.getElementById('main-content');

    setTimeout(() => {
        logoContainer.style.transition = 'opacity 1s';
        logoContainer.style.opacity = '0';
        setTimeout(() => {
            logoContainer.style.display = 'none';
            mainContent.style.display = 'block';
        }, 1000);
    }, 1000);
};

function actualizarImagen(nuevaURL) {
    const imagen = document.getElementById("imagenDinamica");

    imagen.onerror = function () {
        imagen.src = "nophoto.png";
    };

    imagen.src = nuevaURL || "nophoto.png";
}


async function buscarProd(query, marca = null) {
    const page = 1;
    const perPage = 10;

    const params = new URLSearchParams({ query, page, perPage });
    if (marca) {
        params.append('marca', marca);
    }

    const url = `http://localhost:8000/products?${params.toString()}`;

    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
    }
    return response.json();
}

// PARTE DE BÚSQUEDA
const searchInput = document.querySelector('.search-input');
let actualBrand = 'Todos'

function funcionBuscar() {
    if (searchInput.value.trim() === '') {
        console.log('El campo de búsqueda está vacío.');
    } else {
        //FUNCIONALIDAD BÚSQUEDA POR TEXTO
        console.log("ENVIAR")
    }
}

searchInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Para evitar que haga comportamientos no esperados
        funcionBuscar();
    }
});

function highlight(element, brand) { // INTEGRAR, NO ES NUEVA
    var items = document.querySelectorAll('.marcas li');
    items.forEach(function(item) {
        item.classList.remove('active');
    });
    element.classList.add('active');
    actualBrand = brand;

    funcionBuscar()
}

