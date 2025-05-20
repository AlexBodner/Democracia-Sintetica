from pydantic_ai import Agent
from dotenv import load_dotenv
#import tiktoken
from pydantic import BaseModel
import openai
from pydantic_ai import Agent, RunContext
from openai import AsyncOpenAI
import os
from pydantic import BaseModel, Field, ValidationError # Clases base y excepciones de Pydantic
from openai import AsyncAzureOpenAI # Cliente asíncrono de OpenAI
import instructor # Librería para estructurar la salida del modelo
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.common_tools.tavily import tavily_search_tool
api_key_tavily = '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'

# --- Cargar variables de entorno ---
load_dotenv()
deployment_name =  os.getenv("DEPLOYMENT") 
#instruction = instruction
# Asegúrate de que estas variables existan en tu .env
api_key = os.getenv("API_KEY")
endpoint = os.getenv("ENDPOINT")
# --- Configuración de la API ---
api_version = "2024-12-01-preview"

# Crea la instancia del cliente usando los parámetros pasados al __init__
client = AsyncAzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key
)
# Aplica el parche de instructor a la instancia específica del cliente
client = instructor.patch(client) # Almacena el cliente parcheado
model = OpenAIModel(
    deployment_name,
    provider=OpenAIProvider(openai_client=client),
)
agent = Agent(model,system_prompt = 'Search Tavily for the given query and return the results.',
                tools=[tavily_search_tool(api_key_tavily)],
)

async def subfunc():
    return await agent.run('Como salio river?')
async def main():
    result = await subfunc()
    print(result.output)
    #> Paris


import asyncio
asyncio.run(main())