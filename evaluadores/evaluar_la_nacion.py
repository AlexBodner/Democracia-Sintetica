import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from debate_agents.agente_liberal import AgenteLiberal
from debate_agents.agente_izquierda import AgenteIzquierda
from debate_agents.agente_centro_izquierda import AgenteUxP
from debate_agents.agente_centro_derecha import AgenteJxC
from debate_agents.reviewer import AgenteReviewer
from debate_agents.agente_base import AgenteBase, BaseAgent
from pydantic_utils.API_Model import API_Model
import json
from pydantic_utils.response_structures import  LaNacionResponse
import os

import json
import os
import asyncio
from collections import Counter

async def main(output_folder="evaluaciones", output_file="respuestas_la_nacion.json"):
    
    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agente_centro_izquierda = AgenteUxP
    agente_centro_derecha = AgenteJxC
    agente_reviewer = AgenteReviewer
    agente_base =  AgenteBase
    agente_turbo = BaseAgent(name="Agente Turbo")
    agente_grok = BaseAgent(name="Agente Grok")
    agente_DeepSeek = BaseAgent(name="Agente DeepSeek")

    #agentes = [agente_base, agente_reviewer, agente_liberal, agente_centro_derecha, agente_centro_izquierda, agente_izquierda]
    agentes = [agente_DeepSeek]

    with open("testing/la_nacion.json", "r", encoding="utf-8") as f:
        preguntas = json.load(f)

    respuestas_acumuladas = {}

    for agente in agentes:
        respuestas_acumuladas[agente.agent_name] = {}
        for pregunta in preguntas:
            respuestas_acumuladas[agente.agent_name][pregunta["pregunta"]] = {"respuestas": [], "razonamientos": []}


    for i in range(5):
        print(i)
        for agente in agentes:
            for pregunta in preguntas:
                context = [
                    {
                        "role": "user",
                        "content": (
                            "Tu tarea es responder preguntas de un test político con las respuestas que correspondan según tu ideología política. "
                            "Las preguntas solo pueden ser contestadas con: Muy de acuerdo, De acuerdo, Depende, En desacuerdo, Muy en desacuerdo. "
                            f"La pregunta es: {pregunta['pregunta']}"
                        )
                    }
                ]
                respuesta = await agente.responder_test(context, LaNacionResponse)
                respuestas_acumuladas[agente.agent_name][pregunta["pregunta"]]["respuestas"].append(respuesta.eleccion)
                respuestas_acumuladas[agente.agent_name][pregunta["pregunta"]]["razonamientos"].append(respuesta.razonamiento)

    respuestas_finales = {}

    for agente_name, preguntas_dict in respuestas_acumuladas.items():
        respuestas_finales[agente_name] = {}
        for pregunta_texto, data in preguntas_dict.items():
            
            resp_counter = Counter(data["respuestas"])
            respuesta_mas_comun = resp_counter.most_common(1)[0][0]

            razonamientos_filtrados = [
                razon for resp, razon in zip(data["respuestas"], data["razonamientos"])
                if resp == respuesta_mas_comun
            ]


            razonamiento_mas_comun = razonamientos_filtrados[0]
            respuestas_finales[agente_name][pregunta_texto] = {
                "respuesta": respuesta_mas_comun,
                "razonamiento": razonamiento_mas_comun
            }

    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, output_file), "w", encoding='utf8') as archivo:
        json.dump(respuestas_finales, archivo, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(main(output_file="respuestas_la_nacion_agente_DeepSeek.json"))

"""

async def main(output_folder = "evaluaciones"):

    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agente_centro_izquierda = AgenteUxP
    agente_centro_derecha = AgenteJxC
    agente_reviewer = AgenteReviewer

    
    agentes = [agente_reviewer, agente_liberal, agente_centro_derecha, agente_centro_izquierda, agente_izquierda]
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
    with open(os.path.join(output_folder,f"respuestas_la_nacion_izq.json"), "w", encoding ='utf8') as archivo:
        json.dump(respuestas, archivo, indent=4, ensure_ascii = False)
        
if __name__ == "__main__":
    asyncio.run(main())

"""