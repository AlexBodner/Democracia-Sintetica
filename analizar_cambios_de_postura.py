import os
import json
from collections import defaultdict

def get_ley_debate_files(folder):
    # Busca solo archivos en subcarpetas ley_i/debate_j.json
    files = []
    for ley_dir in os.listdir(folder):
        ley_path = os.path.join(folder, ley_dir)
        if os.path.isdir(ley_path) and ley_dir.startswith('ley_'):
            for fname in os.listdir(ley_path):
                if fname.endswith('.json') and fname.startswith('debate_'):
                    files.append((ley_dir, fname, os.path.join(ley_path, fname)))
    return files

def extract_votes(round_data):
    votes = {}
    for agent, data in round_data.items():
        if isinstance(data, dict):
            vote = data.get('voto')
            if vote is None:
                vote = data.get('vote')
            votes[agent] = vote
    return votes

def analyze_debate_votes(debate_path):
    with open(debate_path, 'r', encoding='utf-8') as f:
        debate = json.load(f)
    rounds = [k for k in debate.keys() if k.lower().startswith('round')]
    rounds.sort(key=lambda x: int(x.split()[-1]))
    all_agents = set()
    for round_name in rounds:
        all_agents.update(debate[round_name].keys())
    agent_vote_history = {agent: [] for agent in all_agents}
    for round_name in rounds:
        round_votes = extract_votes(debate[round_name])
        for agent in all_agents:
            agent_vote_history[agent].append(round_votes.get(agent))
    changes = {}
    for agent, votes in agent_vote_history.items():
        for i in range(1, len(votes)):
            if votes[i] is None or votes[i-1] is None:
                continue
            if votes[i] != votes[i-1]:
                # El cambio ocurre en la ronda i (de i-1 a i)
                changes.setdefault(agent, {})[i] = {
                    'from_round': i-1,
                    'to_round': i,
                    'from_vote': votes[i-1],
                    'to_vote': votes[i]
                }
    return changes

def main():
    base_dirs = [
        ('debates/con_research', 'cambios_postura/con_research'),
        ('debates/sin_research', 'cambios_postura/sin_research')
    ]
    for debate_dir, output_dir in base_dirs:
        os.makedirs(output_dir, exist_ok=True)
        # ley -> agente -> debate_num -> [cambios]
        ley_agente_debate = defaultdict(lambda: defaultdict(dict))
        for ley_dir, debate_file, debate_path in get_ley_debate_files(debate_dir):
            ley = ley_dir.replace('ley_', '')
            debate_num = debate_file.replace('debate_', '').replace('.json', '')
            changes = analyze_debate_votes(debate_path)
            for agent, cambios in changes.items():
                if cambios:
                    # Convertir los cambios a lista de diccionarios (sin clave de ronda)
                    cambios_lista = list(cambios.values())
                    ley_agente_debate[ley][agent][f"Debate {debate_num}"] = cambios_lista
        # Ordenar por id de ley (numérico si es posible)
        def sort_ley_id(ley):
            try:
                return int(ley)
            except Exception:
                return ley
        resultado_ordenado = {k: ley_agente_debate[k] for k in sorted(ley_agente_debate.keys(), key=sort_ley_id)}
        with open(os.path.join(output_dir, 'cambios_por_ley_agente.json'), 'w', encoding='utf-8') as f:
            json.dump(resultado_ordenado, f, indent=2, ensure_ascii=False)
        print(f'Resultados guardados en {output_dir}')

if __name__ == "__main__":
    main()
