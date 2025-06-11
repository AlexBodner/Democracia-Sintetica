import asyncio
from copy import deepcopy
from output_utils.logger import new_logger
from debate.round import FirstRound, SecondRoundWithResearch, ThirdRound
import json
import os

logger = new_logger("output_utils/debate_system.log")

class DebateThreeRoundsWithResearch:
    def __init__(self, agents, law, reviewer):  
        
        self.agents = agents
        self.law = law
        self.reviewer = reviewer 
        self.rounds = [FirstRound(law), SecondRoundWithResearch(law, ""), ThirdRound(law)]
        
    

    async def run_debate(self,id = 1, output_folder = "evaluaciones"):
        #Sin intervencion del reviewer en el medio
        
        full_debate = {}
        
        research = await self.reviewer.make_deep_research(self.law)

        self.rounds[1] = SecondRoundWithResearch(self.law, research)

        context = [{"role":"user","content": f"Esto es un debate sobre la ley {self.law}. \n\
                    Van a haber 3 rondas, en la primera cada agente dara su opinion y argumentos a favor o en contra. \
                    En la segunda ronda los agentes recibiran los argumentos del resto y podran contraargumentar. En \
                    la ultima ronda cada uno recibira los argumentos y contraargumentos y podra hacer una argumentacion y conclusion final.\
                    Se espera que en todas las rondas, el agente aclare al finalizar su argumentacion si vota a favor o en contra. El voto puede\
                    cambiar ronda a ronda, pero el voto final para ver si una ley se aprueba o no es el de la ultima ronda."}, ]
        
        for round in self.rounds:
            logger.info(f"-----------------------------------Round {round.round_nr} -----------------------------------")
            result = await self.debate_round(context, round, full_debate)
            context+= result

        full_debate["Debate Completo"] = context
        logger.info("-------------------------------------------------")
        final_summary =  await self.reviewer.make_final_summary(full_debate)
        logger.info("---------------------- Final Summary------------------------")
        logger.info(final_summary)
        full_debate["Resumen final"] = final_summary
        
        logger.info("--- Full debate ---")
        logger.info(full_debate)
        os.makedirs(output_folder, exist_ok=True)

        with open(os.path.join(output_folder,f"debate_{id}.json"), "w", encoding ='utf8') as archivo:
            json.dump(full_debate, archivo, indent=4, ensure_ascii = False)
            
        return full_debate

    async def debate_round(self,prev_round_context, round, full_debate):
        
        prev_round_context.append({"role":"user",
            "content": f"Ahora arranca la ronda {round.round_nr}"}) #este es el reviewer
        
        full_debate[f"Round {round.round_nr}"] = {}
        
        round_context = []
        prev_round_context.append({"role":"user", "content": round.prompt})

        for agent in self.agents:
            logger.info(f"Agente: {agent.agent_name}")
            dar_palabra = {"role":"user", "content": f"Tiene la palabra el {agent.agent_name}"} #este es el reviewer
            agent_context = deepcopy(prev_round_context)
            agent_context.append(dar_palabra)

            agent_response = await agent.speak(agent_context)
            full_debate[f"Round {round.round_nr}"][agent.agent_name] = {"argumentacion": agent_response["content"]["argumentacion"], "voto": agent_response["content"]["voto"]}
            
            agent_context = agent_response
            agent_context['content'] = agent_context['content']['argumentacion']
            
            logger.info(agent_response['content'])
            round_context.append(dar_palabra)

            round_context.append(agent_context)
            
            
        return round_context


    def conclusiones(self,full_debate):
        return self.reviewer.make_final_summary(full_debate)
    
