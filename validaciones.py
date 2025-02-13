def es_mensaje_valido(mensaje):
    """Descarta mensajes que comienzan con '<a href=\"', ya que son imágenes."""
    return not mensaje.startswith('<a href="')