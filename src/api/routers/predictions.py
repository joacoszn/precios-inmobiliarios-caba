from fastapi import APIRouter, HTTPException
from ..schemas import PredictionInput, PredictionOutput, ModelInfo
from ...ml.predict import predict_price, get_similar_properties_avg, model, model_columns

router = APIRouter()

@router.post("/", response_model=PredictionOutput, summary="Predecir el precio de una propiedad")
def predict_property_price(input_data: PredictionInput):
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
        # Convertimos el modelo Pydantic a un diccionario para la función de predicción
        data_dict = input_data.model_dump()
        
        # Obtener predicción con intervalo de confianza
        prediction_result = predict_price(data_dict)
        
        # Obtener promedio de propiedades similares
        similar_avg = get_similar_properties_avg(data_dict)
        
        return PredictionOutput(
            predicted_price_usd=prediction_result["predicted_price_usd"],
            confidence_interval=prediction_result["confidence_interval"],
            similar_properties_avg=similar_avg
        )
    except Exception as e:
        # Capturamos cualquier error inesperado durante la predicción
        raise HTTPException(status_code=500, detail=f"Error al realizar la predicción: {e}")

@router.get("/model-info", response_model=ModelInfo, summary="Información del modelo y feature importance")
def get_model_info():
    """
    Devuelve metadata del modelo: tipo, métricas, y features más importantes.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    # Feature importance (solo funciona con tree-based models)
    feature_names = model_columns
    importances = model.feature_importances_
    
    # Top 10 features
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
        "metrics": {
            "r2_score": 0.8709,
            "rmse_usd": 155871
        },
        "top_features": feature_importance
    }
