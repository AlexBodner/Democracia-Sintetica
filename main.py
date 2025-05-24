import asyncio
from debate_agents.reviewer import Reviewer
from debate_agents.agent import Agent
from debate.debate import Debate
from debate_agents.agente_liberal import AgenteLiberal
from debate_agents.agente_izquierda import AgenteIzquierda
from debate_agents.agente_centro_izquierda import AgenteCentroIzquierda
from debate_agents.agente_centro_derecha import AgenteCentroDerecha
import asyncio
import pydantic

if __name__ == "__main__":
    
    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agente_centro_izquierda = AgenteCentroIzquierda
    agente_centro_derecha = AgenteCentroDerecha
    
    
    agents = [agente_liberal, agente_centro_derecha, agente_centro_izquierda, agente_izquierda]

    #law = "Se debe legalizar el LSD?"
    law = "Proyecto de Ley de Interrupción Voluntaria del Embarazo (IVE) 2020, Argentina. Legalizar el aborto voluntario hasta la semana 14 de gestación inclusive, y garantiza su cobertura por el sistema de salud de forma gratuita y segura. Después de la semana 14, se mantiene el derecho bajo causales."

    debate = Debate(agents, 
                    law,
                    Reviewer(system_prompt = "Sos un agente especializado en análisis de debates normativos. Tu tarea es evaluar y resumir las posturas expresadas por otros agentes de distintas ideologías sobre un proyecto de ley, organizadas por eje temático (por ejemplo: equidad, constitucionalidad, impacto económico, etc.)."\
                                            "Para cada eje temático:" \
                                            "Recibís los argumentos iniciales, las contraargumentaciones y las evaluaciones finales de cada agente."\
                                            "Debés analizar y resumir qué dijo cada agente sobre ese eje, destacando sus fundamentos principales, estilo argumentativo y postura final (a favor o en contra)." \
                                            "Luego, hacés una síntesis general del debate en ese eje: señalás los puntos en común, los principales desacuerdos, si hubo cambio de postura o consenso parcial, y cuál fue la distribución del voto." \
                                            "Tu análisis debe ser claro, objetivo y técnico, sin introducir opiniones propias. Usá un tono institucional, como el de un informe parlamentario." 

                    , agents = agents),
                    obligatory_topics=["Eje Etico","Eje Economico", "Eje Social", "Eje Etico"],
                    n_rounds=3
                    )
    
    asyncio.run(debate.run_debate())

