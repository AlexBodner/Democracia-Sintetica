

import asyncio

from debate_agents.agente_liberal import AgenteLiberal
from debate_agents.agente_izquierda import AgenteIzquierda
from debate_agents.agente_centro_izquierda import AgenteCentroIzquierda
from debate_agents.agente_centro_derecha import AgenteCentroDerecha
import json
from debate_agents.response_structures import  EightValuesResponse
import os
from math import sqrt
import numpy as np

response_weights = {
    "Muy de acuerdo": 1.0,
    "De acuerdo": 0.5,
    "Neutral": 0.0,
    "En desacuerdo": -0.5,
    "Muy en desacuerdo": -1.0
}

def normalize(value):
    # Convierte de [-100, 100] a [0, 100]
    return (value + 100) / 2

def euclidean_distance(p1, p2):
    return sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def obtener_ideologia(vector):
    ideologias = json.load(open("testing/8values_ideologies.json", "r", encoding="utf-8"))
    min_distance = float('inf')
    closest_ideology = None
    
    for ideologia in ideologias:
        ideologia_vector = [
            ideologia["stats"]["econ"],
            ideologia["stats"]["dipl"],
            ideologia["stats"]["govt"],
            ideologia["stats"]["scty"]
        ]
        
        dist = euclidean_distance(vector, ideologia_vector)
        
        if dist < min_distance:
            min_distance = dist
            closest_ideology = ideologia["name"]
            
    return closest_ideology

async def main(output_folder = "evaluaciones"):

    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agente_centro_izquierda = AgenteCentroIzquierda
    agente_centro_derecha = AgenteCentroDerecha

    
    agentes = [ agente_izquierda, agente_liberal, agente_centro_derecha, agente_centro_izquierda ]
    resultados = {}
    
    for agent in agentes:
        print(f"/n/nEvaluando agente: {agent.agent_name}")
        resultados[agent.agent_name] = {"econ": 0,
                                        "dipl": 0,
                                        "govt": 0,
                                        "scty": 0}
        
        with open("testing/8values.json", "r", encoding="utf-8") as f:
            preguntas =  json.load(f)
            
        for q in preguntas:
            pregunta = q["question"]
            context = [ 
                {
                    "role": "user",
                    "content": 
                                "Tu tarea es responder preguntas de un test político con las respuestas que correspondan según tu ideología política."
                                "Las preguntas solo pueden ser contestadas con: Muy de acuerdo, De acuerdo, Neutral, En desacuerdo, Muy en desacuerdo."
                                f"La pregunta es {pregunta}"
                }
            ]
            respuesta = await agent.responder_test(context, EightValuesResponse)
            
            peso = response_weights[respuesta.eleccion]
            for eje in q["effect"]:
                resultados[agent.agent_name][eje] += peso * q["effect"][eje]
                
        results_vector = np.zeros(len(resultados[agent.agent_name]))    
        
        for i, eje in enumerate(resultados[agent.agent_name]):
            resultados[agent.agent_name][eje] = normalize(resultados[agent.agent_name][eje])
            results_vector[i] = resultados[agent.agent_name][eje]
            
        print(f"Resultados para {agent.agent_name}: {obtener_ideologia(results_vector)}")
    with open(os.path.join(output_folder,f"respuestas_8values.json"), "w", encoding ='utf8') as archivo:
        json.dump(resultados, archivo, indent=4, ensure_ascii = False)
        
        
if __name__ == "__main__":
    asyncio.run(main())

