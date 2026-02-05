from streamlit_javascript import st_javascript
import json
import time

STORAGE_KEY = "americano_tournament_data"

def save_to_localstorage(data):
    """Save tournament data to browser localStorage"""
    try:
        json_data = json.dumps(data)
        # Escape single quotes to avoid JavaScript errors
        json_data_escaped = json_data.replace("'", "\\'").replace('"', '\\"')

         # 🔥 Agregar key única basada en timestamp
        unique_key = f"save_{int(time.time() * 1000000)}"
        
        js_code = f"""
        localStorage.setItem('{STORAGE_KEY}', '{json_data_escaped}');
        """
        st_javascript(js_code, key=unique_key)
        return True
    except Exception as e:
        print(f"Error saving to localStorage: {e}")
        return False

def load_from_localstorage():
    """Load tournament data from browser localStorage"""
    try:
        unique_key = f"load_{int(time.time() * 1000000)}"
        js_code = f"""
        localStorage.getItem('{STORAGE_KEY}');
        """
        result = st_javascript(js_code, key=unique_key)
        
        if result and result != "null" and result != "undefined":
            return json.loads(result)
        return None
    except Exception as e:
        print(f"Error loading from localStorage: {e}")
        return None

def clear_localstorage():
    """Clear tournament data from localStorage"""
    try:
        # 🔥 Agregar key única basada en timestamp
        unique_key = f"clear_{int(time.time() * 1000000)}"
        
        js_code = f"""
        localStorage.removeItem('{STORAGE_KEY}');
        return true;
        """
        st_javascript(js_code, key=unique_key)
    except Exception as e:
        print(f"Error clearing localStorage: {e}")