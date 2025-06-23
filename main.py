import asyncio
from debate_agents.reviewer import Reviewer
from debate.debate import DebateThreeRoundsWithResearch
from debate_agents.agente_liberal import AgenteLiberal
from debate_agents.agente_izquierda import AgenteIzquierda
from debate_agents.agente_centro_izquierda import AgenteUxP
from debate_agents.agente_centro_derecha import AgenteJxC
from debate_agents.reviewer import AgenteReviewer
import asyncio
import time
import json
if __name__ == "__main__":
    
    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agente_UxP = AgenteUxP
    agente_jxc = AgenteJxC
    CANTIDAD_DEBATES = 5
    
    agents = [agente_liberal, agente_jxc, agente_UxP, agente_izquierda]

    #law = "Se debe legalizar el LSD?"
    with open("testing/leyes.json", "r", encoding="utf-8") as f:
        leyes = json.load(f)
        
    for ley in leyes[:]:
        for i in range(CANTIDAD_DEBATES):
            ley_texto = ley["nombre"] +". "+ ley["resumen"]#"Proyecto de Ley de Interrupción Voluntaria del Embarazo (IVE) 2020, Argentina. Legalizar el aborto voluntario hasta la semana 14 de gestación inclusive, y garantiza su cobertura por el sistema de salud de forma gratuita y segura. Después de la semana 14, se mantiene el derecho bajo causales."

            debate = DebateThreeRoundsWithResearch(agents, 
                            ley_texto,
                            AgenteReviewer,
                            mock_research= True,
                            use_research=True,
                            ley_id = ley["id"],
                            debate_nro = i,)
            asyncio.run(debate.run_debate())
        print(f"ley {ley['id']} terminada")
            
        time.sleep(10)