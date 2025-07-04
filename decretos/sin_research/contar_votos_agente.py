import os
import json

# Ruta base de los debates
base_path = '/Users/tomascarrie/Library/Mobile Documents/com~apple~CloudDocs/Tomi/NLP/Repo-Final/decretos/sin_research/'

# Diccionario para almacenar los votos
votos_por_agente = {}

# Recorrer cada carpeta de ley
for ley in os.listdir(base_path):
    ley_path = os.path.join(base_path, ley)
    if os.path.isdir(ley_path):
        # Buscar el archivo de debate
        debate_file = os.path.join(ley_path, 'debate_(0,).json')
        if os.path.exists(debate_file):
            with open(debate_file, 'r', encoding='utf-8') as f:
                debate_data = json.load(f)
                round_2 = debate_data.get("Round 2", {})
                for agente, detalles in round_2.items():
                    voto = detalles.get("voto", 0)
                    if voto in [3, 4]:
                        if agente not in votos_por_agente:
                            votos_por_agente[agente] = 0
                        votos_por_agente[agente] += 1

# Guardar los resultados en un archivo JSON
output_path = '/Users/tomascarrie/Library/Mobile Documents/com~apple~CloudDocs/Tomi/NLP/Repo-Final/Regulacion-Agentic/decretos/sin_research/votos_por_agente.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(votos_por_agente, f, ensure_ascii=False, indent=4)

print(f"Votos por agente guardados en {output_path}")

def contar_leyes_todos_en_contra(base_path):
    leyes_todos_en_contra = []
    leyes_union_por_la_patria_a_favor = []

    for ley in os.listdir(base_path):
        ley_path = os.path.join(base_path, ley)
        if os.path.isdir(ley_path):
            debate_file = os.path.join(ley_path, 'debate_(0,).json')
            if os.path.exists(debate_file):
                with open(debate_file, 'r', encoding='utf-8') as f:
                    debate_data = json.load(f)
                    round_2 = debate_data.get("Round 2", {})
                    otros_en_contra = True
                    todos_en_contra = True
                    union_por_la_patria_a_favor = False
                    votos_en_contra = 0

                    for agente, detalles in round_2.items():
                        voto = detalles.get("voto", 0)
                        if voto in [3, 4]:
                            todos_en_contra = False
                            if agente == "Agente de Union Por La Patria":
                                union_por_la_patria_a_favor = True
                            else:
                                otros_en_contra = False
                        elif voto in [0, 1]:
                            votos_en_contra += 1

                    if todos_en_contra:
                        leyes_todos_en_contra.append({"ley": ley, "votos_en_contra": votos_en_contra})
                    if otros_en_contra and union_por_la_patria_a_favor:
                        leyes_union_por_la_patria_a_favor.append({"ley": ley, "votos_en_contra": votos_en_contra})

    return leyes_todos_en_contra, leyes_union_por_la_patria_a_favor

# Llamar a la función y guardar los resultados
leyes_todos_en_contra, leyes_union_por_la_patria_a_favor = contar_leyes_todos_en_contra(base_path)

output_path_todos_en_contra = '/Users/tomascarrie/Library/Mobile Documents/com~apple~CloudDocs/Tomi/NLP/Repo-Final/Regulacion-Agentic/decretos/sin_research/leyes_todos_en_contra.json'
output_path_union_por_la_patria = '/Users/tomascarrie/Library/Mobile Documents/com~apple~CloudDocs/Tomi/NLP/Repo-Final/Regulacion-Agentic/decretos/sin_research/leyes_union_por_la_patria_a_favor.json'

with open(output_path_todos_en_contra, 'w', encoding='utf-8') as f:
    json.dump(leyes_todos_en_contra, f, ensure_ascii=False, indent=4)

with open(output_path_union_por_la_patria, 'w', encoding='utf-8') as f:
    json.dump(leyes_union_por_la_patria_a_favor, f, ensure_ascii=False, indent=4)

print(f"Resultados guardados en {output_path_todos_en_contra} y {output_path_union_por_la_patria}")