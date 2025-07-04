import json
import os

# Ruta del archivo decretos.json
input_path = '/Users/tomascarrie/Library/Mobile Documents/com~apple~CloudDocs/Tomi/NLP/Repo-Final/Regulacion-Agentic/dataset/decretos.json'
output_path = '/Users/tomascarrie/Library/Mobile Documents/com~apple~CloudDocs/Tomi/NLP/Repo-Final/Regulacion-Agentic/decretos/sin_research/leyes_por_id.json'

# Leer el archivo decretos.json
with open(input_path, 'r', encoding='utf-8') as f:
    decretos = json.load(f)

# Crear el nuevo diccionario con las leyes por id
leyes_por_id = {}
for decreto in decretos:
    if "id" in decreto and "nombre" in decreto:
        leyes_por_id[f"ley_{decreto['id']}"] = decreto["nombre"]

# Guardar el nuevo archivo JSON
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(leyes_por_id, f, ensure_ascii=False, indent=4)

print(f"Archivo creado en {output_path}")