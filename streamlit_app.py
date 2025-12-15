import streamlit as st
import os,importlib
from assets.sidebar import sidebar_style
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

# Cargar la lista de páginas desde la carpeta "pages"
pages_list = ["home"] + [f.replace(".py", "") for f in os.listdir("pages") if f.endswith(".py")]
if "page" not in st.session_state:
    st.session_state.page = "home"  # Start with the homepage    

def load_page(page_name):
    if page_name == "home":

        st.markdown("""
            <style>
            
            /* Definición del color azul principal */
            :root {
                --main-blue: #1061a0;
                --main-white: white;
            }

            /* Aplicar color de fondo azul a toda la aplicación (si es posible en Streamlit) y texto blanco por defecto */
            body, .stApp {
                background-color: var(--main-blue) !important;
                color: var(--main-white) !important;
            }

            /* === TÍTULO PRINCIPAL === */
            .main-title {
                text-align: center;
                font-size: 36px;
                color: var(--main-white) !important; /* Letras blancas */
                font-weight: 700;
                margin-bottom: 50px;
            }

            /* === ALTURA UNIFORME PARA TODOS LOS INPUTS (Fondo y Letras) === */

            /* Number Input Container */
            .stNumberInput {
                margin-bottom: 25px !important;
            }

            .stNumberInput > div {
                height: 52px !important;
                display: flex !important;
                align-items: center !important;
            }

            /* Number Input - Campo de texto (Fondo azul, texto blanco) */
            .stNumberInput input {
                height: 52px !important;
                min-height: 52px !important;
                max-height: 52px !important;
                width: 100% !important;
                padding: 0 18px !important;
                font-size: 20px !important;
                border-radius: 10px !important;
                background-color: var(--main-blue) !important; /* Fondo azul */
                color: var(--main-white) !important; /* Texto blanco (puntajes) */
                line-height: 52px !important;
                box-sizing: border-box !important;
            }

            /* Number Input - Botones +/- (Fondo azul, texto blanco) */
            .stNumberInput button {
                height: 52px !important;
                min-height: 52px !important;
                max-height: 52px !important;
                color: var(--main-white) !important;
                background-color: var(--main-blue) !important; /* Asegura que el fondo sea azul si es un elemento separado */
                border: 1px solid var(--main-white) !important; /* Borde blanco para separador */
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }

            /* Contenedor de los botones */
            .stNumberInput > div > div {
                height: 52px !important;
                display: flex !important;
                align-items: stretch !important;
            }

            /* === SELECTBOX IGUALADOS (Fondo azul, texto blanco) === */
            .stSelectbox {
                margin-bottom: 25px !important;
            }

            div[data-baseweb="select"] {
                height: 52px !important;
                min-height: 52px !important;
                max-height: 52px !important;
            }

            div[data-baseweb="select"] > div {
                height: 52px !important;
                min-height: 52px !important;
                max-height: 52px !important;
                padding: 0 18px !important;
                font-size: 20px !important;
                border-radius: 10px !important;
                background-color: var(--main-blue) !important; /* Fondo azul */
                color: var(--main-white) !important; /* Texto blanco */
                display: flex !important;
                align-items: center !important;
                width: 100% !important;
                box-sizing: border-box !important;
            }

            /* Opciones desplegables del Selectbox (ajuste adicional) */
            div[data-baseweb="menu"] {
                background-color: var(--main-blue) !important; /* Fondo azul del menú desplegable */
                color: var(--main-white) !important; /* Texto blanco en las opciones */
            }
            
            div[data-baseweb="menu"] li {
                color: var(--main-white) !important; /* Texto blanco en los items del menú */
            }

            /* === LABELS MÁS GRANDES Y EN NEGRILLA (Letras blancas) === */
            label, .stSelectbox label, .stNumberInput label {
                font-size: 24px !important;
                font-weight: 700 !important;
                color: var(--main-white) !important; /* Letras blancas */
                margin-bottom: 6px !important;
            }
            
            /* Forzar negrilla en todos los labels */
            div[data-testid="stNumberInput"] label,
            div[data-testid="stSelectbox"] label {
                font-weight: 700 !important;
            }

            /* === RESUMEN DEL TORNEO (Fondo azul, texto blanco) === */
            .tournament-summary {
                background-color: var(--main-blue) !important; /* Fondo azul */
                border-left: 4px solid var(--main-white) !important; /* Borde de contraste blanco */
                border-radius: 8px;
                padding: 20px 25px;
                margin: 35px 0 25px 0;
                color: var(--main-white) !important; /* Texto blanco por si acaso */
            }

            .summary-text {
                color: var(--main-white) !important; /* Texto blanco */
                font-size: 18px;
                line-height: 1.6;
                margin: 0;
            }

            .summary-text strong {
                color: var(--main-white) !important; /* Texto blanco resaltado */
                font-weight: 700;
            }

            /* === BOTÓN (Fondo azul, texto blanco) === */
            .stButton button {
                width: 100%;
                background-color:black !important; /* Fondo azul */
                color: var(--main-white) !important; /* Texto blanco */
                font-weight: 700;
                font-size: 18px;
                padding: 1em;
                border-radius: 10px;
                border: 2px solid var(--main-white) !important; /* Borde blanco para contraste */
                margin-top: 20px;
            }
            
            /* Hover del botón */
            .stButton button:hover {
                background-color: var(--main-white) !important; /* Fondo blanco al pasar el ratón */
                color: var(--main-blue) !important; /* Texto azul al pasar el ratón */
            }

            /* === AJUSTES DE STREAMLIT === */
            div[data-testid="column"] { padding: 0 30px !important; } 
            section.main > div { padding-top: 30px; }
            
            /* Para el contenedor principal de Streamlit y barra lateral */
            .stSidebar, section.main {
                background-color: var(--main-blue) !important;
            }
            
            /* Texto genérico en toda la app */
            .stMarkdown, .stText, .stAlert, p, h1, h2, h3, h4, h5, h6 {
                color: var(--main-white) !important;
            }

            </style>
    """, unsafe_allow_html=True)

        # Título centrado
        st.markdown('<div class="main-title">🏆 Padel App</div>', unsafe_allow_html=True)

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