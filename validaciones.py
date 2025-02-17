def es_mensaje_valido(mensaje, limite_caracteres=1000):
    """Descarta mensajes que comienzan con '<a href=\"' o que superan el límite de caracteres."""
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
    return date_str.replace(" ", "").replace(":", "_")
