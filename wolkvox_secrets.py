import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

WOLKVOX_SERVER = os.getenv("WOLKVOX_SERVER")
WOLKVOX_TOKEN = os.getenv("WOLKVOX_TOKEN")
