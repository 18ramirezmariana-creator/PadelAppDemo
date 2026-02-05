from streamlit_javascript import st_javascript
import json
import hashlib

STORAGE_KEY = "americano_tournament_data"
HAS_SAVED_FLAG_KEY = "americano_has_saved_flag"  # 🔥 NUEVO

def _generate_key(operation):
    """Genera una key única para evitar colisiones"""
    import random
    seed = f"{operation}_{random.random()}"
    return hashlib.md5(seed.encode()).hexdigest()[:8]

def save_to_localstorage(data):
    """Save tournament data to browser localStorage"""
    try:
        json_data = json.dumps(data)
        json_data_escaped = json_data.replace('\\', '\\\\').replace("'", "\\'")
        
        js_code = f"""
        localStorage.setItem('{STORAGE_KEY}', '{json_data_escaped}');
        localStorage.setItem('{HAS_SAVED_FLAG_KEY}', 'true');
        return true;
        """
        st_javascript(js_code, key=f"save_{_generate_key('save')}")
        return True
    except Exception as e:
        print(f"Error saving to localStorage: {e}")
        return False

def load_from_localstorage():
    """Load tournament data from browser localStorage"""
    try:
        js_code = f"""
        localStorage.getItem('{STORAGE_KEY}');
        """
        result = st_javascript(js_code, key=f"load_{_generate_key('load')}")
        
        if result and result != "null" and result != "undefined":
            return json.loads(result)
        return None
    except Exception as e:
        print(f"Error loading from localStorage: {e}")
        return None

def has_saved_tournament():
    """Check if there's a saved tournament (faster than loading all data)"""
    try:
        js_code = f"""
        localStorage.getItem('{HAS_SAVED_FLAG_KEY}');
        """
        result = st_javascript(js_code, key=f"check_{_generate_key('check')}")
        return result == 'true'
    except Exception as e:
        print(f"Error checking localStorage: {e}")
        return False

def clear_localstorage():
    """Clear tournament data from localStorage"""
    try:
        js_code = f"""
        localStorage.removeItem('{STORAGE_KEY}');
        localStorage.removeItem('{HAS_SAVED_FLAG_KEY}');
        return true;
        """
        st_javascript(js_code, key=f"clear_{_generate_key('clear')}")
        return True
    except Exception as e:
        print(f"Error clearing localStorage: {e}")
        return False