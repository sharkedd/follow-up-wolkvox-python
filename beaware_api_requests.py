import requests
import beaware_secrets
import base64

def login():
    """Ingresa las credenciales en BeAware, retornando el respectivo token para las solicitudes a la API"""
    try:
        URL_LOGIN = "https://api.beaware360.com/ba360/apir/v10_5/login/auth"
        payload = {
            "company": beaware_secrets.COMPANY,
            "user": beaware_secrets.USER,
            "pass": beaware_secrets.PASSWORD
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(URL_LOGIN, json=payload, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es 200 OK

        data = response.json()
        token = data.get("token")
        return token

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as error:
        print("Error en la solicitud:", error)

def addFile(client, base64_file, file_format, id_caso, id_usuario):
    """
    Agrega un archivo (obtenido en base64) al caso especificado en BeAware.
    
    :param client: Instancia de APIClient previamente inicializada.
    :param base64_file: Cadena en base64 del archivo.
    :param file_format: Formato del archivo (por ejemplo, "png" o "jpg").
    :param id_caso: ID del caso al que se asociará el archivo.
    :param id_usuario: ID del usuario que realiza el registro.
    :return: Respuesta JSON de la API o None en caso de error.
    """
    # Define el endpoint para la carga de archivos
    endpoint = "/uploadfile"
    
    # Decodifica la cadena base64 para obtener los datos binarios
    file_data = base64.b64decode(base64_file)

    # Prepara el payload con los datos requeridos por la API
    payload = {
        "COMPANYNAME": client.company,  
        "IDOBJETO": id_caso,  
        "TIPOOBJETO": "casos",
        "TAGS": "IMAGEN_BOLETA",
        "IDUSUARIO": id_usuario,
    }

    # Construye el diccionario para enviar el archivo.
    # Se genera un nombre dinámico, y se especifica el tipo MIME.
    files = {
        "FILE": (f"archivo.{file_format}", file_data,
                 f"image/{file_format}" if file_format in ["jpg", "png"] else "application/octet-stream")
    }
    
    try:
        # Realiza la solicitud POST utilizando el cliente API.
        # Se utiliza 'use_legacy=True' para usar la URL base antigua, según la configuración del cliente.
        response = client.make_request(endpoint, method="POST", data=payload, files=files, use_legacy=True)
        print("Archivo agregado exitosamente:", response)
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as error:
        print("Error en la solicitud:", error)
    return None

""" 
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción si el código de estado es 4xx o 5xx
            data = response.json()  # Parsea la respuesta JSON
            print("Datos recibidos:", data)

        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Error de conexión. Verifica tu conexión a internet.")
        except requests.exceptions.Timeout:
            print("Tiempo de espera agotado. Inténtalo de nuevo más tarde.")
        except requests.exceptions.RequestException as err:
            print(f"Error en la solicitud: {err}")
        except ValueError:
            print("Error al procesar la respuesta JSON.")

 """