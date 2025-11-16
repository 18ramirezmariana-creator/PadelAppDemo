import streamlit as st
import pandas as pd

def app():

    # VALIDACIÓN 1: La clave debe existir
    if "ranking" not in st.session_state:
        st.warning("Todavía no hay un ranking generado. Regresa al torneo para finalizar los partidos.")
        if st.button("Volver al Torneo"):
            st.session_state.page = "torneo"
            st.rerun()
        return

    # Recuperar
    ranking_data = st.session_state.get("ranking", None)

    # VALIDACIÓN 2: Debe ser DataFrame válido
    if ranking_data is None or not isinstance(ranking_data, pd.DataFrame) or ranking_data.empty:
        st.warning("El ranking está vacío o tiene un formato inválido.")
        if st.button("Volver al Torneo"):
            st.session_state.page = "torneo"
            st.rerun()
        return

    df = ranking_data.copy()

    # --- Estilos Podio ---
    col2, col1, col3 = st.columns([1, 1, 1])

    def podium_card(place, player, points, gradient, height):
        st.markdown(f"""
            <div style="
                background: {gradient};
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                color: white;
                box-shadow: inset 0 1px 4px rgba(255,255,255,0.4),
                            inset 0 -1px 4px rgba(0,0,0,0.3),
                            0 6px 12px rgba(0,0,0,0.3);
                height: {height}px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                border: 1px solid rgba(255,255,255,0.2);
            ">
                <div style="font-size: 14px; background-color: rgba(255,255,255,0.2);
                            padding: 5px 15px; border-radius: 10px; display: inline-block;">
                    {place}
                </div>
                <h2 style="margin-top: 15px; margin-bottom: 10px;">{player}</h2>
                <p style="font-size:16px;">{points} Puntos</p>
            </div>
        """, unsafe_allow_html=True)

    # Gradientes
    gold_gradient = "linear-gradient(145deg, #FFD700, #E6C200, #FFF6A0)"
    silver_gradient = "linear-gradient(145deg, #C0C0C0, #A9A9A9, #E0E0E0)"
    bronze_gradient = "linear-gradient(145deg, #FFA347, #FF7A00, #FFD08A)"

    # Top 3
    top3 = df.head(3)

    with col1:
        podium_card("🥇 1er Puesto", top3.iloc[0]["Jugador"], top3.iloc[0]["Puntos"], gold_gradient, 300)
    with col2:
        podium_card("🥈 2do Puesto", top3.iloc[1]["Jugador"], top3.iloc[1]["Puntos"], silver_gradient, 260)
    with col3:
        podium_card("🥉 3er Puesto", top3.iloc[2]["Jugador"], top3.iloc[2]["Puntos"], bronze_gradient, 230)

    # Otros participantes
    others = df.iloc[3:]
    if not others.empty:
        st.markdown("""
            <div style="text-align:center; margin-top:60px;">
                <h4 style="font-weight:400;"> Otros Participantes</h4>
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
        """, unsafe_allow_html=True)

        for idx, row in others.iterrows():
            st.markdown(f"""
                <div style="background-color:white;
                            width:60%;
                            max-width:600px;
                            border-radius:15px;
                            margin:10px auto;
                            padding:10px 20px;
                            box-shadow:0 2px 6px rgba(0,0,0,0.1);
                            display:flex;
                            justify-content:space-between;
                            align-items:center;">
                    <span style="font-weight:600; color:#5E3187;">{idx+1}ᵗʰ — {row['Jugador']}</span>
                    <span style="font-weight:500; color:#333;">{row['Puntos']} pts</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # Botones
    col2, col1, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("Volver"):
            st.session_state.page = "torneo"
            st.rerun()
    with col4:
        if st.button("Empezar Nuevo Torneo"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "home"
            st.rerun()
