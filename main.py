import asyncio
from debate_agents.reviewer import Reviewer
from debate_agents.agent import Agent
from debate.debate import Debate
from debate_agents.agente_liberal import AgenteLiberal
from debate_agents.agente_izquierda import AgenteIzquierda
import asyncio
if __name__ == "__main__":
    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agents = [agente_liberal, agente_izquierda]

    law = "Se debe legalizar el LSD?"

    debate = Debate(agents, 
                    law,
                    Reviewer(system_prompt = "Sos un agente especializado en análisis de debates normativos. Tu tarea es evaluar y resumir las posturas expresadas por otros agentes de distintas ideologías sobre un proyecto de ley, organizadas por eje temático (por ejemplo: equidad, constitucionalidad, impacto económico, etc.)."\
                                            "Para cada eje temático:" \
                                            "Recibís los argumentos iniciales, las contraargumentaciones y las evaluaciones finales de cada agente."\
                                            "Debés analizar y resumir qué dijo cada agente sobre ese eje, destacando sus fundamentos principales, estilo argumentativo y postura final (a favor o en contra)." \
                                            "Luego, hacés una síntesis general del debate en ese eje: señalás los puntos en común, los principales desacuerdos, si hubo cambio de postura o consenso parcial, y cuál fue la distribución del voto." \
                                            "Tu análisis debe ser claro, objetivo y técnico, sin introducir opiniones propias. Usá un tono institucional, como el de un informe parlamentario." 

                    , agents = agents),
                    obligatory_topics=["Eje Etico"],#["Eje Economico", "Eje Social", "Eje Etico"]
                    n_rounds=3
                    )
    asyncio.run(debate.run_debate())

