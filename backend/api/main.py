# ================================================================
# Servicio Backend API REST - Cinematch
# Ubicación: backend/api/main.py
# ==============================================================================

import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Rutas absolutas del modelo y encoder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../models/modelo_cinematch.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, '../models/label_encoder.pkl')

# Cargar artefactos de IA al iniciar el servidor
modelo = None
label_encoder = None

try:
    modelo = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    print("✓ Modelo y Encoder cargados exitosamente en la API.")
except Exception as e:
    print(f" Error al cargar artefactos de IA: {e}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "sistema": "Cinematch API REST",
        "estado": "Activo",
        "version": "1.0.0"
    })

@app.route('/predict', methods=['POST'])
def predict():
    if not modelo or not label_encoder:
        return jsonify({"error": "El modelo no está disponible en el servidor"}), 500

    try:
        data = request.get_json()

        # Estructurar características para el modelo
        df_input = pd.DataFrame([{
            'duracion': float(data.get('duracion', 100)),
            'anio_estreno': int(data.get('anio_estreno', 2024)),
            'genero': data.get('genero', 'COMEDIA'),
            'violencia': data.get('violencia', 'NO'),
            'lenguaje_ofensivo': data.get('lenguaje_ofensivo', 'BAJO'),
            'romance': data.get('romance', 'NO'),
            'animacion': data.get('animacion', 'NO'),
            'rating': data.get('rating', 'PG')
        }])

        # Aplicar One-Hot Encoding compatible
        df_encoded = pd.get_dummies(df_input)
        
        # Alinear columnas con el dataset de entrenamiento
        for col in modelo.feature_names_in_:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[modelo.feature_names_in_]

        # Realizar la predicción
        pred_idx = modelo.predict(df_encoded)[0]
        publico_predicho = label_encoder.inverse_transform([pred_idx])[0]

        return jsonify({
            "pelicula": data.get("titulo", "Sin título"),
            "publico_objetivo_predicho": publico_predicho,
            "estado_prediccion": "Exitoso"
        })

    except Exception as e:
        return jsonify({"error": f"Fallo en la inferencia: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
