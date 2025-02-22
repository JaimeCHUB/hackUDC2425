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

async function buscarProd(query, brand, page = 1, perPage = 5) {
    const params = new URLSearchParams({ query, brand, page, perPage });

    const url = `http://127.0.0.1:8000/products/text?${params.toString()}`;
    console.log("Buscar produto: ", url);
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error al buscar productos:', error);
        throw error;
    }
}


// PARTE DE BÚSQUEDA
const searchInput = document.querySelector('.search-input');
let actualBrand = 'zara'

function insertarProductos(data) {
    const container = document.getElementById("container-prod");
    container.innerHTML = "";

    if (Array.isArray(data) && data.length > 0) {
        data.forEach(product => {
            const fila = document.createElement("div");
            fila.classList.add("producto-item");

            if (product.price.original == null) {
                fila.innerHTML = `
                <h3>${product.name}</h3>
                <p>Precio: ${product.price.value.current} ${product.price.currency}</p>
                <p>Marca: ${product.brand}</p>
                <a href="${product.link}" target="_blank">Ver Producto</a>
                `
            } else {
                fila.innerHTML = `
                <h3>${product.name}</h3>
                <p>Precio: ${product.price.value.original} ${product.price.currency} - ${product.price.value.current} ${product.price.currency}</p>
                <p>Marca: ${product.brand}</p>
                <a href="${product.link}" target="_blank">Ver Producto</a>
                `
            }

            container.appendChild(fila);
        });
    } else {
        container.innerHTML = "<p>No se encontraron productos.</p>";
    }
}

async function funcionBuscar() {
    if (searchInput.value.trim() === '') {
        console.log('El campo de búsqueda está vacío.');
    }
    try {
        let jsonResp = await buscarProd(searchInput.value.trim(), actualBrand);
        insertarProductos(jsonResp);
    } catch (error) {
        console.error('Error al buscar productos:', error);
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

