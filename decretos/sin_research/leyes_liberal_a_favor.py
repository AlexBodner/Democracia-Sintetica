import os
import json

# Ruta base de los debates
#base_path = os.path.dirname(os.path.abspath(__file__))
base_path = "/Users/julietaggarciapereyra/Documents/UdeSA/Cuarto_Año/NLP/Regulacion-Agentic/decretos"

resultados = []

for ley in os.listdir(base_path):
    ley_path = os.path.join(base_path, ley)
    if os.path.isdir(ley_path):
        debate_file = os.path.join(ley_path, 'debate_(0,).json')
        if os.path.exists(debate_file):
            with open(debate_file, 'r', encoding='utf-8') as f:
                debate_data = json.load(f)
                round_2 = debate_data.get("Round 2", {})
                voto_liberal = round_2.get("Agente Liberal", {}).get("voto", None)
                if voto_liberal in [0, 1]:
                    resultados.append(ley)

output_path = '/Users/julietaggarciapereyra/Documents/UdeSA/Cuarto_Año/NLP/Regulacion-Agentic/decretos/sin_research/leyes_liberal_a_favor.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(resultados, f, ensure_ascii=False, indent=4)

print(f"Leyes con voto a favor del Agente Liberal guardadas en {output_path}")
