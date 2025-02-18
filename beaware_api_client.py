import base64
import requests

class APIClient:
    def __init__(self, company, user, token, base_url="https://api.beaware360.com/ba360/apir/v10_5"):
        self.company = company
        self.user = user
        self.token = token
        self.base_url = base_url
        self.legacy_base_url = "https://api.beaware360.com/ba360"  # URL de la API antigua

    def make_request(self, endpoint, method="GET", data=None, files=None, use_legacy=False):
        """
        Realiza una solicitud a la API de BeAware.
        
        :param endpoint: Ruta del endpoint (ej: "/uploadfile").
        :param method: Método HTTP (GET, POST, etc.).
        :param data: Datos a enviar (en JSON o form-data).
        :param files: Archivos a enviar, si los hay.
        :param use_legacy: Si es True, se usa la URL de la API antigua.
        :return: Respuesta JSON o None en caso de error.
        """
        url = f"{self.legacy_base_url}{endpoint}" if use_legacy else f"{self.base_url}{endpoint}"
        
        # Configura los encabezados.
        headers = {
            "Authorization": f"Basic {self.get_auth_token()}",
            # Si se envían archivos, no forzamos el Content-Type para que requests lo genere automáticamente.
            "Content-Type": "application/json" if not files else None,
        }
        
        try:
            if files:
                response = requests.request(method, url, headers=headers, data=data, files=files)
            else:
                response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None

    def get_auth_token(self):
        auth_string = f"{self.company}/{self.user}:{self.token}"
        return base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
