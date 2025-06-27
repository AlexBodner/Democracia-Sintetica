import json
import os

def analizar_cambios_aciertos(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    resumen = data['resumen']
    resultados = {}
    for tipo in resumen:
        total_cambios = 0
        cambios_acertados = 0
        inicial_erroneo_final_acierto = 0
        inicial_acierto_final_erroneo = 0
        inicial_erroneo_final_errado = 0
        for ley in resumen[tipo]:
            for debate in resumen[tipo][ley]:
                for agente, info in resumen[tipo][ley][debate].items():
                    if not isinstance(info, dict):
                        continue
                    if info.get('hubo_cambio'):
                        total_cambios += 1
                        inicial_acierto = info.get('voto_inicial') == info.get('voto_esperado')
                        final_acierto = info.get('voto_final') == info.get('voto_esperado')
                        final_errado = info.get('voto_final') != info.get('voto_esperado')
                        if not inicial_acierto and final_acierto:
                            inicial_erroneo_final_acierto += 1
                        if inicial_acierto and not final_acierto:
                            inicial_acierto_final_erroneo += 1
                        if final_acierto:
                            cambios_acertados += 1
                        if not final_acierto and final_errado:
                            inicial_erroneo_final_errado += 1
        total = inicial_erroneo_final_acierto + inicial_erroneo_final_errado
        resultados[tipo] = {
            'total_cambios': total_cambios,
            'inicial_erroneo_final_errado': inicial_erroneo_final_errado,
            #'cambios_acertados': cambios_acertados,
            'inicial_erroneo_final_acierto': inicial_erroneo_final_acierto,
            'inicial_acierto_final_erroneo': inicial_acierto_final_erroneo,
            'porcentaje_cambios_acertados': inicial_erroneo_final_acierto / total * 100 if total else 0,
        }
    return resultados

def main():
    path = 'debates_estadisticas/medicion_cambios_postura.json'
    resultados = analizar_cambios_aciertos(path)
    out_path = 'debates_estadisticas/estadisticas_cambios_aciertos.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f'Estadísticas guardadas en {out_path}')


if __name__ == "__main__":
    main()
