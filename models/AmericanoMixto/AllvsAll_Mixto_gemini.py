import random
import pandas as pd
from itertools import combinations
import streamlit as st
import math

# ==============================================================================
# 1. CLASE PRINCIPAL DEL TORNEO (AmericanoPadelTournament)
# ==============================================================================

class AmericanoPadelTournament:
    """
    Generador de fixture para un Torneo Americano Mixto optimizado.
    Busca maximizar la diversidad de compañeros y oponentes a lo largo de las rondas.
    """
    def __init__(self, males, females, num_canchas, puntos_partido):
        self.males = males
        self.females = females
        self.P = len(males) + len(females)  # Total de jugadores
        self.N = len(males)                # Número de jugadores por género
        self.num_canchas = num_canchas
        self.puntos_partido = puntos_partido

        # Inicialización de contadores de diversidad (optimización)
        self.partner_counts = {}   # Cuántas veces ha jugado (M, F) como pareja
        self.opponent_counts = {}  # Cuántas veces (M1, F1) ha jugado VS (M2, F2)
        self.play_counts = {p: 0 for p in self.males + self.females} # Partidos jugados
        self.rest_counts = {p: 0 for p in self.males + self.females} # Descansos
        
        # Inicialización de claves para contadores
        for m in self.males:
            for f in self.females:
                # La clave del partner es una tupla ordenada (M, F)
                self.partner_counts[tuple(sorted((m, f)))] = 0
        
        # Todas las combinaciones posibles de dos parejas mixtas
        all_possible_pairs = [tuple(sorted((m, f))) for m in self.males for f in self.females]
        all_match_combinations = combinations(all_possible_pairs, 2)
        for p1, p2 in all_match_combinations:
            # La clave del oponente es una tupla de tuplas de parejas, ordenada lexicográficamente
            self.opponent_counts[tuple(sorted((p1, p2)))] = 0

    def get_diversity_score(self, current_round_matches):
        """
        Calcula una puntuación de diversidad para un conjunto de partidos propuestos.
        Menor puntuación = Mayor diversidad / Menor repetición.
        """
        score = 0
        # 1. Puntuación por repetición de pareja (mayor penalización)
        for pareja1, pareja2 in current_round_matches:
            m1, f1 = pareja1
            m2, f2 = pareja2
            
            # Penalización por repetición de compañero
            score += self.partner_counts[tuple(sorted((m1, f1)))] ** 2
            score += self.partner_counts[tuple(sorted((m2, f2)))] ** 2
            
            # Penalización por repetición de oponente
            key = tuple(sorted((tuple(sorted((m1, f1))), tuple(sorted((m2, f2))))))
            score += self.opponent_counts.get(key, 0) ** 3  # Mayor penalización para oponentes

        # 2. Puntuación por desequilibrio de descanso/juego (penalización moderada)
        playing_players = set()
        for p1, p2 in current_round_matches:
            playing_players.update(p1)
            playing_players.update(p2)
        
        counts = [self.play_counts[p] for p in self.males + self.females]
        # Varianza simple de los partidos jugados para penalizar desequilibrios
        if counts:
            score += (max(counts) - min(counts)) * 50 
            
        return score

    def update_counts(self, round_matches):
        """Actualiza los contadores de partner y oponente después de una ronda."""
        for pareja1, pareja2 in round_matches:
            m1, f1 = pareja1
            m2, f2 = pareja2
            
            # Actualizar conteo de partners
            self.partner_counts[tuple(sorted((m1, f1)))] += 1
            self.partner_counts[tuple(sorted((m2, f2)))] += 1
            
            # Actualizar conteo de oponentes
            key = tuple(sorted((tuple(sorted((m1, f1))), tuple(sorted((m2, f2))))))
            self.opponent_counts[key] += 1
            
            # Actualizar conteo de juegos
            for player in pareja1 + pareja2:
                self.play_counts[player] += 1

        # Actualizar conteo de descansos
        playing = set()
        for p1, p2 in round_matches:
            playing.update(p1)
            playing.update(p2)
            
        for player in self.males + self.females:
            if player not in playing:
                self.rest_counts[player] += 1
        
    def generate_round(self):
        """Genera una sola ronda optimizando la diversidad."""
        
        # Número de jugadores que deben jugar y descansar
        players_to_play = 4 * self.num_canchas
        
        # Verificar que el número de jugadores sea manejable
        if self.P < players_to_play:
            raise ValueError("No hay suficientes jugadores para la cantidad de canchas especificadas.")
            
        # 1. Definir jugadores disponibles y jugadores que deben descansar (prioridad al que más ha jugado)
        available_males = self.males[:]
        available_females = self.females[:]

        # 2. Heurística de Prioridad (Descanso para los que más han jugado)
        num_rest_males = (self.N * 2 - players_to_play // 2) // 2 # Jugadores totales - Jugadores a jugar. Dividido entre 2 (M/F)
        
        # Identificar jugadores que necesitan descanso (más juegos, menos descanso)
        rest_candidates = sorted(self.males + self.females, key=lambda p: (self.play_counts[p], -self.rest_counts[p]), reverse=True)
        
        # Intentar forzar el descanso para los más jugados (mismo número de M y F)
        resting_players = set()
        for player in rest_candidates:
            is_male = player in self.males
            
            # Asegurar que el número de descansos sea mixto y correcto
            if len(resting_players) < (self.P - players_to_play):
                resting_players.add(player)
        
        # Jugadores disponibles para el juego
        available_males = [m for m in self.males if m not in resting_players]
        available_females = [f for f in self.females if f not in resting_players]

        if len(available_males) != len(available_females) or len(available_males) != players_to_play // 2:
            # Fallback a selección aleatoria si la heurística de descanso falla el balance M/F
            available_players = random.sample(self.males + self.females, players_to_play)
            available_males = [p for p in available_players if p in self.males]
            available_females = [p for p in available_players if p in self.females]
            
            # Si el fallback no es 50/50 (lo cual es raro), se ajusta a la mitad menor
            min_len = min(len(available_males), len(available_females))
            available_males = available_males[:min_len]
            available_females = available_females[:min_len]
            
            # Recalcular el conjunto de descanso
            resting_players = set(self.males + self.females) - set(available_males) - set(available_females)

        # 3. Generar todas las posibles configuraciones de partidos
        all_possible_matches = []
        
        # Generar todas las posibles parejas mixtas (M, F) con los jugadores disponibles
        possible_pairs = [(m, f) for m in available_males for f in available_females]
        
        # Utilizamos una función de puntuación para guiar la búsqueda (Greedy Search)
        # Queremos seleccionar 2*num_canchas parejas para formar num_canchas partidos.
        
        def find_best_round(males_pool, females_pool, matches_needed):
            """
            Busca el mejor set de 'matches_needed' minimizando la repetición.
            Utiliza una búsqueda por muestreo (simplificado).
            """
            best_score = float('inf')
            best_matches = []
            
            # 4. Muestreo de soluciones (para evitar la complejidad factorial)
            # Intentamos generar 200 rondas candidatas y elegimos la mejor.
            for _ in range(200):
                temp_males = males_pool[:]
                temp_females = females_pool[:]
                current_matches = []
                current_pairs = []
                
                # Crear 2 * matches_needed parejas mixtas
                all_candidate_pairs = [(m, f) for m in temp_males for f in temp_females]
                random.shuffle(all_candidate_pairs)
                
                # Heurística: Priorizar parejas que NO han jugado juntas
                candidate_pairs_sorted = sorted(all_candidate_pairs, 
                                                key=lambda p: self.partner_counts[tuple(sorted(p))])
                
                # Seleccionar 2 * num_canchas parejas para el juego
                playing_pairs_set = set()
                temp_m_used = set()
                temp_f_used = set()

                # Fase 1: Formar las 2*C parejas.
                for m, f in candidate_pairs_sorted:
                    if m not in temp_m_used and f not in temp_f_used and len(playing_pairs_set) < 2 * matches_needed:
                        playing_pairs_set.add((m, f))
                        temp_m_used.add(m)
                        temp_f_used.add(f)

                playing_pairs = list(playing_pairs_set)
                if len(playing_pairs) < 2 * matches_needed:
                    continue # Solución incompleta, intentar de nuevo

                # Fase 2: Formar los C partidos a partir de las 2*C parejas.
                # Combinar estas parejas en partidos, priorizando oponentes nuevos.
                match_candidates = list(combinations(playing_pairs, 2))
                match_candidates_scored = []
                
                for p1, p2 in match_candidates:
                    key = tuple(sorted((tuple(sorted(p1)), tuple(sorted(p2)))))
                    score = self.opponent_counts.get(key, 0)
                    match_candidates_scored.append((score, p1, p2))
                
                # Ordenar por menor repetición de oponentes
                match_candidates_scored.sort()
                
                # Greedy selection de partidos
                used_pairs = set()
                final_matches = []
                for score, p1, p2 in match_candidates_scored:
                    if p1 not in used_pairs and p2 not in used_pairs:
                        final_matches.append((p1, p2))
                        used_pairs.add(p1)
                        used_pairs.add(p2)
                        if len(final_matches) == matches_needed:
                            break
                
                if len(final_matches) == matches_needed:
                    current_score = self.get_diversity_score(final_matches)
                    if current_score < best_score:
                        best_score = current_score
                        best_matches = final_matches
                        
            return best_matches

        # Generar la mejor ronda encontrada
        best_round_matches = find_best_round(available_males, available_females, self.num_canchas)
        
        # 5. Formato de salida y actualización
        if not best_round_matches:
            # Fallback: Si no se encontró una solución optimizada, generar una aleatoria
            # Esto puede pasar si el número de muestreos no es suficiente o hay un desequilibrio extremo.
            st.warning("Advertencia: Fallo en la optimización. Generando ronda aleatoria.")
            
            # Simple shuffle and pair for the available players
            players_in_match = available_males + available_females
            random.shuffle(players_in_match)
            
            best_round_matches = []
            for i in range(0, len(players_in_match), 4):
                if i + 3 < len(players_in_match):
                    p1 = (players_in_match[i], players_in_match[i+1])
                    p2 = (players_in_match[i+2], players_in_match[i+3])
                    best_round_matches.append((p1, p2))
            
            # Asegurar que las parejas son mixtas (1M, 1F) en el fallback
            # Es más seguro reorganizar a los disponibles M/F y emparejar M1-F1 vs M2-F2, etc.
            random.shuffle(available_males)
            random.shuffle(available_females)
            
            temp_pairs = []
            for i in range(self.num_canchas * 2):
                if i < len(available_males) and i < len(available_females):
                    temp_pairs.append((available_males[i], available_females[i]))
            
            best_round_matches = []
            for i in range(0, len(temp_pairs), 2):
                if i + 1 < len(temp_pairs):
                    best_round_matches.append((temp_pairs[i], temp_pairs[i+1]))


        # Actualizar contadores y devolver la ronda
        self.update_counts(best_round_matches)
        
        # Determinar jugadores que descansan (los que no están en best_round_matches)
        all_playing_in_round = set()
        for p1, p2 in best_round_matches:
            all_playing_in_round.update(p1)
            all_playing_in_round.update(p2)

        final_resting_players = [p for p in self.males + self.females if p not in all_playing_in_round]
        
        return best_round_matches, final_resting_players

    def get_summary(self):
        """Devuelve un resumen de los contadores de juego y descanso."""
        summary = []
        for player in self.males + self.females:
            summary.append({
                "Jugador": player,
                "Género": "H" if player in self.males else "M",
                "Partidos Jugados": self.play_counts[player],
                "Rondas Descansadas": self.rest_counts[player]
            })
        return summary
    
# ==============================================================================
# 2. FUNCIÓN PRINCIPAL DE GENERACIÓN (generar_torneo_mixto)
# ==============================================================================

def generar_torneo_mixto(male_players, female_players, num_canchas, puntos_partido):
    """
    Función que orquesta la generación del fixture completo.
    
    Args:
        male_players (list): Lista de nombres de hombres.
        female_players (list): Lista de nombres de mujeres.
        num_canchas (int): Número de canchas disponibles.
        puntos_partido (int): Puntos a disputar por partido.

    Returns:
        dict: Diccionario con 'rondas' y 'resumen'.
    """
    
    if len(male_players) != len(female_players):
        return {"rondas": [], "resumen": []}
        
    N = len(male_players)
    total_players = 2 * N
    
    # El número ideal de rondas para una buena diversidad es aproximadamente N o 2N
    # N-1 es el número de rondas para un Round Robin simple. Usaremos un mínimo de N+1
    # para asegurar rotación, o un valor basado en la cantidad de jugadores.
    if total_players <= 8:
        num_rondas = N * 2
    else:
        num_rondas = N + 2
        
    # Inicializar el motor del torneo
    tournament = AmericanoPadelTournament(male_players, female_players, num_canchas, puntos_partido)
    
    rondas_fixture = []
    
    # Generar las rondas
    for i in range(1, num_rondas + 1):
        try:
            # Genera la ronda optimizada
            matches, resting = tournament.generate_round()
            
            ronda_data = {
                "ronda": i,
                "partidos": [],
                "descansan": resting
            }
            
            for j, (pareja1, pareja2) in enumerate(matches):
                # Asegurar que las parejas sean listas (o tuplas) de jugadores
                ronda_data["partidos"].append({
                    "cancha": j + 1,
                    "pareja1": list(pareja1),
                    "pareja2": list(pareja2),
                    "ayudantes": [] # No se usa en mixto, pero se mantiene para consistencia
                })
            
            rondas_fixture.append(ronda_data)
            
        except ValueError as e:
            st.error(f"Error generando ronda {i}: {str(e)}")
            break
        except Exception as e:
            st.error(f"Error inesperado en ronda {i}: {e}")
            break

    return {
        "rondas": rondas_fixture,
        "resumen": tournament.get_summary()
    }

# ==============================================================================
# 3. FUNCIÓN DE ANÁLISIS (analyze_algorithm_results)
# ==============================================================================

def analyze_algorithm_results(fixture, male_players, female_players):
    """
    Analiza la calidad del fixture generado e imprime métricas de diversidad.
    
    Args:
        fixture (list): El fixture generado (lista de rondas).
        male_players (list): Lista de nombres de hombres.
        female_players (list): Lista de nombres de mujeres.
    """
    if not fixture:
        return

    # Contadores
    total_players = male_players + female_players
    player_games = {p: 0 for p in total_players}
    player_rests = {p: 0 for p in total_players}
    partner_pairs = {} 
    opponent_pairs = {}

    for ronda in fixture:
        playing_in_round = set()
        for partido in ronda["partidos"]:
            p1 = tuple(sorted(partido["pareja1"]))
            p2 = tuple(sorted(partido["pareja2"]))
            
            # Conteo de partners
            partner_pairs[p1] = partner_pairs.get(p1, 0) + 1
            partner_pairs[p2] = partner_pairs.get(p2, 0) + 1
            
            # Conteo de oponentes
            key = tuple(sorted((p1, p2)))
            opponent_pairs[key] = opponent_pairs.get(key, 0) + 1
            
            # Conteo de juegos
            for player in partido["pareja1"] + partido["pareja2"]:
                player_games[player] += 1
                playing_in_round.add(player)
        
        # Conteo de descansos
        for player in total_players:
            if player not in playing_in_round:
                player_rests[player] += 1

    # Métricas de diversidad
    total_games = sum(player_games.values()) / 4 # Cada partido cuenta 4 juegos
    if total_games == 0:
        return
        
    avg_games = total_games / len(total_players)

    # 1. Equilibrio de Juegos
    game_counts = list(player_games.values())
    min_g = min(game_counts)
    max_g = max(game_counts)
    game_diff = max_g - min_g
    
    # 2. Diversidad de Compañeros
    if partner_pairs:
        partner_counts = list(partner_pairs.values())
        min_p = min(partner_counts)
        max_p = max(partner_counts)
        partner_diff = max_p - min_p
    else:
        partner_diff = 0
        
    # 3. Diversidad de Oponentes (Cuántos partidos únicos se jugaron)
    total_possible_matches = len(male_players) * len(female_players)
    
    st.markdown("### 🔍 Análisis de la Diversidad del Fixture")
    st.info(f"""
        **Rondas Generadas:** {len(fixture)}
        **Partidos por Jugador (Promedio):** {avg_games:.2f}
        
        **Juegos (Máx vs. Mín):** {max_g} vs {min_g} (Diferencia: {game_diff})
        **Compañeros (Máx vs. Mín):** {max_p} vs {min_p} (Diferencia: {partner_diff})
        
        *Este fixture busca minimizar estas diferencias, asegurando un torneo equitativo.*
    """)
    
# ==============================================================================
# 4. FUNCIÓN AUXILIAR (calcular_ranking_individual)
# ==============================================================================

def calcular_ranking_individual(resultados, fixture):
    """
    Calcula el ranking individual a partir de los resultados ingresados.
    
    Args:
        resultados (dict): Diccionario de resultados {(pareja1_str, pareja2_str): (score1, score2)}.
        fixture (list): Lista de rondas con los partidos.

    Returns:
        pd.DataFrame: DataFrame con el ranking individual.
    """
    
    player_stats = {}
    
    # 1. Inicializar estadísticas de jugadores
    for ronda in fixture:
        for partido in ronda["partidos"]:
            for player in partido["pareja1"] + partido["pareja2"]:
                if player not in player_stats:
                    player_stats[player] = {
                        "Puntos a Favor": 0,
                        "Puntos en Contra": 0,
                        "Diferencia": 0,
                        "Partidos Jugados": 0
                    }

    # 2. Procesar resultados
    for key, (score1, score2) in resultados.items():
        if score1 + score2 > 0: # Solo procesar partidos con resultados
            
            # La clave del resultado es una tupla de strings de las parejas
            pareja1_str, pareja2_str = key
            
            # Intentar parsear los nombres de la pareja
            # El string es "Jugador1 & Jugador2"
            try:
                jugadores_p1 = [p.strip() for p in pareja1_str.split(" & ")]
                jugadores_p2 = [p.strip() for p in pareja2_str.split(" & ")]
            except:
                continue # Saltar si el formato es inesperado

            if not jugadores_p1 or not jugadores_p2:
                continue

            # Asignar puntos a favor y en contra
            for player in jugadores_p1:
                if player in player_stats:
                    player_stats[player]["Puntos a Favor"] += score1
                    player_stats[player]["Puntos en Contra"] += score2
                    player_stats[player]["Partidos Jugados"] += 1

            for player in jugadores_p2:
                if player in player_stats:
                    player_stats[player]["Puntos a Favor"] += score2
                    player_stats[player]["Puntos en Contra"] += score1
                    player_stats[player]["Partidos Jugados"] += 1
                    
    # 3. Calcular diferencia y preparar DataFrame
    data = []
    for player, stats in player_stats.items():
        stats["Diferencia"] = stats["Puntos a Favor"] - stats["Puntos en Contra"]
        data.append({"Jugador": player, **stats})

    df = pd.DataFrame(data)
    
    if df.empty or df["Partidos Jugados"].sum() == 0:
        return None

    # 4. Ordenar ranking: 
    # 1. Diferencia de puntos (Mayor a menor)
    # 2. Puntos a Favor (Mayor a menor)
    # 3. Partidos Jugados (Mayor a menor, para desempate si todo es igual)
    df = df.sort_values(by=["Diferencia", "Puntos a Favor", "Partidos Jugados"], 
                        ascending=[False, False, False]).reset_index(drop=True)
    
    df.index = df.index + 1 # Ranking empieza en 1
    df.index.name = "Rank"
    
    return df

