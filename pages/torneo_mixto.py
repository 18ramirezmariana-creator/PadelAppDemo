import streamlit as st
from models.AmericanoMixto.AllvsAll_MixtoV2 import AmericanoPadelTournament, generar_torneo_mixto,analyze_algorithm_results
from assets.styles import apply_custom_css_torneo_mixto, DEMO_THEME
from assets.helper_funcs import initialize_vars, calcular_ranking_individual, render_nombre
from assets.analyze_funcs import heatmap_parejas_mixtas,heatmap_descansos_por_ronda, heatmap_enfrentamientos
from collections import defaultdict
import random
import pandas as pd

def app():
    st.markdown('<div class="main-title"> Torneo Americano Mixto </div>', unsafe_allow_html=True)
    
    # -----------------------------------------------------
    # 1. FUNCIÓN CALLBACK PARA GUARDAR RESULTADOS AL INSTANTE
    # -----------------------------------------------------
    def actualizar_resultado(pareja1_key, pareja2_key, pareja1_str, pareja2_str):
        """Callback para guardar los puntos en st.session_state.resultados."""
        try:
            val1 = st.session_state[pareja1_key]
            val2 = st.session_state[pareja2_key]
            # La clave de resultados es un tuple de las parejas involucradas
            st.session_state.resultados[(pareja1_str, pareja2_str)] = (val1, val2)
        except KeyError:
            # Esto puede ocurrir si se llama antes de que se hayan inicializado las keys, ignorar
            pass
    # -----------------------------------------------------
    
    # Initialize resultados if not exists
    if 'resultados' not in st.session_state:
        st.session_state.resultados = {}
    
    # Get players and settings from session state
    male_players = st.session_state.hombres
    female_players = st.session_state.mujeres
    num_canchas = st.session_state.num_fields
    puntos_partido = st.session_state.num_pts

    # Validate equal numbers
    if len(male_players) != len(female_players):
        st.error(f"❌ Debes tener el mismo número de hombres y mujeres. Tienes {len(male_players)} hombres y {len(female_players)} mujeres.")
        if st.button("Volver a configuración"):
            st.session_state.page = "players_setup"
            st.rerun()
        return
    
    # Create a unique key for this tournament configuration
    tournament_key = f"mixto_{len(male_players)}_{len(female_players)}_{num_canchas}_{puntos_partido}"
    
    # Generate fixture ONLY if it doesn't exist or configuration changed
    if 'tournament_key' not in st.session_state or st.session_state.tournament_key != tournament_key:
        with st.spinner("Generando fixture optimizado..."):
            out = generar_torneo_mixto(male_players, female_players, 
                                        num_canchas, puntos_partido)
            st.session_state.fixture = out["rondas"]
            st.session_state.out = out
            # NO BORRAMOS st.session_state.resultados aquí, sino solo si el torneo es nuevo.
            # Al cambiar la llave del torneo, esto indica un torneo nuevo, así que lo borramos.
            st.session_state.resultados = {}
            st.session_state.tournament_key = tournament_key

    # Custom CSS
    apply_custom_css_torneo_mixto(DEMO_THEME)

    # Display each round
    for ronda_data in st.session_state.fixture:
        st.markdown(f"### Ronda {ronda_data['ronda']}")
        
        # Create columns for matches
        num_partidos = len(ronda_data["partidos"])
        if num_partidos > 0:
            cols = st.columns(num_partidos)
            
            for c_i, partido in enumerate(ronda_data["partidos"]):
                ayudantes = partido.get("ayudantes", []) or []
                
                # Render player names
                p1_render = [render_nombre(j, ayudantes) for j in partido["pareja1"]]
                p2_render = [render_nombre(j, ayudantes) for j in partido["pareja2"]]
                
                pareja1 = " & ".join(p1_render)
                pareja2 = " & ".join(p2_render)
                
                cancha = partido["cancha"]
                
                with cols[c_i]:
                    # Display match card
                    st.markdown(f"""
                        <div class="match-card">
                            <div class="match-title">Cancha {cancha}</div>
                            <div class="team-name">{pareja1}</div>
                            <div class="vs">VS</div>
                            <div class="team-name">{pareja2}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Score inputs with safe keys
                    raw_p1 = "_".join(partido["pareja1"])
                    raw_p2 = "_".join(partido["pareja2"])
                    
                    # Unique keys for the Streamlit widgets
                    key_p1 = f"score_r{ronda_data['ronda']}_m{c_i}_{raw_p1}_p1"
                    key_p2 = f"score_r{ronda_data['ronda']}_m{c_i}_{raw_p2}_p2"
                    
                    # Unique match key for storing results (uses rendered names)
                    pareja1_str = " & ".join(partido["pareja1"])
                    pareja2_str = " & ".join(partido["pareja2"])
                    
                    # 2. RECUPERAR VALORES GUARDADOS
                    # Usamos el valor por defecto 0, o el valor guardado
                    saved_s1, saved_s2 = st.session_state.resultados.get((pareja1_str, pareja2_str), (0, 0))
                    
                    colA, colB = st.columns(2)
                    with colA:
                        st.number_input(
                            f"Puntos {pareja1}", 
                            key=key_p1, 
                            min_value=0,
                            max_value=puntos_partido,
                            value=saved_s1, # <-- Pasar el valor guardado
                            on_change=actualizar_resultado, # <-- Usar callback
                            kwargs={
                                "pareja1_key": key_p1, 
                                "pareja2_key": key_p2,
                                "pareja1_str": pareja1_str, 
                                "pareja2_str": pareja2_str
                            }
                        )
                    with colB:
                        st.number_input(
                            f"Puntos {pareja2}", 
                            key=key_p2, 
                            min_value=0,
                            max_value=puntos_partido,
                            value=saved_s2, # <-- Pasar el valor guardado
                            on_change=actualizar_resultado, # <-- Usar callback
                            kwargs={
                                "pareja1_key": key_p1, 
                                "pareja2_key": key_p2,
                                "pareja1_str": pareja1_str, 
                                "pareja2_str": pareja2_str
                            }
                        )
                    
                    # 3. ELIMINAR ASIGNACIÓN INMEDIATA.
                    # La asignación (st.session_state.resultados = (score1, score2)) ya no es necesaria
                    # porque el callback la maneja.
        
        # Show resting players
        if ronda_data["descansan"]:
            st.info(f"Descansan: {', '.join(ronda_data['descansan'])}")
        
        st.markdown("---")
    
    # Show summary
    if "out" in st.session_state and "resumen" in st.session_state.out:
        st.markdown("### 📊 Resumen de Participación")
        df_resumen = pd.DataFrame(st.session_state.out["resumen"])
        st.dataframe(df_resumen, use_container_width=True)
    
    #analyze_algorithm_results(st.session_state.fixture,male_players, 
    #    female_players)
    
    # Ranking buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    # El resto del código de navegación y ranking está bien y se mantiene igual.
    with col1:
        if st.button("👀 ¿Cómo va el ranking?", use_container_width=True):
            try:
                # Calculate ranking
                ranking = calcular_ranking_individual(st.session_state.resultados, st.session_state.fixture)
                
                if ranking is not None and not ranking.empty:
                    st.session_state.ranking = ranking
                    st.dataframe(ranking, use_container_width=True)
                else:
                    st.warning("⚠️ No hay suficientes resultados para calcular el ranking")
            except Exception as e:
                st.error(f"❌ Error al calcular ranking: {str(e)}")
                st.write("Detalles del error:", e)
    
    with col2:
        if st.button("🏆 Ver Resultados Finales", use_container_width=True):
            try:
                # Calculate final ranking
                ranking = calcular_ranking_individual(st.session_state.resultados, st.session_state.fixture)
                
                if ranking is not None and not ranking.empty:
                    st.session_state.ranking = ranking
                    st.session_state.page = "z_ranking"
                    st.rerun()
                else:
                    st.warning("⚠️ Debes ingresar al menos algunos resultados antes de ver el ranking final")
            except Exception as e:
                st.error(f"❌ Error al calcular ranking: {str(e)}")

    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Volver", key="back_button", use_container_width=True):
            # Clear tournament data when going back (esto es correcto)
            if 'tournament_key' in st.session_state:
                del st.session_state.tournament_key
            if 'fixture' in st.session_state:
                del st.session_state.fixture
            if 'out' in st.session_state:
                del st.session_state.out
            # Dejamos st.session_state.resultados para que se guarde el estado del fixture.
            # OJO: Si borrabas st.session_state.resultados al volver, también perdías el estado.
            # Lo que quieres es que no se borre al *volver desde el ranking*.
            # Lo dejaré comentado, asumiendo que el usuario quiere borrar el fixture, pero no los resultados.
            # if 'resultados' in st.session_state:
            #     del st.session_state.resultados 
            st.session_state.page = "players_setupMixto"
            st.rerun()