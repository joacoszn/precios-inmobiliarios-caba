from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

# --- Schemas para Propiedades (CRUD y Listado) ---

class PropiedadBase(BaseModel):
    source_id: str
    price_usd: Optional[float] = Field(None, gt=0, description="El precio debe ser mayor que cero")
    expensas_ars: Optional[float] = Field(None, ge=0)
    barrio: str
    address: Optional[str] = None
    ambientes: Optional[int] = Field(None, ge=0)
    dormitorios: Optional[int] = Field(None, ge=0)
    banos: Optional[int] = Field(None, ge=0)
    superficie_total_m2: Optional[int] = Field(None, gt=0)
    cocheras: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    link: Optional[str] = None
    scrap_date: Optional[datetime] = None

class PropiedadCreate(PropiedadBase):
    price_usd: float = Field(..., gt=10000, description="El precio debe ser mayor que 10,000")

class PropiedadUpdate(BaseModel):
    price_usd: Optional[float] = Field(None, gt=10000, description="El precio debe ser mayor que 10,000")
    expensas_ars: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None

class Propiedad(PropiedadBase):
    id: int

    class Config:
        from_attributes = True

# --- Schemas para Estadísticas ---

class EstadisticasBarrio(BaseModel):
    barrio: str
    cantidad_propiedades: int
    precio_promedio_usd: float
    precio_min_usd: float
    precio_max_usd: float
    precio_promedio_m2_usd: float

class EvolucionMercado(BaseModel):
    scrap_date: datetime
    cantidad_propiedades: int
    precio_promedio_usd: float

# --- Schemas para Predicción ---

class PredictionInput(BaseModel):
    barrio: str = Field(..., description="Barrio de CABA")
    ambientes: int = Field(..., ge=1, le=10, description="Entre 1 y 10 ambientes")
    dormitorios: int = Field(..., ge=0, le=8)
    banos: int = Field(..., ge=1, le=6)
    superficie_total_m2: int = Field(..., gt=20, lt=1000, description="Entre 20 y 1000 m²")
    cocheras: int = Field(..., ge=0, le=4)
    
    @field_validator('barrio')
    @classmethod
    def validate_barrio(cls, v):
        barrios_validos = [
            "Palermo", "Recoleta", "Belgrano", "Caballito", "Villa Urquiza",
            "Núñez", "Almagro", "Villa Crespo", "Colegiales", "Barrio Norte",
            "San Telmo", "La Boca", "Puerto Madero", "Retiro", "San Nicolás",
            "Balvanera", "Monserrat", "Constitucion", "Barracas", "Parque Patricios",
            "Boedo", "San Cristobal", "Liniers", "Mataderos", "Villa Lugano",
            "Villa Riachuelo", "Villa Soldati", "Pompeya", "Parque Chacabuco",
            "Parque Avellaneda", "Versalles", "Villa Real", "Monte Castro",
            "Villa Devoto", "Villa del Parque", "Villa Santa Rita", "Agronomia",
            "Chacarita", "Paternal", "Villa Ortuzar", "Coghlan", "Parque Chas",
            "Floresta", "Villa Luro", "Villa Pueyrredon", "Villa General Mitre",
            "Velez Sarsfield", "Flores", "Saavedra"
        ]
        if v not in barrios_validos:
            raise ValueError(f"Barrio '{v}' no es válido. Debe ser uno de: {barrios_validos}")
        return v
    
    @field_validator('dormitorios')
    @classmethod
    def validate_dormitorios_vs_ambientes(cls, v, info):
        if 'ambientes' in info.data and v > info.data['ambientes']:
            raise ValueError("Los dormitorios no pueden superar los ambientes")
        return v

class PredictionOutput(BaseModel):
    predicted_price_usd: float
    confidence_interval: Optional[dict] = Field(
        None, 
        description="Rango de confianza de la predicción"
    )
    similar_properties_avg: Optional[float] = Field(
        None,
        description="Precio promedio de propiedades similares en el mismo barrio"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_price_usd": 185000.0,
                "confidence_interval": {"lower": 170000, "upper": 200000},
                "similar_properties_avg": 178500.0
            }
        }

class FeatureImportance(BaseModel):
    feature: str
    importance: float

class ModelInfo(BaseModel):
    model_type: str
    n_features: int
    n_estimators: int
    metrics: dict
    top_features: List[FeatureImportance]





