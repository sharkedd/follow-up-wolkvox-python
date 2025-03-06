import re
import unicodedata

def es_mensaje_valido(mensaje, limite_caracteres=1000):
    """Descarta como mensaje válido aquellos que comienzan con '<a href=\"' o que superan el límite de caracteres."""
    return not mensaje.startswith('<a href="') and len(mensaje) <= limite_caracteres


def procesar_nombre_apellido(nombre_completo):
    """Recibe un nombre completo y devuelve nombre y apellido separados."""
    
    # Eliminar espacios extra al inicio y final
    nombre_completo = nombre_completo.strip()
    
    # Si la cadena está vacía, devolver valores por defecto
    if not nombre_completo:
        return {"name": "Desconocido", "last_name": "Desconocido"}
    
    # Dividir por espacios
    partes = nombre_completo.split()

    # Si solo tiene un nombre
    if len(partes) == 1:
        return {"name": partes[0], "last_name": "Desconocido"}

    # Si tiene más de un nombre o más de un apellido
    return {
        "name": partes[0],                      # El primer elemento es el nombre
        "last_name": " ".join(partes[1:])          # Todo lo demás se considera apellido
    }


def transform_date_format(date_str):
    """Elimina los espacios y reemplaza los doble puntos de la fecha con barra baja"""
    return date_str.replace(" ", "").replace(":", "_")


def remove_emojis(text):
    """Abarca los unicode de los emojis, y los elimina del texto"""
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Símbolos y pictogramas
        "\U0001F680-\U0001F6FF"  # Transporte y mapas
        "\U0001F700-\U0001F77F"  # Alquimia
        "\U0001F780-\U0001F7FF"  # Geometría
        "\U0001F800-\U0001F8FF"  # Variaciones de flechas
        "\U0001F900-\U0001F9FF"  # Manos, animales, gestos
        "\U0001FA00-\U0001FA6F"  # Objetos adicionales
        "\U0001FA70-\U0001FAFF"  # Símbolos adicionales
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Símbolos adicionales
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def limpiar_texto(texto):
    """Elimina espacios y normaliza el texto eliminando caracteres invisibles."""
    if texto is None:
        return ""
    texto = texto.strip()  # Eliminar espacios al inicio y al final
    return texto.replace(" ", "")  # Eliminar todos los espacios

import re

def formatear_telefono(number):
    """
    Formatea el número telefónico entregado, convirtiendolo a 569XXXXXXXX
    Retorna el teléfono formateado
    En caso de que el teléfono entregado no sea válido, returna null"""
    # Eliminar caracteres no numéricos
    cleaned_number = re.sub(r'\D', '', number)
    
    # Si tiene exactamente 9 dígitos y empieza con 9
    if re.fullmatch(r'9\d{8}', cleaned_number):
        return f"56{cleaned_number}"
    
    # Si tiene exactamente 8 dígitos
    elif re.fullmatch(r'\d{8}', cleaned_number):
        return f"569{cleaned_number}"
    
    # Si tiene exactamente 11 dígitos y ya comienza con 569 (formato correcto)
    elif re.fullmatch(r'569\d{8}', cleaned_number):
        return cleaned_number
    
    else:
        return None  # Retornar el original si es inválido


## FUNCIÓN QUE OBTENIE CAMPOS DE IDENTIFICADOR Y TELEFONOS DE CONTACTOS DE BE AWARE, 
## Lo que ocurre, es que si el contacto fue creado por wsp, su teléfono estará en el identificador, pero si vino por el formulario web, este se encontrará en teléfonos
## Debido a esto, se creo esta función que trabaja con ambos valores, retornando el que corresponde al número
# def obtener_telefono(identificador, telefono):
#     """Obtiene 2 valores, retornando el que corresponda al teléfono. En caso contrario, retorna null"""
#     # Patrón de número telefónico
#     identificador_sin_espacios = limpiar_texto(identificador)      
#     telefono_sin_espacios = limpiar_texto(telefono)

#     patron_telefono = re.compile(r"^(\+?56)?\s?(0?9)\s?[98765432]\d{7}$")
#     # Verificar cuál de los valores coincide con el patrón de teléfono
#     if patron_telefono.match(identificador_sin_espacios):
#         return identificador_sin_espacios
#     elif patron_telefono.match(telefono_sin_espacios):
#         return telefono_sin_espacios
#     else:
#         print(f"Valor que no funcionó: \"{identificador_sin_espacios}\" y \"{telefono_sin_espacios}\"")
#         return None 

