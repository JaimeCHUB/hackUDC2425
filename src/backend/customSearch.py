import requests

def _get_mock_image():
    sample_image = "https://static.zara.net/assets/public/dd96/b577/6c8441ebb864/ad6d53e57aee/08372261507-015-a1/08372261507-015-a1.jpg?ts=1736513008633&w=835"
    return sample_image

def get_google_image(query:str, mock:bool = True):
    if mock: return _get_mock_image()

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