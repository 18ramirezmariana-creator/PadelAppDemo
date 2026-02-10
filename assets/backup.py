import json
from streamlit_js_eval import streamlit_js_eval

def save_to_localstorage(data):
    """Save tournament data to browser localStorage"""
    try:
        json_data = json.dumps(data)
        # Escape quotes for JavaScript
        escaped_data = json_data.replace("'", "\\'").replace('"', '\\"')
        
        js_code = f"""
        localStorage.setItem('padel_tournament', '{escaped_data}');
        console.log('Tournament saved to localStorage');
        true;
        """
        streamlit_js_eval(js_code, key=f"save_{hash(json_data)}")
        return True
    except Exception as e:
        print(f"Error saving to localStorage: {e}")
        return False

def load_from_localstorage():
    """Load tournament data from browser localStorage"""
    try:
        js_code = """
        const data = localStorage.getItem('padel_tournament');
        data;
        """
        result = streamlit_js_eval(js_code, key="load_tournament")
        
        if result:
            return json.loads(result)
        return None
    except Exception as e:
        print(f"Error loading from localStorage: {e}")
        return None

def clear_localstorage():
    """Clear tournament data from browser localStorage"""
    try:
        js_code = """
        localStorage.removeItem('padel_tournament');
        console.log('Tournament cleared from localStorage');
        true;
        """
        streamlit_js_eval(js_code, key="clear_tournament")
        return True
    except Exception as e:
        print(f"Error clearing localStorage: {e}")
        return False