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
    """Función generate_message

    Descripción: Genera un nuevo mensaje para añadir a la lista de mensajes del cliente de OpenAI.
    Parámetros:
    role                                                            string
    content                                                         string
    Retorno: Diccionario con el rol y el contenido del mensaje.     dict
    """

    return {"role": role, "content": content}


def execute_client():
    """Función execute_client

    Descripción: Hace la llamada a la API de OpenAI con la entrada del usuario.
    Retorno: Respuesta de la API a la entrada del usuario.          ChatCompletion
    """

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    return completion
