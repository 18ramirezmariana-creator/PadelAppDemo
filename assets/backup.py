from streamlit_javascript import st_javascript
import json

STORAGE_KEY = "americano_tournament_data"

def save_to_localstorage(data):
    """Save tournament data to browser localStorage"""
    try:
        json_data = json.dumps(data)
        # Escape single quotes to avoid JavaScript errors
        json_data_escaped = json_data.replace("'", "\\'").replace('"', '\\"')
        
        js_code = f"""
        localStorage.setItem('{STORAGE_KEY}', '{json_data_escaped}');
        """
        st_javascript(js_code)
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
        result = st_javascript(js_code)
        
        if result and result != "null":
            return json.loads(result)
        return None
    except Exception as e:
        print(f"Error loading from localStorage: {e}")
        return None

def clear_localstorage():
    """Clear tournament data from localStorage"""
    js_code = f"""
    localStorage.removeItem('{STORAGE_KEY}');
    """
    st_javascript(js_code)