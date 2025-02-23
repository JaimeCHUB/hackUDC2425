// Variables globales para la búsqueda
const searchInput = document.querySelector(".search-input") // Definimos referencia al entry
let actualBrand = "zara" // Por defecto entendemos que es zara
// ------

function insertarProductos(data, append = false) {
    const container = document.getElementById("container-prod") // Donde vamos a agregar html inyectado
    if (!append) { // Si es true, nos interesa añadir, por lo que saltamos está línea
        container.innerHTML = ""
    }

    if (Array.isArray(data) && data.length > 0) { // Nos aseguramos de haber recibido algún dato de la consulta
        data.forEach((product) => {
            const fila = document.createElement("div") // Añadimos un div para inyectar datos
            fila.classList.add("producto-item")

            const enlace = document.createElement("a") // Referencia
            enlace.href = product.link
            enlace.target = "_blank"

            const imagen = document.createElement("img") // Imagen
            imagen.src = product.image
            imagen.alt = product.name

            enlace.appendChild(imagen) // Conectamos el enlace a la imágen
            fila.appendChild(enlace) // Conectamos la imágen a la fila

            if (product.price.original == null) { // Si no tiene rebaja
                fila.innerHTML += `
                <h3>${product.name}</h3>
                <p>Precio: ${product.price.value.current} ${product.price.currency}</p>
                <p>Marca: ${product.brand}</p>
                `
            } else { // Si está de rebaja
                fila.innerHTML += `
                <h3>${product.name}</h3>
                <p>Precio: ${product.price.value.original} ${product.price.currency} - ${product.price.value.current} ${product.price.currency}</p>
                <p>Marca: ${product.brand}</p>
                `
            }

            container.appendChild(fila) // Metemos la fila al container final
        })
    } else if (!append) { // En caso de que no hayamos scrolleado todos los productos y no encontrará ninguno, aparecerá este mensaje
        container.innerHTML = '<div class="noti-class"><p>No se encontraron productos.</p></div>';
    }
}

async function funcionBuscar(resetPage = false) {
    if (resetPage) { // Volver a la página 1 de productos encontrados
        currentPage = 1
        hasMoreProducts = true // Asumimos que tiene más por defecto
    }

    if (searchInput.value.trim() === "") { // Quitamos los espacios/tabuladores y miramos si está vacío
        console.log("El campo de búsqueda está vacío.") // Si lo está notificamos y no hacemos nada
        return
    }

    if (!hasMoreProducts || isLoading) { // Si ya está cargando productos o no tiene más, no podemos mostrar más productos
        return
    }

    isLoading = true // Marcamos que está cargando productos
    try {
        const jsonResp = await buscarProd(searchInput.value.trim(), actualBrand, currentPage) // Espera a la respuesta del REST
        insertarProductos(jsonResp, currentPage > 1)
        currentPage++ // Avanzamos de página
        hasMoreProducts = jsonResp.length > 0 // Mientras haya productos, asumimos que puede haber más
    } catch (error) {
        console.error("Error al buscar productos:", error)
    } finally {
        isLoading = false
    }
}

//AUXILIARES
function highlight(element, brand) {
    var items = document.querySelectorAll(".marcas li")
    items.forEach((item) => {
        item.classList.remove("active")
    })
    element.classList.add("active")
    actualBrand = brand

    funcionBuscar(true)
}

// VARIABLES GLOBALES
let currentPage = 1
let isLoading = false
let hasMoreProducts = true

// FUNCIÓN DE ANIMACIÓN INICIAL
window.onload = () => {
    const logoContainer = document.getElementById("logo-container")
    const mainContent = document.getElementById("main-content")

    setTimeout(() => {
        logoContainer.style.transition = "opacity 1s"
        logoContainer.style.opacity = "0"
        setTimeout(() => {
            logoContainer.style.display = "none"
            mainContent.style.display = "block"
        }, 1000)
    }, 1000)

    // Agregar el evento de scroll
    window.addEventListener("scroll", handleScroll)
}

function handleScroll() {
    if (
        window.innerHeight + window.scrollY >= document.body.offsetHeight - 200 &&
        !isLoading &&
        hasMoreProducts &&
        searchInput.value.trim() !== ""
    ) {
        funcionBuscar()
    }
}

// FUNCIONALIDADES BÁSICAS
searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault()
        funcionBuscar(true) // Al presionar enter resetea los productos cargados y busca lo que haya en el entry
    }
})

async function buscarProd(query, brand, page = 1, perPage = 4) { // Implementa el acceso a datos
    const params = new URLSearchParams({ query, brand, page, perPage })

    const url = `http://127.0.0.1:8000/products/text?${params.toString()}`// SE PARTE DE QUE EL REST ESTÁ ENCENDIDO
    //console.log("Buscar produto: ", url)
    try {
        const response = await fetch(url)
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`)
        }
        return await response.json() // Cuando tenga la respuesta, la devuelve
    } catch (error) {
        console.error("Error al buscar productos:", error)
        throw error
    }
}