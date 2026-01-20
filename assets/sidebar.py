import streamlit as st
from PIL import Image

def sidebar_style():

    sidebar_bg = """
    <style>
        /* Target all sidebar titles with class starting with e1dbuyne */
        [class^="st-emotion-cache"][class*="e1dbuyne"] {
            color: #5E3187;
            font-weight: bold;
            font-size: 20px;
        }
        </style>
    """

    logo = Image.open("assets/logo_demo.jpg")
    watermark = Image.open("assets/watermark_padel_lab.png")
    st.markdown(sidebar_bg, unsafe_allow_html=True)
    with st.sidebar:
        st.image(logo)
        st.image(watermark)
        if st.button("Cerrar sesión"):
            st.session_state.clear()
            st.rerun()