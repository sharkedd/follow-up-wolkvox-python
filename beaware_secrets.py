import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

BEAWARE_COMPANY = os.getenv("BEAWARE_COMPANY")
BEAWARE_USER = os.getenv("BEAWARE_USER")
BEAWARE_PASSWORD = os.getenv("BEAWARE_PASSWORD")
