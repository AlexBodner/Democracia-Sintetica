from API_Model import API_Model
from debate_agents.response_structures import StructuredReviewerResponse
class Reviewer:# o orquestador
    def __init__(self, system_prompt, agents,):
        self.system_prompt = {"role":"system", "content":system_prompt}
        self.agents = agents
        self.api_model_agent = API_Model(
            system_prompt=self.system_prompt, 
            few_shot_examples=None
            )
        self.agent_name = "Reviewer"

        self.final_summary_prompt =  {"role":"user", "content":"Tu tarea es  hacer el resumen final del debate para que un humano"
                    "lo pueda entender rápidamente atravesando todos los ejes. Tendrás que hacer un cierre por agente, indicando"
                    "si cambió en que topicos y debido a que argumento, por otro lado indicar su postura general respecto de la ley diciendo"
                    "si esta a favor o en contra y que ejes hicieron a esta decision. Segui el siguiente formato:"
                    """ #### 🔍 Posturas por agente
                                Agente Izquierda: [resumen del argumento, crítica, respuesta, postura final, voto]
                                Agente Centro-Izquierda: [...]
                                Agente Centro-Derecha: [...]
                                Agente Derecha: [...]
                                
                                #### 🧠 Síntesis del debate
                                Puntos de acuerdo: [...]
                                Conflictos ideológicos principales: [...]
                                Divergencias argumentativas: [...]
                                Resultado de la votación: [x votos a favor / x en contra]
                    """
                    }
    def give_turn(self,):
        pass

    async def make_topic_summary(self,full_topic_debate):
        context = []
        context.extend(full_topic_debate)
        context.append(self.per_topic_summary_prompt)
        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=StructuredReviewerResponse
        )
        return generated_response.resumen
    
    
    async def make_final_summary(self, full_debate: dict):
        """Creates the final summary out of the topic summaries (o lo hacemos dado toda la conversacion?)

        Args:
        Returns:
            string: The final summary.
        """
        context = []

        context.append({"role" : "user", "content": f"El debate generado es: {full_debate['Debate']}"})
        context.append(self.final_summary_prompt)

        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=context,
            pydantic_response_structure= StructuredReviewerResponse
        )

        return  generated_response.resumen
            
    def search_similar_laws(self,):
        """RAG"""
        pass

    def turn_is_valid(self, turn):
        pass
