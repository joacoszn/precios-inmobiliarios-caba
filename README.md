# **preciosCABA: API de Análisis y Predicción de Precios sobre el mercado inmobiliario en la Ciudad de Buenos Aires**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)](https://mysql.com)

## **1\. Propósito del Proyecto**

Este proyecto es un caso de estudio de ciclo completo (end-to-end) diseñado para demostrar habilidades en **Análisis e Ingeniería de Datos, Desarrollo de Backend y Machine Learning**. El objetivo es procesar un dataset crudo de propiedades inmobiliarias en la Ciudad de Buenos Aires, almacenarlo en una base de datos limpia y exponerlo a través de una API RESTful que no solo sirve los datos, sino que también ofrece insights analíticos y **predicciones de precios en tiempo real**.

## **2\. Características Principales de la API**

La API, construida con **FastAPI**, ofrece las siguientes funcionalidades:

* **Gestión de Datos (CRUD):** Endpoints para Crear (POST), Leer (GET), Actualizar (PUT) y Eliminar (DELETE) registros de propiedades.  
* **Consultas Avanzadas:** Endpoint de listado con capacidades de **filtrado** por múltiples criterios (barrio, ambientes, precio) y **paginación**.  
* **Insights Analíticos:**  
  * GET /estadisticas/precio-por-barrio/: Devuelve estadísticas agregadas (conteo, precio promedio, min/max y **precio promedio por m²**) para cada barrio.  
  * GET /estadisticas/evolucion-mercado/: Analiza la evolución de precios y la cantidad de listados a través de las diferentes fechas de recolección de datos.  
* **Predicción de Precios:** Un endpoint para predecir el precio de una propiedad basándose en sus características usando un modelo de Machine Learning entrenado.

## **3\. Arquitectura y Metodología**

El proyecto se desarrolló siguiendo la metodología **D.P.E. (Descubrir, Planificar, Ejecutar)**, asegurando un proceso ordenado y de alta calidad.

* **Fase 1: Descubrir (Análisis Exploratorio \- EDA):**  
  * Se realizó una investigación exhaustiva del dataset crudo en un Jupyter Notebook (notebooks/1\_analisis\_exploratorio.ipynb).  
  * Se identificaron problemas críticos de calidad de datos: tipos de datos incorrectos, valores nulos, inconsistencias en categorías (ej. Location) y la presencia de outliers.  
  * Estos hallazgos fueron la base para planificar el proceso de limpieza.  
* **Fase 2 y 3: Planificar y Ejecutar:**  
  * **ETL:** Un script de Python (scripts/poblar\_db.py) se encarga de la Extracción, Transformación (limpieza, validación, imputación, estandarización de barrios) y Carga de los datos en una base de datos MySQL.  
  * **Base de Datos:** Se utiliza MySQL para almacenar los datos limpios y estructurados.  
  * **Backend:** La API está construida con FastAPI, siguiendo las mejores prácticas de la industria como la gestión de secretos con archivos .env y la validación de datos con Pydantic.

## **4\. Modelo de Machine Learning**

### **4.1 Objetivo del Modelo**
El modelo tiene como objetivo **predecir el precio en USD** de propiedades inmobiliarias en Capital Federal basándose en características estructuradas como ubicación, superficie y número de ambientes.

### **4.2 Metodología: Modelo Base (Baseline)**
Se adoptó una estrategia de **modelo base** como punto de partida, estableciendo un punto de referencia de rendimiento utilizando las características más simples y disponibles, antes de abordar complejidades mayores como el Procesamiento de Lenguaje Natural (NLP) sobre las descripciones textuales.

### **4.3 Preparación de Datos**
- **Dataset:** 50,248 registros de propiedades con datos limpios y validados
- **Características utilizadas:** barrio, ambientes, dormitorios, baños, superficie_total_m², cocheras
- **Preprocesamiento:** 
  - One-Hot Encoding para la variable categórica 'barrio' (52 features resultantes)
  - División 80/20 para entrenamiento y prueba
  - Validación de calidad de datos (eliminación de registros con precios o barrios nulos)

### **4.4 Modelo Seleccionado**
- **Algoritmo:** RandomForestRegressor (100 estimadores)
- **Justificación:** Modelo de conjunto robusto que maneja bien la variabilidad de los datos inmobiliarios
- **Parámetros:** n_estimators=100, random_state=42, n_jobs=-1

### **4.5 Resultados y Evaluación**

#### **Métricas de Rendimiento:**
- **R² (Coeficiente de Determinación): 0.8709** 
  - ✅ **Excelente resultado:** El modelo explica aproximadamente el **87% de la variabilidad** en los precios de las propiedades
  - ✅ **Interpretación:** Confirma que el modelo ha encontrado patrones sólidos y que las características seleccionadas son altamente relevantes

- **RMSE (Error Cuadrático Medio Raíz): $155,871.00 USD**
  - ⚠️ **Contexto importante:** Esta métrica refleja la alta varianza inherente en los datos inmobiliarios, donde coexisten propiedades de $50,000 con otras de varios millones
  - ✅ **Precisión en rango común:** El modelo es muy preciso en el rango de precios más frecuente, pero tiene dificultades con valores atípicos de lujo

#### **Análisis de Predicciones:**
- El modelo muestra un comportamiento consistente en el rango de precios más común ($100K - $500K)
- Las predicciones se alinean bien con los valores reales, como se observa en el análisis de dispersión
- La capacidad de generalización es sólida, indicando que el modelo puede manejar propiedades nuevas no vistas durante el entrenamiento

### **4.6 Decisiones Técnicas Clave**
- **No imputación de variable objetivo:** Se descartaron registros sin precio_usd para mantener la integridad del entrenamiento
- **Estrategia de codificación:** One-Hot Encoding para barrios mantiene la información categórica sin introducir orden artificial
- **Validación temporal:** Los datos se dividieron aleatoriamente para simular condiciones reales de predicción

### **4.7 Próximas Mejoras Planificadas**
- **Feature Engineering avanzado:** Incorporación de NLP en descripciones para extraer características como "luminoso", "balcón", "amenities"
- **Modelos avanzados:** Experimentación con XGBoost, LightGBM y técnicas de ensemble
- **Validación cruzada:** Implementación de k-fold CV para evaluación más robusta
- **Optimización de hiperparámetros:** GridSearch/RandomSearch para mejorar el rendimiento

## **5\. Cómo Ejecutar el Proyecto**

1. **Clonar el repositorio.**  
2. **Configurar el Entorno:** Crear un archivo .env en la raíz del proyecto con las credenciales de la base de datos (ver .env.example).  
3. **Instalar Dependencias:**  
   pip install \-r requirements.txt

4. **Poblar la Base de Datos:**  
   * Asegúrese de que la tabla propiedades esté creada y vacía.  
   * Ejecute el script de ETL: `python scripts/poblar_db.py`  
5. **Entrenar el Modelo de ML:**  
   * Ejecute el notebook de entrenamiento: `jupyter notebook notebooks/entrenamiento_modelo.ipynb`  
   * Esto generará los archivos `model.pkl` y `model_columns.pkl` en `src/ml/`
6. **Iniciar la API:**  
   `uvicorn src.api.main:app --reload`

7. **Acceder a la Documentación:** Navegue a http://127.0.0.1:8000/docs para interactuar con la API.

## **6\. Endpoints Principales**

### **Gestión de Propiedades**
- `GET /propiedades/` - Listar propiedades con filtros y paginación
- `GET /propiedades/{id}` - Obtener una propiedad específica
- `POST /propiedades/` - Crear una nueva propiedad
- `PUT /propiedades/{id}` - Actualizar una propiedad
- `DELETE /propiedades/{id}` - Eliminar una propiedad

### **Análisis y Estadísticas**
- `GET /estadisticas/precio-por-barrio/` - Estadísticas agregadas por barrio
- `GET /estadisticas/evolucion-mercado/` - Evolución temporal del mercado

### **Machine Learning**
- `POST /predict/` - **Predicción de precios en tiempo real**
  - **Input:** `{"barrio": "Palermo", "ambientes": 3, "dormitorios": 2, "banos": 2, "superficie_total_m2": 80, "cocheras": 1}`
  - **Output:** `{"predicted_price_usd": 245000.0}`

## **7\. Tecnologías Utilizadas**

### **Backend y API**
- **FastAPI** - Framework web moderno y rápido
- **Pydantic** - Validación de datos y serialización
- **MySQL** - Base de datos relacional
- **SQLAlchemy** - ORM para Python

### **Machine Learning**
- **Scikit-learn** - Biblioteca de ML
- **Pandas** - Manipulación de datos
- **NumPy** - Computación numérica
- **Pickle** - Serialización de modelos

### **Análisis y Visualización**
- **Jupyter Notebooks** - Análisis exploratorio
- **Matplotlib/Seaborn** - Visualizaciones
- **Pandas** - Análisis de datos

## **8\. Estructura del Proyecto**

```
api/
├── data/                          # Datos crudos
│   └── ventas_deptos.pkl
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
│       ├── model.pkl             # Modelo entrenado
│       ├── model_columns.pkl     # Columnas del modelo
│       ├── predict.py           # Función de predicción
│       └── README.md            # Documentación del modelo
├── requirements.txt              # Dependencias
└── README.md                     # Este archivo
```

## **9\. Estado del Proyecto y Próximos Pasos**

### **✅ Completado**
- [x] Análisis exploratorio de datos (EDA)
- [x] Pipeline ETL completo con limpieza de datos
- [x] API REST con CRUD completo
- [x] Modelo de ML baseline con RandomForest
- [x] Endpoint de predicción funcional
- [x] Documentación técnica completa

### **🚀 En Desarrollo**
- [ ] Feature engineering con NLP en descripciones
- [ ] Validación cruzada y métricas adicionales
- [ ] Optimización de hiperparámetros
- [ ] Testing automatizado

### **📋 Roadmap Futuro**
- [ ] Modelos avanzados (XGBoost, LightGBM)
- [ ] Dashboard interactivo con Streamlit
- [ ] Containerización con Docker
- [ ] CI/CD con GitHub Actions
- [ ] Análisis geográfico con mapas
- [ ] Sistema de monitoreo y logging

## **10\. Contribuciones y Contacto**

Este proyecto forma parte de mi portfolio personal como estudiante de programación orientado a **Ciencia de Datos e Inteligencia Artificial**.

**Tecnologías demostradas:**
- 🔧 **Ingeniería de Datos:** ETL, limpieza, validación
- 🤖 **Machine Learning:** Modelado, evaluación, despliegue
- 🌐 **Desarrollo Backend:** APIs REST, bases de datos
- 📊 **Análisis de Datos:** EDA, visualizaciones, insights

**Contacto:** joaquin99911@gmail.com

---

*Este proyecto demuestra un ciclo completo de ciencia de datos, desde el análisis exploratorio hasta el despliegue de un modelo de ML en producción, siguiendo las mejores prácticas de la industria.*