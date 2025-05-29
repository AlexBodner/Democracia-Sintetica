import asyncio
from copy import deepcopy
from debate_agents.investigador import Investigador
from logger import logger

class Debate:
    def __init__(self, agents, law, reviewer, obligatory_topics , n_rounds = 3):
        self.agents = agents
        self.law = law
        self.reviewer = reviewer 
        self.n_rounds = n_rounds
        self.topics = obligatory_topics
        self.round_info = []
        self.investigador = Investigador("Sos un investigador que va a proveer informacion de noticias y argumentos a distintos agentes que debaten de poltiica.")
    #                                         , instruction="Cuando busques en la web, únicamente busca datos reales que sirvan para argumentar sobre la ley y no debates previos donde políticos expliciten su posición."
    
    async def run_debate(self,):
        #Sin intervencion del reviewer en el medio
        
        full_debate = {}
        topic_summaries = {}
        for topic in self.topics:
            logger.info(f"\n\n\n            -----------------------------------Topic {topic} -----------------------------------\n\n\n")
            context = [{"role":"user","content": f"Esto es un debate sobre la ley {self.law}  y el topico {topic}. Enfocate en argumentar unicamente sobre\
                        este topico. Al final va a haber un espacio para juntar las argumentaciones de varios ejes y hacer un resumen general, pero por ahora\
                        la argumentacion debe limitarse al topico {topic}.\n\
                        Van a haber 3 rondas, en la primera cada agente dara su opinion y argumentos a favor o en contra. \
                        En la segunda ronda los agentes recibiran los argumentos del resto y podran contraargumentar. En \
                        la ultima ronda cada uno recibira los argumentos y contraargumentos y podra hacer una argumentacion y conclusion final.\
                        Se espera que en todas las rondas, el agente aclare al finalizar su argumentacion si vota a favor o en contra. El voto puede\
                        cambiar ronda a ronda, pero el voto final para ver si una ley se aprueba o no es el de la ultima ronda. "}, ]
            
            for round in range(self.n_rounds):
                logger.info(f"-----------------------------------Round {round} -----------------------------------")
                result = await self.debate_round(context, round,  topic, self.law)
                context+= result
            full_debate[topic] = deepcopy(context)
            topic_summary = await self.reviewer.make_topic_summary(context)
            topic_summaries[topic] = topic_summary
            logger.info("Topic sumary")
            logger.info(topic_summary)
            
        logger.info("--- Full debate ---")
        logger.info(full_debate)
        
        full_debate["debate general"] = await self.make_closing_arguments(full_debate)
        logger.info("-------------------------------------------------")
        
    
        final_summary =  await self.reviewer.make_final_summary(topic_summaries)
        logger.info("---------------------- Final Summary------------------------")
        logger.info(final_summary)

        #print(final_summary)

        #return self.conclusiones(full_debate)


    async def debate_round(self,prev_round_context,round_nr, topic, law):
        prev_round_context.append({"role":"user",
            "content": f"Ahora arranca la ronda {round_nr}"}) #este es el reviewer
        
        round_context = []
        
        if round_nr == 0:
            prev_round_context.append({"role":"user",
                    "content": f"En esta ronda cada agente puede dar argumentos a favor o en contra del tema {topic} y la ley {law}.\
                    La argumentacion no debe ser muy extensa pero debe estar bien fundamentada, con ejemplos y referencias a la ley concisos y reales."}) 
        if round_nr == 1:
            prev_round_context.append({"role":"user",
                    "content": f"En esta ronda cada agente recibe como contexto previo los argumentos de los todos agentes de la primera ronda \
                        y van a poder contraargumentar o reafirmar su postura. Deben aclarar a que agente le estan respondiendo. Los agentes pueden intentar convencer al otro o cambiar su postura.\
                        Es importante que los agentes no se repitan y que cada uno aporte algo nuevo y deben ser fieles a su postura politica."}) 
        if round_nr == 2:
            prev_round_context.append({"role":"user",
                    "content": f"En esta ronda cada agente recibe como contexto previo los argumentos y contraargumentos de todos los \
                        agentes de la segunda ronda y van a poder hacer una argumentacion final. Pueden mantener la misma postura o cambiar de opinion \
                        dado los contraargumentos. Deben hacer un resumen final de su postura y una conclusion sobre el tema, siempre fiel a su postura politica."}) 

        for agent in self.agents:
            logger.info(f"Agente: {agent.agent_name}")
            dar_palabra = {"role":"user", "content": f"Tiene la palabra el {agent.agent_name}"} #este es el reviewer
            agent_context = deepcopy(prev_round_context)
            agent_context.append(dar_palabra)

            agent_response = await agent.speak(agent_context, topic, search = True, investigador = self.investigador)
            
            logger.info(agent_response)
            round_context.append(dar_palabra)

            round_context.append(agent_response)
            #time.sleep(61)
        return round_context


    def conclusiones(self,full_debate):
        return self.reviewer.make_final_summary(full_debate)
    
    
    async def make_closing_arguments(self, full_debate):
        closing_round = []
        logger.info("\n\n------------------- RONDA FINAL: CONCLUSIÓN GENERAL -------------------\n\n")


        for agent in self.agents:
            closing_instruction = {
            "role": "user",
            "content": (
                "A continuación, deberás realizar un argumento de cierre sobre la ley en debate, tomando en cuenta todo el intercambio anterior.\n"
                "Revisá tus posturas anteriores y las de los demás agentes, y hacé una síntesis final de tu postura general sobre la ley.\n"
                "Podés mantener o cambiar tu voto si considerás que los argumentos de otros agentes te convencieron en alguno de los ejes.\n\n"
                "Tu respuesta debe:\n"
                f"- Ser coherente con tu identidad política. Recorda que debes ser fiel a {agent.agent_name}. Junta todos tus argumentos,\
                    resumilos, y hace una conclusion final de tu voto general considerando todos los ejes.\n"
                "- Incluir referencias o menciones a los argumentos más relevantes de los distintos tópicos.\n"
                "- Terminar tu argumento con tu voto a favor o en contra, siguiendo este formato: \
                    { argumentacion:  ....,\
                      voto: ....\
                    }\n\n"
                "Este voto será considerado el definitivo."
            )
        }
            logger.info(f"Agente: {agent.agent_name}")
            agent_context = []

        
            for topic, messages in full_debate.items():
                agent_context.append({
                    "role": "user",
                    "content": f"Debate sobre el eje '{topic}':\n"
                })
                agent_context.extend(messages)

        
            agent_context.append(closing_instruction)
        
            response = await agent.speak(agent_context, topic="cierre_final", search=False)
            logger.info(response)
            closing_round.append({"agent": agent.agent_name, "response": response})

        return closing_round
