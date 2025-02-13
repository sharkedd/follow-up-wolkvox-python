import json
import os

def agregar_y_guardar(elemento, archivo="datos.json"):
    datos = []
    
    # Si el archivo existe, cargar los datos previos
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
                if not isinstance(datos, list):  # Asegurar que es una lista
                    datos = []
            except json.JSONDecodeError:
                datos = []

    # Agregar el nuevo elemento
    datos.append(elemento)

    # Guardar de nuevo en el archivo
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


