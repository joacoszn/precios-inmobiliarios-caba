import pickle
import pandas as pd
import numpy as np
import os
import mysql.connector
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Construimos las rutas a los archivos del modelo
# __file__ se refiere a la ubicación de este script (src/ml/predict.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
COLUMNS_PATH = os.path.join(BASE_DIR, 'model_columns.pkl')

# --- Carga de artefactos del modelo ---
# Estos objetos se cargarán una sola vez cuando se inicie la aplicación.
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("✅ Modelo cargado exitosamente.")
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo del modelo en {MODEL_PATH}")
    model = None

try:
    with open(COLUMNS_PATH, 'rb') as f:
        model_columns = pickle.load(f)
    print("✅ Columnas del modelo cargadas exitosamente.")
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo de columnas en {COLUMNS_PATH}")
    model_columns = None

def predict_price(data: dict) -> dict:
    """Retorna predicción + intervalo de confianza"""
    if model is None or model_columns is None:
        raise RuntimeError("El modelo o las columnas no se han cargado correctamente.")

    input_df = pd.DataFrame([data])
    input_encoded = pd.get_dummies(input_df, columns=['barrio'], dtype=int)
    final_df = input_encoded.reindex(columns=model_columns, fill_value=0)
    
    prediction = model.predict(final_df)[0]
    
    # Intervalo de confianza usando desviación estándar de árboles
    tree_predictions = [tree.predict(final_df)[0] for tree in model.estimators_]
    std = np.std(tree_predictions)
    
    # Log de predicción (útil para análisis posterior)
    logger.info(
        f"Predicción realizada: {prediction:.2f} USD | "
        f"Barrio: {data.get('barrio')} | "
        f"Superficie: {data.get('superficie_total_m2')} m²"
    )
    
    return {
        "predicted_price_usd": float(prediction),
        "confidence_interval": {
            "lower": float(prediction - 1.96 * std),
            "upper": float(prediction + 1.96 * std)
        }
    }

def get_similar_properties_avg(data: dict) -> float:
    """
    Calcula el precio promedio de propiedades similares en el mismo barrio.
    
    Args:
        data (dict): Un diccionario con las características de la propiedad.

    Returns:
        float: El precio promedio de propiedades similares en USD.
    """
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
        cursor = conn.cursor()
        
        # Construir query para propiedades similares
        # Buscamos propiedades en el mismo barrio con características similares
        query = """
            SELECT AVG(price_usd) as avg_price
            FROM propiedades 
            WHERE barrio = %s 
            AND ambientes BETWEEN %s AND %s
            AND superficie_total_m2 BETWEEN %s AND %s
            AND price_usd IS NOT NULL
        """
        
        # Definir rangos de similitud (±1 ambiente, ±20% superficie)
        ambientes_min = max(1, data['ambientes'] - 1)
        ambientes_max = data['ambientes'] + 1
        superficie_min = max(20, int(data['superficie_total_m2'] * 0.8))
        superficie_max = int(data['superficie_total_m2'] * 1.2)
        
        cursor.execute(query, (
            data['barrio'],
            ambientes_min, ambientes_max,
            superficie_min, superficie_max
        ))
        
        result = cursor.fetchone()
        avg_price = result[0] if result and result[0] else None
        
        cursor.close()
        conn.close()
        
        return float(avg_price) if avg_price else None
        
    except Exception as e:
        print(f"Error calculando promedio de propiedades similares: {e}")
        return None
