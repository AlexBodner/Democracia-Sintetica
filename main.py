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
                    Reviewer(system_prompt = "Sos el Reviewer del debate sobre el impacto de una regulación. Como tal, tu tarea es " \
                    "resumir la discusion dentro del topico debatido ordenando el resumen por agente. Este resumen va a tener varias secciones:" \
                    "La primera seccion será un resumen general que mostrará  por agente que argumentos" \
                    "propuso, indicando si estuvo a favor o en contra en cada ronda." \
                    "La segunda seccion será de conclusiones del debate, indicando si un agente cambió de opinion debido al argumento de otro" \
                    "(indicando que lo hizo cambiar de opinion) y por ultimo dira para cada agente si terminó a favor o en contra" 
                    , agents = agents),
                    obligatory_topics=["Eje Etico"],#["Eje Economico", "Eje Social", "Eje Etico"]
                    n_rounds=3
                    )
    debate.run_debate()

