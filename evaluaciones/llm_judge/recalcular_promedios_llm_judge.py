import json
from collections import defaultdict
import os

def average_nested_dicts(dicts):
    if not dicts:
        return {}
    result = defaultdict(lambda: defaultdict(float))
    count = defaultdict(lambda: defaultdict(int))
    for d in dicts:
        for agent, agent_data in d.items():
            if not isinstance(agent_data, dict):
                continue
            for rubrica, rubrica_data in agent_data.items():
                if isinstance(rubrica_data, dict) and 'puntaje' in rubrica_data:
                    try:
                        puntaje = float(rubrica_data['puntaje'])
                    except (ValueError, TypeError):
                        continue
                    result[agent][rubrica] += puntaje
                    count[agent][rubrica] += 1
    avg = {}
    for agent in result:
        avg[agent] = {}
        for rubrica in result[agent]:
            avg[agent][rubrica] = result[agent][rubrica] / count[agent][rubrica] if count[agent][rubrica] else None
    return avg

def average_summary_dicts(dicts):
    if not dicts:
        return {}
    global_metrics = defaultdict(float)
    global_count = defaultdict(int)
    agent_metrics = defaultdict(lambda: defaultdict(float))
    agent_count = defaultdict(lambda: defaultdict(int))
    agentwise_metrics = defaultdict(lambda: defaultdict(float))
    agentwise_count = defaultdict(lambda: defaultdict(int))
    for d in dicts:
        for k, v in d.items():
            # Caso métrica global tipo {"consistencia": {"puntaje": ...}}
            if isinstance(v, dict) and 'puntaje' in v:
                try:
                    puntaje = float(v['puntaje'])
                except (ValueError, TypeError):
                    continue
                global_metrics[k] += puntaje
                global_count[k] += 1
            # Caso métrica por agente tipo {"votos": {"Agente X": valor, ...}}
            elif isinstance(v, dict):
                # Si todos los valores son numéricos o None
                if all(isinstance(val, (int, float)) or val is None for val in v.values()):
                    for agent, val in v.items():
                        if val is not None:
                            agentwise_metrics[k][agent] += val
                            agentwise_count[k][agent] += 1
                else:
                    for rubrica, rubrica_data in v.items():
                        if isinstance(rubrica_data, dict) and 'puntaje' in rubrica_data:
                            try:
                                puntaje = float(rubrica_data['puntaje'])
                            except (ValueError, TypeError):
                                continue
                            agent_metrics[k][rubrica] += puntaje
                            agent_count[k][rubrica] += 1
    avg = {}
    for k in global_metrics:
        avg[k] = global_metrics[k] / global_count[k] if global_count[k] else None
    for agent_metric in agentwise_metrics:
        avg[agent_metric] = {}
        for agent in agentwise_metrics[agent_metric]:
            avg[agent_metric][agent] = agentwise_metrics[agent_metric][agent] / agentwise_count[agent_metric][agent] if agentwise_count[agent_metric][agent] else None
    for agent in agent_metrics:
        avg[agent] = {}
        for rubrica in agent_metrics[agent]:
            avg[agent][rubrica] = agent_metrics[agent][rubrica] / agent_count[agent][rubrica] if agent_count[agent][rubrica] else None
    return avg

def flatten_agent_metrics(all_results):
    metrics = defaultdict(list)
    for ley_id, debates in all_results.items():
        for debate in debates:
            agentes = debate.get('agentes_result', {})
            for agent, agent_data in agentes.items():
                for rubrica, rubrica_data in agent_data.items():
                    if isinstance(rubrica_data, dict) and 'puntaje' in rubrica_data:
                        try:
                            puntaje = float(rubrica_data['puntaje'])
                        except (ValueError, TypeError):
                            continue
                        metrics[f"{agent}.{rubrica}"].append(puntaje)
    return metrics

def flatten_summary_metrics(all_results):
    metrics = defaultdict(list)
    def recursive_flatten(d, prefix=None):
        if isinstance(d, dict):
            # Caso: diccionario de agentes con valores numéricos
            if all(isinstance(val, (int, float)) or val is None for val in d.values()):
                for agent, val in d.items():
                    if val is not None and prefix:
                        metrics[f"{agent}.{prefix}"].append(val)
            else:
                for k, v in d.items():
                    if isinstance(v, dict) and 'puntaje' in v:
                        try:
                            puntaje = float(v['puntaje'])
                        except (ValueError, TypeError):
                            continue
                        metrics[k if not prefix else f"{prefix}.{k}"].append(puntaje)
                    else:
                        recursive_flatten(v, prefix=k if not prefix else f"{prefix}.{k}")
    for ley_id, debates in all_results.items():
        for debate in debates:
            summary = debate.get('summary_result', {})
            recursive_flatten(summary)
    return metrics

def main():
    path = "evaluaciones/llm_judge/sin_research/resultados_intermedios.json"
    with open(path, "r", encoding="utf-8") as f:
        all_intermediate = json.load(f)
    # Por ley
    for ley_id, debates in all_intermediate.items():
        agentes_results = [debate['agentes_result'] for debate in debates]
        summary_results = [debate['summary_result'] for debate in debates]
        avg_agentes = average_nested_dicts(agentes_results)
        avg_summary = average_summary_dicts(summary_results)
        with open(f"evaluaciones/llm_judge/sin_research/promedio_agentes_{ley_id}.json", "w", encoding="utf-8") as f:
            json.dump(avg_agentes, f, indent=2, ensure_ascii=False)
        with open(f"evaluaciones/llm_judge/sin_research/promedio_summary_{ley_id}.json", "w", encoding="utf-8") as f:
            json.dump(avg_summary, f, indent=2, ensure_ascii=False)
    # Global agentes
    agent_metrics = flatten_agent_metrics(all_intermediate)
    global_avg_agents = {k: sum(v)/len(v) if v else None for k, v in agent_metrics.items()}
    with open("evaluaciones/llm_judge/sin_research/promedio_global_agentes.json", "w", encoding="utf-8") as f:
        json.dump(global_avg_agents, f, indent=2, ensure_ascii=False)
    # Global summary
    summary_metrics = flatten_summary_metrics(all_intermediate)
    global_avg_summary = {k: sum(v)/len(v) if v else None for k, v in summary_metrics.items()}
    with open("evaluaciones/llm_judge/sin_research/promedio_global_summary.json", "w", encoding="utf-8") as f:
        json.dump(global_avg_summary, f, indent=2, ensure_ascii=False)
    print("Promedios recalculados y guardados.")

if __name__ == "__main__":
    main()
