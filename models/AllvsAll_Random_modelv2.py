import random
import itertools
from collections import defaultdict
from typing import List, Dict, Any
import pandas as pd

""" Esta version maximiza las combinaciones de parejas diferentes: todos juegan con todos
    - Mas rondas
"""

def generar_torneo_todos_contra_todos(
    jugadores: List[str],
    num_canchas: int,
    seed: int | None = None
) -> List[Dict[str, Any]]:
    if seed is not None:
        random.seed(seed)

    n = len(jugadores)
    if n < 4:
        raise ValueError("Se requieren al menos 4 jugadores para dobles 2vs2.")

    todos_pares = set(tuple(sorted(p)) for p in itertools.combinations(jugadores, 2))

    partidos_jugados = defaultdict(int)
    descansos = defaultdict(int)
    last_rest_round = {j: 0 for j in jugadores}  # para control estricto de descansos
    partner_counts = defaultdict(int)  # cuántas veces dos jugadores han sido pareja
    enfrentamientos_cubiertos = set()
    rondas = []
    max_iter = 20000
    iter_count = 0
    ronda_idx = 0

    # parámetros de ajuste (puedes modificar para cambiar comportamiento)
    PARTNER_PENALTY = 5.0    # cuánto penaliza volver a ser pareja (mayor => menos repeticiones)
    PLAYED_PENALTY = 0.5     # penaliza jugadores con muchos partidos
    NEW_OPP_BONUS = 1.0      # premia nuevas combinaciones adversarias (cruces entre parejas)

    # Aux: comprobar si alguien ya descansó 0 veces (para forzar que primero descansen los que no han descansado)
    def existe_que_no_ha_descansado():
        return any(descansos[j] == 0 for j in jugadores)

    while enfrentamientos_cubiertos != todos_pares and iter_count < max_iter:
        iter_count += 1
        ronda_idx += 1

        # ordenar por partidos_jugados asc, luego por descansos asc (los que menos han jugado y descansado primero)
        jugadores_ordenados = sorted(
            jugadores,
            key=lambda g: (partidos_jugados[g], descansos[g], last_rest_round[g])
        )
        disponibles = set(jugadores_ordenados)

        # === CONTROL DE DESCANSOS ESTRICTO ===
        sobrantes = len(disponibles) % 4
        descansan = []
        if sobrantes > 0:
            # si aún hay jugadores que no han descansado, elegir solo entre ellos
            if existe_que_no_ha_descansado():
                candidatos = [j for j in disponibles if descansos[j] == 0]
            else:
                # elegir quienes menos hayan descansado; si empate, elegir los con menor last_rest_round (más tiempo desde último descanso)
                min_desc = min(descansos.values()) if descansos else 0
                candidatos = [j for j in disponibles if descansos[j] == min_desc]

            random.shuffle(candidatos)
            seleccion = candidatos[:sobrantes]
            for j in seleccion:
                descansos[j] += 1
                last_rest_round[j] = ronda_idx
            descansan = seleccion
            disponibles -= set(descansan)
        # ======================================

        partidos_ronda = []
        # intentamos llenar canchas
        for cancha_idx in range(num_canchas):
            if len(disponibles) >= 4:
                candidatos = list(disponibles)
                # heurística: priorizar candidatos que han jugado menos y descansado más tiempo
                candidatos.sort(key=lambda g: (partidos_jugados[g], last_rest_round[g]))

                best_quad = None
                best_score = -1e9
                # limitar pruebas para desempeño
                trials = min(200, max(40, len(candidatos) * 3))
                for _ in range(trials):
                    quad = random.sample(candidatos, 4)
                    # generar particiones de parejas
                    partitions = [
                        ((quad[0], quad[1]), (quad[2], quad[3])),
                        ((quad[0], quad[2]), (quad[1], quad[3])),
                        ((quad[0], quad[3]), (quad[1], quad[2])),
                    ]
                    for p1, p2 in partitions:
                        # 1) contar cuántos enfrentamientos nuevos entre p1 y p2
                        new_cover = 0
                        for a in p1:
                            for b in p2:
                                pair = tuple(sorted((a, b)))
                                if pair not in enfrentamientos_cubiertos:
                                    new_cover += 1

                        # 2) penalizar si miembros de p1 ya han sido pareja muchas veces entre sí (queremos evitar repetir parejas)
                        partner_pen = 0
                        for pair_in_team in itertools.combinations(p1, 2):
                            partner_pen += partner_counts[tuple(sorted(pair_in_team))]
                        for pair_in_team in itertools.combinations(p2, 2):
                            partner_pen += partner_counts[tuple(sorted(pair_in_team))]

                        # 3) penalizar jugadores con muchos partidos ya jugados (quieren equilibrio)
                        worst_played = max(partidos_jugados[a] for a in p1 + p2)

                        # 4) bonus si entre las parejas hay más "nuevos enfrentamientos" (refuerza NEW_OPP_BONUS)
                        score = (NEW_OPP_BONUS * new_cover) - (PARTNER_PENALTY * partner_pen) - (PLAYED_PENALTY * worst_played)

                        # desempate adicional: preferir pares donde cada jugador tenga menos partidos jugados
                        avg_played = sum(partidos_jugados[a] for a in p1 + p2) / 4.0
                        score -= 0.01 * avg_played

                        if score > best_score:
                            best_score = score
                            best_quad = (p1, p2)

                if best_quad is None:
                    take = list(disponibles)[:4]
                    p1 = (take[0], take[1])
                    p2 = (take[2], take[3])
                else:
                    p1, p2 = best_quad

                partidos_ronda.append({
                    "cancha": cancha_idx + 1,
                    "pareja1": tuple(p1),
                    "pareja2": tuple(p2),
                    "ayudantes": [],
                    "valido_para": {p1[0]: True, p1[1]: True, p2[0]: True, p2[1]: True}
                })
                disponibles -= set(p1) | set(p2)

                # actualizar partner_counts para reflejar nueva pareja (aunque pueda ser validado o no será marcado después)
                for team in (p1, p2):
                    pair = tuple(sorted(team))
                    partner_counts[pair] += 1

            else:
                # falta menos de 4 disponibles: intentar completar con ayudantes si es necesario
                # pero no dejar que alguien descanse dos veces antes de que todos hayan descansado al menos una.
                if len(disponibles) == 0:
                    break

                # si aún no todos han descansado, no usamos como ayudantes a quienes ya descansaron 2 veces si hay alternativa
                needed = 4 - len(disponibles)
                no_disp = [g for g in jugadores if g not in disponibles]
                if not no_disp:
                    break

                # seleccionar ayudantes entre los que hayan jugado más (menos impacto competitivo)
                no_disp_sorted = sorted(no_disp, key=lambda g: (-partidos_jugados[g], descansos[g], last_rest_round[g]))
                ayudantes_seleccionados = no_disp_sorted[:needed]

                take4 = list(disponibles) + ayudantes_seleccionados
                if len(take4) > 4:
                    take4 = take4[:4]
                p1 = (take4[0], take4[1])
                p2 = (take4[2], take4[3])

                valido_dict = {}
                for pl in p1 + p2:
                    valido_dict[pl] = (pl not in ayudantes_seleccionados)

                partidos_ronda.append({
                    "cancha": cancha_idx + 1,
                    "pareja1": tuple(p1),
                    "pareja2": tuple(p2),
                    "ayudantes": list(ayudantes_seleccionados),
                    "valido_para": valido_dict
                })

                # actualizar partner_counts igualmente (aunque ayudantes no sumen partidos)
                for team in (p1, p2):
                    pair = tuple(sorted(team))
                    partner_counts[pair] += 1

                disponibles -= set(take4)

        # actualizar enfrentamientos y conteos solo con partidos de la ronda
        for partido in partidos_ronda:
            p1 = partido["pareja1"]
            p2 = partido["pareja2"]
            # añadir enfrentamientos cubiertos solo si al menos uno de los dos jugadores en el cruce lo tiene como válido
            for a in p1:
                for b in p2:
                    pair = tuple(sorted((a, b)))
                    # si alguno de los dos tiene el partido válido para conteo, considerar que ese enfrentamiento fue "jugado"
                    if partido["valido_para"].get(a, False) or partido["valido_para"].get(b, False):
                        enfrentamientos_cubiertos.add(pair)
            # actualizar partidos_jugados sólo para jugadores que son válidos en este partido
            for pl, valido in partido["valido_para"].items():
                if valido:
                    partidos_jugados[pl] += 1

        rondas.append({
            "ronda": ronda_idx,
            "partidos": partidos_ronda,
            "descansan": descansan
        })

        # seguridad: si no se generaron partidos en esta iteración rompemos
        if not partidos_ronda:
            break

    meta_alcanzada = (enfrentamientos_cubiertos == todos_pares)

    resumen_df = pd.DataFrame({
        "jugador": jugadores,
        "partidos_jugados": [partidos_jugados[j] for j in jugadores],
        "descansos": [descansos[j] for j in jugadores]
    }).sort_values(by=["partidos_jugados", "descansos"], ascending=[False, True]).reset_index(drop=True)

    return {
        "rondas": rondas,
        "enfrentamientos_cubiertos": enfrentamientos_cubiertos,
        "todos_pares": todos_pares,
        "meta_alcanzada": meta_alcanzada,
        "partidos_jugados": dict(partidos_jugados),
        "descansos": dict(descansos),
        "resumen": resumen_df
    }
