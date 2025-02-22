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

function highlight(element) {
    var items = document.querySelectorAll('.marcas li');
    items.forEach(function(item) {
        item.classList.remove('active');
    });
    element.classList.add('active');
}

const IP = "http://localhost:9090";
class ModelException extends Error {
    constructor(msg) {
        super(msg);
        this.name = this.constructor.name;
    }
}

async function getInfo() {
    try {
        const queryURL = `${IP}/a`;
        const responseURL = await fetch(queryURL);
        if (!responseURL.ok) {
            throw new ModelException(responseURL);
        }

        let response = await responseURL.json();
    } catch (error) {
        console.error("Error al obtener la respuesta: ", error);
        return null;
    }
}

async function fetchImageUrls() {
    const paginaURL = "https://www.zara.com/es/es/vestido-midi-jacquard-p02463533.html?v1=427807085";

    try {
        const response = await fetch(paginaURL, { mode: 'no-cors' });
        const html = await response.text();

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        const imgTags = doc.querySelectorAll('img');
        const imageUrls = Array.from(imgTags).map(img => img.src);

        return imageUrls;
    } catch (error) {
        console.error('Error fetching the image URLs:', error);
        return [];
    }
}

function actualizarImagen(nuevaURL) {
    const imagen = document.getElementById("imagenDinamica");

    imagen.onerror = function () {
        imagen.src = "nophoto.png";
    };

    imagen.src = nuevaURL || "nophoto.png";
}

const botonFuncion = document.getElementById("miBoton");

botonFuncion.addEventListener("click", async () => {
    const imageUrls = await fetchImageUrls();
    if (imageUrls.length > 0) {
        actualizarImagen(imageUrls[0]); // Usar la primera URL de imagen encontrada
        console.log("EXITO");
    } else {
        actualizarImagen(); // Usar la imagen de respaldo
        console.log("FALLO");
    }
});


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