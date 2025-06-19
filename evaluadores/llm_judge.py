
from evaluadores.judge import Judge


def get_agent_responses(debate, agent_name, n_rounds=3):
    agent_response = ""
    for i in range(n_rounds):
        if f"Round {i}" in debate.keys():
            agent_response += f"\n\n--- Round {i} ---\n" + debate[f"Round {i}"][agent_name]["argumentacion"] + "\n"
    return agent_response


async def judge_rubric_with_arguments(agent_name, rubric, agent_response, pydantic_structure):
    """
    Juzga la rubrica de un agente politico en base a las respuestas del debate.

    Args:
        agent_name (str): Nombre del agente politico.
        rubric (str): Rubrica de evaluacion.
        agent_response (List[str]): Todo lo que dijo el agente en el debate.
        pydantic_structure (Pydantic): Estructura de datos Pydantic para la respuesta del juez.
    Returns:
        dict: Resultados del juicio, incluyendo razonamiento y puntaje.
    """
    judge = Judge(rubric=rubric, pydantic_structure=pydantic_structure,)
    razonamiento, puntaje = await judge.judge_agent_arguments(agent_name, agent_response)
    return razonamiento, puntaje
    
from typing import Optional
async def judge_rubric_with_debate_and_summary(agent_name: Optional,rubric, debate, summary,pydantic_structure):
    """
    Juzga la rubrica de un agente politico en base a las respuestas del debate.

    Args:
        rubric (str): Rubrica de evaluacion.
        debate (List[str]): Todo lo que dijo el/los agente en el debate.
        pydantic_structure (Pydantic): Estructura de datos Pydantic para la respuesta del juez.
    Returns:
        dict: Resultados del juicio, incluyendo razonamiento y puntaje.
    """
    judge = Judge(rubric=rubric, pydantic_structure=pydantic_structure,)
    razonamiento, puntaje = await judge.judge_debate_summary(debate, summary, agent_name,research=None)
    return razonamiento, puntaje

