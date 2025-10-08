# Referencia de API

Documentación completa de todos los endpoints disponibles en la API de análisis inmobiliario.

## Base URL

`http://127.0.0.1:8000`

## Endpoints de Machine Learning

### Predicción de Precios

`POST /predict/`

**Body:**
```json
{
  "barrio": "Palermo",
  "ambientes": 2,
  "superficie_total_m2": 50,
  "dormitorios": 1,
  "banos": 1,
  "cocheras": 0,
  "description": "Departamento luminoso en el corazón de Palermo."
}
```

**Respuesta:**
```json
{
  "predicted_price_usd": 219092.61,
  "confidence_interval": {
    "lower": null,
    "upper": null
  },
  "similar_properties_avg": 156754.73
}
```

### Explicación de Predicción (XAI)

`POST /predict/explain`

**Body:**
```json
{
  "barrio": "Palermo",
  "ambientes": 2,
  "superficie_total_m2": 50,
  "dormitorios": 1,
  "banos": 1,
  "cocheras": 0,
  "description": "Departamento luminoso en el corazón de Palermo."
}
```

**Respuesta:**
```json
{
  "base_value": 150000.0,
  "shap_values": [
    { "feature": "superficie_total_m2", "value": 45000.0 },
    { "feature": "barrio_Palermo", "value": 25000.0 },
    { "feature": "tfidf_25", "value": 3500.0 },
    { "feature": "ambientes", "value": -2000.0 }
  ],
  "prediction_usd": 221500.0
}
```

### Información del Modelo

`GET /predict/model-info`

**Respuesta:**
```json
{
  "model_type": "XGBRegressor",
  "n_features": 156,
  "n_estimators": 300,
  "metrics": {
    "model": "XGBoost",
    "r2_score_mean": 0.914,
    "rmse_usd_mean": 116398
  },
  "top_features": [
    {
      "feature": "superficie_total_m2",
      "importance": 0.35
    },
    {
      "feature": "barrio_Recoleta",
      "importance": 0.08
    },
    {
      "feature": "tfidf_88",
      "importance": 0.02
    }
  ]
}
```
