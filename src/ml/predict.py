# src/ml/predict.py
import pickle
import pandas as pd
import numpy as np
import os
from mysql.connector.cursor import MySQLCursorDict
import logging
from typing import Optional
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Rutas a los archivos del modelo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
COLUMNS_PATH = os.path.join(BASE_DIR, 'model_columns.pkl')

# Carga de artefactos del modelo
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
    
    tree_predictions = [tree.predict(final_df)[0] for tree in model.estimators_]
    std = np.std(tree_predictions)
    
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

def get_similar_properties_avg(data: dict, cursor: MySQLCursorDict) -> Optional[float]:
    """
    Calcula el precio promedio de propiedades similares usando un cursor existente.
    Ahora retorna Optional[float] para permitir el valor None.
    """
    try:
        query = """
            SELECT AVG(price_usd) as avg_price
            FROM propiedades 
            WHERE barrio = %s 
            AND ambientes BETWEEN %s AND %s
            AND superficie_total_m2 BETWEEN %s AND %s
            AND price_usd IS NOT NULL
        """
        
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
        avg_price = result['avg_price'] if result and result.get('avg_price') is not None else None
        
        if isinstance(avg_price, Decimal):
            return float(avg_price)
        
        return avg_price 
        
    except Exception as e:
        print(f"Error calculando promedio de propiedades similares: {e}")
        return None
