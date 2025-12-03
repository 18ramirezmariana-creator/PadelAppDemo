import pandas as pd

def calcular_ranking_parejas_sets(parejas, resultados):
    """
    Calculates the tournament ranking based on set scores.

    Ranking Criteria:
    1. Points (1 for Win, 0 for Loss)
    2. Sets Difference (Sets Won - Sets Lost)
    3. Sets Won (Total)
    """
    # Initialize ranking data structure
    ranking_data = {p: {
        'Partidos Jugados': 0, # PJ
        'Puntos': 0,         # P (1 point for a match win)
        'Sets Ganados': 0,   # SG
        'Sets Perdidos': 0,  # SP
        'Diferencia de Sets': 0 # DS (SG - SP)
    } for p in parejas}

    for (p1, p2), (s1, s2) in resultados.items():
        # Only process matches where at least one team scored a set
        if s1 == 0 and s2 == 0:
            continue

        # Update Matches Played
        ranking_data[p1]['Partidos Jugados'] += 1
        ranking_data[p2]['Partidos Jugados'] += 1

        # Update Sets
        ranking_data[p1]['Sets Ganados'] += s1
        ranking_data[p1]['Sets Perdidos'] += s2
        ranking_data[p2]['Sets Ganados'] += s2
        ranking_data[p2]['Sets Perdidos'] += s1

        # Determine Winner and Update Points
        if s1 > s2:
            # p1 wins the match (more sets won)
            ranking_data[p1]['Puntos'] += 1
        elif s2 > s1:
            # p2 wins the match (more sets won)
            ranking_data[p2]['Puntos'] += 1
        # No points awarded for draws (s1 == s2) as a match must typically have a winner

    # Calculate Sets Difference (DS)
    for p in parejas:
        data = ranking_data[p]
        data['Diferencia de Sets'] = data['Sets Ganados'] - data['Sets Perdidos']

    # Convert to DataFrame and sort
    df_ranking = pd.DataFrame.from_dict(ranking_data, orient='index')
    df_ranking = df_ranking.rename_axis('Pareja').reset_index()

    # Sort Ranking: 1. Puntos (desc), 2. Diferencia de Sets (desc), 3. Sets Ganados (desc)
    df_ranking = df_ranking.sort_values(
        by=['Puntos', 'Diferencia de Sets', 'Sets Ganados'],
        ascending=[False, False, False]
    ).reset_index(drop=True)
    df_ranking.index = df_ranking.index + 1 # Use 1-based indexing for ranking display

    return df_ranking