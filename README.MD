# AI ChatBot Investments

[TOC]

## Instalación

- Se recomienda crear un ambiente virtual para evitar conflictos de versiones. En la raíz del proyecto, ejecutar el siguiente comando:

	`$ python -m venv .\.venv`

- Activar el ambiente virtual recién creado:

	`$ .\.venv\Scripts\activate`

- Instalar las dependencias señaladas en el archivo requiremente.txt:

	`$ python -m pip install -r requirements.txt`

- Ejecutar el archivo 'AIChatBot-Investments.py':

	`$ python AIChatBot-Investments.py`



## Características
- Recopila información financiera sobre empresas.
- Obtiene información adicional si encuentra noticias sobre las empresas.
- Responde preguntas sobre inversiones utilizando la información obtenida.
- Puede recordar interacciones anteriores.

## Restricciones
- Solo puede encontrar empresas que estén en Yahoo Finance.
-  Se debe seguir un formato específico para algunas características.

## Instrucciones

Una vez que cargue la interfaz del chatbot, se le puede empezar a hacer consultas sobre el mercado y las acciones de algunas empresas. El chatbot intentará obtener información financiera sobre esa empresa y recopilar información adicional si es que encuentra una noticia relacionada.
Para obtener información sobre alguna empresa se debe seguir el formato 'Empresa {nombre empresa}:' o el formato 'Empresa "{nombre empresa}".

- Se puede utilizar el primer formato señalado:

`Empresa Netflix: (...)`

`Con respecto a la empresa AMAZON: (...)`

`Me gustaría obtener información sobre la empresa tesla: (...)`


- O el otro formato señalado:

`Empresa "Netflix" (...)`

`Si consideramos las finanzas de la empresa "AMAZON" (...)`

`Tengo interés en las acciones de la empresa "tesla" (...)`

## Repositorio de GitHub

`GitHub`: [AI Chatbot Investments][id/name] 

[id/name]: https://github.com/JuanAdasme/investment-chatbot

> Creado por Juan Adasme
> Escrito y probado con Python 3.11.4
