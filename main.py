from agents.reviewer import *
from agents.agent import Agent
from debate.debate import Debate
from agents.agente_liberal import AgenteLiberal
from agents.agente_izquierda import AgenteIzquierda
if __name__ == "__main__":
    agente_liberal =AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agents = [agente_liberal, agente_izquierda]

    law = "Se debe legalizar el LSD?"

    debate = Debate(agents, 
                    law,
                    Reviewer(prompt = "Sos delfi", agents = agents),
                    obligatory_topics=["Eje Etico"],#["Eje Economico", "Eje Social", "Eje Etico"]
                    n_rounds=3
                    )
    debate.run_debate()

