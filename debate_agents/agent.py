from API_Model import API_Model
from debate_agents.response_structures import *
from  copy import deepcopy
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
                previous_rounds_context = prev_round_context+ [{"role":"user",
                                                                "content":"Tienes la posibilidad de buscar en la web, si tienes la necesidad de buscar mas argumentos,"
                                                                " respaldar alguno de los tuyos con datos o quieres verificar el de otro agente, puedes hacerlo completando el campo 'queres_buscar'"
                                                                "y el campo 'consigna_de_busqueda' con lo que quieras que el Agente Investigador busque por ti."}], 
                                                                pydantic_response_structure = SearchAgentResponse
            )
            print("search_response",search_response)
            if search_response.queres_buscar:
                contexto = deepcopy(prev_round_context)
                busqueda =await investigador.busca(search_response.consigna_de_busqueda)
                contexto.append({
                    "role": "user",
                    "content": f"Los resultados de la investigacion sobre: {search_response.consigna_de_busqueda} son: {busqueda}" ,
                })

                print("-------------------Busqueda de google------------------------------")
                print(busqueda)
                print("-----------------------------------------------------------")
                generated_response = await self.api_model_agent.call_api(
                    previous_rounds_context = contexto
                )
                razonamiento = generated_response.razonamiento
            else:
                razonamiento = search_response.razonamiento
        else:
            generated_response = await self.api_model_agent.call_api(
                previous_rounds_context=prev_round_context
            )
            razonamiento = generated_response.razonamiento
        output = {
            "role": "assistant",
            "content": f"[{self.agent_name}]: " + razonamiento,
        }
        return output

    def vote_topic(self, topic, summary):
        pass
    
