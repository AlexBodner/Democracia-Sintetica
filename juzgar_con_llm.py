import asyncio
import sys
import os
import json
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluadores.llm_judge_agentes import main as judge_main
from evaluadores.llm_judge_summary import main as judge_summary_main

def get_debate_paths(ley_id, base_dir):
    debates = []
    for i in range(5):
        path = os.path.join(base_dir, f"ley_{ley_id}", f"debate_{i}.json")
        if os.path.exists(path):
            debates.append(path)
    return debates

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
                    result[agent][rubrica] += rubrica_data['puntaje']
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
    # Separa métricas globales y por agente
    global_metrics = defaultdict(float)
    global_count = defaultdict(int)
    agent_metrics = defaultdict(lambda: defaultdict(float))
    agent_count = defaultdict(lambda: defaultdict(int))
    for d in dicts:
        for k, v in d.items():
            if isinstance(v, dict) and 'puntaje' in v:
                # Métrica global
                global_metrics[k] += v['puntaje']
                global_count[k] += 1
            elif isinstance(v, dict):
                # Métricas por agente
                for rubrica, rubrica_data in v.items():
                    if isinstance(rubrica_data, dict) and 'puntaje' in rubrica_data:
                        agent_metrics[k][rubrica] += rubrica_data['puntaje']
                        agent_count[k][rubrica] += 1
    avg = {}
    # Promedios globales
    for k in global_metrics:
        avg[k] = global_metrics[k] / global_count[k] if global_count[k] else None
    # Promedios por agente
    for agent in agent_metrics:
        avg[agent] = {}
        for rubrica in agent_metrics[agent]:
            avg[agent][rubrica] = agent_metrics[agent][rubrica] / agent_count[agent][rubrica] if agent_count[agent][rubrica] else None
    return avg

def flatten_metrics(all_results):
    # Devuelve una lista de todos los puntajes por metrica, para promediar globalmente
    metrics = defaultdict(list)
    for ley_id, debates in all_results.items():
        for debate in debates:
            agentes = debate.get('agentes_result', {})
            for agent, agent_data in agentes.items():
                for rubrica, rubrica_data in agent_data.items():
                    if isinstance(rubrica_data, dict) and 'puntaje' in rubrica_data:
                        metrics[f"{agent}.{rubrica}"] .append(rubrica_data['puntaje'])
            summary = debate.get('summary_result', {})
            for metric, metric_data in summary.items():
                if isinstance(metric_data, dict) and 'puntaje' in metric_data:
                    metrics[f"summary.{metric}"] .append(metric_data['puntaje'])
    return metrics

def save_intermediate(all_results, out_dir):
    intermedios_path = os.path.join(out_dir, "resultados_intermedios.json")
    with open(intermedios_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"Resultados intermedios guardados en {intermedios_path}")

def main():
    with open("testing/leyes.json", "r", encoding="utf-8") as f:
        leyes = json.load(f)
    base_dirs = ["debates/con_research", "debates/sin_research"]
    for base_dir in base_dirs:
        print(f"\nEvaluando en {base_dir}")
        out_dir = f"evaluaciones/llm_judge/{'con_research' if 'con' in base_dir else 'sin_research'}"
        os.makedirs(out_dir, exist_ok=True)
        all_intermediate = {}
        for ley in leyes:
            ley_id = str(ley["id"])
            debate_paths = get_debate_paths(ley_id, base_dir)
            agentes_results = []
            summary_results = []
            ley_debates = []
            for idx, debate_path in enumerate(debate_paths):
                agentes_result = asyncio.run(judge_main(debate_path, ley, n_rounds=3, output_folder=out_dir))
                summary_result = asyncio.run(judge_summary_main(debate_path, ley, n_rounds=3, output_folder=out_dir))
                agentes_results.append(agentes_result)
                summary_results.append(summary_result)
                ley_debates.append({
                    "debate_idx": idx,
                    "debate_path": debate_path,
                    "agentes_result": agentes_result,
                    "summary_result": summary_result
                })
                all_intermediate[ley_id] = ley_debates
                save_intermediate(all_intermediate, out_dir)
            avg_agentes = average_nested_dicts(agentes_results)
            avg_summary = average_summary_dicts(summary_results)
            with open(os.path.join(out_dir, f"promedio_agentes_{ley_id}.json"), "w", encoding="utf-8") as f:
                json.dump(avg_agentes, f, indent=2, ensure_ascii=False)
            with open(os.path.join(out_dir, f"promedio_summary_{ley_id}.json"), "w", encoding="utf-8") as f:
                json.dump(avg_summary, f, indent=2, ensure_ascii=False)
            print(f"Promedios guardados para ley {ley_id} en {out_dir}")
        # Calcular promedios globales
        metrics = flatten_metrics(all_intermediate)
        global_avg = {k: sum(v)/len(v) if v else None for k, v in metrics.items()}
        with open(os.path.join(out_dir, "promedio_global.json"), "w", encoding="utf-8") as f:
            json.dump(global_avg, f, indent=2, ensure_ascii=False)
        print(f"Promedio global guardado en {os.path.join(out_dir, 'promedio_global.json')}")

if __name__ == "__main__":
    main()
