from fastapi import FastAPI
from enum import Enum

import requests
from requests.auth import HTTPBasicAuth

from bs4 import BeautifulSoup

from playwright.sync_api import sync_playwright

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

def get_image_url_bad(url):

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

    return image_urls

async def get_image_url(url):
    
    # URL de la página
    url = "https://zara.com/es/en/-P09479040.html?v1=441075492"

    async with sync_playwright() as p:
        # Iniciar el navegador
        browser = p.chromium.launch(headless=True)  # headless=True para modo sin cabeza
        page = browser.new_page()

        # Abrir la página
        page.goto(url)

        # Esperar a que la página cargue completamente (opcional)
        #page.wait_for_timeout(5000)  # Espera 5 segundos para que se carguen las imágenes

        page.wait_for_selector("img", state="attached")  # Espera a que al menos una imagen esté en el DOM

        # Encontrar todas las etiquetas <img>
        imgs = page.query_selector_all("img")

        # Extraer los enlaces de las imágenes (atributo src)
        image_urls = [await img.get_attribute("src") for img in imgs]
        print(image_urls)

        # Cerrar el navegador
        browser.close()

        return image_urls


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

@app.get("/products")
async def get_items(query: str, brand: BrandName | None = None, page: int | None = None, perPage: int | None = None):
    products = get_products(query, None if brand == None else brand.value, page, perPage)
    #for product in products:
        #await get_image_url(product.get("link"))
    return products