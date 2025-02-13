import create_functions
import wolkvox_api_requests


def obtain_conversation_info_from_chat(conn_id, conversations_array):
    """Busca la conversación relacionada con el chat dado."""
    for conversation in conversations_array:
        if conversation.get("conn_id") == conn_id:
            return conversation.get("conversation")
    return None


def main():
    chats_data = wolkvox_api_requests.fetch_chats()
    filtered_chats = [chat for chat in chats_data if chat.get("cod_act") == "Consulta"]
    conversations_data = wolkvox_api_requests.fetch_conversations()

    for chat in filtered_chats:
        #CONTACTOS
        customer_name = chat.get("customer_name")   #Nombre y apellido
        identificador = chat.get("customer_phone")  #Teléfono como identificador
        email = chat.get("customer_email")          #Verificar que correo exista
        #Agregar timezone

        #CASOS
        connection_id = chat.get("conn_id") #Identificador del caso
        origen = chat.get("channel") #Origen del caso
        cod_act = chat.get("cod_act") #Producto ---> (Se debe obtener la id de BeAware)
        description_cod_act = chat.get("description_cod_act") #Tipo ---> (Se debe obtener la id de BeAware)
        #subtipo --> (no aplica?)
        #idcontacto --> Obtener al crear contacto
        #asunto --> Inventar alguna combinación
        
        #Campos extras
        date = chat.get("date") #Fecha del chat
        agent_name = chat.get("agent_name") #Agente que estuvo en la interación
        comments = chat.get("comments") #Comentario sobre el chat, parece que no brindan mucha información

        #Utilidad
        agent_id = chat.get("agent_id") #Puede que sirva para obtener información de wolkvox

        filtered_conversations = obtain_conversation_info_from_chat(connection_id, conversations_data)

        if not filtered_conversations:
            continue

        print(f"Customer name: {customer_name}")
        print(f"Razón: {cod_act}")
        for conversation in filtered_conversations:
            print(f"Enviado por: {conversation.get('from_name')}")
            print(conversation.get("date"))

        print(f"\nInteracciones totales: {len(filtered_conversations)}")
        print("-" * 140)

if __name__ == "__main__":
    main()
