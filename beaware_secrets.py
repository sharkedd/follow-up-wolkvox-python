import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

COMPANY = os.getenv("BEAWARE_COMPANY")
USER = os.getenv("BEAWARE_USER")
PASSWORD = os.getenv("BEAWARE_PASSWORD")
