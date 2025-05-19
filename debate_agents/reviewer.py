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
        self.per_topic_summary_prompt = {"role":"user", "content":"""Sos un agente especializado en análisis de debates normativos. Tu tarea es evaluar y resumir las posturas expresadas por otros agentes de distintas ideologías sobre un proyecto de ley, organizadas por eje temático (por ejemplo: equidad, constitucionalidad, impacto económico, etc.).

                                        Para cada eje temático:
                                        Recibís los argumentos iniciales, las contraargumentaciones y las evaluaciones finales de cada agente.
                                        Debés analizar y resumir qué dijo cada agente sobre ese eje, destacando sus fundamentos principales, estilo argumentativo y postura final (a favor o en contra).
                                        Luego, hacés una síntesis general del debate en ese eje: señalás los puntos en común, los principales desacuerdos, si hubo cambio de postura o consenso parcial, y cuál fue la distribución del voto.

                                        Tu análisis debe ser claro, objetivo y técnico, sin introducir opiniones propias. Usá un tono institucional, como el de un informe parlamentario.

                                        Estructura esperada de tu respuesta:

                                        Eje: [nombre del eje]
                                        #### 🔍 Posturas por agente
                                        Agente Izquierda: [resumen del argumento, crítica, respuesta, postura final, voto]
                                        Agente Centro-Izquierda: [...]
                                        Agente Centro-Derecha: [...]
                                        Agente Derecha: [...]

                                        #### 🧠 Síntesis del debate
                                        Puntos de acuerdo: [...]
                                        Conflictos ideológicos principales: [...]
                                        Divergencias argumentativas: [...]
                                        Resultado de la votación: [x votos a favor / x en contra]

                                        Al final del proceso, vas a integrar todos los resúmenes por eje en un informe general."""
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
        context.extend(full_topic_debate)
        context.append(self.per_topic_summary_prompt)
        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=StructuredReviewerResponse
        )
        return generated_response.resumen
    async def make_final_summary(self, topics_sumaries: dict):
        """Creates the final summary out of the topic summaries (o lo hacemos dado toda la conversacion?)

        Args:
        Returns:
            string: The final summary.
        """
        context = []
        

        for topic in topics_sumaries:
            context.append({"role" : "user", 
                           "content": f"Este es el resumen del Eje de debate {topic}: \n {topics_sumaries[topic]}"})

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
