from fastapi import FastAPI
from .routers import propiedades, predictions

app = FastAPI(
    title="API de Análisis Inmobiliario CABA",
    description="Una API para consultar y analizar datos de propiedades ubicadas en CABA, y predecir sus precios.",
    version="1.0.0"
)

# routers para la aplicación
app.include_router(propiedades.router, prefix="/propiedades", tags=["Propiedades"])
app.include_router(
    predictions.router, 
    prefix="/predict", 
    tags=["Predicciones"]
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Análisis Inmobiliario CABA. Visite /docs para la documentación."}
