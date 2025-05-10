# --- Imports necesarios para las definiciones de clases ---
import asyncio # asyncio es necesario para el tipado AsyncAzureOpenAI
from typing import Any, List, Dict, Union # Tipado para métodos y atributos

from pydantic import BaseModel, Field, ValidationError # Clases base y excepciones de Pydantic
from openai import AsyncAzureOpenAI # Cliente asíncrono de OpenAI
import instructor # Librería para estructurar la salida del modelo

import os
from agents.agent_response_structure import StructuredAgentResponse
from dotenv import load_dotenv


# --- Cargar variables de entorno ---
load_dotenv()


# --- Clase API_Model ---
class API_Model:
    """
    Encapsula la lógica para interactuar con el modelo de lenguaje de OpenAI,
    INCLUYENDO la inicialización del cliente.
    Prepara los prompts (system, few-shot, user) y maneja las llamadas asíncronas,
    esperando una respuesta que cumpla con el esquema StructuredAgentResponse.
    """
    def __init__(
        self,
        system_prompt: Dict[str, str], # El mensaje del sistema que define el rol/persona del agente
        few_shot_examples: List[Dict[str, str]] = None, # Lista opcional de ejemplos few-shot
    ):
        """
        Inicializa la instancia de API_Model y el cliente de OpenAI internamente.

        Args:
            system_prompt: Diccionario {'role': 'system', 'content': '...'} para el agente.
            few_shot_examples: Lista opcional de mensajes few-shot.

        Raises:
            ValueError: Si falla la inicialización o parcheo del cliente OpenAI.
        """
        self.deployment_name =  os.getenv("DEPLOYMENT") 
        self.system_prompt = system_prompt
        self.few_shot_examples = few_shot_examples if few_shot_examples is not None else []
        # Asegúrate de que estas variables existan en tu .env
        api_key = os.getenv("API_KEY")
        endpoint = os.getenv("ENDPOINT")
        # --- Configuración de la API ---
        api_version = "2024-12-01-preview"
        try:
            # Crea la instancia del cliente usando los parámetros pasados al __init__
            async_client_instance = AsyncAzureOpenAI(
                api_version=api_version,
                azure_endpoint=endpoint,
                api_key=api_key
            )
            # Aplica el parche de instructor a la instancia específica del cliente
            self.client = instructor.patch(async_client_instance) # Almacena el cliente parcheado

        except Exception as e:
            raise ValueError(f"ERROR al inicializar o parchear el cliente OpenAI: {e}") from e



    async def call_api(
        self,
        topic: str,
        ronda:int,
        law: str = None,
        previous_rounds_context: List[Dict[str, str]] = None,

    ) -> Union[StructuredAgentResponse, None]:
        """
        Realiza una llamada asíncrona al modelo de lenguaje con el contexto y tópico dados.

        Args:
            topic: El tópico principal de la consulta del usuario.
            law: Opcional, información sobre una ley relacionada con el tópico.
            previous_rounds_context: Opcional, lista de mensajes que representan
                                     conversaciones anteriores (historial del chat).

        Returns:
            Una instancia de StructuredAgentResponse si la llamada a la API y el parseo
            son exitosos. Retorna None en caso de cualquier error (API o validación).
        """
        print(f"\nPreparando llamada a la API para tópico: '{topic}'...")
        if law:
            print(f"Relacionado con ley: '{law}'")

        # --- Construir la lista completa de mensajes para enviar a la API ---
        messages = [self.system_prompt] # 1. Empezamos con el mensaje del sistema

        # 2. Añadir few-shot examples (si existen)
        if self.few_shot_examples:
            messages.extend(self.few_shot_examples)

        # 3. Añadir contexto de rondas previas (si existe)
        if previous_rounds_context:
            messages.extend([{"role": "assistant",
                             "content": previous_rounds_context}])

        # 4. Construir y añadir el mensaje del usuario actual
        user_message_content = f"Siendo esta la ronda {ronda}, por favor genera una respuesta estructurada sobre el tópico: '{topic}'"
        if law:
            user_message_content += f" en relación con la ley '{law}'."
        else:
             user_message_content += "."

        messages.append({
            "role": "user",
            "content": user_message_content,
        })

        print(" message al agente", messages)
        # --- Realizar la llamada a la API utilizando el cliente almacenado ---
        try:
            # Usamos self.client que fue inicializado y parcheado en __init__
            generated_response: StructuredAgentResponse = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                response_model=StructuredAgentResponse,
                max_retries=3
            )
            #print("Llamada a la API exitosa y respuesta parseada.")
            return generated_response

        except ValidationError as e:
            print(f"Error de validación de Pydantic al parsear la respuesta de la API: {e}")
            if hasattr(e, 'response') and e.response and hasattr(e.response, 'text'):
                 print(f"Respuesta cruda recibida (inicio): {e.response.text[:300]}...")
            return None
        except Exception as e:
            print(e)
            print(f"Ocurrió un error inesperado al llamar a la API: {e}")
            return None

