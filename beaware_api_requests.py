import requests
import json
from migration import company, user, password  # Nota: 'pass' es una palabra reservada en Python, por ello se usa 'password'

def login():
    try:
        URL_LOGIN = "https://api.beaware360.com/ba360/apir/v10_5/login/auth"
        payload = {
            "company": company,
            "user": user,
            "pass": password
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(URL_LOGIN, json=payload, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es 200 OK

        data = response.json()
        token = data.get("token")
        return token

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as error:
        print("Error en la solicitud:", error)

# Ejemplo de uso:
if __name__ == '__main__':
    token = login()
    if token:
        print("Token obtenido:", token)
