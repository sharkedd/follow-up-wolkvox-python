import os
import re
import base64

def extract_base64_image(text):
    """
    Extrae el formato y los datos en base64 de un mensaje que contenga una imagen en formato data URI.
    Ejemplo: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    
    :param text: Cadena que contiene la data URI.
    :return: Tupla (formato, base64_data) o (None, None) si no se encuentra.
    """
    match = re.search(r'data:image/(png|jpeg|jpg);base64,([A-Za-z0-9+/=]+)', text)
    if match:
        return match.group(1), match.group(2)  # Retorna formato y datos base64
    return None, None

def get_new_filename(filepath, text):
    """Genera un nombre de archivo nuevo si el archivo ya existe, agregando un número secuencial.
       También verifica si la extracción de base64 es válida."""
    format, base64_data = extract_base64_image(text)
    if not base64_data:
        print("No se encontró una imagen válida en el texto.")
        return None
    
    dirname, filename = os.path.split(filepath)
    name, ext = os.path.splitext(filename)
    
    counter = 1
    new_filepath = filepath  # Inicialmente usamos el nombre base
    
    while os.path.exists(new_filepath):  # Si el archivo existe, incrementamos el número
        new_filepath = os.path.join(dirname, f"{name}{counter}{ext}")
        counter += 1
    
    return new_filepath

def save_image_from_base64(text, asunto_mensaje):
    """Recibe un texto que contiene una imagen en base64 y la guarda como imagen en la carpeta 'images'."""
    format, base64_data = extract_base64_image(text)
    if not base64_data:
        print("No se encontró una imagen válida en el texto.")
        return

    images_dir = os.path.join(os.getcwd(), 'images')
    os.makedirs(images_dir, exist_ok=True)

    file_path = os.path.join(images_dir, f"{asunto_mensaje}.{format}")
    file_path = get_new_filename(file_path, text)  # Asegurar un nombre único
    
    if file_path is None:
        return

    with open(file_path, "wb") as img_file:
        img_file.write(base64.b64decode(base64_data))
    
    print(f"Imagen guardada en: {file_path}")
