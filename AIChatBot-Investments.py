from tkinter import *
from tkinter import ttk
import modules.constants as const
import modules.app as app
import modules.menu as menu
import modules.scraper as scraper

context = []
app.system_message = app.generate_message(
    const.SYSTEM_ROLE, const.MOOD[const.EXECUTIVE])
app.messages.append(app.system_message)


def chatbot_response(user_input):
    if user_input:
        if app.change_mood:
            app.messages[0] = app.system_message
            app.change_mood = False
        message = app.generate_message(const.USER_ROLE, user_input)
        app.messages.append(message)
        return app.execute_client()


def clear_user_input(*args):
    user_in.set("")


def send_message(*args):
    text_area.insert(END, f"(Pensando...)\n\n")

    user_input = user_in.get().__add__("\n")

    clear_user_input()

    response = chatbot_response(user_input)
    response_message = response.choices[0].message
    answer = response_message.content.replace("\\n", "\n")
    context.append(app.generate_message(const.USER_ROLE, user_input))
    context.append(app.generate_message(
        response_message.role, answer + "\n\n"))

    text_area.insert(END, f"Usuario: {user_input}\n")
    text_area.insert(END, f"Chatbot: {answer}\n")
    text_area.see(END)


selected_mood = const.EXECUTIVE


def set_mood(mood):
    global selected_mood
    selected_mood = mood
    app.change_mood = True
    app.system_message = app.generate_message(
        const.SYSTEM_ROLE, const.MOOD[mood])


def set_executive_mood():
    if selected_mood == const.EXECUTIVE:
        print("Ya soy un ejecutivo de inversiones, señor.")
    else:
        print("Bienvenido, señor, soy su asesor de inversiones.")
        set_mood(const.EXECUTIVE)


def set_pirate_mood():
    if selected_mood == const.PIRATE:
        print("¡Arr! ¡Ya soy un pirata, marinero de agua dulce!")
    else:
        print("¡Soy un viejo pirata! ¡Arr!")
        set_mood(const.PIRATE)


def set_romantic_poet_mood():
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
text_area = Text(text_frame, bg="white", width=100,
                 height=40, yscrollcommand=scrollbar.set)

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
ttk.Button(main_frame, text="Borrar", command=clear_user_input).grid(
    column=3, row=3)

for child in main_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Crea la etiqueta para los botones de carácter del chatbot.
ttk.Label(main_frame, text="Carácter del bot:").grid(column=1, row=4)

# Crea los botones para cambiar el carácter del chatbot
ttk.Button(main_frame, text="Ejecutivo", command=set_executive_mood).grid(
    column=2, row=4)
ttk.Button(main_frame, text="Pirata", command=set_pirate_mood).grid(
    column=3, row=4)
ttk.Button(main_frame, text="Poeta", command=set_romantic_poet_mood).grid(
    column=4, row=4)

# Deja el foco en el campo de entrada del usuario
user_prompt.focus_set()

# Crea una relación entre presionar la tecla 'Enter' y gatillar el envío de la información
root.bind("<Return>", send_message)

# send_button = Button(
#    root, text="Enviar", command=lambda: send_message())
# send_button.pack()

root.mainloop()


def main():
    # Primera pregunta que se le hace al sistema.
    content = "Explícame cómo cocinar fideos de arroz con verduras al curry."

    # Genera la estructura del mensaje con el rol de usuario y el contenido del primer mensaje.
    message = app.generate_message(app.USER_ROLE, content)

    # Agrega el mensaje generado a la lista de mensajes que se enviará a la API.
    app.messages.append(message)

    # Ejecuta la llamada a la API con los mensajes definidos.
    completion = app.execute_client(app.messages)

    # Extrae la respuesta del chatbot.
    answer = completion.choices[0].message

    # Imprime el rol de la respuesta.
    print(answer.role)
    print(completion.choices[0].message)

    # Imprime la respuesta del chatbot, formateando los saltos de línea.
    print(answer.content.replace("\\n", "\n"))

    # Genera nuevo mensaje con la respuesta otorgada por la API.
    message = app.generate_message(answer.role, answer.content)

    # Añade la respuesta a la lista de mensajes para darle contexto al chatbot sobre el historial de preguntas. Esto afecta a la cantidad de tokens.
    app.messages.append(message)

    # Segunda pregunta que se le hace al sistema, esperando que mantenga el contexto.
    content = "Y si en vez de fideos de arroz utilizo quínoa, ¿qué tendría que cambiar?"

    # Genera la estructura del segundo mensaje.
    message = app.generate_message(app.USER_ROLE, content)

    # Agrega la nueva entrada a la lista de mensajes.
    app.messages.append(message)

    # Ejecuta la segunda llamada a la API.
    completion = app.execute_client(app.messages)
    print(completion)

    # Extrae la respuesta del chatbot
    answer = completion.choices[0].message

    # Imprime la respuesta del chatbot, formateando los saltos de línea.
    print(answer.content.replace("\\n", "\n"))


# indicators = scraper.get_indicators()
# print(indicators)

menu.print_exit()
