import os
import json
from collections import defaultdict, Counter
from statistics import mean, variance, mode, StatisticsError

INPUT_DIRS = [
    ("debates/con_research", "promedio_debates/con_research/resultados.json"),
    ("debates/sin_research", "promedio_debates/sin_research/resultados.json"),
    ("debates_5_rondas/sin_research", "promedio_debates/5_rondas_sin_research/resultados.json")
]

os.makedirs("promedio_debates/con_research", exist_ok=True)
os.makedirs("promedio_debates/sin_research", exist_ok=True)
os.makedirs("promedio_debates/5_rondas_sin_research", exist_ok=True)

def sort_ley_id(ley):
    try:
        return int(ley)
    except Exception:
        return ley

for input_dir, output_path in INPUT_DIRS:

    leyes = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # {ley: {ronda: {agente: [votos]}}}
    for root, _, files in os.walk(input_dir):
        for fname in files:
            if fname.endswith(".json"):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, encoding="utf-8") as f:
                        debate = json.load(f)
                    # Detect ley number from path (ley_x or debate_x)
                    if "ley_" in fpath:
                        ley = fpath.split("ley_")[-1].split(os.sep)[0].split("/")[0].split("\\")[0]
                    else:
                        # fallback: try to extract from filename
                        ley = fname.split("_")[-1].replace(".json", "")
                    for ronda, agentes in debate.items():
                        if not ronda.lower().startswith("round"): continue
                     
                        for agente, datos in agentes.items():
                            voto = datos.get("voto")
                            if voto is not None:
                                leyes[ley][ronda][agente].append(voto)
                except Exception as e:
                    print(f"Error en {fpath}: {e}")
    # Calcular estadísticos
    resultados = {}
    for ley in sorted(leyes.keys(), key=sort_ley_id):
        resultados[ley] = {}
        for ronda in sorted(leyes[ley].keys()):
            resultados[ley][ronda] = {}
            for agente, votos in leyes[ley][ronda].items():
                if votos:
                    try:
                        moda = mode(votos)
                    except StatisticsError:
                        moda = Counter(votos).most_common(1)[0][0] if votos else None
                    resultados[ley][ronda][agente] = {
                        "voto_promedio": float(mean(votos)),
                        "voto_moda": moda,
                        "varianza_votos": float(variance(votos)) if len(votos) > 1 else 0.0
                    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)
print("Listo. Resultados guardados en promedio_debates/")



