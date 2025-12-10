import streamlit as st

# -----------------------------------------------------
# 1. FUNCIÓN CALLBACK PARA ACTUALIZAR EL NOMBRE AL INSTANTE
# -----------------------------------------------------
def update_player_name(gender, idx, key):
    """
    Callback para sincronizar el valor del widget (st.session_state[key])
    con el elemento correspondiente en la lista maestra (st.session_state.hombres o st.session_state.mujeres).
    """
    # El valor actualizado por el usuario ya está en st.session_state[key]
    
    if gender == "hombres":
        target_list = st.session_state.hombres
    elif gender == "mujeres":
        target_list = st.session_state.mujeres
    else:
        return # No hacer nada si el género no es válido

    try:
        # Lo asignamos a la lista maestra.
        target_list[idx] = st.session_state[key]
    except IndexError:
        # En caso de que el índice sea incorrecto
        pass

def app():
    num_players = st.session_state.get("num_players")
    # Asegúrate de que mod existe (aunque en esta página asumimos que es 'Mixto')
    mod = st.session_state.get("mod", "Mixto")
    
    # === TÍTULO ===
    st.markdown('<div class="main-title">🏅 Registro de Jugadores (Mixto)</div>', unsafe_allow_html=True)

    # El número de jugadores debe ser par para Mixto.
    if num_players is None or num_players % 2 != 0:
         st.error("Error: El número de jugadores debe ser par para esta modalidad.")
         # Opcional: Redirigir o establecer valores por defecto
         n_hombres = n_mujeres = 0
    else:
        n_hombres = n_mujeres = int(num_players / 2)

    # === Inicializar listas en session_state ===
    if "hombres" not in st.session_state:
        st.session_state.hombres = [""] * n_hombres
    if "mujeres" not in st.session_state:
        st.session_state.mujeres = [""] * n_mujeres

    # Ajustar largo de listas al cambiar inputs (si num_players cambia)
    if len(st.session_state.hombres) != n_hombres:
        st.session_state.hombres = st.session_state.hombres[:n_hombres] + [""] * max(0, n_hombres - len(st.session_state.hombres))

    if len(st.session_state.mujeres) != n_mujeres:
        st.session_state.mujeres = st.session_state.mujeres[:n_mujeres] + [""] * max(0, n_mujeres - len(st.session_state.mujeres))

    # === ESTILOS ===
    st.markdown("""
    <style>
        .main-title { text-align: center; font-size: 32px; color: #6C13BF; font-weight: 700; margin-bottom: 40px; }
        .gender-title { font-size: 24px; font-weight: 700; margin-top: 30px; margin-bottom: 10px; color: #0B0B19; }
        .stTextInput input { background-color: #f7f7fb !important; border-radius: 12px !important; font-size: 18px !important; padding: 18px 10px !important; height: 45px !important; color: #0B0B19 !important; text-align: center !important; font-weight: 500 !important; border: 1px solid #ddd !important; width: 95% !important; box-sizing: border-box !important; }
        .stTextInput input:focus { border: 2px solid #6C13BF !important; outline: none !important; }
        div[data-testid="column"] { padding-left: 45px !important; padding-right: 45px !important; }
        .stButton button { width: 100%; background-color: #0B0B19; color: white; font-weight: 700; font-size: 18px; padding: 1em; border-radius: 10px; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

    cols_per_row = 4

    # === INPUTS HOMBRES (REFECTORIZADO) ===
    st.markdown("<div class='gender-title'>Hombres</div>", unsafe_allow_html=True)
    for i in range(0, n_hombres, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < n_hombres:
                player_key = f"hombre_{idx}"
                with col:
                    st.text_input(
                        f"Hombre {idx+1}",
                        value=st.session_state.hombres[idx],
                        key=player_key,
                        # Usar callback para actualizar la lista de hombres
                        on_change=update_player_name,
                        kwargs={
                            "gender": "hombres", 
                            "idx": idx, 
                            "key": player_key
                        }
                    )
                    # Eliminada la asignación directa

    # === INPUTS MUJERES (REFECTORIZADO) ===
    st.markdown("<div class='gender-title'>Mujeres</div>", unsafe_allow_html=True)
    for i in range(0, n_mujeres, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < n_mujeres:
                player_key = f"mujer_{idx}"
                with col:
                    st.text_input(
                        f"Mujer {idx+1}",
                        value=st.session_state.mujeres[idx],
                        key=player_key,
                        # Usar callback para actualizar la lista de mujeres
                        on_change=update_player_name,
                        kwargs={
                            "gender": "mujeres", 
                            "idx": idx, 
                            "key": player_key
                        }
                    )
                    # Eliminada la asignación directa

    # ===== VALIDACIONES ROBUSTAS =====
    # Normalizar y filtrar vacíos
    todos_raw = st.session_state.hombres + st.session_state.mujeres
    nombres_no_vacios = [p.strip() for p in todos_raw if p.strip() != ""]

    # Normalización para comparación (ignorar mayúsculas/acentos si se desea, aquí lowercase simple)
    nombres_norm = [p.lower() for p in nombres_no_vacios]

    # Detección de duplicados solo entre nombres no vacíos
    duplicados = len(nombres_norm) != len(set(nombres_norm))

    # Vacíos: si la cantidad de nombres no vacíos es menor que el total esperado
    total_esperado = n_hombres + n_mujeres
    vacios = len(nombres_no_vacios) < total_esperado

    # Mensajes
    if n_hombres != n_mujeres:
        st.warning("Para un americano mixto, debe haber el mismo número de hombres y mujeres.")

    if duplicados:
        st.error("Hay nombres repetidos.")
    elif vacios:
        st.warning("Todos los nombres deben estar completos.")

    continuar_disabled = (
        n_hombres == 0 or
        n_mujeres == 0 or
        n_hombres != n_mujeres or
        vacios or
        duplicados
    )

    st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Volver a Configuración"):
            st.session_state.page = "home"
            st.rerun()

    with col4:
        # Manejar la acción directamente al hacer click
        if st.button("Empezar Torneo 🔥", disabled=continuar_disabled):
            # doble comprobación antes de avanzar
            if not continuar_disabled:
                st.session_state.page = "torneo_mixto"
                st.rerun()