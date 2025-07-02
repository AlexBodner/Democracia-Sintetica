# Script to aggregate experiment results for agentes_displayed and agentes_ocultos
# Output: statistics_experimentos_agentes.json in this directory

import os
import json
from collections import defaultdict

PROPOSALS_DIR = os.path.dirname(__file__)
STATS_PATH = os.path.join(PROPOSALS_DIR, 'statistics_proposals.json')
OUTPUT_PATH = os.path.join(PROPOSALS_DIR, 'statistics_experimentos_agentes.json')

# --- MAIN ---
def main():
    with open(STATS_PATH, encoding='utf-8') as f:
        stats_by_ley = json.load(f)
    # agent -> {agentes_displayed: {cantidad_de_cambios, mae}, agentes_ocultos: {...}}
    result = defaultdict(lambda: {
        'agentes_displayed': {'cantidad_de_cambios': 0, 'mae': 0, 'n': 0},
        'agentes_ocultos': {'cantidad_de_cambios': 0, 'mae': 0, 'n': 0}
    })
    for law_id, agent_stats in stats_by_ley.items():
        for ag, stats in agent_stats.items():
            # agentes_displayed
            cambio_disp = stats.get('cambios_agentes_displayed', {}).get('change')
            mae_disp = stats.get('mae', {}).get('agentes_displayed')
            if cambio_disp is not None:
                result[ag]['agentes_displayed']['cantidad_de_cambios'] += cambio_disp
                result[ag]['agentes_displayed']['n'] += 1
            if mae_disp is not None:
                result[ag]['agentes_displayed']['mae'] += mae_disp
            # agentes_ocultos
            cambio_oc = stats.get('cambios_agentes_ocultos', {}).get('change')
            mae_oc = stats.get('mae', {}).get('agentes_ocultos')
            if cambio_oc is not None:
                result[ag]['agentes_ocultos']['cantidad_de_cambios'] += cambio_oc
                result[ag]['agentes_ocultos']['n'] += 1
            if mae_oc is not None:
                result[ag]['agentes_ocultos']['mae'] += mae_oc
    # Remove 'n' and output sums only
    output = {}
    for ag, d in result.items():
        output[ag] = {
            'agentes_displayed': {
                'cantidad_de_cambios': d['agentes_displayed']['cantidad_de_cambios'],
                'mae': d['agentes_displayed']['mae']
            },
            'agentes_ocultos': {
                'cantidad_de_cambios': d['agentes_ocultos']['cantidad_de_cambios'],
                'mae': d['agentes_ocultos']['mae']
            }
        }
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
