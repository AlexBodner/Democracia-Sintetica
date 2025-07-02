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
    for d in dicts:
        for k, v in d.items():
            if isinstance(v, dict) and 'puntaje' in v:
                try:
                    puntaje = float(v['puntaje'])
                except (ValueError, TypeError):
                    continue
                global_metrics[k] += puntaje
                global_count[k] += 1
            elif isinstance(v, dict):
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
    for agent in agent_metrics:
        avg[agent] = {}
        for rubrica in agent_metrics[agent]:
            avg[agent][rubrica] = agent_metrics[agent][rubrica] / agent_count[agent][rubrica] if agent_count[agent][rubrica] else None
    return avg

def flatten_metrics(all_results):
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
            summary = debate.get('summary_result', {})
            for metric, metric_data in summary.items():
                if isinstance(metric_data, dict) and 'puntaje' in metric_data:
                    try:
                        puntaje = float(metric_data['puntaje'])
                    except (ValueError, TypeError):
                        continue
                    metrics[f"summary.{metric}"].append(puntaje)
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
    # Global
    metrics = flatten_metrics(all_intermediate)
    global_avg = {k: sum(v)/len(v) if v else None for k, v in metrics.items()}
    with open("evaluaciones/llm_judge/sin_research/promedio_global.json", "w", encoding="utf-8") as f:
        json.dump(global_avg, f, indent=2, ensure_ascii=False)
    print("Promedios recalculados y guardados.")

if __name__ == "__main__":
    main()
