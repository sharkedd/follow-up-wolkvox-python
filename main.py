import requests
import wolkvox_secrets

# Intervalo de fechas que acotarán la solicitud
DATE_INI = "20250211000000"
DATE_END = "20250212000000"

def fetch_chats():
    """Obtiene la lista de chats de Wolkvox."""
    url = f"https://wv{wolkvox_secrets.WOLKVOX_SERVER}.wolkvox.com/api/v2/reports_manager.php?api=chat_1&date_ini={DATE_INI}&date_end={DATE_END}"
    headers = {
        "wolkvox_server": wolkvox_secrets.WOLKVOX_SERVER,
        "wolkvox-token": wolkvox_secrets.WOLKVOX_TOKEN
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza un error si el request falla
        return response.json().get("data", [])
    except requests.RequestException as e:
        print(f"Error al obtener los chats: {e}")
        return []

def fetch_conversations():
    """Obtiene la lista de conversaciones de Wolkvox."""
    url = f"https://wv{wolkvox_secrets.WOLKVOX_SERVER}.wolkvox.com/api/v2/reports_manager.php?api=chat_2&date_ini={DATE_INI}&date_end={DATE_END}"
    headers = {
        "wolkvox_server": wolkvox_secrets.WOLKVOX_SERVER,
        "wolkvox-token": wolkvox_secrets.WOLKVOX_TOKEN
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.RequestException as e:
        print(f"Error al obtener las conversaciones: {e}")
        return []

def obtain_conversation_info_from_chat(conn_id, conversations_array):
    """Busca la conversación relacionada con el chat dado."""
    for conversation in conversations_array:
        if conversation.get("conn_id") == conn_id:
            return conversation.get("conversation")
    return None

def main():
    chats_data = fetch_chats()
    filtered_chats = [chat for chat in chats_data if chat.get("cod_act") == "Consulta"]
    conversations_data = fetch_conversations()

    for chat in filtered_chats:
        customer_name = chat.get("customer_name")
        identificador = chat.get("customer_phone")
        email = chat.get("customer_email")

        connection_id = chat.get("conn_id")
        origen = chat.get("channel")
        cod_act = chat.get("cod_act")
        description_cod_act = chat.get("description_cod_act")
        
        date = chat.get("date")
        agent_id = chat.get("agent_id")
        agent_name = chat.get("agent_name")
        comments = chat.get("comments")

        filtered_conversations = obtain_conversation_info_from_chat(connection_id, conversations_data)

        if not filtered_conversations:
            continue

        print(f"Customer name: {customer_name}")
        print(f"Razón: {cod_act}")
        for conversation in filtered_conversations:
            print(f"Enviado por: {conversation.get('from_name')}")
            print(conversation.get("date"))

        print(f"\nInteracciones totales: {len(filtered_conversations)}")
        print("-" * 140)

if __name__ == "__main__":
    main()
