import json
import os
import decode_images
import requests


def almacenarEnArchivo(lista_elementos, archivo):
    """Guarda una lista de elementos en un archivo JSON, sobrescribiendo su contenido."""
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(lista_elementos, f, ensure_ascii=False, indent=4)

def almacenarContactos(lista_contactos, archivo="contactos.json"):
    almacenarEnArchivo(lista_contactos, archivo)

def almacenarCasos(lista_casos, archivo="casos.json"):
    almacenarEnArchivo(lista_casos, archivo)

def almacenarMensajes(lista_mensajes, archivo="mensajes.json"):
    almacenarEnArchivo(lista_mensajes, archivo)

def addFile(file_string) :
    format, base64_data = decode_images.extract_base64_image(file_string)

    if not base64_data:
        print("No se encontró una imagen válida en el texto.")
        return
    else:
        fileupload = {
        "COMPANYNAME": "aguaspacifico",
        "IDOBJETO": 466,
        "TIPOOBJETO": "casos",
        "TAGS": "IMAGEN_BOLETA",
        "FILE": base64_data,
        "IDUSUARIO": 6
    }
        
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

