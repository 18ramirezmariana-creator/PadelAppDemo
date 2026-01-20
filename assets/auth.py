import streamlit as st
import bcrypt

def check_login():
    if st.session_state.get("authenticated"):
        return True

    st.title("Acceso restringido")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        users = st.secrets["auth"]["users"]

        if username in users:
            stored_hash = users[username].encode()
            if bcrypt.checkpw(password.encode(), stored_hash):
                st.session_state.authenticated = True
                st.session_state.user = username
                st.rerun()

        st.error("Credenciales incorrectas")

    return False
