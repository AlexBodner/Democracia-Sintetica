import json

# Rutas de los archivos
leyes_uxp_en_contra_path = '/Users/tomascarrie/Library/Mobile Documents/com~apple~CloudDocs/Tomi/NLP/Repo-Final/Regulacion-Agentic/decretos/sin_research/leyes_uxp_en_contra.json'
leyes_por_id_path = '/Users/tomascarrie/Library/Mobile Documents/com~apple~CloudDocs/Tomi/NLP/Repo-Final/Regulacion-Agentic/decretos/sin_research/leyes_por_id.json'

# Cargar los datos
with open(leyes_uxp_en_contra_path, 'r', encoding='utf-8') as f:
    leyes_uxp_en_contra = json.load(f)

with open(leyes_por_id_path, 'r', encoding='utf-8') as f:
    leyes_por_id = json.load(f)

# Reemplazar "ley_{id}" por el valor correspondiente en leyes_por_id
leyes_uxp_en_contra = [leyes_por_id.get(ley, ley) for ley in leyes_uxp_en_contra]

# Guardar los cambios en el archivo
with open(leyes_uxp_en_contra_path, 'w', encoding='utf-8') as f:
    json.dump(leyes_uxp_en_contra, f, ensure_ascii=False, indent=4)

print(f"Archivo actualizado en {leyes_uxp_en_contra_path}")