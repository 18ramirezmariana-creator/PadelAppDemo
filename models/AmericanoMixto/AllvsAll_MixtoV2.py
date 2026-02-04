import streamlit as st
from collections import defaultdict
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import itertools

class AmericanoPadelTournament:
    """Mixed Americano Tournament - Men & Women pairs with helper logic"""
    def __init__(self, male_players, female_players, num_fields, points_per_match):
        if len(male_players) != len(female_players):
            raise ValueError(f"Must have equal numbers of men and women. Got {len(male_players)} men and {len(female_players)} women.")
        
        if len(male_players) < 2:
            raise ValueError("Need at least 2 players of each gender (4 total)")
        
        self.male_players = male_players
        self.female_players = female_players
        self.num_players = len(male_players)
        self.total_players = len(male_players) + len(female_players)
        self.num_fields = num_fields
        self.points_per_match = points_per_match
        
        self.player_stats = defaultdict(lambda: {
            'matches': 0,
            'last_round_played': -1, 
            'partners': defaultdict(int),
            'opponents': defaultdict(int),
            'points_for': 0,
            'points_against': 0
        })
        
        self.rounds = []
        self.all_matches_played = set()
        
        self.target_matches = self.num_players
        
    def get_match_signature(self, team1, team2):
        """Create unique signature for a match, ordered by player names"""
        players = sorted(list(team1) + list(team2))
        return tuple(players)
    
    def calculate_match_score(self, team1, team2, current_round):
        """Calculate desirability score for a match (LOWER is better)"""
        players = [team1[0], team1[1], team2[0], team2[1]]
        
        # PRIORITY 1: Gestión de descanso (IMPACTO CRÍTICO)
        rest_bonus = 0
        for p in players:
            rounds_since_last = current_round - self.player_stats[p]['last_round_played']
            
            # Bloqueo ALTO pero ligeramente más flexible para evitar bloqueos totales cerca del final
            if rounds_since_last == 0 or rounds_since_last == 1:
                rest_bonus += 400000 
            elif rounds_since_last >= 2:
                rest_bonus -= rounds_since_last * 5000
        
        # PRIORITY 2: Equilibrio de partidos
        match_count_score = sum(self.player_stats[p]['matches'] for p in players)
        
        # PRIORITY 3 y 4: Penalizaciones por repetición
        partnership_penalty = (self.player_stats[team1[0]]['partners'][team1[1]] * 1000 + 
                               self.player_stats[team2[0]]['partners'][team2[1]] * 1000)
        
        opponent_penalty = 0
        for p1 in [team1[0], team1[1]]:
            for p2 in [team2[0], team2[1]]:
                opponent_penalty += self.player_stats[p1]['opponents'][p2] * 100
        
        total_score = rest_bonus + match_count_score + partnership_penalty + opponent_penalty
        total_score += random.random() * 0.01 
        
        return total_score
    
    def get_current_min_matches(self):
        """Get the current minimum number of matches any player has played (up to target)"""
        all_players = self.male_players + self.female_players
        players_under_target = [p for p in all_players if self.player_stats[p]['matches'] < self.target_matches]
        
        if not players_under_target:
            return self.target_matches
            
        return min(self.player_stats[p]['matches'] for p in players_under_target)
    
    def find_best_matches_for_round(self, num_matches_needed, current_round):
        """Find the best set of matches for a round, prioritizing rest and completeness"""
        selected_matches = []
        used_players = set()
        
        players_needing_matches = set(p for p in self.male_players + self.female_players if self.player_stats[p]['matches'] < self.target_matches)
        
        def player_sort_key(p):
            # Prioriza por mayor descanso, luego por menos partidos
            rounds_since_last = current_round - self.player_stats[p]['last_round_played']
            return (-rounds_since_last, self.player_stats[p]['matches'])
            
        # Ordenamos a TODOS los jugadores por prioridad de descanso
        all_males = sorted(self.male_players, key=player_sort_key)
        all_females = sorted(self.female_players, key=player_sort_key)
        
        for _ in range(num_matches_needed):
            
            # Jugadores disponibles para ESTE partido
            current_available_males = [m for m in all_males if m not in used_players]
            current_available_females = [f for f in all_females if f not in used_players]
            
            if len(current_available_males) < 2 or len(current_available_females) < 2:
                break
            
            best_match = None
            best_score = float('inf')
            
            # Limitar la búsqueda a los top 8 disponibles de la lista ORDENADA
            search_males = current_available_males[:min(8, len(current_available_males))]
            search_females = current_available_females[:min(8, len(current_available_females))]
            
            for i in range(len(search_males)):
                for j in range(i + 1, len(search_males)):
                    m1, m2 = search_males[i], search_males[j]
                    
                    for k in range(len(search_females)):
                        for l in range(k + 1, len(search_females)):
                            f1, f2 = search_females[k], search_females[l]
                            
                            for team1, team2 in [((m1, f1), (m2, f2)), ((m1, f2), (m2, f1))]:
                                signature = self.get_match_signature(team1, team2)
                                
                                if signature in self.all_matches_played:
                                    continue
                                
                                all_match_players = set([m1, m2, f1, f2])
                                
                                # Condición de Progresión: Verificar que al menos UN jugador necesite el partido
                                has_player_needing_match = any(p in players_needing_matches for p in all_match_players)
                                
                                if not players_needing_matches or has_player_needing_match:
                                    score = self.calculate_match_score(team1, team2, current_round)
                                    
                                    if score < best_score:
                                        best_score = score
                                        best_match = (team1, team2)
            
            # Solo aceptamos si el score NO está bloqueado por penalización de descanso
            if best_match and best_score < 350000: 
                selected_matches.append(best_match)
                team1, team2 = best_match
                used_players.update([team1[0], team1[1], team2[0], team2[1]])
            else:
                # Si el mejor partido disponible está bloqueado o es demasiado malo, rompemos la búsqueda de esta ronda
                break 

        return selected_matches, used_players
    
    def update_player_stats(self, match, round_num):
        """Update statistics after a match is scheduled"""
        team1, team2 = match
        
        for player in [team1[0], team1[1], team2[0], team2[1]]:
            self.player_stats[player]['matches'] += 1
            self.player_stats[player]['last_round_played'] = round_num 
        
        self.player_stats[team1[0]]['partners'][team1[1]] += 1
        self.player_stats[team1[1]]['partners'][team1[0]] += 1
        self.player_stats[team2[0]]['partners'][team2[1]] += 1
        self.player_stats[team2[1]]['partners'][team2[0]] += 1
        
        for p1 in [team1[0], team1[1]]:
            for p2 in [team2[0], team2[1]]:
                self.player_stats[p1]['opponents'][p2] += 1
                self.player_stats[p2]['opponents'][p1] += 1
    
    def generate_schedule(self):
        """Generate the complete tournament schedule (LÓGICA CORREGIDA)"""
        round_num = 0
        consecutive_empty_rounds = 0
        max_rounds = 50 
        
        while consecutive_empty_rounds < 3 and round_num < max_rounds:
            round_num += 1
            
            min_matches = self.get_current_min_matches()
            max_matches = max(self.player_stats[p]['matches'] for p in self.male_players + self.female_players) if self.rounds else 0
            
            # Condición de parada
            if min_matches >= self.target_matches and (max_matches - min_matches) <= 1:
                break
            
            # Encontrar la mejor ronda posible (máximo de partidos)
            round_matches, _ = self.find_best_matches_for_round(self.num_fields, round_num)
            
            if not round_matches:
                consecutive_empty_rounds += 1
                continue
                
            consecutive_empty_rounds = 0
            
            # ⚠️ FIX DEL BUCLE INFINITO: Eliminamos la condición que forzaba el reintento.
            # Simplemente publicamos la ronda encontrada, aunque sea incompleta, para garantizar el avance.
            
            # 1. Determinar quién descansa
            all_players = set(self.male_players + self.female_players)
            playing_players = set(p for match in round_matches for team in match for p in team)
            resting_players = list(all_players - playing_players)
            
            # 2. Registrar la ronda
            self.rounds.append({
                'matches': round_matches,
                'resting': resting_players
            })
            
            # 3. Actualizar estadísticas y all_matches_played SOLO cuando la ronda se publica
            for match in round_matches:
                self.update_player_stats(match, round_num)
                self.all_matches_played.add(self.get_match_signature(match[0], match[1]))
            
        return self.rounds
    
    def format_for_streamlit(self):
        """Format schedule for Streamlit visualization with helper logic"""
        formatted_rounds = []
        
        all_players = self.male_players + self.female_players
        
        min_matches_played = min(self.player_stats[p]['matches'] for p in all_players) if all_players else 0
        final_min_matches = min(min_matches_played, self.target_matches)
        
        player_current_counts = defaultdict(int)

        for round_num, round_data in enumerate(self.rounds, 1):
            partidos = []
            
            for cancha_num, match in enumerate(round_data['matches'], 1):
                team1, team2 = match
                all_players_in_match = list(team1) + list(team2)
                
                helpers = []
                valido_para = []
                
                for player in all_players_in_match:
                    matches_before_this = player_current_counts[player]
                    
                    if matches_before_this >= final_min_matches:
                        helpers.append(player)
                    else:
                        valido_para.append(player)
                        
                    player_current_counts[player] += 1 

                partido = {
                    "cancha": cancha_num,
                    "pareja1": list(team1),
                    "pareja2": list(team2),
                    "ayudantes": helpers,
                    "valido_para": valido_para if valido_para else all_players_in_match
                }
                partidos.append(partido)
            
            formatted_rounds.append({
                "ronda": round_num,
                "partidos": partidos,
                "descansan": round_data['resting']
            })
        
        # Generate summary with valid vs helper games
        resumen_data = []
        for player in all_players:
            total_matches = self.player_stats[player]['matches']
            valid_matches = min(total_matches, final_min_matches)
            helper_matches = max(0, total_matches - final_min_matches)
            
            resumen_data.append({
                "Jugador": player,
                "Partidos": total_matches,
                "Partidos Válidos": valid_matches,
                "Partidos Ayudante": helper_matches,
                "Descansos": len(self.rounds) - total_matches
            })
        
        return {
            "rondas": formatted_rounds,
            "resumen": resumen_data,
            "min_matches": final_min_matches
        }


def generar_torneo_mixto(male_players, female_players, num_canchas, puntos_partido):
    """Generate mixed Americano tournament - each man plays with each woman"""
    try:
        tournament = AmericanoPadelTournament(male_players, female_players, 
                                             num_canchas, puntos_partido)
        tournament.generate_schedule()
        return tournament.format_for_streamlit()
    except ValueError as e:
        return {"error": str(e)}
    
def get_unique_players(fixture):
    """Devuelve lista ordenada de jugadores únicos del fixture."""
    return sorted({p for r in fixture for m in r["partidos"] for p in (m["pareja1"] + m["pareja2"])})

def plot_heatmap(matrix, title, cmap, cbar_label):
    """Genera y muestra un mapa de calor triangular superior."""
    mask = np.tril(np.ones_like(matrix, dtype=bool))
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(matrix, mask=mask, annot=True, fmt="d", cmap=cmap, ax=ax,
                cbar_kws={"label": cbar_label})
    plt.title(title)
    st.pyplot(fig)

def analyze_descansos(fixture, players):
    """Analiza descansos consecutivos y genera mapa de calor."""
    descanso_data = []
    for p in players:
        pattern = [1 if p in r["descansan"] else 0 for r in fixture]
        descanso_data.append(pattern)

    df_desc = pd.DataFrame(descanso_data, index=players)
    df_desc["consec_descansos"] = df_desc.apply(
        lambda x: max((sum(1 for _ in g) for k, g in itertools.groupby(x) if k == 1), default=0), axis=1
    )

    st.dataframe(df_desc[["consec_descansos"]].rename(columns={"consec_descansos": "Descansos consecutivos"}))

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(pd.DataFrame(descanso_data, index=players), cmap="YlOrRd", cbar=False, ax=ax)
    plt.title("Mapa de descansos por ronda (1 = descanso)")
    plt.xlabel("Ronda")
    plt.ylabel("Jugador")
    st.pyplot(fig)

def build_matrices(fixture, players):
    """Construye matrices de parejas y enfrentamientos."""
    matrix_parejas = pd.DataFrame(0, index=players, columns=players)
    matrix_enfrentamientos = pd.DataFrame(0, index=players, columns=players)

    for ronda in fixture:
        for partido in ronda["partidos"]:
            p1, p2 = partido["pareja1"], partido["pareja2"]

            # compañeros
            for a, b in itertools.combinations(p1, 2):
                matrix_parejas.loc[a, b] += 1
                matrix_parejas.loc[b, a] += 1
            for a, b in itertools.combinations(p2, 2):
                matrix_parejas.loc[a, b] += 1
                matrix_parejas.loc[b, a] += 1

            # enfrentamientos
            for a in p1:
                for b in p2:
                    matrix_enfrentamientos.loc[a, b] += 1
                    matrix_enfrentamientos.loc[b, a] += 1

    return matrix_parejas, matrix_enfrentamientos


def heatmap_parejas_mixtas_visualizar(matrix, male_players, female_players):
    """
    Toma la matriz Hombre-Mujer y la grafica en Streamlit.
    """
    fig, ax = plt.subplots(figsize=(len(male_players) * 1.5, len(female_players) * 1.5))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Purples", linewidths=.5, linecolor='black', ax=ax,
                cbar_kws={"label": "Veces como Pareja Mixta"})
    ax.set_title("Combinaciones de Parejas Mixtas (Hombre vs. Mujer) 🤝")
    ax.set_xlabel("Hombres")
    ax.set_ylabel("Mujeres")
    st.pyplot(fig)

def heatmap_parejas_mixtas(fixture, male_players, female_players):
    # Crear matriz mujer vs hombre
    matrix = pd.DataFrame(0, index=female_players, columns=male_players)

    for ronda in fixture:
        for partido in ronda["partidos"]:
            p1a, p1b = partido["pareja1"]
            p2a, p2b = partido["pareja2"]

            # --- Pareja 1 ---
            # Detectar quién es mujer y quién es hombre
            for f, m in [(p1a, p1b), (p1b, p1a)]:
                if f in female_players and m in male_players:
                    matrix.loc[f, m] += 1

            # --- Pareja 2 ---
            for f, m in [(p2a, p2b), (p2b, p2a)]:
                if f in female_players and m in male_players:
                    matrix.loc[f, m] += 1

    # === Heatmap ===
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(matrix, annot=True, cmap="Purples", linewidths=.5, ax=ax)
    ax.set_title("Combinaciones de Parejas Mixtas (Mujer con Hombre)")

    return matrix, fig


def analyze_algorithm_results(fixture, male_players, female_players):
    """Ejecuta todo el análisis visual y estadístico del algoritmo, incluyendo el análisis mixto."""
    st.markdown("## 🔍 Análisis de Resultados del Algoritmo")

    players = get_unique_players(fixture)
    matrix_parejas, matrix_enfrentamientos = build_matrices(fixture, players)

    # ----------------------------------------------------
    # 1. Mapa de Calor: Parejas Mixtas (Hombre con Mujer)
    # ----------------------------------------------------
    st.markdown("### 1. Parejas Mixtas (Balanceo por género) 🚺🚹")
    matrix_mixta, _ = heatmap_parejas_mixtas(fixture, male_players, female_players)
    
    # Usar la nueva función de visualización
    heatmap_parejas_mixtas_visualizar(matrix_mixta, male_players, female_players)
    
    st.divider()

    # ----------------------------------------------------
    # 2. Mapa de Calor: Parejas Generales (General)
    # ----------------------------------------------------
    st.markdown("### 2. Parejas Generales (Compañeros totales)")
    # Se utiliza la función existente plot_heatmap
    plot_heatmap(matrix_parejas, 
                 "Frecuencia de jugadores que compartieron pareja (General)", 
                 "PuBuGn", "Veces como pareja")

    st.divider()

    # ----------------------------------------------------
    # 3. Mapa de Calor: Enfrentamientos
    # ----------------------------------------------------
    st.markdown("### 3. Enfrentamientos (Oponentes)")
    plot_heatmap(matrix_enfrentamientos, 
                 "Frecuencia de jugadores que se enfrentaron", 
                 "OrRd", "Veces como oponentes")
                 
    st.divider()

    # ----------------------------------------------------
    # 4. Análisis de Descansos
    # ----------------------------------------------------
    st.markdown("### 4. Análisis de Descansos 😴")
    analyze_descansos(fixture, players)