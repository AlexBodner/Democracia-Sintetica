import asyncio
from debate_agents.reviewer import Reviewer
from debate.debate import DebateThreeRoundsWithResearch
from debate_agents.agente_liberal import AgenteLiberal
from debate_agents.agente_izquierda import AgenteIzquierda
from debate_agents.agente_centro_izquierda import AgenteUxP
from debate_agents.agente_centro_derecha import AgenteJxC
import asyncio
import json
if __name__ == "__main__":
    
    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agente_UxP = AgenteUxP
    agente_jxc = AgenteJxC
    
    
    agents = [agente_liberal, agente_jxc, agente_UxP, agente_izquierda]

    #law = "Se debe legalizar el LSD?"
    with open("testing/leyes_limpias.json", "r", encoding="utf-8") as f:
        leyes = json.load(f)
    for ley in leyes:
        ley_texto = ley["nombre"] +". "+ ley["resumen"]#"Proyecto de Ley de Interrupción Voluntaria del Embarazo (IVE) 2020, Argentina. Legalizar el aborto voluntario hasta la semana 14 de gestación inclusive, y garantiza su cobertura por el sistema de salud de forma gratuita y segura. Después de la semana 14, se mantiene el derecho bajo causales."

        debate = DebateThreeRoundsWithResearch(agents, 
                        ley_texto,
                        Reviewer(system_prompt = "Sos un agente especializado en análisis de debates normativos. Tu tarea es evaluar y resumir las posturas expresadas por otros agentes de distintas ideologías sobre un proyecto de ley, organizadas por eje temático (por ejemplo: equidad, constitucionalidad, impacto económico, etc.)."\
                                                "Para cada eje temático:" \
                                                "Recibís los argumentos iniciales, las contraargumentaciones y las evaluaciones finales de cada agente."\
                                                "Debés analizar y resumir qué dijo cada agente sobre ese eje, destacando sus fundamentos principales, estilo argumentativo y postura final (a favor o en contra)." \
                                                "Luego, hacés una síntesis general del debate en ese eje: señalás los puntos en común, los principales desacuerdos, si hubo cambio de postura o consenso parcial, y cuál fue la distribución del voto." \
                                                "Tu análisis debe ser claro, objetivo y técnico, sin introducir opiniones propias. Usá un tono institucional, como el de un informe parlamentario." 
                        , agents = agents),
                        mock_research= False)
        asyncio.run(debate.run_debate(id = ley["id"]))
        print(f"ley {ley['id']} terminada")
