import asyncio
from copy import deepcopy
from output_utils.logger import new_logger
from debate.round import FirstRound, SecondRoundWithResearch, ThirdRound
import json
import os

logger = new_logger("output_utils/debate_system.log")

class DebateThreeRoundsWithResearch:
    
    async def __init__(self, agents, law, reviewer, mock_research = False):  
        
        self.agents = agents
        self.law = law
        self.reviewer = reviewer 
        self.research = await self.reviewer.make_deep_research(self.law, mock = self.mock_research, id = id)
        self.rounds = [FirstRound(law), SecondRoundWithResearch(law, self.research), ThirdRound(law)]
        self.mock_research = mock_research 

    async def run_debate(self,id = 1, output_folder = "evaluaciones"):

        full_debate = {}
        
        #research = await self.reviewer.make_deep_research(self.law, mock = self.mock_research, id = id)
        #self.rounds[1] = SecondRoundWithResearch(self.law, research)

        context = [{"role":"user",
                    "content":  f"""Este es un debate simulado entre agentes políticos argentinos sobre la ley {self.law}.
                                    El debate constará de tres rondas:
                                    1. **Primera ronda**: Cada agente expresará su postura inicial, presentando argumentos a favor o en contra de la ley.
                                    2. **Segunda ronda**: Los agentes recibirán un informe con datos (provenientes de búsquedas en Google) y los argumentos expuestos por el resto de los agentes. Con esta información, podrán formular contraargumentos o reforzar su postura inicial.
                                    3. **Tercera ronda**: Los agentes recibirán tanto los argumentos iniciales como los contraargumentos de las rondas previas. En base a ello, deberán realizar una argumentación final y emitir una conclusión definitiva.
                                    En cada ronda, al finalizar su exposición, cada agente deberá explicitar su voto (a favor o en contra de la ley). El voto puede modificarse de ronda a ronda, pero el voto que determina la aprobación o rechazo de la ley será el emitido en la última ronda."""
                                    }]

        
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
            "content": f"Ahora arranca la ronda {round.round_nr}"})
        
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
    
