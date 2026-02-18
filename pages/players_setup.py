import streamlit as st
from assets.styles import apply_custom_css_player_setup, DEMO_THEME
from assets.backup import save_to_localstorage # Importante para guardar antes de empezar

def update_player_name(idx, key):
    try:
        st.session_state.players[idx] = st.session_state[key]
    except IndexError:
        pass

def app():
    # --- 1. VERIFICACIÓN DE SEGURIDAD ---
    # Si se pierde el session_state, intentamos recuperar num_players
    if "num_players" not in st.session_state:
        st.warning("Configuración no encontrada. Volviendo al inicio...")
        st.session_state.page = "home"
        st.query_params["p"] = "home"
        st.rerun()

    num_players = st.session_state.num_players
    mod = st.session_state.get("mod", "Todos Contra Todos")
    
    st.markdown('<div class="main-title">🏅 Registro de Jugadores</div>', unsafe_allow_html=True)
    
    # Lógica de tarjetas
    if mod == "Todos Contra Todos":
        card_label = "Jugador"
        num_cards = num_players
    elif mod == "Parejas Fijas":
        card_label = "Pareja"
        num_cards = num_players // 2
    else:
        card_label = "Elemento"
        num_cards = 0 
        
    # 🔥 FIX: Si venimos de un torneo nuevo, siempre reiniciar players
    if st.session_state.get("starting_new_tournament", False):
        st.session_state.players = [""] * num_cards
        st.session_state.starting_new_tournament = False  # Consumir el flag
    elif "players" not in st.session_state:
        st.session_state.players = [""] * num_cards
    else:
        current_len = len(st.session_state.players)
        if current_len < num_cards:
            st.session_state.players += [""] * (num_cards - current_len)
        elif current_len > num_cards: 
            st.session_state.players = st.session_state.players[:num_cards]
            
    apply_custom_css_player_setup(DEMO_THEME)

    # --- 2. ENTRADAS DE TEXTO ---
    cols_per_row = 4
    for i in range(0, num_cards, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < num_cards:
                player_key = f"player_input_{idx}"
                with col:
                    st.text_input(
                        f"{card_label} {idx+1}",
                        value=st.session_state.players[idx],
                        key=player_key,
                        on_change=update_player_name,
                        kwargs={"idx": idx, "key": player_key}
                    )

    st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
    
    # Validaciones
    players_clean = [p.strip() for p in st.session_state.players if p.strip()]
    duplicated = len(players_clean) != len(set(players_clean))
    incomplete = len(players_clean) < num_cards

    if duplicated:
        st.error("⚠️ Hay nombres repetidos o vacíos.")
    elif incomplete:
        st.warning("⚠️ Completa todos los nombres para continuar.")

    # --- 3. NAVEGACIÓN ---
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Volver", key="back_button", use_container_width=True):
            st.session_state.page = "home"
            st.query_params["p"] = "home"
            st.rerun()

    with col2:
        disabled = duplicated or incomplete
        if st.button("Empezar Torneo 🔥", key="next_button", disabled=disabled, use_container_width=True, type="primary"):
            
            # 🔥 PASO CRUCIAL: Guardar configuración inicial en LocalStorage antes de saltar
            # Esto evita que si el internet falla justo al cargar la página de torneo, se pierdan los nombres.
            data_to_save = {
                'mod': st.session_state.mod,
                'num_fields': st.session_state.num_fields,
                'num_pts': st.session_state.get('num_pts', 16),
                'players': st.session_state.players,
                'num_players': st.session_state.num_players
            }
            save_to_localstorage(data_to_save)

            # Navegación con URL
            target_page = "torneo" # O "torneo_sets" si usas archivos separados
            st.session_state.page = target_page
            st.query_params["p"] = target_page
            st.rerun()