import pytest
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import os

# Añadir el directorio raíz al path para permitir la importación de módulos del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ml.feature_engineering import crear_features_nlp

@pytest.fixture
def sample_dataframe():
    """Crea un DataFrame de ejemplo para usar en las pruebas."""
    data = {
        'description': [
            'un departamento luminoso con balcon',
            'propiedad reciclada a nuevo, con seguridad 24hs',
            'amenities como pileta y gimnasio',
            '',
            None
        ]
    }
    return pd.DataFrame(data)

def test_crear_features_nlp_shape(sample_dataframe):
    """Prueba que la salida de crear_features_nlp tenga la forma correcta."""
    df_features, vectorizer = crear_features_nlp(sample_dataframe)
    
    # Verificar que el número de filas es el mismo
    assert len(df_features) == len(sample_dataframe)
    
    # Verificar que se crearon el número correcto de columnas
    assert df_features.shape[1] == len(vectorizer.vocabulary_)

def test_crear_features_nlp_return_type(sample_dataframe):
    """Prueba que la función devuelva los tipos de objeto correctos"""
    result = crear_features_nlp(sample_dataframe)
    
    # Verificar que el resultado es una tupla
    assert isinstance(result, tuple)
    assert len(result) == 2
    
    # Verificar que el primer elemento es un DataFrame
    assert isinstance(result[0], pd.DataFrame)
    
    # Verificar que el segundo elemento es un TfidfVectorizer
    assert isinstance(result[1], TfidfVectorizer)

def test_crear_features_nlp_con_vectorizador_existente(sample_dataframe):
    """Prueba que la función puede usar un vectorizer pre-entrenado."""
    # Entrenar un vectorizer con los primeros 2 registros
    train_data = sample_dataframe.iloc[:2]
    _, vectorizer = crear_features_nlp(train_data)
    
    # Usar el vectorizer entrenado en los datos restantes
    test_data = sample_dataframe.iloc[2:]
    df_features, _ = crear_features_nlp(test_data, vectorizer=vectorizer)
    
    # Verificar que la forma de la salida es correcta
    assert len(df_features) == len(test_data)
    assert df_features.shape[1] == len(vectorizer.vocabulary_)
