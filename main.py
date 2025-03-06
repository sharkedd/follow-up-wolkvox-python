from beaware_api_client import APIClient
import beaware_api_requests
import create_functions
import wolkvox_api_requests
import beaware_secrets
from datetime import datetime, timedelta


def main():
    """Flujo principal de la aplicación."""
    message_list = []  # Lista de mensajes a almacenar en JSON
    case_list = []     # Lista de casos a almacenar en JSON

    #Formato: YYYYmmddHHiiss
    #EJEMPLO: 20250305000000
    #EJEMPLO: 20250306000000

    # Obtener la fecha y hora actual
    now = datetime.now()
    date_end = now.strftime("%Y%m%d%H%M%S")
    print(f"Hora limitante: {date_end}")

    one_hour_ago = now - timedelta(hours=5)
    date_ini = one_hour_ago.strftime("%Y%m%d%H%M%S")
    print(f"Hora inicio: {date_ini}")

    # Obtención de los datos de Wolkvox
    chats_data = wolkvox_api_requests.fetch_chats(date_ini, date_end)

    # Filtra chats con el código de actividad "Consulta"
    filtered_chats = [chat for chat in chats_data if (chat.get("cod_act") == "Consulta" or chat.get("cod_act") == "Reclamo")]
    print("Filtrando por cod_Act Consulta")

    conversations_data = wolkvox_api_requests.fetch_conversations(date_ini, date_end)

    # Obtiene el token para luego crear al cliente que mantendrá la comunicación con la API
    token = beaware_api_requests.login()
    if not token:
        raise Exception("No se pudo obtener el token")
    
    print("Token obtenido")
    
    # Crear cliente que se comunicara con la api de BeAware
    client = APIClient(beaware_secrets.COMPANY, beaware_secrets.USER, token)

    if not client:
        print("Ocurrió un problema al crear al cliente")
        
    types = beaware_api_requests.obtainTypes(client)
    print(f"Tipos: {types}")

    products = beaware_api_requests.obtainProducts(client)
    print(f"Productos: {products}")

    contact_list = beaware_api_requests.obtainContacts(client)
    print("Contactos de BeAware obtenidos")

    case_list = beaware_api_requests.obtainCases(client)
    print("Casos de BeAware obtenidos")

    
    # Procesa cada chat filtrado
    print("Comenzando procesamiento...")
    for chat in filtered_chats:
        create_functions.process_chat(client, chat, conversations_data, contact_list, case_list, message_list, types, products)

    # Almacena las listas en los JSON correspondientes
    create_functions.almacenarContactos(contact_list)
    create_functions.almacenarMensajes(message_list)
    create_functions.almacenarCasos(case_list)


if __name__ == "__main__":
    main()
