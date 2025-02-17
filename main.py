from email import message
import create_functions
import wolkvox_api_requests
import validaciones
import decode_images


def obtain_conversation_info_from_chat(conn_id, conversations_array):
    """Busca y retorna la conversación (mensajes) del chat a través de la id de conexión."""
    for conversation in conversations_array:
        if conversation.get("conn_id") == conn_id:
            return conversation.get("conversation")
    return None


def build_contact(chat):
    """Construye y retorna el diccionario de contacto a partir del chat."""
    customer_name = chat.get("customer_name")
    full_name = validaciones.procesar_nombre_apellido(customer_name)
    return {
        "nombre": full_name["name"],
        "apellido": full_name["last_name"],
        "identificador": chat.get("customer_phone"),
        "email": chat.get("customer_email"),
        "timezone": "America/Santiago",
    }


def build_case(chat):
    """Construye y retorna el diccionario del caso a partir del chat."""
    asunto = (
        f"{chat.get('date')}-{chat.get('cod_act')}/"
        f"{chat.get('description_cod_act')}-{chat.get('conn_id')}"
    )
    return {
        "idcontacto": "***___OBTENER___***",
        "idproducto": chat.get("cod_act"),
        "idtipo": chat.get("description_cod_act"),
        "subtipo": "***___OBTENER___***",
        "asunto": asunto,
        "origen": chat.get("channel"),
    }


def process_messages(conversation_info, message_list, image_counter):
    """
    Procesa cada mensaje de la conversación.
    
    - Si el mensaje es válido (texto), lo agrega a message_list.
    - Si no, asume que es una imagen y la decodifica, incrementando el contador.
    """
    for mensaje in conversation_info:
        if validaciones.es_mensaje_valido(mensaje.get('message')):
            message = {
                "idobjeto": "***___OBTENER___***",
                "tipoobjeto": "casos",
                "texto": f"{mensaje.get('from')} {mensaje.get('from_name')}: {mensaje.get('message')}",
                "privado": 1
            }
            message_list.append(message)
        else:
            fecha_para_asunto = validaciones.transform_date_format(mensaje.get('date'))
            asunto_mensaje = f"{mensaje.get('from_name')}{fecha_para_asunto}{mensaje.get('customer_phone')}"
            decode_images.save_image_from_base64(mensaje.get('message'), asunto_mensaje)
            image_counter += 1
    return image_counter


def process_chat(chat, conversations_data, contact_list, case_list, message_list, image_counter):
    """Procesa un chat individual y actualiza las listas de contactos, casos y mensajes."""
    # Procesa el contacto y el caso
    contacto = build_contact(chat)
    contact_list.append(contacto)
    caso = build_case(chat)
    case_list.append(caso)

    # Obtiene la conversación del chat
    conversation_info = obtain_conversation_info_from_chat(chat.get("conn_id"), conversations_data)
    if not conversation_info:
        return image_counter

    print(f"Customer name: {chat.get('customer_name')}")
    print(f"Razón: {chat.get('cod_act')}")
    # Se llama a la función para almacenar mensajes, si es que ese comportamiento es requerido aquí.
    create_functions.almacenarMensajes(chat.get('customer_name'))

    # Procesa los mensajes
    image_counter = process_messages(conversation_info, message_list, image_counter)
    print(f"\nInteracciones totales: {len(conversation_info)}")
    print("-" * 140)
    return image_counter


def main():
    """Flujo principal de la aplicación."""
    contact_list = []  # Lista de contactos a almacenar en JSON
    message_list = []  # Lista de mensajes a almacenar en JSON
    case_list = []     # Lista de casos a almacenar en JSON
    image_counter = 0

    # Obtención de los datos de Wolkvox
    chats_data = wolkvox_api_requests.fetch_chats()
    # Filtra chats con el código de actividad "Consulta"
    filtered_chats = [chat for chat in chats_data if chat.get("cod_act") == "Consulta"]
    conversations_data = wolkvox_api_requests.fetch_conversations()

    # Procesa cada chat filtrado
    for chat in filtered_chats:
        image_counter = process_chat(chat, conversations_data, contact_list, case_list, message_list, image_counter)

    # Almacena las listas en los JSON correspondientes
    create_functions.almacenarContactos(contact_list)
    create_functions.almacenarMensajes(message_list)
    create_functions.almacenarCasos(case_list)

    print("Imágenes obtenidas:", image_counter)


if __name__ == "__main__":
    main()
