import requests
import beaware_secrets
import decode_images
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


def addFile(base64_file, id_caso, id_usuario) :
    """Agrega el archivo en base 64 'base64_file' al caso con id 'id_caso' a BeAware. 'id_usuario' corresponde al usuario que realizó el registr del archivo"""

    fileupload = {
        "COMPANYNAME": "aguaspacifico",
        "IDOBJETO": id_caso or 466,
        "TIPOOBJETO": "casos",
        "TAGS": "IMAGEN_BOLETA",
        "FILE": base64_file,
        "IDUSUARIO": id_usuario or 6
    }

    try:
        token = login()
        print(token)

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as error:
        print("Error en la solicitud:", error)



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