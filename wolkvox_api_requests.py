import requests
import wolkvox_secrets

#Intervalo de fechas que acotarán la solicitud.
#Formato: YYYYmmddHHiiss
DATE_INI = "20250215000000"
DATE_END = "20250216000000"

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
