import streamlit as st
from assets.helper_funcs import generar_fixture_parejas
from models.sets.All_pairs_sets import calcular_ranking_parejas_sets
def app():
    st.title('TORNEO POR SETS')
    num_canchas = st.session_state.num_fields
    num_sets = st.session_state.num_sets
    parejas = st.session_state.players
    if 'resultados' not in st.session_state:
        st.session_state.resultados = {}
    tournament_key = f"parejas_fijas_{len(parejas)}_{num_canchas}_{num_sets}_sets"
    # Generate fixture ONLY if it doesn't exist or configuration changed
    if 'tournament_key' not in st.session_state or st.session_state.tournament_key != tournament_key:
        with st.spinner("Generando fixture optimizado..."):
            st.session_state.fixture = generar_fixture_parejas(parejas,num_canchas)
            st.session_state.resultados = {}
            st.session_state.parejas = parejas
            st.session_state.tournament_key = tournament_key
    st.markdown("""
            <style>
            .match-card {
                background-color: #f7f7fb;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 25px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.07);
            }
            .final-match-card {
                background-color: #5E3187; 
                color: white;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 25px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .match-title {
                font-weight: 700;
                font-size: 18px;
                color: #0B0B19;
                margin-bottom: 10px;
            }
            .final-title {
                font-weight: 700;
                font-size: 24px;
                color: white;
                margin-bottom: 10px;
                text-align: center;
            }
            .team-name {
                font-weight: 600;
                color: #0B0B19;
                font-size: 16px;
                text-align: center;
            }
            .final-team-name {
                font-weight: 700;
                color: white;
                font-size: 20px;
                text-align: center;
            }
            .vs {
                font-weight: 800;
                font-size: 20px;
                color: #6C13BF;
                text-align: center;
                margin-top: 8px;
                margin-bottom: 8px;
            }
            .final-vs {
                font-weight: 800;
                font-size: 24px;
                color: #00CED1; /* CAMBIO: Color turquesa estilizado */
                text-align: center;
                margin-top: 15px;
                margin-bottom: 15px;
            }
            
            .stNumberInput input {
            background-color: #5E3187 !important;
            color: white !important; 
            font-weight: 700 !important; 
            }
            .stNumberInput button {
            color: white !important; 
            }
            /* === BOTÓN === */
            .stButton button {
                width: 100%;
                background-color: #0B0B19;
                color: white;
                font-weight: 700;
                font-size: 18px;
                padding: 1em;
                border-radius: 10px;
                margin-top: 40px;
            }
            </style>
        """, unsafe_allow_html=True)
    
    # ----------------------------------------------------------------------
    # FASE DE GRUPOS (FIXTURE)
    # ----------------------------------------------------------------------
    for i, ronda in enumerate(st.session_state.fixture, start=1):
        st.subheader(f"Ronda {i}")
        cols = st.columns(len(ronda))  # una columna por cancha

        for c_i, match in enumerate(ronda):
            p1, p2 = match
            with cols[c_i]:
                st.markdown(f"""
                    <div class="match-card">
                        <div class="match-title">Cancha {c_i+1}</div>
                        <div class="team-name">{p1}</div>
                        <div class="vs">VS</div>
                        <div class="team-name">{p2}</div>
                    </div>
                """, unsafe_allow_html=True)

                colA, colB = st.columns(2)
                # Usamos una clave única basada en el partido, pero en la columna del partido
                match_key = f"{p1}_{p2}_ronda_{i}_cancha_{c_i}"
                
                # Inicializar valores en 0 si no existen
                score1_key = f"{match_key}_p1"
                score2_key = f"{match_key}_p2"
                if score1_key not in st.session_state: st.session_state[score1_key] = 0
                if score2_key not in st.session_state: st.session_state[score2_key] = 0

                with colA:
                    score1 = st.number_input(f"Sets {p1}", key=score1_key, min_value=0, label_visibility="collapsed")
                with colB:
                    score2 = st.number_input(f"Sets {p2}", key=score2_key, min_value=0, label_visibility="collapsed")

                st.session_state.resultados[(p1, p2)] = (score1, score2)

    colY,colX = st.columns(2)
    with colY:
        # Botón para ver ranking temporal
        if st.button("¿Cómo va el ranking? 👀"):
            # Esto solo muestra el ranking temporal, no cambia de página
            st.header('Clasificación Actual')
            st.info(f"Regla: 1 Punto por partido ganado. Desempate por Diferencia de Sets (SG - SP).")
            
            try:
                df_ranking = calcular_ranking_parejas_sets(parejas, st.session_state.resultados)
                
                # Format DataFrame columns for a cleaner display
                col_config = {
                    'Partidos Jugados': st.column_config.NumberColumn("Partidos Jugados", format="%d"),
                    'Puntos': st.column_config.NumberColumn("Puntos", format="%d"),
                    'Sets Ganados': st.column_config.NumberColumn("Sets Ganados", format="%d"),
                    'Sets Perdidos': st.column_config.NumberColumn("Sets Perdidos", format="%d"),
                    'Diferencia de Sets': st.column_config.NumberColumn("Diferencia de Sets", format="%d"),
                }
                
                st.dataframe(
                    df_ranking, 
                    column_order=('Pareja', 'Partidos Jugados', 'Puntos', 'Sets Ganados', 'Sets Perdidos', 'Diferencia de Sets'),
                    column_config=col_config,
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Error al calcular ranking: {str(e)}")
    # ----------------------------------------------------------------------
    # FASE FINALES: Gran Final (Top 2)
    # ----------------------------------------------------------------------
    
    # 1. Calcular el ranking de la fase de grupos para obtener los 2 finalistas
    try:
        df_ranking = calcular_ranking_parejas_sets(parejas, st.session_state.resultados)
    except Exception:
        df_ranking = None

    # Inicializar el estado de la final
    if 'show_final' not in st.session_state:
        st.session_state.show_final = False
        
    # Lógica de renderizado de la final
    if st.session_state.show_final and df_ranking is not None and len(df_ranking) >= 2:
        
        finalists = df_ranking.head(2)['Pareja'].tolist()
        final_p1 = finalists[0]
        final_p2 = finalists[1]
        
        # Separador visual
        st.markdown("<hr style='border: 1px solid #ddd; margin: 50px 0;'>", unsafe_allow_html=True)
        st.header('🏆 Fase Final: Gran Final')
        st.markdown(f"<p style='text-align:center; font-size:18px; font-weight:600;'>El partido final es entre:</p>", unsafe_allow_html=True)
        
        # Centrar la tarjeta de la final
        col_final_spacer_1, col_final_match, col_final_spacer_2 = st.columns([1, 2, 1])

        with col_final_match:
            st.markdown(f"""
                <div class="final-match-card">
                    <div class="final-title">GRAN FINAL</div>
                    <div class="final-team-name">{final_p1}</div>
                    <div class="final-vs">VS</div>
                    <div class="final-team-name">{final_p2}</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"<p style='text-align:center; font-weight:600; color:#00CED1;'>Introduce los sets de la Final</p>", unsafe_allow_html=True)
            colA, colB = st.columns(2)
            
            # Usar claves únicas para el resultado de la final
            final_key_p1 = f"final_sets_{final_p1}"
            final_key_p2 = f"final_sets_{final_p2}"

            # Inicializar los resultados de la final
            if final_key_p1 not in st.session_state: st.session_state[final_key_p1] = 0
            if final_key_p2 not in st.session_state: st.session_state[final_key_p2] = 0

            with colA:
                # Nombre de la pareja (COLOR CAMBIADO A #00CED1)
                st.markdown(f"<p style='color: #00CED1; font-weight: 600; text-align: center; margin-bottom: 5px;'>{final_p1}</p>", unsafe_allow_html=True)
                final_score1 = st.number_input(f"Sets {final_p1}", key=final_key_p1, min_value=0, label_visibility="collapsed")
            with colB:
                # Nombre de la pareja (COLOR CAMBIADO A #00CED1)
                st.markdown(f"<p style='color: #00CED1; font-weight: 600; text-align: center; margin-bottom: 5px;'>{final_p2}</p>", unsafe_allow_html=True)
                final_score2 = st.number_input(f"Sets {final_p2}", key=final_key_p2, min_value=0, label_visibility="collapsed")

            # Almacenar el resultado de la final
            st.session_state.final_match_teams = (final_p1, final_p2)
            st.session_state.final_match_scores = (final_score1, final_score2)
            
            # Mostrar el ganador dinámicamente
            final_winner = ""
            if final_score1 > final_score2:
                final_winner = final_p1
            elif final_score2 > final_score1:
                final_winner = final_p2
            
            if final_winner:
                st.success(f"🎉 **Ganador de la Final:** {final_winner} ({final_score1}-{final_score2})")
            elif final_score1 > 0 or final_score2 > 0:
                 st.warning("El partido es un empate (Sets iguales).")
            else:
                st.markdown("<p style='text-align:center;'>Pendiente de resultado</p>", unsafe_allow_html=True)
    with colX:
        # Mostrar botón para ver la final si hay suficientes equipos y la final no está visible
        if df_ranking is not None and len(df_ranking) >= 2 and not st.session_state.show_final:
            if st.button("🎉 Mostrar Gran Final 🎉", use_container_width=True):
                st.session_state.show_final = True
                st.rerun() # Disparar un nuevo renderizado para mostrar la final
        # Si la final ya se mostró, esta columna queda como espaciador o se puede usar para un botón de ocultar.
    
    # ----------------------------------------------------------------------
    # NAVEGACIÓN
    # ----------------------------------------------------------------------
    
    # Nuevo layout para los botones: Volver, Mostrar Final/Espaciador, Ver Resultados
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Volver", key="back_buttonS", use_container_width=True):
            # Clear tournament data when going back
            if 'tournament_key' in st.session_state:
                del st.session_state.tournament_key
            if 'fixture' in st.session_state:
                del st.session_state.fixture
            if 'resultados' in st.session_state:
                del st.session_state.resultados
            if 'show_final' in st.session_state:
                del st.session_state.show_final
            st.session_state.page = "players_setup"
            st.rerun()


    with col3:
        if st.button("🏆 Ver Resultados Finales", use_container_width=True):
            try:
                # Calculate final ranking (based on group stage)
                df_ranking = calcular_ranking_parejas_sets(parejas, st.session_state.resultados)
                
                if df_ranking is not None and not df_ranking.empty:
                    st.session_state.ranking = df_ranking
                    
                    # Opcionalmente, puedes usar st.session_state.final_match_scores 
                    # para darle un tratamiento especial al campeón en la página de ranking.
                    
                    st.session_state.page = "z_ranking"
                    st.rerun()
                else:
                    st.warning("⚠️ Debes ingresar al menos algunos resultados antes de ver el ranking final")
            except Exception as e:
                st.error(f"❌ Error al calcular ranking: {str(e)}")