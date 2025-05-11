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
            context = [{"role":"user","content": f"Esto es un debate sobre la ley {self.law}  y el topico {topic}.\
                        Van a haber 3 rondas, en la primera cada agente dara su opinion y argumentos a favor o en contra. \
                        En la segunda ronda los agentes recibiran los argumentos del resto y podran contraargumentar. En \
                        la ultima ronda cada uno recibira los argumentos y contraargumentos y podra hacer una argumentacion y conclusion final."}, ]
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
        prev_round_context.append({"role":"user",
            "content": f"Ahora arranca la ronda {round_nr}"}) #este es el reviewer
        
        round_context = []
        
        if round_nr == 0:
            prev_round_context.append({"role":"user",
                    "content": f"En esta ronda cada aagente puede dar argumentos a favor o en contra del tema {topic} y la ley {law}.\
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
