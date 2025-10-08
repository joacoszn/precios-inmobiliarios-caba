# **Ejemplos y Casos de Uso**

Esta sección contiene ejemplos prácticos de cómo usar la API de análisis inmobiliario para diferentes casos de uso.

## **Casos de Uso Principales**

### **1. Análisis de Mercado para Inversores**
### **2. Evaluación de Propiedades para Compradores**
### **3. Pricing para Vendedores**
### **4. Análisis Comparativo de Barrios**
### **5. Investigación de Tendencias del Mercado**

## **Caso de Uso 1: Análisis de Mercado para Inversores**

### **Escenario**
Un inversor quiere analizar el mercado inmobiliario de CABA para identificar oportunidades de inversión.

### **Pasos del Análisis**

#### **1. Obtener Estadísticas por Barrio**
```bash
curl "http://127.0.0.1:8000/estadisticas/precio-por-barrio/" | jq
```

**Respuesta:**
```json
[
  {
    "barrio": "Puerto Madero",
    "cantidad_propiedades": 45,
    "precio_promedio_usd": 450000.0,
    "precio_min_usd": 300000.0,
    "precio_max_usd": 800000.0,
    "precio_promedio_m2_usd": 5625.0
  },
  {
    "barrio": "Palermo",
    "cantidad_propiedades": 1250,
    "precio_promedio_usd": 185000.0,
    "precio_min_usd": 120000.0,
    "precio_max_usd": 450000.0,
    "precio_promedio_m2_usd": 2312.5
  }
]
```

#### **2. Analizar Evolución Temporal**
```bash
curl "http://127.0.0.1:8000/estadisticas/evolucion-mercado/" | jq
```

#### **3. Identificar Propiedades de Interés**
```bash
curl "http://127.0.0.1:8000/propiedades/?barrio=Palermo&ambientes_min=3&price_max_usd=200000" | jq
```

### **Insights del Análisis**
- **Puerto Madero:** Mercado premium, pocas propiedades, alto precio por m²
- **Palermo:** Mercado consolidado, muchas opciones, precio medio-alto
- **Oportunidad:** Propiedades en Palermo con 3+ ambientes bajo $200K

## 🏡 **Caso de Uso 2: Evaluación de Propiedades para Compradores**

### **Escenario**
Un comprador encuentra una propiedad en Recoleta y quiere evaluar si el precio es justo.

### **Propiedad a Evaluar**
- **Barrio:** Recoleta
- **Ambientes:** 4
- **Dormitorios:** 3
- **Baños:** 2
- **Superficie:** 120 m²
- **Cocheras:** 1
- **Precio solicitado:** $280,000

### **Análisis con la API**

#### **1. Predicción del Modelo**
```bash
curl -X POST "http://127.0.0.1:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "barrio": "Recoleta",
    "ambientes": 4,
    "dormitorios": 3,
    "banos": 2,
    "superficie_total_m2": 120,
    "cocheras": 1,
    "description": "Espectacular piso en Recoleta, muy luminoso y con balcón."
  }' | jq
```

**Respuesta:**
```json
{
  "predicted_price_usd": 275000.0,
  "confidence_interval": {
    "lower": 250000.0,
    "upper": 300000.0
  },
  "similar_properties_avg": 268000.0
}
```

#### **2. Análisis de Propiedades Similares**
```bash
curl "http://127.0.0.1:8000/propiedades/?barrio=Recoleta&ambientes_min=3&ambientes_max=5&superficie_total_m2_min=100&superficie_total_m2_max=140" | jq
```

### **Conclusión del Análisis**
- **Precio solicitado:** $280,000
- **Predicción del modelo:** $275,000
- **Promedio de similares:** $268,000
- **Rango de confianza:** $250,000 - $300,000

**Recomendación:** El precio está dentro del rango esperado, ligeramente por encima del promedio pero justificado por la ubicación premium.

## **Caso de Uso 3: Pricing para Vendedores**

### **Escenario**
Un vendedor quiere determinar el precio óptimo para su propiedad en Belgrano.

### **Propiedad a Vender**
- **Barrio:** Belgrano
- **Ambientes:** 3
- **Dormitorios:** 2
- **Baños:** 2
- **Superficie:** 85 m²
- **Cocheras:** 1

### **Análisis de Pricing**

#### **1. Predicción del Modelo**
```bash
curl -X POST "http://127.0.0.1:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "barrio": "Belgrano",
    "ambientes": 3,
    "dormitorios": 2,
    "banos": 2,
    "superficie_total_m2": 85,
    "cocheras": 1,
    "description": "Departamento con excelente distribución y amenities. Pileta y SUM."
  }' | jq
```

**Respuesta:**
```json
{
  "predicted_price_usd": 165000.0,
  "confidence_interval": {
    "lower": 150000.0,
    "upper": 180000.0
  },
  "similar_properties_avg": 162000.0
}
```

#### **2. Análisis de Competencia**
```bash
curl "http://127.0.0.1:8000/propiedades/?barrio=Belgrano&ambientes=3&superficie_total_m2_min=80&superficie_total_m2_max=90" | jq
```

### **Estrategia de Pricing**
- **Precio base (modelo):** $165,000
- **Rango de confianza:** $150,000 - $180,000
- **Promedio de similares:** $162,000
- **Precio recomendado:** $165,000 - $170,000 (centro del rango de confianza)

## **Caso de Uso 4: Análisis Comparativo de Barrios**

### **Escenario**
Un usuario quiere comparar diferentes barrios para decidir dónde comprar.

### **Barrios a Comparar**
- Palermo
- Recoleta
- Belgrano
- Caballito

### **Análisis Comparativo**

#### **1. Estadísticas de Cada Barrio**
```bash
# Palermo
curl "http://127.0.0.1:8000/estadisticas/precio-por-barrio/" | jq '.[] | select(.barrio == "Palermo")'

# Recoleta
curl "http://127.0.0.1:8000/estadisticas/precio-por-barrio/" | jq '.[] | select(.barrio == "Recoleta")'

# Belgrano
curl "http://127.0.0.1:8000/estadisticas/precio-por-barrio/" | jq '.[] | select(.barrio == "Belgrano")'

# Caballito
curl "http://127.0.0.1:8000/estadisticas/precio-por-barrio/" | jq '.[] | select(.barrio == "Caballito")'
```

#### **2. Predicción para Propiedad Estándar**
```bash
# Propiedad estándar: 3 ambientes, 2 dormitorios, 2 baños, 80 m², 1 cochera

for barrio in Palermo Recoleta Belgrano Caballito; do
  echo "=== $barrio ==="
  curl -X POST "http://127.0.0.1:8000/predict/" \
    -H "Content-Type: application/json" \
    -d "{
      \"barrio\": \"$barrio\",
      \"ambientes\": 3,
      \"dormitorios\": 2,
      \"banos\": 2,
      \"superficie_total_m2\": 80,
      \"cocheras\": 1,
      \"description\": \"Departamento estándar, luminoso y con balcón."
    }" | jq '.predicted_price_usd'
done
```

### **Tabla Comparativa**

| Barrio | Precio Promedio | Precio Predicho | Precio/m² | Cantidad Propiedades |
|--------|----------------|-----------------|-----------|---------------------|
| Recoleta | $220,000 | $195,000 | $2,750 | 450 |
| Palermo | $185,000 | $175,000 | $2,312 | 1,250 |
| Belgrano | $165,000 | $155,000 | $2,062 | 800 |
| Caballito | $140,000 | $135,000 | $1,750 | 600 |

### **Recomendaciones**
- **Mejor relación precio/calidad:** Caballito
- **Mayor liquidez:** Palermo (más propiedades)
- **Premium:** Recoleta (mayor precio)
- **Equilibrio:** Belgrano (precio medio, buena ubicación)

## **Caso de Uso 5: Investigación de Tendencias del Mercado**

### **Escenario**
Un analista quiere investigar las tendencias del mercado inmobiliario.

### **Análisis Temporal**

#### **1. Evolución de Precios**
```bash
curl "http://127.0.0.1:8000/estadisticas/evolucion-mercado/" | jq
```

**Respuesta:**
```json
[
  {
    "fecha_scraping": "2024-01-15T00:00:00",
    "cantidad_propiedades": 12500,
    "precio_promedio_usd": 175000.0
  },
  {
    "fecha_scraping": "2024-02-15T00:00:00",
    "cantidad_propiedades": 13200,
    "precio_promedio_usd": 178000.0
  },
  {
    "fecha_scraping": "2024-03-15T00:00:00",
    "cantidad_propiedades": 12800,
    "precio_promedio_usd": 182000.0
  }
]
```

### Obtener Información del Modelo

```bash
curl http://127.0.0.1:8000/predict/model-info
```

### Explicar una Predicción (XAI)

Para entender qué factores influyen en una predicción específica, puede usar el endpoint `/explain`.

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/predict/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "barrio": "Palermo",
    "ambientes": 2,
    "superficie_total_m2": 50,
    "dormitorios": 1,
    "banos": 1,
    "cocheras": 0,
    "description": "Departamento luminoso en el corazón de Palermo."
  }'
```

**Response (Ejemplo):**
```json
{
  "base_value": 150000.0,
  "shap_values": [
    { "feature": "superficie_total_m2", "value": 45000.0 },
    { "feature": "barrio_Palermo", "value": 25000.0 }
  ],
  "prediction_usd": 221500.0
}
```

### **Tendencias Identificadas**
- **Precios en alza:** +4% en 3 meses
- **Oferta estable:** Cantidad de propiedades se mantiene
- **Factores clave:** Superficie (45%), ubicación (22%), ambientes (8%)

## **Scripts de Automatización**

### **Script de Análisis Completo**
```python
#!/usr/bin/env python3
import requests
import json
import pandas as pd

def analisis_completo_propiedad(barrio, ambientes, dormitorios, banos, superficie, cocheras, description=""):
    """Análisis completo de una propiedad, incluyendo descripción."""
    
    # 1. Predicción del modelo
    prediction_data = {
        "barrio": barrio,
        "ambientes": ambientes,
        "dormitorios": dormitorios,
        "banos": banos,
        "superficie_total_m2": superficie,
        "cocheras": cocheras,
        "description": description
    }
    
    response = requests.post("http://127.0.0.1:8000/predict/", json=prediction_data)
    prediction = response.json()
    
    # 2. Estadísticas del barrio
    response = requests.get("http://127.0.0.1:8000/estadisticas/precio-por-barrio/")
    estadisticas = response.json()
    barrio_stats = next((b for b in estadisticas if b['barrio'] == barrio), None)
    
    # 3. Propiedades similares
    response = requests.get(f"http://127.0.0.1:8000/propiedades/?barrio={barrio}&ambientes_min={ambientes-1}&ambientes_max={ambientes+1}")
    similares = response.json()
    
    # 4. Generar reporte
    reporte = {
        "propiedad": prediction_data,
        "prediccion": prediction,
        "estadisticas_barrio": barrio_stats,
        "propiedades_similares": len(similares),
        "recomendacion": generar_recomendacion(prediction, barrio_stats)
    }
    
    return reporte

def generar_recomendacion(prediction, barrio_stats):
    """Genera recomendación basada en el análisis"""
    precio_pred = prediction['predicted_price_usd']
    precio_prom_barrio = barrio_stats['precio_promedio_usd']
    
    if precio_pred < precio_prom_barrio * 0.9:
        return "OPORTUNIDAD: Precio por debajo del promedio del barrio"
    elif precio_pred > precio_prom_barrio * 1.1:
        return "CARO: Precio por encima del promedio del barrio"
    else:
        return "JUSTO: Precio alineado con el mercado del barrio"

# Ejemplo de uso
if __name__ == "__main__":
    resultado = analisis_completo_propiedad("Palermo", 3, 2, 2, 80, 1, "Balcón con parrilla, muy luminoso.")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
```

## **Enlaces Relacionados**

- **[Referencia de API](referencia-api.md)** - Documentación completa de endpoints
- **[Modelo de ML](modelo-ml.md)** - Detalles técnicos del modelo
- **[Visualizaciones](visualizaciones.md)** - Gráficos y análisis visual
- **[Inicio Rápido](inicio-rapido.md)** - Configuración inicial
