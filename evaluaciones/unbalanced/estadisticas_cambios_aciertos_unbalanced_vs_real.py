import json
import os

def analizar_cambios_aciertos_unbalanced_vs_real(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    resultados = {}
    for ley in data:
        for combinacion in data[ley]:
            total_cambios = 0
            cambios_acertados = 0
            inicial_erroneo_final_acierto = 0
            inicial_acierto_final_erroneo = 0
            inicial_erroneo_final_errado = 0
            for entry in data[ley][combinacion]:
                # No hay voto_inicial, solo unbalanced_vote y real_vote
                unbalanced_vote = entry.get('unbalanced_vote')
                real_vote = entry.get('real_vote')
                # Consideramos "acierto" si unbalanced_vote == real_vote
                hubo_cambio = unbalanced_vote != real_vote
                if hubo_cambio:
                    total_cambios += 1
                    # No hay voto_inicial, así que solo medimos acierto/fallo final
                    if unbalanced_vote == real_vote:
                        inicial_erroneo_final_acierto += 1
                        cambios_acertados += 1
                    else:
                        inicial_erroneo_final_errado += 1
            total = inicial_erroneo_final_acierto + inicial_erroneo_final_errado
            key = f"{ley}/{combinacion}"
            resultados[key] = {
                'total_cambios': total_cambios,
                'inicial_erroneo_final_errado': inicial_erroneo_final_errado,
                'inicial_erroneo_final_acierto': inicial_erroneo_final_acierto,
                'inicial_acierto_final_erroneo': 0,  # No se puede calcular sin voto_inicial
                'porcentaje_cambios_acertados': inicial_erroneo_final_acierto / total * 100 if total else 0,
            }
    return resultados

def main():
    path = 'debates_estadisticas/unbalanced_vs_real_vote_stats.json'
    resultados = analizar_cambios_aciertos_unbalanced_vs_real(path)
    out_path = 'debates_estadisticas/estadisticas_cambios_aciertos_unbalanced_vs_real.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f'Estadísticas guardadas en {out_path}')

if __name__ == "__main__":
    main()
