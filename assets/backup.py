import streamlit as st
import streamlit.components.v1 as components
import json
from streamlit_javascript import st_javascript  # <--- Necesitas esta librería

def save_to_localstorage(data):
    """Guarda en session_state y en el localStorage del navegador"""
    try:
        st.session_state._tournament_data = data
        json_str = json.dumps(data, ensure_ascii=False)
        json_escaped = json_str.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', ' ')
        
        # Guardar en el navegador (JS)
        save_html = f"""
        <script>
            localStorage.setItem('padel_tournament', '{json_escaped}');
        </script>
        """
        components.html(save_html, height=0)
        return True
    except Exception as e:
        return False

def load_from_browser():
    """
    LEE REALMENTE DEL NAVEGADOR.
    Esta función es la que salva el torneo tras la caída de internet.
    """
    # Ejecutamos JS para obtener el valor
    data_js = st_javascript("localStorage.getItem('padel_tournament');")
    
    if data_js and isinstance(data_js, str):
        try:
            return json.loads(data_js)
        except:
            return None
    return None

def load_from_localstorage():
    """Mantiene compatibilidad con tu código actual de sesión"""
    return st.session_state.get('_tournament_data', None)

def clear_localstorage():
    """Limpia ambos"""
    if '_tournament_data' in st.session_state:
        del st.session_state._tournament_data
    
    clear_html = """<script>localStorage.removeItem('padel_tournament');</script>"""
    components.html(clear_html, height=0)