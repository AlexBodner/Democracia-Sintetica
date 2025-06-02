from API_Model import API_Model
from debate_agents.response_structures import *
from  copy import deepcopy
from logger import logger

class Agent:
    def __init__(self, sys_prompt, few_shot_ex, agent_name):
        self.sys_prompt = sys_prompt
        self.few_shot_ex = few_shot_ex
        self.api_model_agent = API_Model(
            system_prompt=sys_prompt, 
            few_shot_examples=few_shot_ex
            )
        self.agent_name = agent_name

    async def speak(self, prev_round_context, search = False, investigador =None):
        
        if search:
            search_response: SearchAgentResponse = await self.api_model_agent.call_api(
                previous_rounds_context = prev_round_context + [{"role":"user",
                                                                "content":f"Tienes la posibilidad de buscar en la web, si tienes la necesidad de buscar mas argumentos."
                                                                " respaldar alguno de los tuyos con datos o quieres verificar el de otro agente, puedes hacerlo completando el campo 'queres_buscar'"
                                                                "y el campo 'consigna_de_busqueda' con lo que quieras que el Agente Investigador busque por ti."
                                                                "Podes buscar leyes similares que se hayan aplicado en uno o varios paises y sus consecuencias,"
                                                                "o buscar datos estadísticos o casos que respalden tus argumentos. Asegurate de no buscar"
                                                                " información que ya tengas en el contexto de la conversación ni repetir busquedas."}], 
                                                                pydantic_response_structure = SearchAgentResponse
            )
            if search_response.queres_buscar:
                logger.info(f"\n\n       Consigna de busqueda: {search_response.consigna_de_busqueda}\n\n")
                contexto = deepcopy(prev_round_context)
                busqueda =await investigador.busca(search_response.consigna_de_busqueda)
                contexto.append({
                    "role": "user", 
                    "content": f"Los resultados de tu investigación sobre: {search_response.consigna_de_busqueda} son: {busqueda}" ,
                })

                logger.info("------------------- Búsqueda de Google ------------------------------")
                logger.info(busqueda)
                logger.info("---------------------------------------------------------------------")
                generated_response = await self.api_model_agent.call_api(
                    previous_rounds_context = contexto
                )
                razonamiento = f"Investigué sobre: {search_response.consigna_de_busqueda} y los resultados obtenidos son: \n {busqueda} \n\n Mi argumentación es:" + generated_response.razonamiento 
            else:
                razonamiento = search_response.razonamiento
        else:
            generated_response = await self.api_model_agent.call_api(
                previous_rounds_context=prev_round_context
            )
            razonamiento = generated_response.razonamiento
        output = {
            "role": "assistant",
            "content": f"[{self.agent_name}]: " + f"{razonamiento}",
        }
        return output

    def vote_topic(self, topic, summary):
        pass

    def get_system_prompt(self):
        return self.sys_prompt