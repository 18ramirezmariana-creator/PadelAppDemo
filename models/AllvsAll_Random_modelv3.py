import random
import itertools
from collections import defaultdict
from typing import List, Dict, Any
import pandas as pd

def generar_torneo_todos_contra_todos(
    jugadores: List[str],
    num_canchas: int,
    seed: int | None = None
) -> List[Dict[str, Any]]:
    """
    Versión modificada:
    - máximo RONDAS = 9
    - objetivo cobertura >= 80% (opcional)
    - prioriza nuevos enfrentamientos y nuevas parejas
    - evita descansos consecutivos siempre que sea posible
    - mantiene la lógica de 'ayudantes' y 'valido_para' (partidos con ayudantes no cuentan para ranking)
    """
    if seed is not None:
        random.seed(seed)

    n = len(jugadores)
    if n < 4:
        raise ValueError("Se requieren al menos 4 jugadores para dobles 2vs2.")

    TODOS_PARES = set(tuple(sorted(p)) for p in itertools.combinations(jugadores, 2))
    TARGET_COVERAGE = 0.80  # objetivo mínimo de cobertura
    MAX_ROUNDS = 9

    # contadores
    partidos_jugados = defaultdict(int)   # cuenta solo partidos 'validos' (no ayudantes)
    descansos = defaultdict(int)
    enfrentamientos_cubiertos = set()
    parejas_contadas = defaultdict(int)   # cuenta cuantas veces se formó cada pareja (for penalización)
    rondas = []

    last_rest = None  # para evitar descansos consecutivos

    # pesos de scoring (ajustables)
    W_NEW_AD = 100.0     # nuevo enfrentamiento (prioridad alta)
    W_NEW_PART = 25.0    # nueva pareja (segunda prioridad)
    PEN_REPEAT_PART = 8.0   # penaliza repetir pareja
    PEN_REST_CONSEC = 1e4   # penaliza que los descansos intersecten el last_rest (evitarlo)
    TRIALS_PER_CANCHA = 80  # número de muestreos aleatorios para elegir quad (puedes bajar para velocidad)

    # precomputes helpers
    all_pairs = TODOS_PARES.copy()

    round_idx = 0
    # Generar hasta MAX_ROUNDS o hasta que se alcance cobertura objetivo razonable
    while round_idx < MAX_ROUNDS:
        round_idx += 1
        # ordenar jugadores por partidos válidos ascendentes y descansos ascendentes
        jugadores_ordenados = sorted(jugadores, key=lambda g: (partidos_jugados[g], descansos[g]))
        disponibles = set(jugadores_ordenados)

        # calcular cuántos deben descansar esta ronda (2 si n=10 y 2 canchas)
        # general: resto = n - 4*num_canchas  (si >0 descansan ese número)
        sobrantes = max(0, n - 4 * num_canchas)
        descansan = []
        if sobrantes > 0:
            # elegir los que menos descansos han tenido, evitando last_rest si es posible
            min_desc = min(descansos.values()) if descansos else 0
            candidatos = [j for j in jugadores_ordenados if descansos[j] == min_desc]
            # intentar escoger candidatos que no estén en last_rest
            if last_rest is not None:
                candidatos_no_last = [c for c in candidatos if c not in (last_rest or [])]
                if len(candidatos_no_last) >= sobrantes:
                    candidatos = candidatos_no_last
            random.shuffle(candidatos)
            descansan = candidatos[:sobrantes]
            for j in descansan:
                descansos[j] += 1
            disponibles -= set(descansan)
        else:
            # si sobrantes == 0, nadie descansa esta ronda
            descansan = []

        partidos_ronda = []
        used_players_this_round = set()

        # para cada cancha, buscamos la mejor quad disjunta según heurística
        for cancha_idx in range(num_canchas):
            # recompute disponibles para este punto
            cur_avail = list(disponibles - used_players_this_round)
            # si hay menos de 4 jugadores disponibles, intentamos traer ayudantes según la lógica original
            if len(cur_avail) < 4:
                # aplicamos la regla original: solo usar ayudantes si todos tienen igual número de partidos válidos
                counts = [partidos_jugados[g] for g in jugadores]
                todos_igual = (min(counts) == max(counts))
                if not todos_igual:
                    # no podemos formar más partidos válidos cómodamente en esta ronda
                    break
                else:
                    needed = 4 - len(cur_avail)
                    no_disp = [g for g in jugadores if g not in (disponibles - set(descansan)) and g not in cur_avail]
                    # seleccionar ayudantes con mayor partidos_jugados (siguiendo tu lógica original)
                    no_disp_sorted = sorted(no_disp, key=lambda g: -partidos_jugados[g])
                    ayudantes_seleccionados = no_disp_sorted[:needed]
                    take4 = cur_avail + ayudantes_seleccionados
                    if len(take4) < 4:
                        break
                    p1 = (take4[0], take4[1])
                    p2 = (take4[2], take4[3])
                    valido_dict = {pl: (pl not in ayudantes_seleccionados) for pl in p1 + p2}
                    partidos_ronda.append({
                        "cancha": cancha_idx + 1,
                        "pareja1": tuple(p1),
                        "pareja2": tuple(p2),
                        "ayudantes": list(ayudantes_seleccionados),
                        "valido_para": valido_dict
                    })
                    used_players_this_round |= set(take4)
                    continue

            # buscar la mejor quad entre muestreos aleatorios
            best_quad = None
            best_score = -float("inf")
            # si hay muchos candidatos, limitamos el set para muestreo por eficiencia
            pool = cur_avail.copy()
            # aumentamos aleatoriedad en pool si es grande
            for _ in range(min(TRIALS_PER_CANCHA, max(20, len(pool) * 3))):
                if len(pool) < 4:
                    break
                quad = random.sample(pool, 4)
                # probar las 3 particiones
                partitions = [
                    ((quad[0], quad[1]), (quad[2], quad[3])),
                    ((quad[0], quad[2]), (quad[1], quad[3])),
                    ((quad[0], quad[3]), (quad[1], quad[2])),
                ]
                for p1, p2 in partitions:
                    # penalizar si alguno de estos jugadores ya será usado en otro partido de esta ronda
                    if set(p1) & used_players_this_round or set(p2) & used_players_this_round:
                        continue
                    # calcular cuántos nuevos adversarios aporta
                    new_ad = 0
                    new_part = 0
                    repeat_part_pen = 0
                    for a in p1:
                        for b in p2:
                            pair = tuple(sorted((a, b)))
                            if pair not in enfrentamientos_cubiertos:
                                new_ad += 1
                    for p in (p1, p2):
                        partnership = tuple(sorted(p))
                        if parejas_contadas[partnership] == 0:
                            new_part += 1
                        repeat_part_pen += parejas_contadas[partnership]
                    # penalizar si descansos de esta ronda chocan con last_rest
                    rest_consec_pen = 0
                    if last_rest is not None and len(set(descansan) & set(last_rest)) > 0:
                        # esta penalización es por escoger descansos que repitan; pero aquí preferimos
                        rest_consec_pen = PEN_REST_CONSEC if any(x in last_rest for x in descansan) else 0
                    # score combine
                    score = (W_NEW_AD * new_ad) + (W_NEW_PART * new_part) - (PEN_REPEAT_PART * repeat_part_pen) - rest_consec_pen
                    # tie-breaker: favorecer quads with lower max(partidos_jugados) to balance carga
                    worst_count = max(partidos_jugados[a] for a in p1 + p2)
                    score -= 0.2 * worst_count
                    if score > best_score:
                        best_score = score
                        best_quad = (tuple(p1), tuple(p2))

            # fallback si no se encontró quad por muestreo (poco probable)
            if best_quad is None:
                take = cur_avail[:4]
                p1 = (take[0], take[1])
                p2 = (take[2], take[3])
                ayudantes = []
                valido_dict = {pl: True for pl in p1 + p2}
                partidos_ronda.append({
                    "cancha": cancha_idx + 1,
                    "pareja1": p1,
                    "pareja2": p2,
                    "ayudantes": ayudantes,
                    "valido_para": valido_dict
                })
                used_players_this_round |= set(p1) | set(p2)
            else:
                p1, p2 = best_quad
                valido_dict = {pl: True for pl in p1 + p2}
                partidos_ronda.append({
                    "cancha": cancha_idx + 1,
                    "pareja1": tuple(p1),
                    "pareja2": tuple(p2),
                    "ayudantes": [],
                    "valido_para": valido_dict
                })
                used_players_this_round |= set(p1) | set(p2)

        # si no se crearon partidos en la ronda, salir
        if not partidos_ronda:
            break

        # actualizar estructura con los partidos de esta ronda
        rondas.append({
            "ronda": round_idx,
            "partidos": partidos_ronda,
            "descansan": tuple(sorted(descansan))
        })

        # actualizar contadores y conjuntos (solo al final de la ronda)
        for partido in partidos_ronda:
            p1 = partido["pareja1"]
            p2 = partido["pareja2"]
            # actualizar parejas contadas (si son validas)
            for pair in (tuple(sorted(p1)), tuple(sorted(p2))):
                parejas_contadas[pair] += 1
            # actualizar enfrentamientos adversarios y partidos_jugados según valido_para
            for a in p1:
                for b in p2:
                    pair = tuple(sorted((a, b)))
                    # si al menos uno de los dos tiene valido=True en este partido, contar el enfrentamiento
                    if partido["valido_para"].get(a, False) or partido["valido_para"].get(b, False):
                        enfrentamientos_cubiertos.add(pair)
            for pl, valido in partido["valido_para"].items():
                if valido:
                    partidos_jugados[pl] += 1

        # setear last_rest para la próxima ronda para intentar evitar descansos consecutivos
        last_rest = tuple(sorted(descansan)) if descansan else None

        # comprobación temprana de cobertura objetivo
        coverage = len(enfrentamientos_cubiertos) / len(TODOS_PARES)
        if coverage >= TARGET_COVERAGE:
            # si alcanzamos target, podemos seguir un par de rondas más para mejorar parejas
            # pero como queremos mantener MAX_ROUNDS = 9, solo se cortará si hemos alcanzado target y
            # ya generamos la cantidad mínima de rondas (aquí permitimos seguir hasta MAX_ROUNDS)
            pass

        # continuar hasta MAX_ROUNDS
        # loop sigue

    # después de construir las rondas, calculamos métricas y devolvemos en la estructura original
    meta_alcanzada = (len(enfrentamientos_cubiertos) == len(TODOS_PARES))
    resumen_df = pd.DataFrame({
        "jugador": jugadores,
        "partidos_jugados": [partidos_jugados[j] for j in jugadores],
        "descansos": [descansos[j] for j in jugadores]
    }).sort_values(by=["partidos_jugados", "descansos"], ascending=[False, True]).reset_index(drop=True)

    return {
        "rondas": rondas,
        "enfrentamientos_cubiertos": enfrentamientos_cubiertos,
        "todos_pares": TODOS_PARES,
        "meta_alcanzada": meta_alcanzada,
        "partidos_jugados": dict(partidos_jugados),
        "descansos": dict(descansos),
        "resumen": resumen_df
    }
