import base64
import requests

from beaware_api_requests import login

class APIClient:
    """Crea el cliente que se encargará de comunicarse con la api de BeAware"""
    def __init__(self, company, user, token, base_url="https://api.beaware360.com/ba360/apir/v10_5"):
        """
        Constructor del cliente que se comunicará con la API
        :param company: Nombre de la compañia para ingresar a BeAware (ej: mcdonalds)
        :param user: Credencial de usuario para iniciar sesión
        :param token: Token obtenido al iniciar sesón
        :param base_url: Url base a la que se realizarán las solicitudes
        """
        self.company = company
        self.user = user
        self.token = token
        self.base_url = base_url
        self.legacy_base_url = "https://api.beaware360.com/ba360"  # URL de la API antigua (Se utiliza para subir archivos)

    def make_request(self, endpoint, method="GET", data=None, files=None, use_legacy=False):
        """
        Realiza una solicitud a la API de BeAware
        :param endpoint: Ruta del endpoint (ej: "/uploadfile").
        :param method: Método HTTP (GET, POST, etc.).
        :param data: Datos a enviar (en JSON o form-data).
        :param files: Archivos a enviar, si los hay.
        :param use_legacy: Si es True, se usa la URL de la API antigua.
        :return: Respuesta JSON o None en caso de error.
        """
        url = f"{self.legacy_base_url}{endpoint}" if use_legacy else f"{self.base_url}{endpoint}"
        
        # Intentaremos la solicitud hasta 2 veces: la original y una reintento si se obtiene 401.
        for intento in range(2):
            headers = {
                "Authorization": f"Basic {self.get_auth_token()}",
                # Si se envían archivos, dejamos que requests configure el Content-Type.
                "Content-Type": "application/json" if not files else None,
            }
            
            try:
                if files:
                    response = requests.request(method, url, headers=headers, data=data, files=files)
                else:
                    response = requests.request(method, url, headers=headers, json=data)
                
                # Si obtenemos un error 401 y es el primer intento, actualizamos el token y reintentamos.
                if response.status_code == 401 and intento == 0:
                    print("Error 401: Token expirado, renovando token...")
                    self.token = login()  # Se asume que login() retorna un nuevo token
                    continue  # Reintenta la solicitud con el nuevo token
                            
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.RequestException as e:
                print(f"Error en la solicitud: {e}")
                return None

        # Si después de reintentar la solicitud sigue habiendo error, se retorna None.
        return None


    def get_auth_token(self):
        """Retorna y codifica el token de autenticación para realizar las solicitudes"""
        auth_string = f"{self.company}/{self.user}:{self.token}"
        return base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
