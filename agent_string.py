import json

def get_agent_responses(debate, agent_name, n_rounds=3):
    agent_response = ""
    for i in range(n_rounds):
        if f"Round {i}" in debate.keys():
            agent_response += f"\n\n--- Round {i} ---\n" + debate[f"Round {i}"][agent_name] + "\n"
    return agent_response


with open('debate.json', 'r') as file:
    debate = json.load(file)
    
print(get_agent_responses(debate, "Agente de Izquierda"))
            