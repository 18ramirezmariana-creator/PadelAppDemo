import streamlit as st

# ============================================
# 🎨 TEMAS PREDEFINIDOS
# ============================================

DEMO_THEME = {
    # Colores principales
    'primary_color': '#6C13BF',
    'background_light': '#f7f7fb',
    'background_summary': '#f0e6ff',
    'text_dark': '#0B0B19',
    'text_light': '#ffffff',
    'border_color': '#ddd',

    # Colores específicos de torneo parejas
    'match_card_gradient_start': '#ffffff',
    'match_card_gradient_end': '#f0f0f5',
    'match_card_border_color': 'rgba(108, 19, 191, 0.1)',
    'match_card_shadow': 'rgba(0,0,0,0.15)',
    'number_input_bg': '#5E3187',
    'vs_color': '#6C13BF',
    
    # Tipografía - Tamaños
    'title_size': '36px',
    'subtitle_size': '32px',
    'category_title_size': '24px',
    'label_size': '24px',
    'input_size': '20px',
    'summary_size': '18px',
    'button_size': '18px',
    'match_title_size': '18px',
    'team_name_size': '16px',
    'vs_size': '20px',
    
    # Tipografía - Fuentes
    'font_title': 'inherit',
    'font_labels': 'inherit',
    'font_body': 'inherit',
    'font_inputs': 'inherit',
    'font_buttons': 'inherit',
    
    # Tipografía - Pesos
    'font_weight_title': '700',
    'font_weight_category_title': '700',
    'font_weight_labels': '700',
    'font_weight_body': '500',
    'font_weight_buttons': '700',
    'font_weight_match_title': '700',
    'font_weight_team_name': '600',
    'font_weight_vs': '800',
    'font_weight_number_input': '700',
    
    # Dimensiones
    'input_height': '52px',
    'input_width': '95%',
    'border_radius': '10px',
    'button_border_radius': '10px',
    'input_padding': '18px',
    'match_card_border_radius': '18px',
    'match_card_padding': '22px',
    
    # Espaciado
    'input_margin': '25px',
    'title_margin_bottom': '50px',
    'subtitle_margin_bottom': '40px',
    'category_title_margin_top': '30px',
    'category_title_margin_bottom': '10px',
    'summary_margin_top': '35px',
    'summary_margin_bottom': '25px',
    'column_padding_horizontal': '45px',
    'button_margin_top': '40px',
    'match_card_margin_bottom': '25px',
    'match_title_margin_bottom': '10px',
    'vs_margin_top': '8px',
    'vs_margin_bottom': '8px',
    
    # Bordes
    'input_border': '1px solid',
    'input_focus_border': '2px solid',
    'match_card_border': '1px solid',

    # Sombras
    'match_card_shadow_values': '0 8px 20px',

     # Nuevos parámetros para torneo sets
    'match_card_simple_border_radius': '15px',
    'match_card_simple_padding': '20px',
    'match_card_simple_shadow': '0 2px 6px rgba(0,0,0,0.07)',
    'number_input_border_radius': '8px',
    'number_input_hover_bg': '#6C13BF',
    'number_input_hover_color': '#00CED1',
    'final_match_bg': '#5E3187',
    'final_match_shadow': '0 5px 15px rgba(0,0,0,0.3)',
    'final_title_size': '24px',
    'final_team_name_size': '20px',
    'final_vs_size': '24px',
    'final_vs_color': '#00CED1',
    'final_vs_margin_top': '15px',
    'final_vs_margin_bottom': '15px',
    'font_weight_final_title': '700',
    'font_weight_final_team_name': '700',

    # Nuevos parámetros para torneo mixto
    'team_name_padding': '8px',
    'match_card_hover_translate': '-2px',
    'match_card_hover_shadow_values': '0 12px 28px',
    'match_card_hover_shadow': 'rgba(0,0,0,0.2)',
}

DARK_THEME = {
    'primary_color': '#00D9FF',
    'background_light': '#1E1E2E',
    'background_summary': '#252535',
    'text_dark': '#FFFFFF',
    'text_light': '#000000',
    'border_color': '#444',
    'title_size': '36px',
    'subtitle_size': '32px',
    'category_title_size': '24px',
    'label_size': '24px',
    'input_size': '20px',
    'summary_size': '18px',
    'button_size': '18px',
    'font_title': 'inherit',
    'font_labels': 'inherit',
    'font_body': 'inherit',
    'font_inputs': 'inherit',
    'font_buttons': 'inherit',
    'font_weight_title': '700',
    'font_weight_category_title': '700',
    'font_weight_labels': '700',
    'font_weight_body': '500',
    'font_weight_buttons': '700',
    'input_height': '52px',
    'input_width': '95%',
    'border_radius': '10px',
    'button_border_radius': '10px',
    'input_padding': '18px',
    'input_margin': '25px',
    'title_margin_bottom': '50px',
    'subtitle_margin_bottom': '40px',
    'category_title_margin_top': '30px',
    'category_title_margin_bottom': '10px',
    'summary_margin_top': '35px',
    'summary_margin_bottom': '25px',
    'column_padding_horizontal': '45px',
    'button_margin_top': '20px',
    'input_border': '1px solid',
    'input_focus_border': '2px solid',
}

CLUB_THEME = {
    # Colores principales
    'primary_color': '#002d4e',
    'background_light': '#f7f7fb',
    'background_summary': '#e0f9fc',
    'text_dark': '#0B0B19',
    'text_light': '#ffffff',
    'border_color': '#ddd',
    
    # Tipografía - Tamaños
    'title_size': '36px',
    'subtitle_size': '32px',
    'category_title_size': '24px',
    'label_size': '24px',
    'input_size': '20px',
    'summary_size': '18px',
    'button_size': '18px',
    
    # Tipografía - Fuentes
    'font_title': "'Anton', sans-serif",
    'font_labels': "'Antonio', sans-serif",
    'font_body': "'Antonio', sans-serif",
    'font_inputs': "'Antonio', sans-serif",
    'font_buttons': "'Antonio', sans-serif",
    
    # Tipografía - Pesos (Antonio tiene: 100-700)
    'font_weight_title': '400',
    'font_weight_category_title': '700',
    'font_weight_labels': '700',
    'font_weight_body': '400',
    'font_weight_buttons': '700',
    
    # Dimensiones
    'input_height': '52px',
    'input_width': '95%',
    'border_radius': '10px',
    'button_border_radius': '10px',
    'input_padding': '18px',
    
    # Espaciado
    'input_margin': '25px',
    'title_margin_bottom': '50px',
    'subtitle_margin_bottom': '40px',
    'category_title_margin_top': '30px',
    'category_title_margin_bottom': '10px',
    'summary_margin_top': '35px',
    'summary_margin_bottom': '25px',
    'column_padding_horizontal': '45px',
    'button_margin_top': '20px',
    
    # Bordes
    'input_border': '1px solid',
    'input_focus_border': '2px solid',

    # Sombras
    'match_card_shadow_values': '0 8px 20px',

    # Nuevos parámetros para torneo mixto
    'team_name_padding': '8px',
    'match_card_hover_translate': '-2px',
    'match_card_hover_shadow_values': '0 12px 28px',
    'match_card_hover_shadow': 'rgba(0,0,0,0.2)',
}

# Tema activo por defecto
DEFAULT_THEME = CLUB_THEME


def apply_custom_css_main(config=None):
    """
    Aplica los estilos CSS personalizados para la página principal.
    
    Args:
        config (dict, optional): Diccionario de configuración de estilos.
                                Si es None, usa DEFAULT_THEME.
    
    Example:
        >>> from assets.styles import apply_custom_css_main, DARK_THEME
        >>> apply_custom_css_main(DARK_THEME)
    """
    if config is None:
        config = DEFAULT_THEME
    
    # Determinar si necesitamos importar fuentes
    google_fonts_import = ""
    if "'Anton'" in config['font_title'] or "'Antonio'" in config['font_labels']:
        google_fonts_import = "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Antonio:wght@100;200;300;400;500;600;700&display=swap');"
    
    css = f"""
    <style>
        /* Importar fuentes si es necesario */
        {google_fonts_import}
        
        :root {{
            --primary-color: {config['primary_color']};
            --bg-light: {config['background_light']};
            --bg-summary: {config['background_summary']};
            --text-dark: {config['text_dark']};
            --text-light: {config['text_light']};
            --title-size: {config['title_size']};
            --label-size: {config['label_size']};
            --input-size: {config['input_size']};
            --summary-size: {config['summary_size']};
            --button-size: {config['button_size']};
            --font-title: {config['font_title']};
            --font-labels: {config['font_labels']};
            --font-body: {config['font_body']};
            --font-inputs: {config['font_inputs']};
            --font-buttons: {config['font_buttons']};
            --font-weight-title: {config['font_weight_title']};
            --font-weight-labels: {config['font_weight_labels']};
            --font-weight-body: {config['font_weight_body']};
            --font-weight-buttons: {config['font_weight_buttons']};
            --input-height: {config['input_height']};
            --border-radius: {config['border_radius']};
            --input-padding: {config['input_padding']};
            --input-margin: {config['input_margin']};
            --summary-margin-top: {config['summary_margin_top']};
            --summary-margin-bottom: {config['summary_margin_bottom']};
        }}

        .main-title {{
            text-align: center;
            font-size: var(--title-size);
            color: var(--primary-color);
            font-family: var(--font-title);
            font-weight: var(--font-weight-title);
            margin-bottom: {config['title_margin_bottom']};
        }}

        .stNumberInput {{
            margin-bottom: var(--input-margin) !important;
        }}

        .stNumberInput > div {{
            height: var(--input-height) !important;
            display: flex !important;
            align-items: center !important;
        }}

        .stNumberInput input {{
            height: var(--input-height) !important;
            min-height: var(--input-height) !important;
            max-height: var(--input-height) !important;
            width: 100% !important;
            padding: 0 var(--input-padding) !important;
            font-size: var(--input-size) !important;
            font-family: var(--font-inputs) !important;
            font-weight: var(--font-weight-body) !important;
            border-radius: var(--border-radius) !important;
            background-color: var(--bg-light) !important;
            line-height: var(--input-height) !important;
            box-sizing: border-box !important;
        }}

        .stNumberInput button {{
            height: var(--input-height) !important;
            min-height: var(--input-height) !important;
            max-height: var(--input-height) !important;
            color: var(--text-light) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        .stNumberInput > div > div {{
            height: var(--input-height) !important;
            display: flex !important;
            align-items: stretch !important;
        }}

        .stSelectbox {{
            margin-bottom: var(--input-margin) !important;
        }}

        div[data-baseweb="select"] {{
            height: var(--input-height) !important;
            min-height: var(--input-height) !important;
            max-height: var(--input-height) !important;
        }}

        div[data-baseweb="select"] > div {{
            height: var(--input-height) !important;
            min-height: var(--input-height) !important;
            max-height: var(--input-height) !important;
            padding: 0 var(--input-padding) !important;
            font-size: var(--input-size) !important;
            font-family: var(--font-inputs) !important;
            font-weight: var(--font-weight-body) !important;
            border-radius: var(--border-radius) !important;
            background-color: var(--bg-light) !important;
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }}

        label, .stSelectbox label, .stNumberInput label {{
            font-size: var(--label-size) !important;
            font-family: var(--font-labels) !important;
            font-weight: var(--font-weight-labels) !important;
            color: var(--text-dark) !important;
            margin-bottom: 6px !important;
        }}
        
        div[data-testid="stNumberInput"] label,
        div[data-testid="stSelectbox"] label {{
            font-family: var(--font-labels) !important;
            font-weight: var(--font-weight-labels) !important;
        }}

        .tournament-summary {{
            background-color: var(--bg-summary);
            border-left: 4px solid var(--primary-color);
            border-radius: var(--border-radius);
            padding: 20px 25px;
            margin: var(--summary-margin-top) 0 var(--summary-margin-bottom) 0;
        }}

        .summary-text {{
            color: var(--text-dark);
            font-size: var(--summary-size);
            font-family: var(--font-body);
            font-weight: var(--font-weight-body);
            line-height: 1.6;
            margin: 0;
        }}

        .summary-text strong {{
            color: var(--primary-color);
            font-weight: 700;
        }}

        .stButton button {{
            width: 100%;
            background-color: var(--text-dark);
            color: var(--text-light);
            font-family: var(--font-buttons);
            font-weight: var(--font-weight-buttons);
            font-size: var(--button-size);
            padding: 1em;
            border-radius: var(--border-radius);
            margin-top: {config['button_margin_top']};
        }}

        div[data-testid="column"] {{ 
            padding: 0 30px !important; 
        }} 
        
        section.main > div {{ 
            padding-top: 30px; 
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def apply_custom_css_player_setup(config=None):
    """
    Aplica los estilos CSS personalizados para la página de organización de jugadores.
    
    Args:
        config (dict, optional): Diccionario de configuración de estilos.
                                Si es None, usa DEFAULT_THEME.
    
    Example:
        >>> from assets.styles import apply_custom_css_player_setup, DARK_THEME
        >>> apply_custom_css_player_setup(DARK_THEME)
    """
    if config is None:
        config = DEFAULT_THEME
    
    # Determinar si necesitamos importar fuentes
    google_fonts_import = ""
    if "'Anton'" in config['font_title'] or "'Antonio'" in config['font_labels']:
        google_fonts_import = "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Antonio:wght@100;200;300;400;500;600;700&display=swap');"
    
    css = f"""
    <style>
        /* Importar fuentes si es necesario */
        {google_fonts_import}
        
        :root {{
            --primary-color: {config['primary_color']};
            --bg-light: {config['background_light']};
            --text-dark: {config['text_dark']};
            --text-light: {config['text_light']};
            --border-color: {config['border_color']};
            --subtitle-size: {config['subtitle_size']};
            --label-size: {config['label_size']};
            --input-size: {config['input_size']};
            --button-size: {config['button_size']};
            --font-title: {config['font_title']};
            --font-labels: {config['font_labels']};
            --font-body: {config['font_body']};
            --font-inputs: {config['font_inputs']};
            --font-buttons: {config['font_buttons']};
            --font-weight-title: {config['font_weight_title']};
            --font-weight-labels: {config['font_weight_labels']};
            --font-weight-body: {config['font_weight_body']};
            --font-weight-buttons: {config['font_weight_buttons']};
            --input-height: {config['input_height']};
            --input-width: {config['input_width']};
            --border-radius: {config['border_radius']};
            --button-border-radius: {config['button_border_radius']};
            --input-padding: {config['input_padding']};
            --subtitle-margin-bottom: {config['subtitle_margin_bottom']};
            --column-padding-horizontal: {config['column_padding_horizontal']};
            --button-margin-top: {config['button_margin_top']};
            --input-border: {config['input_border']};
            --input-focus-border: {config['input_focus_border']};
        }}

        .main-title {{
            text-align: center;
            font-size: var(--subtitle-size);
            color: var(--primary-color);
            font-family: var(--font-title);
            font-weight: var(--font-weight-title);
            margin-bottom: var(--subtitle-margin-bottom);
        }}

        .player-label {{
            font-weight: var(--font-weight-labels) !important;
            font-size: var(--label-size) !important;
            font-family: var(--font-labels) !important;
            color: var(--text-dark) !important;
        }}

        /* Input estilo tarjeta */
        .stTextInput input {{
            background-color: var(--bg-light) !important;
            border-radius: var(--border-radius) !important;
            font-size: var(--input-size) !important;
            font-family: var(--font-inputs) !important;
            padding: var(--input-padding) !important;
            height: var(--input-height) !important;
            color: var(--text-dark) !important;
            text-align: center !important;
            font-weight: var(--font-weight-body) !important;
            border: var(--input-border) var(--border-color) !important;
            width: var(--input-width) !important;
            box-sizing: border-box !important;
        }}

        .stTextInput input:focus {{
            border: var(--input-focus-border) var(--primary-color) !important;
            outline: none !important;
        }}

        /* Espaciado entre columnas */
        div[data-testid="column"] {{
            padding-left: var(--column-padding-horizontal) !important;
            padding-right: var(--column-padding-horizontal) !important;
        }}

        /* Botón principal */
        .stButton button {{
            width: 100%;
            background-color: var(--text-dark);
            color: var(--text-light);
            font-family: var(--font-buttons);
            font-weight: var(--font-weight-buttons);
            font-size: var(--button-size);
            padding: 1em;
            border-radius: var(--button-border-radius);
            margin-top: var(--button-margin-top);
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def apply_custom_css_setup_mixto(config=None):
    """
    Aplica los estilos CSS personalizados para la página de configuración de categorías.
    
    Args:
        config (dict, optional): Diccionario de configuración de estilos.
                                Si es None, usa DEFAULT_THEME.
    
    Example:
        >>> from assets.styles import apply_custom_css_category_setup, DARK_THEME
        >>> apply_custom_css_category_setup(DARK_THEME)
    """
    if config is None:
        config = DEFAULT_THEME
    
    # Determinar si necesitamos importar fuentes
    google_fonts_import = ""
    if "'Anton'" in config['font_title'] or "'Antonio'" in config['font_labels']:
        google_fonts_import = "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Antonio:wght@100;200;300;400;500;600;700&display=swap');"
    
    css = f"""
    <style>
        /* Importar fuentes si es necesario */
        {google_fonts_import}
        
        :root {{
            --primary-color: {config['primary_color']};
            --bg-light: {config['background_light']};
            --text-dark: {config['text_dark']};
            --text-light: {config['text_light']};
            --border-color: {config['border_color']};
            --subtitle-size: {config['subtitle_size']};
            --category-title-size: {config['category_title_size']};
            --input-size: {config['input_size']};
            --button-size: {config['button_size']};
            --font-title: {config['font_title']};
            --font-labels: {config['font_labels']};
            --font-body: {config['font_body']};
            --font-inputs: {config['font_inputs']};
            --font-buttons: {config['font_buttons']};
            --font-weight-title: {config['font_weight_title']};
            --font-weight-category-title: {config['font_weight_category_title']};
            --font-weight-body: {config['font_weight_body']};
            --font-weight-buttons: {config['font_weight_buttons']};
            --input-height: {config['input_height']};
            --input-width: {config['input_width']};
            --border-radius: {config['border_radius']};
            --button-border-radius: {config['button_border_radius']};
            --input-padding: {config['input_padding']};
            --subtitle-margin-bottom: {config['subtitle_margin_bottom']};
            --category-title-margin-top: {config['category_title_margin_top']};
            --category-title-margin-bottom: {config['category_title_margin_bottom']};
            --column-padding-horizontal: {config['column_padding_horizontal']};
            --button-margin-top: {config['button_margin_top']};
            --input-border: {config['input_border']};
            --input-focus-border: {config['input_focus_border']};
        }}

        .main-title {{
            text-align: center;
            font-size: var(--subtitle-size);
            color: var(--primary-color);
            font-family: var(--font-title);
            font-weight: var(--font-weight-title);
            margin-bottom: var(--subtitle-margin-bottom);
        }}

        .gender-title {{
            font-size: var(--category-title-size);
            font-weight: var(--font-weight-category-title);
            font-family: var(--font-labels);
            margin-top: var(--category-title-margin-top);
            margin-bottom: var(--category-title-margin-bottom);
            color: var(--text-dark);
        }}

        /* Input estilo tarjeta */
        .stTextInput input {{
            background-color: var(--bg-light) !important;
            border-radius: var(--border-radius) !important;
            font-size: var(--input-size) !important;
            font-family: var(--font-inputs) !important;
            padding: var(--input-padding) !important;
            height: var(--input-height) !important;
            color: var(--text-dark) !important;
            text-align: center !important;
            font-weight: var(--font-weight-body) !important;
            border: var(--input-border) var(--border-color) !important;
            width: var(--input-width) !important;
            box-sizing: border-box !important;
        }}

        .stTextInput input:focus {{
            border: var(--input-focus-border) var(--primary-color) !important;
            outline: none !important;
        }}

        /* Espaciado entre columnas */
        div[data-testid="column"] {{
            padding-left: var(--column-padding-horizontal) !important;
            padding-right: var(--column-padding-horizontal) !important;
        }}

        /* Botón principal */
        .stButton button {{
            width: 100%;
            background-color: var(--text-dark);
            color: var(--text-light);
            font-family: var(--font-buttons);
            font-weight: var(--font-weight-buttons);
            font-size: var(--button-size);
            padding: 1em;
            border-radius: var(--button-border-radius);
            margin-top: var(--button-margin-top);
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def apply_custom_css_torneo(config=None):
    """
    Aplica los estilos CSS personalizados para la página de torneo de parejas.
    
    Args:
        config (dict, optional): Diccionario de configuración de estilos.
                                Si es None, usa DEFAULT_THEME.
    
    Example:
        >>> from assets.styles import apply_custom_css_torneo_parejas, DEMO_THEME
        >>> apply_custom_css_torneo_parejas(DEMO_THEME)
    """
    if config is None:
        config = DEFAULT_THEME
    
    # Determinar si necesitamos importar fuentes
    google_fonts_import = ""
    if "'Anton'" in config['font_title'] or "'Antonio'" in config['font_labels']:
        google_fonts_import = "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Antonio:wght@100;200;300;400;500;600;700&display=swap');"
    
    css = f"""
    <style>
        /* Importar fuentes si es necesario */
        {google_fonts_import}
        
        .main-title {{
            text-align: center;
            font-size: {config['subtitle_size']};
            color: {config['primary_color']};
            font-weight: {config['font_weight_title']};
            margin-bottom: {config['subtitle_margin_bottom']};
        }}
        
        .match-card {{
            background: linear-gradient(145deg, {config['match_card_gradient_start']}, {config['match_card_gradient_end']});
            border-radius: {config['match_card_border_radius']};
            padding: {config['match_card_padding']};
            margin-bottom: {config['match_card_margin_bottom']};
            box-shadow: {config['match_card_shadow_values']} {config['match_card_shadow']};
            border: {config['match_card_border']} {config['match_card_border_color']};
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        
        .match-title {{
            font-weight: {config['font_weight_match_title']};
            font-size: {config['match_title_size']};
            color: {config['text_dark']};
            margin-bottom: {config['match_title_margin_bottom']};
        }}
        
        .team-name {{
            font-weight: {config['font_weight_team_name']};
            color: {config['text_dark']};
            font-size: {config['team_name_size']};
            text-align: center;
        }}
        
        .vs {{
            font-weight: {config['font_weight_vs']};
            font-size: {config['vs_size']};
            color: {config['vs_color']};
            text-align: center;
            margin-top: {config['vs_margin_top']};
            margin-bottom: {config['vs_margin_bottom']};
        }}
        
        .stNumberInput input {{
            background-color: {config['number_input_bg']} !important;
            color: {config['text_light']} !important;
            font-weight: {config['font_weight_number_input']} !important;
        }}
                
        .stNumberInput button {{
            color: {config['text_light']} !important;
        }}
        
        /* === BOTÓN === */
        .stButton button {{
            width: 100%;
            background-color: {config['text_dark']};
            color: {config['text_light']};
            font-weight: {config['font_weight_buttons']};
            font-size: {config['button_size']};
            padding: 1em;
            border-radius: {config['button_border_radius']};
            margin-top: {config['button_margin_top']};
        }}
        /* Ensure button container also takes full width */
        .stButton {{
            width: 100%;
        }}

        /* For buttons inside columns */
        div[data-testid="column"] .stButton {{
            width: 100%;
        }}

        div[data-testid="column"] .stButton button {{
            width: 100%;
        }}
        
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def apply_custom_css_torneo_mixto(config=None):
    """
    Aplica los estilos CSS personalizados para la página de torneo mixto.
    
    Args:
        config (dict, optional): Diccionario de configuración de estilos.
                                Si es None, usa DEFAULT_THEME.
    
    Example:
        >>> from assets.styles import apply_custom_css_torneo_mixto, DEMO_THEME
        >>> apply_custom_css_torneo_mixto(DEMO_THEME)
    """
    if config is None:
        config = DEFAULT_THEME
    
    # Determinar si necesitamos importar fuentes
    google_fonts_import = ""
    if "'Anton'" in config['font_title'] or "'Antonio'" in config['font_labels']:
        google_fonts_import = "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Antonio:wght@100;200;300;400;500;600;700&display=swap');"
    
    css = f"""
    <style>
        /* Importar fuentes si es necesario */
        {google_fonts_import}
        
        .main-title {{
            text-align: center;
            font-size: {config['subtitle_size']};
            color: {config['primary_color']};
            font-weight: {config['font_weight_title']};
            margin-bottom: {config['subtitle_margin_bottom']};
        }}
        
        .match-card {{
            background: linear-gradient(145deg, {config['match_card_gradient_start']}, {config['match_card_gradient_end']});
            border-radius: {config['match_card_border_radius']};
            padding: {config['match_card_padding']};
            margin-bottom: {config['match_card_margin_bottom']};
            box-shadow: {config['match_card_shadow_values']} {config['match_card_shadow']};
            border: {config['match_card_border']} {config['match_card_border_color']};
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        
        .match-card:hover {{
            transform: translateY({config['match_card_hover_translate']});
            box-shadow: {config['match_card_hover_shadow_values']} {config['match_card_hover_shadow']};
        }}
        
        .match-title {{
            font-weight: {config['font_weight_match_title']};
            font-size: {config['match_title_size']};
            color: {config['text_dark']};
            margin-bottom: {config['match_title_margin_bottom']};
            text-align: center;
        }}
        
        .team-name {{
            font-weight: {config['font_weight_team_name']};
            color: {config['text_dark']};
            font-size: {config['team_name_size']};
            text-align: center;
            padding: {config['team_name_padding']};
        }}
        
        .vs {{
            font-weight: {config['font_weight_vs']};
            font-size: {config['vs_size']};
            color: {config['vs_color']};
            text-align: center;
            margin-top: {config['vs_margin_top']};
            margin-bottom: {config['vs_margin_bottom']};
        }}
        
        .stNumberInput input {{
            background-color: {config['number_input_bg']} !important;
            color: {config['text_light']} !important;
            font-weight: {config['font_weight_number_input']} !important;
        }}
        
        .stNumberInput button {{
            color: {config['text_light']} !important;
        }}
        
        .stButton button {{
            width: 100%;
            background-color: {config['text_dark']};
            color: {config['text_light']};
            font-weight: {config['font_weight_buttons']};
            font-size: {config['button_size']};
            padding: 1em;
            border-radius: {config['button_border_radius']};
            margin-top: 20px;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def apply_custom_css_torneo_sets(config=None):
    """
    Aplica los estilos CSS personalizados para la página de torneo por sets.
    
    Args:
        config (dict, optional): Diccionario de configuración de estilos.
                                Si es None, usa DEFAULT_THEME.
    
    Example:
        >>> from assets.styles import apply_custom_css_torneo_sets, DEMO_THEME
        >>> apply_custom_css_torneo_sets(DEMO_THEME)
    """
    if config is None:
        config = DEFAULT_THEME
    
    # Determinar si necesitamos importar fuentes
    google_fonts_import = ""
    if "'Anton'" in config['font_title'] or "'Antonio'" in config['font_labels']:
        google_fonts_import = "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Antonio:wght@100;200;300;400;500;600;700&display=swap');"
    
    css = f"""
    <style>
        /* Importar fuentes si es necesario */
        {google_fonts_import}
        
        .main-title {{
            text-align: center;
            font-size: {config['subtitle_size']};
            color: {config['primary_color']};
            font-weight: {config['font_weight_title']};
            margin-bottom: {config['subtitle_margin_bottom']};
        }}
        
        .match-card {{
            background-color: {config['background_light']};
            border-radius: {config['match_card_simple_border_radius']};
            padding: {config['match_card_simple_padding']};
            margin-bottom: {config['match_card_margin_bottom']};
            box-shadow: {config['match_card_simple_shadow']};
        }}

        .stNumberInput input {{
            background-color: {config['number_input_bg']} !important;
            color: {config['text_light']} !important;
            font-weight: {config['font_weight_number_input']} !important;
            border-radius: {config['number_input_border_radius']} !important;
            border: none !important;
        }}

        .stNumberInput button {{
            background-color: {config['number_input_bg']} !important;
            color: {config['text_light']} !important;
            border: none !important;
        }}

        .stNumberInput button:hover {{
            background-color: {config['number_input_hover_bg']} !important;
            color: {config['number_input_hover_color']} !important;
        }}

        .final-match-card {{
            background-color: {config['final_match_bg']};
            color: {config['text_light']};
            border-radius: {config['match_card_simple_border_radius']};
            padding: {config['match_card_simple_padding']};
            margin-bottom: {config['match_card_margin_bottom']};
            box-shadow: {config['final_match_shadow']};
        }}
        
        .match-title {{
            font-weight: {config['font_weight_match_title']};
            font-size: {config['match_title_size']};
            color: {config['text_dark']};
            margin-bottom: {config['match_title_margin_bottom']};
        }}
        
        .final-title {{
            font-weight: {config['font_weight_final_title']};
            font-size: {config['final_title_size']};
            color: {config['text_light']};
            margin-bottom: {config['match_title_margin_bottom']};
            text-align: center;
        }}
        
        .team-name {{
            font-weight: {config['font_weight_team_name']};
            color: {config['text_dark']};
            font-size: {config['team_name_size']};
            text-align: center;
        }}
        
        .final-team-name {{
            font-weight: {config['font_weight_final_team_name']};
            color: {config['text_light']};
            font-size: {config['final_team_name_size']};
            text-align: center;
        }}
        
        .vs {{
            font-weight: {config['font_weight_vs']};
            font-size: {config['vs_size']};
            color: {config['vs_color']};
            text-align: center;
            margin-top: {config['vs_margin_top']};
            margin-bottom: {config['vs_margin_bottom']};
        }}
        
        .final-vs {{
            font-weight: {config['font_weight_vs']};
            font-size: {config['final_vs_size']};
            color: {config['final_vs_color']};
            text-align: center;
            margin-top: {config['final_vs_margin_top']};
            margin-bottom: {config['final_vs_margin_bottom']};
        }}
        
        div[data-testid="stForm"] div.stNumberInput input {{
            text-align: center;
            font-weight: {config['font_weight_number_input']};
        }}
        
        .stButton button {{
            width: 100%;
            background-color: {config['text_dark']};
            color: {config['text_light']};
            font-weight: {config['font_weight_buttons']};
            font-size: {config['button_size']};
            padding: 1em;
            border-radius: {config['button_border_radius']};
            margin-top: {config['button_margin_top']};
        }}

        /* Ensure button container also takes full width */
        .stButton {{
            width: 100%;
        }}

        /* For buttons inside columns */
        div[data-testid="column"] .stButton {{
            width: 100%;
        }}

        div[data-testid="column"] .stButton button {{
            width: 100%;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# components/ranking_display.py
import streamlit as st
import pandas as pd

def display_ranking_table(ranking_df, ranking_type='individual'):
    """
    Muestra una tabla de ranking estilizada.
    
    Args:
        ranking_df (pd.DataFrame): DataFrame con el ranking
        ranking_type (str): 'individual' o 'parejas' para determinar la columna de nombre
    """
    # Determinar la columna de nombre según el tipo
    name_col = 'Jugador' if ranking_type == 'individual' else 'Pareja'
    points_col = 'Puntos'
    
    # Verificar que las columnas existan
    if name_col not in ranking_df.columns or points_col not in ranking_df.columns:
        st.error(f"El DataFrame debe contener las columnas '{name_col}' y '{points_col}'")
        return
    
    # Generar las filas HTML
    rows_html = ""
    for idx, row in ranking_df.iterrows():
        position = idx + 1
        name = row[name_col]
        points = row[points_col]
        
        # Agregar medalla para top 3
        if position == 1:
            position_display = '<span class="rank-medal">🥇</span>'
        elif position == 2:
            position_display = '<span class="rank-medal">🥈</span>'
        elif position == 3:
            position_display = '<span class="rank-medal">🥉</span>'
        else:
            position_display = str(position)
        
        rows_html += f"""
        <div class="ranking-row">
            <div class="rank-position">{position_display}</div>
            <div class="player-name">{name}</div>
            <div class="player-points">{points}</div>
        </div>
        """
    
    # Renderizar la tabla completa
    st.markdown(f"""
        <style>
            .ranking-table {{
                width: 100%;
                max-width: 400px;
                margin: 0 auto 40px auto;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            
            .ranking-header {{
                background: linear-gradient(145deg, #6C13BF, #5E3187);
                color: white;
                padding: 15px;
                display: grid;
                grid-template-columns: 60px 1fr 80px;
                font-weight: 700;
                font-size: 16px;
            }}
            
            .ranking-row {{
                background-color: white;
                padding: 12px 15px;
                display: grid;
                grid-template-columns: 60px 1fr 80px;
                align-items: center;
                border-bottom: 1px solid #f0f0f0;
                transition: background-color 0.2s ease;
            }}
            
            .ranking-row:hover {{
                background-color: #f7f7fb;
            }}
            
            .ranking-row:last-child {{
                border-bottom: none;
            }}
            
            .rank-position {{
                font-weight: 700;
                color: #6C13BF;
                font-size: 18px;
            }}
            
            .player-name {{
                font-weight: 600;
                color: #0B0B19;
                font-size: 16px;
            }}
            
            .player-points {{
                text-align: right;
                font-weight: 700;
                color: #5E3187;
                font-size: 16px;
            }}
            
            .rank-medal {{
                font-size: 24px;
            }}
        </style>
        
        <div class="ranking-table">
            <div class="ranking-header">
                <div>Pos.</div>
                <div>{name_col}</div>
                <div style="text-align: right;">Puntos</div>
            </div>
            {rows_html}
        </div>
    """, unsafe_allow_html=True)