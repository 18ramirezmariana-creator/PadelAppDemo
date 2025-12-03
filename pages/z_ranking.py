import streamlit as st
import pandas as pd
from assets.show_rankings import define_ranking_items


def app():
    
    rank = st.session_state.ranking
    # Convert to DataFrame
    df = rank.copy()
    # Display header

    # --- Estilos Podio ---
    col2, col1, col3 = st.columns([1, 1, 1])
    define_ranking_items(df,col1,col2,col3)
    

    col2, col1, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("Volver"):
            if ("mixto_op" in st.session_state) and (st.session_state.mixto_op == "Siempre Mixto"):
                st.session_state.page = "torneo_mixto"
            elif ("num_sets" in st.session_state) and (st.session_state.mod == 'Parejas Fijas'):
                st.session_state.page = "torneo_sets"
            else:
                st.session_state.page = "torneo"
            st.rerun()
    with col4:
        if st.button("Empezar Nuevo Torneo"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "home"
            st.rerun()
