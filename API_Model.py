# --- Imports necesarios para las definiciones de clases ---
import asyncio # asyncio es necesario para el tipado AsyncAzureOpenAI
from typing import Any, List, Dict, Union # Tipado para métodos y atributos

from pydantic import BaseModel, Field, ValidationError # Clases base y excepciones de Pydantic
from openai import AsyncAzureOpenAI # Cliente asíncrono de OpenAI
import instructor # Librería para estructurar la salida del modelo

import os
from debate_agents.response_structures import StructuredAgentResponse
from dotenv import load_dotenv
#import tiktoken
from pydantic import BaseModel
import openai
from pydantic_ai import Agent, RunContext
from openai import AsyncOpenAI
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
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
        self.api_key = os.getenv("API_KEY")
        self.endpoint = os.getenv("ENDPOINT")
        # --- Configuración de la API ---
        self.api_version = "2024-12-01-preview"
        try:
            # Crea la instancia del cliente usando los parámetros pasados al __init__
            self.client = AsyncAzureOpenAI(
                api_version=self.api_version,
                azure_endpoint=self.endpoint,
                api_key=self.api_key
            )
            # Aplica el parche de instructor a la instancia específica del cliente
            self.client = instructor.patch(self.client) # Almacena el cliente parcheado

        except Exception as e:
            raise ValueError(f"ERROR al inicializar o parchear el cliente OpenAI: {e}") from e



    async def call_api(
        self,
        previous_rounds_context: List[Dict[str, str]] = None,
        pydantic_response_structure=StructuredAgentResponse
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
        # --- Construir la lista completa de mensajes para enviar a la API ---
        messages = [self.system_prompt] # 1. Empezamos con el mensaje del sistema

        # 2. Añadir few-shot examples (si existen)
        if self.few_shot_examples:
            messages.extend(self.few_shot_examples)

        # 3. Añadir contexto de rondas previas (si existe)
        if previous_rounds_context:
            messages.extend(previous_rounds_context)

        #enc = tiktoken.encoding_for_model("gpt-4o-mini")

        # --- Realizar la llamada a la API utilizando el cliente almacenado ---
        try:
            # Validar que todos los mensajes tengan la clave "content"
            for message in messages:
                if "content" not in message:
                    raise ValueError(f"El mensaje no contiene la clave 'content': {message}")

            # Realizar la llamada al modelo
            generated_response: pydantic_response_structure = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                response_model=pydantic_response_structure,
                max_retries=3,
                seed=42
            )
            return generated_response
        except ValidationError as e:
            print(f"Error de validación de Pydantic al parsear la respuesta de la API: {e}")
            if hasattr(e, 'response') and e.response and hasattr(e.response, 'text'):
                 print(f"Respuesta cruda recibida (inicio): {e.response.text[:300]}...")
            return None

