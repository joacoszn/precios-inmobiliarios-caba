from pydantic import BaseModel, Field
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
    barrio: str
    ambientes: int = Field(..., ge=0)
    dormitorios: int = Field(..., ge=0)
    banos: int = Field(..., ge=0)
    superficie_total_m2: int = Field(..., gt=0)
    cocheras: int = Field(..., ge=0)

class PredictionOutput(BaseModel):
    predicted_price_usd: float





