import json
from pydantic_utils.response_structures import JudgeConsistencia, JudgeDatos, JudgeReflexividad
from evaluadores.rubricas import RubricaConsistencia, RubricaDatos, RubricaReflexividad
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluadores.judge import Judge
from evaluadores.llm_judge import judge_rubric_with_arguments, judge_rubric_with_debate_and_summary
from pydantic_utils.response_structures import EstructuraVotos, EstructuraPosicionFinal, EstructuraArgumentos, EstructuraFidelidad, EstructuraImparcialidad


def get_agent_responses(debate, agent_name, n_rounds=3):
    agent_response = ""
    for i in range(n_rounds):
        if f"Round {i}" in debate.keys():
            agent_response += f"\n\n--- Round {i} ---\n" + debate[f"Round {i}"][agent_name]["argumentacion"] + "\n"
    return agent_response

async def judge_agent_debate(debate, agent_name, n_rounds=3):
    """
    Juzga el debate de un agente político en base a las respuestas del debate.

    Args:
        debate (dict): Diccionario que contiene el debate completo.
        agent_name (str): Nombre del agente político.
        n_rounds (int): Número de rondas del debate.

    Returns:
        dict: Resultados del juicio, incluyendo consistencia, datos y reflexividad.
    """
    agent_response = get_agent_responses(debate, agent_name, n_rounds)

    consistencia_razonamiento, consistencia_puntaje = await judge_rubric_with_arguments(agent_name, RubricaConsistencia, agent_response, JudgeConsistencia)#judgeConsistencia.judge_debate(agent_name, agent_response)
    
    datos_razonamiento, datos_puntaje = await judge_rubric_with_arguments(agent_name, RubricaDatos, agent_response, JudgeDatos)
    reflexividad_razonamiento, reflexividad_puntaje = await judge_rubric_with_arguments(agent_name, RubricaReflexividad, agent_response, JudgeReflexividad)
   
    return {
        "consistencia": {
            "razonamiento": consistencia_razonamiento,
            "puntaje": consistencia_puntaje
        },
        "datos": {
            "razonamiento": datos_razonamiento,
            "puntaje": datos_puntaje
        },
        "reflexividad": {
            "razonamiento": reflexividad_razonamiento,
            "puntaje": reflexividad_puntaje
        }
    }
        


async def judge_full_debate(debate, id, n_rounds=3, output_folder="evaluaciones"):
    """
    Juzga el debate completo de todos los agentes políticos.

    Args:
        debate (dict): Diccionario que contiene el debate completo.
        n_rounds (int): Número de rondas del debate.

    Returns:
        dict: Resultados del juicio para cada agente político.
    """
    results = {}
    with open(debate, "r", encoding="utf-8") as f:
        debate = json.load(f)
        
    for agent_name in debate[f"Round {n_rounds-1}"].keys():
        results[agent_name] = await judge_agent_debate(debate, agent_name, n_rounds)
    
    print(results)
    #json.dump(results, open(f"{output_folder}/judgment_results_{id}.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    return results


async def main(debate_path, ley, n_rounds=3, output_folder="evaluaciones"):
    return await judge_full_debate(debate_path, ley['id'], n_rounds=3, output_folder=output_folder)
