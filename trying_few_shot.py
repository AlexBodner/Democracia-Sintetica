# --- Imports ---
import os
from dotenv import load_dotenv
import asyncio # Necesario para correr funciones asíncronas
from typing import Any
from pydantic import BaseModel, Field , ValidationError # Necesitas BaseModel y Field de pydantic

from openai import AsyncAzureOpenAI
import instructor # Importa instructor

# Inicializa el cliente de Azure OpenAI utilizando tus variables cargadas
# Necesitas pasar la version_api que estés usando también.
# Puedes definirla como una variable si no la tienes en .env
API_VERSION = "2024-12-01-preview" # <-- Define tu versión de API aquí. Verifica la correcta para tu deployment.

# Cargar variables de entorno desde .env file
load_dotenv()

# Asegúrate de que las variables API_KEY, ENDPOINT, y DEPLOYMENT_NAME se cargaron
api_key = os.getenv("API_KEY")
endpoint = os.getenv("ENDPOINT")
deployment_name = os.getenv("DEPLOYMENT")

if not all([api_key, endpoint, deployment_name]):
    print("Error: Asegúrate de que API_KEY, ENDPOINT y DEPLOYMENT están definidos en tu archivo .env")
    exit()

# Crea la instancia del cliente *antes* de parchearla
# Pasa explícitamente el endpoint y la clave API
async_client_instance = AsyncAzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=endpoint,
    api_key=api_key
)

# Aplica el parche de instructor a la instancia específica del cliente
client = instructor.patch(async_client_instance)

print(f"Endpoint (loaded): {endpoint}")
print(f"Deployment (loaded): {deployment_name}")

# --- Definición del Modelo Pydantic para la Respuesta ---
# Estructura para la opinión liberal
class OpinionLiberal(BaseModel):
    razonamiento: str = Field(description="El razonamiento detallado detrás de la opinión desde una perspectiva liberal, explicando los principios aplicados.")
    opinion_resumen: str = Field(description="Un resumen conciso de la opinión principal sobre el tópico propuesto, formulada desde una perspectiva liberal.")
    # Cambié 'opinion' a 'opinion_resumen' para diferenciarlo del campo 'razonamiento'


# --- Definición de Ejemplos Few-Shot para el Agente Liberal ---
# Estos ejemplos guían al modelo sobre el tipo de respuesta esperada.
# Nota: Las respuestas del assistant aquí son TEXTO, no JSON, ya que instructor las parseará después.
LIBERAL_FEWSHOT_EXAMPLES = [
    {
        "role": "user",
        "content": "Opina sobre el rol del estado en la economía.",
    },
    {
        "role": "assistant",
        "content": (
            "Desde una perspectiva liberal clásica, el rol del estado en la economía debería ser mínimo, centrándose en proteger los derechos de propiedad, hacer cumplir los contratos y garantizar un marco legal estable. "
            "El razonamiento fundamental es que los mercados libres, impulsados por la interacción voluntaria de individuos y empresas, asignan recursos de manera más eficiente y fomentan la innovación. "
            "La intervención estatal excesiva, como regulaciones intrusivas, subsidios o empresas estatales, tiende a distorsionar las señales del mercado, crear ineficiencias y limitar la libertad económica individual. "
            "La opinión principal es que una economía más libre, con menos injerencia estatal, conduce a una mayor prosperidad y libertad para todos."
        ),
    },
    {
        "role": "user",
        "content": "¿Qué postura liberal hay sobre los impuestos altos?",
    },
    {
        "role": "assistant",
        "content": (
            "El liberalismo tiende a oponerse a los impuestos altos, considerándolos una restricción significativa a la libertad económica y un desincentivo a la producción y la inversión. "
            "El razonamiento es que los individuos tienen derecho a conservar la mayor parte de los frutos de su trabajo, y que los impuestos confiscatorios reducen el capital disponible para inversión y consumo privado, factores clave para el crecimiento. "
            "Argumentamos que un sistema fiscal más bajo y simple fomenta la actividad económica, reduce la evasión y permite a las personas decidir cómo gastar o invertir su propio dinero de manera más efectiva que el gobierno. "
            "La opinión principal es que reducir la carga fiscal es esencial para una economía dinámica y para respetar la autonomía financiera de los ciudadanos."
        ),
    },
]


# --- Función Asíncrona Principal ---
async def main():
    # Define el tópico sobre el que quieres la opinión
    topico_a_opinar = "¿Es deseable un sistema de salud universal administrado por el estado desde una perspectiva liberal?"

    # --- Definición de Mensajes ---
    # Incluimos el mensaje del sistema, los few-shots y el nuevo tópico del usuario
    messages = [
        {
            "role": "system",
            "content": (
                "Eres un agente de opinión con una fuerte perspectiva liberal clásica. "
                "Tu tarea es analizar el tópico presentado y generar una opinión detallada y concisa desde esta óptica. "
                "Enfócate en principios como la libertad individual, la competencia, la mínima intervención estatal, los mercados libres y la responsabilidad personal. "
                "La respuesta debe ser estructurada para que pueda ser parseada como un JSON válido que cumpla con el esquema de OpinionLiberal, conteniendo el razonamiento y un resumen de la opinión."
            ),
        },
    ]
    # Agregamos los ejemplos few-shot
    messages.extend(LIBERAL_FEWSHOT_EXAMPLES)
    # Agregamos el tópico actual del usuario
    messages.append({
        "role": "user",
        "content": f"Opina desde una perspectiva liberal sobre: {topico_a_opinar}",
    })


    # --- Llamada a la API usando response_model ---
    # Usamos el cliente parcheado 'client'
    try:
        opinion_generada: OpinionLiberal = await client.chat.completions.create(
            model=deployment_name, # Usar el nombre del deployment en Azure
            messages=messages,
            response_model=OpinionLiberal, # Especifica el modelo Pydantic esperado
            max_retries=3 # instructor puede reintentar si el parseo falla inicialmente
        )

        # --- Imprimir la opinión generada ---
        print("\n--- Opinión Liberal Generada ---")
        print(f"Tópico: {topico_a_opinar}")
        print(f"Opinión Resumen: {opinion_generada.opinion_resumen}")
        print(f"Razonamiento: {opinion_generada.razonamiento}")

        # Si quieres ver el JSON crudo que cumple el esquema:
        # print("\n--- JSON de la Opinión ---")
        # print(opinion_generada.model_dump_json(indent=2)) # Usa model_dump_json() en Pydantic v2+

    except ValidationError as e:
        print(f"Error de validación de Pydantic: {e}")
        # Opcional: imprimir la respuesta cruda del modelo si falla la validación
        # print(f"Respuesta cruda recibida: {e.response.text}")
    except Exception as e:
        print(f"Ocurrió un error al llamar a la API: {e}")


# --- Ejecutar la función principal asíncrona ---
if __name__ == "__main__":
    # Verifica si el bucle de asyncio ya se está ejecutando (útil en notebooks)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError: # No running loop
        loop = None

    if loop and loop.is_running():
        print("Running from a notebook or context with an existing loop. Awaiting main()...")
        # Si estás en un entorno con un loop ya corriendo (como Jupyter/IPython),
        # simplemente await main()
        # await main() # Descomentar si realmente estás en ese entorno

    else:
        # Si no hay un loop corriendo, usamos asyncio.run()
        print("Running with asyncio.run()...")
        asyncio.run(main())