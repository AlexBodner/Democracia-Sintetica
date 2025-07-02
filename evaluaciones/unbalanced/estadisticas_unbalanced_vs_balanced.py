import os
import glob
import json
from collections import Counter, defaultdict
import numpy as np
# Paths
BALANCED_DIR = 'debates/sin_research'
UNBALANCED_DIR = 'debates_unbalanced'
LEY_JSON = 'dataset/leyes.json'
OUTPUT_DIR = 'debates_estadisticas'
OUTPUT_DIFFS = os.path.join(OUTPUT_DIR, 'unbalanced_vs_balanced_vote_diffs.json')
OUTPUT_STATS = os.path.join(OUTPUT_DIR, 'unbalanced_vote_change_stats.json')
OUTPUT_REAL = os.path.join(OUTPUT_DIR, 'unbalanced_vs_real_vote_stats.json')

# Helper: get final round name (assume 3 rounds, so 'Round 2')
FINAL_ROUND = 'Round 2'

def get_final_votes_from_debate(debate_path):
    with open(debate_path) as f:
        debate = json.load(f)
    if FINAL_ROUND not in debate:
        return {}
    return {ag: d.get('voto') for ag, d in debate[FINAL_ROUND].items() if 'voto' in d}

def get_mode_vote(votes):
    votes = [v for v in votes if v is not None]
    if not votes:
        return None
    return Counter(votes).most_common(1)[0][0]

def get_law_ids_from_dir(base_dir):
    return [d for d in os.listdir(base_dir) if d.startswith('ley_')]

def normalize_agent_name(name):
    # Quita sufijos numéricos y el prefijo 'de' si existe
    import re
    name = name.strip()
    name = re.sub(r'\s*\d+$', '', name)  # Quita número al final
    name = re.sub(r'^Agente de ', 'Agente ', name)  # Unifica 'Agente de X' y 'Agente X'
    return name

# Mapeo manual de nombres normalizados de agentes a claves de postura en leyes.json
AGENT_TO_POSTURA = {
    'Agente Liberal': 'derecha_lla_pro_otros',
    'Agente Liberal 1': 'derecha_lla_pro_otros',
    'Agente Liberal 2': 'derecha_lla_pro_otros',
    'Agente Liberal 3': 'derecha_lla_pro_otros',
    'Agente Liberal 4': 'derecha_lla_pro_otros',
    'Agente Izquierda': 'izquierda_fit',
    'Agente Izquierda 1': 'izquierda_fit',
    'Agente Izquierda 2': 'izquierda_fit',
    'Agente Izquierda 3': 'izquierda_fit',
    'Agente Izquierda 4': 'izquierda_fit',
    'Agente UxP': 'centro_izquierda_fdt_otros',
    'Agente UxP 1': 'centro_izquierda_fdt_otros',
    'Agente UxP 2': 'centro_izquierda_fdt_otros',
    'Agente UxP 3': 'centro_izquierda_fdt_otros',
    'Agente UxP 4': 'centro_izquierda_fdt_otros',
    'Agente de Union Por La Patria': 'centro_izquierda_fdt_otros',
    'Agente de Juntos Por El Cambio': 'centro_derecha_jxc_otros',
    'Agente JxC': 'centro_derecha_jxc_otros',
    'Agente JxC 1': 'centro_derecha_jxc_otros',
    'Agente JxC 2': 'centro_derecha_jxc_otros',
    'Agente JxC 3': 'centro_derecha_jxc_otros',
    'Agente JxC 4': 'centro_derecha_jxc_otros',
}

def calcular_estadisticas_cambios_aciertos_y_mae_unbalanced_vs_real(real_vote_stats):
    resultados = {}
    global_total_cambios = 0
    global_aciertos = 0
    global_errados = 0
    global_sum_abs_diff = 0
    global_count_diff = 0
    for ley in real_vote_stats:
        for combinacion in real_vote_stats[ley]:
            total_cambios = 0
            aciertos = 0
            errados = 0
            sum_abs_diff = 0
            count_diff = 0
            for entry in real_vote_stats[ley][combinacion]:
                unbalanced_vote = entry.get('unbalanced_vote')
                real_vote = entry.get('real_vote')
                if unbalanced_vote is not None and real_vote is not None:
                    total_cambios += 1
                    global_total_cambios += 1
                    if unbalanced_vote == real_vote:
                        aciertos += 1
                        global_aciertos += 1
                    else:
                        errados += 1
                        global_errados += 1
                    # MAE
                    if isinstance(unbalanced_vote, (int, float)) and isinstance(real_vote, (int, float)):
                        sum_abs_diff += abs(unbalanced_vote - real_vote)
                        count_diff += 1
                        global_sum_abs_diff += abs(unbalanced_vote - real_vote)
                        global_count_diff += 1
            total = aciertos + errados
            mae = sum_abs_diff / count_diff if count_diff else None
            key = f"{ley}/{combinacion}"
            resultados[key] = {
                'total_cambios': total_cambios,
                'aciertos': aciertos,
                'errados': errados,
                'porcentaje_cambios_acertados': aciertos / total * 100 if total else 0,
                'mae': mae
            }
    # Promedios globales
    global_mae = global_sum_abs_diff / global_count_diff if global_count_diff else None
    promedios_globales = {
        'total_cambios': global_total_cambios,
        'aciertos': global_aciertos,
        'errados': global_errados,
        'porcentaje_cambios_acertados': global_aciertos / global_total_cambios * 100 if global_total_cambios else 0,
        'mae': global_mae
    }
    return resultados, promedios_globales

def calcular_estadisticas_por_agente_unbalanced_vs_real(real_vote_stats):
    resultados = {}
    for ley in real_vote_stats:
        for combinacion in real_vote_stats[ley]:
            agentes = {}
            for entry in real_vote_stats[ley][combinacion]:
                ag = entry.get('agent')
                unbalanced_vote = entry.get('unbalanced_vote')
                real_vote = entry.get('real_vote')
                if ag is None or unbalanced_vote is None or real_vote is None:
                    continue
                if ag not in agentes:
                    agentes[ag] = {
                        'total_cambios': 0,
                        'aciertos': 0,
                        'errados': 0,
                        'sum_abs_diff': 0,
                        'count_diff': 0
                    }
                agentes[ag]['total_cambios'] += 1
                if unbalanced_vote == real_vote:
                    agentes[ag]['aciertos'] += 1
                else:
                    agentes[ag]['errados'] += 1
                if isinstance(unbalanced_vote, (int, float)) and isinstance(real_vote, (int, float)):
                    agentes[ag]['sum_abs_diff'] += abs(unbalanced_vote - real_vote)
                    agentes[ag]['count_diff'] += 1
            # Calcular métricas finales por agente
            for ag in agentes:
                total = agentes[ag]['total_cambios']
                aciertos = agentes[ag]['aciertos']
                errados = agentes[ag]['errados']
                mae = agentes[ag]['sum_abs_diff'] / agentes[ag]['count_diff'] if agentes[ag]['count_diff'] else None
                agentes[ag] = {
                    'total_cambios': total,
                    'aciertos': aciertos,
                    'errados': errados,
                    'porcentaje_cambios_acertados': aciertos / total * 100 if total else 0,
                    'mae': mae
                }
            resultados.setdefault(ley, {})[combinacion] = agentes
    return resultados

def calcular_promedios_por_agente(stats_real_por_agente):
    # stats_real_por_agente: ley -> combinacion -> agente -> stats
    from collections import defaultdict
    promedios = defaultdict(lambda: defaultdict(lambda: {'total_cambios': 0, 'aciertos': 0, 'errados': 0, 'sum_porcentaje': 0, 'sum_mae': 0, 'count': 0, 'count_mae': 0}))
    for ley in stats_real_por_agente:
        for combinacion in stats_real_por_agente[ley]:
            for agente, stats in stats_real_por_agente[ley][combinacion].items():
                p = promedios[combinacion][agente]
                p['total_cambios'] += stats['total_cambios']
                p['aciertos'] += stats['aciertos']
                p['errados'] += stats['errados']
                p['sum_porcentaje'] += stats['porcentaje_cambios_acertados']
                p['count'] += 1
                if stats['mae'] is not None:
                    p['sum_mae'] += stats['mae']
                    p['count_mae'] += 1
    # Calcular promedios finales
    resultado = {}
    for combinacion in promedios:
        resultado[combinacion] = {}
        for agente, p in promedios[combinacion].items():
            resultado[combinacion][agente] = {
                'total_cambios': p['total_cambios'],
                'aciertos': p['aciertos'],
                'errados': p['errados'],
                'porcentaje_cambios_acertados': p['sum_porcentaje'] / p['count'] if p['count'] else 0,
                'mae': p['sum_mae'] / p['count_mae'] if p['count_mae'] else None
            }
    return resultado

def calcular_mae_por_agente_combinacion_balanceado_vs_desbalanceado(vote_diffs):
    # vote_diffs: law -> combinacion -> list of diffs (cada diff tiene agent, unbalanced_vote, balanced_mode_vote)
    maes = {}  # combinacion -> agente -> [abs_diff,...]
    for law in vote_diffs:
        for combinacion in vote_diffs[law]:
            for entry in vote_diffs[law][combinacion]:
                ag = entry.get('agent')
                unbalanced_vote = entry.get('unbalanced_vote')
                balanced_vote = entry.get('balanced_mode_vote')
                if ag is None or unbalanced_vote is None or balanced_vote is None:
                    continue
                maes.setdefault(combinacion, {}).setdefault(ag, []).append(abs(unbalanced_vote - balanced_vote) if isinstance(unbalanced_vote, (int, float)) and isinstance(balanced_vote, (int, float)) else None)
    # Calcular promedio MAE por agente y combinacion
    maes_prom = {}
    for combinacion in maes:
        maes_prom[combinacion] = {}
        for ag in maes[combinacion]:
            vals = [v for v in maes[combinacion][ag] if v is not None]
            mae = sum(vals) / len(vals) if vals else None
            maes_prom[combinacion][ag] = mae
    return maes_prom

def detectar_cambio_por_mayoria_ideologica(vote_diffs):
    # Definir grupos ideológicos
    derecha = {'Agente Liberal', 'Agente Liberal 1', 'Agente Liberal 2', 'Agente Liberal 3', 'Agente Liberal 4',
               'Agente de Juntos Por El Cambio', 'Agente JxC', 'Agente JxC 1', 'Agente JxC 2', 'Agente JxC 3', 'Agente JxC 4'}
    izquierda = {'Agente Izquierda', 'Agente Izquierda 1', 'Agente Izquierda 2', 'Agente Izquierda 3', 'Agente Izquierda 4',
                 'Agente UxP', 'Agente UxP 1', 'Agente UxP 2', 'Agente UxP 3', 'Agente UxP 4', 'Agente de Union Por La Patria'}
    combinaciones_mayoria = {'combinacion_0', 'combinacion_1', 'combinacion_2', 'combinacion_3'}
    resultados = {}
    for law in vote_diffs:
        for combinacion in vote_diffs[law]:
            if combinacion not in combinaciones_mayoria:
                continue
            # Para cada debate, identificar el agente en minoría y si cambió su voto respecto al modo balanceado
            for entry in vote_diffs[law][combinacion]:
                ag = entry.get('agent')
                unbalanced_vote = entry.get('unbalanced_vote')
                balanced_vote = entry.get('balanced_mode_vote')
                # Determinar grupo del agente
                if ag in derecha:
                    grupo = 'derecha'
                elif ag in izquierda:
                    grupo = 'izquierda'
                else:
                    grupo = 'otro'
                # Si el agente cambió su voto (unbalanced != balanced), y está en minoría, lo contamos
                # Para saber si está en minoría, necesitamos saber qué agentes hay en la combinación
                # Suponemos que si solo hay un agente de su grupo, está en minoría
                # (esto es una simplificación, para mayor precisión habría que leer los debates y ver los presentes)
                # Aquí, solo contamos los cambios de voto de agentes de derecha o izquierda
                key = f"{law}/{combinacion}/{ag}"
                if unbalanced_vote != balanced_vote:
                    resultados.setdefault(key, {'grupo': grupo, 'cambio_por_mayoria': 0, 'total': 0})
                    resultados[key]['cambio_por_mayoria'] += 1
                resultados.setdefault(key, {'grupo': grupo, 'cambio_por_mayoria': 0, 'total': 0})
                resultados[key]['total'] += 1
    # Resumir por grupo y combinacion
    resumen = {}
    for key, val in resultados.items():
        _, combinacion, ag = key.split('/', 2)
        grupo = val['grupo']
        resumen.setdefault(combinacion, {}).setdefault(grupo, {'cambio_por_mayoria': 0, 'total': 0})
        resumen[combinacion][grupo]['cambio_por_mayoria'] += val['cambio_por_mayoria']
        resumen[combinacion][grupo]['total'] += val['total']
    # Calcular porcentaje
    for combinacion in resumen:
        for grupo in resumen[combinacion]:
            total = resumen[combinacion][grupo]['total']
            cambios = resumen[combinacion][grupo]['cambio_por_mayoria']
            resumen[combinacion][grupo]['porcentaje_cambio_por_mayoria'] = cambios / total * 100 if total else 0
    return resumen

def detectar_cambio_por_mayoria_ideologica_entre_rondas(unbalanced_dir):
    import re
    derecha = {'Agente Liberal', 'Agente Liberal 1', 'Agente Liberal 2', 'Agente Liberal 3', 'Agente Liberal 4',
               'Agente de Juntos Por El Cambio', 'Agente JxC', 'Agente JxC 1', 'Agente JxC 2', 'Agente JxC 3', 'Agente JxC 4'}
    izquierda = {'Agente Izquierda', 'Agente Izquierda 1', 'Agente Izquierda 2', 'Agente Izquierda 3', 'Agente Izquierda 4',
                 'Agente UxP', 'Agente UxP 1', 'Agente UxP 2', 'Agente UxP 3', 'Agente UxP 4', 'Agente de Union Por La Patria'}
    combinaciones_mayoria = {'combinacion_0', 'combinacion_1', 'combinacion_2', 'combinacion_3'}
    resultados = {}
    for ley in get_law_ids_from_dir(unbalanced_dir):
        law_path = os.path.join(unbalanced_dir, ley)
        if not os.path.isdir(law_path):
            continue
        for combinacion in os.listdir(law_path):
            if combinacion not in combinaciones_mayoria:
                continue
            comb_path = os.path.join(law_path, combinacion)
            if not os.path.isdir(comb_path):
                continue
            for debate_path in glob.glob(os.path.join(comb_path, 'debate_iteracion_*.json')):
                with open(debate_path) as f:
                    debate = json.load(f)
                # Detectar agentes presentes
                agentes_presentes = set()
                for ronda in debate:
                    if not re.match(r'^Round', ronda):
                        continue
                    for ag in debate[ronda]:
                        agentes_presentes.add(ag)
                # Contar cuántos de cada grupo
                derecha_presentes = [a for a in agentes_presentes if a in derecha]
                izquierda_presentes = [a for a in agentes_presentes if a in izquierda]
                # Detectar minoría y mayoría
                if len(derecha_presentes) == 1 and len(izquierda_presentes) > 1:
                    minoritario = derecha_presentes[0]
                    grupo_mayoritario = 'izquierda'
                    agentes_mayoria = izquierda_presentes
                elif len(izquierda_presentes) == 1 and len(derecha_presentes) > 1:
                    minoritario = izquierda_presentes[0]
                    grupo_mayoritario = 'derecha'
                    agentes_mayoria = derecha_presentes
                else:
                    print("No hay una minoría clara en el debate:", debate_path)
                    continue  # No hay minoría clara
                # Voto inicial y final del minoritario
                ronda_final = max([r for r in debate if re.match(r'^Round', r)], key=lambda x: int(x.split()[1]))
                voto_inicial:int = int(debate["Round 0"][minoritario]['voto'])
                voto_final:int = debate[ronda_final][minoritario]['voto']
                # Voto mayoritario (modo entre los agentes de la mayoría en la ronda final)
                votos_mayoria = [debate[ronda_final][ag]['voto'] for ag in agentes_mayoria if 'voto' in debate[ronda_final][ag]]
                if votos_mayoria:
                    from collections import Counter
                    voto_mayoritario = np.mean(votos_mayoria)
                else:
                    voto_mayoritario = None
                # ¿El minoritario cambió su voto hacia la mayoría?
                cambio_hacia_mayoria = abs(voto_inicial - voto_mayoritario) > abs(voto_final - voto_mayoritario)
                if cambio_hacia_mayoria:
                    print(f"Agente {minoritario} cambió su voto hacia la mayoría en ley {ley}, combinacion {combinacion}, debate {os.path.basename(debate_path)}")
                key = f"{ley}/{combinacion}/{minoritario}"
                resultados.setdefault(key, {'cambio_hacia_mayoria': 0, 'total': 0})
                if cambio_hacia_mayoria:
                    resultados[key]['cambio_hacia_mayoria'] += 1
                resultados[key]['total'] += 1
    # Resumir por grupo y combinacion
    resumen = {}
    for key, val in resultados.items():
        _, combinacion, ag = key.split('/', 2)
        resumen.setdefault(combinacion, {'cambio_hacia_mayoria': 0, 'total': 0})
        resumen[combinacion]['cambio_hacia_mayoria'] += val['cambio_hacia_mayoria']
        resumen[combinacion]['total'] += val['total']
    for combinacion in resumen:
        total = resumen[combinacion]['total']
        cambios = resumen[combinacion]['cambio_hacia_mayoria']
        resumen[combinacion]['porcentaje_cambio_hacia_mayoria'] = cambios / total * 100 if total else 0
    return resumen

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # 1. Get mode votes from balanced debates
    balanced_modes = defaultdict(dict)  # law -> agent -> mode_vote
    for law in get_law_ids_from_dir(BALANCED_DIR):
        agent_votes = defaultdict(list)
        for debate_path in glob.glob(os.path.join(BALANCED_DIR, law, 'debate_*.json')):
            votes = get_final_votes_from_debate(debate_path)
            for ag, v in votes.items():
                agent_votes[ag].append(v)
        for ag, votes in agent_votes.items():
            balanced_modes[law][ag] = get_mode_vote(votes)
    # 2. Compare unbalanced debates to balanced mode, grouped by combination
    vote_diffs = defaultdict(lambda: defaultdict(list))  # law -> combinacion -> list of diffs
    vote_change_count = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # law -> combinacion -> agent -> count
    real_vote_stats = defaultdict(lambda: defaultdict(list))  # law -> combinacion -> list of real vote diffs
    # Load real votes
    with open(LEY_JSON) as f:
        leyes = json.load(f)
    real_votes = {f"ley_{ley['id']}": ley['posturas'] for ley in leyes}
    # Iterate unbalanced
    for law in get_law_ids_from_dir(UNBALANCED_DIR):
        law_path = os.path.join(UNBALANCED_DIR, law)
        if not os.path.isdir(law_path):
            continue
        for combinacion in os.listdir(law_path):
            comb_path = os.path.join(law_path, combinacion)
            if not os.path.isdir(comb_path):
                continue
            for debate_path in glob.glob(os.path.join(comb_path, 'debate_iteracion_*.json')):
                votes = get_final_votes_from_debate(debate_path)
                for ag, v in votes.items():
                    ag_norm = normalize_agent_name(ag)
                    mode_vote = balanced_modes.get(law, {}).get(ag_norm)
                    if mode_vote is not None and v is not None:
                        if v != mode_vote:
                            vote_diffs[law][combinacion].append({
                                'law': law,
                                'combinacion': combinacion,
                                'debate': os.path.basename(debate_path),
                                'agent': ag,
                                'unbalanced_vote': v,
                                'balanced_mode_vote': mode_vote
                            })
                            vote_change_count[law][combinacion][ag] += 1
                    # Real vote comparison
                    postura_key = AGENT_TO_POSTURA.get(ag, AGENT_TO_POSTURA.get(ag_norm))
                    real_v = None
                    if postura_key:
                        real_posturas = real_votes.get(law, {})
                        if postura_key in real_posturas:
                            real_v = real_posturas[postura_key].get('voto')
                            # Map "A favor"/"En contra"/"Abstención" a valores numéricos si es posible
                            if real_v == "A favor":
                                real_v_num = 4
                            elif real_v == "En contra":
                                real_v_num = 0
                            elif real_v == "Abstención" or real_v == "Apoyo critico":
                                real_v_num = 2
                            else:
                                real_v_num = None
                        else:
                            real_v_num = None
                    else:
                        real_v_num = None
                    if real_v_num is not None and v is not None:
                        real_vote_stats[law][combinacion].append({
                            'law': law,
                            'combinacion': combinacion,
                            'debate': os.path.basename(debate_path),
                            'agent': ag,
                            'unbalanced_vote': v,
                            'real_vote': real_v_num,
                            'diff': abs(v - real_v_num) if isinstance(v, (int, float)) else None
                        })
    # Save results
    with open(OUTPUT_DIFFS, 'w') as f:
        json.dump(vote_diffs, f, indent=2, ensure_ascii=False)
    with open(OUTPUT_STATS, 'w') as f:
        json.dump(vote_change_count, f, indent=2, ensure_ascii=False)
    with open(OUTPUT_REAL, 'w') as f:
        json.dump(real_vote_stats, f, indent=2, ensure_ascii=False)
    # NUEVO: Estadísticas de aciertos/errores y MAE para unbalanced vs real
    out_stats_real = os.path.join(OUTPUT_DIR, 'estadisticas_cambios_aciertos_unbalanced_vs_real.json')
    stats_real, promedios_globales = calcular_estadisticas_cambios_aciertos_y_mae_unbalanced_vs_real(real_vote_stats)
    with open(out_stats_real, 'w', encoding='utf-8') as f:
        json.dump(stats_real, f, indent=2, ensure_ascii=False)
    # Guardar promedios por combinacion como antes
    promedios_por_combinacion = {}
    combinacion_stats = defaultdict(list)
    for key, stats in stats_real.items():
        _, combinacion = key.split('/', 1)
        combinacion_stats[combinacion].append(stats)
    for combinacion, stats_list in combinacion_stats.items():
        n = len(stats_list)
        if n == 0:
            continue
        total_cambios = sum(s['total_cambios'] for s in stats_list)
        aciertos = sum(s['aciertos'] for s in stats_list)
        errados = sum(s['errados'] for s in stats_list)
        porcentaje_cambios_acertados = (sum(s['porcentaje_cambios_acertados'] for s in stats_list) / n) if n else 0
        maes = [s['mae'] for s in stats_list if s['mae'] is not None]
        mae_prom = sum(maes) / len(maes) if maes else None
        promedios_por_combinacion[combinacion] = {
            'total_cambios': total_cambios,
            'aciertos': aciertos,
            'errados': errados,
            'porcentaje_cambios_acertados': porcentaje_cambios_acertados,
            'mae': mae_prom
        }
    # Guardar promedios en archivo aparte
    out_stats_real_prom = os.path.join(OUTPUT_DIR, 'estadisticas_cambios_aciertos_unbalanced_vs_real_promedios.json')
    with open(out_stats_real_prom, 'w', encoding='utf-8') as f:
        json.dump({
            'promedios_por_combinacion': promedios_por_combinacion,
            'promedios_globales': promedios_globales
        }, f, indent=2, ensure_ascii=False)
    # Guardar estadísticas por agente en cada combinación
    out_stats_real_agente = os.path.join(OUTPUT_DIR, 'estadisticas_cambios_aciertos_unbalanced_vs_real_por_agente.json')
    stats_real_por_agente = calcular_estadisticas_por_agente_unbalanced_vs_real(real_vote_stats)
    with open(out_stats_real_agente, 'w', encoding='utf-8') as f:
        json.dump(stats_real_por_agente, f, indent=2, ensure_ascii=False)
    # Guardar promedios por agente a lo largo de todas las leyes
    out_stats_real_agente_prom = os.path.join(OUTPUT_DIR, 'estadisticas_cambios_aciertos_unbalanced_vs_real_por_agente_promedios.json')
    with open(out_stats_real_agente, 'r', encoding='utf-8') as f:
        stats_real_por_agente = json.load(f)
    promedios_por_agente = calcular_promedios_por_agente(stats_real_por_agente)
    with open(out_stats_real_agente_prom, 'w', encoding='utf-8') as f:
        json.dump(promedios_por_agente, f, indent=2, ensure_ascii=False)
    # Guardar MAE por agente y combinacion entre votos balanceados y desbalanceados
    out_mae_agente_comb = os.path.join(OUTPUT_DIR, 'mae_balanceado_vs_desbalanceado_por_agente.json')
    maes_agente_comb = calcular_mae_por_agente_combinacion_balanceado_vs_desbalanceado(vote_diffs)
    with open(out_mae_agente_comb, 'w', encoding='utf-8') as f:
        json.dump(maes_agente_comb, f, indent=2, ensure_ascii=False)
    # Guardar estadística de cambio por mayoría ideológica
    out_mayoria = os.path.join(OUTPUT_DIR, 'estadisticas_cambio_por_mayoria_ideologica.json')
    mayoria_stats = detectar_cambio_por_mayoria_ideologica(vote_diffs)
    with open(out_mayoria, 'w', encoding='utf-8') as f:
        json.dump(mayoria_stats, f, indent=2, ensure_ascii=False)
    # Guardar estadística de cambio hacia mayoría ideológica entre rondas
    out_mayoria_rondas = os.path.join(OUTPUT_DIR, 'estadisticas_cambio_hacia_mayoria_ideologica_entre_rondas.json')
    mayoria_rondas_stats = detectar_cambio_por_mayoria_ideologica_entre_rondas(UNBALANCED_DIR)
    with open(out_mayoria_rondas, 'w', encoding='utf-8') as f:
        json.dump(mayoria_rondas_stats, f, indent=2, ensure_ascii=False)
    print(f"Saved: {OUTPUT_DIFFS}, {OUTPUT_STATS}, {OUTPUT_REAL}, {out_stats_real}, {out_stats_real_prom}, {out_stats_real_agente}, {out_mae_agente_comb}, {out_mayoria}, {out_mayoria_rondas}")

if __name__ == '__main__':
    main()
