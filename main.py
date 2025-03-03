from beaware_api_client import APIClient
import beaware_api_requests
import create_functions
import wolkvox_api_requests
import beaware_secrets

def main():
    """Flujo principal de la aplicación."""
    message_list = []  # Lista de mensajes a almacenar en JSON
    case_list = []     # Lista de casos a almacenar en JSON
    image_counter = 0
    

    # # Obtención de los datos de Wolkvox
    # chats_data = wolkvox_api_requests.fetch_chats()

    # # Filtra chats con el código de actividad "Consulta"
    # filtered_chats = [chat for chat in chats_data if chat.get("cod_act") == "Consulta"]
    # conversations_data = wolkvox_api_requests.fetch_conversations()

    # Obtiene el token para luego crear al cliente que mantendrá la comunicación con la API
    token = beaware_api_requests.login()
    if not token:
        raise Exception("No se pudo obtener el token")
    
    client = APIClient(beaware_secrets.COMPANY, beaware_secrets.USER, token)

    types = beaware_api_requests.obtainTypes(client)
    print(types)

    productos = beaware_api_requests.obtainProducts(client)
    print(productos)

    # contact_list = beaware_api_requests.obtainContacts(client)

    
    # # Procesa cada chat filtrado
    # for chat in filtered_chats:
    #     image_counter = create_functions.process_chat(client, chat, conversations_data, contact_list, case_list, message_list, types, image_counter)

    # # Almacena las listas en los JSON correspondientes
    # create_functions.almacenarContactos(contact_list)
    # create_functions.almacenarMensajes(message_list)
    # create_functions.almacenarCasos(case_list)

    # print("Imágenes obtenidas:", image_counter)


if __name__ == "__main__":
    main()
