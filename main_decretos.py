import asyncio
from debate_agents.reviewer import Reviewer
from debate.debate import DebateDecretos
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
    CANTIDAD_DEBATES = 1
    
    agents = [agente_liberal, agente_jxc, agente_UxP, agente_izquierda]

    #law = "Se debe legalizar el LSD?"
    with open("dataset/decretos.json", "r", encoding="utf-8") as f:
        decretos = json.load(f)
        
    for decreto in decretos[:]:
        for i in range(CANTIDAD_DEBATES):
            ley_texto = decreto["nombre"] +". "+ decreto["decreto"]#"Proyecto de Ley de Interrupción Voluntaria del Embarazo (IVE) 2020, Argentina. Legalizar el aborto voluntario hasta la semana 14 de gestación inclusive, y garantiza su cobertura por el sistema de salud de forma gratuita y segura. Después de la semana 14, se mantiene el derecho bajo causales."

            debate = DebateDecretos(agents, 
                            ley_texto,
                            AgenteReviewer,
                            ley_id = decreto["id"],
                            debate_nro = i,)
            asyncio.run(debate.run_debate())
        print(f"ley {decreto['id']} terminada")
            
        time.sleep(10)