import random
import itertools
from collections import defaultdict
from typing import List, Dict, Any
import pandas as pd

"""Esta version de todos contra todos minimiza las rondas jugadas
    No se juega con todos ya que el algoritmo es propenso a repetir parejas
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
    descansos = defaultdict(int)  # ← nuevo: contador de descansos por jugador
    enfrentamientos_cubiertos = set()
    rondas = []
    max_iter = 10000
    iter_count = 0

    while enfrentamientos_cubiertos != todos_pares and iter_count < max_iter:
        iter_count += 1

        # jugadores ordenados por menor cantidad de partidos válidos y descansos
        jugadores_ordenados = sorted(
            jugadores,
            key=lambda g: (partidos_jugados[g], descansos[g])
        )

        disponibles = set(jugadores_ordenados)

        # === CONTROL DE DESCANSOS EQUILIBRADOS ===
        # Si no se puede dividir perfectamente entre grupos de 4
        sobrantes = len(disponibles) % 4
        descansan = []
        if sobrantes > 0:
            # seleccionamos quienes descansan: los que menos hayan descansado hasta ahora
            min_desc = min(descansos.values()) if descansos else 0
            candidatos = [j for j in disponibles if descansos[j] == min_desc]
            random.shuffle(candidatos)
            descansan = candidatos[:sobrantes]
            for j in descansan:
                descansos[j] += 1
            disponibles -= set(descansan)
        # =========================================

        partidos_ronda = []
        for cancha_idx in range(num_canchas):
            if len(disponibles) >= 4:
                candidatos = list(disponibles)
                random.shuffle(candidatos)
                best_quad = None
                best_new = -1
                trials = min(60, max(20, len(candidatos)))
                for _ in range(trials):
                    quad = random.sample(candidatos, 4)
                    partitions = [
                        ((quad[0], quad[1]), (quad[2], quad[3])),
                        ((quad[0], quad[2]), (quad[1], quad[3])),
                        ((quad[0], quad[3]), (quad[1], quad[2])),
                    ]
                    for p1, p2 in partitions:
                        new_cover = 0
                        for a in p1:
                            for b in p2:
                                pair = tuple(sorted((a, b)))
                                if pair not in enfrentamientos_cubiertos:
                                    new_cover += 1
                        worst_count = max(partidos_jugados[a] for a in p1 + p2)
                        best_score = new_cover - (0.1 * worst_count)
                        if best_score > best_new:
                            best_new = best_score
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

            else:
                counts = [partidos_jugados[g] for g in jugadores]
                todos_igual = (min(counts) == max(counts))
                if not todos_igual:
                    break
                else:
                    needed = 4 - len(disponibles)
                    if len(disponibles) == 0:
                        break
                    no_disp = [g for g in jugadores if g not in disponibles]
                    if not no_disp:
                        break
                    no_disp_sorted = sorted(no_disp, key=lambda g: -partidos_jugados[g])
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
                    disponibles -= set(take4)

        # actualizar enfrentamientos y conteos
        for partido in partidos_ronda:
            p1 = partido["pareja1"]
            p2 = partido["pareja2"]
            for a in p1:
                for b in p2:
                    pair = tuple(sorted((a, b)))
                    if partido["valido_para"].get(a, False) or partido["valido_para"].get(b, False):
                        enfrentamientos_cubiertos.add(pair)
            for pl, valido in partido["valido_para"].items():
                if valido:
                    partidos_jugados[pl] += 1

        ronda_idx = len(rondas) + 1
        # después de armar todos los partidos de la ronda:
        # jugadores que no fueron asignados ni como ayudantes
        no_usados = [j for j in jugadores if all(j not in (p['pareja1'] + p['pareja2'] + tuple(p['ayudantes'])) for p in partidos_ronda)]
        for j in no_usados:
            descansos[j] += 1
        descansan += no_usados
        rondas.append({
            "ronda": ronda_idx,
            "partidos": partidos_ronda,
            "descansan": descansan
        })

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
        "resumen": resumen_df  # ← DataFrame listo para mostrar
    }
