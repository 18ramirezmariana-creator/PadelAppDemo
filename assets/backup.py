import json
from streamlit_js_eval import streamlit_js_eval
import time

def save_to_localstorage(data):
    """Save tournament data to browser localStorage"""
    try:
        json_data = json.dumps(data)
        # Use base64 encoding to avoid escaping issues
        import base64
        encoded_data = base64.b64encode(json_data.encode()).decode()
        
        js_code = f"""
        try {{
            localStorage.setItem('padel_tournament', atob('{encoded_data}'));
            console.log('Tournament saved to localStorage');
        }} catch(e) {{
            console.error('Save error:', e);
        }}
        true;
        """
        # Use timestamp as key to avoid conflicts
        streamlit_js_eval(js_code, key=f"save_{int(time.time() * 1000)}")
        return True
    except Exception as e:
        print(f"Error saving to localStorage: {e}")
        return False

def load_from_localstorage():
    """Load tournament data from browser localStorage"""
    try:
        js_code = """
        try {
            const data = localStorage.getItem('padel_tournament');
            if (data) {
                console.log('Tournament loaded from localStorage');
            }
            data;
        } catch(e) {
            console.error('Load error:', e);
            null;
        }
        """
        # Use timestamp to force fresh evaluation
        result = streamlit_js_eval(js_code, key=f"load_{int(time.time() * 1000)}")
        
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
        try {
            localStorage.removeItem('padel_tournament');
            console.log('Tournament cleared from localStorage');
        } catch(e) {
            console.error('Clear error:', e);
        }
        true;
        """
        streamlit_js_eval(js_code, key=f"clear_{int(time.time() * 1000)}")
        return True
    except Exception as e:
        print(f"Error clearing localStorage: {e}")
        return False