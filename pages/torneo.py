import streamlit as st
from assets.helper_funcs import  calcular_ranking_parejas,initialize_vars, calcular_ranking_individual,render_nombre
from models.AmericanoParejas.AmericanoParejasv1 import FixedPairsTournament
from assets.styles import DEMO_THEME,apply_custom_css_torneo,display_ranking_table
from assets.analyze_funcs import analyze_algorithm_results
from models.AllvsAll_Random_modelv3 import AmericanoTournament
from assets.backup import save_to_localstorage, load_from_localstorage, clear_localstorage
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import itertools,random
import numpy as np

def app():
    num_canchas = st.session_state.num_fields
    puntos_partido =st.session_state.num_pts
    to_init = {"code_play": "", "ranking":""}
    initialize_vars(to_init)
    # load from local storage on first run
    if "data_loaded_from_storage" not in st.session_state:
        saved_data = load_from_localstorage()

        if saved_data:
            st.session_state.fixture = saved_data.get("fixture", [])
            st.session_state.resultados = saved_data.get("resultados", {})
            st.session_state.code_play = saved_data.get("code_play", "")
            st.session_state.tournament_key = saved_data.get("tournament_key", "")

            if "parejas" in saved_data:
                st.session_state.parejas = saved_data["parejas"]
            if "out" in saved_data:
                st.session_state.out = saved_data["out"]
            st.success("✅ Torneo restaurado desde la última conexión" )
        st.session_state.data_loaded_from_storage = True
    #helper func to save current state to localstorage
    def save_current_state():
        data_to_save = {
            'fixture': st.session_state.get("fixture", []),
            'resultados': st.session_state.get("resultados", {}),
            'code_play': st.session_state.get("code_play", ""),
            'tournament_key': st.session_state.get("tournament_key", ""),
            'mod':st.session_state.mod,
            'num_fields':st.session_state.num_fields,
            'num_pts':st.session_state.num_pts
        }
        if st.session_state.mod == "Parejas Fijas":
            data_to_save['parejas'] = st.session_state.get("parejas", [])
        elif st.session_state.mod == "Todos Contra Todos":
            data_to_save['out'] = st.session_state.get("out", {})
        save_to_localstorage(data_to_save)

    # Función Callback para actualizar inmediatamente
    def actualizar_resultado(p1_str, p2_str, k1, k2):
        # Leemos el valor actual de los inputs usando sus keys
        val1 = st.session_state[k1]
        val2 = st.session_state[k2]
        # Guardamos inmediatamente en el diccionario de resultados
        st.session_state.resultados[(p1_str, p2_str)] = (val1, val2)
        # Guardar el estado actual en localStorage
        save_current_state()
    
    #divission logica parejas fijas vs aleatorias
    mod_parejas = st.session_state.mod
    if mod_parejas == "Parejas Fijas":
        st.markdown('<div class="main-title"> Torneo Americano - Parejas Fijas </div>', unsafe_allow_html=True)
        parejas = st.session_state.players
        
        # AUTO-GENERATE fixture on first load
        tournament_key = f"parejas_fijas_{len(parejas)}_{num_canchas}_{puntos_partido}"
        if 'tournament_key' not in st.session_state or st.session_state.tournament_key != tournament_key:
            with st.spinner("Generando fixture..."):
                generator = FixedPairsTournament(parejas, num_canchas)
                resultados_torneo = generator.generate_schedule()
                st.session_state.fixture = resultados_torneo["rondas"]
                st.session_state.code_play = "parejas_fijas"
                st.session_state.resultados = {}
                st.session_state.parejas = parejas
                st.session_state.tournament_key = tournament_key
                #save initial fixture to local storage
                save_current_state()
        if st.session_state.code_play == "parejas_fijas" :
            apply_custom_css_torneo(DEMO_THEME)
            for i, ronda in enumerate(st.session_state.fixture, start=1):
                st.subheader(f"Ronda {i}")
            
                # 1. Agrupar partidos por turno
                partidos_por_turno = {}
                for match in ronda['partidos']:
                    turno = match['turno']
                    if turno not in partidos_por_turno:
                        partidos_por_turno[turno] = []
                    partidos_por_turno[turno].append(match)

                # 2. Iterar sobre los turnos dentro de la ronda
                for turno, partidos_del_turno in partidos_por_turno.items():
                    
                    # Solo mostramos el número de turno si hay más de uno
                    if len(partidos_por_turno) > 1:
                        st.markdown(f"**Turno {turno}:**", unsafe_allow_html=True)

                    # Usamos st.columns para visualizar los partidos de ESTE TURNO
                    # El número de columnas es el número de canchas usadas en este turno
                    cols = st.columns(len(partidos_del_turno))

                    for c_i, match in enumerate(partidos_del_turno):
                        # 🎯 CLAVE: Usamos el nombre del equipo/pareja DIRECTAMENTE
                        p1_equipo_str = match['pareja1'] 
                        p2_equipo_str = match['pareja2'] 

                        with cols[c_i]:
                            st.markdown(f"""
                                <div class="match-card">
                                    <div class="match-title">Cancha {match['cancha']}</div>
                                    <div class="team-name">{p1_equipo_str}</div>
                                    <div class="vs">VS</div>
                                    <div class="team-name">{p2_equipo_str}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # --- Input de Resultados a nivel de EQUIPO ---
                            # Las keys y los strings de referencia usan el nombre completo de la pareja.
                            k1 = f"{p1_equipo_str}_vs_{p2_equipo_str}_p1"
                            k2 = f"{p1_equipo_str}_vs_{p2_equipo_str}_p2"
                            
                            # Recuperar resultados usando los nombres de los equipos
                            saved_s1, saved_s2 = st.session_state.resultados.get((p1_equipo_str, p2_equipo_str), (0, 0))

                            colA, colB = st.columns(2)
                            with colA:
                                # Etiqueta de input con el nombre del equipo
                                st.number_input(
                                    f"Puntos {p1_equipo_str}", 
                                    key=k1, 
                                    min_value=0,
                                    max_value=puntos_partido, 
                                    value=saved_s1,
                                    on_change=actualizar_resultado,
                                    kwargs={"p1_str": p1_equipo_str, "p2_str": p2_equipo_str, "k1": k1, "k2": k2}
                                )
                            with colB:
                                # Etiqueta de input con el nombre del equipo
                                st.number_input(
                                    f"Puntos {p2_equipo_str}", 
                                    key=k2, 
                                    min_value=0,
                                    max_value=puntos_partido, 
                                    value=saved_s2,
                                    on_change=actualizar_resultado,
                                    kwargs={"p1_str": p1_equipo_str, "p2_str": p2_equipo_str, "k1": k1, "k2": k2})

                # Mostrar parejas que descansan
                parejas_descansando = ronda['descansan'] # Directamente del diccionario
                if parejas_descansando:
                    st.info(f"Descansan en Ronda {i}: {', '.join(parejas_descansando)}")
            # --- Ranking Final ---            
            if st.button("¿Cómo va el ranking? 👀", key="ranking_parejas",use_container_width=True):
                ranking = calcular_ranking_parejas(st.session_state.parejas, st.session_state.resultados)
                st.session_state.ranking = ranking
                display_ranking_table(ranking, ranking_type="parejas")


    elif mod_parejas == "Todos Contra Todos":
        def generar_torneo_todos_contra_todos(jugadores, num_canchas, seed=None):
            if seed:
                random.seed(seed)
            
            tournament = AmericanoTournament(st.session_state.players, num_canchas)
            schedule, helpers = tournament.generate_tournament()
            return tournament.format_for_streamlit(schedule, helpers)
        
        st.markdown('<div class="main-title"> Torneo Americano</div>', unsafe_allow_html=True)

        
        # AUTO-GENERATE fixture on first load (igual que en sets)
        jugadores = st.session_state.players
        tournament_key = f"todos_contra_todos_{len(jugadores)}_{num_canchas}_{puntos_partido}"
        
        if 'tournament_key' not in st.session_state or st.session_state.tournament_key != tournament_key:
            with st.spinner("Generando fixture optimizado..."):
                out = generar_torneo_todos_contra_todos(jugadores, num_canchas, seed=42)
                st.session_state.code_play = "AllvsAll"
                st.session_state.fixture = out["rondas"]
                st.session_state.out = out
                st.session_state.resultados = {}
                st.session_state.tournament_key = tournament_key
                save_current_state()


        # Visualización especial para Todos Contra Todos
        if st.session_state.code_play == "AllvsAll":
            apply_custom_css_torneo(DEMO_THEME)

            for ronda_data in st.session_state.fixture:
                st.subheader(f"Ronda {ronda_data['ronda']}")
                cols = st.columns(len(ronda_data["partidos"]))

                for c_i, partido in enumerate(ronda_data["partidos"]):
                    ayudantes = partido.get("ayudantes", []) or []
                    # aplicar ícono a los nombres que son ayudantes
                    p1_render = [render_nombre(j, ayudantes) for j in partido["pareja1"]]
                    p2_render = [render_nombre(j, ayudantes) for j in partido["pareja2"]]

                    pareja1 = " & ".join(p1_render)
                    pareja2 = " & ".join(p2_render)
                    if ayudantes:
                        lista_ayudantes = ", ".join([render_nombre(a, ayudantes) for a in ayudantes])
                        ayud_text = f"<div style='font-size:14px;color:#6C13BF;margin-top:5px;'>Ayudantes: {lista_ayudantes}</div>"
                    else:
                        ayud_text = ""

                    cancha = partido["cancha"]

                    with cols[c_i]:
                        st.markdown(f"""
                            <div class="match-card">
                                <div class="match-title">Cancha {cancha}</div>
                                <div class="team-name">{pareja1}</div>
                                <div class="vs">VS</div>
                                <div class="team-name">{pareja2}</div>
                                {ayud_text}
                            </div>
                        """, unsafe_allow_html=True)

                        # --- keys seguras basadas en nombres reales ---
                        raw_p1 = "_".join(partido["pareja1"])
                        raw_p2 = "_".join(partido["pareja2"])

                        key_p1 = f"score_r{ronda_data['ronda']}_m{c_i}_{raw_p1}_p1"
                        key_p2 = f"score_r{ronda_data['ronda']}_m{c_i}_{raw_p2}_p2"

                        # --- CAMBIO: Recuperar valores guardados si existen ---
                        pareja1_str = " & ".join(partido["pareja1"])
                        pareja2_str = " & ".join(partido["pareja2"])
                        # Buscamos si ya hay un resultado guardado para este partido
                        saved_s1, saved_s2 = st.session_state.resultados.get((pareja1_str, pareja2_str), (0, 0))

                        colA, colB = st.columns(2)
                        with colA:
                            st.number_input(
                                f"Puntos {pareja1}", 
                                key=key_p1, 
                                min_value=0,
                                max_value=puntos_partido, 
                                value=saved_s1,
                                on_change=actualizar_resultado,
                                kwargs={"p1_str": pareja1_str, "p2_str": pareja2_str, "k1": key_p1, "k2": key_p2}
                            )
                        with colB:
                            st.number_input(
                                f"Puntos {pareja2}", 
                                key=key_p2, 
                                min_value=0,
                                max_value=puntos_partido, 
                                value=saved_s2,
                                on_change=actualizar_resultado,
                                kwargs={"p1_str": pareja1_str, "p2_str": pareja2_str, "k1": key_p1, "k2": key_p2}
                            )

                if ronda_data["descansan"]:
                    st.info(f"Descansan: {', '.join(ronda_data['descansan'])}")
                        
            # Mostrar resumen de partidos jugados y descansos
            if "out" in st.session_state and "resumen" in st.session_state.out:
                st.markdown("### Resumen de participación")
                st.dataframe(st.session_state.out["resumen"])
            
            # --- Ranking Final ---
            if st.button("¿Cómo va el ranking? 👀",use_container_width=True):
                ranking = calcular_ranking_individual(st.session_state.resultados, st.session_state.fixture)
                st.session_state.ranking = ranking
                display_ranking_table(ranking, ranking_type="individual")
            

    # --- Navegación inferior ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Volver y Reiniciar", key="back_button"):
            clear_localstorage()
            # Limpiar datos del torneo al volver
            if 'tournament_key' in st.session_state:
                del st.session_state.tournament_key
            if 'fixture' in st.session_state:
                del st.session_state.fixture
            if 'resultados' in st.session_state:
                del st.session_state.resultados
            if 'data_loaded_from_storage' in st.session_state:
                del st.session_state.data_loaded_from_storage
            st.session_state.page = "players_setup"
            st.rerun()
    with col2:
        if st.button("Ver Resultados Finales 🏆"):
            if mod_parejas == "Parejas Fijas":
                ranking = calcular_ranking_parejas(st.session_state.parejas, st.session_state.resultados)
            elif mod_parejas == "Todos Contra Todos":
                ranking = calcular_ranking_individual(st.session_state.resultados,st.session_state.fixture)
            st.session_state.ranking = ranking
            save_current_state()
            st.session_state.page = "z_ranking"
            st.rerun()