import asyncio
from debate_agents.agent import Agent
from debate_agents.reviewer import AgenteReviewer
from debate.debate import DebateThreeRoundsWithResearch

from debate_agents.agente_liberal import SYSTEM_PROMPT_LIBERAL, LIBERAL_FEWSHOT_EXAMPLES
from debate_agents.agente_izquierda import SYSTEM_PROMPT_ULTRAIZQUIERDA, ULTRAIZQUIERDA_FEWSHOT_EXAMPLES
from debate_agents.agente_centro_izquierda import SYSTEM_PROMPT_UxP, UxP_FEWSHOT_EXAMPLES
from debate_agents.agente_centro_derecha import SYSTEM_PROMPT_JxC, JxC_FEWSHOT_EXAMPLES

import time
import json

def create_combinations(type_agents, proportions):
    combinations = []
    for prop in proportions:
        group = []
        for i, count in enumerate(prop):
            for j in range(count):
                if type_agents[i] == "Agente Liberal":
                    agent_instance = Agent(
                        SYSTEM_PROMPT_LIBERAL,
                        LIBERAL_FEWSHOT_EXAMPLES,
                        agent_name=f"Agente Liberal {j + 1}"
                    )
                elif type_agents[i] == "Agente Izquierda":
                    agent_instance = Agent(
                        SYSTEM_PROMPT_ULTRAIZQUIERDA,
                        ULTRAIZQUIERDA_FEWSHOT_EXAMPLES,
                        agent_name=f"Agente Izquierda {j + 1}"
                    )
                elif type_agents[i] == "AgenteUxP":
                    agent_instance = Agent(
                        SYSTEM_PROMPT_UxP,
                        UxP_FEWSHOT_EXAMPLES,
                        agent_name=f"Agente UxP {j + 1}"
                    )
                elif type_agents[i] == "AgenteJxC":
                    agent_instance = Agent(
                        SYSTEM_PROMPT_JxC,
                        JxC_FEWSHOT_EXAMPLES,
                        agent_name=f"Agente JxC {j + 1}"
                    )

                group.append(agent_instance)
        combinations.append(group)
    return combinations

if __name__ == "__main__":
    type_agents = ["Agente Liberal", "Agente Izquierda", "AgenteUxP", "AgenteJxC"]
    proportions = [
        (1, 1, 1, 0), 
        (1, 1, 0, 1),
        (1, 0, 1, 1), 
        (0, 1, 1, 1), 

        (4, 0, 0, 0), 
        (0, 4, 0, 0),
        (0, 0, 4, 0),
        (0, 0, 0, 4),
    ]

    agent_combinations = create_combinations(type_agents, proportions)

    with open("dataset/leyes.json", "r", encoding="utf-8") as f:
        leyes = json.load(f)

    for ley in leyes[:1]:
        ley_texto = ley["nombre"] + ". " + ley["resumen"]

        for i, combination in enumerate(agent_combinations):
            print(f"Simulando debate con combinación: {[agent.agent_name for agent in combination]}")
            debate = DebateThreeRoundsWithResearch(
                combination,
                ley_texto,
                AgenteReviewer,
                mock_research=False,
                use_research=True,
                ley_id= i
            )
            asyncio.run(debate.run_debate("debates_unbalanced"))
            print(f"Ley {ley['id']} terminada con combinación: {[agent.agent_name for agent in combination]}")

            time.sleep(10)