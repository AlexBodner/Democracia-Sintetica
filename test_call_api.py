# --- Imports ---
import os
from dotenv import load_dotenv
import asyncio # Necesario para correr funciones asíncronas
from typing import Any
from pydantic import BaseModel, Field, ValidationError 
from openai import AsyncAzureOpenAI
import instructor # Importa instructor

# Cargar variables de entorno desde .env file
load_dotenv()

# Acceder a las variables (asegúrate de que estas existan en tu .env)
api_key = os.getenv("API_KEY")
endpoint = os.getenv("ENDPOINT")
model_name = os.getenv("MODEL") # Cambiado a model_name para evitar conflicto con la variable 'model' en la clase si la crearas
deployment_name = os.getenv("DEPLOYMENT") # Cambiado a deployment_name

# Validar que las variables se cargaron (opcional pero recomendado)
if not all([api_key, endpoint, deployment_name]):
    print("Error: Asegúrate de que API_KEY, ENDPOINT y DEPLOYMENT están definidos en tu archivo .env")
    exit() # Salir si faltan variables esenciales

# Inicializar el cliente de Azure OpenAI (ya parcheado por instructor)

async_client_instance = AsyncAzureOpenAI(
    api_version="2024-12-01-preview", # O la versión de API que uses
    azure_endpoint=endpoint,
    api_key=api_key
)
client = instructor.patch(async_client_instance) # Parchea la instancia específica

# --- Definición del Modelo Pydantic para la Respuesta ---
# Adaptamos la estructura para una opinión liberal
class OpinionLiberal(BaseModel):
    razonamiento: str = Field(description="El razonamiento detrás de la opinión desde una perspectiva liberal.")
    opinion: str = Field(description="La opinión principal sobre el tópico propuesto, formulada desde una perspectiva liberal.")
    # Puedes añadir más campos si quieres estructurar más la respuesta (ej: 'puntos_clave: list[str]')


# --- Función Asíncrona Principal ---
async def main():
    print(f"Endpoint: {endpoint}")
    print(f"Deployment: {deployment_name}")

    # Define el tópico sobre el que quieres la opinión
    topico_a_opinar = "¿Cuál debería ser el rol del estado en la educación?"

    # --- Definición de Mensajes ---
    # Adaptamos el mensaje del sistema y removemos el few-shot de clasificación de tickets
    messages = [
        {
            "role": "system",
            "content": (
                "Eres un agente de opinión con una fuerte perspectiva liberal clásica. "
                "Tu tarea es analizar el tópico presentado y generar una opinión clara y concisa desde esta óptica. "
                "Enfócate en principios como la libertad individual, la competencia, la mínima intervención estatal, los mercados libres y la responsabilidad personal. "
                "La respuesta debe ser estructurada y concisa, y debe poder ser parseada como un JSON válido que cumpla con el esquema de OpinionLiberal." # Indicamos que la salida debe ajustarse al schema
            ),
        },
        # Puedes añadir few-shot examples aquí si quieres guiar MÁS el estilo de la opinión,
        # pero no necesitan ser JSONs si usas response_model. Solo mostrar la interacción User/Assistant
        # que lleve a una respuesta *que el modelo sea capaz de generar y que se pueda parsear*.
        # Por ejemplo (opcional):
        # {
        #     "role": "user",
        #     "content": "¿Opina sobre los impuestos a la riqueza?"
        # },
        # {
        #     "role": "assistant",
        #     "content": "Desde una óptica liberal, los impuestos a la riqueza son contraproducentes. Argumento que desincentivan la inversión y el ahorro, fomentando la fuga de capitales y limitando la libertad de los individuos sobre los frutos de su trabajo. Su implementación a menudo resulta compleja y puede generar ineficiencias económicas..." # Este sería el tipo de texto que el modelo generaría antes de ser parseado
        # },
        {
            "role": "user",
            "content": f"Opina desde una perspectiva liberal sobre: {topico_a_opinar}",
        },
    ]

    # --- Llamada a la API usando response_model ---
    # Usamos el cliente parcheado 'client'
    # El response_model le indica a instructor que intente parsear la respuesta en el objeto OpinionLiberal
    try:
        opinion_generada: OpinionLiberal = await client.chat.completions.create(
            model=deployment_name, # Usar el nombre del deployment en Azure
            messages=messages,
            response_model=OpinionLiberal, # Especifica el modelo Pydantic esperado
            max_retries=3 # instructor puede reintentar si el parseo falla inicialmente
        )

        # --- Imprimir la opinión generada ---
        # Como la respuesta es un objeto OpinionLiberal, puedes acceder a sus atributos
        print("\n--- Opinión Liberal Generada ---")
        print(f"Tópico: {topico_a_opinar}")
        print(f"Opinión: {opinion_generada.opinion}")
        print(f"Razonamiento: {opinion_generada.razonamiento}")
        # Si quieres ver el JSON crudo que cumple el esquema:
        # print("\n--- JSON de la Opinión ---")
        # print(opinion_generada.model_dump_json(indent=2)) # Usa model_dump_json() en Pydantic v2+

    except ValidationError as e:
        print(f"Error de validación de Pydantic: {e}")
    except Exception as e:
        print(f"Ocurrió un error al llamar a la API: {e}")


# --- Ejecutar la función principal asíncrona ---
# Este bloque es el punto de entrada al script
if __name__ == "__main__":
    asyncio.run(main())