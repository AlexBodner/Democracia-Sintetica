
from pydantic import BaseModel, Field, ValidationError # Clases base y excepciones de Pydantic

from debate_agents.response_structures import *

from API_Model import API_Model
from dotenv import load_dotenv
import tiktoken
import http.client
import json
import requests
from logger import logger

# --- Cargar variables de entorno ---
load_dotenv()
from boilerpy3 import extractors

class Investigador:
    def __init__(
        self,
        system_prompt: str, # El mensaje del sistema que define el rol/persona del agente
        #instruction: str
        ):
        self.key = "a44bce33a7cc6234f7fd5ec6084a446260289206"

        self.api_model_agent = API_Model(
            system_prompt={"role":"system", "content": system_prompt}, 
            )

        self.conn = http.client.HTTPSConnection("google.serper.dev")


    def get_pages_info(self, consigna_de_busqueda):
        payload = json.dumps({
          "q": consigna_de_busqueda,
          "gl": "ar"
        })
        headers = {
          'X-API-KEY': self.key,
          'Content-Type': 'application/json'
        }
        self.conn.request("POST", "/search", payload, headers)
        res = self.conn.getresponse()
        response_body = res.read()
        response = json.loads(response_body)
        busqueda = ""
        cantidad_correctos = 0
        extractor = extractors.ArticleExtractor()

        for i in response["organic"]:
            if cantidad_correctos == 3:
                break
            link = i["link"]
            try:
                content = extractor.get_doc_from_url(link)
            except:
                continue

            busqueda+= f"El contenido para la pagina {link} es : \n"
            busqueda+= content.content + "\n"
            cantidad_correctos+=1
            #print(data.text)
        return busqueda
    
    
    async def busca(self, consigna_de_busqueda) :
        try:
            busqueda = self.get_pages_info( consigna_de_busqueda)
            contexto = [{
                "role": "user",
                "content": "Extrae la informacion importante sobre las siguientes paginas solicitadas para que luego los agentes\
                    políticos puedan debatir con fundamento. La idea es que extraigas datos que le puedan servir al agente \
                        para sustentar su debate y contraargumentar o fortalecer ciertas ideas. La consigna de busqueda fue" 
                        + consigna_de_busqueda + " y los contenidos devueltos fueron: "+ busqueda ,
            }]


            generated_response:InvestigadorResponse = await self.api_model_agent.call_api(
                previous_rounds_context = contexto,pydantic_response_structure=InvestigadorResponse

            )
            return generated_response.razonamiento
        except ValidationError as e:
            logger.error(f"Error de validación de Pydantic al parsear la respuesta de la API: {e}")
            if hasattr(e, 'response') and e.response and hasattr(e.response, 'text'):
                 logger.error(f"Respuesta cruda recibida (inicio): {e.response.text[:300]}...")
            return None
    