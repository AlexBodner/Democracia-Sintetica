import os
import json

def get_debate_files(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.json')]

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
    rounds = [k for k in debate.keys() if k.startswith('Round')]
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
        changes[agent] = []
        for i in range(1, len(votes)):
            if votes[i] is None or votes[i-1] is None:
                continue  # Skip if any vote is missing
            if votes[i] != votes[i-1]:
                changes[agent].append((i-1, i, votes[i-1], votes[i]))
    return changes

def main():
    base_dirs = [
        'debates/con_research',
        'debates/sin_research'
    ]
    output_dir = 'vote_change_reports'
    os.makedirs(output_dir, exist_ok=True)
    for base_dir in base_dirs:
        report_lines = []
        report_lines.append(f'--- Checking debates in {base_dir} ---\n')
        for debate_file in get_debate_files(base_dir):
            changes = analyze_debate_votes(debate_file)
            report_lines.append(f'\nDebate: {debate_file}')
            for agent, change_list in changes.items():
                if change_list:
                    report_lines.append(f'  Agent: {agent}')
                    for (from_idx, to_idx, from_vote, to_vote) in change_list:
                        report_lines.append(f'    Round {from_idx} -> {to_idx}: {from_vote} -> {to_vote}')
                else:
                    report_lines.append(f'  Agent: {agent} - No vote changes')
        # Save report for this base_dir
        out_file = os.path.join(output_dir, f'report_{os.path.basename(base_dir)}.txt')
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        print(f'Results saved to {out_file}')

if __name__ == "__main__":
    main()
