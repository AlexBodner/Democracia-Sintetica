import os
import json
from collections import Counter, defaultdict

def load_cambios(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def estadisticas_cambios(cambios_dict):
    cambios_norma2 = Counter()  # agente -> cantidad de cambios con norma >=2
    cambios_por_ronda = Counter()  # (from_round, to_round) -> cantidad
    cambios_por_ronda_norma2 = Counter()  # (from_round, to_round) -> cantidad (solo norma >=2)
    for ley, agentes in cambios_dict.items():
        for agente, debates in agentes.items():
            for debate, cambios in debates.items():
                for cambio in cambios:
                    # Cambios con norma >=2
                    if abs(cambio['to_vote'] - cambio['from_vote']) >= 2:
                        cambios_norma2[agente] += 1
                        cambios_por_ronda_norma2[(cambio['from_round'], cambio['to_round'])] += 1
                    # Cambios por ronda (sin restricción de norma)
                    cambios_por_ronda[(cambio['from_round'], cambio['to_round'])] += 1
    return cambios_norma2, cambios_por_ronda, cambios_por_ronda_norma2

def main():
    base_dirs = [
        ('cambios_postura/con_research/cambios_por_ley_agente.json', 'con_research'),
        ('cambios_postura/sin_research/cambios_por_ley_agente.json', 'sin_research')
    ]
    os.makedirs('debates_estadisticas', exist_ok=True)
    resumen = {}
    for path, tipo in base_dirs:
        cambios = load_cambios(path)
        cambios_norma2, cambios_por_ronda, cambios_por_ronda_norma2 = estadisticas_cambios(cambios)
        resumen[tipo] = {
            'cambios_norma_mayor_igual_2_por_agente': dict(cambios_norma2),
            'cambios_por_ronda': {f"{k[0]}->{k[1]}": v for k, v in sorted(cambios_por_ronda.items())},
            'cambios_por_ronda_norma_mayor_igual_2': {f"{k[0]}->{k[1]}": v for k, v in sorted(cambios_por_ronda_norma2.items())}
        }
        # Guardar estadística individual
        with open(f'debates_estadisticas/estadisticas_{tipo}.json', 'w', encoding='utf-8') as f:
            json.dump(resumen[tipo], f, indent=2, ensure_ascii=False)
    # Guardar resumen general
    with open('debates_estadisticas/estadisticas_generales.json', 'w', encoding='utf-8') as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)
    print('Estadísticas guardadas en debates_estadisticas/')

if __name__ == "__main__":
    main()
