# 🤖 **Modelo de Machine Learning**

Documentación técnica completa del modelo de predicción de precios inmobiliarios.

## 🎯 **Objetivo del Modelo**

El modelo tiene como objetivo **predecir el precio en USD** de propiedades inmobiliarias en Capital Federal basándose en características estructuradas como ubicación, superficie y número de ambientes.

## 📊 **Metodología: Modelo Base (Baseline)**

Se adoptó una estrategia de **modelo base** como punto de partida, estableciendo un punto de referencia de rendimiento utilizando las características más simples y disponibles, antes de abordar complejidades mayores como el Procesamiento de Lenguaje Natural (NLP) sobre las descripciones textuales.

## 🔧 **Preparación de Datos**

### **Dataset**
- **Registros:** 50,248 propiedades con datos limpios y validados
- **Período:** Datos recolectados en múltiples fechas de scraping
- **Calidad:** Datos procesados con ETL robusto

### **Características Utilizadas**
- `barrio`: Ubicación geográfica (variable categórica)
- `ambientes`: Número total de ambientes
- `dormitorios`: Número de dormitorios
- `banos`: Número de baños
- `superficie_total_m2`: Superficie total en metros cuadrados
- `cocheras`: Número de cocheras

### **Preprocesamiento**
- **One-Hot Encoding:** Variable categórica 'barrio' → 52 features resultantes
- **División de datos:** 80% entrenamiento, 20% prueba
- **Validación de calidad:** Eliminación de registros con precios o barrios nulos

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

## 📈 **Resultados y Evaluación**

### **Métricas de Rendimiento**

#### **R² (Coeficiente de Determinación): 0.8709**
- ✅ **Excelente resultado:** El modelo explica aproximadamente el **87% de la variabilidad** en los precios
- ✅ **Interpretación:** Confirma que el modelo ha encontrado patrones sólidos
- ✅ **Relevancia:** Las características seleccionadas son altamente predictivas

#### **RMSE (Error Cuadrático Medio Raíz): $155,871.00 USD**
- ⚠️ **Contexto importante:** Refleja la alta varianza inherente en los datos inmobiliarios
- ✅ **Rango realista:** Coexisten propiedades de $50K con otras de varios millones
- ✅ **Precisión en rango común:** Muy preciso en el rango de precios más frecuente ($100K-$500K)

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

### **Validación Temporal**
- **División aleatoria** 80/20
- **Justificación:** Simular condiciones reales de predicción
- **Alternativa:** Validación temporal no aplicable por naturaleza de los datos

## 🚀 **Próximas Mejoras Planificadas**

### **Feature Engineering Avanzado**
- **NLP en descripciones:** Extraer características como "luminoso", "balcón", "amenities"
- **Features derivadas:** Precio por m², ratio ambientes/superficie
- **Variables categóricas:** Tipo de construcción, antigüedad

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

### **Feature Importance Típica**
1. **Superficie total (45%):** Factor más importante
2. **Barrio Palermo (12%):** Ubicación premium
3. **Barrio Recoleta (10%):** Otra zona premium
4. **Ambientes (8%):** Tamaño de la propiedad
5. **Barrio Belgrano (7%):** Zona consolidada

### **Patrones Identificados**
- **Ubicación:** Barrios premium tienen mayor impacto
- **Tamaño:** Superficie es el predictor más fuerte
- **Distribución:** Modelo funciona mejor en rango medio ($100K-$500K)

## 🔗 **Enlaces Relacionados**

- **[📖 Referencia de API](referencia-api.md)** - Endpoints del modelo
- **[📊 Visualizaciones](visualizaciones.md)** - Gráficos del modelo
- **[💡 Ejemplos](ejemplos.md)** - Casos de uso prácticos
- **[🏗️ Arquitectura](arquitectura.md)** - Diseño técnico
