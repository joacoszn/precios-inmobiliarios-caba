# src/ml/feature_engineering.py
import pandas as pd
from typing import List

# Definicion de keywords
# Basado en el análisis exploratorio, estas palabras tienen un alto potencial predictivo.
KEYWORDS: List[str] = [
    'balcon', 
    'luminoso', 
    'seguridad', 
    'pileta', 
    'gimnasio', 
    'sum', 
    'parrilla', 
    'estrenar',  
    'reciclado', 
    'cochera', 
    'amenities'
]

def crear_features_nlp(df: pd.DataFrame, text_column: str = 'description') -> pd.DataFrame:
    """
    Analiza una columna de texto en un DataFrame y crea características booleanas
    basadas en la presencia de palabras clave predefinidas.

    Args:
        df (pd.DataFrame): El DataFrame de entrada que contiene la columna de texto.
        text_column (str): El nombre de la columna que contiene las descripciones.

    Returns:
        pd.DataFrame: Un nuevo DataFrame con una columna booleana (0 o 1) por cada
                      palabra clave, indicando su presencia en el texto.
    """
    # Asegurarse de que la columna de texto exista y rellenar valores nulos
    if text_column not in df.columns:
        # Si la columna no existe (ej. en una predicción sin descripción),
        # devolvemos un DataFrame de ceros con la estructura correcta.
        return pd.DataFrame({f'feature_{key}': [0] * len(df) for key in KEYWORDS}, index=df.index)
        
    # Convertir a minúsculas y rellenar NaNs con string vacío para evitar errores
    text_series = df[text_column].str.lower().fillna('')
    
    # Crear un DataFrame para las nuevas características
    nlp_features = pd.DataFrame(index=df.index)
    
    # Para cada palabra clave, verificar si está presente en la descripción
    for keyword in KEYWORDS:
        new_column_name = f'feature_{keyword}'
        nlp_features[new_column_name] = text_series.str.contains(keyword, regex=False).astype(int)
        
    return nlp_features