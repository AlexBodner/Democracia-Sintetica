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
        self.per_topic_summary_prompt = {"role":"user", "content":"Ahora tu tarea es " \
                    "resumir la discusion dentro del topico debatido ordenando el resumen por agente. Este resumen va a tener varias secciones:" \
                    "La primera seccion será un resumen general que mostrará  por agente que argumentos" \
                    "propuso, indicando si estuvo a favor o en contra en cada ronda. Tambien indicá si un agente cambió de opinion debido al argumento de otro" \
                    "(indicando que lo hizo cambiar de opinion)" \
                    "La segunda seccion será de conclusiones del debate, aca se esperan bullet points sobre cada agente indicando " \
                    "Puntos de acuerdo, Conflictos ideológicos principales, Divergencias argumentativas, Resultado de la votación: [x votos a favor / x en contra]" \
                    ""
                    }
        self.final_summary_prompt =  {"role":"user", "content":"Ahora tu tarea es  hacer el resumen final de la discusion para que un humano"
                    "lo pueda entender rápidamente atravesando todos los ejes. Tendrás que hacer un cierre por agente, indicando"
                    "si cambió en que topicos y debido a que argumento, por otro lado indicar su postura general respecto de la ley diciendo"
                    "si esta a favor o en contra y que ejes hicieron a esta decision."
                    }
    def give_turn(self,):
        pass

    async def make_topic_summary(self,full_topic_debate):
        context = []
        context.append(self.per_topic_summary_prompt)
        context.extend(full_topic_debate)
        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=full_topic_debate,
            pydantic_response_structure=StructuredReviewerResponse
        )
        # output = {
        #     "role": "user",
        #     "content": f"[{self.agent_name}]: " + generated_response.razonamiento,
        # }
        return generated_response.resumen
    async def make_final_summary(self, topics_sumaries: dict):
        """Creates the final summary out of the topic summaries (o lo hacemos dado toda la conversacion?)

        Args:
        Returns:
            string: The final summary.
        """
        context = []
        context.append(self.final_summary_prompt)

        for topic in topics_sumaries:
            context.append({"role" : "user", 
                           "content": f"Este es el resumen del Eje de debate {topic}: \n {topics_sumaries[topics_sumaries]}"})


        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=context,
            pydantic_response_structure= StructuredReviewerResponse
        )
        output = {
            "role": "assistant",
            "content": f"[{self.agent_name}]: " + generated_response.razonamiento,
        }
        return output    
    def search_similar_laws(self,):
        """RAG"""
        pass

    def turn_is_valid(self, turn):
        pass
