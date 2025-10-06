import pickle
import pandas as pd
import os

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

def predict_price(data: dict) -> float:
    """
    Realiza una predicción de precio basada en los datos de entrada.
    
    Args:
        data (dict): Un diccionario con las características de la propiedad.

    Returns:
        float: El precio predicho en USD.
    """
    if model is None or model_columns is None:
        raise RuntimeError("El modelo o las columnas no se han cargado correctamente.")

    # 1. Crear un DataFrame a partir de los datos de entrada
    input_df = pd.DataFrame([data])
    
    # 2. Convertir la variable categórica 'barrio' usando One-Hot Encoding
    input_encoded = pd.get_dummies(input_df, columns=['barrio'], dtype=int)
    
    # 3. Alinear las columnas con las del modelo
    # Nos aseguramos de que el DataFrame de entrada tenga exactamente las mismas
    # columnas (y en el mismo orden) que el modelo espera.
    # Las columnas faltantes (otros barrios) se rellenarán con 0.
    final_df = input_encoded.reindex(columns=model_columns, fill_value=0)
    
    # 4. Realizar la predicción
    prediction = model.predict(final_df)
    
    return float(prediction[0])
