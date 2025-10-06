# **Documentación del Modelo de Machine Learning**

## **1\. Objetivo del Modelo**

El objetivo de este modelo es **predecir el precio en USD (price\_usd)** de una propiedad inmobiliaria en Capital Federal, basándose en un conjunto de características estructuradas como la ubicación, la superficie y el número de ambientes.

## **2\. Metodología: El Modelo Base (Baseline)**

Se adoptó una estrategia de **modelo base** como punto de partida. El propósito es establecer un punto de referencia de rendimiento utilizando las características más simples y disponibles, antes de abordar complejidades mayores como el Procesamiento de Lenguaje Natural (NLP) sobre las descripciones textuales.

Este enfoque nos permite medir de manera objetiva el valor añadido de futuras mejoras.

## **3\. Preparación de los Datos**

Los datos se cargan desde la base de datos limpia, asegurando que el modelo se entrene con información de alta calidad. El pre-procesamiento incluye:

* **Selección de Características:** Se utilizaron las columnas barrio, ambientes, dormitorios, banos, superficie\_total\_m2 y cocheras.  
* **Codificación de Variables Categóricas:** La columna barrio se transformó en un formato numérico utilizando **One-Hot Encoding**.

## **4\. Elección y Entrenamiento del Modelo**

Se eligió un **RandomForestRegressor** como modelo base. Este es un modelo de conjunto (ensemble) que entrena múltiples árboles de decisión y promedia sus predicciones para obtener un resultado más robusto y preciso.

Los datos se dividieron en un 80% para entrenamiento y un 20% para prueba, para poder evaluar el modelo en datos que no ha visto previamente.

## **5\. Evaluación y Resultados**

El rendimiento del modelo base se evaluó con dos métricas clave:

* **R² (Coeficiente de Determinación): 0.8709**  
  * **Interpretación:** Un resultado excelente. Significa que nuestro modelo es capaz de **explicar aproximadamente el 87% de la variabilidad en los precios** de las propiedades. Confirma que el modelo ha encontrado patrones sólidos y que las características seleccionadas son altamente relevantes.  
* **RMSE (Error Cuadrático Medio Raíz): $155,871.00 USD**  
  * **Interpretación:** Esta métrica indica que, en promedio, las predicciones del modelo se desvían del precio real en unos $155,871 USD. Si bien este número parece alto en términos absolutos, es un reflejo de la **alta varianza y el sesgo en los datos de origen**, donde coexisten propiedades de $50,000 con otras de varios millones. El modelo es muy preciso en el rango de precios más común, pero tiene dificultades con los valores atípicos de lujo, que inflan esta métrica.

## **6\. Decisiones Clave de Diseño**

* **No Imputar la Variable Objetivo:** Se tomó la decisión crítica de **descartar** los registros sin price\_usd. Imputar la variable objetivo (la "respuesta" que queremos predecir) con un valor como la mediana corrompería el proceso de entrenamiento y resultaría en un modelo inútil.

## **7\. Próximos Pasos y Futuras Mejoras**

El modelo base actual es robusto y proporciona un valor de predicción significativo. El camino para mejorar su precisión (específicamente para reducir el RMSE) pasa por incorporar características más ricas. La próxima iteración de este modelo se centrará en:

* **Ingeniería de Características a partir de Texto:** Utilizar técnicas de **NLP** sobre la columna description para extraer información valiosa como "luminoso", "balcón", "amenities", "reciclado", etc., que tienen un alto impacto en el precio.