import streamlit as st

# -----------------------------------------------------
# 1. FUNCIÓN CALLBACK PARA ACTUALIZAR EL NOMBRE AL INSTANTE
# -----------------------------------------------------
def update_player_name(idx, key):
    """
    Callback para sincronizar el valor del widget (st.session_state[key])
    con el elemento correspondiente en la lista maestra (st.session_state.players).
    """
    # El valor actualizado por el usuario ya está en st.session_state[key]
    # Lo asignamos a la lista maestra.
    try:
        st.session_state.players[idx] = st.session_state[key]
    except IndexError:
        # En caso de que el índice sea incorrecto (poco probable aquí, pero buena práctica)
        pass

def app():
    # Obtener número de jugadores desde la primera página
    num_players = st.session_state.get("num_players")
    # Asegúrate de que mod existe
    mod = st.session_state.get("mod", "Todos Contra Todos")
    
    # === TÍTULO ===
    st.markdown('<div class="main-title">🏅 Registro de Jugadores</div>', unsafe_allow_html=True)
    
    # Lógica según modalidad
    if mod == "Todos Contra Todos":
        card_label = "Jugador"
        st.write(f"Ingresa los nombres de los **{num_players} jugadores**:")
        num_cards = num_players
    elif mod == "Parejas Fijas":
        card_label = "Pareja"
        st.write("Ingresa los nombres de cada pareja con este formato: jugador1-jugador2")
        num_cards = num_players // 2
    else:
        # Manejo de caso por defecto o error si 'mod' es inesperado
        card_label = "Elemento"
        num_cards = 0 
        
    # Asegurar que la lista 'players' tenga la longitud correcta
    if "players" not in st.session_state:
        st.session_state.players = [""]*num_cards
    else:
        current_len = len(st.session_state.players)
        if current_len < num_cards:
            st.session_state.players += [""] * (num_cards - current_len)
        # El código original usaba 'num_players' aquí, pero debe ser 'num_cards'
        elif current_len > num_cards: 
            st.session_state.players = st.session_state.players[:num_cards]
            
    # === ESTILOS ===
    st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 32px;
            color: #6C13BF;
            font-weight: 700;
            margin-bottom: 40px;
        }

        .player-label {
            font-weight: 700 !important;
            font-size: 20px !important;
            color: #0B0B19 !important;
        }

        /* Input estilo tarjeta */
        .stTextInput input {
            background-color: #f7f7fb !important;
            border-radius: 12px !important;
            font-size: 18px !important;
            padding: 18px 10px !important;
            height: 45px !important;        /* un poco más alto */
            color: #0B0B19 !important;
            text-align: center !important;
            font-weight: 500 !important;
            border: 1px solid #ddd !important;
            width: 95% !important;          /* solo un poco más angosto */
            box-sizing: border-box !important;
        }

        .stTextInput input:focus {
            border: 2px solid #6C13BF !important;
            outline: none !important;
        }

        /* Espaciado entre columnas */
        div[data-testid="column"] {
            padding-left: 45px !important;
            padding-right: 45px !important;
        }

        /* Botón principal */
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

    
    # === ENTRADAS DE JUGADORES (REFECTORIZADO) ===
    cols_per_row = 4
    for i in range(0, num_cards, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < num_cards:
                # 1. Definir la clave única
                player_key = f"player_{idx}"
                with col:
                    st.text_input(
                        f"{card_label} {idx+1}",
                        # 2. Inicializar con el valor actual de la lista maestra
                        value=st.session_state.players[idx],
                        key=player_key,
                        # 3. Usar on_change para actualizar la lista maestra
                        on_change=update_player_name,
                        kwargs={
                            "idx": idx, 
                            "key": player_key
                        }
                    )
                    # NOTA CLAVE: Ya no se usa la asignación directa: st.session_state.players[idx] = st.text_input(...)

    st.markdown("<div style='margin-top:180px;'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    # === BOTÓN ATRAS ===
    with col1:
        if st.button("Volver a Configuración", key="back_button"):
            st.session_state.page = "home"
            st.rerun()

        # === BOTÓN SIGUIENTE ===
    with col4:
        players = [p.strip() for p in st.session_state.players if p.strip()]
        duplicated = len(players) != len(set(players))
        incomplete = len(players) < num_cards

        if duplicated:
            st.error("⚠️ Hay nombres repetidos. Corrige antes de continuar.")
        elif incomplete:
            st.warning("⚠️ Todos los nombres deben estar llenos.")

        disabled = duplicated or incomplete
        
        # Streamlit ejecuta el botón y luego la lógica condicional
        if st.button("Empezar Torneo 🔥", key="next_button", disabled=disabled):
            if "num_sets" in st.session_state:
                st.session_state.page = "torneo_sets"
                st.rerun()
            else:
                st.session_state.page = "torneo"
                st.rerun()