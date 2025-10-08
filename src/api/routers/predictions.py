# src/api/routers/predictions.py
from fastapi import APIRouter, HTTPException, Depends
from ..schemas import PredictionInput, PredictionOutput, ModelInfo, PredictionExplanation, ShapValue
from ...ml.predict import (
    predict_price, get_similar_properties_avg, 
    model, model_columns, vectorizer, explainer
)
from ...ml.feature_engineering import crear_features_nlp
from ..db_connection import get_db_cursor
from mysql.connector.cursor import MySQLCursorDict
import json
import os
import pandas as pd
import numpy as np

# ruta de de forma relativa y robusta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, '..', '..', 'ml')
METRICS_PATH = os.path.join(ML_DIR, 'metrics.json')

try:
    with open(METRICS_PATH, 'r') as f:
        model_metrics = json.load(f)
    print("✅ Métricas del modelo cargadas exitosamente.")
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo de métricas en {METRICS_PATH}")
    #  métricas por defecto si el archivo no existe
    model_metrics = {"r2_score": "N/A", "rmse_usd": "N/A"}


router = APIRouter()

@router.post("/", response_model=PredictionOutput, summary="Predecir el precio de una propiedad")
def predict_property_price(input_data: PredictionInput, cursor: MySQLCursorDict = Depends(get_db_cursor)):
    """
    Recibe las características de una propiedad y devuelve una predicción de su precio en USD
    con intervalo de confianza y promedio de propiedades similares.
    """
    if model is None or model_columns is None:
        raise HTTPException(
            status_code=503, 
            detail="Modelo de predicción no está disponible. Revise los logs del servidor."
        )
    
    try:
        data_dict = input_data.model_dump()
        
        prediction_result = predict_price(data_dict)
        
        similar_avg = get_similar_properties_avg(data_dict, cursor)
        
        return PredictionOutput(
            predicted_price_usd=prediction_result["predicted_price_usd"],
            confidence_interval=prediction_result["confidence_interval"],
            similar_properties_avg=similar_avg
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la predicción: {e}")

@router.get("/model-info", response_model=ModelInfo, summary="Información del modelo y feature importance")
def get_model_info():
    """
    Devuelve metadata del modelo: tipo, métricas, y features más importantes.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    feature_names = model_columns
    importances = model.feature_importances_
    
    feature_importance = [
        {"feature": name, "importance": float(imp)} 
        for name, imp in sorted(
            zip(feature_names, importances), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
    ]
    
    return {
        "model_type": type(model).__name__,
        "n_features": len(model_columns),
        "n_estimators": model.n_estimators,
        "metrics": model_metrics, 
        "top_features": feature_importance
    }

@router.post("/explain", response_model=PredictionExplanation, summary="Explicar una predicción de precio")
def explain_property_price(input_data: PredictionInput):
    """
    Recibe las características de una propiedad y devuelve un análisis de SHAP
    que explica cómo cada característica contribuye a la predicción final.
    """
    if explainer is None or model is None or model_columns is None or vectorizer is None:
        raise HTTPException(
            status_code=503, 
            detail="El explicador del modelo no está disponible."
        )

    try:
        # --- Replicar el pipeline de transformación de datos ---
        data_dict = input_data.model_dump()
        input_df = pd.DataFrame([data_dict])
        
        nlp_features_df, _ = crear_features_nlp(input_df, 'description', vectorizer=vectorizer)
        
        input_df_no_desc = input_df.drop(columns=['description'], errors='ignore')
        input_enriquecido = pd.concat([input_df_no_desc, nlp_features_df], axis=1)

        input_encoded = pd.get_dummies(input_enriquecido, columns=['barrio'], dtype=int)
        
        final_df = input_encoded.reindex(columns=model_columns, fill_value=0)
        
        # --- Calcular valores SHAP ---
        shap_values = explainer.shap_values(final_df)
        
        # Formatear la salida
        shap_values_list = []
        for feature, shap_value in zip(final_df.columns, shap_values[0]):
            # Solo incluir features que tienen un impacto (no son cero)
            if shap_value != 0:
                shap_values_list.append(ShapValue(feature=feature, value=shap_value))
        
        # Ordenar por valor absoluto para mostrar los más importantes primero
        shap_values_list.sort(key=lambda x: abs(x.value), reverse=True)
        
        base_value = explainer.expected_value
        prediction = np.sum(shap_values[0]) + base_value

        return PredictionExplanation(
            base_value=base_value,
            shap_values=shap_values_list[:15], # Devolver solo los 15 más importantes
            prediction_usd=prediction
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar la explicación: {e}")