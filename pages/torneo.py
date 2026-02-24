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
    if st.session_state.get("is_restoring_tournament", False):
        st.info("🔄 Restaurando torneo... por favor espera")
        st.stop()

    if "tournament_initialized" not in st.session_state:
        st.session_state.tournament_initialized = False

    # --- 1. VERIFICACIÓN DE SEGURIDAD ---
    # Si por algún motivo llegamos aquí sin jugadores (y el main no pudo restaurar), volvemos al home
    if 'players' not in st.session_state and not st.session_state.get("is_restoring_tournament", False):
        st.warning("⚠️ No se encontraron datos activos. Volviendo al inicio...")
        st.query_params["p"] = "home"
        st.session_state.page = "home"
        st.rerun()

    # --- 2. CONFIGURACIÓN INICIAL ---
    num_canchas = st.session_state.num_fields
    puntos_partido = st.session_state.num_pts
    initialize_vars({"code_play": "", "ranking": "","parejas": []})

    if st.session_state.get('tournament_restored', False):
        st.toast("✅ Datos restaurados correctamente", icon="🔄")
        st.session_state.tournament_restored = False
        st.session_state.tournament_initialized = True
    # --- 3. FUNCIONES DE PERSISTENCIA ---
    def save_current_state():
        """Guarda el estado actual en el navegador"""
        data_to_save = {
            'fixture': st.session_state.get("fixture", []),
            'resultados': st.session_state.get("resultados", {}),
            'mod': st.session_state.mod,
            'num_fields': st.session_state.num_fields,
            'num_pts': st.session_state.num_pts,
            'players': st.session_state.players,
            'num_players': len(st.session_state.players),
            'tournament_key': st.session_state.get("tournament_key", ""),
            'code_play': st.session_state.get("code_play", "")
        }
        # Añadir datos específicos según modalidad
        if st.session_state.mod == "Parejas Fijas":
            data_to_save['parejas'] = st.session_state.get("parejas", [])
        else:
            data_to_save['out'] = st.session_state.get("out", {})
            
        save_to_localstorage(data_to_save)
    # Función Callback para actualizar inmediatamente
    def actualizar_resultado(p1_str, p2_str, k1, k2):
        # 🔒 NO permitir guardado si el torneo no está estable
        if not st.session_state.get("tournament_initialized", False):
            return

        if "players" not in st.session_state:
            return

        if "fixture" not in st.session_state:
            return

        if "resultados" not in st.session_state:
            return

        val1 = st.session_state[k1]
        val2 = st.session_state[k2]

        st.session_state.resultados[(p1_str, p2_str)] = (val1, val2)

        save_current_state()
    
    #divission logica parejas fijas vs aleatorias
    # --- 4. LÓGICA DE MODALIDADES ---
    mod_parejas = st.session_state.mod
    apply_custom_css_torneo(DEMO_THEME)

    if mod_parejas == "Parejas Fijas":
        st.markdown('<div class="main-title"> Torneo Americano - Parejas Fijas </div>', unsafe_allow_html=True)
        
        # Generar fixture solo si no existe o es un torneo nuevo
        tk = f"pf_{len(st.session_state.players)}_{num_canchas}"
        if st.session_state.get('tournament_key') != tk and 'fixture' not in st.session_state:
            generator = FixedPairsTournament(st.session_state.players, num_canchas)
            out = generator.generate_schedule()
            st.session_state.fixture = out["rondas"]
            st.session_state.tournament_key = tk
            st.session_state.resultados = {}
            st.session_state.code_play = "parejas_fijas"
            save_current_state()
            st.session_state.tournament_initialized = True

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
                ranking = calcular_ranking_parejas(st.session_state.players, st.session_state.resultados)
                st.session_state.ranking = ranking
                display_ranking_table(ranking, ranking_type="parejas")


    elif mod_parejas == "Todos Contra Todos":
        st.markdown('<div class="main-title"> Torneo Americano </div>', unsafe_allow_html=True)
        
        tk = f"all_{len(st.session_state.players)}_{num_canchas}"
        if st.session_state.get('tournament_key') != tk and 'fixture' not in st.session_state:
            from models.AllvsAll_Random_modelv3 import AmericanoTournament
            tournament = AmericanoTournament(st.session_state.players, num_canchas)
            schedule, helpers = tournament.generate_tournament()
            out = tournament.format_for_streamlit(schedule, helpers)
            st.session_state.fixture = out["rondas"]
            st.session_state.out = out
            st.session_state.tournament_key = tk
            st.session_state.resultados = {}
            st.session_state.code_play = "AllvsAll"
            save_current_state()
            st.session_state.tournament_initialized = True


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
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Volver y Reiniciar", key="back_button"):
            st.session_state.tournament_initialized = False
            clear_localstorage()
            keys_to_clear = ['fixture', 'resultados', 'tournament_key', 'players', 'out']
            for k in keys_to_clear:
                if k in st.session_state: del st.session_state[k]
            
            st.query_params["p"] = "home" # Sincronizamos URL
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("🏆 Ver Resultados Finales", type="primary", use_container_width=True):
            # Calculamos ranking antes de irnos para asegurar que se guarde el último cambio
            if mod_parejas == "Parejas Fijas":
                ranking = calcular_ranking_parejas(st.session_state.players, st.session_state.resultados)
            else:
                ranking = calcular_ranking_individual(st.session_state.resultados, st.session_state.fixture)
            
            st.session_state.ranking = ranking
            save_current_state()
            
            st.query_params["p"] = "z_ranking" # Sincronizamos URL
            st.session_state.page = "z_ranking"
            st.rerun()