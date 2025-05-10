from agents.reviewer import Reviewer
import asyncio
from copy import deepcopy
import time
class Debate:
    def __init__(self, agents, law, reviewer, obligatory_topics , n_rounds = 3):
        self.agents = agents
        self.law = law
        self.reviewer = reviewer 
        self.n_rounds = n_rounds
        self.topics = obligatory_topics
        self.round_info = []
    def run_debate(self,):
        #Sin intervencion del reviewer en el medio
        full_debate = {}
        for topic in self.topics:
            context = []
            for round in range(self.n_rounds):
                print("-----------------------------------","Round", round,"-----------------------------------")
                context+=(self.debate_round(context, round,  topic, self.law))
            full_debate[topic] = deepcopy(context)

        print("--- Full debate ---")
        print(full_debate)
        #return self.conclusiones(full_debate)
    # def inicializar_ronda (self):
    #     context_few_shots = []
    #     for agent in self.agents:
    #         context_few_shots.append()

    def debate_round(self,prev_round_context,round_nr, topic, law):
        round_context = [  {"role":"user",
            "content": "Arranca la ronda 0"} #este es el reviewer
            ]
        

        for agent in self.agents:
            print("Agente:", agent.agent_name)
            dar_palabra = {"role":"user", "content": f"Tiene la palabra el {agent.agent_name}"} #este es el reviewer
            agent_response = asyncio.run(agent.speak(prev_round_context, topic, law, round_nr))
            
            print(agent_response)
            round_context.append(dar_palabra)

            round_context.append(agent_response)
            #time.sleep(61)
        return round_context

    # def debate_round(self,prev_round_context,round_nr, topic, law):
    #     round_context = {"ronda": round_nr, "intervenciones": []} 
    #     for agent in self.agents:
    #         round_context["intervenciones"].append(asyncio.run(agent.speak(prev_round_context, topic, law, round_nr)))

    #     return round_context
    def conclusiones(self,full_debate):
        return self.reviewer.make_final_summary(full_debate)
