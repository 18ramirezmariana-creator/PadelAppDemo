import streamlit as st
import streamlit.components.v1 as components
import json

def save_to_localstorage(data):
    """
    Dual save: 
    1. session_state (primario - sobrevive mientras la pestaña esté abierta)
    2. localStorage (backup - sobrevive cierre de app en iPad)
    """
    try:
        # 1. Guardar en session_state (SIEMPRE funciona)
        st.session_state._tournament_data = data
        
        # 2. Intentar guardar en localStorage (backup para iPad)
        json_str = json.dumps(data, ensure_ascii=False)
        # Escapar para JavaScript
        json_escaped = json_str.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', ' ')
        
        save_html = f"""
        <script>
        try {{
            localStorage.setItem('padel_tournament', '{json_escaped}');
            console.log('✅ Saved to localStorage');
        }} catch(e) {{
            console.error('localStorage save failed:', e);
        }}
        </script>
        """
        
        components.html(save_html, height=0, key=f"save_{hash(json_str)}")
        return True
        
    except Exception as e:
        print(f"Save error: {e}")
        return False

def load_from_localstorage():
    """
    Cargar desde session_state (que es donde realmente se guarda)
    """
    return st.session_state.get('_tournament_data', None)

def clear_localstorage():
    """Clear both session and localStorage"""
    try:
        # Limpiar session_state
        if '_tournament_data' in st.session_state:
            del st.session_state._tournament_data
        
        # Limpiar localStorage
        clear_html = """
        <script>
        try {
            localStorage.removeItem('padel_tournament');
            console.log('✅ Cleared localStorage');
        } catch(e) {
            console.error('localStorage clear failed:', e);
        }
        </script>
        """
        components.html(clear_html, height=0, key="clear_storage")
        return True
        
    except Exception as e:
        print(f"Clear error: {e}")
        return False