# **preciosCABA: API de Análisis y Predicción de Precios sobre el mercado inmobiliario en la Ciudad de Buenos Aires.**

## 

## **1\. Propósito del Proyecto**

Este proyecto es un caso de estudio de ciclo completo (end-to-end) diseñado para demostrar habilidades en **Análisis y Ingeniería de Datos, Desarrollo de Backend y Machine Learning**. El objetivo es procesar un dataset crudo de propiedades inmobiliarias en la Ciudad de Buenos Aires, almacenarlo en una base de datos limpia y exponerlo a través de una API RESTful que no solo sirve los datos, sino que también ofrece insights analíticos y predicciones de precios.

## **2\. Características Principales de la API**

La API, construida con **FastAPI**, ofrece las siguientes funcionalidades:

* **Gestión de Datos (CRUD):** Endpoints para Crear (POST), Leer (GET), Actualizar (PUT) y Eliminar (DELETE) registros de propiedades.  
* **Consultas Avanzadas:** Endpoint de listado con capacidades de **filtrado** por múltiples criterios (barrio, ambientes, precio) y **paginación**.  
* **Insights Analíticos:**  
  * GET /estadisticas/precio-por-barrio/: Devuelve estadísticas agregadas (conteo, precio promedio, min/max y **precio promedio por m²**) para cada barrio.  
  * GET /estadisticas/evolucion-mercado/: Analiza la evolución de precios y la cantidad de listados a través de las diferentes fechas de recolección de datos.  
* **Predicción de Precios (Próximamente):** Un endpoint para predecir el precio de una propiedad basándose en sus características.

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

## **4\. Cómo Ejecutar el Proyecto**

1. **Clonar el repositorio.**  
2. **Configurar el Entorno:** Crear un archivo .env en la raíz del proyecto con las credenciales de la base de datos (ver .env.example).  
3. **Instalar Dependencias:**  
   pip install \-r requirements.txt

4. **Poblar la Base de Datos:**  
   * Asegúrese de que la tabla propiedades esté creada y vacía.  
   * Ejecute el script de ETL: python scripts/poblar\_db.py  
5. **Iniciar la API:**  
   uvicorn src.api.main:app \--reload

6. **Acceder a la Documentación:** Navegue a http://12-7.0.0.1:8000/docs para interactuar con la API.