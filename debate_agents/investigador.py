# --- Imports necesarios para las definiciones de clases ---
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
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
# --- Clase API_Model ---
class Investigador:
    def __init__(
        self,
        system_prompt: str, # El mensaje del sistema que define el rol/persona del agente
        instruction: str
    ):

        self.deployment_name =  os.getenv("DEPLOYMENT") 
        self.system_prompt = system_prompt #"Cuando busques en la web, únicamente busca datos reales que sirvan para argumentar sobre la ley y no debates previos donde políticos expliciten su posición."
        self.instruction = instruction
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
            model = OpenAIModel(
                self.deployment_name,
                provider=OpenAIProvider(openai_client=self.client),
            )
            self.agent = Agent(model, system_prompt = self.system_prompt, tools=[duckduckgo_search_tool()],
                           instructions = self.instruction)
        except Exception as e:
            raise ValueError(f"ERROR al inicializar o parchear el cliente OpenAI: {e}") from e


    async def busca(
        self, consigna_de_busqueda
    ) :
        try:
            result = await self.agent.run(self, "Busca en google lo siguiente:"+ consigna_de_busqueda)
            #print("Structured Result:", result.output)
            return result.output

        except ValidationError as e:
            print(f"Error de validación de Pydantic al parsear la respuesta de la API: {e}")
            if hasattr(e, 'response') and e.response and hasattr(e.response, 'text'):
                 print(f"Respuesta cruda recibida (inicio): {e.response.text[:300]}...")
            return None