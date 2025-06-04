import asyncio
import random
import numpy as np
#from agenteEvaluador import AgenteEvaluador
from agente_evaluador import AgenteEvaluador
from debate_agents.agente_liberal import AgenteLiberal
from debate_agents.agente_izquierda import AgenteIzquierda
from debate_agents.agente_centro_izquierda import AgenteCentroIzquierda
from debate_agents.agente_centro_derecha import AgenteCentroDerecha
import os
import json







def set_seed(seed: int):
    """
    Establece una semilla global para garantizar reproducibilidad.
    """
    random.seed(seed)
    np.random.seed(seed)
    
def format_system_prompt(agent):
    return {"role": "system",
        "content": """Sos un evaluador experto en política argentina. Tu tarea es comparar dos debates políticos sobre una misma ley: uno generado por agentes de IA ideológicos, y otro basado en argumentos reales utilizados por representantes de partidos políticos argentinos.

        Debés analizar qué tan similares son ambos debates en cuanto a:
        - Posturas generales adoptadas por cada ideología (izquierda, centro-izquierda, centro-derecha, derecha).
        - Argumentos esgrimidos (legales, éticos, económicos, etc.). 
        - Nivel de polarización y alineamiento político.
        - Tono y fundamentos de cada postura.

        Además, es fundamental que evalúes la fidelidad ideológica de los agentes. Cada agente debe seguir estrictamente las ideologías del partido político que representa:
        En este caso analizaras el comportamiento del agente """ + agent.agent_name + ", cuyo prompt de sistema es: " + agent.sys_prompt["content"]+ 
        """Respondé con:
        1. Un análisis detallado por agente:
        - Qué dijo el agente en el debate sintético.
        - Qué postura real se esperaba del agente según su ideología.
        - Similitudes y diferencias entre el debate sintético y el debate real.
        - Puntaje de similitud para el agente.

        2. Una explicación clara, global, del razonamiento comparativo (qué coincidencias encontraste, qué diferencias, si alguna ideología cambió de posición, etc.).
        3. Un puntaje global del debate, basado en la fidelidad ideológica y la similitud general.

        Formato de salida esperado:
        {{
            "debate_sintetico": "...",
            "postura_real": "...",
            "similitudes": "...",
            "diferencias": "...",
            "puntaje": ...
        }}
        """.strip()
    }
    
agente2postura = {
    "Agente Liberal": "derecha_lla_pro_otros",
    "Agente de Centro Derecha": "centro_derecha_jxc_otros",
    "Agente de Centro Izquierda": "centro_izquierda_fdt_otros",
    "Agente de Izquierda": "izquierda_fit"
}


async def main(output_folder = "evaluaciones"):
    set_seed(42) 

    agente_liberal = AgenteLiberal
    agente_izquierda = AgenteIzquierda
    agente_centro_izquierda = AgenteCentroIzquierda
    agente_centro_derecha = AgenteCentroDerecha

    
    agentes = [agente_liberal, agente_centro_derecha, agente_centro_izquierda, agente_izquierda]

    with open("testing/leyes_limpias.json", "r", encoding="utf-8") as f:
        leyes = json.load(f)
    for ley in leyes:
        #with open('debate_{ley["id"]}.json', 'r') as file:
        with open('evaluaciones/debate_1.json', 'r', encoding="utf-8") as file:
            debate_sintetico_por_agente = json.load(file)
        puntaje_final = 0 

        for agente in agentes:
            evaluador = AgenteEvaluador(system_prompt=format_system_prompt(agente))
            evaluacion = await evaluador.evaluar_debate(debate_sintetico_por_agente, agente.agent_name,
                                                    ley['posturas'][agente2postura[agente.agent_name]]["argumentacion"], n_rounds = 3 , id=  ley["id"])
            
            print(f"PRUEBA DELFI: {agente.agent_name}: {evaluador.evaluar_votacion(debate_sintetico_por_agente, agente.agent_name, ley['id'])}")
            print(evaluacion)
            puntaje_final+=evaluacion.puntaje
            argumentos_encontrados = await evaluador.contar_argumentos(debate_sintetico_por_agente, agente.agent_name,
                                 ley['posturas'][agente2postura[agente.agent_name]]["argumentacion"], n_rounds=3, )
        puntaje_final/=len(agentes)


        resultado = f"\nPuntaje final promedio: {puntaje_final}\n"
        resultado += f"{'-'*80}\n"
        with open(os.path.join(output_folder,f"evaluador_{ley['id']}.log"), "a+", encoding="utf-8") as f:
            f.write(resultado)
        break # PARA SOLO HACER CON LA PRIMERA
    
    
    
if __name__ == "__main__":
    asyncio.run(main())

