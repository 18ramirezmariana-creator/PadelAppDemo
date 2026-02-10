import streamlit as st
from assets.auth import check_login
import os,importlib
from assets.sidebar import sidebar_style
from assets.styles import apply_custom_css_main, apply_custom_css_player_setup, DEMO_THEME
from assets.helper_funcs import initialize_vars
from assets.backup import load_from_localstorage, clear_localstorage, save_to_localstorage
st.set_page_config(page_title=" Padel App",page_icon=":tennis:", layout="wide")
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 🔥 CHECK SESSION STATE FOR SAVED TOURNAMENT
# Con la nueva implementación, los datos están en session_state._tournament_data
saved_data = load_from_localstorage()

if saved_data and isinstance(saved_data, dict):
    # Store that we found saved data
    st.session_state.has_saved_tournament = True
    st.session_state.saved_tournament_data = saved_data
else:
    st.session_state.has_saved_tournament = False


#if not check_login():
#    st.stop()

# Cargar la lista de páginas desde la carpeta "pages"
pages_list = ["home"] + [f.replace(".py", "") for f in os.listdir("pages") if f.endswith(".py")]
if "page" not in st.session_state:
    st.session_state.page = "home"  # Start with the homepage    

def load_page(page_name):
    if page_name == "home":
        apply_custom_css_main(DEMO_THEME)

        # 🔥 SHOW RESTORE OPTION IF TOURNAMENT EXISTS
        if st.session_state.get('has_saved_tournament', False):
            saved_data = st.session_state.saved_tournament_data
            
            st.success("💾 ¡Torneo guardado encontrado!")
            
            # Show tournament info
            mod = saved_data.get('mod', 'Desconocido')
            num_players = len(saved_data.get('players', []))
            num_fields = saved_data.get('num_fields', 0)
            
            st.info(f"📋 **{mod}** con {num_players} jugadores en {num_fields} cancha(s)")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Continuar Torneo Guardado", use_container_width=True, type="primary"):
                    # Restore all tournament data to session_state
                    st.session_state.num_fields = saved_data.get('num_fields', 2)
                    st.session_state.num_pts = saved_data.get('num_pts', 16)
                    st.session_state.mod = saved_data.get('mod', 'Parejas Fijas')
                    st.session_state.players = saved_data.get('players', [])
                    st.session_state.num_players = len(st.session_state.players)
                    st.session_state.fixture = saved_data.get('fixture', [])
                    st.session_state.resultados = saved_data.get('resultados', {})
                    st.session_state.code_play = saved_data.get('code_play', '')
                    st.session_state.tournament_key = saved_data.get('tournament_key', '')
                    
                    # Restore mode-specific data
                    if 'parejas' in saved_data:
                        st.session_state.parejas = saved_data['parejas']
                    if 'out' in saved_data:
                        st.session_state.out = saved_data['out']
                    if 'mixto_op' in saved_data:
                        st.session_state.mixto_op = saved_data['mixto_op']
                    if 'num_sets' in saved_data:
                        st.session_state.num_sets = saved_data['num_sets']
                    
                    # Mark as restored and go to tournament page
                    st.session_state.tournament_restored = True
                    st.session_state.page = "torneo"
                    st.rerun()
                    
            with col2:
                if st.button("🗑️ Borrar y Empezar Nuevo", use_container_width=True):
                    clear_localstorage()
                    st.session_state.has_saved_tournament = False
                    if 'saved_tournament_data' in st.session_state:
                        del st.session_state.saved_tournament_data
                    st.rerun()
            
            st.divider()
            st.markdown("**O configura un nuevo torneo:**")
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
                    num_sets = st.number_input("Número de games",value=6,key="num_sets_input")
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
            summary_text += f". Partidos a <strong>{st.session_state.num_sets} games</strong>."
        
        summary_html = f"""
        <div class="tournament-summary">
            <p class="summary-text">📋 {summary_text}</p>
        </div>
        """
        
        st.markdown(summary_html, unsafe_allow_html=True)

        if st.button("Continuar a Registro de Jugadores", key="button0", use_container_width=True):
            if can_continue:
                # 🔥 CLEAR LOCALSTORAGE WHEN STARTING NEW TOURNAMENT
                clear_localstorage()
                st.session_state.has_saved_tournament = False
                if 'saved_tournament_data' in st.session_state:
                    del st.session_state.saved_tournament_data
                
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