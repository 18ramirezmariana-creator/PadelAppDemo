import streamlit as st
from assets.auth import check_login
import os,importlib
from assets.sidebar import sidebar_style
from assets.styles import apply_custom_css_main, apply_custom_css_player_setup, DEMO_THEME
from assets.helper_funcs import initialize_vars
st.set_page_config(page_title=" Padel App",page_icon=":tennis:", layout="wide")
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
if not check_login():
    st.stop()

# Cargar la lista de páginas desde la carpeta "pages"
pages_list = ["home"] + [f.replace(".py", "") for f in os.listdir("pages") if f.endswith(".py")]
if "page" not in st.session_state:
    st.session_state.page = "home"  # Start with the homepage    

def load_page(page_name):
    if page_name == "home":

        apply_custom_css_main(DEMO_THEME)
        # Título centrado
        st.markdown('<div class="main-title">🏆 Tu Padel App</div>', unsafe_allow_html=True)

        c1,c2 = st.columns(2)
        mixto = False
        with c1:
            num_fields = st.number_input("Número de canchas",value = 2,key="fields_input",min_value=1)
            st.session_state.num_fields = num_fields
            mod = st.selectbox("Modalidad", ["Todos Contra Todos","Parejas Fijas"],key="modalidad_input",index=1)
            st.session_state.mod = mod
            if mod == "Todos Contra Todos":
                composition = st.selectbox("Composición Parejas", ["Aleatorio","Siempre Mixto"],key="mixto_input",index=0)
                st.session_state.mixto_op = composition
                if st.session_state.mixto_op == "Siempre Mixto":
                    mixto = True
                else:
                    mixto = False
        with c2:
            num_players = st.number_input("Número de jugadores",
                                          key="select_players",step=1,min_value=8)
            st.session_state.num_players = num_players
            if ((st.session_state.mod == "Parejas Fijas") or (st.session_state.mixto_op == "Siempre Mixto")) and st.session_state.num_players % 2 != 0:
                st.warning("En esta modalidad el número de jugadores debe ser PAR.")
                can_continue = False
            else:
                can_continue = True
            if st.session_state.mod == "Parejas Fijas":
                pts = st.selectbox("Formato Puntaje", ["Sets","Puntos"],key="scoring",index=1)
                if pts == "Sets":
                    num_sets = st.number_input("Número de sets",value=6,key="num_sets_input")
                    st.session_state.num_sets = num_sets
            elif st.session_state.mod == "Todos Contra Todos":
                pts = "Puntos"
            if pts == "Puntos":
                num_pts = st.number_input("Número de puntos",value=16,key="num_point_input")
                st.session_state.num_pts = num_pts

        # === RESUMEN DEL TORNEO ===
        # Construir el texto del resumen
        summary_text = f"Torneo <strong>{st.session_state.mod}</strong> con <strong>{st.session_state.num_players} jugadores</strong> en <strong>{st.session_state.num_fields} {'cancha' if st.session_state.num_fields == 1 else 'canchas'}</strong>"
        
        # Agregar información de composición solo si es Siempre Mixto
        if st.session_state.mod == "Todos Contra Todos" and st.session_state.mixto_op == "Siempre Mixto":
            summary_text += f", parejas <strong>siempre mixtas</strong>"
        
        # Agregar información de puntaje
        if pts == "Puntos":
            summary_text += f". Partidos a <strong>{st.session_state.num_pts} puntos</strong>."
        elif pts == "Sets":
            summary_text += f". Partidos a <strong>{st.session_state.num_sets} sets</strong>."
        
        summary_html = f"""
        <div class="tournament-summary">
            <p class="summary-text">📋 {summary_text}</p>
        </div>
        """
        
        st.markdown(summary_html, unsafe_allow_html=True)

        if st.button("Continuar a Registro de Jugadores",key="button0",use_container_width=True):
            if can_continue:
                if mixto:
                    st.session_state.page = "players_setupMixto"
                    st.rerun()
                else:
                    st.session_state.page = "players_setup"
                    st.rerun()
            
    
        
    else:
        module = importlib.import_module(f"pages.{page_name}")
        module.app()
current_page = st.session_state.page
load_page(current_page)

sidebar_style()