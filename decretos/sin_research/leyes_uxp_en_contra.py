import os
import json

# Ruta base de los debates
base_path = os.path.dirname(os.path.abspath(__file__))

resultados = []

for ley in os.listdir(base_path):
    ley_path = os.path.join(base_path, ley)
    if os.path.isdir(ley_path):
        debate_file = os.path.join(ley_path, 'debate_(0,).json')
        if os.path.exists(debate_file):
            with open(debate_file, 'r', encoding='utf-8') as f:
                debate_data = json.load(f)
                round_2 = debate_data.get("Round 2", {})
                voto_uxp = round_2.get("Agente de Union Por La Patria", {}).get("voto", None)
                if voto_uxp in [3, 4]:
                    resultados.append(ley)

output_path = os.path.join(base_path, 'leyes_uxp_en_contra.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(resultados, f, ensure_ascii=False, indent=4)

print(f"Leyes con voto en contra de UXP guardadas en {output_path}")
