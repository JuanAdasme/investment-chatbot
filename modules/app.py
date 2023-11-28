from openai import OpenAI
import os
from dotenv import load_dotenv

# Carga el contenido del archivo .env, donde se encuentra la API_KEY de OpenAI
load_dotenv()
client = OpenAI()
MODEL = os.environ.get("AI_MODEL")

system_message = ""

# Contiene el historial y las entradas del usuario para enviarlas al chatbot.
messages = []

# Bandera que indica si es necesario cambiar el carácter del bot o no.
change_mood = False


def generate_message(role, content):
    """ 
    Descripción:
        Genera un nuevo mensaje para añadir a la lista de mensajes del cliente de OpenAI.

    Parámetros:
        role Rol que se le asigna según el remitente del mensaje, que indica si es de sistema, de asistente o de usuario.
        content Contenido del mensaje, ya sea la entrada del usuario o la respuesta de la API.

    Retorno:
        Diccionario con el rol y el contenido del mensaje. (Diccionario).
    """
    return {"role": role, "content": content}


def execute_client():
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    return completion
