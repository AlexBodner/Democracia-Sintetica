import os
import json
from glob import glob

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
SIN_RESEARCH = os.path.join('evaluaciones/llm_judge/sin_research/ley por ley')
CON_RESEARCH = os.path.join( 'evaluaciones/llm_judge/con_research/ley por ley')

# Normalización de nombres
def normalize(name):
    return name.strip().lower().replace('  ', ' ')

# Extraer leyes desde los archivos
leyes = []
sin_files = glob(os.path.join(SIN_RESEARCH, 'promedio_agentes_*.json'))
for f in sin_files:
    fname = os.path.basename(f)
    if fname.startswith("promedio_agentes_") and fname.endswith(".json"):
        ley = fname.replace("promedio_agentes_", "").replace(".json", "")
        leyes.append(ley)

leyes = sorted(leyes)

# Resultados
all_results = {}

for ley in leyes:
    sin_path = os.path.join(SIN_RESEARCH, f'promedio_agentes_{ley}.json')
    con_path = os.path.join(CON_RESEARCH, f'promedio_agentes_{ley}.json')

    if not os.path.exists(sin_path) or not os.path.exists(con_path):
        print(f"[WARNING] Archivos faltantes para ley {ley}")
        continue

    with open(sin_path) as f:
        sin_data = json.load(f)
    with open(con_path) as f:
        con_data = json.load(f)

    sin_agents = {normalize(k): k for k in sin_data}
    con_agents = {normalize(k): k for k in con_data}

    common_agents = set(sin_agents.keys()) & set(con_agents.keys())
    resultados_ley = {}

    for agent_norm in common_agents:
        agent_sin = sin_agents[agent_norm]
        agent_con = con_agents[agent_norm]

        datos_sin = sin_data[agent_sin].get("datos")
        datos_con = con_data[agent_con].get("datos")

        if datos_sin is None or datos_con is None or datos_sin == 0:
            continue

        incremento_pct = ((datos_con - datos_sin) / datos_sin) * 100
        resultados_ley[agent_sin] = incremento_pct

    if resultados_ley:
        all_results[ley] = resultados_ley

# Mostrar resultados
for ley, agentes in all_results.items():
    print(f"\n📘 Ley {ley}:")
    for agent, pct in agentes.items():
        print(f"  {agent}: {pct:.2f}%")

# Guardar resultados en JSON
output_path = os.path.join(BASE, 'porcentaje_incremento_por_agente.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Resultados guardados en: {output_path}")
