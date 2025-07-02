from pydantic_utils.API_Model import API_Model
from pydantic_utils.response_structures import StructuredReviewerResponse, DeepResearchQuery, RepreguntaResponse, ProposalsList
from researcher.deepresearch import deepresearch

class Reviewer:# o orquestador
    def __init__(self, system_prompt, agents = None,):
        self.system_prompt = {"role":"system", "content": system_prompt}
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
        self.separate_proposals_prompt = {"role":"user", "content":"Vas a recibir parafos con diferentes propuestas para modificar una ley. Tu tarea es analizar esos parrafos y generar una lista con las propuestas sin repetir"}
    def give_turn(self,):
        pass
    async def responder_pregunta(self, preguntas):
        context = []
        #  Como especialista en Geopolitica, ciencias sociales y economía,
        context.append({"role" : "user", "content":  f"""\
            Tu tarea es redactar una consigna de búsqueda exhaustiva y bien estructurada para que un Agente especializado realice una investigación profunda sobre el tema de desregulación indicado.

            El objetivo de esta investigación es proporcionar a los legisladores de la República Argentina un panorama completo que les permita comprender a fondo el contexto, los antecedentes, los impactos potenciales y los casos comparables a nivel nacional e internacional.

            La desregulación a debatir es: {self.ley}

            La consigna debe incluir:
            - Qué aspectos investigar (económicos, sociales, legales, ambientales, etc.)
            - Qué fuentes consultar (académicas, gubernamentales, medios especializados, organismos internacionales, informes técnicos)
            - Qué tipo de datos buscar (estadísticas, estudios de impacto, experiencias previas, legislación comparada, opinión de expertos)
            - Qué países o regiones podrían ofrecer casos relevantes para comparar
            - Posibles efectos positivos y negativos reportados
            - Actores clave involucrados (empresas, sindicatos, ONGs, organismos públicos)

            La búsqueda debe enfocarse en brindar insumos que enriquezcan el debate parlamentario, ofreciendo tanto evidencia empírica como argumentos teóricos.

            Ahora redactá una consigna clara, detallada y orientada a la acción para el Agente de investigación, que incluya todos estos elementos.
            """})
        context.append({"role":"user", "content":"Para que el investigador finalice su investigación,"\
            f" debe responder a las siguientes preguntas que le ha hecho:{preguntas}"})
                
        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=RepreguntaResponse
        )
        return generated_response.respuestas
    
    async def make_topic_summary(self,full_topic_debate):
        context = []
        context.extend(full_topic_debate)
        context.append(self.per_topic_summary_prompt)
        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=StructuredReviewerResponse
        )
        return generated_response.resumen
    
    async def responder_test(self, context, response_structure):
        generated_response = await self.api_model_agent.call_api(
                previous_rounds_context=context,
                pydantic_response_structure = response_structure
            )
        return generated_response
    
    async def make_deep_research(self, ley, mock=True, id=1):
        context = []
        
        context.append({"role" : "user", "content":  f"""\
            Tu tarea es redactar una consigna de búsqueda exhaustiva y bien estructurada para que un Agente especializado realice una investigación profunda sobre el tema de desregulación indicado.
            El objetivo de esta investigación es proporcionar a los legisladores de la República Argentina un panorama completo que les permita comprender a fondo el contexto, los antecedentes, los impactos potenciales y los casos comparables a nivel nacional e internacional.
            La desregulación a debatir es: {ley}

            La consigna debe incluir:
            - Qué aspectos investigar (económicos, sociales, legales, ambientales, etc.)
            - Qué fuentes consultar (académicas, gubernamentales, medios especializados, organismos internacionales, informes técnicos)
            - Qué tipo de datos buscar (estadísticas, estudios de impacto, experiencias previas, legislación comparada, opinión de expertos)
            - Qué países o regiones podrían ofrecer casos relevantes para comparar
            - Posibles efectos positivos y negativos reportados
            - Actores clave involucrados (empresas, sindicatos, ONGs, organismos públicos)

            La búsqueda debe enfocarse en brindar insumos que enriquezcan el debate parlamentario, ofreciendo tanto evidencia empírica como argumentos teóricos.
            Es fundamental que la consigna de busqueda pida estadisticas, datos concretos y estudios de caso que permitan a los legisladores evaluar los pros y contras de la desregulación en cuestión con evidencia sólida y objetiva.
            Ahora redactá una consigna clara, detallada y orientada a la acción para el Agente de investigación, que incluya todos estos elementos.
            """})
        self.ley = ley
        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=context,
            pydantic_response_structure= DeepResearchQuery
        )
        if mock == False:
            report, questions_and_answers = await deepresearch(generated_response.consigna_de_busqueda,self)
            # Save final report
            with open(f"researchs/{id}.txt",'w', encoding='utf-8') as f:
                f.write(report)
        else:
            with open(f"researchs/{id}.txt", "r") as archivo:
                report = archivo.read()
            questions_and_answers = ""
        return  report, questions_and_answers
    
    
    async def make_final_summary(self, full_debate: dict):
        """Creates the final summary out of the topic summaries (o lo hacemos dado toda la conversacion?)

        Args:
        Returns:
            string: The final summary.
        """
        context = []

        context.append({"role" : "user", "content": f"El debate generado es: {full_debate['Debate Completo']}"})
        context.append(self.final_summary_prompt)

        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=context,
            pydantic_response_structure= StructuredReviewerResponse
        )

        return  generated_response.resumen
    
    async def separar_propuestas(self, parrafo_propuestas):
        
        context = []
        context.append({"role" : "user", "content": f"El debate generado es: {parrafo_propuestas}"})
        context.append(self.separate_proposals_prompt)

        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=context,
            pydantic_response_structure= ProposalsList
        )

        return generated_response.propuestas
                
AgenteReviewer = Reviewer(system_prompt =  (
        "Sos un agente especializado en el análisis técnico de debates legislativos. "
        "Tu tarea consiste en evaluar y sintetizar las posturas expresadas por diferentes agentes políticos en relación con un proyecto de ley, organizando el análisis por ejes temáticos relevantes "
        "(por ejemplo: equidad, constitucionalidad, impacto económico, entre otros). "
        "\n\nPara cada eje temático:\n"
        "- Recibirás los argumentos iniciales, las contraargumentaciones y las conclusiones finales formuladas por cada agente.\n"
        "- Debés resumir qué planteó cada agente respecto de ese eje, destacando sus fundamentos principales, estilo argumentativo (por ejemplo: técnico, ideológico, pragmático) y su postura final (a favor o en contra de la ley).\n"
        "- Luego, elaborá una síntesis general del debate en ese eje: indicá los principales puntos de acuerdo y desacuerdo, señalá si algún agente modificó su postura, si surgieron consensos parciales y cuál fue la distribución final de los votos.\n\n"
        "El análisis debe ser claro, preciso y objetivo, sin incorporar valoraciones personales. Adoptá un tono institucional y técnico, propio de un informe parlamentario oficial.")
        , agents = None)