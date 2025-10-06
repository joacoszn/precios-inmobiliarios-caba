# 📊 **Visualizaciones y Análisis Estadísticos**

Esta sección contiene visualizaciones interactivas y análisis estadísticos del mercado inmobiliario de CABA.

## 🎯 **Objetivo de las Visualizaciones**

Las visualizaciones proporcionan insights visuales sobre:
- **Distribución de precios** por barrio y características
- **Tendencias temporales** del mercado
- **Rendimiento del modelo** de Machine Learning
- **Análisis comparativo** entre diferentes zonas

## 📈 **Dashboard de Estadísticas**

### **1. Precio Promedio por Barrio**

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_precio_por_barrio():
    """Gráfico de barras: Precio promedio por barrio"""
    # Obtener datos desde la API
    response = requests.get("http://127.0.0.1:8000/estadisticas/precio-por-barrio/")
    data = response.json()
    
    df = pd.DataFrame(data)
    df = df.sort_values('precio_promedio_usd', ascending=True)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(data=df, y='barrio', x='precio_promedio_usd')
    plt.title('Precio Promedio por Barrio (USD)', fontsize=16)
    plt.xlabel('Precio Promedio (USD)', fontsize=12)
    plt.ylabel('Barrio', fontsize=12)
    plt.tight_layout()
    plt.show()
```

### **2. Distribución de Precios vs Superficie**

```python
def plot_precio_vs_superficie():
    """Scatter plot: Precio vs Superficie con colores por barrio"""
    # Obtener datos de propiedades
    response = requests.get("http://127.0.0.1:8000/propiedades/?limit=1000")
    data = response.json()
    
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='superficie_total_m2', y='price_usd', 
                   hue='barrio', alpha=0.6)
    plt.title('Precio vs Superficie por Barrio', fontsize=16)
    plt.xlabel('Superficie Total (m²)', fontsize=12)
    plt.ylabel('Precio (USD)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
```

### **3. Heatmap de Distribución por Barrio y Precio**

```python
def plot_heatmap_barrio_precio():
    """Heatmap: Distribución de propiedades por barrio y rango de precio"""
    response = requests.get("http://127.0.0.1:8000/propiedades/?limit=2000")
    data = response.json()
    
    df = pd.DataFrame(data)
    
    # Crear bins de precio
    df['precio_bin'] = pd.cut(df['price_usd'], 
                             bins=[0, 100000, 200000, 300000, 500000, float('inf')],
                             labels=['<100K', '100K-200K', '200K-300K', '300K-500K', '>500K'])
    
    # Crear tabla de contingencia
    heatmap_data = pd.crosstab(df['barrio'], df['precio_bin'])
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd')
    plt.title('Distribución de Propiedades por Barrio y Rango de Precio', fontsize=16)
    plt.xlabel('Rango de Precio (USD)', fontsize=12)
    plt.ylabel('Barrio', fontsize=12)
    plt.tight_layout()
    plt.show()
```

## 🤖 **Análisis del Modelo de ML**

### **4. Feature Importance**

```python
def plot_feature_importance():
    """Gráfico de barras: Importancia de características"""
    response = requests.get("http://127.0.0.1:8000/predict/model-info")
    data = response.json()
    
    features = [f['feature'] for f in data['top_features']]
    importance = [f['importance'] for f in data['top_features']]
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x=importance, y=features)
    plt.title('Feature Importance - Top 10 Características', fontsize=16)
    plt.xlabel('Importancia', fontsize=12)
    plt.ylabel('Característica', fontsize=12)
    plt.tight_layout()
    plt.show()
```

### **5. Predicciones vs Valores Reales**

```python
def plot_predicciones_vs_reales():
    """Scatter plot: Predicciones del modelo vs valores reales"""
    # Generar predicciones para un conjunto de datos de prueba
    test_data = [
        {"barrio": "Palermo", "ambientes": 3, "dormitorios": 2, "banos": 2, 
         "superficie_total_m2": 80, "cocheras": 1},
        {"barrio": "Recoleta", "ambientes": 4, "dormitorios": 3, "banos": 2, 
         "superficie_total_m2": 120, "cocheras": 2},
        # ... más datos de prueba
    ]
    
    predicciones = []
    valores_reales = []  # Obtener desde base de datos
    
    for data in test_data:
        response = requests.post("http://127.0.0.1:8000/predict/", json=data)
        pred = response.json()['predicted_price_usd']
        predicciones.append(pred)
    
    plt.figure(figsize=(10, 10))
    plt.scatter(valores_reales, predicciones, alpha=0.6)
    
    # Línea de predicción perfecta
    min_val = min(min(valores_reales), min(predicciones))
    max_val = max(max(valores_reales), max(predicciones))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
    
    plt.title('Predicciones vs Valores Reales', fontsize=16)
    plt.xlabel('Precio Real (USD)', fontsize=12)
    plt.ylabel('Precio Predicho (USD)', fontsize=12)
    plt.axis('equal')
    plt.grid(True)
    plt.show()
```

## 📊 **Análisis Temporal**

### **6. Evolución de Precios por Fecha**

```python
def plot_evolucion_precios():
    """Gráfico de línea: Evolución de precios promedio por fecha"""
    response = requests.get("http://127.0.0.1:8000/estadisticas/evolucion-mercado/")
    data = response.json()
    
    df = pd.DataFrame(data)
    df['fecha_scraping'] = pd.to_datetime(df['fecha_scraping'])
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['fecha_scraping'], df['precio_promedio_usd'], marker='o', linewidth=2)
    plt.title('Evolución del Precio Promedio del Mercado', fontsize=16)
    plt.xlabel('Fecha de Scraping', fontsize=12)
    plt.ylabel('Precio Promedio (USD)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
```

### **7. Cantidad de Propiedades por Fecha**

```python
def plot_cantidad_propiedades():
    """Gráfico de barras: Cantidad de propiedades por fecha de scraping"""
    response = requests.get("http://127.0.0.1:8000/estadisticas/evolucion-mercado/")
    data = response.json()
    
    df = pd.DataFrame(data)
    df['fecha_scraping'] = pd.to_datetime(df['fecha_scraping'])
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='fecha_scraping', y='cantidad_propiedades')
    plt.title('Cantidad de Propiedades por Fecha de Scraping', fontsize=16)
    plt.xlabel('Fecha de Scraping', fontsize=12)
    plt.ylabel('Cantidad de Propiedades', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
```

## 🏘️ **Análisis Geográfico**

### **8. Precio por Metro Cuadrado por Barrio**

```python
def plot_precio_m2_por_barrio():
    """Gráfico de barras: Precio promedio por m² por barrio"""
    response = requests.get("http://127.0.0.1:8000/estadisticas/precio-por-barrio/")
    data = response.json()
    
    df = pd.DataFrame(data)
    df = df.sort_values('precio_promedio_m2_usd', ascending=True)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(data=df, y='barrio', x='precio_promedio_m2_usd')
    plt.title('Precio Promedio por m² por Barrio', fontsize=16)
    plt.xlabel('Precio por m² (USD)', fontsize=12)
    plt.ylabel('Barrio', fontsize=12)
    plt.tight_layout()
    plt.show()
```

## 📊 **Dashboard Interactivo con Streamlit**

### **9. Dashboard Completo**

```python
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_dashboard():
    """Dashboard interactivo con Streamlit"""
    st.title("🏠 Dashboard de Análisis Inmobiliario CABA")
    
    # Sidebar para filtros
    st.sidebar.header("Filtros")
    barrio_selected = st.sidebar.selectbox("Seleccionar Barrio", ["Todos"] + get_barrios())
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Propiedades", get_total_propiedades())
    
    with col2:
        st.metric("Precio Promedio", f"${get_precio_promedio():,.0f}")
    
    with col3:
        st.metric("R² del Modelo", "0.8709")
    
    with col4:
        st.metric("RMSE", f"${155871:,.0f}")
    
    # Gráficos
    st.subheader("📊 Análisis de Precios")
    
    # Precio por barrio
    fig_barrio = px.bar(get_data_precio_barrio(), 
                       x='precio_promedio_usd', 
                       y='barrio',
                       title='Precio Promedio por Barrio')
    st.plotly_chart(fig_barrio, use_container_width=True)
    
    # Distribución de precios
    fig_dist = px.histogram(get_data_propiedades(), 
                           x='price_usd',
                           title='Distribución de Precios',
                           nbins=50)
    st.plotly_chart(fig_dist, use_container_width=True)
    
    # Feature importance
    st.subheader("🤖 Análisis del Modelo")
    fig_importance = px.bar(get_feature_importance(), 
                           x='importance', 
                           y='feature',
                           title='Feature Importance')
    st.plotly_chart(fig_importance, use_container_width=True)

if __name__ == "__main__":
    create_dashboard()
```

## 🚀 **Cómo Ejecutar las Visualizaciones**

### **1. Instalar Dependencias Adicionales**
```bash
pip install matplotlib seaborn plotly streamlit
```

### **2. Ejecutar Scripts Individuales**
```bash
python scripts/visualizaciones.py
```

### **3. Dashboard Interactivo**
```bash
streamlit run dashboard.py
```

## 📈 **Insights Generados**

### **Patrones Identificados**
- **Barrios Premium:** Palermo, Recoleta, Puerto Madero tienen precios más altos
- **Relación Lineal:** Precio vs Superficie muestra correlación fuerte
- **Estacionalidad:** Variaciones en cantidad de propiedades por período
- **Concentración:** 60% de propiedades en top 5 barrios

### **Recomendaciones del Modelo**
- **Superficie:** Factor más importante para predicción
- **Ubicación:** Barrios premium tienen mayor impacto
- **Confianza:** Intervalos más amplios en propiedades de lujo

## 🔗 **Enlaces Relacionados**

- **[🤖 Modelo de ML](modelo-ml.md)** - Detalles técnicos del modelo
- **[📖 Referencia de API](referencia-api.md)** - Endpoints para obtener datos
- **[💡 Ejemplos](ejemplos.md)** - Casos de uso prácticos
- **[🏗️ Arquitectura](arquitectura.md)** - Diseño del sistema
