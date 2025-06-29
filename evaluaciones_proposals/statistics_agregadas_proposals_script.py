import os
import json
import glob
from collections import defaultdict, Counter, OrderedDict

PROPOSALS_DIR = os.path.dirname(__file__)
DEBATES_GLOB = os.path.join(PROPOSALS_DIR, 'debate_*.json')
OUTPUT_PATH = os.path.join(PROPOSALS_DIR, 'statistics_agregadas_proposals.json')

# --- MAIN ---
def main():
    # agent -> Counter of proposals voted in favor by proposer
    agent_vote_counter = defaultdict(lambda: Counter())
    for debate_path in glob.glob(DEBATES_GLOB):
        with open(debate_path, encoding='utf-8') as f:
            debate = json.load(f)
        proposals_por_agente = debate.get('proposals_por_agente', {})
        round4 = debate.get('Round 4', {})
        agents = list(debate.get('Round 0', {}).keys())
        for ag in agents:
            for prop, proposer in proposals_por_agente.items():
                if proposer != ag and round4.get(ag, {}).get(prop) is True:
                    agent_vote_counter[ag][proposer] += 1
    # Sumar propuestas hechas y propuestas propias votadas en contra
    proposals_made_total = Counter()
    propias_votadas_en_contra_total = Counter()
    for debate_path in glob.glob(DEBATES_GLOB):
        with open(debate_path, encoding='utf-8') as f:
            debate = json.load(f)
        proposals_por_agente = debate.get('proposals_por_agente', {})
        round4 = debate.get('Round 4', {})
        agents = list(debate.get('Round 0', {}).keys())
        for ag in agents:
            # propuestas hechas
            proposals_made_total[ag] += list(proposals_por_agente.values()).count(ag)
            # propuestas propias votadas en contra
            propias = [prop for prop, proposer in proposals_por_agente.items() if proposer == ag]
            for prop in propias:
                if round4.get(ag, {}).get(prop) is False:
                    propias_votadas_en_contra_total[ag] += 1
    # Build output: for each agent, order by most voted
    result = {}
    for ag, counter in agent_vote_counter.items():
        sorted_counts = OrderedDict(sorted(counter.items(), key=lambda x: -x[1]))
        total_votadas = sum(counter.values())
        result[ag] = {
            'cantidad_propuestas_votadas': dict(sorted_counts) | {'total': total_votadas},
            'propuestas_totales_hechas': proposals_made_total.get(ag, 0),
            'propuestas_propias_votadas_en_contra_total': propias_votadas_en_contra_total.get(ag, 0)
        }
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
