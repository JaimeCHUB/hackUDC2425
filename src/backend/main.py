from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum

import requests
from requests.auth import HTTPBasicAuth

#from bs4 import BeautifulSoup

#from playwright.async_api import async_playwright #versión async porque usamos fastAPI

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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

def get_google_results(query:str):
    api_key = "AIzaSyCn897caMX-UEnDdDNFDSFvWLftlQmlZ8M"
    cx = "333e8cb4385db41c0"
    num = 1
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "q": query,          # Término de búsqueda
        "key": api_key,      # Tu clave de API
        "cx": cx,            # ID del motor de búsqueda
        "searchType": "image",  # Buscar solo imágenes
        "num": num           # Número de resultados a devolver
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        # Extraer las URLs de las imágenes
        image_urls = [item["link"] for item in results.get("items", [])]
        return image_urls[0]
    else:
        print("Error en la solicitud:", response.status_code)

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
    #for product in products:
    #    print(get_google_results(f"{products[0].get("name")} {products[0].get("brand")}"))

    return products

@app.get("/products/image")
async def get_items_by_image(image: str, page: int | None = None, perPage:int | None = None):
    products = get_products_by_image(image, page, perPage)
    return products