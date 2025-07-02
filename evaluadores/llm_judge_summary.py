from evaluadores.rubricas import RubricaVotos, RubricaPosicionFinal, RubricaArgumentos, RubricaFidelidad, RubricaImparcialidad
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluadores.judge import Judge
from evaluadores.llm_judge import judge_rubric_with_arguments, judge_rubric_with_debate_and_summary
from pydantic_utils.response_structures import EstructuraVotos, EstructuraPosicionFinal, EstructuraArgumentos, EstructuraFidelidad, EstructuraImparcialidad



def get_agent_responses(debate, agent_name, n_rounds=3):
    # esto deberia estar definido en un solo archivo e importado en todos lados.
    agent_response = ""
    for i in range(n_rounds):
        if f"Round {i}" in debate.keys():
            agent_response += f"\n\n--- Round {i} ---\n" + debate[f"Round {i}"][agent_name]["argumentacion"] + "\n"
    return agent_response


async def judge_summary(debate, ley_id, n_rounds=3,  output_folder="evaluaciones"): # FALTA COMPLETAR LAS ESTRUCTURAS Y GUARDAR LOS RESULTADOS
    """
    Juzga el final summary del debate.

    Args:
        debate (str):  path al json que contiene el debate completo y el final summary.
        ley_id (str): ID de la ley que se está debatiendo.
        n_rounds (int): Número de rondas del debate.
        output_folder (str): Carpeta donde se guardarán los resultados del juicio.

    Returns:
        dict: Resultados del juicio, incluyendo consistencia, datos y reflexividad.
    """
    results = {}
    
    with open(debate, "r", encoding="utf-8") as f:
        debate = json.load(f)
        
    for agent_name in debate[f"Round {n_rounds-1}"].keys():
        
        agent_response = get_agent_responses(debate, agent_name, n_rounds)
        voto_razonamiento, voto_puntaje = await judge_rubric_with_debate_and_summary(agent_name, RubricaVotos, debate, agent_response, EstructuraVotos)
        posicion_final_razonamiento, posicion_final_puntaje = await judge_rubric_with_debate_and_summary(agent_name,RubricaPosicionFinal, debate, agent_response,EstructuraPosicionFinal)
        argumentos_razonamiento, argumentos_puntaje = await judge_rubric_with_debate_and_summary(agent_name,RubricaArgumentos, debate, agent_response,EstructuraArgumentos)
        results[agent_name] = {
            "votos": {"razonamiento": voto_razonamiento, "puntaje": voto_puntaje},
            "posicion_final": {"razonamiento": posicion_final_razonamiento, "puntaje": posicion_final_puntaje},
            "argumentos": {"razonamiento": argumentos_razonamiento, "puntaje": argumentos_puntaje},
        }

    fidelidad_razonamiento, fidelidad_puntaje = await judge_rubric_with_debate_and_summary(None,RubricaFidelidad, debate, agent_response,EstructuraFidelidad)
    imparcialidad_razonamiento, imparcialidad_puntaje = await judge_rubric_with_debate_and_summary(None,RubricaImparcialidad, debate, agent_response,EstructuraImparcialidad)
    results["fidelidad"] = {"razonamiento": fidelidad_razonamiento, "puntaje": fidelidad_puntaje}
    results["imparcialidad"] = {"razonamiento": imparcialidad_razonamiento, "puntaje": imparcialidad_puntaje}

    print(results)
    #json.dump(results, open(f"{output_folder}/summary_judgment_results_{ley_id}.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    return results
        
async def main(debate_path, ley, n_rounds=3, output_folder="evaluaciones"):
    return await judge_summary(debate_path, ley['id'], n_rounds=n_rounds, output_folder=output_folder)
