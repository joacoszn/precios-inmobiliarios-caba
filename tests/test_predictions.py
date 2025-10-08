import pytest
from fastapi.testclient import TestClient
import sys
import os

# Añadir el directorio raíz al path para permitir la importación de la app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.api.main import app

client = TestClient(app)

def test_predict_endpoint_input_valido():
    """Prueba el endpoint /predict con una entrada válida."""
    # Datos de ejemplo que se ajustan al esquema de la API
    test_data = {
        "barrio": "Palermo",
        "ambientes": 2,
        "dormitorios": 1,
        "banos": 1,
        "superficie_total_m2": 50,
        "cocheras": 0,
        "description": "Departamento luminoso en el corazón de Palermo."
    }
    
    response = client.post("/predict/", json=test_data)
    
    # Verificar que la respuesta es exitosa
    assert response.status_code == 200
    
    # Verificar que la respuesta es un JSON
    response_json = response.json()
    assert isinstance(response_json, dict)
    
    # Verificar que las claves esperadas están en la respuesta
    assert "predicted_price_usd" in response_json
    assert "confidence_interval" in response_json
    assert "similar_properties_avg" in response_json

def test_get_model_info_endpoint():
    """Prueba el endpoint /predict/model-info."""
    response = client.get("/predict/model-info")
    
    # Verificar que la respuesta es exitosa
    assert response.status_code == 200
    
    # Verificar que la respuesta es un JSON
    response_json = response.json()
    assert isinstance(response_json, dict)
    
    # Verificar que las claves de información del modelo están presentes
    assert "model_type" in response_json
    assert "n_features" in response_json
    assert "metrics" in response_json
    assert "top_features" in response_json

def test_predict_endpoint_input_invalido():
    """Prueba el endpoint /predict con una entrada inválida (falta un campo)."""
    # Datos inválidos (falta 'superficie_total_m2')
    test_data = {
        "barrio": "Villa Crespo",
        "ambientes": 3,
        "dormitorios": 2,
        "banos": 1,
        "cocheras": 1,
        "description": "Amplio departamento."
    }
    
    response = client.post("/predict/", json=test_data)
    
    # FastAPI debe devolver un error 422 Unprocessable Entity por fallo de validación de Pydantic
    assert response.status_code == 422

def test_explain_endpoint_valid_input():
    """Prueba el endpoint /predict/explain con una entrada válida."""
    test_data = {
        "barrio": "Palermo",
        "ambientes": 2,
        "dormitorios": 1,
        "banos": 1,
        "superficie_total_m2": 50,
        "cocheras": 0,
        "description": "Departamento luminoso en el corazón de Palermo."
    }
    
    response = client.post("/predict/explain", json=test_data)
    
    # Verificar que la respuesta es exitosa
    assert response.status_code == 200
    
    # Verificar que la respuesta es un JSON
    response_json = response.json()
    assert isinstance(response_json, dict)
    
    # Verificar que las claves esperadas están en la respuesta
    assert "base_value" in response_json
    assert "shap_values" in response_json
    assert "prediction_usd" in response_json
    
    # Verificar que shap_values es una lista
    assert isinstance(response_json["shap_values"], list)