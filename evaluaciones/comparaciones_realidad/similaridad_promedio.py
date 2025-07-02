import os
import json

# Mapeo de nombres de agentes a posturas en leyes.json
AGENTE_TO_POSTURA = {
    'Agente de Izquierda': 'izquierda_fit',
    'Agente de Union Por La Patria': 'centro_izquierda_fdt_otros',
    'Agente de Juntos Por El Cambio': 'centro_derecha_jxc_otros',
    'Agente Liberal': 'derecha_lla_pro_otros',
}

# Mapeo de votos reales a número
VOTO_REALIDAD = {
    'En contra': 0,
    'Critico': 1,
    'Dividido': 2,
    'Apoyo critico': 3,
    'A favor': 4,
}

def cargar_votos_reales(leyes_path):
    with open(leyes_path, encoding='utf-8') as f:
        leyes = json.load(f)
    votos = {}
    for ley in leyes:
        ley_id = str(ley['id'])
        votos[ley_id] = {}
        for agente, postura in AGENTE_TO_POSTURA.items():
            voto = ley['posturas'].get(postura, {}).get('voto', None)
            votos[ley_id][agente] = VOTO_REALIDAD.get(voto, None)
    return votos

def calcular_mae(promedio_path, votos_reales):
    with open(promedio_path, encoding='utf-8') as f:
        promedios = json.load(f)
    resultado = {}
    for ley_id, rondas in promedios.items():
        resultado[ley_id] = {}
        for ronda, agentes in rondas.items():
            resultado[ley_id][ronda] = {}
            for agente, datos in agentes.items():
                voto_real = votos_reales.get(ley_id, {}).get(agente, None)
                voto_prom = datos.get('voto_promedio', None)
                if voto_real is not None and voto_prom is not None:
                    resultado[ley_id][ronda][agente] = abs(voto_prom - voto_real)
                else:
                    resultado[ley_id][ronda][agente] = None
    return resultado

def sumar_maes_por_ronda_agente(mae_path, out_path):
    with open(mae_path, encoding='utf-8') as f:
        maes = json.load(f)
    resultado = {}
    # Acumular por ronda y agente
    for ley, rondas in maes.items():
        for ronda, agentes in rondas.items():
            if ronda not in resultado:
                resultado[ronda] = {}
            for agente, valor in agentes.items():
                if valor is not None:
                    resultado[ronda][agente] = resultado[ronda].get(agente, 0) + valor
    # Calcular mae_total por ronda
    for ronda in resultado:
        mae_total = sum(v for v in resultado[ronda].values() if v is not None)
        resultado[ronda]['mae_total'] = mae_total
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    print(f'Sumatoria de MAEs guardada en {out_path}')

def main():
    os.makedirs('comparaciones_realidad/con_research', exist_ok=True)
    os.makedirs('comparaciones_realidad/sin_research', exist_ok=True)
    os.makedirs('comparaciones_realidad/5_rondas_sin_research', exist_ok=True)
    leyes_path = 'dataset/leyes.json'
    votos_reales = cargar_votos_reales(leyes_path)
    for tipo in ['con_research', 'sin_research', '5_rondas_sin_research']:
        promedio_path = f'promedio_debates/{tipo}/resultados.json'
        resultado = calcular_mae(promedio_path, votos_reales)
        out_path = f'comparaciones_realidad/{tipo}/mae_vs_realidad.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        print(f'Resultados guardados en {out_path}')

if __name__ == "__main__":
    main()
    # Sumar MAEs para con_research y sin_research
    for tipo in ['con_research', 'sin_research', '5_rondas_sin_research']:
        mae_path = f'comparaciones_realidad/{tipo}/mae_vs_realidad.json'
        out_path = f'comparaciones_realidad/{tipo}/mae_sumado_por_ronda.json'
        sumar_maes_por_ronda_agente(mae_path, out_path)
