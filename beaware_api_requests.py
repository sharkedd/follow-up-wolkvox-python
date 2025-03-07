from urllib import response
import requests
import beaware_secrets
import base64
import json

import validaciones

def login():
    """Ingresa las credenciales en BeAware, retornando el respectivo token de usuario"""
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

        data = response.json()
        token = data.get("token")
        return token

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as error:
        print("Error en la solicitud:", error)

def addFile(client, base64_file, file_format, asunto_mensaje, id_caso, id_usuario):
    """
    Agrega un archivo (obtenido en base64) al caso especificado en BeAware.
    
    :param client: Instancia de APIClient previamente inicializada.
    :param base64_file: Cadena en base64 del archivo.
    :param file_format: Formato del archivo (por ejemplo, "png" o "jpg").
    :param asunto_mensaje: Asunto del mensaje, servirá como titulo para el archivo
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
        "TAGS": asunto_mensaje,
        "IDUSUARIO": id_usuario,
    }

    # Construye el diccionario para enviar el archivo.
    # Se genera un nombre dinámico, y se especifica el tipo .
    files = {
        "FILE": (f"archivo.{file_format}", file_data,
                 f"image/{file_format}" if file_format in ["jpg", "png"] else "application/octet-stream")
    }
    
    try:
        # Realiza la solicitud POST utilizando el cliente API
        # Se utiliza 'use_legacy=True' para usar la URL base antigua (Sólo esta puede subir archivos)
        response = client.make_request(endpoint, method="POST", data=payload, files=files, use_legacy=True)
        print("Archivo agregado exitosamente:", response)
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as error:
        print("Error en la solicitud:", error)
    return None

def obtainContacts(client):
    endpoint = "/contacto/get/?pagina=1&cantidad=15000"
    contacts_array = []
    try:
        # Realiza la solicitud GET utilizando el cliente API
        # Como la Request utiliza la API nueva, y no necesita datos, sólo se inserta el endpoint en conjunto de su método
        response = client.make_request(endpoint, method="GET")
        contacts = response['data']

        for contact in contacts:
            contact_iden = contact.get('identificador', None)
            telefono = validaciones.formatear_telefono(contact_iden)
            if not telefono:
                #En caso de que el teléfono no sea válido, no se insertará en la lista de los contactos existentes
                #Esto es debido a que se tomo la decisión, de que los contactos de form y de wsp, sean diferentes.
                #En caso de que se quiera modificar esto, existe una función que obtiene el identificador, en conjunto del teléfono, retornando el que corresponda al número
                #Porque en wsp, el teléfono esta en identificador, en formweb, está en el campo telefono
                continue
            contact = {
                "id": contact.get('id'),
                "identificador": telefono,
                "nombre": contact.get('nombre'),
                "apellido": contact.get('apellido')
            }
            contacts_array.append(contact)

        return contacts_array
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as error:
        print("Error en la solicitud:", error)
    return None

def createContact(client, contact):
    """
    Crea un contacto en BeAware con el objeto entregado

    :param client: Cliente API que realizará la solicitud
    :param contact: Objeto que contiene los parámetros del cliente
    """
    endpoint = "/contacto/add"

    try:
        response = client.make_request(endpoint, method="POST", data=contact)
        contact = response['data']
        print(f"Contacto creado en BeAware para {contact['nombre']} {contact['apellido']}")
        return contact

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al crear contacto: {http_err}")
    except Exception as error:
        print("Error en la solicitud al crear contacto:", error)
    return None

def createCase(client, case):
    """
    Crea un caso en BeAware con el objeto entregado

    :param client: Cliente API que realizará la solicitud
    :param case: Objeto que contiene los parámetros del caso
    """
    endpoint = "/caso/add"

    try:
        response = client.make_request(endpoint, method="POST", data=case)
        caso = response['data']
        print(f"Caso creado en BeAware")
        return caso

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al crear contacto: {http_err}")
    except Exception as error:
        print("Error en la solicitud al crear contacto:", error)
    return None

def obtainProducts(client):
    endpoint = "/producto/get"

    try:
        response = client.make_request(endpoint)
        products = response['data']
        return [{"id": item["id"], "nombre": item["nombre"]} for item in products]
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP obtener los tipos: {http_err}")
    except Exception as error:
        print("Error en la solicitud al obtener los tipos:", error)
    return None

def obtainTypes(client):
    endpoint = "/tipo/get"

    try:
        response = client.make_request(endpoint)
        types = response['data']
        return [{"id": item["id"], "nombre": item["nombre"]} for item in types]
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP obtener los tipos: {http_err}")
    except Exception as error:
        print("Error en la solicitud al obtener los tipos:", error)
    return None

def addNotes(client, note):

    endpoint = "/actividad/add"

    try:
        response = client.make_request(endpoint, method="POST", data=note)
        beaware_note = response['data']
        print("Nota añadida con éxito")
        return beaware_note
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al asignar la nota: {http_err}")
    except Exception as error:
        print("Error en la solicitud al asignar las notas:", error)
    return None

def obtainCases(client):
    endpoint = "/caso/get/?filtro=history&pagina=1&cantidad=15000"

    try:
        response = client.make_request(endpoint)
        types = response['data']
        return [{"id": item["id"], "asunto": item["asunto"]} for item in types]
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP obtener los tipos: {http_err}")
    except Exception as error:
        print("Error en la solicitud al obtener los tipos:", error)
    return None