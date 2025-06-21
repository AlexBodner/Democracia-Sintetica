import os
import json

def get_debate_ids(folder):
    return sorted([
        f.split('_')[-1].split('.')[0]
        for f in os.listdir(folder)
        if f.startswith('debate_') and f.endswith('.json')
    ])

def load_votes(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    round2 = data.get("Round 2", {})
    votes = {}
    for agent, agent_data in round2.items():
        # Try to get the vote from the agent's data
        vote = None
        if isinstance(agent_data, dict):
            # Try common keys
            vote = agent_data.get("voto")
            if vote is None:
                # Try to extract from argumentacion if present
                arg = agent_data.get("argumentacion", "")
                if isinstance(arg, str):
                    for line in arg.splitlines():
                        if "Voto:" in line:
                            vote = line.split("Voto:")[-1].strip()
                            break
        votes[agent] = vote
    return votes

def main():
    folder_with = "debates/con_research"
    folder_without = "debates/sin_research"
    ids_with = set(get_debate_ids(folder_with))
    ids_without = set(get_debate_ids(folder_without))
    common_ids = sorted(ids_with & ids_without)

    output_dir = 'vote_change_reports'
    os.makedirs(output_dir, exist_ok=True)
    report_lines = []
    report_lines.append('--- Comparing votes in Round 2 between research and no research ---\n')
    
    for debate_id in common_ids:
        path_with = os.path.join(folder_with, f"debate_{debate_id}.json")
        path_without = os.path.join(folder_without, f"debate_{debate_id}.json")
        votes_with = load_votes(path_with)
        votes_without = load_votes(path_without)
        changes_found = False
        for agent in set(votes_with) | set(votes_without):
            vote_with = votes_with.get(agent)
            vote_without = votes_without.get(agent)
            if vote_with != vote_without:
                changes_found = True
                report_lines.append(f"Debate {debate_id} - Agent {agent}:")
                report_lines.append(f"  With research:    {vote_with}")
                report_lines.append(f"  Without research: {vote_without}")
                report_lines.append("-" * 40)
        
        if not changes_found:
            report_lines.append(f'Debate: {debate_id} - No vote changes in Round 2 between research and no research')
            report_lines.append('')

    out_file = os.path.join(output_dir, 'compare_votes_research.txt')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f'Results saved to {out_file}')

if __name__ == "__main__":
    main()