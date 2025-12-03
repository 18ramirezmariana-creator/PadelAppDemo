import streamlit as st
import pandas as pd

def podium_card(place, player, points, gradient, height):
    """Genera la tarjeta visual para los puestos del podio (Torneo por Puntos)."""
    st.markdown(f"""
        <div style="
            background: {gradient};
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            color: white;
            box-shadow: inset 0 1px 4px rgba(255,255,255,0.4),
                        inset 0 -1px 4px rgba(0,0,0,0.3),
                        0 6px 12px rgba(0,0,0,0.3);
            height: {height}px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="font-size: 14px; background-color: rgba(255,255,255,0.2);
                        padding: 5px 15px; border-radius: 10px; display: inline-block;">
                {place}
            </div>
            <h2 style="margin-top: 15px; margin-bottom: 10px;">{player}</h2>
            <p style="font-size:16px;">{points} Puntos</p>
        </div>
    """, unsafe_allow_html=True)

def podium_card_sets(place,player,points,diff,gradient,height, status_label=None, show_diff=True ):
    """Genera la tarjeta visual para los puestos del podio (Torneo por Sets)."""
    
    # Lógica para mostrar 'CAMPEÓN' o 'SUBCAMPEÓN' en lugar de puntos
    if status_label:
        points_html = f'<p style="font-size:18px;margin-bottom: 5px; font-weight: 800;">{status_label}</p>'
    else:
        points_html = f'<p style="font-size:16px;margin-bottom: 5px; font-weight: 600;">{points} Puntos</p>'
    
    # Lógica para mostrar la Diferencia de Sets (DS)
    diff_html = ''
    if show_diff:
        diff_html = f'<p style="font-size:14px; opacity: 0.8;">DS: {diff} Sets</p>'
        
    st.markdown(f"""
        <div style="background: {gradient};
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            color: white;
            box-shadow: inset 0 1px 4px rgba(255,255,255,0.4),
                        inset 0 -1px 4px rgba(0,0,0,0.3),
                        0 6px 12px rgba(0,0,0,0.3);
            height: {height}px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="font-size: 14px; background-color: rgba(255,255,255,0.2);
                        padding: 5px 15px; border-radius: 10px; display: inline-block;">
                {place}
            </div>
            <h2 style="margin-top: 15px; margin-bottom: 10px;">{player}</h2>
            {points_html}
            {diff_html}

        </div>
    """, unsafe_allow_html=True)

def define_ranking_items(df_group_ranking, col1, col2, col3):
    """
    Define y muestra los elementos del ranking, ajustando el Top 2 basado en el resultado de la final
    si se jugó un torneo por sets con parejas fijas.
    """
    df = df_group_ranking.copy()
    sets_flag = "Diferencia de Sets" in df.columns
    
    # Efecto metálico para cada puesto
    gold_gradient = "linear-gradient(145deg, #FFD700, #E6C200, #FFF6A0)"
    silver_gradient = "linear-gradient(145deg, #C0C0C0, #A9A9A9, #E0E0E0)"
    bronze_gradient = "linear-gradient(145deg, #FFA347, #FF7A00, #FFD08A)"
    
    # --------------------------------------------------------------------------
    # Lógica de Ajuste del Ranking por Final (Solo Sets Parejas Fijas)
    # --------------------------------------------------------------------------
    
    final_teams = st.session_state.get('final_match_teams')
    final_scores = st.session_state.get('final_match_scores')
    show_final = st.session_state.get('show_final', False)
    
    # Determinar si se usará la lógica de la final (solo sets, final jugada y no empate)
    use_final_ranking = sets_flag and show_final and final_teams and final_scores and final_scores[0] != final_scores[1]
    
    if use_final_ranking:
        
        # 1. Determinar Ganador y Subcampeón de la Final
        winner = final_teams[0] if final_scores[0] > final_scores[1] else final_teams[1]
        runner_up = final_teams[1] if winner == final_teams[0] else final_teams[0]
        
        # 2. Obtener las filas del grupo para mantener los stats (Puntos/DS)
        winner_row = df[df['Pareja'] == winner].iloc[0]
        runner_up_row = df[df['Pareja'] == runner_up].iloc[0]

        # 3. Obtener el tercer lugar (el mejor rankeado que no jugó la final)
        
        # Equipos que no jugaron la final
        non_finalists_df = df[~df['Pareja'].isin([winner, runner_up])]
        
        if not non_finalists_df.empty:
            third_place_row = non_finalists_df.iloc[0]
            
            # 4. Reconstruir el DataFrame de ranking final (solo para la visualización)
            
            # Crear las tres filas del podio ordenadas por el resultado de la final
            podium_list = [winner_row.to_dict(), runner_up_row.to_dict(), third_place_row.to_dict()]
            final_podium_df = pd.DataFrame(podium_list)
            
            # Los demás participantes son el resto del ranking, sin el top 3
            others = df[~df['Pareja'].isin(final_podium_df['Pareja'].tolist())]
        else:
            # Caso especial: solo hay 2 equipos o no se puede determinar el 3ro.
            final_podium_df = pd.DataFrame([winner_row.to_dict(), runner_up_row.to_dict()])
            others = pd.DataFrame()
            
    else:
        # Si no hay final, fue empate, o no es torneo por sets, se usa el ranking de fase de grupos
        final_podium_df = df.head(3)
        others = df.iloc[3:]

    # --------------------------------------------------------------------------
    # Renderizado
    # --------------------------------------------------------------------------
    
    # Top 3 rendering
    if sets_flag and not final_podium_df.empty:
        
        # Top 1
        with col1:
            if len(final_podium_df) >= 1:
                row = final_podium_df.iloc[0]
                # Si se usó la lógica de la final, muestra CAMPEÓN y oculta la diferencia de sets
                status_label = "CAMPEÓN" if use_final_ranking else None
                show_diff = not use_final_ranking # Determina si se oculta la DS
                podium_card_sets("🥇 1er Puesto", row["Pareja"], row["Puntos"], row["Diferencia de Sets"], gold_gradient, 300, status_label=status_label, show_diff=show_diff)
        
        # Top 2
        with col2:
            if len(final_podium_df) >= 2:
                row = final_podium_df.iloc[1]
                # Si se usó la lógica de la final, muestra SUBCAMPEÓN FINAL y oculta la diferencia de sets
                status_label = "SUBCAMPEÓN" if use_final_ranking else None
                show_diff = not use_final_ranking # Determina si se oculta la DS
                podium_card_sets("🥈 2do Puesto", row["Pareja"], row["Puntos"], row["Diferencia de Sets"], silver_gradient, 260, status_label=status_label, show_diff=show_diff)
        
        # Top 3 (siempre muestra los puntos del ranking de fase de grupos y la DS)
        with col3:
            if len(final_podium_df) >= 3:
                row = final_podium_df.iloc[2]
                podium_card_sets("🥉 3er Puesto", row["Pareja"], row["Puntos"], row["Diferencia de Sets"], bronze_gradient, 230, show_diff=True)
                
    elif not final_podium_df.empty: # Torneo por Puntos (Jugador)
        # Top 1
        with col1:
            if len(final_podium_df) >= 1:
                row = final_podium_df.iloc[0]
                podium_card("🥇 1er Puesto", row["Jugador"], row["Puntos"], gold_gradient, 300)
        # Top 2
        with col2:
            if len(final_podium_df) >= 2:
                row = final_podium_df.iloc[1]
                podium_card("🥈 2do Puesto", row["Jugador"], row["Puntos"], silver_gradient, 260)
        # Top 3
        with col3:
            if len(final_podium_df) >= 3:
                row = final_podium_df.iloc[2]
                podium_card("🥉 3er Puesto", row["Jugador"], row["Puntos"], bronze_gradient, 230)

    # Others rendering (for both sets and points)
    if not others.empty:
        st.markdown("""
            <div style="text-align:center; margin-top:60px;">
                <h4 style="font-weight:400;"> Otros Participantes</h4>
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
        """, unsafe_allow_html=True)
        
        for rank_position, (idx, row) in enumerate(others.iterrows(), start=len(final_podium_df) + 1):            
            if sets_flag:
                st.markdown(f"""
                <div style="background-color:white;
                                width:80%;
                                max-width:600px;
                                border-radius:15px;
                                margin:10px auto;
                                padding:10px 20px;
                                box-shadow:0 2px 6px rgba(0,0,0,0.1);
                                display:flex;
                                justify-content:space-between;
                                align-items:center;">

                <span style="font-weight:600; color:#5E3187; min-width: 100px;">
                    {rank_position}ᵗʰ — {row['Pareja']}
                </span>

                <div style="text-align: right;">
                    <span style="font-weight:600; color:#333; display:block; font-size:14px;">
                        PG: {row['Puntos']}
                    </span>
                    <span style="font-weight:400; color:#777; font-size: 12px; display:block;">
                        DS: {row['Diferencia de Sets']}
                    </span>
                </div>
                    </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div style="background-color:white;
                                width:60%;
                                max-width:600px;
                                border-radius:15px;
                                margin:10px auto;
                                padding:10px 20px;
                                box-shadow:0 2px 6px rgba(0,0,0,0.1);
                                display:flex;
                                justify-content:space-between;
                                align-items:center;">
                    <span style="font-weight:600; color:#5E3187;">{rank_position}ᵗʰ — {row['Jugador']}</span>
                    <span style="font-weight:500; color:#333;">{row['Puntos']} pts</span>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)