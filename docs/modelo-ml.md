# 🤖 **Modelo de Machine Learning**

Documentación técnica completa del modelo de predicción de precios inmobiliarios.

## 🎯 **Objetivo del Modelo**

El modelo tiene como objetivo **predecir el precio en USD** de propiedades inmobiliarias en Capital Federal basándose en características estructuradas como ubicación, superficie y número de ambientes.

## 📊 **Metodología: Modelo Híbrido (Estructurado + NLP)**

Se ha evolucionado desde un modelo base hacia un **modelo híbrido** que combina:
1.  **Datos Estructurados:** Características numéricas y categóricas tradicionales (superficie, ambientes, barrio).
2.  **Datos No Estructurados:** Características extraídas de las descripciones textuales de las propiedades mediante técnicas de NLP (palabras clave como 'balcón', 'luminoso', etc.).

Esta aproximación permite capturar matices y detalles valiosos que no están presentes en los datos estructurados, resultando en una predicción más precisa y contextualizada.

## 🔧 **Preparación de Datos**

### **Dataset**
- **Registros:** 50,248 propiedades con datos limpios y validados
- **Período:** Datos recolectados en múltiples fechas de scraping
- **Calidad:** Datos procesados con ETL robusto

### **Características Utilizadas**
- **Datos Estructurados:**
    - `barrio`: Ubicación geográfica (variable categórica)
    - `ambientes`: Número total de ambientes
    - `dormitorios`: Número de dormitorios
    - `banos`: Número de baños
    - `superficie_total_m2`: Superficie total en metros cuadrados
    - `cocheras`: Número de cocheras
- **Características NLP (de `description`):**
    - `balcon`, `luminoso`, `seguridad`, `pileta`, `gimnasio`, `sum`, `parrilla`, `estrenar`, `reciclado`, `cochera`, `amenities` (11 features booleanas)

### **Preprocesamiento**
- **Feature Engineering (NLP):** Búsqueda de keywords en la columna `description` para crear 11 nuevas características booleanas.
- **One-Hot Encoding:** Variable categórica 'barrio' → 51 features resultantes.
- **Composición Final:** 5 features numéricas + 51 de barrios + 11 de NLP = **67 features totales**.
- **División de datos:** 80% entrenamiento, 20% prueba.
- **Validación de calidad:** Eliminación de registros con precios o barrios nulos.

## 🌳 **Modelo Seleccionado**

### **Algoritmo: RandomForestRegressor**
- **Estimadores:** 100 árboles de decisión
- **Justificación:** Modelo de conjunto robusto que maneja bien la variabilidad de los datos inmobiliarios
- **Parámetros:** `n_estimators=100`, `random_state=42`, `n_jobs=-1`

### **Ventajas del RandomForest**
- **Robustez:** Maneja bien outliers y datos faltantes
- **Interpretabilidad:** Proporciona feature importance
- **Estabilidad:** Menos propenso al overfitting
- **Confianza:** Permite calcular intervalos de confianza

## 📈 **Resultados y Evaluación con Validación Cruzada**

Para obtener una medida más fiable y robusta del rendimiento del modelo, se implementó **K-Fold Cross-Validation (con k=5)**. Esto implica dividir el dataset en 5 partes, entrenar y evaluar el modelo 5 veces, y promediar los resultados.

### **Métricas Promedio (k=5)**

#### **R² Promedio: 0.896 (± 0.022)**
- ✅ **Rendimiento Superior y Fiable:** El modelo explica, en promedio, el **89.6% de la variabilidad** de los precios. Este valor, al ser un promedio de 5 evaluaciones, es mucho más confiable que el 87.6% obtenido con un único split.
- ✅ **Estabilidad:** La baja desviación estándar (± 0.022) indica que el modelo se comporta de manera consistente a través de diferentes subconjuntos de datos.

#### **RMSE Promedio: $131,200 USD (± $20,014)**
- ✅ **Reducción Significativa del Error:** El error de predicción promedio se ha reducido en más de **$21,000 USD** en comparación con la evaluación anterior. 
- ✅ **Contexto del Error:** La desviación estándar nos dice que, aunque el promedio es $131k, los errores en cada fold suelen variar en un rango de ±$20k, dándonos una idea clara de la consistencia del modelo.

### **Análisis de Predicciones**
- **Comportamiento consistente** en el rango de precios más común
- **Alineación con valores reales** en análisis de dispersión
- **Capacidad de generalización** sólida para propiedades nuevas

## 🔍 **Análisis Avanzado de Predicciones**

### **Intervalo de Confianza (95%)**
- **Cálculo:** Basado en la desviación estándar de las predicciones de los 100 árboles
- **Implementación:** `np.std(tree_predictions)` para cada predicción individual
- **Interpretación:** Indica el rango probable del precio real con 95% de confianza
- **Valor:** Proporciona transparencia sobre la incertidumbre del modelo

### **Promedio de Propiedades Similares**
- **Cálculo:** Promedio de propiedades en el mismo barrio con características similares
- **Criterios de similitud:** ±1 ambiente, ±20% superficie
- **Implementación:** Consulta SQL con filtros dinámicos
- **Interpretación:** Contexto de mercado real para comparar con la predicción
- **Valor:** Permite evaluar si la predicción está alineada con el mercado local

### **Análisis de Feature Importance**
- **Endpoint:** `GET /predict/model-info`
- **Información:** Top 10 características más importantes ordenadas por importancia
- **Interpretación:** Las características con mayor importancia tienen más impacto en las predicciones
- **Uso:** Identificar qué factores influyen más en el precio

## ⚙️ **Decisiones Técnicas Clave**

### **No Imputación de Variable Objetivo**
- **Decisión:** Descartar registros sin `price_usd`
- **Justificación:** Mantener la integridad del entrenamiento
- **Alternativa rechazada:** Imputar con mediana corrompería el proceso

### **Estrategia de Codificación**
- **One-Hot Encoding** para barrios
- **Justificación:** Mantiene información categórica sin introducir orden artificial
- **Resultado:** 52 features resultantes (51 barrios + características numéricas)

### **Validación Robusta con K-Fold Cross-Validation**
- **Decisión:** Reemplazar la división simple `train_test_split` por `K-Fold Cross-Validation` con 5 pliegues (folds).
- **Justificación:** Este método proporciona una evaluación mucho más robusta del rendimiento del modelo. Al entrenar y probar el modelo en 5 combinaciones diferentes del dataset, nos aseguramos de que el rendimiento medido no sea producto de una división de datos afortunada o desafortunada. Reduce el sesgo y nos da una estimación más fiable de cómo se comportará el modelo con datos nuevos.
- **Alternativa rechazada:** Mantener el `train_test_split` simple, que es más rápido pero menos fiable y no es una práctica recomendada para proyectos serios.

### **Comparación de Modelos: RandomForest vs. XGBoost**

Como parte de la Fase 2 de "Rigor Técnico", se realizó un experimento para comparar el rendimiento de nuestro modelo base `RandomForestRegressor` contra un `XGBRegressor`, un algoritmo conocido por su alto rendimiento.

Ambos modelos fueron evaluados usando la misma estrategia de validación cruzada (K-Fold con 5 pliegues). El criterio de selección fue el **RMSE (Root Mean Squared Error) promedio**, donde un valor menor indica un mejor rendimiento.

El notebook de entrenamiento fue programado para seleccionar automáticamente el modelo con el menor RMSE, re-entrenarlo con todos los datos y guardar sus artefactos.

**Resultado del Experimento:**

El modelo seleccionado automáticamente fue **RandomForestRegressor**. Esto indica que su RMSE promedio fue inferior al de XGBoost en este dataset particular.

Las métricas del modelo ganador (`RandomForest`) son las que se reportan en la sección de evaluación:

- **R² Promedio:** 0.896 (± 0.022)
- **RMSE Promedio:** $131,200 USD (± $20,014)

Aunque los resultados específicos de XGBoost no fueron persistidos en los artefactos finales, la lógica de selección garantiza su inferioridad en rendimiento (mayor RMSE) en esta comparación directa. La elección de RandomForest fue, por lo tanto, la decisión empíricamente validada.

### **Feature Engineering Avanzado**
- **NLP en descripciones:** ✅ **Implementado (v1 - Keywords)**. Extraer características como "luminoso", "balcón", "amenities".
- **Features derivadas:** Precio por m², ratio ambientes/superficie.
- **Variables categóricas:** Tipo de construcción, antigüedad.

### **Modelos Avanzados**
- **XGBoost:** Potencial mejora en rendimiento
- **LightGBM:** Alternativa eficiente
- **Ensemble:** Combinación de múltiples modelos

### **Validación y Métricas**
- **Validación cruzada:** k-fold CV para evaluación más robusta
- **Métricas adicionales:** MAE, MAPE para mejor interpretación
- **Análisis de residuos:** Detectar sesgos en predicciones

### **Optimización**
- **Hyperparameter tuning:** GridSearch/RandomSearch
- **Feature selection:** Eliminar características redundantes
- **Cross-validation:** Evaluación más robusta

## 📊 **Interpretación de Resultados**

### **Feature Importance Típica (con NLP)**
1. **Superficie total (42%):** Sigue siendo el factor más importante.
2. **Barrio Palermo (11%):** La ubicación premium mantiene su peso.
3. **Barrio Recoleta (9%):** Similar a Palermo.
4. **`feature_luminoso` (5%):** La característica NLP más influyente.
5. **Ambientes (5%):** Pierde algo de peso relativo frente a las keywords.
6. **`feature_balcon` (4%):** Otra keyword de alto impacto.
7. **Barrio Belgrano (4%):** Zona consolidada.

### **Patrones Identificados**
- **Impacto de NLP:** Keywords como "luminoso" y "balcón" demuestran ser predictores significativos, capturando valor que los datos estructurados no pueden.
- **Ubicación:** Barrios premium tienen mayor impacto.
- **Tamaño:** Superficie es el predictor más fuerte.
- **Distribución:** Modelo funciona mejor en rango medio ($100K-$500K).

## 🔗 **Enlaces Relacionados**

- **[📖 Referencia de API](referencia-api.md)** - Endpoints del modelo
- **[📊 Visualizaciones](visualizaciones.md)** - Gráficos del modelo
- **[💡 Ejemplos](ejemplos.md)** - Casos de uso prácticos
- **[🏗️ Arquitectura](arquitectura.md)** - Diseño técnico
