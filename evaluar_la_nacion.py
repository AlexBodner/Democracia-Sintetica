import asyncio
import random
import numpy as np
#from agenteEvaluador import AgenteEvaluador
from agente_evaluador import AgenteEvaluador
from debate_agents.agente_liberal import AgenteLiberal
from debate_agents.agente_izquierda import AgenteIzquierda
from debate_agents.agente_centro_izquierda import AgenteCentroIzquierda
from debate_agents.agente_centro_derecha import AgenteCentroDerecha
import json
from debate_agents.response_structures import  LaNacionResponse
import os


async def main(output_folder = "evaluaciones"):

    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agente_centro_izquierda = AgenteCentroIzquierda
    agente_centro_derecha = AgenteCentroDerecha

    
    agentes = [agente_liberal, agente_centro_derecha, agente_centro_izquierda, agente_izquierda]
    with open("testing/la_nacion.json", "r", encoding="utf-8") as f:
        preguntas =  json.load(f)
    respuestas  = {}
    for agente in agentes:
        respuestas[agente.agent_name] = {}

        for pregunta in preguntas: 
            context = [ 
                {
                    "role": "user",
                    "content": 
                                "Tu tarea es responder preguntas de un test político con las respuestas que correspondan según tu ideología política."
                                "Las preguntas solo pueden ser contestadas con: : Muy de acuerdo, De acuerdo, Depende, En desacuerdo, Muy en desacuerdo."
                                f"La pregunta es {pregunta['pregunta']}"
                }
            ]
            respuesta = await agente.responder_test(context, LaNacionResponse)
            respuestas[agente.agent_name][pregunta["pregunta"]] = {"respuesta": respuesta.eleccion, "razonamiento": respuesta.razonamiento}
    with open(os.path.join(output_folder,f"respuestas_la_nacion.json"), "w", encoding ='utf8') as archivo:
        json.dump(respuestas, archivo, indent=4, ensure_ascii = False)
if __name__ == "__main__":
    asyncio.run(main())

