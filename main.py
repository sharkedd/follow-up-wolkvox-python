from email import message
import create_functions
import wolkvox_api_requests
import validaciones


def obtain_conversation_info_from_chat(conn_id, conversations_array):
    """Busca y retorna la conversación(mensajes) del chat a través de la id de conexión."""
    for conversation in conversations_array:
        if conversation.get("conn_id") == conn_id:
            return conversation.get("conversation")
    return None


def main():
    """Flujo principal"""
    chats_data = wolkvox_api_requests.fetch_chats()
    filtered_chats = [chat for chat in chats_data if chat.get("cod_act") == "Consulta"]
    conversations_data = wolkvox_api_requests.fetch_conversations()

    contact_list = [] #Lista con contactos que se almacenará en JSON
    message_list = [] #Lista con mensajes que se almacenará en JSON
    case_list = [] #Lista con casos que se almacenará en JSON

    for chat in filtered_chats:

        #Campos de contacto
        customer_name = chat.get("customer_name")
        full_name = validaciones.procesar_nombre_apellido(customer_name)
        contacto = {
            "nombre": full_name["name"],                    #Nombre
            "apellido": full_name["last_name"],             #Apellido
            "identificador": chat.get("customer_phone"),    #Teléfono como identificador
            "email": chat.get("customer_email") ,           #Verificar que correo exista
            "timezone": "America/Santiago",                 #Zona Horaria 
        }
        contact_list.append(contacto) #Agrega contacto a la lista
                
        #Campos de caso
        asunto = chat.get("date") + "-" + chat.get("cod_act") + "/" + chat.get("description_cod_act") + "-" + chat.get("conn_id")
        caso = {
        "idcontacto": "OBTENER",
        "idproducto" : chat.get("cod_act"), #cod_act ---> idproducto
        "idtipo" : chat.get("description_cod_act"), #description_cod_act ---> idtipo 
        "subtipo": "OBTENER",
        "asunto": asunto,
        "origen" : chat.get("channel"), #Origen del caso
        }
        case_list.append(caso) #Agrega caso a la lista

        #Campos extras
        agent_name = chat.get("agent_name") #Agente que estuvo en la interación
        comments = chat.get("comments") #Comentario sobre el chat, parece que no brindan mucha información

        #Utilidad
        agent_id = chat.get("agent_id") #Puede que sirva para obtener información de wolkvox

        conversationInfo = obtain_conversation_info_from_chat(chat.get("conn_id"), conversations_data)

        if not conversationInfo:
            continue

        print(f"Customer name: {customer_name}")
        print(f"Razón: {chat.get("cod_act")}")
        create_functions.almacenarMensajes(customer_name)
        #Itera sobre todos los mensajes enviados en la conversación
        for mensaje in conversationInfo:
            if(validaciones.es_mensaje_valido(mensaje.get('message'))): #Verifica que mensaje no sea imagen
                #Agrega mensaje modificado a la lista
                message = {
                    "idobjeto":"OBTENER",
                    "tipoobjeto":"casos",
                    "texto":mensaje.get('from') + " " + mensaje.get('from_name') + ": " + mensaje.get('message'),
                    "privado":1
                }
                message_list.append(message)

        print(f"\n Interacciones totales: {len(conversationInfo)}")
        print("-" * 140)

    #Almacenar las listas en los JSON correspondientes
    create_functions.almacenarContactos(contact_list)
    create_functions.almacenarMensajes(message_list)
    create_functions.almacenarCasos(case_list)

if __name__ == "__main__":
    main()
