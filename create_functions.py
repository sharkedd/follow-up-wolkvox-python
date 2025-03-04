from http.client import CannotSendRequest
import json
import create_functions
import decode_images
import validaciones
import beaware_api_requests

def obtain_conversation_info_from_chat(conn_id, conversations_array):
    """
    Busca y retorna la información de la conversación del chat a través de la id de conexión.

    :param conn_id: Id en Wolkvox de la conversación a buscar 
    :param conversations_array: Array que contiene todas las conversaciones obtenidas
    """
    # Un chat tiene un array llamado conversaciones, que contiene todos los mensajes asociados a un chat.
    for conversation in conversations_array:
        if conversation.get("conn_id") == conn_id:
            return conversation.get("conversation")
    return None



def build_contact(client, chat, contact_list):
    """Construye y retorna el formato de contacto a partir del chat."""
    
    telefono = chat.get("customer_phone")
    if not telefono:
        print("Contacto no tiene teléfono")
        return None  # Validación temprana: Si no hay teléfono, no se puede crear un contacto.

    # Buscar si el contacto ya existe
    contacto = findContact(telefono, contact_list)
    if contacto:
        print("Contacto existente encontrado")
        return contacto  # Si el contacto ya existe, lo retornamos directamente.

    # Procesar el nombre y apellido
    customer_name = chat.get("customer_name", "")
    full_name = validaciones.procesar_nombre_apellido(customer_name)
    false_mail = [f"{full_name.get("name", "examplename")}.{full_name.get("last_name", "examplelastnanme")}.{telefono}@tarragona.example.com"]
    # Construir el nuevo contacto
    contacto = {
        "nombre": full_name.get("name", ""),
        "apellido": full_name.get("last_name", ""),
        "identificador": telefono,
        "email": false_mail,
        "timezone": "America/Santiago",
    }

    # Intentar crear el contacto en BeAware
    beaware_contact = beaware_api_requests.createContact(client, contacto)
    if not beaware_contact:
        return None  # Si la API falla, retornamos None.

    # Construcción del objeto final con el ID retornado por la API

    # Agregar a la lista de contactos
    contact_list.append(beaware_contact)
    print("Contacto agregado a contact_list")
    
    return beaware_contact


def findContact(identificador, contact_list):
    """
    Busca un contacto a través de su identificador en el array de contactos

    :param contact_identifier: Identificador del contacto, corresponde al teléfono
    :param contact_array: Array que contiene los contactos obtenidos de BeAware, junto a los creados en ejecución
    """
    return next((c for c in contact_list if c["identificador"] == identificador), None) 


def build_case(client, chat, case_list, contact_id, types):
    """Construye y retorna el diccionario del caso a partir del chat."""
    asunto = (
        f"{chat.get('date')}-{chat.get('cod_act')}/"
        f"{chat.get('description_cod_act')}-{chat.get('conn_id')}"
    )

    print(f"Asunto del caso a crear: {asunto}")
    id_producto = get_product_id_by_cod_act(chat.get("cod_act"), types)

    caso = {
        "idcontacto": contact_id,
        "idproducto": id_producto or 4, # MIENTRAS TANTO, SI NO SE ENCUENTRA EL PRODUCTO, SE PASARÁ COMO "Consulta"
        "idtipo": 1, # EN LO QUE LLEGA FELIPE PARA RESPONDER DUDAS, SE UTILIZARÁ TIPO 1
        "idsubtipo": 1, # LO MISMO CON SUBTIPO
        "asunto": asunto,
        "origen": chat.get("channel") or "whatsapp|",
    }

    beaware_case = beaware_api_requests.createCase(client, caso)
    if not beaware_case:
        return None  # Si la API falla, retornamos None.    
    
    case_list.append(beaware_case)
    print("Caso agregado a la lista case_list")
    return beaware_case

def get_product_id_by_cod_act(cod_act, types):
    return next((t["id"] for t in types if t["nombre"] == cod_act), None)

    

def process_messages(client, conversation_info, message_list, case_id):
    """
    Procesa cada mensaje de la conversación.
    
    - Si el mensaje es válido (texto), lo agrega a message_list.
    - Si no, asume que es un archivo, llamando a la función addFile para subirlo a BeAware
    """
    messages = [] 

    for mensaje in conversation_info:
        if validaciones.es_mensaje_valido(mensaje.get('message')):
            messages.append(f"{mensaje.get('from')} {mensaje.get('from_name')}: {mensaje.get('message')}<br>")
        else:
            fecha_para_asunto = validaciones.transform_date_format(mensaje.get('date'))
            asunto_mensaje = f"{mensaje.get('from_name')}{fecha_para_asunto}{mensaje.get('customer_phone')}"
            file_format, base64_data = decode_images.extract_base64_image(mensaje.get('message'))
            if file_format and base64_data:
                beaware_api_requests.addFile(client, base64_data, file_format, asunto_mensaje, case_id, 9) #9 ES LA ID DEL USUARIO JCARRILLO
            else:
                print("No se pudo extraer la imagen en base64 del mensaje.")
    
    if messages:
        conversation = " ".join(messages)  # Se unen todas als interacciones en un string
        conversation_without_emojis = validaciones.remove_emojis(conversation)
        note = {
            "idobjeto": case_id,
            "tipoobjeto": "casos",
            "texto":  f"<p>{conversation_without_emojis}</p>",
            "privado": 1
        }

        beaware_note = beaware_api_requests.addNotes(client, note)
        message_list.append(beaware_note)
        return note


def process_chat(client, chat, conversations_data, contact_list, case_list, message_list, types):
    """Procesa un chat individual y actualiza las listas de contactos, casos y mensajes."""
    # Procesa el contacto
    contacto = build_contact(client, chat, contact_list)
    
    if not contacto:
        return None
    
    id_contacto = contacto.get("id")
    if not id_contacto:
        print("Fallo al obtener la id del contacto")
        return None

    # AGREGAR LÓGICA PARA CREAR CONTACTO EN BE AWARE
    # SI CONTACTO SE CREA EXITOSAMENTE, OBTENER ID Y AGREGAR A LISTA
    # SI NO, CANCELAR EL FLUJO CORRESPONDIENTE AL CONTACTO, Y SEGUIR CON EL SIGUIENTE

    case = build_case(client, chat, case_list, id_contacto, types)

    if not case:
        return None
    
    case_id = case.get("id")
    if not case_id:
        print("No se pudo obtener la id del caso")
        return None

    conversation_info = obtain_conversation_info_from_chat(chat.get("conn_id"), conversations_data)
    if not conversation_info:
        return None

    # Procesa los mensajes
    beaware_message = process_messages(client, conversation_info, message_list, case_id)
    print(f"\nInteracciones totales: {len(conversation_info)}")
    print("-" * 140)
    return 



def almacenarEnArchivo(lista_elementos, archivo):
    """Guarda una lista de elementos en un archivo JSON, sobrescribiendo su contenido."""
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(lista_elementos, f, ensure_ascii=False, indent=4)

def almacenarContactos(lista_contactos, archivo="contactos.json"):
    """Almacena los contactos en el archivo contactos.json"""
    almacenarEnArchivo(lista_contactos, archivo)

def almacenarCasos(lista_casos, archivo="casos.json"):
    """Almacena los casps en el archivo casos.json"""
    almacenarEnArchivo(lista_casos, archivo)

def almacenarMensajes(lista_mensajes, archivo="mensajes.json"):
    """Almacena los mensajes en el archivo mensajes.json"""
    almacenarEnArchivo(lista_mensajes, archivo)

def almacenarImagenesData(lista_casos, archivo="imagenes_data.json"):
    """Almacena los casps en el archivo casos.json"""
    almacenarEnArchivo(lista_casos, archivo)

