import requests
from requests.auth import HTTPBasicAuth

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

        # print(f"Respuesta: {response.json()}")

        if response.status_code==200:
            return (response.json())
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud:", e)