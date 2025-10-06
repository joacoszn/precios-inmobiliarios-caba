from fastapi import APIRouter, HTTPException
from ..schemas import PredictionInput, PredictionOutput
from ...ml.predict import predict_price, model, model_columns

router = APIRouter()

@router.post("/", response_model=PredictionOutput, summary="Predecir el precio de una propiedad")
def predict_property_price(input_data: PredictionInput):
    """
    Recibe las características de una propiedad y devuelve una predicción de su precio en USD.
    """
    if model is None or model_columns is None:
        raise HTTPException(
            status_code=503, 
            detail="Modelo de predicción no está disponible. Revise los logs del servidor."
        )
    
    try:
        # Convertimos el modelo Pydantic a un diccionario para la función de predicción
        data_dict = input_data.model_dump()
        predicted_price = predict_price(data_dict)
        return PredictionOutput(predicted_price_usd=predicted_price)
    except Exception as e:
        # Capturamos cualquier error inesperado durante la predicción
        raise HTTPException(status_code=500, detail=f"Error al realizar la predicción: {e}")
