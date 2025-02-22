from fastapi import FastAPI
from enum import Enum

import requests
from requests.auth import HTTPBasicAuth

#from bs4 import BeautifulSoup

#from playwright.async_api import async_playwright #versión async porque usamos fastAPI

app = FastAPI()

class BrandName(str, Enum):
    zara = "zara"
    zara_home = "zara_home"
    stradivarius = "stradivarius"
    pull_and_bear = "pull_and_bear"
    oysho = "oysho"
    massimo_dutti = "massimo_dutti"
    lefties = "lefties"

def get_token():
    # URL de la API
    #url = "https://auth.inditex.com:443/openam/oauth2/itxid/itxidmp/sandbox/access_token"
    url = "https://auth.inditex.com:443/openam/oauth2/itxid/itxidmp/access_token"

    # Credenciales de autenticación básica
    #username = "oauth-mkpsbox-oauthrpqkodgkfmpritxkffsnbxpro"
    username= "oauth-mkplace-oauthsmbhufobimglobpshkpropro"
    #password = "Ny8eKaz3L9@:sDzp"
    password = "-GY7Q[CA0yHYSZjC"

    # Datos del cuerpo de la solicitud
    data = {
        "grant_type": "client_credentials",
        "scope": "technology.catalog.read"
    }

    # Encabezados de la solicitud
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Realizar la solicitud POST
    try:
        response = requests.post(
        url,
        auth=HTTPBasicAuth(username, password),
        data=data,
        headers=headers
        )

        if response.status_code==200:
            return (response.json().get("id_token"))
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud:", e)

id_token = get_token()
#print(f"Token: {id_token}")

def get_image_url_static(url):

    image_endpoint="https://static.zara.net/assets/public/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar todas las etiquetas <img>
    imgs = soup.find_all("img")

    # Extraer los enlaces de las imágenes (atributo src)
    image_urls = [img["src"] for img in imgs if "src" in img.attrs]

    print(image_urls)

    return image_urls

async def get_image_url(url):

    async with async_playwright() as p:
        # Iniciar el navegador
        #Headless = True para que sea invisible
        browser = await p.chromium.launch(
            headless=False,  # Ejecutar en modo headless
            args=[
                "--disable-blink-features=AutomationControlled",  # Deshabilitar la detección de automatización
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-breakpad",
                "--disable-client-side-phishing-detection",
                "--disable-component-update",
                "--disable-default-apps",
                "--disable-domain-reliability",
                "--disable-extensions",
                "--disable-features=AudioServiceOutOfProcess",
                "--disable-hang-monitor",
                "--disable-ipc-flooding-protection",
                "--disable-popup-blocking",
                "--disable-prompt-on-repost",
                "--disable-renderer-backgrounding",
                "--disable-sync",
                "--force-color-profile=srgb",
                "--metrics-recording-only",
                "--no-first-run",
                "--safebrowsing-disable-auto-update",
                "--enable-automation",  # Habilitar la automatización (paradójicamente, esto puede ayudar a evitar detecciones)
                "--password-store=basic",
                "--use-mock-keychain",
            ],
        )
        #browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )
        page = await context.new_page()

        #page = await browser.new_page()
        #await page.set_extra_http_headers(headers)

        # Abrir la página
        await page.goto(url)

        # Esperar a que la página cargue completamente (opcional)
        #await page.wait_for_timeout(5000)  # Espera a que se carguen las imágenes

        await page.wait_for_selector("img", state="attached")  # Espera a que al menos una imagen esté en el DOM
        
        #print(await page.content())

        # Encontrar todas las etiquetas <img>
        #imgs = await page.query_selector_all("img")

        # Extraer los enlaces de las imágenes (atributo src)
        #image_urls = [await img.get_attribute("src") for img in imgs]
        #print(image_urls)

        # Cerrar el navegador
        #await browser.close()

        #return image_urls

        #await page.wait_for_selector("img", state="attached")
        img = await page.query_selector("img")
        image_url = await img.get_attribute("src")
        await browser.close()
        print(url)
        print(image_url)
        return image_url





def get_products(query:str, brand:str, page:int, perPage:int):
    # URL de la API
    #url = "https://api-sandbox.inditex.com/searchpmpa-sandbox"
    url = "https://api.inditex.com/searchpmpa"
    endpoint= "/products"

    # Encabezados de la solicitud
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    params = {
        "query": query,  # Ejemplo de búsqueda
        "brand": brand,  # Ejemplo de marca
    }
    if page != None:
        params["page"] = page
    if perPage != None:
        params["perPage"] = perPage

    # Realizar la solicitud POST
    try:
        response = requests.get(
            f"{url}{endpoint}",
            headers=headers,
            params=params
        )

        print(f"Respuesta: {response.json()}")

        if response.status_code==200:
            return (response.json())
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud:", e)

def get_products_by_image(image: str, page: int, perPage:int):
    url = "https://api.inditex.com/pubvsearch"
    endpoint= "/products"

    # Encabezados de la solicitud
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    params = {
        "image": image
    }
    if page != None:
        params["page"] = page
    if perPage != None:
        params["perPage"] = perPage

    # Realizar la solicitud POST
    try:
        response = requests.get(
            f"{url}{endpoint}",
            headers=headers,
            params=params
        )

        print(f"Respuesta: {response.json()}")

        if response.status_code==200:
            return (response.json())
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud:", e)


#Interfaz de la API

@app.get("/products/text")
async def get_items(query: str, brand: BrandName | None = None, page: int | None = None, perPage: int | None = None):
    products = get_products(query, None if brand == None else brand.value, page, perPage)
    #for product in products:
        #await get_image_url(product.get("link"))
    return products

@app.get("/products/image")
async def get_items_by_image(image: str, page: int | None = None, perPage:int | None = None):
    products = get_products_by_image(image, page, perPage)
    return products