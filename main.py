import create_functions
import wolkvox_api_requests


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
        image_counter = create_functions.process_chat(chat, conversations_data, contact_list, case_list, message_list, image_counter)

    # Almacena las listas en los JSON correspondientes
    create_functions.almacenarContactos(contact_list)
    create_functions.almacenarMensajes(message_list)
    create_functions.almacenarCasos(case_list)

    print("Imágenes obtenidas:", image_counter)


if __name__ == "__main__":
    main()
