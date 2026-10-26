# ==============================================================================
# Cinematch - Portal de Clasificación Cinematográfica (UI Premium)
# Ubicación: frontend/app.py
# ==============================================================================

import os
import joblib
import pandas as pd
import streamlit as st

# 1. Configuración del Portal Web
st.set_page_config(
    page_title="Cinematch | Clasificación Cinematográfica",
    page_icon="🍿",
    layout="centered"
)

# 2. Estilos CSS Personalizados (Fondo Oscuro Degradado e Ícono Gigante)
custom_styles = '''
    <style>
    /* Ocultar elementos nativos del entorno */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Fondo degradado oscuro estilo cine */
    .stApp {
        background: linear-gradient(135deg, #0d0b18 0%, #140f2d 50%, #080612 100%) !important;
        color: #ffffff !important;
    }

    /* Color de texto blanco para títulos y etiquetas */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #ffffff !important;
    }

    /* Botón de acción estilo Netflix */
    .stButton>button {
        background-color: #E50914 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.15rem !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #B81D24 !important;
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.7);
        transform: translateY(-2px);
    }

    /* Cajas de selección e input oscuras */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #1a1636 !important;
        border-radius: 8px !important;
    }
    </style>
'''
st.markdown(custom_styles, unsafe_allow_html=True)

# 3. Encabezado con Ícono Gigante de Palomitas de Maíz
header_html = '''
    <div style="text-align: center; padding-top: 10px; padding-bottom: 20px;">
        <span style="font-size: 5rem; display: block; line-height: 1; margin-bottom: 5px;">🍿</span>
        <h1 style="font-size: 2.8rem; margin: 0; font-weight: 800; letter-spacing: -1px; color: #ffffff;">Cinematch</h1>
        <p style="font-size: 1.1rem; color: #b0b0d0; margin-top: 5px;">Consultoría de Clasificación Cinematográfica</p>
    </div>
'''
st.markdown(header_html, unsafe_allow_html=True)

st.markdown("---")

# 4. Carga interna de recursos de IA
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../backend/models/modelo_cinematch.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, '../backend/models/label_encoder.pkl')

@st.cache_resource
def cargar_recursos():
    try:
        mod = joblib.load(MODEL_PATH)
        enc = joblib.load(ENCODER_PATH)
        return mod, enc
    except Exception:
        return None, None

modelo, label_encoder = cargar_recursos()

# 5. Formulario Limpio e Intuitivo
st.markdown("#### 📋 Ficha Técnica de la Producción")

titulo = st.text_input("Título de la película", value="Ej. El Viaje Fantástico")

col1, col2 = st.columns(2)

with col1:
    genero = st.selectbox("Género principal", ['ACCION', 'ANIMACION', 'AVENTURA', 'CIENCIA FICCION', 'COMEDIA', 'DRAMA', 'ROMANCE', 'TERROR'])
    duracion = st.number_input("Duración en minutos", min_value=30, max_value=300, value=105, step=5)
    violencia = st.selectbox("¿Contenido con violencia?", ['NO', 'SI'])
    lenguaje = st.selectbox("Lenguaje sensible", ['NINGUNO', 'BAJO', 'MEDIO', 'ALTO'])

with col2:
    rating = st.selectbox("Rating de referencia", ['G', 'PG', 'PG-13', 'R', 'NC-17'])
    anio = st.number_input("Año de estreno", min_value=1950, max_value=2030, value=2024, step=1)
    romance = st.selectbox("¿Contenido romántico?", ['NO', 'SI'])
    animacion = st.selectbox("¿Formato animado?", ['NO', 'SI'])

st.markdown("<br>", unsafe_allow_html=True)

# 6. Acción y Resultado Visual
if st.button("✨ Consultar Clasificación de Audiencia"):
    if modelo is not None and label_encoder is not None:
        input_data = pd.DataFrame([{
            'duracion': float(duracion),
            'anio_estreno': int(anio),
            'genero': genero,
            'violencia': violencia,
            'lenguaje_ofensivo': lenguaje,
            'romance': romance,
            'animacion': animacion,
            'rating': rating
        }])
        
        df_encoded = pd.get_dummies(input_data)
        for col in modelo.feature_names_in_:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[modelo.feature_names_in_]
        
        pred_idx = modelo.predict(df_encoded)
        clase_predicha = label_encoder.inverse_transform([pred_idx])
        
        st.success(f"### 🎯 Audiencia Sugerida: **{clase_predicha[0]}**")
        st.markdown(f"**Película:** {titulo} | **Género:** {genero} | **Duración:** {duracion} min.")
    else:
        st.error("Servicio no disponible en este momento. Intente más tarde.")
