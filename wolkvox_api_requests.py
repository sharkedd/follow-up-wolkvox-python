import requests
import wolkvox_secrets


#Intervalo de fechas que acotarán la solicitud.


def fetch_chats(date_ini, date_end):
    """Obtiene la lista de chats de Wolkvox."""
    url = f"https://wv{wolkvox_secrets.WOLKVOX_SERVER}.wolkvox.com/api/v2/reports_manager.php?api=chat_1&date_ini={date_ini}&date_end={date_end}"
    headers = {
        "wolkvox_server": wolkvox_secrets.WOLKVOX_SERVER,
        "wolkvox-token": wolkvox_secrets.WOLKVOX_TOKEN
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza un error si el request falla
        print("Chats obtenidos de Wolkvox")
        return response.json().get("data", [])
    except requests.RequestException as e:
        print(f"Error al obtener los chats: {e}")
        return []
    


def fetch_conversations(date_ini, date_end):
    """Obtiene la lista de conversaciones de Wolkvox."""
    url = f"https://wv{wolkvox_secrets.WOLKVOX_SERVER}.wolkvox.com/api/v2/reports_manager.php?api=chat_2&date_ini={date_ini}&date_end={date_end}"
    headers = {
        "wolkvox_server": wolkvox_secrets.WOLKVOX_SERVER,
        "wolkvox-token": wolkvox_secrets.WOLKVOX_TOKEN
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("Conversaciones obtenidas de wolkvox")
        return response.json().get("data", [])
    except requests.RequestException as e:
        print(f"Error al obtener las conversaciones: {e}")
        return []
