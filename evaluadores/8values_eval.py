import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from debate_agents.agente_liberal import AgenteLiberal
from debate_agents.agente_izquierda import AgenteIzquierda
from debate_agents.agente_centro_izquierda import AgenteUxP
from debate_agents.agente_centro_derecha import AgenteJxC
import json
from response_structures import  EightValuesResponse
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

preguntas = json.load(open("testing/8values.json", "r", encoding="utf-8"))
max_econ = sum(abs(q["effect"].get("econ", 0)) for q in preguntas)
max_dipl = sum(abs(q["effect"].get("dipl", 0)) for q in preguntas)
max_govt = sum(abs(q["effect"].get("govt", 0)) for q in preguntas)
max_scty = sum(abs(q["effect"].get("scty", 0)) for q in preguntas)
    
def calc_score(score, max_val):
        return 100 * (max_val + score) / (2 * max_val)
    
    
    
def normalizar_resultados_js_style(resultados_ejes):

    econ_norm = calc_score(resultados_ejes.get("econ", 0), max_econ)
    dipl_norm = calc_score(resultados_ejes.get("dipl", 0), max_dipl)
    govt_norm = calc_score(resultados_ejes.get("govt", 0), max_govt)
    scty_norm = calc_score(resultados_ejes.get("scty", 0), max_scty)
    
    resultados_ejes["econ"] = econ_norm
    resultados_ejes["dipl"] = 100 - dipl_norm
    resultados_ejes["govt"] = govt_norm
    resultados_ejes["scty"] = 100 - scty_norm
    
    return np.array([econ_norm, dipl_norm, govt_norm, scty_norm])


def obtener_ideologia_por_eje(vector):
    ideologias = json.load(open("testing/8values_ideologies.json", "r", encoding="utf-8"))
    
    resultados_por_eje = {}
    ejes = ["econ", "dipl", "govt", "scty"]
    
    for eje in ejes:
        min_diff = float('inf')
        closest_ideology = None
        
        for ideologia in ideologias:
            ideologia_val = ideologia["stats"].get(eje, 0)
            diff = abs(vector[ejes.index(eje)] - ideologia_val)
            
            if diff < min_diff:
                min_diff = diff
                closest_ideology = ideologia["name"]
        
        resultados_por_eje[eje] = closest_ideology
    
    return resultados_por_eje

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


def obtener_resultado_por_eje(vector):
    
    ejes = {
            "econ": ["Equidad", "Mercado"],
            "dipl": ["Global", "Nacion"],
            "govt": ["Libertad", "Autoridad"],
            "scty": ["Progresista", "Tradicional"]
            }

    for i, eje in enumerate(ejes):
        if vector[i] >= 50:
            ejes[eje] = ejes[eje][0]  
        else:
            ejes[eje] = ejes[eje][1]

    return ejes

async def main(output_folder = "evaluaciones"):

    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agente_centro_izquierda = AgenteUxP
    agente_centro_derecha = AgenteJxC

    
    agentes = [ agente_izquierda, agente_liberal, agente_centro_derecha, agente_centro_izquierda ]
    resultados = {}
    
    with open("testing/8values.json", "r", encoding="utf-8") as f:
            preguntas =  json.load(f)
            
    respuestas_por_pregunta = {p["pregunta"]: p for p in preguntas}
    
    for agent in agentes:
        print(f"\n\nEvaluando agente: {agent.agent_name}")
        resultados[agent.agent_name] = {}
        resultados[agent.agent_name]["puntaje"] = {"econ": 0,
                                        "dipl": 0,
                                        "govt": 0,
                                        "scty": 0}
        
        for q in preguntas:
            
            pregunta = q["pregunta"]
            respuestas_por_pregunta[pregunta][agent.agent_name] = {}
            context = [ 
                {
                    "role": "user",
                    "content": 
                                "Tu tarea es responder las afirmaciones de un test político con las respuestas que correspondan según tu ideología política."
                                "Las respuestas son: Muy de acuerdo, De acuerdo, Neutral, En desacuerdo, Muy en desacuerdo."
                                f"La afirmacion es {pregunta}"
                }
            ]
            
            respuesta = await agent.responder_test(context, EightValuesResponse)
            
            respuestas_por_pregunta[pregunta][agent.agent_name]["razonamiento"] = respuesta.razonamiento
            respuestas_por_pregunta[pregunta][agent.agent_name]["eleccion"] = respuesta.eleccion
            
            peso = response_weights[respuesta.eleccion]
            for eje in q["effect"]:
                resultados[agent.agent_name]["puntaje"][eje] += peso * q["effect"][eje]
                
        results_vector = normalizar_resultados_js_style(resultados[agent.agent_name]["puntaje"])
        resultados_por_ideologia = obtener_resultado_por_eje(results_vector)
        
            
        ideologia = obtener_ideologia(results_vector)  
        resultados[agent.agent_name]["orientacion"] = resultados_por_ideologia  
    
        resultados[agent.agent_name]["ideologia"] = ideologia
        print(f"Resultados para {agent.agent_name}: {ideologia}")
        print(f"Resultados para {agent.agent_name}: {resultados_por_ideologia}")
        
        #print(f"Resultados para {agent.agent_name}: {resultados_por_ideologia}")
        
    with open(os.path.join(output_folder,f"resultados_8values.json"), "w", encoding ='utf8') as archivo:
        json.dump(resultados, archivo, indent=4, ensure_ascii = False)
    
    with open(os.path.join(output_folder,f"respuestas_8values.json"), "w", encoding ='utf8') as archivo:
        json.dump(respuestas_por_pregunta, archivo, indent=4, ensure_ascii = False)
        
if __name__ == "__main__":
    asyncio.run(main())

