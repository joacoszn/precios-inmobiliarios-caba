# Real State CABA API: API de Análisis y Predicción de Precios Inmobiliarios basado en el mercado de la Ciudad Autonoma de Buenos Aires.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.0-orange.svg)](https://xgboost.ai/)

## 🏠 ¿Qué es preciosCABA?

Una API de nivel profesional para el análisis del mercado inmobiliario que procesa datos de propiedades en la Ciudad de Buenos Aires y ofrece:

- **🤖 Predicciones de precios** precisas utilizando un modelo XGBoost optimizado.
- **🧠 Explicabilidad de predicciones (XAI)**, detallando qué factores influyen en cada estimación.
- **📊 Consultas estadísticas** sobre el mercado inmobiliario.
- **📈 Visualizaciones** y insights de mercado.

## 🚀 Inicio Rápido (con Docker)

El proyecto está containerizado para un despliegue rápido y sencillo. Solo necesita tener Docker instalado.

**1. Crear archivo de credenciales (`.env`)**

En la raíz del proyecto (`api/`), cree un archivo llamado `.env` con el siguiente contenido, reemplazando los valores con sus credenciales de MySQL:

```
DB_USER=su_usuario_de_mysql
DB_PASSWORD=su_contraseña_de_mysql
DB_HOST=host.docker.internal
DB_NAME=inmobiliario
```
> **Nota:** `host.docker.internal` es un DNS especial que permite al contenedor conectarse a la base de datos que corre en su máquina local.

**2. Construir la imagen de Docker**

```bash
docker build -t real-estate-api .
```

**3. Ejecutar el contenedor**

```bash
docker run -d -p 8000:8000 --name real-estate-container --env-file .env real-estate-api
```

**4. Acceder a la API**

La API ahora está corriendo en segundo plano. Puede acceder a la documentación interactiva (Swagger UI) en:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

## Documentación Completa

Para un entendimiento profundo del proyecto, consulte la carpeta `docs/`:

- **[Referencia de API](docs/referencia-api.md)** - Documentación completa de endpoints.
- **[Modelo de ML](docs/modelo-ml.md)** - Detalles del modelo, feature engineering y métricas.
- **[Arquitectura](docs/arquitectura.md)** - Diseño técnico y decisiones.
- **[Visualizaciones](docs/visualizaciones.md)** - Gráficos y análisis estadísticos.

## Características Principales

- **Machine Learning Avanzado:**
  - Modelo `XGBoost` optimizado con `RandomizedSearchCV` (R² = 0.914).
  - Explicabilidad de predicciones (XAI) con `SHAP` a través del endpoint `/explain`.
  - Feature Engineering con `TF-IDF` para procesar descripciones textuales.
- **API Robusta:**
  - Endpoints para predicción, explicación e información del modelo.
  - Suite de tests unitarios con `pytest` que garantiza la fiabilidad.
  - Validaciones de entrada de datos con `Pydantic`.
- **Containerización:**
  - `Dockerfile` optimizado para producción.
  - Archivo `.dockerignore` para builds limpios y rápidos.

## 🛠️ Tecnologías Utilizadas

- **Backend:** FastAPI, Pydantic, Uvicorn
- **Machine Learning:** Scikit-learn, XGBoost, SHAP, Pandas, NumPy
- **Base de Datos:** MySQL
- **Testing:** Pytest
- **Despliegue:** Docker

## Ejemplo de Explicación (XAI)

```json
POST /predict/explain
{
  "barrio": "Palermo",
  "ambientes": 2,
  "superficie_total_m2": 50,
  "dormitorios": 1,
  "banos": 1,
  "cocheras": 0,
  "description": "Departamento luminoso en el corazón de Palermo, cerca del subte."
}
```

**Respuesta (Ejemplo):**
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

## Estado del Proyecto: Completado

- [x] Análisis Exploratorio de Datos (EDA).
- [x] Pipeline ETL para limpieza y carga de datos.
- [x] Feature Engineering avanzado con TF-IDF.
- [x] Comparación y optimización de modelos (RandomForest vs. XGBoost).
- [x] Implementación de explicabilidad del modelo (XAI con SHAP).
- [x] API REST completa con endpoints de predicción y explicación.
- [x] Suite de tests unitarios con Pytest.
- [x] Containerización de la aplicación con Docker.
- [x] Documentación técnica completa de todo el proceso.

## 👨‍💻 Sobre el Proyecto

Este proyecto demuestra un ciclo de vida de ciencia de datos completo y de nivel profesional, desde el análisis exploratorio hasta el despliegue de un modelo interpretable en un contenedor, siguiendo las mejores prácticas de la industria en MLOps y desarrollo de software.

**Contacto:** joaquin99911@gmail.com
