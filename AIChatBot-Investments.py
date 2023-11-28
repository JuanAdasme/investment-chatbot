from tkinter import *
from tkinter import ttk
import re
import modules.constants as const
import modules.app as app
import modules.menu as menu
import modules.scraper as scraper

context = []
companies = {}
assistant = []
initial_currency_values = None
selected_mood = const.EXECUTIVE


def initial_state():
    """Función initial_state

    Descripción: Define los valores iniciales para variables globales que
    sirven para manejar el contexto.

    """

    context.clear()
    companies.clear()
    assistant.clear()
    app.system_message = app.generate_message(
        const.SYSTEM_ROLE, const.MOOD[const.EXECUTIVE])
    app.messages.clear()
    app.messages.append(app.system_message)


def set_indicators():
    """Función set_indicators

    Descripción: Llama a la función get_indicators del web scraper, de 
    donde se obtienen los valores del dólar y la UF y se almacenan en 
    una variable global. Luego genera el mensaje de bienvenida.

    """

    currency_values = scraper.get_indicators()
    dollars = currency_values[0]
    ufs = currency_values[1]
    dollars_text = "Estos son los valores del dólar el último mes. "
    for day in dollars:
        dollars_text = f"{dollars_text}{day}: {dollars[day]}. "
    ufs_text = "Estos son los valores de la UF el último mes. "
    for day in ufs:
        ufs_text = f"{ufs_text}{day}: {ufs[day]}. "
    global initial_currency_values
    initial_currency_values = dollars_text + ufs_text
    app.messages.append(app.generate_message(
        const.SYSTEM_ROLE, initial_currency_values))
    input = "Por favor, dame la bienvenida a la asesoría de inversiones Davy Jones."
    app.messages.append(app.generate_message(const.USER_ROLE, input))
    response = app.execute_client()
    response_message = response.choices[0].message
    answer = response_message.content.replace("\\n", "\n")
    context.append(app.generate_message(const.USER_ROLE, input))
    context.append(app.generate_message(const.ASSISTANT_ROLE, answer))

    text_area.insert(END, f"Chatbot: {answer}\n\n")
    text_area.see(END)


def send_to_chatbot(user_input):
    """Función send_to_chatbot

    Descripción: Verifica el cambio de comportamiento del chatbot, 
    agrega el contexto y llama al método execute_client, que llama
    a la API de OpenAI con la entrada del usuario.
    Parámetros:
    user_input                              string
    Retorno: La respuesta del chatbot.      ChatCompletion
    """

    del app.messages[2:]
    if app.change_mood:
        # El primer mensaje es siempre para el comportamiento del bot.
        app.messages[0] = app.system_message
        app.change_mood = False

    # if len(context):
    context_content = "Este es el contexto: " + ("".join(context))
    context_message = app.generate_message(const.SYSTEM_ROLE, context_content)

    # El tercer mensaje es siempre para el contexto.
    app.messages.append(context_message)

    message = app.generate_message(const.USER_ROLE, user_input)

    # El cuarto mensaje es siempre para la entrada del usuario.
    app.messages.append(message)
    return app.execute_client()


def clear_cache(*args):
    """Función clear_cache

    Descripción: Limpia los campos y reinicia el estado de chatbot, 
    limpiando el historial.
    Parámetros:
    *args               Any
    """

    user_in.set("")
    text_area.delete('1.0', END)
    initial_state()
    app.messages.append(app.generate_message(
        const.SYSTEM_ROLE, initial_currency_values))


def check_company(user_input):
    """Función check_company

    Descripción: Busca el nombre de una empresa en la entrada del usuario.
    Si la encuentra, llama a la función get_company_stocks del web scraper
    para obtener sus datos financieros. Luego lo añade a un diccionario
    que sirve para entregar datos al contexto.
    Parámetros:
    user_input                  string
    """

    # Patrón para buscar el nombre de la empresa en formato 'empresa {nombre}:' o en formato 'empresa "{nombre}"' en mayúsculas o minúsculas.
    pattern = "(?:.*empresa (.*)\s*:)|(?:.*empresa \"(.*)\")"

    # Si encuentra el patrón, entonces busca información financiera de {nombre} en el mercado.
    match = re.search(pattern, user_input, re.I)

    if match is not None:
        first = match.group(1)
        second = match.group(2)
        company_name = first if first else second

        # Si la empresa ya está en el historial, no busca sus datos financieros.
        regex = re.compile(f"\s*{company_name}\s*", re.I)
        exists = list(filter(regex.match, companies))
        if exists:
            return

        company_info = scraper.get_company_stocks(company_name)

        # Si no se encuentra información de la empresa, se le notifica al usuario.
        if company_info is None:
            text_area.insert(
                END, f"Chatbot: No se encontró información sobre {company_name}, por favor intenta con otra empresa.\n\n")
            text_area.see(END)
            return

        # Agrega la información de la empresa a un diccionario.
        companies[company_name] = company_info


def fill_context(user_input):
    """Función fill_context

    Descripción: Define el contexto de una entrada según la entrada del usuario.
    Si el usuario menciona una empresa que esté en el historial, el contexto 
    va a almacenar las respuestas del historial relevantes para esa empresa.
    Parámetros:
    user_input                      string
    """

    context.clear()

    for company in companies:
        # Genera un patrón con el nombre de la empresa. Si el nombre está en la entrada del usuario,
        # añade la información de esa empresa al contexto para considerarla en la respuesta.
        pattern = f".*{company}.*"
        match = re.search(pattern, user_input, re.I)
        if match:
            print(f"Agregando {company} al contexto.\n")
            context.append(f"{company}: {companies[company]}")

            # Verifica si alguna de las respuestas anteriores menciona la empresa ingresada.
            # Si la menciona, añade la respuesta del bot al contexto.
            assistant_messages = ""
            for assist in assistant:
                matches = re.search(pattern, assist, re.I)
                if matches:
                    assistant_messages += assist
            context.append(assistant_messages)


def send_message(*args):
    """Función send_message

    Descripción: Recibe la entrada del usuario desde la interfaz y se
    la pasa a la función send_to_chatbot para enviarla al chatbot.
    También llama a las funciones check_company y fill_context y
    se encarga de mostrar la respuesta del chatbot en la interfaz.
    Parámetros:
    *args                           Any
    """

    user_input = user_in.get()

    if not user_input:
        return

    check_company(user_input)
    fill_context(user_input)

    text_area.insert(END, f"Usuario: {user_input}\n\n")
    user_in.set("")

    response = send_to_chatbot(user_input)
    response_message = response.choices[0].message
    answer = response_message.content.replace("\\n", "\n")
    assistant.append(answer)

    text_area.insert(END, f"Chatbot: {answer}\n\n")
    text_area.see(END)


def set_mood(mood):
    """Función set_mood

    Descripción: Establece el comportamiento del chatbot.
    Parámetros:
    mood                    string
    """

    global selected_mood
    selected_mood = mood
    app.change_mood = True
    app.system_message = app.generate_message(
        const.SYSTEM_ROLE, const.MOOD[mood])


def set_executive_mood():
    """Función set_executive_mood

    Descripción: Establece la variable global que define el
    comportamiento y el carácter del chatbot. En este caso,
    se comporta como un ejecutivo asesor de inversiones.
    """

    if selected_mood == const.EXECUTIVE:
        print("Ya soy un ejecutivo de inversiones, señor.")
    else:
        print("Bienvenido, señor, soy su asesor de inversiones.")
        set_mood(const.EXECUTIVE)


def set_pirate_mood():
    """Función set_pirate_mood

    Descripción: Establece la variable global que define el
    comportamiento y el carácter del chatbot. En este caso,
    se comporta como un pirata. ADVERTENCIA: Puede comportarse
    de forma grosera, usar con discreción.
    """

    if selected_mood == const.PIRATE:
        print("¡Arr! ¡Ya soy un pirata, marinero de agua dulce!")
    else:
        print("¡Soy un viejo pirata! ¡Arr!")
        set_mood(const.PIRATE)


def set_romantic_poet_mood():
    """Función set_romantic_poet_mood

    Descripción: Establece la variable global que define el
    comportamiento y el carácter del chatbot. En este caso,
    se comporta como un poeta del siglo XIX.
    """

    if selected_mood == const.POET:
        print("Si pudiese ser otra cosa, algo que tú más quisieras, aquello con gusto sería, ¡pero he nacido poeta!")
    else:
        print("Permíteme, ¡oh, mi querido amigo!, darte consejo en este, para bien o para mal, necesario asunto mundano.")
        set_mood(const.POET)


# Crea la ventana del programa.
root = Tk()
root.title("Inversiones Davy Jones")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Crea un elemento contenedor para los demás elementos.
main_frame = ttk.Frame(root, padding="3 3 12 12")
main_frame.grid(column=0, row=0)

# Crea un contenedor para el cuadro de texto.
text_frame = ttk.Frame(main_frame)
text_frame.grid(column=1, row=1, columnspan=4, sticky=(N, W, E))

# Crea una barra de desplazamiento para el cuadro de texto.
scrollbar = Scrollbar(text_frame)

# Crea el cuadro de texto donde se mostrarán las interacciones entre el usuario y el chatbot.
text_area = Text(text_frame, bg="white", width=60,
                 height=20, yscrollcommand=scrollbar.set)

# Configura la barra de desplazamiento.
scrollbar.config(command=text_area.yview)
scrollbar.pack(side=RIGHT, fill=Y)
text_area.pack(side=LEFT)

# Crea el campo de entrada para las consultas del usuario.
user_in = StringVar()
user_prompt = ttk.Entry(main_frame, width=7, textvariable=user_in)
user_prompt.grid(column=1, row=2, columnspan=4, sticky=(W, E))

# Crea el botón para enviar la entrada del usuario al chatbot.
ttk.Button(main_frame, text="Enviar", command=send_message).grid(
    column=2, row=3)

# Crea el botón para borrar la entrada del usuario.
ttk.Button(main_frame, text="Reiniciar", command=clear_cache).grid(
    column=3, row=3)

for child in main_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Crea la etiqueta para los botones de carácter del chatbot.
ttk.Label(main_frame, text="Carácter del bot:").grid(column=1, row=4)

# Crea los botones para cambiar el carácter del chatbot.
ttk.Button(main_frame, text="Ejecutivo", command=set_executive_mood).grid(
    column=2, row=4)
ttk.Button(main_frame, text="Pirata", command=set_pirate_mood).grid(
    column=3, row=4)
ttk.Button(main_frame, text="Poeta", command=set_romantic_poet_mood).grid(
    column=4, row=4)

# Deja el foco en el campo de entrada del usuario.
user_prompt.focus_set()

# Crea una relación entre presionar la tecla 'Enter' y gatillar el envío de la información.
root.bind("<Return>", send_message)

initial_state()
set_indicators()
root.mainloop()

menu.print_exit()
