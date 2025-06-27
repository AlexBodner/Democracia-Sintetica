import os
import json
from collections import defaultdict

# Mapeo de nombres de agentes a posturas en leyes.json
AGENTE_TO_POSTURA = {
    'Agente de Izquierda': 'izquierda_fit',
    'Agente de Union Por La Patria': 'centro_izquierda_fdt_otros',
    'Agente de Juntos Por El Cambio': 'centro_derecha_jxc_otros',
    'Agente Liberal': 'derecha_lla_pro_otros',
}

# Mapeo de votos numéricos a string 
VOTO_NUM_TO_STR = {
    0: 'En contra',
    1: 'Critico', 
    2: 'Dividido',  
    3: 'Apoyo critico',
    4: 'A favor',
}

# Cargar posturas esperadas por ley y agente
def cargar_posturas_esperadas(leyes_path):
    with open(leyes_path, encoding='utf-8') as f:
        leyes = json.load(f)
    posturas = {}
    for ley in leyes:
        ley_id = str(ley['id'])
        posturas[ley_id] = {}
        for agente, postura in AGENTE_TO_POSTURA.items():
            voto_esperado = ley['posturas'].get(postura, {}).get('voto', None)
            posturas[ley_id][agente] = voto_esperado
    return posturas

# Analizar un debate y devolver si hubo cambio y si el voto final es el esperado
def analizar_debate(path, voto_esperado):
    with open(path, encoding='utf-8') as f:
        debate = json.load(f)
    resultados = {}
    for agente in AGENTE_TO_POSTURA:
        votos = []
        rounds = [k for k in debate.keys() if k.lower().startswith('round')]
        #for ronda in ["Round 0", "Round 1", "Round 2"]
        for ronda in rounds:
            v = debate.get(ronda, {}).get(agente, {}).get('voto')
            if v is not None:
                votos.append(v)
        if not votos:
            continue
        hubo_cambio = any(v != votos[0] for v in votos[1:])
        voto_final = votos[-1]
        voto_final_str = VOTO_NUM_TO_STR.get(voto_final, str(voto_final))
        esperado = voto_esperado.get(agente)
        acierto = (voto_final_str == esperado)
        resultados[agente] = {
            'hubo_cambio': hubo_cambio,
            'voto_inicial': VOTO_NUM_TO_STR.get(votos[0], str(votos[0])),
            'voto_final': voto_final_str,
            'voto_esperado': esperado,
            'acierto': acierto
        }
    return resultados

def main():
    leyes_path = 'testing/leyes.json'
    posturas_esperadas = cargar_posturas_esperadas(leyes_path)
    resumen = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for tipo, folder in [('con_research', 'debates/con_research'), ('sin_research', 'debates/sin_research'), ('5_rondas_sin_research', 'debates_5_rondas/sin_research')]:
        for ley_dir in os.listdir(folder):
            if not ley_dir.startswith('ley_'):
                continue
            ley_id = ley_dir.replace('ley_', '')
            ley_path = os.path.join(folder, ley_dir)
            for fname in os.listdir(ley_path):
                if not fname.startswith('debate_') or not fname.endswith('.json'):
                    continue
                debate_path = os.path.join(ley_path, fname)
                resultados = analizar_debate(debate_path, posturas_esperadas.get(ley_id, {}))
                resumen[tipo][ley_id][fname] = resultados
    # Estadísticas globales
    stats = { 'con_research': defaultdict(int), 'sin_research': defaultdict(int), '5_rondas_sin_research': defaultdict(int) }
    for tipo in resumen:
        for ley in resumen[tipo]:
            for debate in resumen[tipo][ley]:
                for agente, res in resumen[tipo][ley][debate].items():
                    if res['hubo_cambio']:
                        stats[tipo]['cambios'] += 1
                        if res['acierto']:
                            stats[tipo]['cambios_y_acierto'] += 1
                    if res['acierto']:
                        stats[tipo]['aciertos'] += 1
    os.makedirs('debates_estadisticas', exist_ok=True)
    with open('debates_estadisticas/medicion_cambios_postura.json', 'w', encoding='utf-8') as f:
        json.dump({'resumen': resumen, 'stats': stats}, f, indent=2, ensure_ascii=False)
    print('Resultados guardados en debates_estadisticas/medicion_cambios_postura.json')

if __name__ == "__main__":
    main()
