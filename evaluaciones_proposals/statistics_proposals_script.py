# Script to compute statistics for proposal debates
# Output: statistics_proposals.json in this directory

import os
import json
import glob
from collections import defaultdict, Counter
import numpy as np

# --- CONFIG ---
PROPOSALS_DIR = os.path.dirname(__file__)
DEBATES_GLOB = os.path.join(PROPOSALS_DIR, 'debate_*.json')
LEY_MAP_PATH = os.path.abspath(os.path.join(PROPOSALS_DIR, '..', 'testing', 'leyes.json'))
OUTPUT_PATH = os.path.join(PROPOSALS_DIR, 'statistics_proposals.json')

# --- LOAD LEYES ---
def load_leyes():
    with open(LEY_MAP_PATH, encoding='utf-8') as f:
        leyes = json.load(f)
    # Map: nombre -> {ley dict}
    return {ley['nombre']: ley for ley in leyes}, {ley['id']: ley for ley in leyes}

# --- AGENT TO POSTURA MAPPING ---
PARTY_MAP = {
    'Agente de Izquierda': 'izquierda_fit',
    'Agente de Union Por La Patria': 'centro_izquierda_fdt_otros',
    'Agente de Juntos Por El Cambio': 'centro_derecha_jxc_otros',
    'Agente Liberal': 'derecha_lla_pro_otros',
}

# --- MAIN ---
def main():
    leyes_by_name, leyes_by_id = load_leyes()
    stats_by_ley = {}
    for debate_path in glob.glob(DEBATES_GLOB):
        with open(debate_path, encoding='utf-8') as f:
            debate = json.load(f)
        # Law name from debate (assume in "Debate Completo" or infer from file)
        law_name = None
        for entry in debate.get('Debate Completo', []):
            if 'Ley' in entry.get('content', ''):
                for ley in leyes_by_name:
                    if ley in entry['content']:
                        law_name = ley
                        break
            if law_name:
                break
        if not law_name:
            for ley in leyes_by_name:
                if str(leyes_by_name[ley]['id']) in debate_path:
                    law_name = ley
                    break
        if not law_name:
            continue  # skip if cannot match
        law_id = leyes_by_name[law_name]['id']
        # --- AGENTS ---
        agents = list(debate.get('Round 0', {}).keys())
        # --- Proposals ---
        proposals_por_agente = debate.get('proposals_por_agente', {})
        # --- Votes on proposals ---
        round4 = debate.get('Round 4', {})
        # --- Final votes ---
        final_votes = {}
        for r in ["Round 5", "Round 6"]:
            if r in debate:
                for ag, d in debate[r].items():
                    final_votes[ag] = d.get('voto')
        # --- Real votes ---
        ley_posturas = leyes_by_name[law_name]['posturas']
        real_votes = {ag: ley_posturas[PARTY_MAP[ag]]['voto'] for ag in agents if ag in PARTY_MAP}
        # --- Proposal stats ---
        agent_stats = {ag: {} for ag in agents}
        # 1. Number of proposals by agent
        proposals_by_agent = Counter(proposals_por_agente.values())
        # 2. For each agent: proposals by others they approved
        for ag in agents:
            approved = []
            for prop, proposer in proposals_por_agente.items():
                if proposer != ag and round4.get(ag, {}).get(prop) is True:
                    approved.append(proposer)
            agent_stats[ag]['approved_others'] = len(approved)
            agent_stats[ag]['approved_distribution'] = dict(Counter(approved))
            # Most similar agent: the one whose proposals this agent approved most
            if approved:
                agent_stats[ag]['most_similar'] = max(agent_stats[ag]['approved_distribution'], key=agent_stats[ag]['approved_distribution'].get)
            else:
                agent_stats[ag]['most_similar'] = None
        # 3. Vote changes after proposals (all, and norm>=2)
        for ag in agents:
            votes = []
            for r in range(0, 7):
                rkey = f"Round {r}"
                if rkey in debate and ag in debate[rkey]:
                    v = debate[rkey][ag].get('voto')
                    if v is not None:
                        votes.append(v)
            # Vote changes
            #changes = [abs(votes[i+1] - votes[i]) for i in range(len(votes)-1)] if len(votes) > 1 else []
            #agent_stats[ag]['vote_changes'] = changes
            #agent_stats[ag]['vote_changes_norm2'] = [c for c in changes if c >= 2]
        # 4. Number of proposals made
        for ag in agents:
            agent_stats[ag]['proposals_made'] = proposals_by_agent.get(ag, 0)
        # --- VOTE CHANGES: cambio entre ronda 1 y ronda 5 (agentes ocultos), y ronda 1 y ronda 6 (agentes visibles) ---
        for ag in agents:
            vote_r1 = None
            vote_r5 = None
            vote_r6 = None
            if 'Round 1' in debate and ag in debate['Round 1']:
                vote_r1 = debate['Round 1'][ag].get('voto')
            if 'Round 5' in debate and ag in debate['Round 5']:
                vote_r5 = debate['Round 5'][ag].get('voto')
            if 'Round 6' in debate and ag in debate['Round 6']:
                vote_r6 = debate['Round 6'][ag].get('voto')
            agent_stats[ag]['cambios_agentes_ocultos'] = {
                'from_vote': vote_r1,
                'to_vote': vote_r5,
                'change': abs(vote_r5 - vote_r1) if vote_r1 is not None and vote_r5 is not None else None
            }
            agent_stats[ag]['cambios_agentes_displayed'] = {
                'from_vote': vote_r1,
                'to_vote': vote_r6,
                'change': abs(vote_r6 - vote_r1) if vote_r1 is not None and vote_r6 is not None else None
            }
        # --- MAE: para ronda 5 y ronda 6 ---
        vote_map = {'A favor': 4, 'En contra': 0, 'Dividido': 2, 'Apoyo critico': 3, 'Crítico': 2, 'Abstención': 2}
        for ag in agents:
            real = real_votes.get(ag)
            # Ronda 5
            pred5 = None
            if 'Round 5' in debate and ag in debate['Round 5']:
                pred5 = debate['Round 5'][ag].get('voto')
            pred5_num = pred5 if isinstance(pred5, (int, float)) else vote_map.get(str(pred5), 2)
            real_num = real if isinstance(real, (int, float)) else vote_map.get(str(real), 2)
            mae_r5 = abs(pred5_num - real_num) if pred5 is not None and real is not None else None
            # Ronda 6
            pred6 = None
            if 'Round 6' in debate and ag in debate['Round 6']:
                pred6 = debate['Round 6'][ag].get('voto')
            pred6_num = pred6 if isinstance(pred6, (int, float)) else vote_map.get(str(pred6), 2)
            mae_r6 = abs(pred6_num - real_num) if pred6 is not None and real is not None else None
            agent_stats[ag]['mae'] = {
                'agentes_ocultos': mae_r5,
                'agentes_displayed': mae_r6
            }
        stats_by_ley[law_id] = agent_stats
    # --- Write output ---
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(stats_by_ley, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
