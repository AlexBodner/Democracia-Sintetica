from agents.reviewer import *
from agents.agent import Agent
from debate import Debate


if __name__ == "__main__":
    agente_liberal = Agent("Sos Milei")
    agente_izquierda = Agent("Sos Del CAño")
    agents = [agente_liberal, agente_izquierda]

    law = "Queremos legalizarla"

    debate = Debate(agents, 
                    law,
                    Reviewer(prompt = "Sos delfi", agents = agents),
                    n_rounds=3
                    )
    debate.run_debate()

