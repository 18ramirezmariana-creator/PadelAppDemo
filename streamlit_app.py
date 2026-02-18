import streamlit as st
from assets.auth import check_login
import os, importlib
from assets.sidebar import sidebar_style
from assets.styles import apply_custom_css_main, apply_custom_css_player_setup, DEMO_THEME
from assets.helper_funcs import initialize_vars
from assets.backup import load_from_localstorage, clear_localstorage, load_from_browser

st.set_page_config(page_title=" Padel App", page_icon=":tennis:", layout="wide")

# --- 1. ESTILOS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# --- 2. NAVEGACIÓN RESISTENTE ---
if "page" not in st.session_state:
    # Prioridad: 1. URL (?p=...), 2. Home
    st.session_state.page = st.query_params.get("p", "home")

def navigate_to(page_name):
    """Actualiza estado, actualiza URL y recarga"""
    st.session_state.page = page_name
    st.query_params["p"] = page_name
    st.rerun()

# --- 3. GESTIÓN DE DATOS Y RECUPERACIÓN AUTOMÁTICA ---
saved_data = load_from_browser()
if "is_restoring_tournament" not in st.session_state:
    st.session_state.is_restoring_tournament = False

if (
    st.session_state.page != "home"
    and "players" not in st.session_state
    and saved_data
):
    st.session_state.is_restoring_tournament = True
    restored_data = saved_data

    if restored_data:
        for key, value in restored_data.items():
            st.session_state[key] = value
        
        st.session_state.is_restoring_tournament = False
        st.toast("🔄 Conexión restablecida: Datos recuperados")
        st.rerun()
    else:
        st.session_state.is_restoring_tournament = False
        st.session_state.page = "home"
        st.query_params["p"] = "home"
        st.rerun()
# Evita ejecución parcial mientras restaura
if st.session_state.get("is_restoring_tournament", False):
    st.stop()

st.session_state.has_saved_tournament = bool(saved_data)

# --- 4. RENDERIZADO DE PÁGINAS ---
def load_page(page_name):
    if page_name == "home":
        apply_custom_css_main(DEMO_THEME)

        # OPCIÓN DE RESTAURAR TORNEO EXISTENTE
        if st.session_state.get('has_saved_tournament', False) and saved_data:
            st.success("💾 ¡Torneo guardado encontrado!")
            
            mod = saved_data.get('mod', 'Desconocido')
            num_players = len(saved_data.get('players', []))
            num_fields = saved_data.get('num_fields', 0)
            
            st.info(f"📋 **{mod}** con {num_players} jugadores en {num_fields} cancha(s)")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Continuar Torneo", use_container_width=True, type="primary"):
                    for key, value in saved_data.items():
                        st.session_state[key] = value
                    st.session_state.tournament_restored = True
                    navigate_to("torneo")
                    
            with col2:
                if st.button("🗑️ Borrar y Empezar Nuevo", use_container_width=True):
                    clear_localstorage()
                    st.session_state.has_saved_tournament = False
                    navigate_to("home")
            
            st.divider()
            st.markdown("**O configura un nuevo torneo:**")

        st.markdown('<div class="main-title">🏆 Tu Padel App</div>', unsafe_allow_html=True)

        # --- FORMULARIO DE CONFIGURACIÓN ---
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.num_fields = st.number_input("Número de canchas", value=2, key="fields_input", min_value=1)
            st.session_state.mod = st.selectbox("Modalidad", ["Todos Contra Todos", "Parejas Fijas"], key="modalidad_input", index=1)
            
            mixto = False
            if st.session_state.mod == "Todos Contra Todos":
                st.session_state.mixto_op = st.selectbox("Composición Parejas", ["Aleatorio", "Siempre Mixto"], key="mixto_input")
                mixto = (st.session_state.mixto_op == "Siempre Mixto")
        
        with c2:
            st.session_state.num_players = st.number_input("Número de jugadores", key="select_players", step=1, min_value=8)
            
            # Validación de paridad
            can_continue = True
            if (st.session_state.mod == "Parejas Fijas" or mixto) and st.session_state.num_players % 2 != 0:
                st.warning("⚠️ Esta modalidad requiere número de jugadores PAR.")
                can_continue = False
            
            # Formato de puntos/sets
            if st.session_state.mod == "Parejas Fijas":
                pts_format = st.selectbox("Formato Puntaje", ["Sets", "Puntos"], index=1)
                if pts_format == "Sets":
                    st.session_state.num_sets = st.number_input("Número de games", value=6)
                else:
                    st.session_state.num_pts = st.number_input("Número de puntos", value=16)
            else:
                st.session_state.num_pts = st.number_input("Número de puntos", value=16)

        if st.button("Continuar a Registro de Jugadores", key="btn_start", use_container_width=True):
            if can_continue:
                st.session_state.starting_new_tournament = True  # 🔥 FLAG CRÍTICO

                # 🔥 FIX: Forzar valores actuales del formulario
                st.session_state.mod = st.session_state.modalidad_input
                st.session_state.num_players = st.session_state.select_players
                st.session_state.num_fields = st.session_state.fields_input

                keys_to_clear = [
                    "players",
                    "rounds",
                    "results",
                    "matches",
                    "tournament_restored",
                    "fixture",
                    "resultados",
                    "tournament_key",
                    "code_play",
                    "out",
                    "parejas",
                    "ranking"
                ]

                for k in keys_to_clear:
                    if k in st.session_state:
                        del st.session_state[k]

                clear_localstorage()

                target = "players_setupMixto" if mixto else "players_setup"
                navigate_to(target)

    else:
        # Carga dinámica de páginas en /pages
        try:
            module = importlib.import_module(f"pages.{page_name}")
            module.app()
        except Exception as e:
            st.error(f"Error al cargar la página: {e}")
            if st.button("Volver al Inicio"):
                navigate_to("home")

# Ejecución
load_page(st.session_state.page)
sidebar_style()