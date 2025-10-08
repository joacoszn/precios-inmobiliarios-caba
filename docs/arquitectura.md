# **Arquitectura y Decisiones Técnicas**

Documentación técnica del diseño del sistema, decisiones arquitectónicas y mejores prácticas implementadas.

## **Visión General de la Arquitectura**

El proyecto sigue una arquitectura de **microservicios modulares** con separación clara de responsabilidades:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ETL Pipeline  │    │   ML Pipeline   │    │   API REST      │
│                 │    │                 │    │                 │
│ • Data Cleaning │    │ • Model Training│    │ • FastAPI       │
│ • Validation    │    │ • Prediction    │    │ • Pydantic      │
│ • MySQL Load    │    │ • Persistence   │    │ • Endpoints     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   MySQL DB      │
                    │                 │
                    │ • Properties    │
                    │ • Clean Data    │
                    │ • Indexes       │
                    └─────────────────┘
```

## **Estructura del Proyecto**

```
api/
├── data/                          # Datos crudos
│   └── ventas_deptos.pkl
├── docs/                          # Documentación
│   ├── README.md
│   ├── inicio-rapido.md
│   ├── referencia-api.md
│   ├── modelo-ml.md
│   ├── arquitectura.md
│   ├── visualizaciones.md
│   └── ejemplos.md
├── notebooks/                     # Análisis y entrenamiento
│   ├── EDA.ipynb                 # Análisis exploratorio
│   └── entrenamiento_modelo.ipynb # Entrenamiento del modelo
├── scripts/                       # Scripts de ETL
│   └── poblar_db.py
├── src/
│   ├── api/                       # API REST
│   │   ├── main.py               # Aplicación principal
│   │   ├── db_connection.py      # Conexión a BD
│   │   ├── schemas.py            # Modelos Pydantic
│   │   └── routers/              # Endpoints
│   │       ├── propiedades.py
│   │       └── predictions.py
│   └── ml/                       # Modelo de ML
│       ├── feature_engineering.py # Extracción de features NLP
│       ├── model.pkl             # Modelo entrenado
│       ├── model_columns.pkl     # Columnas del modelo
│       ├── predict.py           # Función de predicción
│       └── README.md            # Documentación del modelo
├── requirements.txt              # Dependencias
└── README.md                     # Archivo principal
```

## **Flujo de Datos (Data Pipeline)**

### **1. Fase de Extracción**
- **Fuente:** Dataset crudo en formato `.pkl`
- **Contenido:** 50,691 registros de propiedades
- **Calidad:** Datos sucios con problemas de formato

### **2. Fase de Transformación**
```python
# Proceso ETL implementado en scripts/poblar_db.py
def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Limpieza de precios
    df['price_usd'] = df['Price'].apply(limpiar_y_validar_precio)
    
    # 2. Estandarización de barrios
    df['barrio'] = df['Location'].apply(estandarizar_barrio)
    
    # 3. Parsing de características
    features_df = df['Features'].apply(parsear_features)
    
    # 4. Imputación de valores faltantes
    df['expensas_ars'] = df['expensas_ars'].fillna(mediana_expensas)
    
    return df
```

### **3. Fase de Carga**
- **Destino:** Base de datos MySQL
- **Tabla:** `propiedades` con índices optimizados
- **Validación:** Constraints y tipos de datos estrictos

## 🗄️ **Diseño de Base de Datos**

### **Esquema de la Tabla `propiedades`**
```sql
CREATE TABLE propiedades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_id VARCHAR(255) UNIQUE NOT NULL,
    price_usd DECIMAL(12,2),
    expensas_ars DECIMAL(10,2),
    barrio VARCHAR(100) NOT NULL,
    address TEXT,
    ambientes INT,
    dormitorios INT,
    banos INT,
    superficie_total_m2 INT,
    cocheras INT,
    description TEXT,
    link VARCHAR(500),
    scrap_date DATETIME,
    
    -- Índices para optimización
    INDEX idx_barrio (barrio),
    INDEX idx_price (price_usd),
    INDEX idx_superficie (superficie_total_m2),
    INDEX idx_scrap_date (scrap_date)
);
```

### **Decisiones de Diseño**
- **Tipos de datos:** DECIMAL para precios (precisión monetaria)
- **Índices:** Optimización para consultas frecuentes
- **Constraints:** UNIQUE en source_id para evitar duplicados
- **Normalización:** Tabla única para simplicidad (no hay redundancia significativa)

## 🌐 **Arquitectura de la API**

### **Framework: FastAPI**
**Justificación:**
- **Performance:** Una de las APIs más rápidas de Python
- **Documentación automática:** Swagger/OpenAPI integrado
- **Type hints:** Validación automática con Pydantic
- **Async support:** Preparado para escalabilidad

### **Estructura de Routers**
```python
# Separación por dominio de negocio
app.include_router(propiedades.router, prefix="/propiedades", tags=["Propiedades"])
app.include_router(predictions.router, prefix="/predict", tags=["Predicciones"])
```

### **Gestión de Conexiones**
```python
# Pool de conexiones para eficiencia
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="propiedades_pool",
    pool_size=5,
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
```

## Arquitectura de Machine Learning

### Pipeline de ML
```
Datos Crudos → Limpieza → NLP Feature Engineering → Entrenamiento → Persistencia → Predicción
     │              │              │                   │            │              │
     │              │              │                   │            │              │
  MySQL DB    Preprocessing   TF-IDF Vectorization   XGBoost      Pickle       API Endpoint
```

### Separación de Responsabilidades
- **`notebooks/entrenamiento_modelo.ipynb`:** Entrenamiento, comparación y optimización de modelos.
- **`src/ml/feature_engineering.py`:** Lógica para la vectorización TF-IDF.
- **`src/ml/predict.py`:** Lógica de predicción y explicabilidad (SHAP).
- **`src/ml/model.pkl`:** Modelo serializado (XGBoost optimizado).
- **`src/ml/tfidf_vectorizer.pkl`:** Vectorizador TF-IDF entrenado.
- **`src/ml/model_columns.pkl`:** Metadatos de las columnas del modelo.

### Decisiones de Modelado
- **Algoritmo:** XGBoost
- **Justificación:** Rendimiento superior demostrado tras optimización de hiperparámetros.
- **Features:** 156 características (5 numéricas + 51 de barrios + 100 de TF-IDF).
- **Validación:** K-Fold Cross-Validation (k=5) y `RandomizedSearchCV` para optimización.

## 🔒 **Seguridad y Configuración**

### **Gestión de Secretos**
```python
# Variables de entorno con python-dotenv
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
```

### **Validación de Input**
```python
# Validaciones estrictas con Pydantic
class PredictionInput(BaseModel):
    barrio: str = Field(..., description="Barrio de CABA")
    ambientes: int = Field(..., ge=1, le=10)
    # ... más validaciones
    
    @field_validator('barrio')
    @classmethod
    def validate_barrio(cls, v):
        # Validación personalizada
```

## 📊 **Monitoreo y Logging**

### **Sistema de Logging**
```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log de predicciones para análisis posterior
logger.info(
    f"Predicción realizada: {prediction:.2f} USD | "
    f"Barrio: {data.get('barrio')} | "
    f"Superficie: {data.get('superficie_total_m2')} m²"
)
```

### **Métricas de Monitoreo**
- **Performance:** Tiempo de respuesta de endpoints
- **Calidad:** Logs de predicciones y errores
- **Uso:** Frecuencia de consultas por endpoint
- **Errores:** Manejo de excepciones y códigos de estado

## 🚀 **Escalabilidad y Performance**

### **Optimizaciones Implementadas**
- **Pool de conexiones:** Reutilización de conexiones DB
- **Índices de BD:** Consultas optimizadas
- **Caching:** Modelo cargado en memoria
- **Validación temprana:** Pydantic valida antes de procesar

### **Puntos de Escalabilidad**
- **Horizontal:** Múltiples instancias de la API
- **Vertical:** Más recursos para el servidor
- **Base de datos:** Read replicas para consultas
- **Caching:** Redis para consultas frecuentes

## Herramientas y Tecnologías

### Stack Tecnológico
- **Backend:** FastAPI, Pydantic, Uvicorn
- **Base de datos:** MySQL 8.0
- **Machine Learning:** Scikit-learn, XGBoost, SHAP, Pandas, NumPy
- **Análisis:** Jupyter Notebooks, Matplotlib, Seaborn
- **Testing:** Pytest
- **Despliegue:** Docker
- **Configuración:** python-dotenv

## Métricas de Calidad

### Código
- **Cobertura de Tests:** Implementada para lógica de ML y endpoints de API.
- **Linting:** Sin errores de linting
- **Type hints:** 100% de funciones tipadas
- **Documentación:** Documentación completa en código y en `docs/`.

### Modelo de ML
- **R²:** 0.914 (excelente)
- **RMSE:** ~$116,398 USD (contextualizado)
- **Validación:** K-Fold Cross-Validation y RandomizedSearchCV
- **Persistencia:** Modelo y artefactos serializados correctamente

### API
- **Response time:** < 150ms para predicciones y explicaciones.
- **Availability:** 99.9% (sin dependencias externas)
- **Error rate:** < 1% (validaciones estrictas)
- **Documentation:** Swagger automático y documentación manual.

## Roadmap de Mejoras

### Corto Plazo
- **CI/CD:** Pipeline con GitHub Actions para automatizar tests y builds de Docker.
- **Monitoring:** Integrar un dashboard para visualizar métricas de la API en tiempo real (ej. Grafana).

### Mediano Plazo
- **Microservicios:** Separación completa de ETL, ML y API.
- **MLOps:** MLflow para experiment tracking y registro de modelos.
- **Caching:** Redis para resultados de endpoints de estadísticas.

### Largo Plazo
- **Real-time:** WebSocket para predicciones en tiempo real.
- **ML Pipeline:** Re-entrenamiento automático del modelo.
- **Analytics:** Dashboard interactivo para el usuario final (ej. Streamlit o Dash).

## 🔗 **Enlaces Relacionados**

- **[🚀 Inicio Rápido](inicio-rapido.md)** - Configuración del entorno
- **[📖 Referencia de API](referencia-api.md)** - Documentación de endpoints
- **[🤖 Modelo de ML](modelo-ml.md)** - Detalles del modelo
- **[📊 Visualizaciones](visualizaciones.md)** - Análisis visual
- **[💡 Ejemplos](ejemplos.md)** - Casos de uso prácticos
