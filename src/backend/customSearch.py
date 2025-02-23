import requests
import configparser

config = configparser.ConfigParser()

# Leer el archivo INI
config.read("config.ini")

def _get_mock_image():
    sample_image = config["google"]["sample_image"]
    return sample_image

def get_google_image(query:str, mock:bool | None = None):
    if mock == None:
        mock = config["google"]["mock"]
    if mock == "True": return _get_mock_image()

    api_key = config["google"]["api_key"]
    cx = config["google"]["cx"]
    num = 1
    url = config["google"]["api_url"]

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