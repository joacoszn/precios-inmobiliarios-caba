# Modelo de Machine Learning

Documentación técnica completa del modelo de predicción de precios inmobiliarios.

## Objetivo del Modelo

El modelo tiene como objetivo **predecir el precio en USD** de propiedades inmobiliarias en Capital Federal basándose en características estructuradas como ubicación, superficie y número de ambientes.

## Metodología: Modelo Híbrido (Estructurado + NLP)

Se ha evolucionado desde un modelo base hacia un **modelo híbrido** que combina:
1.  **Datos Estructurados:** Características numéricas y categóricas tradicionales (superficie, ambientes, barrio).
2.  **Datos No Estructurados:** Características extraídas de las descripciones textuales de las propiedades mediante técnicas de NLP (palabras clave como 'balcón', 'luminoso', etc.).

Esta aproximación permite capturar matices y detalles valiosos que no están presentes en los datos estructurados, resultando en una predicción más precisa y contextualizada.

## Preparación de Datos

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
- **Feature Engineering (NLP):** Se utiliza `TfidfVectorizer` para convertir la columna `description` en un conjunto de 100 características numéricas que representan la importancia de las palabras en el texto. Este método es más robusto y captura más información que la simple búsqueda de keywords.
- **One-Hot Encoding:** Variable categórica 'barrio' → 51 features resultantes.
- **Composición Final:** 5 features numéricas + 51 de barrios + 100 de TF-IDF = **156 features totales**.
- **División de datos:** 80% entrenamiento, 20% prueba.
- **Validación de calidad:** Eliminación de registros con precios o barrios nulos.

## Modelo Seleccionado

### **Algoritmo: XGBoost (Extreme Gradient Boosting)**
- **Justificación:** Tras un proceso de búsqueda de hiperparámetros, `XGBoost` demostró un rendimiento superior al `RandomForest`, logrando un error de predicción significativamente menor. Es un algoritmo de boosting de gradiente conocido por su eficiencia y precisión.
- **Parámetros Optimizados:**
    - `n_estimators`: 300
    - `max_depth`: 7
    - `learning_rate`: 0.1
    - `subsample`: 1.0
    - `colsample_bytree`: 1.0

### **Ventajas del XGBoost**
- **Rendimiento Superior:** Generalmente considerado el estado del arte para datos tabulares.
- **Regularización:** Incluye regularización L1 y L2 para combatir el sobreajuste.
- **Flexibilidad:** Altamente personalizable a través de sus numerosos hiperparámetros.

## Resultados y Evaluación

Para obtener una medida fiable del rendimiento, se utilizó `RandomizedSearchCV` con validación cruzada de 5 pliegues para encontrar la mejor combinación de hiperparámetros. Las siguientes métricas reflejan el rendimiento del modelo `XGBoost` **optimizado**.

### **Métricas Promedio (k=5)**

#### **R² Promedio: 0.914 (± 0.035)**
- **Rendimiento del Modelo:** El modelo explica el **91.4% de la variabilidad** de los precios, una mejora significativa que demuestra el valor de la optimización de hiperparámetros.
- **Estabilidad:** La baja desviación estándar indica un comportamiento consistente del modelo.

#### **RMSE Promedio: $116,398 USD (± $22,376)**
- **Precisión del Modelo:** El error de predicción promedio se ha **reducido en casi $15,000 USD** en comparación con el modelo anterior sin optimizar, representando un avance sustancial en la precisión.
- **Consistencia:** La desviación estándar da una idea clara de la consistencia del modelo a través de los diferentes pliegues de la validación cruzada.

### **Análisis de Predicciones**
- **Comportamiento consistente** en el rango de precios más común
- **Alineación con valores reales** en análisis de dispersión
- **Capacidad de generalización** sólida para propiedades nuevas

## Análisis Avanzado de Predicciones

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

## Decisiones Técnicas Clave

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

### **Optimización de Hiperparámetros con RandomizedSearchCV**
- **Decisión:** Implementar un proceso de búsqueda de hiperparámetros utilizando `RandomizedSearchCV` para explorar sistemáticamente un amplio rango de configuraciones para `RandomForest` y `XGBoost`.
- **Justificación:** Los parámetros por defecto de un modelo raramente son los óptimos para un dataset específico. `RandomizedSearchCV` automatiza el proceso de encontrar una combinación de parámetros de alto rendimiento, mejorando significativamente la precisión del modelo final. Es un paso estándar en cualquier proyecto de machine learning serio.
- **Alternativa rechazada:** `GridSearchCV`, que prueba todas las combinaciones posibles y puede ser computacionalmente prohibitivo. `RandomizedSearchCV` es más eficiente para una primera fase de optimización.

### **Comparación de Modelos**

Tras la optimización de hiperparámetros, se realizó la comparación final entre el mejor `RandomForest` y el mejor `XGBoost`.

**Resultado del Experimento:**

El modelo **`XGBoost` optimizado** resultó ser el ganador, con un RMSE promedio de **$116,398 USD**, una mejora sustancial sobre el `RandomForest` optimizado.

Esto confirma la hipótesis de que `XGBoost`, aunque más complejo, tiene una capacidad predictiva superior cuando sus hiperparámetros se sintonizan correctamente para el dataset en cuestión. La elección de `XGBoost` es, por lo tanto, la decisión final basada en evidencia empírica.

### **Feature Engineering Avanzado**
- **NLP en descripciones:** Implementado (v2 - TF-IDF). Se reemplazó la búsqueda de keywords por una vectorización TF-IDF (`TfidfVectorizer`) que genera 100 features, capturando de forma más efectiva la información del texto.
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

## Interpretación de Resultados

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

## Enlaces Relacionados

- **[Referencia de API](referencia-api.md)** - Endpoints del modelo
- **[Visualizaciones](visualizaciones.md)** - Gráficos del modelo
- **[Ejemplos](ejemplos.md)** - Casos de uso prácticos
- **[Arquitectura](arquitectura.md)** - Diseño técnico
